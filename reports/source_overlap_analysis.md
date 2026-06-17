# Source Overlap Analysis: OpenAlex vs Crossref
## Scope
- Analysis date: 2026-06-17 KST
- Curated records (`data/papers.json`): 1,357
- Archived/hidden records (`data/archive_papers.json`): 1,718
- Total records scanned: 3,075
- Site meta raw candidates: 3,075
- Last collection: 2026-06-16T21:47:55Z UTC / 2026-06-17 06:47 KST

## Method
- Each of the 3,075 collected candidate records was scanned.
- Paper-level grouping uses DOI as the primary key; if DOI is missing, a normalized title key is used.
- Source classes are based on the union of `source` values within each group: `OpenAlex only`, `Crossref only`, or `Both OpenAlex and Crossref`.
- Venue-level grouping uses normalized venue names and the union of sources observed for records in that venue.
- `Semantic Scholar` is not counted as a primary retrieval source for this comparison; this report focuses on OpenAlex and Crossref.

## Record-Level Counts: all 3,075 candidates
- openalex_only: 1,369
- crossref_only: 1,399
- both_openalex_crossref: 307
- other_or_unknown: 0

## Unique Paper Counts: DOI-first / title fallback
- openalex_only: 1,369
- crossref_only: 1,399
- both_openalex_crossref: 307
- other_or_unknown: 0
- Total unique paper keys: 3,075

## Venue Counts
- openalex_only: 428 venues
- crossref_only: 427 venues
- both_openalex_crossref: 211 venues
- other_or_unknown: 0 venues
- Total normalized venues: 1,066

## Top Venues By Source Class

### openalex_only
| Venue | Records | Unique paper keys | Curated | Archived | Sources |
|---|---:|---:|---:|---:|---|
| Zenodo (CERN European Organization for Nuclear Research) | 76 | 76 | 9 | 67 | OpenAlex |
| ArXiv.org | 48 | 48 | 12 | 36 | OpenAlex |
| arXiv (Cornell University) | 46 | 46 | 20 | 26 | OpenAlex |
| Figshare | 23 | 23 | 2 | 21 | OpenAlex |
| Open MIND | 12 | 12 | 9 | 3 | OpenAlex |
| Springer Link (Chiba Institute of Technology) | 9 | 9 | 4 | 5 | OpenAlex |
| Biomimetics | 8 | 8 | 4 | 4 | OpenAlex |
| Sensors | 7 | 7 | 3 | 4 | OpenAlex |
| ACS Applied Materials & Interfaces | 6 | 6 | 4 | 2 | OpenAlex |
| ACS Applied Polymer Materials | 5 | 5 | 5 | 0 | OpenAlex |
| Science | 5 | 5 | 4 | 1 | OpenAlex |
| ACS Polymers Au | 4 | 4 | 4 | 0 | OpenAlex |
| Materials & Design | 4 | 4 | 3 | 1 | OpenAlex |
| Nano-Micro Letters | 4 | 4 | 4 | 0 | OpenAlex |
| Sustainability | 4 | 4 | 0 | 4 | OpenAlex |
| VTechWorks (Virginia Tech) | 4 | 4 | 1 | 3 | OpenAlex |
| Bioengineering | 3 | 3 | 2 | 1 | OpenAlex |
| bioRxiv (Cold Spring Harbor Laboratory) | 3 | 3 | 3 | 0 | OpenAlex |
| Communications Materials | 3 | 3 | 1 | 2 | OpenAlex |
| Espace ÉTS (ETS) | 3 | 3 | 3 | 0 | OpenAlex |

