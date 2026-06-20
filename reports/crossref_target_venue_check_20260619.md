# Crossref Target Venue Check - 2026-06-19

## Purpose

Check whether `ACS Applied Materials & Interfaces` and `Materials & Design` are represented in the current dataset and whether they can be collected through Crossref without using OpenAlex as a paper discovery source.

## Current Dataset Check

Source files checked:

- `data/papers.json`
- `data/archive_papers.json`

Results:

| Venue | Active papers | Archived papers | Notes |
|---|---:|---:|---|
| ACS Applied Materials & Interfaces | 1 | 0 | Stored as `ACS Applied Materials &amp; Interfaces` in Crossref metadata. |
| Materials & Design | 11 | 0 | Stored as `Materials &amp; Design` in Crossref metadata. |

Existing ACS AMI record:

- `Scalable Accelerated Materials Discovery of Sustainable Polysaccharide-Based Hydrogels by Autonomous Experimentation and Collaborative Learning`
- DOI: `10.1021/acsami.4c16614`
- Year: 2024

Example existing Materials & Design records:

- `An efficient closed-loop design framework for additive manufacturing of multiphysical metamaterials`, DOI `10.1016/j.matdes.2026.115961`
- `Topology optimization of 3D-printed material architectures: Testing toolpath consideration in design`, DOI `10.1016/j.matdes.2025.114700`
- `Residual stress control in large-format additive manufacturing of polylactic acid via a digital twin and in-operando imaging`, DOI `10.1016/j.matdes.2025.114870`

## Crossref Coverage Check

Crossref journal lookup by exact title query was unreliable for these names, but ISSN lookup worked.

| Venue | Crossref ISSN lookup | ISSN used |
|---|---|---|
| ACS Applied Materials & Interfaces | Found | `1944-8244`, `1944-8252` |
| Materials & Design | Found | `0264-1275` |

Manual Crossref works probes using `filter=from-pub-date:2024-01-01,issn:<ISSN>` and `query.bibliographic=additive manufacturing` returned relevant records from both venues.

Example Crossref probe hits:

- ACS AMI: `Metal-Organic Decomposition for Additive Manufacturing of Extreme Environment Electronics`, DOI `10.1021/acsami.5c03450`
- ACS AMI: `Emerging Trends in Additive Manufacturing for Thermoelectric Devices: Materials, Structures, and Engineering Approaches`, DOI `10.1021/acsami.6c04499`
- Materials & Design: `Overcoming the challenges of fusion-based brass additive manufacturing through solid-state additive friction-stir deposition`, DOI `10.1016/j.matdes.2025.114756`
- Materials & Design: `Generative design strategies for additive manufacturing of lattice structures: A review`, DOI `10.1016/j.matdes.2026.115431`

## Implemented Fix

Added Crossref ISSN-targeted venue search:

- Config: `data/crossref_venue_queries.json`
- Fetcher: `fetch_crossref_by_issn_query()` in `scripts/fetch_crossref.py`
- Collector: `_collect_crossref_venue_candidates()` in `scripts/full_rebuild_crossref_dataset.py`

This keeps paper discovery Crossref-only. OpenAlex is still only used for DOI-based missing corresponding-author completion after Crossref has found the paper.

## Safety

- Venue-targeted Crossref search uses ISSN filters, not publisher crawling.
- No PDFs are downloaded or stored.
- Raw abstracts are not displayed.
- `CROSSREF_VENUE_MAX_PAGES` defaults to `1` so broad venue queries do not run unbounded during local execution.
