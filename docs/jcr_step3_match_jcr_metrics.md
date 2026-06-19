# JCR Step 3: Match JCR Metrics

## Purpose

This step matches the local journal candidate list from Step 1 against a
manually exported Journal Citation Reports CSV file and creates journal metrics
JSON files that the website can consume.

This step uses only local files. It does not scrape or query Web of Science,
Journal Citation Reports, Clarivate, Crossref, OpenAlex, publisher sites, or any
external API.

## Inputs

Local journal list from Step 1:

```bash
data/private/journals_to_match_jcr.csv
```

Manual JCR CSV export:

```bash
data/private/jcr_export_original_2025.csv
```

The script also tolerates an accidental double-extension file named
`data/private/jcr_export_original_2025.csv.csv` if the expected file is absent.

Expected JCR columns:

- `Journal name`
- `JCR Abbreviation`
- `Publisher`
- `ISSN`
- `eISSN`
- `Category`
- `Edition`
- `Total Citations`
- `2025 JIF`
- `JIF Quartile`
- `2025 JCI`
- `5 Year JIF Quartile`
- `JIF Rank`
- `5 Year JIF`

The current script treats this as `jcr_year = 2025`.

## How To Run

Default:

```bash
python scripts/match_jcr_metrics.py
```

Explicit paths:

```bash
python scripts/match_jcr_metrics.py \
  --journals data/private/journals_to_match_jcr.csv \
  --jcr data/private/jcr_export_original_2025.csv \
  --year 2025
```

Folder input is also supported:

```bash
python scripts/match_jcr_metrics.py \
  --journals data/private/journals_to_match_jcr.csv \
  --jcr-dir data/private/jcr_exports \
  --year 2025
```

## Matching Method

Matching priority:

1. ISSN/eISSN set intersection
2. normalized journal name exact match
3. normalized JCR abbreviation exact match
4. fuzzy journal name match with Python standard-library `difflib`
5. manual review / not found

Match method labels:

- `issn_exact`
- `eissn_exact`
- `issn_cross`
- `journal_name_exact`
- `jcr_abbreviation_exact`
- `journal_name_fuzzy`
- `ambiguous`
- `not_found`

Confidence values:

- ISSN/eISSN match: `1.00`
- journal-name exact match: `0.95`
- JCR abbreviation exact match: `0.90`
- fuzzy match: normalized fuzzy score, capped at `0.94`
- ambiguous: `0.50`
- not found: `0.00`

## Multiple Categories

JCR can export multiple rows for one journal because the journal may belong to
multiple categories. The script groups those rows by journal identity and
preserves all category records in `categories`.

For each matched journal:

- `best_quartile` is the best quartile across all categories, where Q1 is best.
- `selected_category` is the category with the best quartile.
- ties are resolved by stable sorted category name.
- `has_multiple_categories` is true when more than one category row exists.

## Outputs

Public outputs:

- `data/journal_metrics.json`
- `public/data/journal_metrics.json`

Private/debug outputs:

- `data/private/jcr_matched_debug.csv`
- `data/private/jcr_matched_debug.json`
- `data/private/jcr_manual_review.csv`

The private outputs and original JCR export are ignored by Git. The public JSON
files are intended to be committed because the website can use them.

## Manual Review

Review:

```bash
data/private/jcr_manual_review.csv
```

Rows appear here when:

- no match is found
- multiple JCR journal groups match
- fuzzy match is below the high-confidence threshold
- the local journal has no ISSN/eISSN and name matching was used
- the local venue looks like a repository, archive, conference, or non-journal
- JIF or quartile is missing
- the local/JCR title similarity is suspiciously low

The manual review CSV includes blank columns such as `manual_jcr_journal`,
`manual_issn`, `manual_jif`, and `manual_note` for later human correction.

## Website Use

The website can load:

```bash
public/data/journal_metrics.json
```

Each public object includes journal identity, JCR journal title, JIF, quartile,
selected category, all JCR category rows, match method, confidence, and
`manual_review_required`.

The public JSON intentionally excludes raw JCR rows, local file paths, debug
notes, and private review notes.