### crossref_only
| Venue | Records | Unique paper keys | Curated | Archived | Sources |
|---|---:|---:|---:|---:|---|
| Multi-material Additive Manufacturing | 14 | 14 | 0 | 14 | Crossref |
| Manufacturing Letters | 13 | 13 | 2 | 11 | Crossref |
| Procedia CIRP | 13 | 13 | 4 | 9 | Crossref |
| 4D Printing of Composites | 11 | 11 | 0 | 11 | Crossref |
| Materials &amp; Design | 11 | 11 | 1 | 10 | Crossref |
| Generation and Update of a Digital Twin in a Process Plant | 10 | 10 | 0 | 10 | Crossref |
| Vat Photopolymerization Additive Manufacturing | 10 | 10 | 9 | 1 | Crossref |
| 4D Printing in Healthcare | 9 | 9 | 0 | 9 | Crossref |
| Computational Design and Robotic Fabrication | 9 | 9 | 9 | 0 | Crossref |
| International Journal of Computer Integrated Manufacturing | 9 | 9 | 2 | 7 | Crossref |
| Manufacturing Process Optimization for Sustainable Development Using Digital Twin Applications | 9 | 9 | 9 | 0 | Crossref |
| Smart Materials in Additive Manufacturing, Volume 3 | 7 | 7 | 1 | 6 | Crossref |
| SpringerBriefs in Energy | 7 | 7 | 0 | 7 | Crossref |
| Artificial Intelligence‐Enabled Digital Twin for Smart Manufacturing | 6 | 6 | 6 | 0 | Crossref |
| Digital Twin and Blockchain for Sensor Networks in Smart Cities | 6 | 6 | 0 | 6 | Crossref |
| Driving Innovation through AI and Digital Twin for 6G Powered Sustainable Ultra Smart Cities | 6 | 6 | 0 | 6 | Crossref |
| Lecture Notes in Mechanical Engineering | 6 | 6 | 0 | 6 | Crossref |
| Materials Research Proceedings | 6 | 6 | 1 | 5 | Crossref |
| AIP Conference Proceedings | 5 | 5 | 0 | 5 | Crossref |
| Blockchain and Digital Twin for Smart Hospitals | 5 | 5 | 0 | 5 | Crossref |

### both_openalex_crossref
| Venue | Records | Unique paper keys | Curated | Archived | Sources |
|---|---:|---:|---:|---:|---|
| Venue unknown | 227 | 227 | 50 | 177 | Crossref; OpenAlex |
| Nature Communications | 67 | 67 | 56 | 11 | Crossref; OpenAlex |
| Additive manufacturing | 62 | 62 | 54 | 8 | Crossref; OpenAlex |
| Additive Manufacturing | 56 | 56 | 39 | 17 | Crossref; OpenAlex |
| Polymers | 42 | 42 | 26 | 16 | Crossref; OpenAlex |
| Progress in Additive Manufacturing | 40 | 40 | 14 | 26 | Crossref; OpenAlex |
| Virtual and Physical Prototyping | 40 | 40 | 29 | 11 | Crossref; OpenAlex |
| The International Journal of Advanced Manufacturing Technology | 37 | 37 | 16 | 21 | Crossref; OpenAlex |
| Advanced Materials | 35 | 35 | 24 | 11 | Crossref; OpenAlex |
| 3D Printing and Additive Manufacturing | 34 | 34 | 21 | 13 | Crossref; OpenAlex |
| Advanced Materials Technologies | 33 | 33 | 25 | 8 | Crossref; OpenAlex |
| Digital Twin | 30 | 30 | 5 | 25 | Crossref; OpenAlex |
| Materials | 27 | 27 | 15 | 12 | Crossref; OpenAlex |
| Scientific Reports | 27 | 27 | 14 | 13 | Crossref; OpenAlex |
| Journal of Manufacturing Systems | 26 | 26 | 11 | 15 | Crossref; OpenAlex |
| Research Square | 25 | 25 | 12 | 13 | Crossref; OpenAlex |
| Advanced Science | 22 | 22 | 19 | 3 | Crossref; OpenAlex |
| Advanced Functional Materials | 21 | 21 | 13 | 8 | Crossref; OpenAlex |
| Applied Sciences | 21 | 21 | 12 | 9 | Crossref; OpenAlex |
| Journal of Manufacturing and Materials Processing | 20 | 20 | 8 | 12 | Crossref; OpenAlex |

### other_or_unknown
- None

## Title-Level Cross-Source Matches
- Normalized titles that appear in both OpenAlex and Crossref records: 307
- These are useful for spotting possible overlap when DOI differs or is missing. See `source_overlap_title_matches.csv`.

## Output Files
- `reports/source_overlap_records_all_3075.csv`: every scanned candidate record with source class.
- `reports/source_overlap_unique_papers.csv`: DOI/title grouped paper-level source classes.
- `reports/source_overlap_venues.csv`: venue-level source classes.
- `reports/source_overlap_title_matches.csv`: normalized title matches observed in both sources.

## Interpretation Notes
- `both_openalex_crossref` at unique-paper level means the same DOI/title grouping had both sources somewhere in the 3,075 records.
- `both_openalex_crossref` at venue level means at least one OpenAlex-sourced and at least one Crossref-sourced candidate appeared in that venue; it does not mean every paper in that venue was found by both APIs.
- Some records with different DOIs but nearly identical titles may represent preprint/published-version pairs; the title-match CSV highlights these cases separately.
