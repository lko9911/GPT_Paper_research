"""Match local journal candidates to a local JCR CSV export.

Step 3 of the JCR workflow. This script reads only local files, preserves
multiple JCR category rows, and writes public journal metrics JSON plus private
debug/review files. It does not scrape or query any external service.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
from difflib import SequenceMatcher
from html import unescape
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JOURNALS = ROOT / "data" / "private" / "journals_to_match_jcr.csv"
DEFAULT_JCR = ROOT / "data" / "private" / "jcr_export_original_2025.csv"
DEFAULT_PRIVATE_DEBUG_CSV = ROOT / "data" / "private" / "jcr_matched_debug.csv"
DEFAULT_PRIVATE_DEBUG_JSON = ROOT / "data" / "private" / "jcr_matched_debug.json"
DEFAULT_MANUAL_REVIEW_CSV = ROOT / "data" / "private" / "jcr_manual_review.csv"
DEFAULT_PUBLIC_JSON = ROOT / "data" / "journal_metrics.json"
DEFAULT_PUBLIC_COPY_JSON = ROOT / "public" / "data" / "journal_metrics.json"

JCR_COLUMN_MAP = {
    "Journal name": "jcr_journal",
    "JCR Abbreviation": "jcr_abbreviation",
    "Publisher": "publisher",
    "ISSN": "jcr_issn",
    "eISSN": "jcr_eissn",
    "Category": "jcr_category",
    "Edition": "edition",
    "Total Citations": "total_citations",
    "2025 JIF": "jif",
    "JIF Quartile": "jif_quartile",
    "2025 JCI": "jci",
    "5 Year JIF Quartile": "five_year_jif_quartile",
    "JIF Rank": "jif_rank",
    "5 Year JIF": "five_year_jif",
}

DEBUG_FIELDS = [
    "journal_id",
    "journal_original",
    "journal_normalized",
    "issn",
    "eissn",
    "all_issns",
    "paper_count",
    "jcr_journal",
    "jcr_abbreviation",
    "jcr_issn",
    "jcr_eissn",
    "publisher",
    "jcr_year",
    "jif",
    "best_quartile",
    "selected_category",
    "selected_quartile",
    "jif_rank",
    "match_method",
    "match_confidence",
    "manual_review_required",
    "review_note",
    "example_title",
    "example_doi",
]

MANUAL_EXTRA_FIELDS = [
    "manual_jcr_journal",
    "manual_issn",
    "manual_eissn",
    "manual_jif",
    "manual_quartile",
    "manual_category",
    "manual_note",
]

NON_JOURNAL_MARKERS = [
    "arxiv",
    "ssrn",
    "research square",
    "chemrxiv",
    "techrxiv",
    "zenodo",
    "figshare",
    "repository",
    "proceedings",
    "conference",
    "dissertation",
    "thesis",
    "preprint",
]

MISSING_VALUES = {"", "n/a", "na", "null", "none", "-"}


@dataclass
class JcrGroup:
    group_id: str
    jcr_journal: str
    jcr_abbreviation: str
    publisher: str
    jcr_issn: str
    jcr_eissn: str
    all_issns: set[str]
    name_normalized: str
    abbreviation_normalized: str
    rows: list[dict[str, str]]


def main() -> None:
    parser = argparse.ArgumentParser(description="Match local journal list to a manually exported JCR CSV.")
    parser.add_argument("--journals", default=str(DEFAULT_JOURNALS), help="Step 1 journal CSV path.")
    parser.add_argument("--jcr", default=str(DEFAULT_JCR), help="Manual JCR CSV export path.")
    parser.add_argument("--jcr-dir", default="", help="Optional directory containing JCR CSV exports.")
    parser.add_argument("--year", default="2025", help="JCR year.")
    parser.add_argument("--public-output", default=str(DEFAULT_PUBLIC_JSON), help="Public metrics JSON path.")
    parser.add_argument("--public-copy-output", default=str(DEFAULT_PUBLIC_COPY_JSON), help="Second public metrics JSON path.")
    parser.add_argument("--debug-csv", default=str(DEFAULT_PRIVATE_DEBUG_CSV), help="Private debug CSV path.")
    parser.add_argument("--debug-json", default=str(DEFAULT_PRIVATE_DEBUG_JSON), help="Private debug JSON path.")
    parser.add_argument("--manual-review", default=str(DEFAULT_MANUAL_REVIEW_CSV), help="Private manual review CSV path.")
    args = parser.parse_args()

    journal_path = resolve_path(args.journals)
    jcr_paths = resolve_jcr_paths(args.jcr, args.jcr_dir)
    year = int(args.year)
    updated_at = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    local_journals = load_csv(journal_path)
    jcr_rows = []
    for path in jcr_paths:
        jcr_rows.extend(load_jcr_csv(path, year))

    groups = build_jcr_groups(jcr_rows)
    indexes = build_indexes(groups)
    matched = [match_local_journal(row, groups, indexes, year, updated_at) for row in local_journals]

    public_rows = [item["public"] for item in matched]
    debug_rows = [item["debug"] for item in matched]
    manual_rows = [
        {**item["debug"], **{field: "" for field in MANUAL_EXTRA_FIELDS}}
        for item in matched
        if item["debug"]["manual_review_required"] == "true"
    ]

    write_json(resolve_path(args.public_output), public_rows)
    write_json(resolve_path(args.public_copy_output), public_rows)
    write_csv(resolve_path(args.debug_csv), debug_rows, DEBUG_FIELDS)
    write_json(resolve_path(args.debug_json), debug_rows)
    write_csv(resolve_path(args.manual_review), manual_rows, DEBUG_FIELDS + MANUAL_EXTRA_FIELDS)

    print(f"Total local journals loaded: {len(local_journals)}")
    print(f"Total JCR rows loaded: {len(jcr_rows)}")
    print(f"Total matched journals: {sum(1 for row in debug_rows if row['match_method'] not in {'not_found', 'ambiguous'})}")
    print(f"Matched by ISSN/eISSN: {sum(1 for row in debug_rows if row['match_method'] in {'issn_exact', 'eissn_exact', 'issn_cross'})}")
    print(f"Matched by exact journal name: {sum(1 for row in debug_rows if row['match_method'] in {'journal_name_exact', 'jcr_abbreviation_exact'})}")
    print(f"Matched by fuzzy journal name: {sum(1 for row in debug_rows if row['match_method'] == 'journal_name_fuzzy')}")
    print(f"Not found: {sum(1 for row in debug_rows if row['match_method'] == 'not_found')}")
    print(f"Manual review count: {len(manual_rows)}")
    print(f"Public output path: {resolve_path(args.public_output)}")
    print(f"Private debug output path: {resolve_path(args.debug_csv)}")
    print(f"Manual review output path: {resolve_path(args.manual_review)}")


def resolve_jcr_paths(jcr: str, jcr_dir: str) -> list[Path]:
    if jcr_dir:
        directory = resolve_path(jcr_dir)
        if not directory.exists():
            raise FileNotFoundError(f"JCR directory does not exist: {directory}")
        paths = sorted(directory.glob("*.csv"))
        if not paths:
            raise FileNotFoundError(f"No CSV files found in JCR directory: {directory}")
        return paths

    path = resolve_path(jcr)
    if path.exists():
        return [path]
    accidental_double_csv = Path(str(path) + ".csv")
    if accidental_double_csv.exists():
        return [accidental_double_csv]
    raise FileNotFoundError(f"JCR export CSV does not exist: {path}")


def load_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"CSV does not exist: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def load_jcr_csv(path: Path, year: int) -> list[dict[str, str]]:
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    header_index = None
    for index, line in enumerate(lines):
        cells = next(csv.reader([line])) if line.strip() else []
        if "Journal name" in cells and "JIF Quartile" in cells:
            header_index = index
            break
    if header_index is None:
        raise ValueError(f"Could not find JCR header row in {path}")
    reader = csv.DictReader(lines[header_index:])
    rows = []
    for row in reader:
        if not row or not row.get("Journal name"):
            continue
        normalized = {internal: clean_cell(row.get(source, "")) for source, internal in JCR_COLUMN_MAP.items()}
        normalized["jcr_year"] = str(year)
        rows.append(normalized)
    return rows


def build_jcr_groups(rows: list[dict[str, str]]) -> list[JcrGroup]:
    groups: dict[str, JcrGroup] = {}
    for row in rows:
        issns = collect_jcr_issns(row)
        normalized_name = normalize_journal_name(row.get("jcr_journal", ""))
        normalized_abbrev = normalize_journal_name(row.get("jcr_abbreviation", ""))
        key = f"issn:{sorted(issns)[0]}" if issns else f"name:{normalized_name}"
        group = groups.get(key)
        if group is None:
            group = JcrGroup(
                group_id=key,
                jcr_journal=row.get("jcr_journal", ""),
                jcr_abbreviation=row.get("jcr_abbreviation", ""),
                publisher=row.get("publisher", ""),
                jcr_issn=normalize_issn(row.get("jcr_issn", "")),
                jcr_eissn=normalize_issn(row.get("jcr_eissn", "")),
                all_issns=set(issns),
                name_normalized=normalized_name,
                abbreviation_normalized=normalized_abbrev,
                rows=[],
            )
            groups[key] = group
        group.rows.append(row)
        group.all_issns.update(issns)
        if not group.jcr_issn and normalize_issn(row.get("jcr_issn", "")):
            group.jcr_issn = normalize_issn(row.get("jcr_issn", ""))
        if not group.jcr_eissn and normalize_issn(row.get("jcr_eissn", "")):
            group.jcr_eissn = normalize_issn(row.get("jcr_eissn", ""))
    return list(groups.values())


def build_indexes(groups: list[JcrGroup]) -> dict[str, Any]:
    by_issn: dict[str, list[JcrGroup]] = defaultdict(list)
    by_name: dict[str, list[JcrGroup]] = defaultdict(list)
    by_abbrev: dict[str, list[JcrGroup]] = defaultdict(list)
    for group in groups:
        for issn in group.all_issns:
            by_issn[issn].append(group)
        if group.name_normalized:
            by_name[group.name_normalized].append(group)
        if group.abbreviation_normalized:
            by_abbrev[group.abbreviation_normalized].append(group)
    return {"by_issn": by_issn, "by_name": by_name, "by_abbrev": by_abbrev}


def match_local_journal(
    local: dict[str, str],
    groups: list[JcrGroup],
    indexes: dict[str, Any],
    year: int,
    updated_at: str,
) -> dict[str, dict[str, Any]]:
    local_issns = collect_local_issns(local)
    local_print = normalize_issn(local.get("issn", ""))
    local_e = normalize_issn(local.get("eissn", ""))
    local_name = local.get("journal_normalized") or normalize_journal_name(local.get("journal_original", ""))

    matched_group, method, confidence, candidate_count = find_match(local, local_issns, local_print, local_e, local_name, groups, indexes)
    notes = review_notes(local, matched_group, method, confidence, candidate_count, local_issns, local_name)
    category_info = select_categories(matched_group.rows if matched_group else [])
    manual_review = bool(notes)

    public = public_metric(local, matched_group, category_info, method, confidence, manual_review, year, updated_at)
    debug = debug_metric(local, matched_group, category_info, method, confidence, manual_review, notes, year)
    return {"public": public, "debug": debug}


def find_match(
    local: dict[str, str],
    local_issns: set[str],
    local_print: str,
    local_e: str,
    local_name: str,
    groups: list[JcrGroup],
    indexes: dict[str, Any],
) -> tuple[JcrGroup | None, str, float, int]:
    candidates = unique_groups([group for issn in local_issns for group in indexes["by_issn"].get(issn, [])])
    if candidates:
        method = issn_match_method(candidates[0], local_print, local_e)
        return single_or_ambiguous(candidates, method, 1.0)

    if local_name and local_name in indexes["by_name"]:
        return single_or_ambiguous(indexes["by_name"][local_name], "journal_name_exact", 0.95)

    if local_name and local_name in indexes["by_abbrev"]:
        return single_or_ambiguous(indexes["by_abbrev"][local_name], "jcr_abbreviation_exact", 0.90)

    fuzzy_group, score = best_fuzzy_match(local_name, groups)
    if fuzzy_group and score >= 0.85:
        return fuzzy_group, "journal_name_fuzzy", min(score, 0.94), 1
    return None, "not_found", 0.0, 0


def single_or_ambiguous(candidates: list[JcrGroup], method: str, confidence: float) -> tuple[JcrGroup | None, str, float, int]:
    candidates = unique_groups(candidates)
    if len(candidates) == 1:
        return candidates[0], method, confidence, 1
    return candidates[0] if candidates else None, "ambiguous", 0.50, len(candidates)


def unique_groups(candidates: list[JcrGroup]) -> list[JcrGroup]:
    seen = set()
    unique = []
    for group in candidates:
        if group.group_id in seen:
            continue
        seen.add(group.group_id)
        unique.append(group)
    return unique


def issn_match_method(group: JcrGroup, local_print: str, local_e: str) -> str:
    if local_print and local_print == group.jcr_issn:
        return "issn_exact"
    if local_e and local_e == group.jcr_eissn:
        return "eissn_exact"
    return "issn_cross"


def best_fuzzy_match(local_name: str, groups: list[JcrGroup]) -> tuple[JcrGroup | None, float]:
    if not local_name:
        return None, 0.0
    best_group = None
    best_score = 0.0
    for group in groups:
        for candidate in (group.name_normalized, group.abbreviation_normalized):
            if not candidate:
                continue
            score = SequenceMatcher(None, local_name, candidate).ratio()
            if score > best_score:
                best_group = group
                best_score = score
    if best_score < 0.85:
        return None, best_score
    return best_group, best_score


def select_categories(rows: list[dict[str, str]]) -> dict[str, Any]:
    categories = []
    for row in rows:
        categories.append(
            {
                "category": row.get("jcr_category", ""),
                "quartile": normalize_quartile(row.get("jif_quartile", "")),
                "rank": row.get("jif_rank", ""),
                "edition": row.get("edition", ""),
                "jif": row.get("jif", ""),
                "jci": row.get("jci", ""),
                "five_year_jif": row.get("five_year_jif", ""),
                "five_year_jif_quartile": normalize_quartile(row.get("five_year_jif_quartile", "")),
            }
        )
    categories.sort(key=lambda item: (quartile_rank(item["quartile"]), item["category"]))
    selected = categories[0] if categories else {}
    return {
        "categories": categories,
        "best_quartile": selected.get("quartile", ""),
        "selected_category": selected.get("category", ""),
        "selected_quartile": selected.get("quartile", ""),
        "selected_rank": selected.get("rank", ""),
        "has_multiple_categories": len(categories) > 1,
    }


def public_metric(
    local: dict[str, str],
    group: JcrGroup | None,
    category_info: dict[str, Any],
    method: str,
    confidence: float,
    manual_review: bool,
    year: int,
    updated_at: str,
) -> dict[str, Any]:
    selected = category_info["categories"][0] if category_info["categories"] else {}
    return {
        "journal_id": local.get("journal_id", ""),
        "journal": local.get("journal_original", ""),
        "journal_normalized": local.get("journal_normalized", ""),
        "issn": local.get("issn", ""),
        "eissn": local.get("eissn", ""),
        "all_issns": local.get("all_issns", ""),
        "jcr_journal": group.jcr_journal if group else "",
        "jcr_abbreviation": group.jcr_abbreviation if group else "",
        "publisher": group.publisher if group else "",
        "jcr_year": year,
        "jif": selected.get("jif", ""),
        "jif_quartile": selected.get("quartile", ""),
        "best_quartile": category_info["best_quartile"],
        "selected_category": category_info["selected_category"],
        "selected_quartile": category_info["selected_quartile"],
        "selected_rank": category_info["selected_rank"],
        "total_citations": group.rows[0].get("total_citations", "") if group and group.rows else "",
        "jci": selected.get("jci", ""),
        "five_year_jif": selected.get("five_year_jif", ""),
        "five_year_jif_quartile": selected.get("five_year_jif_quartile", ""),
        "categories": category_info["categories"],
        "has_multiple_categories": category_info["has_multiple_categories"],
        "match_method": method,
        "match_confidence": round(confidence, 3),
        "manual_review_required": manual_review,
        "updated_at": updated_at,
    }


def debug_metric(
    local: dict[str, str],
    group: JcrGroup | None,
    category_info: dict[str, Any],
    method: str,
    confidence: float,
    manual_review: bool,
    notes: list[str],
    year: int,
) -> dict[str, str]:
    selected = category_info["categories"][0] if category_info["categories"] else {}
    return {
        "journal_id": local.get("journal_id", ""),
        "journal_original": local.get("journal_original", ""),
        "journal_normalized": local.get("journal_normalized", ""),
        "issn": local.get("issn", ""),
        "eissn": local.get("eissn", ""),
        "all_issns": local.get("all_issns", ""),
        "paper_count": local.get("paper_count", ""),
        "jcr_journal": group.jcr_journal if group else "",
        "jcr_abbreviation": group.jcr_abbreviation if group else "",
        "jcr_issn": group.jcr_issn if group else "",
        "jcr_eissn": group.jcr_eissn if group else "",
        "publisher": group.publisher if group else "",
        "jcr_year": str(year),
        "jif": selected.get("jif", ""),
        "best_quartile": category_info["best_quartile"],
        "selected_category": category_info["selected_category"],
        "selected_quartile": category_info["selected_quartile"],
        "jif_rank": selected.get("rank", ""),
        "match_method": method,
        "match_confidence": f"{confidence:.3f}",
        "manual_review_required": "true" if manual_review else "false",
        "review_note": "; ".join(notes),
        "example_title": local.get("example_title", ""),
        "example_doi": local.get("example_doi", ""),
    }


def review_notes(
    local: dict[str, str],
    group: JcrGroup | None,
    method: str,
    confidence: float,
    candidate_count: int,
    local_issns: set[str],
    local_name: str,
) -> list[str]:
    notes = []
    local_existing_note = clean_cell(local.get("review_note", ""))
    if local_existing_note:
        notes.append(f"local step1: {local_existing_note}")
    if method == "not_found":
        notes.append("no JCR match found")
    if method == "ambiguous" or candidate_count > 1:
        notes.append("multiple possible JCR journal groups match")
    if method == "journal_name_fuzzy" and confidence < 0.94:
        notes.append("fuzzy match below high-confidence threshold")
    if method in {"journal_name_exact", "jcr_abbreviation_exact", "journal_name_fuzzy"} and not local_issns:
        notes.append("local journal has no ISSN/eISSN and used name matching")
    if appears_non_journal(local_name):
        notes.append("local venue appears to be repository, archive, conference, or non-journal source")
    if group:
        category_info = select_categories(group.rows)
        selected = category_info["categories"][0] if category_info["categories"] else {}
        if not selected.get("jif") or not selected.get("quartile"):
            notes.append("JIF or JIF quartile missing")
        mismatch = title_mismatch(local_name, group.name_normalized)
        if mismatch:
            notes.append("large title mismatch")
    return dedupe_preserve_order(notes)


def title_mismatch(left: str, right: str) -> bool:
    if not left or not right:
        return False
    if left == right:
        return False
    return SequenceMatcher(None, left, right).ratio() < 0.70


def collect_local_issns(row: dict[str, str]) -> set[str]:
    values = [row.get("issn", ""), row.get("eissn", ""), row.get("all_issns", "")]
    result = set()
    for value in values:
        result.update(find_issns(value))
    return result


def collect_jcr_issns(row: dict[str, str]) -> set[str]:
    return set().union(find_issns(row.get("jcr_issn", "")), find_issns(row.get("jcr_eissn", "")))


def find_issns(value: Any) -> set[str]:
    if value is None:
        return set()
    text = str(value)
    if clean_cell(text).lower() in MISSING_VALUES:
        return set()
    matches = re.findall(r"\b([0-9]{4})-?([0-9]{3}[0-9Xx])\b", text)
    return {f"{left}-{right.upper()}" for left, right in matches if valid_issn(left + right)}


def normalize_issn(value: Any) -> str:
    values = sorted(find_issns(value))
    return values[0] if values else ""


def valid_issn(value: str) -> bool:
    clean = value.replace("-", "").upper()
    if not re.fullmatch(r"[0-9]{7}[0-9X]", clean):
        return False
    total = 0
    for index, char in enumerate(clean):
        digit = 10 if char == "X" else int(char)
        total += digit * (8 - index)
    return total % 11 == 0


def normalize_journal_name(value: Any) -> str:
    text = clean_cell(value).lower()
    text = re.sub(r"[\u2010-\u2015]", "-", text)
    text = re.sub(r"[’`]", "'", text)
    text = re.sub(r"\s*&\s*", " and ", text)
    text = re.sub(r"\band\b", " and ", text)
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"[\s,;:/.-]+$", "", text).strip()
    text = re.sub(r"(?<=[a-z]{3})\.(?=\s|$)", "", text)
    return text


def clean_cell(value: Any) -> str:
    text = unescape(str(value or ""))
    text = re.sub(r"\s+", " ", text).strip()
    return "" if text.lower() in MISSING_VALUES else text


def normalize_quartile(value: Any) -> str:
    text = clean_cell(value).upper()
    return text if text in {"Q1", "Q2", "Q3", "Q4"} else ""


def quartile_rank(value: str) -> int:
    return {"Q1": 1, "Q2": 2, "Q3": 3, "Q4": 4}.get(value, 9)


def appears_non_journal(name: str) -> bool:
    return any(marker in name for marker in NON_JOURNAL_MARKERS)


def dedupe_preserve_order(values: list[str]) -> list[str]:
    seen = set()
    output = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        output.append(value)
    return output


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def resolve_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


if __name__ == "__main__":
    main()
