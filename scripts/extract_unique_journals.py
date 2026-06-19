"""Extract unique journal candidates from local paper metadata.

Step 1 for a later manual JCR matching workflow. This script only reads local
JSON/CSV paper data and writes a private journal list. It does not call any
external APIs and does not perform JCR matching.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from html import unescape
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data" / "papers.json"
DEFAULT_OUTPUT = ROOT / "data" / "private" / "journals_to_match_jcr.csv"
DEFAULT_JSON_OUTPUT = ROOT / "data" / "private" / "journals_to_match_jcr.json"

JOURNAL_FIELDS = [
    "journal",
    "venue",
    "container-title",
    "container_title",
    "publication",
    "source_title",
    "sourceTitle",
    "journal_name",
]

ISSN_FIELDS = ["issn", "ISSN", "print_issn", "printISSN", "pissn"]
EISSN_FIELDS = ["eissn", "eISSN", "EISSN", "electronic_issn", "electronicISSN", "issn_l", "ISSN-L"]
GENERIC_ISSN_FIELDS = ["all_issns", "issns"]

OUTPUT_FIELDS = [
    "journal_id",
    "journal_original",
    "journal_normalized",
    "issn",
    "eissn",
    "all_issns",
    "paper_count",
    "example_doi",
    "example_title",
    "example_year",
    "source_fields",
    "manual_review_required",
    "review_note",
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


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract unique journals for later manual JCR matching.")
    parser.add_argument("--input", default=str(DEFAULT_INPUT), help="Input paper JSON or CSV path.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Output journal CSV path.")
    parser.add_argument(
        "--json-output",
        default=str(DEFAULT_JSON_OUTPUT),
        help="Optional JSON output path. Pass an empty string to skip JSON output.",
    )
    args = parser.parse_args()

    input_path = _resolve_path(args.input)
    output_path = _resolve_path(args.output)
    json_output_path = _resolve_path(args.json_output) if args.json_output else None

    records = load_records(input_path)
    rows = extract_unique_journals(records)
    write_csv(output_path, rows)
    if json_output_path:
        write_json(json_output_path, rows)

    with_issn = sum(1 for row in rows if row["all_issns"])
    missing_issn = len(rows) - with_issn
    manual_review = sum(1 for row in rows if row["manual_review_required"] == "true")

    print(f"Input paper data path: {input_path}")
    print(f"Total papers read: {len(records)}")
    print(f"Total unique journals extracted: {len(rows)}")
    print(f"Journals with ISSN/eISSN: {with_issn}")
    print(f"Journals missing ISSN/eISSN: {missing_issn}")
    print(f"Journals requiring manual review: {manual_review}")
    print(f"Output CSV path: {output_path}")
    if json_output_path:
        print(f"Output JSON path: {json_output_path}")


def load_records(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"Input file does not exist: {path}")
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            for key in ("papers", "items", "records", "data"):
                if isinstance(data.get(key), list):
                    data = data[key]
                    break
        if not isinstance(data, list):
            raise ValueError(f"JSON input must contain a list of records: {path}")
        return [record for record in data if isinstance(record, dict)]
    if path.suffix.lower() == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return [dict(row) for row in csv.DictReader(handle)]
    raise ValueError(f"Unsupported input format: {path.suffix}. Use JSON or CSV.")


def extract_unique_journals(records: list[dict[str, Any]]) -> list[dict[str, str]]:
    groups: dict[str, dict[str, Any]] = {}
    missing_group = _new_group("missing-journal", "", "", "", "", "missing_journal")

    for record in records:
        journal, journal_field = find_journal(record)
        normalized = normalize_journal_name(journal)
        issn_values, eissn_values, all_issn_values = collect_issns(record)
        group_key = f"issn:{sorted(all_issn_values)[0]}" if all_issn_values else f"name:{normalized}"
        if not normalized:
            group_key = "missing-journal"

        group = missing_group if group_key == "missing-journal" else groups.setdefault(
            group_key,
            _new_group(group_key, journal, normalized, record.get("doi", ""), record.get("title", ""), journal_field),
        )
        update_group(group, record, journal, normalized, issn_values, eissn_values, all_issn_values, journal_field)

    if missing_group["paper_count"]:
        groups[missing_group["journal_id"]] = missing_group

    rows = [finalize_group(group) for group in groups.values()]
    rows.sort(key=lambda row: (-int(row["paper_count"]), row["journal_normalized"], row["journal_original"]))
    return rows


def _new_group(
    key: str,
    journal: str,
    normalized: str,
    example_doi: Any,
    example_title: Any,
    source_field: str,
) -> dict[str, Any]:
    return {
        "key": key,
        "journal_id": "",
        "journal_names": Counter(),
        "normalized_names": Counter(),
        "issns": set(),
        "print_issns": set(),
        "eissns": set(),
        "paper_count": 0,
        "example_doi": str(example_doi or ""),
        "example_title": str(example_title or ""),
        "example_year": "",
        "source_fields": Counter(),
        "review_notes": set(),
        "first_journal": journal,
        "first_normalized": normalized,
    } | ({"source_fields": Counter([source_field])} if source_field else {})


def update_group(
    group: dict[str, Any],
    record: dict[str, Any],
    journal: str,
    normalized: str,
    issns: set[str],
    eissns: set[str],
    all_issns: set[str],
    source_field: str,
) -> None:
    group["paper_count"] += 1
    if journal:
        group["journal_names"][journal] += 1
    if normalized:
        group["normalized_names"][normalized] += 1
    group["print_issns"].update(issns)
    group["eissns"].update(eissns)
    group["issns"].update(all_issns)
    if source_field:
        group["source_fields"][source_field] += 1
    if not group["example_doi"] and record.get("doi"):
        group["example_doi"] = str(record.get("doi") or "")
    if not group["example_title"] and record.get("title"):
        group["example_title"] = str(record.get("title") or "")
    if not group["example_year"] and record.get("year"):
        group["example_year"] = str(record.get("year") or "")

    if not journal:
        group["review_notes"].add("missing journal name")
    if not all_issns:
        group["review_notes"].add("missing ISSN/eISSN")
    if normalized and is_ambiguous_journal_name(normalized):
        group["review_notes"].add("journal name is short or ambiguous")
    if appears_non_journal(normalized):
        group["review_notes"].add("venue may be repository, conference, archive, or non-journal source")


def finalize_group(group: dict[str, Any]) -> dict[str, str]:
    names = group["journal_names"]
    normalized_names = group["normalized_names"]
    issns = sorted(group["issns"])
    print_issns = sorted(group["print_issns"])
    eissns = sorted(group["eissns"])
    if names:
        journal_original = choose_best_name(names)
    else:
        journal_original = group["first_journal"]
    journal_normalized = normalized_names.most_common(1)[0][0] if normalized_names else group["first_normalized"]

    if len(normalized_names) > 1 and names_are_very_different(normalized_names):
        group["review_notes"].add("multiple different journal names share the same ISSN")

    issn = print_issns[0] if print_issns else ""
    eissn = eissns[0] if eissns else ""
    source_fields = "; ".join(name for name, _ in group["source_fields"].most_common())
    notes = sorted(group["review_notes"])
    manual_review = bool(notes)
    journal_id = make_journal_id(issns, journal_normalized or journal_original or group["key"])

    return {
        "journal_id": journal_id,
        "journal_original": journal_original,
        "journal_normalized": journal_normalized,
        "issn": issn,
        "eissn": eissn,
        "all_issns": "; ".join(issns),
        "paper_count": str(group["paper_count"]),
        "example_doi": group["example_doi"],
        "example_title": group["example_title"],
        "example_year": group["example_year"],
        "source_fields": source_fields,
        "manual_review_required": "true" if manual_review else "false",
        "review_note": "; ".join(notes),
    }


def find_journal(record: dict[str, Any]) -> tuple[str, str]:
    for field in JOURNAL_FIELDS:
        value = record.get(field)
        text = first_text(value)
        if text:
            return clean_original(text), field
    return "", ""


def collect_issns(record: dict[str, Any]) -> tuple[set[str], set[str], set[str]]:
    print_issns: set[str] = set()
    eissns: set[str] = set()
    generic_issns: set[str] = set()
    for field in ISSN_FIELDS:
        if field in record:
            print_issns.update(find_issn_values(record.get(field)))
    for field in EISSN_FIELDS:
        if field in record:
            eissns.update(find_issn_values(record.get(field)))
    for field in GENERIC_ISSN_FIELDS:
        if field in record:
            generic_issns.update(find_issn_values(record.get(field)))
    all_issns = set().union(print_issns, eissns, generic_issns)
    if not print_issns and generic_issns:
        print_issns.update(generic_issns)
    return print_issns, eissns, all_issns


def find_issn_values(value: Any) -> set[str]:
    if value is None:
        return set()
    if isinstance(value, list):
        result = set()
        for item in value:
            result.update(find_issn_values(item))
        return result
    if isinstance(value, dict):
        result = set()
        for item in value.values():
            result.update(find_issn_values(item))
        return result
    text = str(value)
    matches = re.findall(r"\b([0-9]{4})-?([0-9]{3}[0-9Xx])\b", text)
    return {f"{left}-{right.upper()}" for left, right in matches if valid_issn(f"{left}{right}")}


def valid_issn(value: str) -> bool:
    clean = value.replace("-", "").upper()
    if not re.fullmatch(r"[0-9]{7}[0-9X]", clean):
        return False
    total = 0
    for index, char in enumerate(clean):
        digit = 10 if char == "X" else int(char)
        total += digit * (8 - index)
    return total % 11 == 0


def normalize_journal_name(value: str) -> str:
    text = clean_original(value).lower()
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"[\s,;:/.-]+$", "", text).strip()
    text = re.sub(r"\s*&\s*", " and ", text)
    text = re.sub(r"\band\b", " and ", text)
    text = re.sub(r"\s+", " ", text).strip()
    text = remove_safe_periods(text)
    return text


def remove_safe_periods(text: str) -> str:
    # Keep abbreviation periods such as "J. Manuf." but remove periods between
    # ordinary full words only when this cannot merge initials.
    return re.sub(r"(?<=[a-z]{3})\.(?=\s|$)", "", text)


def clean_original(value: Any) -> str:
    text = unescape(str(value or ""))
    text = re.sub(r"\s+", " ", text).strip()
    return re.sub(r"[\s,;:/.-]+$", "", text).strip()


def first_text(value: Any) -> str:
    if isinstance(value, list):
        for item in value:
            text = first_text(item)
            if text:
                return text
        return ""
    if isinstance(value, dict):
        for key in ("title", "name", "value"):
            text = first_text(value.get(key))
            if text:
                return text
        return ""
    return str(value or "").strip()


def choose_best_name(names: Counter[str]) -> str:
    return sorted(names.items(), key=lambda item: (-item[1], len(item[0]), item[0].lower()))[0][0]


def names_are_very_different(names: Counter[str]) -> bool:
    normalized = list(names)
    if len(normalized) <= 1:
        return False
    tokens = [set(name.split()) for name in normalized]
    first = tokens[0]
    for token_set in tokens[1:]:
        overlap = len(first & token_set) / max(1, min(len(first), len(token_set)))
        if overlap < 0.5:
            return True
    return False


def is_ambiguous_journal_name(name: str) -> bool:
    if not name:
        return True
    if len(name) < 4:
        return True
    return name in {"unknown", "none", "journal", "proceedings"}


def appears_non_journal(name: str) -> bool:
    return any(marker in name for marker in NON_JOURNAL_MARKERS)


def make_journal_id(issns: list[str], fallback: str) -> str:
    if issns:
        return f"issn-{issns[0]}"
    digest = hashlib.sha1(fallback.encode("utf-8")).hexdigest()[:12]
    return f"name-{digest}"


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _resolve_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


if __name__ == "__main__":
    main()
