# AGENT_LOG

## 2026-06-25 12:06

### Change Summary
- Fixed AML/general author badge logic so existing corresponding-author metadata is always shown before falling back to last author.

### Edited Files
- `assets/app.js`: author chips now mark a visible author as `Corresponding` when their name appears in `corresponding_authors`, even if `author_details.is_corresponding` is missing. Last-author fallback is used only when no corresponding-author metadata exists.
- `index.html`: bumped static asset cache versions.
- `AGENT_LOG.md`: recorded this correction.

### Implemented Features
- If `corresponding_authors` exists, the matching author chip shows `Corresponding`.
- If `corresponding_authors` exists but the author is not in the visible first author chips, the corresponding author is added as a supplemental chip.
- Only records with no corresponding-author metadata use `Last author`.

### Design Decisions
- Treated `corresponding_authors` as the authoritative display source over `author_details.is_corresponding`, because AML recommendation records may have `corresponding_authors` without per-author flags.
- Kept `Last author` separate from `Corresponding` to avoid implying the final author is confirmed as corresponding author.

### Validation
- Current AML recommendation data: 391 records have corresponding-author metadata; 204 records have no corresponding-author metadata and can use last-author fallback; 9 have no author data.
- `git diff --check`

### Remaining Work
- Visually confirm AML recommendation cards after deployment.

### Notes / Cautions
- OpenAI API was not used.
- No metadata collection was run; this is a frontend display correction.

## 2026-06-25 12:01

### Change Summary
- Made AML recommendation last-author display explicit by adding and consuming a `last_author` field.

### Edited Files
- `assets/app.js`: AML recommendation records now carry `last_author` into the common paper-card renderer, and the author renderer uses explicit `last_author` before recomputing from author arrays.
- `scripts/aml_common.py`: public AML recommendation output now includes `last_author` computed from the candidate author list.
- `public/data/aml_recommended_papers.json`: backfilled `last_author` for current AML recommendation records.
- `index.html`: bumped static asset cache versions.
- `AGENT_LOG.md`: recorded this update.

### Implemented Features
- AML recommendation cards no longer depend only on implicit author-array fallback to show the final author.
- Records with no confirmed `corresponding_authors` and a known final author can show `Last author` consistently.

### Design Decisions
- Kept `Last author` separate from `Corresponding`, because the final author is not guaranteed to be the corresponding author.
- Stored `last_author` in AML public output to make the recommendation data self-contained for the frontend.

### Validation
- Current AML public data: 595 records have `last_author`.
- Current AML public data: 204 records have no confirmed corresponding author but do have `last_author`.
- Current AML public data: 9 records still have no corresponding author and no author data.
- `python -m py_compile scripts/aml_common.py`
- `git diff --check`

### Remaining Work
- After deployment, verify an AML recommendation card with no corresponding-author metadata shows `Last author`.

### Notes / Cautions
- OpenAI API was not used.
- No external metadata API was called; this was a local/public JSON and frontend path correction.

## 2026-06-25 10:35

### Change Summary
- Changed the missing-corresponding-author fallback label from `Corresponding` to `Last author`.

### Edited Files
- `assets/app.js`: confirmed corresponding authors still receive `Corresponding`; fallback final authors now receive `Last author` and a tooltip explaining that corresponding-author metadata is unavailable.
- `assets/style.css`: changed fallback chip styling to a neutral last-author style instead of green corresponding-author styling.
- `index.html`: bumped static asset cache versions.
- `AGENT_LOG.md`: recorded this correction.

### Implemented Features
- The UI no longer implies that the last author is definitely the corresponding author.
- Papers with confirmed corresponding-author metadata still show `Corresponding`.
- Papers without confirmed corresponding-author metadata show `Last author` on the final listed author.

### Design Decisions
- Used a neutral badge color for `Last author` to separate inferred display fallback from confirmed corresponding-author metadata.
- Kept the last-author fallback in the authors row only, with no duplicate author row.

### Validation
- Confirmed no stale references to `fallbackCorrespondingTitle`, `fallbackCorrespondingSearchText`, or `.is-fallback-corresponding`.
- `git diff --check`

### Remaining Work
- Visually confirm deployed cards after Pages deployment.

### Notes / Cautions
- OpenAI API was not used.
- No metadata collection was run; this is a frontend label correction.

## 2026-06-25 10:33

### Change Summary
- Removed the duplicate dedicated `Corresponding Author` row and kept only the requested inline last-author fallback inside the existing authors row.

### Edited Files
- `assets/app.js`: removed the separate corresponding-author row logic and kept the rule that if no corresponding author is marked, the final listed author receives the `Corresponding` badge inside the authors list.
- `assets/style.css`: removed unused CSS for the deleted corresponding-author row.
- `index.html`: bumped static asset cache versions.
- `AGENT_LOG.md`: recorded this correction.

### Implemented Features
- The UI no longer duplicates corresponding author information.
- Papers with confirmed corresponding authors still show the `Corresponding` badge on those authors in the authors row.
- Papers without confirmed corresponding authors show the `Corresponding` badge on the last listed author in the same authors row.

### Design Decisions
- Followed the user-requested behavior exactly: do not create another author section; only fill the missing corresponding-author indication with the last author.
- Kept robust author normalization from the previous hardening work.

### Validation
- Confirmed no remaining references to `correspondingAuthorLabel`, `renderCorrespondingAuthorLine`, or `.corresponding-author-line`.
- Current `data/papers_index.json`: 560 records have inline last-author fallback candidates; 12 records have no author data.
- Current `public/data/aml_recommended_papers.json`: 204 records have inline last-author fallback candidates; 9 records have no author data.
- `git diff --check`

### Remaining Work
- Visually confirm deployed cards show only one author row.

### Notes / Cautions
- OpenAI API was not used.
- No metadata collection was run; this is a frontend display correction.

## 2026-06-25 10:29

### Change Summary
- Changed the author UI so papers without confirmed corresponding-author metadata show the last author in a dedicated `Corresponding Author` line.

### Edited Files
- `assets/app.js`: added a dedicated corresponding-author row, displays confirmed corresponding authors when available, and displays the final listed author in that same row when no confirmed corresponding author exists.
- `index.html`: bumped static asset cache versions.
- `AGENT_LOG.md`: recorded this update.

### Implemented Features
- Cards no longer rely on a small badge hidden inside the author list to communicate the fallback.
- For records with no `corresponding_authors` but with `authors`, the UI explicitly shows the last author under `Corresponding Author`.
- Records with no author list still show `No author data`.

### Design Decisions
- The public UI now treats last-author fallback as a display rule, while the underlying data still keeps confirmed corresponding authors separate from fallback display.
- Kept the full authors row below the corresponding-author row so users can still inspect the author list.

### Validation
- Current `data/papers_index.json`: 560 records will show last-author fallback in the `Corresponding Author` line; 12 records have no author data.
- Current `public/data/aml_recommended_papers.json`: 204 records will show last-author fallback in the `Corresponding Author` line; 9 records have no author data.
- `git diff --check`

### Remaining Work
- Visually confirm the deployed card layout after Pages deployment.

### Notes / Cautions
- OpenAI API was not used.
- No metadata collection was run; this is a frontend display change.

## 2026-06-25 10:25

### Change Summary
- Hardened the frontend corresponding-author fallback so papers without confirmed corresponding-author metadata more reliably show the final listed author.

### Edited Files
- `assets/app.js`: normalized author details and author-name arrays before rendering/search/citation, made last-author fallback choose the longer available author source, and added support for author objects with `display_name` / `full_name` fields.
- `index.html`: bumped static asset cache versions.
- `AGENT_LOG.md`: recorded this update.

### Implemented Features
- If `corresponding_authors` is empty but `authors` exists, the UI now reliably uses the final author in `authors` as the corresponding-author fallback.
- If `author_details` exists but is incomplete, the UI falls back to `authors` instead of returning no fallback.
- Search text and copied citations now use the same robust author-name normalization.

### Design Decisions
- The fallback remains a display fallback only; the data still distinguishes confirmed `corresponding_authors` from inferred final-author fallback.
- The final author is chosen from the longer available author list to avoid using the last item of a truncated `author_details` list.
- Records with no author list in Crossref/OpenAlex metadata still show `No author data` rather than inventing a name.

### Validation
- Current curated/index data: 485 papers have renderable last-author fallback and 11 have no author data available.
- Current AML recommendations: 204 papers have renderable last-author fallback and 9 have no author data available.
- `git diff --check`

### Remaining Work
- Visually confirm deployed cards that previously looked blank in the author row.

### Notes / Cautions
- OpenAI API was not used.
- No metadata collection was run; this is a frontend hardening change.

## 2026-06-24 13:40

### Change Summary
- Expanded self-driving laboratory discovery for reaction optimization, formulation discovery, polymer nanoparticle synthesis, and chemistry/materials automation papers.

### Edited Files
- `data/queries.json`: added general and title-fragment Crossref queries for SDL reaction/formulation/polymer/nanoparticle/catalysis papers.
- `data/crossref_venue_queries.json`: added Nature Synthesis, Polymer Chemistry, Digital Discovery, and Materials Horizons as ISSN-targeted venue routes, and added SDL/formulation queries to selected high-impact/core venues.
- `scripts/summarize.py`: expanded `Self-driving Labs` tag signals and ensured SDL/formulation papers classify under `AI and Machine Learning for AM` with a minimum relevance score of 7.
- `scripts/update_papers.py`: expanded legacy relevance/plausibility signals and core venue labels for the new SDL-relevant journals.
- `scripts/collect_aml_candidates.py`: added SDL/formulation/polymer/catalysis queries and signals to AML recommendation external candidate collection.
- `assets/app.js`: expanded frontend `Self-driving Labs` matching and added Nature Synthesis / Materials Horizons to priority venue display.
- `index.html`: bumped static asset cache versions.
- `AGENT_LOG.md`: recorded this update.

### Implemented Features
- Papers about automated reaction optimization, photochemical SDLs, polymer nanoparticle SDLs, formulation discovery, LCST optimization, homogeneous catalysis, polymer processing SDLs, and SDL 2.0 reviews are more likely to be discovered and tagged.
- AML recommendation external search now includes these SDL/formulation routes.
- Future cards can filter these records under `Self-driving Labs`.

### Design Decisions
- Treated chemistry/materials SDL papers as relevant to the tracker because they are close to DLP resin/additive formulation and DM-filament/material-search workflows.
- Added exact title-fragment queries for the user-supplied priority examples to reduce missed discovery from generic keyword mismatch.
- Did not run a full paper update in this change; the new discovery paths apply on the next scheduled/manual update.

### Validation
- Confirmed `data/queries.json` has 95 default queries, including 23 SDL-related queries.
- Confirmed `data/crossref_venue_queries.json` has 30 venue targets and 435 ISSN-query routes.
- Confirmed Nature Synthesis, Polymer Chemistry, Digital Discovery, and Materials Horizons venue routes exist with ISSNs.
- Sample fallback summaries for three SDL titles produced `Self-driving Labs`, `AI and Machine Learning for AM`, and relevance score 7.
- `python -m py_compile scripts/summarize.py scripts/update_papers.py scripts/collect_aml_candidates.py`

### Remaining Work
- Run the normal paper update workflow to collect these papers into the public dataset.
- Inspect the resulting SDL papers after collection to tighten overly broad chemistry-only matches if needed.

### Notes / Cautions
- OpenAI API was not used.
- This change expands Crossref discovery and AML candidate discovery only; it does not itself add new papers until an update run occurs.

## 2026-06-24 13:34

### Change Summary
- Added `Inverse Design` as a searchable, taggable, and sidebar-visible topic.

### Edited Files
- `data/queries.json`: added default Crossref search queries for inverse design in additive manufacturing, 3D printing, and metamaterials/manufacturing.
- `data/crossref_venue_queries.json`: added `inverse design` to each core venue ISSN-targeted query set.
- `assets/app.js`: added `Inverse Design` to the left sidebar under AI Manufacturing, tag display labels, card tag priority, canonical topic matching, and runtime subtopic derivation.
- `scripts/summarize.py`: added `Inverse Design` as a generated tag and included inverse design in relevance scoring terms.
- `scripts/update_papers.py`: added inverse-design terms to the legacy relevance/plausibility signal list.
- `index.html`: bumped static asset cache versions.
- `AGENT_LOG.md`: recorded this update.

### Implemented Features
- New and existing metadata can be classified/displayed with the `Inverse Design` tag.
- The left sidebar can filter papers by `Inverse Design`.
- Future scheduled/manual paper updates will search for inverse-design papers through both the default query list and core-venue ISSN query routes.

### Design Decisions
- Treated `Inverse Design` as an independent subtopic instead of folding it only into `Design Automation`, because it is a specific research method users may want to filter directly.
- Kept the broader `Design Automation` tag for computational/generative/topology-design papers.

### Validation
- Parsed `data/queries.json` and `data/crossref_venue_queries.json` successfully.
- Confirmed 3 inverse-design default queries and 26 core-venue inverse-design query routes.
- `python -m py_compile scripts/summarize.py scripts/update_papers.py`
- `git diff --check`

### Remaining Work
- Run the normal paper update workflow to collect newly discoverable inverse-design papers.

### Notes / Cautions
- OpenAI API was not used.

## 2026-06-24 13:03

### Change Summary
- Expanded Crossref ISSN-based core venue searches so important journals are searched more broadly before the existing relevance/curation filters narrow the public site.

### Edited Files
- `data/crossref_venue_queries.json`: expanded from 3 venue targets to 26 core/high-impact/manufacturing venue targets and added broader manufacturing-adjacent queries.
- `AGENT_LOG.md`: recorded this update.

### Implemented Features
- Core venue search now covers Nature, Science, Nature Communications, Nature Materials, Nature Reviews Materials, Science Advances, Science Robotics, PNAS, Advanced Materials, Advanced Functional Materials, Advanced Science, ACS Applied Materials & Interfaces, Materials & Design, Additive Manufacturing, and several core manufacturing journals.
- Query coverage now includes broader phrases such as volumetric printing, photopolymerization, liquid crystal elastomers, soft robotics, metamaterials, robotic manufacturing, digital twins, self-driving laboratories, and machine-learning-driven materials/manufacturing.

### Design Decisions
- Used Crossref ISSN venue search as the broad discovery layer and kept the existing relevance score / archive split as the narrow public-display layer.
- Kept mostly one representative ISSN per venue to avoid multiplying API calls unnecessarily.
- Did not run a full data rebuild in this change; the expanded search scope will apply on the next scheduled or manual paper update.

### Validation
- Parsed `data/crossref_venue_queries.json` successfully as JSON.
- Counted 26 venue targets, 296 query entries, and 296 ISSN-query routes.

### Remaining Work
- Run the manual paper update or wait for the scheduled update to collect new papers under the broader core-venue search scope.
- After collection, inspect whether newly added core-venue papers are relevant enough or whether specific broad terms should be tightened.

### Notes / Cautions
- OpenAI API was not used.
- This expands discovery breadth, so the next update may add more candidates; relevance filtering should still decide what appears publicly.

## 2026-06-24 12:49

### Change Summary
- Fixed author display fallback so papers without confirmed corresponding-author metadata use the final listed author as a corresponding-author fallback.
- Backfilled missing author lists for current local paper data where OpenAlex DOI metadata could provide authors.
- Fixed the Crossref full-rebuild path so OpenAlex DOI lookup preserves author lists even when OpenAlex does not provide confirmed corresponding authors.

### Edited Files
- `assets/app.js`: replaced the old last-author proxy UI with a corresponding-author fallback, added fallback author search text, and displays `No author data` when neither Crossref nor OpenAlex provides authors.
- `assets/style.css`: updated the fallback author chip styling and removed obsolete proxy-badge styling.
- `scripts/full_rebuild_crossref_dataset.py`: stores OpenAlex `authors` / `author_details` during missing-corresponding-author DOI cross-checks, even if no corresponding author is found.
- `data/papers.json`: backfilled available author lists for existing records that had DOI but no author list.
- `data/papers_index.json` and `data/details/`: regenerated split public data from the updated paper database.
- `public/data/aml_recommended_papers.json`: synchronized author/corresponding fields from the main paper database for matching DOI records.
- `index.html`: bumped static asset cache version.
- `AGENT_LOG.md`: recorded this update.

### Implemented Features
- Cards now show confirmed `Corresponding` authors when available.
- If confirmed corresponding-author metadata is missing but the paper has an author list, the final listed author is shown with a `Corresponding` badge as a metadata fallback.
- If no author list exists in Crossref/OpenAlex metadata, the card explicitly shows `No author data` instead of leaving the author area blank.
- Future Crossref full rebuilds can still support last-author fallback when OpenAlex supplies author lists but no corresponding-author flags.

### Design Decisions
- The UI no longer uses a separate `Last author` badge, because the intended behavior is to use the final listed author as the corresponding-author fallback.
- The fallback tooltip explains that the displayed author is based on missing corresponding-author metadata, not a confirmed publisher/OpenAlex flag.
- OpenAlex was used only for DOI-based metadata backfill; it was not used as a general paper discovery source.

### Validation
- `python -m py_compile scripts/full_rebuild_crossref_dataset.py scripts/build_split_data.py scripts/update_papers.py`
- Current curated data: 876 papers with confirmed corresponding authors, 485 papers with last-author fallback possible, 11 papers with no author data available.
- Current AML recommendations: 391 papers with confirmed corresponding authors, 204 papers with last-author fallback possible, 9 papers with no author data available.
- `node --check assets/app.js` could not be run because Node.js is not installed in the local shell.

### Remaining Work
- After deployment, visually confirm a few cards with missing confirmed corresponding authors to ensure the fallback chip reads naturally.

### Notes / Cautions
- OpenAI API was not used.
- Do not infer a last author when no author list exists; those cases remain marked as `No author data`.

## 2026-06-24 12:07

### Change Summary
- Fixed AML Recommendation Manual deployment behavior so updated recommendation JSON is deployed to GitHub Pages.
- Investigated why the site still showed 564 AML recommendations after the workflow produced 604.

### Edited Files
- `.github/workflows/aml-recommendation-manual.yml`: added Pages permissions, github-pages environment metadata, artifact build/upload, and `actions/deploy-pages@v4` deployment steps after publishing AML recommendation output.
- `AGENT_LOG.md`: recorded this update and the root cause.

### Implemented Features
- Running AML Recommendation Manual with `publish_output=true` now commits `public/data/aml_recommended_papers.json` and deploys the current site artifact in the same workflow.
- The site no longer depends on a separate push-triggered Pages workflow after an Actions bot commit.

### Design Decisions
- Kept the existing standalone `Deploy GitHub Pages` workflow for normal user pushes.
- Added deployment directly to the AML workflow because GitHub Actions commits made with `GITHUB_TOKEN` do not reliably trigger downstream push workflows.
- Did not call OpenAI, Crossref, or OpenAlex.

### Validation
- Confirmed raw GitHub `main` had 604 AML recommendations updated at `2026-06-24T02:50:07Z`.
- Confirmed GitHub Pages was still serving the older 564-recommendation JSON updated at `2026-06-22T02:48:47Z`.
- Confirmed the latest deploy-pages run predated the AML recommendation commit, explaining the mismatch.

### Remaining Work
- After this workflow change is pushed, GitHub Pages should redeploy from the new commit and start serving the 604-recommendation JSON.

### Notes / Cautions
- If `publish_output=false`, the AML workflow still uploads an artifact only and does not deploy public Pages output.

## 2026-06-24 10:37

### Change Summary
- Strengthened `Soft robotics` tag detection for soft robot / soft robots wording.

### Edited Files
- `scripts/summarize.py`: added `soft robot`, `soft robots`, `soft actuator(s)`, `embedded actuation`, and `embedded sensing` to the `Soft robotics` tag map.
- `scripts/update_papers.py`: added the same soft-robotics terms to the legacy relevance/topic signal list.
- `assets/app.js`: added the same terms to canonical topic and runtime subtopic derivation.
- `index.html`: bumped the CSS/JS cache version for GitHub Pages.
- `AGENT_LOG.md`: recorded this update.

### Implemented Features
- Papers titled like `Multimaterial 3D printed soft robots with embedded actuation and sensing` now receive the `Soft robotics` tag in fallback metadata summarization.
- Frontend filtering/card tagging can recognize `soft robot`, `soft robots`, embedded actuation, and embedded sensing as soft-robotics signals.

### Design Decisions
- Kept the existing canonical tag name as `Soft robotics` / displayed as `Soft Robotics`.
- Did not create a separate `Soft robot` tag because it would fragment the topic taxonomy.
- Did not call OpenAI, Crossref, or OpenAlex.

### Validation
- Local fallback summary test for `Multimaterial 3D printed soft robots with embedded actuation and sensing` produced `tags: ['Soft robotics']`.

### Remaining Work
- Run the normal paper update workflow so newly collected papers receive this improved tag metadata.

### Notes / Cautions
- `MMAM` may still be represented as the `Multi-material AM` category in stored metadata; frontend topic derivation can still surface MMAM-like filtering from title text.

## 2026-06-24 09:52

### Change Summary
- Expanded Crossref collection coverage for multimaterial 3D-printed soft robotics papers.
- Added `Science Advances` to ISSN-targeted Crossref venue search.

### Edited Files
- `data/queries.json`: added soft-robotics/MMAM queries for multimaterial 3D printed soft robots with embedded actuation and sensing.
- `data/crossref_venue_queries.json`: added `Science Advances` with ISSN `2375-2548` and AM/soft-robotics/4D-printing/materials-discovery queries.
- `AGENT_LOG.md`: recorded this update.

### Implemented Features
- Future Crossref full rebuilds can capture papers like `Multimaterial 3D printed soft robots with embedded actuation and sensing`.
- Science Advances now has an ISSN-based venue-search route, so relevant Sci. Adv. papers are less dependent on broad keyword rank.

### Design Decisions
- Used Crossref official metadata and ISSN-targeted search only.
- Did not use OpenAlex as a paper discovery source.
- Did not call OpenAI.

### Validation
- Confirmed Crossref has DOI `10.1126/sciadv.adz2928` for `Multimaterial 3D printed soft robots with embedded actuation and sensing`.
- Confirmed the new general query `multimaterial 3D printed soft robot` finds the DOI in Crossref top results.
- Confirmed the repository's `fetch_crossref_by_issn_query()` finds the DOI at rank 1 for Science Advances ISSN `2375-2548`.

### Remaining Work
- Run the normal `Update papers` workflow to rebuild the public dataset with the new query coverage.

### Notes / Cautions
- This change updates collection criteria only; it does not itself rebuild `data/papers.json`.

## 2026-06-24 09:43

### Change Summary
- Removed duplicate corresponding-author display from paper cards.
- Added a conservative last-author proxy marker for records without confirmed corresponding-author metadata.

### Edited Files
- `assets/app.js`: removed the separate `Corresponding authors` line, kept confirmed corresponding authors as badges inside the author chip list, and added `Last author` proxy marking/search text when no confirmed corresponding author exists.
- `assets/style.css`: added styling for the `Last author` proxy chip/badge.
- `index.html`: bumped the CSS/JS cache version for GitHub Pages.
- `AGENT_LOG.md`: recorded this update.

### Implemented Features
- Confirmed corresponding authors are no longer shown twice.
- If Crossref/OpenAlex do not provide corresponding-author metadata, the final listed author is marked as `Last author` instead of being mislabeled as a corresponding author.
- Search can match `last author`, `senior author proxy`, and the final author's name.

### Design Decisions
- Did not infer or store the last author as an actual corresponding author.
- Kept confirmed corresponding-author display distinct from last-author proxy display.
- Did not call OpenAI, Crossref, or OpenAlex.

### Remaining Work
- Verify on GitHub Pages that author chips no longer duplicate confirmed corresponding authors.

### Notes / Cautions
- `Last author` is only a proxy marker. It is not a claim that the person is the corresponding author.

## 2026-06-23 16:02

### Change Summary
- Removed the visible `Load details` / `Details loaded` control from paper cards.

### Edited Files
- `assets/app.js`: removed the manual detail-load button and click handler from paper cards while keeping automatic lazy loading for AI/Q5 summaries.
- `index.html`: bumped the CSS/JS cache version for GitHub Pages.
- `AGENT_LOG.md`: recorded this update.

### Implemented Features
- Users no longer see internal detail-loading state on cards.
- If an AI/Q5 summary is available, the automatic detail loader still brings it into the card.

### Design Decisions
- Treated detail chunks as an internal performance implementation detail, not a user-facing feature.
- Kept DOI, Open Paper, and Copy Cite actions visible.
- Did not call OpenAI, Crossref, or OpenAlex.

### Remaining Work
- Verify on GitHub Pages that paper cards no longer show `Load details` or `Details loaded`.

### Notes / Cautions
- Automatic detail loading is still limited to visible cards to preserve initial-load performance.

## 2026-06-23 16:01

### Change Summary
- Added automatic lazy loading of OpenAI/Q5 summaries for visible paper cards.
- Confirmed that the OpenAI summary data was not lost; it remains in `data/papers.json` and detail chunks.

### Edited Files
- `assets/app.js`: added visible-card detail preloading for papers marked with OpenAI summaries, while keeping the lightweight index loading strategy.
- `index.html`: bumped the CSS/JS cache version for GitHub Pages.
- `AGENT_LOG.md`: recorded this update.

### Implemented Features
- Visible non-AML cards with `summary_provider=openai` or `openai_summary_applied=true` now automatically load their detail chunk.
- Once the detail chunk is loaded, the card can show the stored Q5 AI summary and the `AI summary` badge without requiring the user to click `Load details`.
- Auto-loading is limited to the currently rendered cards, so the site does not fetch all 1,148 AI summaries at startup.

### Design Decisions
- Preserved the reduced initial payload from `data/papers_index.json`.
- Used lazy detail loading instead of putting `ai_summary_en` back into the index file.
- Did not call OpenAI, Crossref, or OpenAlex.

### Remaining Work
- Verify on the deployed site that visible cards switch from fallback metadata text to Q5 AI summaries shortly after initial render.

### Notes / Cautions
- The first paint may briefly show metadata fallback text before the detail chunk finishes loading.
- AML recommendation cards already carry their AI summaries directly in `public/data/aml_recommended_papers.json`.

## 2026-06-23 15:57

### Change Summary
- Fixed misleading `AI summary` badges on cards that do not currently display an AI-written summary.

### Edited Files
- `assets/app.js`: changed summary badge logic to require a displayable stored OpenAI/Q5 summary, not just the `summary_provider` or `openai_summary_applied` flag.
- `index.html`: bumped the CSS/JS cache version for GitHub Pages.
- `AGENT_LOG.md`: recorded this update.

### Implemented Features
- Initial lightweight index cards no longer show `AI summary` when the actual OpenAI summary text is not present in the loaded card data.
- Cards show `AI summary` only when a parseable stored Q5 summary is available for display.
- Metadata fallback summaries continue to show as `Metadata summary`.

### Design Decisions
- Preserved the lightweight `papers_index.json` loading strategy instead of putting all AI summaries back into the initial payload.
- Kept original OpenAI summary data in `data/papers.json` and detail chunks unchanged.
- Did not call OpenAI, Crossref, or OpenAlex.

### Remaining Work
- If desired later, add a separate `AI summary available` state for index cards whose full detail chunk contains an OpenAI summary but has not yet been loaded.

### Notes / Cautions
- After clicking `Load details`, a card with a stored Q5 OpenAI summary can switch from `Metadata summary` to `AI summary`.

## 2026-06-23 15:51

### Change Summary
- Added multi-select behavior for left-panel subtopic keywords.
- Updated sidebar active-state styling so selected subtopics remain visible in light and dark modes.

### Edited Files
- `assets/app.js`: changed sidebar subtopic filtering from a single active subtopic to a multi-select `Set`, added toggle/clear helpers, and updated filter logic.
- `assets/style.css`: added visual styling for fields that contain selected subtopics.
- `index.html`: bumped the CSS/JS cache version for GitHub Pages.
- `AGENT_LOG.md`: recorded this update.

### Implemented Features
- Multiple left-panel subtopics can be selected at the same time.
- Selected subtopics are combined with OR logic: a paper appears if it matches any selected subtopic.
- Clicking a field title still works as a single field filter and clears multi-selected subtopics.
- Changing the top `Field` or `Tag/Subtopic` dropdown clears sidebar multi-selection to avoid conflicting filter states.

### Design Decisions
- Kept the existing top dropdowns as single-select controls and used the left panel for multi-select keyword filtering.
- Preserved the current AML Recommendations, venue, year, summary, search, and sort behavior.
- Did not call OpenAI, Crossref, or OpenAlex.

### Remaining Work
- After deployment, verify the sidebar multi-select interaction on desktop and mobile.

### Notes / Cautions
- Multi-selected subtopics are not persisted across page reloads.
- The filter uses OR logic rather than AND logic so selecting more keywords expands the result set instead of narrowing it.

## 2026-06-23 15:47

### Change Summary
- Improved AML Recommendation cards to show corresponding authors explicitly.
- Added corresponding-author metadata to the existing search index.
- Allowed normal sort modes to work in AML Recommendations view while preserving AML-score sorting for relevance.

### Edited Files
- `assets/app.js`: added a corresponding-author line, included corresponding-author names/affiliations in search text, and adjusted AML sorting behavior.
- `assets/style.css`: added styling for the corresponding-author line.
- `index.html`: bumped the CSS/JS cache version for GitHub Pages.
- `AGENT_LOG.md`: recorded this update.

### Implemented Features
- AML recommendation cards now display `Corresponding authors` when the data exists.
- Search can match corresponding author names, ORCID/OpenAlex author IDs, institutions, country codes, and raw affiliation strings.
- In AML Recommendations view, `Relevance` sorts by AML score; `Newest`, `Recently added`, and `Title` use the normal site sort behavior.

### Design Decisions
- Reused the existing paper card design instead of creating a separate AML-specific card.
- Treated corresponding-author metadata as part of the general keyword/search surface instead of adding another filter.
- Did not call OpenAI, Crossref, or OpenAlex.

### Remaining Work
- Verify the deployed GitHub Pages page after cache refresh.

### Notes / Cautions
- Papers without `corresponding_authors` still hide the corresponding-author line.
- This change does not rescore or recollect AML recommendations.

## 2026-06-23 12:58

### Change Summary
- Tightened the public AML recommendation threshold from 0.60 to 0.75.

### Edited Files
- `scripts/score_aml_recommendations.py`: changed the default `PUBLIC_AML_SCORE_THRESHOLD` to `0.75`, so future AML Recommendation Manual runs publish only stronger recommendations unless explicitly overridden.
- `assets/app.js`: changed the frontend AML threshold defense to `0.75`.
- `public/data/aml_recommended_papers.json`: filtered current recommendations from 641 to 564 by removing 77 papers below 0.75.
- `README.md`: documented the stricter public threshold.
- `index.html`: bumped frontend asset cache version to `20260623-aml-threshold-075`.
- `AGENT_LOG.md`: recorded this threshold update.

### Implemented Features
- Pressing the AML Recommendation Manual button now uses the stricter 0.75 default threshold for public output.
- The site displays only AML recommendations scoring 75/100 or higher.

### Design Decisions
- Used 0.75 because it aligns with the existing `High` recommendation boundary and narrows the list without jumping straight to a very small top-only set.
- Kept `AML_PUBLIC_SCORE_THRESHOLD` as an environment-variable override for future experimentation.

### Remaining Work
- If the list is still too broad, test 0.80 or 0.85 after reviewing the 0.75 output.

### Notes / Cautions
- No OpenAI, Crossref, or OpenAlex API calls were made.

## 2026-06-23 12:51

### Change Summary
- Removed keyword score and discovery-route score from AML scoring.

### Edited Files
- `scripts/score_aml_recommendations.py`: changed AML score formula to 80% semantic similarity, 10% recency, and 10% venue; removed keyword/route score calculations and route text from OpenAI reason prompts.
- `assets/app.js`: AML fallback explanation no longer describes discovery route as part of the recommendation method, and source summaries are still prioritized when available.
- `public/data/aml_recommended_papers.json`: recomputed current public AML scores using nearest-seed similarity as the available semantic proxy, plus recency and venue; kept only score >= 0.60.
- `README.md`: documented the new AML scoring formula and the rationale for excluding keyword/route scores.
- `ARCHITECTURE.md`: documented the new AML scoring basis.
- `index.html`: bumped frontend asset cache version to `20260623-aml-semantic-score`.
- `AGENT_LOG.md`: recorded this scoring change.

### Implemented Features
- AML score no longer rewards papers just because they matched collection keywords or came from a particular discovery route.
- Negative keyword effects, such as penalizing scaffold-related future research directions, no longer affect AML score.

### Design Decisions
- Matched topics remain available for labels/explanations, but they are not score components.
- For the current public JSON only, nearest seed similarity was used as the available semantic proxy. Future AML workflow runs compute semantic similarity from candidate/profile/seed embeddings in the scoring script.

### Remaining Work
- Run `AML Recommendation Manual` again when convenient so every public recommendation score is recomputed from the full embedding-based semantic formula.

### Notes / Cautions
- No OpenAI, Crossref, or OpenAlex API calls were made during this code/data update.

## 2026-06-22 12:02

### Change Summary
- Reused existing curated-paper summaries in AML recommendation cards.

### Edited Files
- `scripts/score_aml_recommendations.py`: merges `data/papers.json` summary fields into AML candidates before scoring/public export.
- `scripts/aml_common.py`: includes summary fields in `public/data/aml_recommended_papers.json`.
- `assets/app.js`: uses AML item summary metadata instead of forcing AML cards to metadata-only summaries.
- `public/data/aml_recommended_papers.json`: backfilled existing source summaries into current AML recommendations.
- `index.html`: bumped frontend asset cache version to `20260622-aml-source-summary`.
- `AGENT_LOG.md`: recorded this summary reuse update.

### Implemented Features
- AML recommendation cards now reuse existing `ai_summary_en`, `relevance_note_en`, `summary_provider`, and `openai_summary_applied` from the original curated paper when available.
- Current AML recommendations: 641/641 matched to source summaries, with 638 OpenAI summaries reused.

### Design Decisions
- Reused existing summaries by DOI/title key to avoid additional OpenAI cost.
- Kept AML-specific score/recommendation metadata while borrowing the source paper's summary content.

### Remaining Work
- If the three non-OpenAI AML recommendations matter, refresh only those with the manual OpenAI summary workflow later.

### Notes / Cautions
- No OpenAI, Crossref, or OpenAlex API calls were made.

## 2026-06-22 11:56

### Change Summary
- Bumped frontend asset cache version so the AML sidebar count and recommendation list use the latest no-cap logic.

### Edited Files
- `index.html`: updated `assets/style.css` and `assets/app.js` query versions to `20260622-aml-all-visible`.
- `AGENT_LOG.md`: recorded the cache-busting fix.

### Implemented Features
- Browsers should now load the app.js version where AML recommendations are not capped at 24.
- The left sidebar AML count should reflect all visible recommendations above the 0.60 threshold.

### Design Decisions
- The sidebar already used `amlVisibleRecommendations().length`; the missing piece was forcing clients to fetch the updated JS.

### Remaining Work
- Wait for GitHub Pages deployment, then hard-refresh the browser if the old cached JS is still visible.

### Notes / Cautions
- No external APIs were called.

## 2026-06-22 11:50

### Change Summary
- Removed the frontend 24-item cap from AML recommendation display.

### Edited Files
- `assets/app.js`: removed `.slice(0, 24)` from `amlVisibleRecommendations()`.
- `AGENT_LOG.md`: recorded the correction.

### Implemented Features
- The site now displays all AML recommendations that pass the public threshold (`AML score >= 0.60`), not just the first 24.

### Design Decisions
- Kept the 60/100 threshold filter and score sorting.
- Removed the hard cap because it made the updated recommendation file look unchanged on the site.

### Remaining Work
- If rendering all recommendations feels heavy on mobile, add a clear `Load more` button later instead of silently truncating.

### Notes / Cautions
- Root cause of the user's report: `public/data/aml_recommended_papers.json` had 641 eligible recommendations, but the UI rendered only 24 due to a leftover frontend cap.
- No OpenAI, Crossref, or OpenAlex API calls were made.

## 2026-06-22 11:42

### Change Summary
- Limited public AML recommendations to papers with `AML score >= 0.60`.

### Edited Files
- `scripts/score_aml_recommendations.py`: added `PUBLIC_AML_SCORE_THRESHOLD` and filters public AML output by score.
- `public/data/aml_recommended_papers.json`: reduced current public AML recommendations from 1,112 to 641 entries by removing 471 papers below 0.60.
- `assets/app.js`: added a frontend defense so recommendations below 0.60 are not displayed even if present in the JSON.
- `README.md`: documented the public AML recommendation threshold.
- `AGENT_LOG.md`: recorded this threshold change.

### Implemented Features
- AML recommendation output now shows only recommendations with score 60/100 or higher.

### Design Decisions
- Kept lower-scoring candidates out of the public recommendation JSON instead of only hiding them in the UI, so the published file is smaller and cleaner.
- The UI still shows the top visible AML recommendations first.

### Remaining Work
- If the user wants to browse all 641 visible recommendations, add pagination or a `Load more AML recommendations` button because the current UI renders the top subset.

### Notes / Cautions
- The latest successful AML workflow did update `public/data/aml_recommended_papers.json`; it expanded from 50 to 1,112 before this threshold cleanup.
- No OpenAI, Crossref, or OpenAlex API calls were made during this cleanup.

## 2026-06-22 11:28

### Change Summary
- Fixed Crossref/JATS markup artifacts in paper titles such as `(M- <scp>STARC</scp>)`.

### Edited Files
- `scripts/fetch_crossref.py`: cleans Crossref title and venue strings by removing inline markup tags, decoding HTML entities, normalizing whitespace, and preserving sub/sup text compactly.
- `assets/app.js`: added frontend display cleanup so any future residual markup is not shown to users.
- `data/papers.json`, `data/archive_papers.json`: cleaned existing title/venue strings.
- `data/papers_index.json`, `data/archive_papers_index.json`, `data/details/detail_*.json`: regenerated split public data after cleanup.
- `data/papers.csv`, `data/papers.xlsx`: cleaned exported title/venue fields.
- `AGENT_LOG.md`: recorded this cleanup.

### Implemented Features
- Paper titles now render without raw tags such as `<scp>`, `<i>`, and `<sub>`.
- Examples now display as readable text such as `M-STARC`, `via`, and `Al2O3`.

### Design Decisions
- Kept tag contents while removing the markup, because the words/chemical indices are part of the title.
- Added both ingestion-time cleanup and frontend display-time defense to prevent recurrence.

### Remaining Work
- Watch the next Crossref rebuild to confirm no new JATS tags appear in titles or venues.

### Notes / Cautions
- No external APIs were called.

## 2026-06-22 11:16

### Change Summary
- Restored OpenAI summary fields from historical commit `a105670` without making new OpenAI API calls.

### Edited Files
- `data/papers.json`: restored OpenAI summary fields for currently matching papers.
- `data/papers_index.json`: regenerated split startup index after restoration.
- `data/details/detail_000.json` through `data/details/detail_004.json`: regenerated lazy detail chunks after restoration.
- `AGENT_LOG.md`: recorded the restoration.

### Implemented Features
- Recovered previously generated OpenAI summaries for 1,231 of 1,236 current curated papers.
- Preserved metadata/fallback summaries for 5 current papers that did not match the historical OpenAI-summary commit by DOI/title dedupe key.

### Design Decisions
- Restored only summary-related fields: `ai_summary_en`, `relevance_note_en`, `tags`, `categories`, `relevance_score`, `summary_provider`, `openai_summary_applied`, and `abstract_used_for_summary`.
- Did not restore older paper metadata wholesale, so current Crossref rebuild metadata remains the source of truth.

### Remaining Work
- The remaining 5 fallback papers can be refreshed with the manual OpenAI summary workflow if needed.

### Notes / Cautions
- No OpenAI, Crossref, or OpenAlex API calls were made.
- Source used for restoration: `git show a105670:data/papers.json`.

## 2026-06-22 11:10

### Change Summary
- Investigated why the June 20 OpenAI summary refresh did not remain visible and fixed the overwrite path.

### Edited Files
- `scripts/full_rebuild_crossref_dataset.py`: preserves existing OpenAI summaries by DOI/title dedupe key during Crossref-only full rebuilds.
- `.github/workflows/refresh-openai-summaries.yml`: changed Pages deployment to use a staged artifact that excludes `data/private/` and root `private/`.
- `AGENT_LOG.md`: recorded the root cause and fix.

### Implemented Features
- OpenAI summaries are no longer reset to metadata fallback just because the scheduled Crossref full rebuild runs later.
- OpenAI summary refresh deployments no longer upload private seed/debug folders to Pages.

### Design Decisions
- Preserved only records explicitly marked `summary_provider=openai` or `openai_summary_applied=true`.
- Matched preserved summaries by the existing DOI/title-year-author dedupe key, so the rebuild remains Crossref-only for discovery while keeping user-approved OpenAI summary work.

### Remaining Work
- To restore OpenAI summaries already overwritten by later rebuilds, either rerun the OpenAI summary refresh or recover from the `a105670` commit before the overwrite.

### Notes / Cautions
- Historical check: commit `a105670 Refresh OpenAI paper summaries` had 1,237 OpenAI-applied summaries, but later `Update paper metadata` commits reset the active dataset to fallback summaries.
- No OpenAI, Crossref, or OpenAlex API calls were made during this investigation/fix.

## 2026-06-22 10:52

### Change Summary
- Added the AML seed JSON as the only allowed tracked file under `data/private/` and protected it from GitHub Pages deployment.

### Edited Files
- `data/private/aml_seed_papers_core_enriched.json`: copied from the local private seed source so GitHub Actions can run the AML recommendation pipeline.
- `scripts/aml_common.py`: changed the default AML seed path to `data/private/aml_seed_papers_core_enriched.json`.
- `.github/workflows/aml-recommendation-manual.yml`: added optional secret restore support and recognition of the tracked private seed file.
- `.github/workflows/deploy-pages.yml`: changed Pages deployment to build a staging artifact that excludes `data/private/` and root `private/`.
- `.github/workflows/update-papers.yml`: applied the same Pages artifact exclusion to scheduled paper update deployments.
- `README.md`: documented the tracked private seed file, Pages exclusion, and optional secret override.
- `ARCHITECTURE.md`: documented the private seed path and deployment exclusion.
- `PROJECT_STATUS.md`: updated the AML setup status.
- `AGENT_LOG.md`: recorded this private seed setup.

### Implemented Features
- `collect_and_score` and `full_refresh` can now use the AML seed file on GitHub Actions without requiring a large Actions secret.
- GitHub Pages artifacts exclude private seed/debug folders.

### Design Decisions
- Did not commit root `private/` files, CSV/XLSX seed exports, or AML debug outputs.
- Allowed only `data/private/aml_seed_papers_core_enriched.json` to be tracked because the user explicitly approved that JSON.
- Excluded `data/private/` from Pages artifacts because the Pages workflow previously uploaded the repository root.

### Remaining Work
- Run `Actions > AML Recommendation Manual` with `collect_and_score`, `max_candidates=0`, `use_ai_judge=false`, and the desired `use_ai_reason` setting.

### Notes / Cautions
- The AML seed includes private seed metadata and should remain in the private repository.
- No OpenAI, Crossref, or OpenAlex API calls were made during this setup.

## 2026-06-22 10:39

### Change Summary
- Fixed the AML manual workflow behavior so external discovery modes do not silently fall back to reason-only refresh when the AML seed file is missing.

### Edited Files
- `scripts/run_aml_recommendation_pipeline.py`: allows seed-missing reason-only refresh only in `score_existing` mode; `collect_and_score` and `full_refresh` now fail clearly without the seed file.
- `README.md`: documented that external AML discovery modes require the seed file on the runner.
- `AGENT_LOG.md`: recorded the silent-fallback issue and fix.

### Implemented Features
- Manual `collect_and_score` / `full_refresh` runs now make the missing-seed problem visible instead of completing quickly with no recommendation changes.

### Design Decisions
- Kept the existing reason-only fallback for `score_existing`, because that path can still update public recommendation wording without collecting/scoring new candidates.
- Required the seed file for external candidate collection and scoring because AML scoring depends on the seed-profile/embedding workflow.

### Remaining Work
- Add or provide `data/seed/aml_seed_papers_core_enriched.json` on the GitHub Actions runner before expecting external AML discovery to update recommendations.

### Notes / Cautions
- No OpenAI, Crossref, or OpenAlex API calls were made during this fix.

## 2026-06-22 10:27

### Change Summary
- Changed the manual AML recommendation workflow so `max_candidates` value `0` or blank means score all collected AML candidates.

### Edited Files
- `.github/workflows/aml-recommendation-manual.yml`: updated the `max_candidates` input description, made it optional, and changed the default to `0`.
- `scripts/collect_aml_candidates.py`: treats `max_candidates <= 0` as unlimited for the selected candidate pool and records `score_limit`.
- `scripts/score_aml_recommendations.py`: scores the full candidate pool when `max_candidates <= 0` and records pool/limit metadata in the recommendation log.
- `scripts/run_aml_recommendation_pipeline.py`: added safe parsing so blank `--max-candidates` values become `0`.
- `README.md`: documented that `0` or blank means score all collected AML candidates.
- `AGENT_LOG.md`: recorded this AML workflow behavior change.

### Implemented Features
- AML manual runs now support full candidate scoring without requiring the user to guess a large upper bound.
- Positive `max_candidates` values remain available for quick test runs.

### Design Decisions
- `collect_and_score` still limits Crossref fetch breadth per query to avoid runaway API requests, but it no longer truncates the collected candidate pool before scoring when the limit is `0`.
- The default manual workflow behavior now matches the recommendation-system intent: rank all AML-keyword candidates that were collected.

### Remaining Work
- Run the GitHub Actions manual workflow once after push to confirm the UI input behaves as expected on GitHub.

### Notes / Cautions
- No OpenAI API calls were made during this code change.
- No Crossref/OpenAlex API calls were made during validation.
- Validation: `python -m py_compile scripts\collect_aml_candidates.py scripts\score_aml_recommendations.py scripts\run_aml_recommendation_pipeline.py`.

## 2026-06-19 16:48

### Change Summary
- Deleted local private journal-matching preparation outputs as part of the same conservative JCR cleanup.

### Edited Files
- `data/private/journals_to_match_jcr.csv`: deleted local ignored journal matching preparation output.
- `data/private/journals_to_match_jcr.json`: deleted local ignored journal matching preparation output.
- `AGENT_LOG.md`: recorded this local cleanup.

### Implemented Features
- No application feature change; this was a local data hygiene cleanup.

### Design Decisions
- Treated JCR matching preparation artifacts as unnecessary to retain locally after deciding not to proceed with JCR matching.
- Kept AML private debug files because they are unrelated to JCR/JCR matching.

### Remaining Work
- Recreate journal extraction later only if a private, license-safe JCR workflow is explicitly resumed.

### Notes / Cautions
- `data/private/` remains ignored by Git.
- No external APIs were called.

## 2026-06-19 16:46

### Change Summary
- Deleted local private JCR source/export artifacts to avoid retaining licensed JCR-derived material in the working copy.

### Edited Files
- `data/private/jcr_export_original_2025.csv`: deleted local ignored JCR export file.
- `data/private/jcr_manual_review.csv`: deleted local ignored JCR review output.
- `data/private/jcr_matched_debug.csv`: deleted local ignored JCR debug output.
- `data/private/jcr_matched_debug.json`: deleted local ignored JCR debug output.
- `AGENT_LOG.md`: recorded this local cleanup.

### Implemented Features
- No application feature change; this was a local data hygiene cleanup.

### Design Decisions
- Kept `data/private/journals_to_match_jcr.csv` and `.json` because they are generated from the project's own paper database, not from JCR.
- Did not commit private files or JCR-derived outputs.

### Remaining Work
- If JCR matching is resumed later, use a private/manual workflow and confirm redistribution permissions before generating any public output.

### Notes / Cautions
- `data/private/` remains ignored by Git.
- No external APIs were called.

## 2026-06-19 14:59

### Change Summary
- Reverted the Step 3 JCR metrics matching commit to avoid possible Clarivate/JCR licensing and public redistribution risk.

### Edited Files
- `AGENT_LOG.md`: recorded the rollback rationale.
- Reverted commit `1c2721d Add local JCR metrics matching`.

### Implemented Features
- Removed public JCR-derived outputs from Git history going forward:
  - `data/journal_metrics.json`
  - `public/data/journal_metrics.json`
- Removed the Step 3 matching script and documentation that were introduced in the reverted commit.

### Design Decisions
- Treat JCR/JIF/quartile/rank/category values as licensed data that should not be publicly redistributed through GitHub Pages unless the license explicitly permits it.
- Keep JCR-related work private-only until a safer internal-use design is chosen.

### Validation
- Reverted commit `1c2721d` with `git revert --no-edit`.
- Confirmed the public JCR metrics JSON files are deleted from the tracked tree by the revert.

### Remaining Work
- If JCR data is needed later, redesign Step 3 as private/internal-only or publish only non-sensitive derived labels after confirming license terms.

### Notes
- No external APIs were called.
- Private files under `data/private/` remain ignored by Git.

## 2026-06-19 13:00

### Change Summary
- Implemented Step 1 of the JCR matching workflow: extract a local unique journal list from existing paper data.

### Edited Files
- `scripts/extract_unique_journals.py`: added a local-only JSON/CSV journal extraction script with journal normalization, ISSN normalization, ISSN/name-based deduplication, and manual-review flags.
- `docs/jcr_step1_extract_unique_journals.md`: documented the Step 1 purpose, input/output paths, command usage, output columns, normalization behavior, and the no-scraping/no-JCR-matching boundary.
- `.gitignore`: explicitly ignored `data/private/journals_to_match_jcr.csv` and `data/private/journals_to_match_jcr.json`.
- `AGENT_LOG.md`: recorded this implementation and validation.

### Implemented Features
- Default input is `data/papers.json`, the current active source-of-truth paper database.
- Default outputs are:
  - `data/private/journals_to_match_jcr.csv`
  - `data/private/journals_to_match_jcr.json`
- Supports JSON and CSV input through `--input`.
- Supports custom CSV and JSON output paths through `--output` and `--json-output`.
- Extracts journal names from fields such as `journal`, `venue`, `container-title`, `container_title`, `publication`, `source_title`, and related aliases.
- Extracts ISSN/eISSN-like values from fields such as `issn`, `ISSN`, `issn_l`, `eissn`, `EISSN`, and related aliases.
- Produces columns requested for later manual JCR matching: `journal_id`, `journal_original`, `journal_normalized`, `issn`, `eissn`, `all_issns`, `paper_count`, `example_doi`, `example_title`, `example_year`, `source_fields`, `manual_review_required`, and `review_note`.

### Validation
- Ran `python scripts/extract_unique_journals.py`.
- Input paper data path: `data/papers.json`.
- Total papers read: 1,155.
- Total unique journals extracted: 428.
- Journals with ISSN/eISSN: 297.
- Journals missing ISSN/eISSN: 131.
- Journals requiring manual review: 143.
- Ran `python -m py_compile scripts/extract_unique_journals.py`.
- Confirmed generated private outputs are ignored by Git.

### Design Decisions
- Did not scrape or query Web of Science, JCR, Clarivate, Crossref, OpenAlex, or publisher pages.
- Did not perform JCR matching in this step.
- Did not modify existing paper data files, update workflows, or website runtime files.
- Used ISSN/eISSN grouping when available; otherwise used normalized journal names.
- Marked missing journal names, missing ISSNs, repository/conference/archive-like venues, ambiguous names, and inconsistent ISSN groups for manual review.

### Remaining Work
- Step 2 should load the manually exported JCR CSV and match it against `data/private/journals_to_match_jcr.csv`.
- Before Step 2, manually review high-count missing-journal rows and repository/preprint venue rows.

### Notes
- The generated CSV/JSON outputs are private intermediate files and were not committed.

## 2026-06-19 12:34

### Change Summary
- Reduced the startup paper index payload by moving non-first-paint provenance fields into lazy detail chunks.

### Edited Files
- `scripts/build_split_data.py`: removed Crossref/OpenAlex provenance, ISSN, publisher, raw safety flags, and core-source compatibility fields from the startup index; these fields remain in detail chunks.
- `scripts/build_split_data.py`: compacted startup corresponding-author data to name plus corresponding flag.
- `data/papers_index.json`, `data/archive_papers_index.json`, `data/details/`, `data/archive_details/`: regenerated split data with the smaller startup index.
- `AGENT_LOG.md`: recorded this payload reduction.

### Implemented Features
- Startup index now focuses on first-paint fields: id, title, authors, year, venue, DOI/URL, source, categories, tags, score, dates, summary provider, OpenAI flag, compact corresponding authors, core flag, and status.
- Heavier metadata remains available after `Load details` through the detail chunk system.

### Performance Notes
- `data/papers_index.json` changed from about 2.0 MB raw / 194 KB gzip to about 1.1 MB raw / 142 KB gzip.
- Compared with full `data/papers.json`, startup active paper data is now about 80% smaller raw and about 64% smaller gzip.
- Split-data report shows about 81.1% raw initial-load reduction against active+archive source JSON.

### Validation
- Regenerated split data with `python scripts/build_split_data.py`.
- Verified `data/papers_index.json` still contains 1,155 active records.
- Verified 711 startup records still expose compact `corresponding_authors`.
- Ran `python -m py_compile scripts/build_split_data.py`.

### Design Decisions
- Kept `source` in the startup index for lightweight provenance.
- Moved detailed provenance such as `metadata_source`, `crossref_type`, ISSN, publisher, OpenAlex cross-check ids, and core-source labels to lazy detail chunks.
- Did not change source-of-truth `data/papers.json`.

### Remaining Work
- If the site still feels heavy, the next step is chunked startup loading by year/topic instead of loading all 1,155 index records at once.

### Notes
- No OpenAI API was used.

## 2026-06-19 12:24

### Change Summary
- Improved frontend responsiveness after the split-data payload optimization.

### Edited Files
- `assets/app.js`: added runtime paper caches for derived field, visible tags, subtopics, canonical tag set, normalized venue, summary provider, and search text.
- `assets/app.js`: changed filtering, venue counting, filter option building, sidebar counts, and grouping to reuse cached runtime values.
- `assets/app.js`: debounced search input by 120 ms and reduced initial/load-more render batches from 120 to 80 cards.
- `index.html`: bumped asset query version to `20260619-filter-cache`.
- `AGENT_LOG.md`: recorded this performance pass.

### Implemented Features
- Initial network payload remains reduced by loading `data/papers_index.json` instead of `data/papers.json`.
- Typing in the search field no longer triggers full filtering on every keystroke immediately.
- Repeated filter/render operations avoid recomputing expensive topic/tag/search strings for all papers.

### Performance Notes
- Current raw JSON sizes:
  - `data/papers.json`: about 5.6 MB raw, 391 KB gzip.
  - `data/papers_index.json`: about 2.0 MB raw, 194 KB gzip.
- Initial JSON payload is about 65% smaller raw than loading active+archive source JSON, and about 50% smaller gzip than active full JSON alone.
- Remaining perceived lag is mostly browser-side parsing/filtering/rendering for 1,155 paper records, not only network transfer.

### Validation
- Confirmed `index.html` now references `assets/app.js?v=20260619-filter-cache`.
- Confirmed gzip/raw size estimates after the change.
- Could not run `node --check` because Node.js is not installed in the local shell environment.
- Browser automation tools were not available in this session, so visual runtime verification was not performed.

### Remaining Work
- For a larger speedup, generate a smaller `papers_index.json` by removing fields not needed for first paint or by splitting index pages by year/topic.
- Consider moving search/filter work into a Web Worker if the dataset grows beyond the current 1,155 records.
- Consider virtual scrolling if rendering hundreds of cards becomes necessary.

### Notes
- No OpenAI API was used.

## 2026-06-19 12:10

### Change Summary
- Fixed HTML entity display so venue names such as `ACS Applied Materials &amp; Interfaces` and `Materials &amp; Design` render with `&`.

### Edited Files
- `assets/app.js`: added `displayText()` and applied it to venue normalization, venue cards, title rendering, and HTML escaping.
- `index.html`: bumped CSS/JS asset query version to `20260619-display-entities`.
- `AGENT_LOG.md`: recorded this display fix.

### Implemented Features
- Crossref HTML entities are decoded for display before being safely escaped again.
- Venue board labels now show `ACS Applied Materials & Interfaces` and `Materials & Design`.
- Venue matching still treats `&amp;` and `&` as the same venue.

### Validation
- Confirmed `displayText("ACS Applied Materials &amp; Interfaces")` maps to `ACS Applied Materials & Interfaces`.
- Confirmed `displayText("Materials &amp; Design")` maps to `Materials & Design`.
- Confirmed `index.html` now references `assets/app.js?v=20260619-display-entities`.

### Design Decisions
- Decoded entities only for UI display/matching; source JSON was not rewritten.
- Kept escaping after decoding so rendered text remains safe in `innerHTML`.

### Notes
- No OpenAI API was used.

## 2026-06-19 12:03

### Change Summary
- Fixed GitHub Pages asset cache busting so the newly added core venues appear in the venue board.

### Edited Files
- `index.html`: changed CSS/JS asset query version from `20260618-aml-score-reason` to `20260619-core-venues`.
- `AGENT_LOG.md`: recorded the cache-busting fix.

### Implemented Features
- Forces browsers and GitHub Pages to load the updated `assets/app.js` containing `ACS Applied Materials & Interfaces` and `Materials & Design` in `TARGET_VENUES`.

### Verification
- Confirmed `data/papers_index.json` contains 1 ACS AMI record and 11 Materials & Design records.
- Confirmed the same normalization used by the UI matches Crossref HTML entity venue names such as `Materials &amp; Design`.

### Design Decisions
- Did not change paper data again; the previous core data patch was already correct.
- Treated this as a deployment/cache visibility fix.

### Remaining Work
- Wait for GitHub Pages deployment after push, then hard-refresh the browser if the old JS is still cached locally.

### Notes
- No OpenAI API was used.

## 2026-06-19 11:55

### Change Summary
- Temporarily promoted `ACS Applied Materials & Interfaces` and `Materials & Design` to core venues.

### Edited Files
- `assets/app.js`: added both venues to `TARGET_VENUES` and fixed venue-key normalization for Crossref HTML entities such as `&amp;`.
- `scripts/update_papers.py`: added ACS AMI to the manual core manufacturing journal rule and normalized venue names with HTML entity decoding before journal-quality checks.
- `scripts/full_rebuild_crossref_dataset.py`: changed full rebuild finalization so manual core journal quality sets `is_core_venue`, `core_status`, `venue_scope`, and `core_source` instead of leaving all records as placeholder non-core.
- `data/papers.json`: updated existing ACS AMI and Materials & Design records to temporary core status.
- `data/papers.csv`, `data/papers.xlsx`: regenerated active exports from the updated active dataset.
- `data/papers_index.json`, `data/details/`: regenerated public split data.
- `AGENT_LOG.md`: recorded this temporary core-venue promotion.

### Implemented Features
- The venue board treats ACS AMI and Materials & Design as core venues.
- Existing records from those venues are marked with `is_core_venue=true`, `core_status=core`, and `venue_scope=core`.
- Future Crossref-only rebuilds will mark manual core journals as core rather than placeholder non-core.

### Verification
- `ACS Applied Materials & Interfaces`: 1 active paper, 1 marked core.
- `Materials & Design`: 11 active papers, 11 marked core.
- `data/papers_index.json` contains the same core status for those 12 active records.
- Ran `python -m py_compile scripts/fetch_crossref.py scripts/full_rebuild_crossref_dataset.py scripts/build_split_data.py scripts/update_papers.py`.

### Design Decisions
- Used a temporary manual core label rather than inventing JIF/Q ranking.
- Kept OpenAlex limited to corresponding-author DOI cross-check; no paper collection source change.

### Remaining Work
- Later replace temporary core labels with a stable curated core venue policy or licensed JCR/Scopus data if needed.

### Notes
- No OpenAI API was used.
- No PDFs or raw publisher abstracts were downloaded or stored.

## 2026-06-19 11:41

### Change Summary
- Added Crossref ISSN-targeted venue search for `ACS Applied Materials & Interfaces` and `Materials & Design`.
- Verified whether those venues already exist in the current active/archive dataset.

### Edited Files
- `scripts/fetch_crossref.py`: added `fetch_crossref_by_issn_query()` and a venue-specific max-page guard through `CROSSREF_VENUE_MAX_PAGES`.
- `scripts/full_rebuild_crossref_dataset.py`: added Crossref ISSN venue collection from `data/crossref_venue_queries.json` and provenance fields for the collection route.
- `scripts/build_split_data.py`: added the new Crossref venue collection provenance fields to the startup index.
- `data/crossref_venue_queries.json`: added ISSN-based target searches for ACS AMI and Materials & Design.
- `reports/crossref_target_venue_check_20260619.md`: recorded the current-dataset check and Crossref ISSN probe results.
- `README.md`, `ARCHITECTURE.md`, `PROJECT_STATUS.md`: documented the new Crossref ISSN target venue search behavior.
- `AGENT_LOG.md`: recorded this change.

### Implemented Features
- ACS AMI and Materials & Design can now be searched through Crossref by ISSN plus topical query.
- The full rebuild still keeps paper discovery Crossref-only.
- OpenAlex remains limited to DOI-based missing corresponding-author completion.
- Venue-targeted Crossref records carry `crossref_collection_route`, `crossref_target_venue`, and `crossref_target_issn` provenance.

### Verification
- Current active dataset check:
  - `ACS Applied Materials & Interfaces`: 1 active paper, 0 archived papers.
  - `Materials & Design`: 11 active papers, 0 archived papers.
- Crossref ISSN lookup confirmed:
  - ACS AMI: `1944-8244`, `1944-8252`.
  - Materials & Design: `0264-1275`.
- Crossref works probes with ISSN filters returned relevant 2024-2026 additive manufacturing records from both venues.
- Ran `python -m py_compile scripts/fetch_crossref.py scripts/full_rebuild_crossref_dataset.py scripts/build_split_data.py`.

### Design Decisions
- Did not use Crossref journal title query as the primary mechanism because it was unreliable for these venue names.
- Used HTML entity normalization during verification because Crossref stores these venues as `ACS Applied Materials &amp; Interfaces` and `Materials &amp; Design` in local JSON.
- Used ISSN-filtered Crossref works search instead of publisher crawling or OpenAlex discovery.
- Set venue search to default to one cursor page through `CROSSREF_VENUE_MAX_PAGES=1` to prevent unbounded local/API runs.

### Remaining Work
- Run the scheduled/manual `Update papers` workflow to rebuild the public dataset with the new venue-targeted candidates.
- Review newly added ACS AMI and Materials & Design records after rebuild to tune query specificity if needed.

### Notes
- No OpenAI API was used.
- No PDFs or raw publisher abstracts were downloaded or stored.

## 2026-06-19 11:29

### Change Summary
- Fixed corresponding-author visibility in the GitHub Pages startup data and paper card rendering.

### Edited Files
- `scripts/build_split_data.py`: added compact `corresponding_authors` entries to the lightweight startup index while omitting empty arrays and reducing each corresponding-author record to display-safe fields.
- `assets/app.js`: updated author rendering so fallback author lists can still mark OpenAlex-cross-checked corresponding authors when full `author_details` have not been lazy-loaded yet.
- `data/papers_index.json`, `data/archive_papers_index.json`, `data/details/`, `data/archive_details/`: regenerated split data from the existing Crossref-only source JSON files.
- `AGENT_LOG.md`: recorded this visibility fix.

### Implemented Features
- Corresponding authors completed by OpenAlex DOI cross-check are now visible from the initial paper index.
- Initial card rendering can display the corresponding-author badge even before a detail chunk is loaded.

### Design Decisions
- Did not rerun Crossref collection or OpenAlex DOI enrichment; this was a presentation/indexing fix only.
- Kept OpenAlex as corresponding-author cross-check provenance only, not a paper discovery source.
- Stored only compact corresponding-author display fields in the startup index to avoid undoing the previous initial-payload reduction.

### Validation
- Verified active startup index has 1,155 records.
- Verified 711 active records expose `corresponding_authors` in `data/papers_index.json`.
- Verified 16 archived records expose `corresponding_authors` in `data/archive_papers_index.json`.
- Verified no empty `corresponding_authors` arrays remain in the active startup index.
- Ran `python -m py_compile scripts/build_split_data.py`.

### Remaining Work
- If richer corresponding-author details are desired on cards, load full detail chunks on demand rather than expanding the startup index further.

### Notes
- Crossref is still the only paper collection source in the rebuilt dataset.
- OpenAlex is used only for DOI-based missing corresponding-author completion.

## 2026-06-19 11:11

### Change Summary
- Replaced the scheduled metadata collection pipeline with a Crossref-only full rebuild flow and executed the rebuild locally.

### Edited Files
- `scripts/full_rebuild_crossref_dataset.py`: added the full rebuild orchestrator. It archives current outputs, ignores existing paper records as input, searches Crossref from scratch, de-duplicates Crossref results, optionally completes missing corresponding authors through OpenAlex DOI lookup only, and exports JSON/CSV/XLSX.
- `scripts/fetch_crossref.py`: expanded Crossref normalization to include author details, ISSN, ISSN-L, publisher, Crossref type, metadata provenance, and any Crossref-provided corresponding-author flags.
- `scripts/build_split_data.py`: added Crossref provenance, OpenAlex cross-check, and core/non-core compatibility fields to the startup index.
- `.github/workflows/update-papers.yml`: changed the scheduled update from `scripts/update_papers.py` to `scripts/full_rebuild_crossref_dataset.py`; removed Semantic Scholar/OpenAlex search-related environment use from the update step; added CSV/XLSX/backup outputs to the commit step.
- `requirements.txt`: added `openpyxl` for XLSX export.
- `data/papers.json`: replaced the previous dataset with 1,155 active records from the Crossref-only rebuild.
- `data/archive_papers.json`: replaced the previous archive with 48 archived records from the same Crossref-only rebuild.
- `data/papers.csv`: created the active dataset CSV export.
- `data/papers.xlsx`: created the active dataset XLSX export.
- `data/site_meta.json`: recorded `collection_mode=full_rebuild_crossref_only`, `sources=["Crossref"]`, backup path, and OpenAlex corresponding-author completion stats.
- `data/papers_index.json`, `data/archive_papers_index.json`, `data/detail_manifest.json`, `data/archive_detail_manifest.json`, `data/details/`, `data/archive_details/`: regenerated split GitHub Pages data.
- `data/old_exports/full_rebuild_20260619014047/`: stored compressed backups of the previous active/archive JSON, split data, and site metadata before overwrite.
- `README.md`, `ARCHITECTURE.md`, `PROJECT_STATUS.md`: documented the new Crossref-only full rebuild architecture, outputs, and verification results.
- `AGENT_LOG.md`: recorded this handoff entry.

### Implemented Features
- Full rebuild mode enabled.
- Existing paper dataset archived before overwrite.
- Existing dataset ignored for new collection.
- Crossref-only search started and completed from `data/queries.json`.
- Priority venue search disabled.
- OpenAlex general search disabled.
- OpenAlex used only for missing corresponding author DOI cross-check.
- New Crossref-based dataset exported to JSON, CSV, and XLSX.
- Core/non-core compatibility fields preserved as placeholders.

### Rebuild Results
- Crossref raw records after relevance filters: 2,762.
- De-duplicated Crossref records: 1,203.
- Active curated records: 1,155.
- Archived records: 48.
- Records with `source=["Crossref"]`: 1,203.
- Records with `OpenAlex` in `source`: 0.
- OpenAlex DOI checks for missing corresponding author: 1,203.
- Corresponding-author entries completed from OpenAlex: 727.
- CSV rows including header: 1,156.
- XLSX rows including header: 1,156.

### Design Decisions
- Did not reuse existing `data/papers.json` or `data/archive_papers.json` as seeds, merge inputs, or append targets.
- Kept `source` as `["Crossref"]` even when OpenAlex completed corresponding-author metadata, so paper discovery provenance stays clean.
- Stored OpenAlex use in explicit fields (`openalex_checked`, `openalex_used_for`, `openalex_crosscheck_work_id`, `corresponding_author_source`) instead of adding OpenAlex as a source.
- Preserved core/non-core schema fields for UI/export compatibility but did not use priority venue lists to assign them.
- Compressed old outputs under `data/old_exports/` to preserve rollback material without keeping duplicate raw JSON loose in the data root.

### Validation
- Verified every rebuilt record has `source=["Crossref"]`.
- Verified every rebuilt record has `metadata_source="crossref"`.
- Verified no rebuilt record has `OpenAlex` in the `source` array.
- Verified no OpenAlex-checked record lacks DOI.
- Verified `openalex_used_for` is either `null` or `corresponding_author_completion`.
- Verified core/non-core compatibility fields exist on all records.
- Verified `data/papers.csv`, `data/papers.xlsx`, and split GitHub Pages data were regenerated.
- Ran `python -m py_compile scripts/fetch_crossref.py scripts/full_rebuild_crossref_dataset.py scripts/build_split_data.py`.
- Ran `python scripts/build_split_data.py`.

### Remaining Work
- Review the 48 archived records and threshold behavior after seeing the new Crossref-only site output.
- If Crossref title searches miss known journals, add DOI/ISSN-based Crossref verification utilities separately; do not reintroduce OpenAlex as a discovery source.

### Notes / Cautions
- One Crossref query (`wavelength selective resin multimaterial 3D printing`) timed out during the local run; the job continued and completed successfully.
- Scheduled updates now perform full rebuilds, which are slower than the old incremental update.
- No OpenAI API was used.

## 2026-06-18 18:31

### Change Summary
- Corrected the venue reports from dataset provenance-only logic to verified API-coverage logic.

### Edited Files
- `reports/openalex_only_no_crossref_journal_match_venues_20260618.xlsx`: generated the verified OpenAlex-only venue report using the existing Crossref journal lookup result (`no_crossref_journal_match`).
- `reports/crossref_only_no_openalex_source_match_venues_20260618.xlsx`: generated the verified Crossref-only venue report using the existing OpenAlex source lookup result (`no_openalex_source_match`).
- `reports/source_overlap_openalex_no_crossref_venues_20260618.xlsx`: removed the previous provenance-only report.
- `reports/source_overlap_crossref_no_openalex_venues_20260618.xlsx`: removed the previous provenance-only report.
- `AGENT_LOG.md`: recorded this correction.

### Implemented Features
- Final OpenAlex-only report now means OpenAlex-observed venues with no Crossref journal match, not merely records whose local source field lacked Crossref.
- Final Crossref-only report now means Crossref-observed venues with no OpenAlex source match, not merely records whose local source field lacked OpenAlex.

### Design Decisions
- Reused the already verified `reports/api_source_coverage_report.xlsx` lookup sheets instead of rerunning external API checks.
- Used explicit filenames containing `no_crossref_journal_match` and `no_openalex_source_match` to avoid ambiguity.

### Remaining Work
- None for this correction.

### Notes / Cautions
- Verified OpenAlex-only venue count: 93.
- Verified Crossref-only venue count: 202.
- No OpenAI API was used.

## 2026-06-18 18:28

### Change Summary
- Corrected the source-overlap venue reports to include only the two requested groups.

### Edited Files
- `reports/source_overlap_openalex_no_crossref_venues_20260618.xlsx`: generated the exact OpenAlex records with no Crossref source venue report.
- `reports/source_overlap_crossref_no_openalex_venues_20260618.xlsx`: generated the exact Crossref records with no OpenAlex source venue report.
- `reports/source_overlap_only_openalex_venues_20260618.xlsx`: removed the earlier less-explicit OpenAlex-only filename.
- `reports/source_overlap_only_crossref_venues_20260618.xlsx`: removed the earlier less-explicit Crossref-only filename.
- `reports/source_overlap_both_venues_20260618.xlsx`: removed because the user asked for only OpenAlex-no-Crossref and Crossref-no-OpenAlex.
- `AGENT_LOG.md`: recorded this correction.

### Implemented Features
- Final report output now has exactly two Excel files:
  - OpenAlex with no Crossref.
  - Crossref with no OpenAlex.

### Design Decisions
- Removed the `Both` report entirely because it was outside the user's corrected scope.
- Used explicit `NO Crossref` / `NO OpenAlex` naming to avoid ambiguity.

### Remaining Work
- None for this correction.

### Notes / Cautions
- The counts are based on current local dataset provenance after DOI/title de-duplication.
- No OpenAI API was used.

## 2026-06-18 18:26

### Change Summary
- Replaced the combined source-overlap workbook with exactly the three requested venue Excel files.

### Edited Files
- `reports/source_overlap_only_openalex_venues_20260618.xlsx`: generated the OpenAlex-only venue list only.
- `reports/source_overlap_only_crossref_venues_20260618.xlsx`: generated the Crossref-only venue list only.
- `reports/source_overlap_both_venues_20260618.xlsx`: generated the venues observed in both OpenAlex and Crossref only.
- `reports/source_overlap_venues_recreated_20260618.xlsx`: removed the previous combined workbook because it included extra `Summary` and `All_Venues` sheets beyond the user's request.
- `AGENT_LOG.md`: recorded this report replacement.

### Implemented Features
- Created three separate Excel files instead of one multi-sheet report.
- Each file contains only venue rows for its source group, with columns for all/site/archive paper counts and sample titles.

### Design Decisions
- Kept the same DOI-first, normalized-title fallback paper identity logic from the previous analysis.
- Removed the extra combined report to avoid confusion, because the user asked for only the groups they mentioned.

### Remaining Work
- None for this report correction.

### Notes / Cautions
- These reports describe current local dataset provenance, not universal API coverage.
- No OpenAI API was used.

## 2026-06-18 18:24

### Change Summary
- Recreated the OpenAlex / Crossref / Both venue coverage Excel report.

### Edited Files
- `reports/source_overlap_venues_recreated_20260618.xlsx`: generated a new workbook with `Summary`, `Only_OpenAlex_Venues`, `Only_Crossref_Venues`, `Both_Venues`, and `All_Venues` sheets.
- `AGENT_LOG.md`: recorded the recreated report and counting method.

### Implemented Features
- Recomputed source groups from current `data/papers.json` and `data/archive_papers.json`.
- Used DOI-first and normalized-title fallback de-duplication for paper identity.
- Counted active site papers separately from archive papers.
- Grouped venues by observed source provenance:
  - Only OpenAlex
  - Only Crossref
  - Both OpenAlex + Crossref

### Design Decisions
- Created one consolidated Excel workbook instead of several separate files so the report is easier to keep and compare.
- Kept `All_Venues` as group-specific venue rows, meaning the same venue can appear in more than one source group; the `Summary` sheet contains the unique venue counts.

### Remaining Work
- None for this report recreation.

### Notes / Cautions
- This report describes source provenance in the current local dataset, not universal API coverage for every journal.
- No OpenAI API was used.

## 2026-06-18 15:37

### Change Summary
- Added a paper-specific explanation for AML recommendation scores.

### Edited Files
- `assets/app.js`: expanded AML relevance notes with a `Why this score:` sentence based on matched topics, discovery route, and closest seed paper when available.
- `assets/app.js`: normalized repeated LCE topic variants so notes do not show duplicates such as `LCE, LCE`.
- `index.html`: bumped the frontend asset cache version for the updated AML note renderer.
- `AGENT_LOG.md`: recorded this AML score-explanation change.

### Implemented Features
- AML cards now explain the reason for the displayed score, not just the score calculation scale.
- Example output: `Relevant to the tracker through LCE and Soft Robotics; AML score: 66/100. Why this score: matched LCE and Soft Robotics and found through existing keyword pool.`

### Design Decisions
- Did not expose the raw deterministic scoring formula in every card, because the user already understands the calculation and wants item-level reasoning.
- Used existing public recommendation metadata only; no new API calls were made.

### Remaining Work
- None for this UI explanation update.

### Notes / Cautions
- No data files were changed.
- OpenAI API was not used.

## 2026-06-18 15:36

### Change Summary
- Revised the AML recommendation relevance sentence to use the actual AML score scale.

### Edited Files
- `assets/app.js`: changed AML relevance notes from `score: x/10` to `AML score: xx/100` and removed duplicate matched-topic labels before rendering.
- `index.html`: removed the separate AML score explanation sentence from the section heading and bumped the asset cache version.
- `assets/style.css`: removed the now-unused AML score explanation style.
- `AGENT_LOG.md`: recorded this AML score wording correction.

### Implemented Features
- AML recommendation cards now show relevance notes such as `Relevant to the tracker through LCE and Soft Robotics; AML score: 66/100.`
- Duplicate matched topics such as `LCE, LCE` are collapsed in the displayed note.

### Design Decisions
- Used the same 0-100 AML score scale shown in the card badge to avoid implying a separate 10-point relevance score.
- Removed the section-level explanation because the user wanted the card sentence itself corrected instead.

### Remaining Work
- None for this wording correction.

### Notes / Cautions
- No data files were changed.
- OpenAI API was not used.

## 2026-06-18 15:32

### Change Summary
- Explained the AML recommendation score in the UI and removed the recommendation-level badge from AML cards.

### Edited Files
- `index.html`: added a short AML score explanation under the AML Recommendation Engine heading and bumped the asset cache version.
- `assets/app.js`: removed the visible `High` / `Possible` / `Watch` badge from AML recommendation cards and simplified the empty-state copy.
- `assets/style.css`: added lightweight spacing for the AML score explanation.
- `AGENT_LOG.md`: recorded this display and explanation update.

### Implemented Features
- AML cards now show only the numerical `AML xx/100` score in the topline.
- The AML section explains that the score is a 0-100 profile-match score based on seed-paper similarity, topic overlap, discovery route, recency, and venue signal.

### Design Decisions
- Kept the internal recommendation-level field for filtering and pipeline logic, but removed it from the public card UI because `Possible` and `Watch` were unclear as badges.
- Clarified that AML score is not a journal ranking or impact metric.

### Remaining Work
- None for this UI clarification.

### Notes / Cautions
- No data files were changed.
- OpenAI API was not used.

## 2026-06-18 15:29

### Change Summary
- Moved the AML score reason out of the card badge area and into the normal card body.

### Edited Files
- `assets/app.js`: removed the `Reason:` badge from AML recommendation cards and added a normal relevance-note sentence using the template `Relevant to the tracker through ...; score: .../10.`
- `assets/style.css`: removed the unused `score-reason-badge` styling and dark-mode override.
- `index.html`: bumped the frontend asset cache version so GitHub Pages loads the updated UI files.
- `AGENT_LOG.md`: recorded this AML recommendation-card display change.

### Implemented Features
- AML recommendation cards now show the reason as text in the body, not as a badge.
- The reason uses up to three matched topics and converts the AML score to a 10-point display.

### Design Decisions
- Kept the score badge as the compact AML score indicator.
- Treated the explanation as reading content rather than metadata, because the user wanted the reason template but explicitly not as a badge.

### Remaining Work
- None for this UI correction.

### Notes / Cautions
- No data files were regenerated.
- OpenAI API was not used.

## 2026-06-18 16:02

### Change Summary
- Removed Korean-language content from tracked public/source JSON files.

### Edited Files
- `data/papers.json`: removed Korean duplicate fields, removed Korean tags, converted categories to English, and romanized the remaining Korean author names.
- `data/archive_papers.json`: removed Korean duplicate fields, removed Korean tags, and converted categories to English.
- `data/papers_index.json`, `data/archive_papers_index.json`, `data/details/detail_001.json`: regenerated split data from the cleaned source JSON.
- `scripts/summarize.py`: changed the fallback category from Korean `다중재료 적층제조` to English `Multi-material AM`.
- `scripts/update_papers.py`: changed the stored default category from Korean to English.
- `AGENT_LOG.md`: recorded this English-only JSON cleanup.

### Implemented Features
- Tracked JSON files no longer contain Korean duplicate fields such as `ai_summary_ko`, `relevance_note_ko`, or `archive_note_ko`.
- Korean category values were replaced with English category names.
- Korean tags were removed from source JSON and regenerated split JSON.
- Remaining Korean author names were replaced with English forms:
  - `심수안` -> `Suan Sim`
  - `전승배` -> `Seungbae Jeon`

### Design Decisions
- Removed Korean tags instead of machine-translating thousands of low-signal API tags, because many were noisy and not central to the current English UI.
- Preserved source-of-truth `data/papers.json` and `data/archive_papers.json` paths.
- Regenerated split files after source cleanup so GitHub Pages continues to use the lightweight English-only public data.

### Validation
- Scanned all tracked `*.json` files for Hangul characters, `_ko` keys, `korean` keys, and `translated_` keys: 0 hits.
- Ran `python scripts/build_split_data.py`.
- Ran `python -m py_compile scripts/summarize.py scripts/update_papers.py scripts/build_split_data.py`.

### Remaining Work
- If future metadata APIs return non-English author display names, decide whether to romanize from trusted source metadata or omit only that name.

### Notes / Cautions
- OpenAI API was not used.
- Name romanization was checked against public metadata/search results before replacement.

## 2026-06-18 15:44

### Change Summary
- Reduced initial GitHub Pages paper-data payload by splitting full paper JSON into lightweight indexes and lazy-loaded detail chunks.

### Edited Files
- `scripts/build_split_data.py`: added deterministic split-data generator with size reporting and Korean duplicate field stripping.
- `data/papers_index.json`: generated lightweight active-paper index for startup filtering/sorting/rendering.
- `data/archive_papers_index.json`: generated lightweight archive index for future archive browsing.
- `data/detail_manifest.json`: generated active paper id to detail chunk mapping.
- `data/archive_detail_manifest.json`: generated archive paper id to detail chunk mapping.
- `data/details/detail_*.json`: generated active detail chunks.
- `data/archive_details/archive_detail_*.json`: generated archive detail chunks.
- `assets/app.js`: changed startup fetch from full `data/papers.json` to `data/papers_index.json`, added local fallback warning, lazy detail chunk loading/caching, detail loading/error states, and first-page render limiting.
- `index.html`: added `Load more papers` control and bumped asset cache version.
- `assets/style.css`: added minimal `Load more` and detail error styling.
- `.github/workflows/update-papers.yml`: runs split generation after paper update and commits split outputs.
- `.github/workflows/refresh-openai-summaries.yml`: runs split generation after manual OpenAI summary refresh when not dry-run.
- `.github/workflows/enrich-openalex-metadata.yml`: runs split generation after OpenAlex metadata enrichment.
- `ARCHITECTURE.md`, `README.md`, `PROJECT_STATUS.md`: documented split loading, regeneration, testing, and size results.
- `AGENT_LOG.md`: recorded this performance refactor.

### Implemented Features
- Production startup loads `data/papers_index.json` instead of the 10.8 MB full `data/papers.json`.
- The archive split files are generated but not loaded at startup.
- Paper details are loaded lazily from `data/details/detail_*.json` only after clicking `Load details`.
- Loaded detail chunks are cached in memory.
- The paper list renders only the first 120 filtered records initially, with `Load more papers` for incremental rendering.
- Generated split public JSON files remove Korean duplicate keys such as `ai_summary_ko`, `relevance_note_ko`, and `archive_note_ko`.

### Design Decisions
- `data/papers.json` and `data/archive_papers.json` remain source-of-truth files for automation and were not moved.
- Summary text and detailed authorship moved to detail chunks because they dominate payload size.
- Initial search no longer includes unloaded summary text; once a detail is loaded, its summary text participates in search.
- A full `data/papers.json` fallback remains for local development only when `papers_index.json` is missing, and the UI logs/shows an error first.

### Size Report
- Original active `papers.json`: 10,781.5 KB.
- Original archive `archive_papers.json`: 11,323.6 KB.
- Combined original: 22,105.0 KB.
- New active `papers_index.json`: 1,488.4 KB.
- New archive `archive_papers_index.json`: 1,839.4 KB, not loaded at startup.
- Active detail chunks total: 7,914.3 KB.
- Archive detail chunks total: 7,745.0 KB.
- Estimated default initial paper JSON load reduction: 93.3%.

### Validation
- Ran `python scripts/build_split_data.py`.
- Verified generated split files contain zero Korean duplicate keys.
- Ran `python -m py_compile scripts/build_split_data.py scripts/update_papers.py scripts/collect_aml_candidates.py scripts/aml_common.py`.
- Verified `assets/app.js` references `data/papers_index.json` for startup and only keeps `data/papers.json` as fallback.

### Remaining Work
- Browser Network tab should be checked after deployment: startup should show `data/papers_index.json`, not full `data/papers.json` or `data/archive_papers.json`; `data/details/detail_*.json` should appear only after clicking `Load details`.
- Add an archive UI later if archived papers should be user-browsable.

### Notes / Cautions
- OpenAI API was not used.
- No backend, API key exposure, PDF storage, or publisher crawling was added.

## 2026-06-18 15:18

### Change Summary
- Added a visible score-reason badge to AML recommendation cards.

### Edited Files
- `assets/app.js`: added `formatAmlScoreReason()` and rendered a compact `Reason: ...` badge next to the AML score.
- `assets/style.css`: styled the score-reason badge and added a dark-mode override so it does not inherit the amber last-badge styling.
- `index.html`: bumped asset cache versions to `20260618-aml-score-reason`.
- `AGENT_LOG.md`: recorded this score-explanation UI change.

### Implemented Features
- AML cards now keep the `Possible` / `Watch` badge and show a nearby reason badge.
- The reason badge uses matched topics when available, otherwise seed similarity, discovery route, or profile match.
- Hovering the reason badge exposes the full `why_recommended` text through the title attribute.

### Design Decisions
- Kept the score explanation compact to avoid making the card header too heavy.
- The full score rationale remains in the Q5 Takeaway as readable text.

### Remaining Work
- Verify the deployed GitHub Pages UI after cache refresh.

### Notes / Cautions
- OpenAI API was not used.

## 2026-06-18 15:11

### Change Summary
- Added corresponding-author support to AML recommendation cards.

### Edited Files
- `scripts/collect_aml_candidates.py`: preserved `author_details`, `corresponding_authors`, and `corresponding_author_available` when collecting AML candidates.
- `scripts/aml_common.py`: included public-safe author detail and corresponding-author fields in AML public recommendation output.
- `public/data/aml_recommended_papers.json`: enriched current AML recommendations with author metadata from `data/papers.json`.
- `AGENT_LOG.md`: recorded this authorship metadata change.

### Implemented Features
- AML recommendation cards can now display the same author chips and corresponding-author badges as normal paper cards.
- Current public AML recommendations now include detailed author metadata for 49 of 50 records.
- Current public AML recommendations now include corresponding authors for 34 of 50 records.

### Design Decisions
- Used existing public metadata from `data/papers.json`; no publisher crawling, PDF download, or raw abstract display was introduced.
- Reused the frontend's existing `renderAuthorDetails()` path instead of creating a separate AML-only author UI.

### Remaining Work
- Verify the deployed GitHub Pages UI after cache refresh.
- Future AML recommendation workflow runs will preserve corresponding-author fields when the source candidate has them.

### Notes / Cautions
- OpenAI API was not used.
- Validation confirmed the public AML JSON still has no `abstract` key.
- Tests run: `python -m py_compile scripts/collect_aml_candidates.py scripts/aml_common.py`.

## 2026-06-18 15:02

### Change Summary
- Made the AML recommendation section use the same comfortable grid spacing as the normal paper cards.

### Edited Files
- `assets/style.css`: aligned AML recommendation grid width and gaps with the main paper-card comfort layout, including desktop and mobile overrides.
- `index.html`: bumped asset cache versions to `20260618-aml-comfort`.
- `AGENT_LOG.md`: recorded this comfort-layout change.

### Implemented Features
- AML recommendation cards now use wider, more relaxed card columns.
- AML Q5 cards have spacing closer to the main curated paper cards.
- Mobile AML cards collapse to a single comfortable column.

### Design Decisions
- Comfort was handled as layout spacing, not as a restored compact/comfort toggle.
- The site remains default comfortable-only, as requested earlier.

### Remaining Work
- Check GitHub Pages visually after deployment.

### Notes / Cautions
- OpenAI API was not used.

## 2026-06-18 14:55

### Change Summary
- Added Q5-style summaries to AML recommendation cards so they match normal paper cards.

### Edited Files
- `assets/app.js`: added `renderAmlSummaryBlock()` and `amlSummarySections()`; AML recommendation cards now render the same `summary-qa` Q5 layout used by regular paper cards.
- `index.html`: bumped asset cache versions to `20260618-aml-q5`.
- `AGENT_LOG.md`: recorded this AML Q5 UI change.

### Implemented Features
- AML recommendation cards now show five sections: Topic, Problem, Method, Key Result, and Takeaway.
- The Q5 content is generated from public-safe recommendation metadata: title, venue, year, matched topics, discovery routes, AML score, recommendation reason, and nearest seed paper when available.

### Design Decisions
- AML Q5 is recommendation-oriented, not a full abstract summary. It avoids claiming detailed findings that are not present in the public recommendation data.
- The detailed method/result fields tell the user to check the DOI source when the recommendation data does not contain paper-level details.

### Remaining Work
- If richer AML paper abstracts are later available in a public-safe generated-summary field, map that field into the Q5 answers.

### Notes / Cautions
- OpenAI API was not used.
- Raw abstracts/PDFs are still not displayed or stored in public output.

## 2026-06-18 14:45

### Change Summary
- Changed AML recommendation cards to use the same visual/card structure as the main paper cards.

### Edited Files
- `assets/app.js`: reworked `renderAmlRecommendationCard()` to use the same card topline, title, author chips, summary, relevance note, tag line, links, copy citation button, and policy footer pattern as `renderPaperRow()`.
- `assets/style.css`: removed AML-specific publication badge and route styling so AML cards inherit the normal paper-card design.
- `index.html`: bumped asset cache versions to `20260618-aml-card`.
- `AGENT_LOG.md`: recorded this UI alignment.

### Implemented Features
- AML recommendation cards now visually match regular paper cards.
- AML cards now include `Open Paper`, `DOI`, and `Copy Cite` actions.
- AML score remains visible as a normal relevance-style badge.

### Design Decisions
- Kept only the content-specific labels (`Possible`, `Watch`, `AML xx/100`) while reusing the main paper-card design system.
- Removed the special AML route text block and moved route/update information into the same `policy-mini` area used by regular cards.

### Remaining Work
- Verify the deployed GitHub Pages UI after cache refresh.

### Notes / Cautions
- OpenAI API was not used.
- `node --check` is still unavailable locally because `node` is not in PATH.

## 2026-06-18 14:31

### Change Summary
- Corrected the AML sidebar behavior so `AML Recommendations` means opening the recommendation papers, not moving to the page top.
- Published the existing local AML scoring result as a public-safe recommendation JSON file.

### Edited Files
- `assets/app.js`: changed the AML sidebar shortcut badge from `Top` to `Open`, made the click always open the AML recommendation section, and added an explicit empty-state message when no public recommendation file exists.
- `assets/style.css`: added styling for the AML recommendation empty-state card.
- `index.html`: bumped asset cache versions to `20260618-aml-open`.
- `public/data/aml_recommended_papers.json`: generated 50 public-safe AML recommendation records from the existing local AML scoring debug output.
- `AGENT_LOG.md`: recorded this AML recommendation UI/data correction.

### Implemented Features
- Clicking `AML Recommendations` now opens the recommendation paper area.
- If recommendation data exists, the user sees related AML recommendation papers.
- If recommendation data is missing, the section explains that the manual AML Recommendation workflow needs to publish it.

### Design Decisions
- `Top` was removed from the button because the user meant top position only, not a button label or behavior.
- The public recommendation file uses the existing `public_paper()` sanitizer and does not include abstracts.
- The existing scheduled paper update workflow and public paper data paths were not changed.

### Remaining Work
- Confirm the deployed GitHub Pages UI after Pages finishes rebuilding.
- Future AML recommendation refreshes should be done through `Actions > AML Recommendation Manual`.

### Notes / Cautions
- OpenAI API was not used.
- Validation confirmed `public/data/aml_recommended_papers.json` has 50 records and no `abstract` key.
- Browser screenshot QA could not be run because the browser automation tool is not available in this session.

## 2026-06-18 14:18

### Change Summary
- Reinterpreted `AML` as the recommendation engine entry point, not as a paper keyword/subtopic.
- Moved AML access to the top of the left sidebar as `AML Recommendations`.

### Edited Files
- `assets/app.js`: removed `AML` from tag/subtopic classification logic and added a top sidebar shortcut that scrolls to the AML recommendation section when available.
- `assets/style.css`: added light/dark styling for the top `AML Recommendations` shortcut.
- `index.html`: bumped asset cache versions to `20260618-aml-top`.
- `AGENT_LOG.md`: recorded the correction.

### Implemented Features
- The left panel now starts with an `AML Recommendations` button.
- The button shows the number of visible AML recommendations when generated, otherwise it shows `Top`.
- `AML` no longer appears as a normal paper tag or AI Manufacturing subtopic.

### Design Decisions
- `AML` represents the manual recommendation workflow/section, so it should behave like a navigation shortcut rather than a taxonomy filter.
- Existing scheduled collection, public data fetch paths, and paper classification data remain unchanged.

### Remaining Work
- Verify on GitHub Pages after deployment that the top shortcut appears above all fields and that it scrolls correctly when recommendation output exists.

### Notes / Cautions
- OpenAI API was not used.
- This corrects the previous `AML` sidebar-topic implementation from commit `f148e6c`.

## 2026-06-18 14:07

### Change Summary
- Added `AML` as a visible keyword/subtopic in the left sidebar under `AI Manufacturing`.

### Edited Files
- `assets/app.js`: added `AML` to the AI Manufacturing sidebar subtopics, canonical tag labels, representative tag priority, and conservative AML signal detection.
- `index.html`: bumped asset cache versions to `20260618-aml-topic`.
- `AGENT_LOG.md`: recorded this sidebar keyword change.

### Implemented Features
- The left panel now shows `AML` as a selectable subtopic under `AI Manufacturing`.
- Papers with an explicit `AML` tag or a title/venue/tag signal such as standalone `AML`, `Advanced Manufacturing Lab`, or `Additive Manufacturing Lab` can be counted and filtered through the AML subtopic.

### Design Decisions
- `AML` was added as a UI/subtopic signal only; no existing data files or scheduled collection workflow were moved or changed.
- Matching uses a standalone `AML` acronym or manufacturing-lab phrase to reduce accidental matches against unrelated words.

### Remaining Work
- Verify the deployed GitHub Pages UI after cache refresh.
- If the intended meaning of `AML` should be broader than lab/manufacturing-lab wording, expand the matching terms later.

### Notes / Cautions
- OpenAI API was not used.
- `node --check` could not be run because `node` is not available in the local PATH.
- The existing website fetch paths remain unchanged: `data/papers.json`, `data/site_meta.json`, and `data/update_status.json`.

## 2026-06-17 23:03

### Change Summary
- Made every corresponding author use the same highlighted author-chip style.
- Restored the stronger corresponding-author highlight style requested by the user.

### Edited Files
- `assets/app.js`: removed the supplemental/prefix display variant so visible and extra corresponding authors render consistently with the same badge.
- `assets/style.css`: restored the stronger green chip and filled role badge while keeping the badge non-shrinking.
- `index.html`: bumped JS/CSS cache versions for GitHub Pages.
- `AGENT_LOG.md`: recorded the correction.

### Design Notes
- Corresponding authors are not moved into a separate visual category. They remain author chips and all use the same corresponding-author treatment.
- Extra corresponding authors outside the first visible author range are appended using the same chip style, not a different `Corresponding: name` style.

### Follow-up
- None.

## 2026-06-17 22:52

### Change Summary
- Unified corresponding-author chip styling with the rest of the paper-card design system.

### Edited Files
- `assets/style.css`: replaced the strong standalone green badge style with token-based chip colors and a subtle inline divider label.
- `index.html`: bumped JS/CSS cache versions for GitHub Pages.
- `AGENT_LOG.md`: recorded the design unification.

### Design Notes
- The corresponding-author state remains visible through green tinting and the inline role label, but now uses existing CSS variables so light/dark themes stay consistent.
- The badge still does not shrink, so long names cannot clip the role label.

### Follow-up
- None.

## 2026-06-17 22:45

### Change Summary
- Fixed long corresponding-author names causing the `Corresponding` badge to be clipped.

### Edited Files
- `assets/app.js`: wrapped author names in a dedicated `.author-chip-name` span so only the name text ellipsizes.
- `assets/style.css`: moved ellipsis behavior from the whole chip to the name span, widened corresponding-author chips, and made the badge non-shrinking.
- `index.html`: bumped JS/CSS cache versions for GitHub Pages.
- `AGENT_LOG.md`: recorded the UI fix.

### Design Notes
- The corresponding-author badge now remains visible even when the author name is long.
- Long names still truncate cleanly to keep paper cards compact.

### Follow-up
- None.

## 2026-06-17 22:33

### Change Summary
- Simplified author display so corresponding authors are highlighted inside the author list instead of shown in a separate repeated line.
- Increased corresponding-author highlight contrast.

### Edited Files
- `assets/app.js`: removed the separate corresponding-author row, keeps corresponding authors in the author chip list, and appends hidden corresponding authors as supplemental `Corresponding: Name` chips when they fall outside the visible author limit.
- `assets/style.css`: strengthened corresponding-author chip contrast and added dashed styling for supplemental corresponding-author chips.
- `index.html`: bumped JS/CSS cache versions for GitHub Pages.
- `AGENT_LOG.md`: recorded the display decision.

### Design Notes
- The UI now treats corresponding author as a role within the author list, avoiding duplicate names.
- If a corresponding author is beyond the first 8 visible authors, the UI still surfaces them as an extra highlighted chip.

### Follow-up
- None.

## 2026-06-17 22:20

### Change Summary
- Improved author and corresponding-author display on paper cards.
- Added OpenAlex DOI cross-check for Crossref-only records so missing detailed author and corresponding-author metadata can be filled when OpenAlex has it.

### Edited Files
- `assets/app.js`: hides the corresponding-author line when no corresponding author is available, localizes author labels, and replaces the unexplained `*` marker with an explicit corresponding-author badge.
- `assets/style.css`: added distinct styling for corresponding-author chips and badges.
- `scripts/update_papers.py`: new DOI-based OpenAlex cross-check path merges `author_details`, `corresponding_authors`, OpenAlex IDs, venue metrics, and missing metadata into Crossref-derived candidates.
- `index.html`: bumped JS/CSS cache versions for GitHub Pages.
- `AGENT_LOG.md`: recorded the UI and metadata pipeline change.

### Design Notes
- Missing corresponding-author metadata is now treated as "not provided by the metadata source" rather than shown as `No data`.
- The pipeline still does not infer corresponding authors. It only displays OpenAlex-provided `authorships.is_corresponding` when available.

### Follow-up
- Run or wait for the scheduled `Update papers` workflow to let Crossref-only records receive OpenAlex DOI cross-check enrichment.

## 2026-06-17 01:05
### 변경 요약
- 사용자가 OpenAlex-only venue가 실제로 Crossref에 없는 venue인지 확인하고 싶다고 요청하여, 기존 3,075 후보 기반 OpenAlex-only venue 428개를 Crossref journal lookup으로 재검사했습니다.
- 각 OpenAlex-only venue에 대해 Crossref `/journals?query=...&rows=20`를 호출하고 exact/possible/no match로 분류했습니다.
- `Nature`가 Crossref에 없는 것이 아니라, 현재 파이프라인에서 OpenAlex로만 수집된 것임을 확인했습니다.

### 수정/생성한 파일
- `reports/openalex_only_venues_crossref_check.md`: OpenAlex-only venue 428개에 대한 Crossref lookup 요약 보고서입니다.
- `reports/openalex_only_venues_crossref_check.csv`: 전체 OpenAlex-only venue별 Crossref lookup 결과 CSV입니다.
- `reports/openalex_only_venues_crossref_check.xlsx`: Excel 형식의 동일 분석 결과입니다.
- `AGENT_LOG.md`: 이번 분석 작업과 결론을 기록했습니다.

### 구현한 기능
- OpenAlex-only venue를 단순 pipeline 관측값과 Crossref 실제 journal coverage 관점으로 분리했습니다.
- Crossref exact title match, possible match, no match를 venue별로 기록했습니다.
- `Nature`는 Crossref exact journal match로 보정되어 `Nature` 자체가 Crossref에 없다는 오해를 제거했습니다.

### 설계 결정
- Crossref venue coverage 확인에는 DOI가 아니라 venue 이름 기반 `/journals` endpoint를 사용했습니다.
- `rows=20`까지 확인해 `Nature`처럼 query 결과 상위 8개 안에는 없지만 실제 exact title이 존재하는 경우를 보정했습니다.
- 이번 분석은 API coverage의 1차 판별용이며, 최종 논문 단위 coverage는 DOI-level lookup이 더 정확합니다.

### 결과 요약
- OpenAlex-only로 관측된 venue: 428개
- Crossref exact journal match: 332개
- Crossref possible journal match: 3개
- Crossref journal no match: 93개

### 남은 작업
- Crossref 중심 운영으로 전환하려면 `no_crossref_journal_match` venue들을 우선 제거/숨김 후보로 검토합니다.
- `exact_crossref_journal_match` venue들은 Crossref에 존재하므로, OpenAlex-only로 보이는 원인이 검색/병합 파이프라인 때문인지 DOI-level enrichment로 추가 확인할 수 있습니다.

### 주의사항
- OpenAI API는 사용하지 않았습니다.

## 2026-06-17 14:36
### 변경 요약
- 논문 카드에서 `Venue signal` / `Repository / preprint source (metadata source type)` 표시를 제거했습니다.
- 사용자가 지적한 `Repository / preprint source ... Topic`처럼 summary 앞에 붙는 venue quality line이 더 이상 렌더링되지 않습니다.

### 수정/생성한 파일
- `assets/app.js`: `qualityHtml` 삽입과 `renderJournalQuality` 함수를 제거했습니다.
- `assets/style.css`: `.quality-line` 관련 스타일을 제거했습니다.
- `index.html`: GitHub Pages cache busting query를 `20260617-no-venue-signal`로 갱신했습니다.
- `AGENT_LOG.md`: 이번 UI 제거 작업을 기록했습니다.

### 구현한 기능
- 카드에는 더 이상 `Venue signal` 또는 journal_quality 기반 문장이 표시되지 않습니다.
- 저장된 `journal_quality`/`venue_metrics` 데이터는 유지하여 향후 JCR/IF importer에 재사용할 수 있게 했습니다.

### 설계 결정
- 현재 단계에서는 JCR/IF 공식 데이터가 없으므로 venue quality 신호를 사용자-facing UI에서 숨기는 편이 더 명확하다고 판단했습니다.

### 남은 작업
- JCR manual export importer가 추가되면 공식 IF/Q만 별도 디자인으로 다시 표시할 수 있습니다.

### 주의사항
- OpenAI API는 사용하지 않았습니다.

## 2026-06-17 14:30
### 변경 요약
- 논문 카드 author 영역을 사용자 요청 형식에 맞게 다시 정리했습니다.
- `Corresponding Authors`는 항상 표시하고, 데이터가 없으면 `No data`를 표시하도록 변경했습니다.
- 기존 `Alin Bustihan, Ioan Botiz · Polymers · Crossref` 같은 compact meta line을 제거했습니다.
- `Authors:` / `Corresponding author:`의 colon을 제거했습니다.

### 수정/생성한 파일
- `assets/app.js`: old meta line 제거, `Corresponding Authors` 기본 표시, `Authors` 라벨 colon 제거를 적용했습니다.
- `index.html`: GitHub Pages cache busting query를 `20260617-author-no-meta`로 갱신했습니다.
- `AGENT_LOG.md`: 이번 카드 UI 변경을 기록했습니다.

### 구현한 기능
- Corresponding author metadata가 있으면 `Corresponding Authors 이름`을 표시합니다.
- Corresponding author metadata가 없으면 `Corresponding Authors No data`를 표시합니다.
- Authors는 기존 authors 배열 또는 OpenAlex author_details를 사용해 `Authors` 라벨 뒤 chip으로 표시합니다.

### 설계 결정
- Corresponding author가 없을 때 라인을 숨기면 사용자가 데이터 부재인지 UI 누락인지 알기 어렵기 때문에 `No data`를 명시했습니다.
- venue/source 반복 meta line은 카드 상단 publication badge 및 DOI/source context와 중복되어 제거했습니다.

### 남은 작업
- 전체 논문에 corresponding author coverage를 늘리려면 `Enrich OpenAlex metadata` workflow를 계속 실행해야 합니다.

### 주의사항
- OpenAI API는 사용하지 않았습니다.

## 2026-06-17 14:08
### 변경 요약
- `Enrich OpenAlex metadata` GitHub Actions 실패 원인을 분석하고, OpenAlex 개별 DOI lookup 실패가 workflow 전체 실패로 이어지지 않도록 수정했습니다.
- GitHub Actions의 Node.js 20 deprecation 경고를 줄이기 위해 Node 24 opt-in 환경변수를 추가했습니다.
- 로컬에서 추가 batch enrichment를 실행해 현재 85개 curated paper에 author/venue metadata가 들어간 상태를 만들었습니다.

### 수정/생성한 파일
- `.github/workflows/enrich-openalex-metadata.yml`: `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24=true`를 추가하고, OpenAlex rate limit 완화를 위해 `API_SLEEP_SECONDS=0.75`, `OPENALEX_RETRIES=6`으로 조정했습니다.
- `scripts/enrich_openalex_metadata.py`: DOI별 OpenAlex lookup 예외를 개별적으로 잡아 로그를 남기고 계속 진행하도록 수정했습니다.
- `data/papers.json`: 로컬 enrichment batch 결과로 85개 논문에 `author_details`/`journal_quality`가 있고, 46개 논문에 `corresponding_authors`가 채워졌습니다.
- `AGENT_LOG.md`: 실패 원인 분석과 수정 내용을 기록했습니다.

### 구현한 기능
- 특정 DOI에서 OpenAlex가 429/5xx/네트워크 오류를 반환해도 전체 workflow가 exit code 1로 실패하지 않고 해당 DOI만 skip합니다.
- workflow가 Node 24 JavaScript actions runtime을 사용하도록 명시했습니다.
- OpenAlex 요청 간격과 retry 횟수를 늘려 대량 enrichment 실행 안정성을 높였습니다.

### 설계 결정
- Corresponding author 보강은 best-effort metadata enrichment이므로, 일부 DOI 실패 때문에 전체 작업이 멈추는 것보다 skip 후 계속 진행하는 편이 안전하다고 판단했습니다.
- Node 20 메시지는 실패 원인이 아니라 warning이지만, 사용자 혼란을 줄이기 위해 workflow에서 Node 24 opt-in을 명시했습니다.

### 검증 결과
- `python -m py_compile scripts/enrich_openalex_metadata.py scripts/fetch_openalex.py scripts/update_papers.py` 통과.
- 로컬 `OPENALEX_ENRICH_MAX=80` batch가 성공적으로 완료되었습니다.
- 현재 `data/papers.json` 기준: 전체 1357편, author detail 85편, corresponding author 46편, journal quality 85편.

### 남은 작업
- GitHub Actions에서 `Enrich OpenAlex metadata`를 다시 실행하면 남은 논문도 계속 보강됩니다.
- 완전 보강에는 시간이 걸릴 수 있으므로, 필요하면 `max_records=200`처럼 나누어 실행할 수 있습니다.

### 주의사항
- OpenAI API는 사용하지 않았습니다.
- publisher page crawling, PDF download/storage, raw abstract display는 수행하지 않았습니다.

## 2026-06-17 14:20
### 변경 요약
- `Enrich OpenAlex metadata` workflow가 다시 exit code 1로 실패한 원인을 GitHub Actions push race condition으로 판단하고 완화했습니다.
- Node.js 20 메시지는 실패 원인이 아니라 warning이며, 실제 실패는 enrichment workflow 실행 중 다른 workflow가 `main`에 먼저 커밋을 push해서 마지막 `git push`가 reject된 상황으로 보입니다.

### 수정/생성한 파일
- `.github/workflows/enrich-openalex-metadata.yml`: checkout에 `fetch-depth: 0`을 추가하고, enrichment commit 후 `git pull --rebase origin main`을 수행한 뒤 push하도록 변경했습니다.
- `AGENT_LOG.md`: 실패 원인 분석과 workflow 수정 내용을 기록했습니다.

### 구현한 기능
- enrichment workflow가 오래 실행되는 동안 `Update papers` workflow가 `main`을 갱신해도, commit 후 rebase를 시도한 뒤 push합니다.
- full history checkout으로 GitHub Actions 환경에서 rebase가 가능하도록 했습니다.

### 설계 결정
- enrichment는 data file을 변경하는 장시간 작업이라 scheduled update workflow와 충돌할 수 있습니다. 완전한 잠금보다 rebase 후 push가 사용자 수동 실행 흐름에 더 간단하다고 판단했습니다.
- Node 24 opt-in은 이미 적용되어 있으므로 Node warning은 기능 실패로 취급하지 않습니다.

### 남은 작업
- 만약 rebase conflict가 계속 발생하면, update workflow와 enrichment workflow에 동일 concurrency group을 추가해 data-writing workflow를 직렬화하는 방식으로 더 강하게 막을 수 있습니다.

### 주의사항
- OpenAI API는 사용하지 않았습니다.
- 출판사 웹사이트 크롤링, PDF 저장, raw abstract 표시는 수행하지 않았습니다.

## 2026-06-17 00:30
### 변경 요약
- 사용자가 요청한 OpenAlex/Crossref 출처 집합 분석을 전체 collected candidates 3,075건 대상으로 수행했습니다.
- curated `data/papers.json` 1,357건과 hidden/archive `data/archive_papers.json` 1,718건을 합쳐 분석했습니다.
- 논문 단위는 DOI 우선, DOI가 없으면 normalized title 기준으로 분류했고, 게재지 단위는 normalized venue name 기준으로 분류했습니다.

### 수정/생성한 파일
- `reports/source_overlap_analysis.md`: 분석 방법, record-level/unique-paper/venue-level 집계, 주요 venue 표를 담은 요약 보고서입니다.
- `reports/source_overlap_analysis.xlsx`: Summary, All 3075 Records, Unique Papers, Venues, Title Matches 시트를 포함한 Excel 통합 보고서입니다.
- `reports/source_overlap_records_all_3075.csv`: 3,075개 후보 레코드 전체의 출처 분류 CSV입니다.
- `reports/source_overlap_unique_papers.csv`: DOI/title key 기준 unique paper 출처 분류 CSV입니다.
- `reports/source_overlap_venues.csv`: 게재지별 OpenAlex-only/Crossref-only/both 분류 CSV입니다.
- `reports/source_overlap_title_matches.csv`: normalized title 기준으로 양쪽 출처가 모두 관측된 제목 목록 CSV입니다.
- `AGENT_LOG.md`: 이번 분석 작업과 결과 파일을 기록했습니다.

### 구현한 기능
- 전체 후보 3,075건에 대해 `OpenAlex only`, `Crossref only`, `both_openalex_crossref` 집합을 계산했습니다.
- 논문 레코드, unique paper key, venue 세 수준으로 결과를 분리했습니다.
- Excel에서 바로 열 수 있도록 UTF-8 BOM CSV와 `.xlsx` 보고서를 생성했습니다.

### 설계 결정
- 분석 대상은 사이트 하단 ops note의 `3,075 collected candidates`와 일치하도록 curated + archive 전체로 잡았습니다.
- 같은 논문 판단은 기존 파이프라인 정책과 맞춰 DOI를 우선했고, DOI가 없을 때만 normalized title을 사용했습니다.
- Semantic Scholar는 보강 API이므로 이번 OpenAlex/Crossref 집합 비교의 primary source에는 포함하지 않았습니다.

### 남은 작업
- 사용자가 원하면 이 분석을 재실행 가능한 `scripts/analyze_source_overlap.py`로 정식 스크립트화할 수 있습니다.
- venue 이름의 대소문자/HTML entity 차이(`Additive manufacturing` vs `Additive Manufacturing`, `Materials &amp; Design` 등)를 더 강하게 정규화하면 venue-level 결과가 더 깔끔해질 수 있습니다.

### 주의사항
- OpenAI API는 사용하지 않았습니다.
- 출판사 웹사이트 크롤링, PDF 저장, raw abstract 표시는 수행하지 않았습니다.

## 2026-06-17 00:00
### 변경 요약
- 헤더 제작자 credit 문구를 `Curated by`에서 `Developed by`로 변경했습니다.
- 사이트가 단순 큐레이션 목록이 아니라 자동화/웹 구현 프로젝트라는 성격을 더 잘 드러내도록 표현을 조정했습니다.

### 수정/생성한 파일
- `index.html`: `Curated by Gyuwon Lee...` 문구를 `Developed by Gyuwon Lee...`로 변경했습니다.
- `AGENT_LOG.md`: 이번 문구 변경과 의도를 기록했습니다.

### 구현한 기능
- 헤더의 제작자 표기가 개발자/구현자 중심 표현으로 표시됩니다.

### 설계 결정
- 과거 작업 로그의 `Curated by` 기록은 당시 이력으로 유지하고, 현재 사이트에 표시되는 문구만 변경했습니다.

### 남은 작업
- GitHub Pages 반영 후 모바일/데스크톱 헤더에서 줄바꿈이 자연스러운지 확인합니다.

### 주의사항
- OpenAI API는 사용하지 않았습니다.

## 2026-06-16 11:45
### 변경 요약
- 사용자의 의도에 맞춰 `OpenAI summary refresh` workflow의 `dry_run` 기본값을 `false`로 변경했습니다.
- 이제 사용자가 버튼을 눌러 실행하면 기본적으로 OpenAI Q5 요약 결과가 `data/papers.json`에 저장되고 사이트에 반영됩니다.

### 수정/생성한 파일
- `.github/workflows/refresh-openai-summaries.yml`: `dry_run` 기본값을 `false`로 바꾸고 선택지 순서도 `false`, `true`로 정리했습니다.
- `README.md`: 기본 실행은 저장/반영이며, 테스트만 원할 때 `dry_run=true`로 바꾸라고 설명을 갱신했습니다.
- `PROJECT_STATUS.md`: 현재 운영 정책에 `dry_run=false` 기본값을 기록했습니다.
- `AGENT_LOG.md`: 이번 변경의 이유와 주의사항을 기록했습니다.

### 구현한 기능
- `OpenAI summary refresh` 수동 실행 시 기본값 기준으로 실제 요약 반영이 일어납니다.
- 비용 확인 안전장치인 `confirm_openai_cost=true` 요구는 그대로 유지됩니다.

### 설계 결정
- 사용자의 목적이 metadata summary 논문을 실제 OpenAI Q5 요약으로 바꾸는 것이므로 `dry_run=false`가 더 적합하다고 판단했습니다.
- 실수 비용 방지는 `confirm_openai_cost=false` 기본값으로 담당하게 했습니다.

### 남은 작업
- GitHub Actions 화면에서 `OpenAI summary refresh` 실행 시 `dry_run` 기본값이 `false`로 보이는지 확인합니다.

### 주의사항
- `confirm_openai_cost=true`를 선택하지 않으면 OpenAI API는 호출되지 않습니다.
- OpenAI API는 이번 변경 중 호출하지 않았습니다.

## 2026-06-16 11:32
### 변경 요약
- OpenAI 요약 workflow를 `Update papers`처럼 더 명확한 별도 운영 단위로 분리했습니다.
- Actions에 표시되는 이름을 `OpenAI summary refresh`로 바꾸고, OpenAI 요약 전용 상태 파일을 추가했습니다.

### 수정/생성한 파일
- `.github/workflows/refresh-openai-summaries.yml`: workflow 표시 이름을 `OpenAI summary refresh`로 변경하고, 시작/종료 시 전용 status 파일을 기록/커밋하도록 step을 추가했습니다.
- `scripts/write_openai_summary_status.py`: OpenAI 요약 workflow 상태를 `OPENAI_SUMMARY_STATUS.md`와 `data/openai_summary_status.json`에 쓰는 스크립트를 추가했습니다.
- `OPENAI_SUMMARY_STATUS.md`: OpenAI 요약 workflow의 공개 상태 확인 파일을 추가했습니다.
- `data/openai_summary_status.json`: 사이트/자동화에서 읽을 수 있는 OpenAI 요약 workflow 상태 JSON을 추가했습니다.
- `README.md`: 사용자가 Actions에서 선택할 workflow 이름을 `OpenAI summary refresh`로 정리했습니다.
- `ARCHITECTURE.md`: OpenAI 요약 workflow와 상태 파일이 논문 업데이트 workflow와 분리되어 있음을 문서화했습니다.
- `PROJECT_STATUS.md`: 현재 OpenAI 요약 운영 상태와 별도 status 파일 정책을 기록했습니다.
- `AGENT_LOG.md`: 이번 분리 작업을 기록했습니다.

### 구현한 기능
- `Update papers`는 논문 수집 상태를 `UPDATE_STATUS.md`/`data/update_status.json`에 기록합니다.
- `OpenAI summary refresh`는 OpenAI 요약 상태를 `OPENAI_SUMMARY_STATUS.md`/`data/openai_summary_status.json`에 기록합니다.
- OpenAI 요약 workflow가 시작되면 `in_progress` 상태를 먼저 커밋하고, 종료 시 성공/실패/스킵 결과를 다시 커밋합니다.

### 설계 결정
- 비용이 발생하는 OpenAI 요약 작업과 무료/정기 논문 수집 작업은 상태 파일까지 분리하는 편이 운영상 더 안전하다고 판단했습니다.
- OpenAI 요약 workflow는 계속 수동 전용이며, `confirm_openai_cost=true`가 없으면 실행을 차단합니다.
- 초기 status 파일은 `not_run_yet` 상태로 추가했습니다. 실제 workflow가 한 번 실행되면 자동으로 최신 run 정보로 갱신됩니다.

### 남은 작업
- GitHub Actions에서 `OpenAI summary refresh`가 별도 항목으로 보이는지 확인합니다.
- 필요하면 사이트 footer나 개발자 영역에 `OPENAI_SUMMARY_STATUS.md` 링크를 추가할 수 있습니다.

### 주의사항
- OpenAI API는 이번 변경 중 호출하지 않았습니다.
- secret/token 값은 문서와 로그에 기록하지 않았습니다.

## 2026-06-16 11:20
### 변경 요약
- OpenAI 요약도 논문 업데이트처럼 사용자가 GitHub Actions에서 직접 수동 실행할 수 있도록 workflow 사용성을 개선했습니다.
- 기존에는 `OPENAI_REFRESH_ENABLED=true` repository variable을 별도로 열어야 했지만, 이제 `Run workflow` 화면에서 `confirm_openai_cost=true`를 선택하면 실행됩니다.
- 기본 `dry_run` 값을 `true`로 바꿔 실수로 비용이 발생하는 위험을 줄였습니다.

### 수정/생성한 파일
- `.github/workflows/refresh-openai-summaries.yml`: `confirm_openai_cost` 입력을 추가하고, `OPENAI_REFRESH_ENABLED` repository variable gate를 제거했습니다. `dry_run` 기본값을 `true`로 변경하고 커밋 전 `git pull --rebase --autostash origin main`을 추가했습니다.
- `README.md`: 수동 OpenAI 요약 실행 예시에 `confirm_openai_cost=true`를 추가하고 dry-run/실행 방법을 설명했습니다.
- `ARCHITECTURE.md`: OpenAI 요약 workflow의 입력값과 비용 확인 정책을 최신화했습니다.
- `PROJECT_STATUS.md`: 현재 OpenAI 요약 운영 방식이 수동 workflow + `confirm_openai_cost=true` 기준임을 기록했습니다.
- `AGENT_LOG.md`: 이번 변경의 이유와 주의사항을 기록했습니다.

### 구현한 기능
- 사용자는 GitHub Actions의 `Refresh OpenAI summaries`에서 `Run workflow`를 누르고 입력값을 선택해 OpenAI 요약을 직접 실행할 수 있습니다.
- `confirm_openai_cost=false`이면 workflow가 즉시 중단되어 OpenAI API가 호출되지 않습니다.
- `OPENAI_API_KEY`가 repository secret에 없으면 workflow가 즉시 중단됩니다.

### 설계 결정
- 비용이 발생하는 작업이므로 완전 자동 또는 정기 실행은 계속 금지했습니다.
- 숨겨진 repository variable 대신 workflow 입력값으로 명시적 비용 확인을 받는 방식이 사용자가 직접 운영하기 쉽다고 판단했습니다.
- 기본값은 `dry_run=true`로 두어 사용자가 먼저 작은 batch 테스트를 할 수 있게 했습니다.

### 남은 작업
- GitHub Actions 화면에서 `Refresh OpenAI summaries`를 `max_summaries=5`, `refresh_mode=metadata`, `dry_run=true`, `confirm_openai_cost=true`로 테스트하면 입력 흐름을 안전하게 확인할 수 있습니다.
- 실제 반영 시에는 `dry_run=false`로 바꾸고 batch 크기를 비용에 맞춰 조정합니다.

### 주의사항
- OpenAI API key, secret, token은 문서와 로그에 기록하지 않습니다.
- 정기 `Update papers` workflow는 여전히 OpenAI API를 호출하지 않습니다.

## 2026-06-16 11:06
### 변경 요약
- 사용자가 `Run workflow`를 눌렀고 GitHub Actions run #17은 실제로 `in_progress` 상태였지만, 사이트 UI가 여전히 이전 상태를 보여주는 원인을 확인했습니다.
- 원인은 `data/update_status.json`의 시작 상태 커밋은 GitHub raw/main에는 즉시 반영되지만, GitHub Pages 배포본에는 workflow가 끝나기 전까지 반영되지 않는 구조였습니다.
- 사이트가 update status만큼은 GitHub raw URL을 먼저 읽고, 실패하면 기존 Pages 경로로 fallback하도록 수정했습니다.

### 수정/생성한 파일
- `assets/app.js`: `UPDATE_STATUS_URLS`와 `loadUpdateStatus()`를 추가해 raw GitHub의 `data/update_status.json`을 우선 로드하도록 변경했습니다.
- `index.html`: GitHub Pages 캐시 무효화를 위해 `assets/app.js` query version을 갱신했습니다.
- `AGENT_LOG.md`: 이번 원인 조사와 수정 내용을 기록했습니다.

### 구현한 기능
- workflow가 시작 직후 `data/update_status.json`을 커밋하면, 사이트가 Pages 배포 완료를 기다리지 않고 raw GitHub 상태 파일을 통해 `updating now` 상태를 더 빨리 표시할 수 있습니다.
- raw GitHub 요청이 실패하면 기존 `data/update_status.json` Pages 경로를 fallback으로 사용합니다.

### 설계 결정
- 논문 본문 데이터(`papers.json`)는 계속 GitHub Pages 배포본을 사용하고, 빠른 상태 확인이 필요한 `update_status.json`만 raw GitHub를 우선 사용합니다.
- token이나 secret을 클라이언트에 노출하지 않습니다. public repository의 public raw JSON만 읽습니다.
- OpenAI API는 사용하지 않았습니다.

### 남은 작업
- 이번 run #17 또는 다음 수동/정기 run에서 사이트 상단의 `Now / Updated` 패널이 `updating now`를 빠르게 표시하는지 확인합니다.

### 주의사항
- raw GitHub도 CDN/cache 영향을 받을 수 있지만, Pages 배포 완료를 기다리는 것보다는 상태 반영이 빠릅니다.
- GitHub Actions run 자체가 생성되지 않는 경우에는 여전히 `run not seen yet` 표시가 필요합니다.

## 2026-06-16 10:45
### 변경 요약
- GitHub Actions scheduled trigger가 10:17 KST 슬롯에서 새 run을 생성하지 않은 상황을 줄이기 위해 논문 업데이트 주기를 12시간에서 6시간으로 조정했습니다.
- 새 기준은 KST `04:17`, `10:17`, `16:17`, `22:17`입니다.

### 수정/생성한 파일
- `.github/workflows/update-papers.yml`: cron을 `17 1,7,13,19 * * *`로 변경하고 status writer에 전달하는 schedule description도 같은 값으로 맞췄습니다.
- `assets/app.js`: `run not seen yet` 감지 기준을 6시간 슬롯으로 변경했습니다.
- `scripts/write_update_status.py`: 기본 schedule 및 KST 표시 문구를 6시간 주기로 갱신했습니다.
- `index.html`: GitHub Pages 캐시 무효화를 위해 `assets/app.js` query version을 갱신했습니다.
- `PROJECT_STATUS.md`: 현재 update schedule 정책을 6시간 주기로 갱신했습니다.
- `ARCHITECTURE.md`: workflow 구조 설명의 schedule 정보를 6시간 주기로 갱신했습니다.
- `AGENT_LOG.md`: 이번 운영 정책 변경을 기록했습니다.

### 구현한 기능
- 정기 논문 업데이트가 하루 2회가 아니라 하루 4회 시도됩니다.
- 사이트의 `Now / Updated` 패널은 6시간 기준 예정 시간이 지났는데 상태 파일이 갱신되지 않으면 `run not seen yet` / `시도 미감지`를 표시합니다.

### 설계 결정
- GitHub Actions schedule은 정확한 실행 보장이 없으므로, 실행 기회를 늘리기 위해 6시간 주기로 조정했습니다.
- KST 10:17 기준은 유지하고, 같은 minute offset에서 6시간 간격으로 확장했습니다.
- `UPDATE_STATUS.md`는 마지막 실제 workflow 실행 기록이므로 수동으로 새 schedule처럼 고치지 않았습니다. 다음 workflow가 시작되면 자동으로 새 cron 정보가 기록됩니다.

### 남은 작업
- 다음 16:17 또는 22:17 KST 슬롯에서 GitHub Actions run이 생성되는지 확인해야 합니다.
- schedule 누락이 반복되면 외부 스케줄러가 `workflow_dispatch`를 호출하는 구조를 검토합니다.

### 주의사항
- OpenAI API는 사용하지 않았습니다.
- 6시간 주기는 API 호출 빈도를 늘리므로 OpenAlex/Crossref rate limit 상황을 계속 관찰해야 합니다.

## 2026-06-16 10:22
### 변경 요약
- 10:17 KST 정기 업데이트 시간이 지났는데 사이트의 `Now / Updated` 패널이 여전히 이전 업데이트 시각만 보여주는 문제를 점검했습니다.
- GitHub Actions 예약 실행은 GitHub 인프라 상황에 따라 지연되거나 드물게 누락될 수 있으므로, workflow가 아예 시작되지 않은 경우도 UI에서 구분할 수 있게 했습니다.
- 기존 `data/update_status.json`에 예전 cron 문자열이 남아 있어도 현재 의도된 10:17/22:17 KST 기준으로 누락 여부를 판단하도록 수정했습니다.

### 수정/생성한 파일
- `assets/app.js`: 예정 시각이 지났지만 상태 파일이 갱신되지 않은 경우 `시도 미감지` / `run not seen yet` 문구를 표시하는 로직을 추가했습니다.
- `index.html`: GitHub Pages 캐시 무효화를 위해 `assets/app.js` query version을 갱신했습니다.
- `PROJECT_STATUS.md`: 업데이트 상태 표시 정책에 scheduled run 미감지 표시 기준을 기록했습니다.
- `AGENT_LOG.md`: 이번 조사와 수정 내용을 기록했습니다.

### 구현한 기능
- `data/update_status.json`의 마지막 `checked_at_utc`가 최신 예정 실행 시각보다 오래된 경우, 사이트 상단 통계의 `Now / Updated` 카드에 예정 실행이 아직 감지되지 않았음을 표시합니다.
- workflow가 실제로 시작되면 기존처럼 `업데이트 중`, 실패/취소 시 `last attempt failed/cancelled` 계열 문구를 표시합니다.

### 설계 결정
- GitHub Actions 예약 실행은 정확한 시각 보장이 없기 때문에, 사이트에서는 성공/실패뿐 아니라 "예정 시각 이후 상태 파일 갱신 없음"이라는 관측 상태를 별도로 보여주도록 했습니다.
- 상태 파일에 이전 schedule 값(`17 */12 * * *`)이 남아 있는 과도기에도 현재 운영 의도인 `17 1,13 * * *` 기준을 적용합니다.
- OpenAI API는 사용하지 않았습니다. 정기 업데이트에서도 계속 비활성화 상태를 유지합니다.

### 남은 작업
- 다음 예정 실행 이후 GitHub Actions 탭과 공개 사이트의 `Now / Updated` 카드가 각각 `업데이트 중`, 성공/실패, 또는 `시도 미감지` 상태를 올바르게 보여주는지 확인해야 합니다.
- 더 정확한 예약 실행 보장이 필요하면 GitHub cron 대신 외부 스케줄러가 `workflow_dispatch`를 호출하는 구조를 검토할 수 있습니다.

### 주의사항
- `시도 미감지`는 논문 수집 코드가 실패했다는 뜻이 아니라, 예정 시각 이후 새 workflow 상태 기록이 아직 저장소에 반영되지 않았다는 뜻입니다.
- GitHub Actions schedule 이벤트는 default branch의 workflow 파일 기준으로 동작하며, GitHub 쪽 부하로 지연되거나 누락될 수 있습니다.

## 2026-06-15 15:05

### 변경 요약
- 사이트가 무거워졌다는 피드백에 따라 2026-06-15 수동 업데이트와 기존 curated 목록을 함께 검수했습니다.
- biomedical/bioprinting/dental/food/electronics/photovoltaics/prosthetics 등 명확히 범위 밖인 논문을 archive로 내리고, 향후 재유입을 줄이도록 검색어와 필터를 조정했습니다.

### 수정/생성한 파일
- `data/papers.json`: 명확히 범위 밖인 논문 85편을 메인 curated 목록에서 제거했습니다.
- `data/archive_papers.json`: 제거한 논문 85편을 `manual_scope_cleanup` archive reason으로 보존했습니다.
- `data/site_meta.json`: curated/archive/raw candidate 수와 cleanup metadata를 갱신했습니다.
- `data/queries.json`: 너무 넓었던 soft robotics 검색어를 제거하고 fin-ray/soft robotic finger 중심의 좁은 검색어로 교체했습니다.
- `scripts/update_papers.py`: title/venue 기반 off-scope application filter를 추가했습니다.
- `AGENT_LOG.md`: 이번 정리 작업과 기준을 기록했습니다.

### 구현한 기능
- `Dispensing Volumetric Additive Manufacturing`와 `Versatile 3D-printed fin-ray effect soft robotic fingers`는 유지했습니다.
- 의료/치과/바이오프린팅/식품/농업/프린티드 전자/광전지 등 트래커 범위 밖 항목은 메인 표시 목록에서 내려갔습니다.
- 제거된 논문은 삭제하지 않고 archive에 보존해 필요하면 복구할 수 있습니다.

### 설계 결정
- 완전 삭제가 아니라 archive 이동을 선택했습니다. 큐레이션 기준이 바뀌면 되돌릴 수 있어야 하기 때문입니다.
- off-scope 필터는 abstract가 아니라 title/venue 중심으로 적용했습니다. 핵심 VAM/4D 논문이 초록에서 biomedical application을 언급했다는 이유만으로 빠지는 일을 줄이기 위해서입니다.
- soft robotics 검색은 broad gripper 전체가 아니라 fin-ray/3D-printed soft robotic finger 중심으로 좁혔습니다.

### 남은 작업
- 배포 후 사이트 속도와 검색 결과가 나아졌는지 확인합니다.
- 애매한 40여 편은 필요 시 추가 수동 검수합니다.

### 주의사항
- 이 정리 작업은 OpenAI API를 호출하지 않았습니다.
- PDF나 raw abstract는 저장하지 않았습니다.

## 2026-06-15 14:36

### 변경 요약
- 사용자의 요청에 따라 OpenAI 없이 수동 논문 업데이트를 실행했습니다.
- 전체 업데이트는 오래 걸려 타임아웃 후 백그라운드 완료되었지만 데이터 변경이 없었고, 이후 신규 volumetric/soft robotics 검색어만 좁혀 다시 실행해 데이터를 갱신했습니다.

### 수정/생성한 파일
- `data/papers.json`: curated 논문 수가 812편에서 958편으로 증가했습니다.
- `data/archive_papers.json`: archive 논문 수가 1688편에서 1696편으로 증가했습니다.
- `data/site_meta.json`: 마지막 수동 수집 시각, raw candidate 수, curated/archive 수, 추가 논문 수를 갱신했습니다.
- `AGENT_LOG.md`: 이번 수동 업데이트 실행과 검증 결과를 기록했습니다.

### 구현한 기능
- `Dispensing Volumetric Additive Manufacturing`이 메인 논문 목록에 추가되었습니다.
- `Versatile 3D-printed fin-ray effect soft robotic fingers: lightweight optimization and performance analysis`가 메인 논문 목록에 추가되었습니다.
- 두 논문 모두 OpenAI 없이 metadata/fallback summary 상태로 저장되었습니다.

### 설계 결정
- GitHub CLI가 설치되어 있지 않아 GitHub Actions workflow_dispatch 대신 로컬에서 동일한 OpenAI 비활성 설정으로 업데이트를 실행했습니다.
- `UPDATE_STATUS.md`는 GitHub Actions 실행 상태 파일이므로 로컬 수동 업데이트로 임의 갱신하지 않았습니다.

### 남은 작업
- 배포 후 사이트에서 두 논문이 검색되는지 확인합니다.
- 이번 좁힌 수동 실행으로 volumetric AM/soft robotics 주변 논문도 다수 들어왔으므로, 필요하면 추후 검색어 또는 relevance 필터를 더 조정합니다.

### 주의사항
- 이 수동 업데이트는 OpenAI API를 호출하지 않았습니다.
- 검증 결과 저장 데이터에 `_abstract` 필드가 없고, `raw_abstract_displayed=false`, `pdf_stored=false`가 유지됩니다.

## 2026-06-15 00:20

### 변경 요약
- `Dispensing Volumetric Additive Manufacturing`와 `Versatile 3D-printed fin-ray effect soft robotic fingers` 계열 논문이 다음 자동 수집에서 잡히도록 검색어와 규칙 기반 필터를 보강했습니다.

### 수정/생성한 파일
- `data/queries.json`: volumetric AM/photopolymerization/computed axial lithography/tomographic printing 계열 검색어와 3D printed soft robotic finger/fin-ray/soft gripper 계열 검색어를 추가했습니다.
- `scripts/update_papers.py`: `_is_plausible()` topic terms에 volumetric AM, computed axial lithography, tomographic printing, photopolymerization, soft robotics, fin-ray, soft gripper 계열 신호를 추가했습니다.
- `scripts/summarize.py`: 신규 계열 논문에 `Volumetric AM`, `Soft robotics` 태그가 붙을 수 있도록 태그 맵과 카테고리 alias를 보강했습니다.
- `AGENT_LOG.md`: 이번 검색/필터 보강 작업을 기록했습니다.

### 구현한 기능
- Crossref에서 잡히던 두 논문이 검색어와 plausibility 필터를 통과할 수 있게 되었습니다.
- 두 논문 계열이 들어왔을 때 기존의 MMAM/Material distribution 같은 부정확한 단일 태그에만 의존하지 않고 더 명확한 태그를 받을 수 있습니다.

### 설계 결정
- DOI를 seed로 고정하는 대신 검색어와 규칙을 보강했습니다. 같은 계열의 후속 논문까지 자동으로 잡기 위해서입니다.
- OpenAI 요약은 실행하지 않고, 다음 정기 수집 시 metadata/fallback summary로 들어오도록 유지했습니다.

### 남은 작업
- 다음 scheduled run 이후 두 논문이 `data/papers.json`에 들어왔는지 확인합니다.
- 필요하면 DOI를 `data/seed_dois.json`에 추가해 대표 논문으로 고정 추적할 수 있습니다.

### 주의사항
- 이 수정은 OpenAI API를 호출하지 않습니다.
- 논문 수집 스크립트도 실행하지 않았습니다.

## 2026-06-15 00:00

### 변경 요약
- 사용자의 운영 의도에 맞춰 논문 자동 업데이트 주기를 6시간마다에서 12시간마다로 변경했습니다.
- 상태 파일과 문서의 스케줄 설명도 12시간 주기 기준으로 정리했습니다.
- 원격에 먼저 들어온 2026-06-14 UI/status 변경은 보존하고 그 위에 스케줄 변경을 rebase했습니다.

### 수정/생성한 파일
- `.github/workflows/update-papers.yml`: cron을 `17 */6 * * *`에서 `17 */12 * * *`로 변경하고 상태 파일에 전달하는 cron 설명도 갱신했습니다.
- `scripts/write_update_status.py`: 기본 cron 설명을 12시간 기준으로 바꾸고, 현재 cron의 KST 예상 실행 시각을 출력하는 helper를 추가했습니다.
- `UPDATE_STATUS.md`: 현재 스케줄 설명을 `09:17`, `21:17` KST 기준으로 수정했습니다.
- `data/update_status.json`: 최신 workflow run 상태는 유지하고 schedule 값만 `17 */12 * * *`로 갱신했습니다.
- `README.md`: 자동 업데이트 주기를 12시간 기준으로 수정하고, OpenAI key는 정기 업데이트가 아니라 수동 refresh에서만 사용한다는 설명으로 정정했습니다.
- `ARCHITECTURE.md`: workflow 구조 설명을 12시간 주기 기준으로 수정했습니다.
- `PROJECT_STATUS.md`: 2026-06-15 현재 상태 항목을 추가했습니다.
- `AGENT_LOG.md`: 이번 스케줄 정리 작업을 기록했습니다.

### 구현한 기능
- 정기 논문 수집 workflow가 하루 두 번 실행되도록 예약됩니다.
- 상태 Markdown은 다음 workflow 실행부터 12시간 주기의 KST 예상 시각을 표시합니다.

### 설계 결정
- 17분 실행은 유지했습니다. GitHub Actions 정각 부하를 피하면서도 하루 두 번 주기적으로 돌리는 의도에 맞기 때문입니다.
- OpenAI 자동 미사용 정책은 변경하지 않았습니다.
- `data/update_status.json`의 최신 수집 수치와 run id는 원격 최신 값을 유지했습니다.

### 남은 작업
- 다음 scheduled run 이후 `UPDATE_STATUS.md`가 새 run 정보로 갱신되는지 확인합니다.

### 주의사항
- 이 수정은 OpenAI API를 호출하지 않습니다.
- 논문 수집 스크립트는 실행하지 않았고 스케줄/문서만 정리했습니다.

## 2026-06-14 09:10

### 변경 요약
- 상단 통계 패널에 최근 7일 동안 새로 추가된 curated 논문 수를 표시하는 카드를 추가했습니다.
- 최신 업데이트 실행에서 추가된 논문 수를 새 카드의 작은 보조 문구로 함께 보여주도록 했습니다.

### 수정/생성한 파일
- `index.html`: `최근 7일 추가` 통계 카드를 `Papers` 카드 바로 다음에 추가하고 CSS/JS cache version을 `20260614-0050`으로 갱신했습니다.
- `assets/app.js`: `first_added` 기준 최근 7일 추가 논문 수 계산과 `papers_added` 기준 최근 실행 추가 수 표시 로직을 추가했습니다.
- `assets/style.css`: 상단 통계 패널을 5칸 레이아웃으로 조정하고, 보조 문구 스타일을 추가했습니다.
- `AGENT_LOG.md`: 이번 주간 추가량 표시 작업 기록을 추가했습니다.

### 구현된 기능
- 마지막 수집 실행일(KST)을 기준으로 그 날짜를 포함한 최근 7일의 `first_added` 논문 수를 계산해 표시합니다.
- 현재 데이터 기준 `최근 7일 추가`는 793편, `최근 실행` 추가 수는 20편으로 계산됩니다.

### 검증
- 실제 `data/papers.json`과 `data/site_meta.json` 기준 최근 7일/최근 실행 추가 수를 PowerShell로 검산했습니다.
- `git diff --check`로 whitespace 문제 없음 확인했습니다.
- `assets/app.js`를 최소 DOM/스토리지 스텁 환경에서 실제 모듈로 import해 문법 및 초기 실행 오류가 없는지 확인했습니다.

### 주의사항
- 이번 변경은 프론트엔드 표시 로직만 수정하며 논문 데이터와 수집 파이프라인은 변경하지 않습니다.
- OpenAI API 호출은 발생하지 않았습니다.

## 2026-06-14 08:55

### 변경 요약
- 사용자가 되돌릴 수 있음을 염두에 두고 필터 바와 주요 게재지 영역의 작은 디자인 개선을 별도 polish layer로 추가했습니다.
- `요약 방식` 문구를 `요약 유형`으로 바꾸고, reset 문구를 `필터 초기화`로 더 구체화했습니다.

### 수정/생성한 파일
- `index.html`: 필터 문구와 CSS/JS cache version을 `20260614-0040`으로 갱신했습니다.
- `assets/app.js`: 한글/영문 UI 문구를 `요약 유형` / `Summary type`, `필터 초기화`로 조정했습니다.
- `assets/style.css`: 파일 하단에 되돌리기 쉬운 `2026-06-14 filter polish` 블록을 추가했습니다.
- `AGENT_LOG.md`: 이번 디자인 실험 기록을 추가했습니다.

### 구현된 기능
- 필터 바의 간격과 입력 요소 톤을 조금 낮춰 검색창 중심의 위계를 강화했습니다.
- 주요 게재지 카드의 높이, padding, 글자 크기를 줄여 논문 목록으로 더 빨리 시선이 내려가도록 했습니다.

### 검증
- `git diff --check`로 whitespace 문제 없음 확인했습니다.
- `assets/app.js`를 최소 DOM/스토리지 스텁 환경에서 실제 모듈로 import해 문법 및 초기 실행 오류가 없는지 확인했습니다.

### 주의사항
- 이번 변경은 UI polish만 포함하며 논문 데이터, 필터 동작, 수집 파이프라인은 변경하지 않습니다.
- OpenAI API 호출은 발생하지 않았습니다.

## 2026-06-14 08:45

### 변경 요약
- `초기화` 버튼을 별도 grid 칸에서 검색 필드의 라벨 오른쪽으로 옮겼습니다.
- 버튼이 입력창처럼 보이지 않도록 박스형 스타일을 제거하고, 작은 텍스트 액션처럼 정리했습니다.

### 수정/생성한 파일
- `index.html`: reset 버튼을 검색 필드 헤더 내부로 이동하고 CSS/JS cache version을 `20260614-0030`으로 갱신했습니다.
- `assets/style.css`: reset 전용 grid 영역과 관련 반응형 규칙을 제거하고 inline action 스타일로 조정했습니다.
- `assets/app.js`: 언어 전환 시 검색 라벨만 바뀌고 reset 버튼은 유지되도록 selector를 분리했습니다.
- `AGENT_LOG.md`: 이번 위치 조정 기록을 추가했습니다.

### 검증
- `assets/app.js`를 최소 DOM/스토리지 스텁 환경에서 실제 모듈로 import해 문법 및 초기 실행 오류가 없는지 확인했습니다.

### 주의사항
- 이번 변경은 reset 위치와 스타일만 조정하며 필터 동작과 논문 데이터는 변경하지 않습니다.
- OpenAI API 호출은 발생하지 않았습니다.

## 2026-06-14 08:35

### 변경 요약
- 검색/필터 바의 새 `요약 방식` 선택창과 `초기화` 버튼 배치가 빽빽해 보이는 문제를 개선했습니다.
- 데스크톱에서는 검색창과 초기화 버튼을 첫 줄에 두고, 세부 필터 6개를 두 번째 줄에 균등 배치하도록 정리했습니다.

### 수정/생성한 파일
- `index.html`: 필터별 class를 추가하고 CSS/JS cache version을 `20260614-0020`으로 갱신했습니다.
- `assets/style.css`: 컨트롤 바를 grid-area 기반 레이아웃으로 재구성하고, 기존 넓은 화면 override와 충돌하던 구형 grid 규칙을 제거했습니다.
- `AGENT_LOG.md`: 이번 디자인 조정 기록을 추가했습니다.

### 구현된 기능
- 검색창이 다시 충분히 넓게 보이고, `초기화` 버튼은 보조 액션으로 오른쪽에 작게 배치됩니다.
- 태블릿에서는 3열, 모바일에서는 1열로 자연스럽게 내려가도록 반응형 배치를 조정했습니다.

### 주의사항
- 이번 변경은 UI 배치/스타일만 수정하며 필터 동작과 논문 데이터는 변경하지 않습니다.
- OpenAI API 호출은 발생하지 않았습니다.

## 2026-06-14 05:40

### 변경 요약
- 검색/필터 영역에 선택 상태를 한 번에 되돌리는 `초기화` 버튼을 추가했습니다.
- 논문 카드의 `AI 요약` / `메타데이터 요약` 배지 기준으로 결과를 거를 수 있는 `요약 방식` 선택창을 추가했습니다.

### 수정/생성한 파일
- `index.html`: 요약 방식 필터와 초기화 버튼을 추가하고 CSS/JS cache version을 갱신했습니다.
- `assets/app.js`: summary provider 필터링, 필터 초기화 로직, 한글/영문 UI 문구를 추가했습니다.
- `assets/style.css`: 새 선택창과 초기화 버튼이 기존 컨트롤 바에 자연스럽게 맞도록 레이아웃과 다크모드 스타일을 조정했습니다.
- `AGENT_LOG.md`: 이번 UI 변경 기록을 추가했습니다.

### 구현된 기능
- `요약 방식`에서 전체, AI 요약, 메타데이터 요약을 선택해 논문 목록을 필터링할 수 있습니다.
- `초기화` 버튼은 검색어, 분야, 태그/서브 토픽, 게재지, 요약 방식, 연도, 정렬, 주요 게재지 quick filter, 사이드바 서브토픽 선택을 기본 상태로 되돌립니다.

### 검증
- `assets/app.js`를 최소 DOM/스토리지 스텁 환경에서 실제 모듈로 import해 문법 및 초기 실행 오류가 없는지 확인했습니다.
- 현재 세션에서는 in-app browser 인스턴스가 제공되지 않아 실제 브라우저 화면 검증은 수행하지 못했습니다.

### 주의사항
- 이번 변경은 프론트엔드 필터 UI만 수정하며 논문 데이터, 수집 파이프라인, OpenAI API 호출 정책은 변경하지 않습니다.
- OpenAI API 호출은 발생하지 않았습니다.

## 2026-06-13 23:11

### 변경 요약
- 긴 저널/게재지 badge가 말줄임 처리로 과도하게 잘리는 문제를 수정했습니다.

### 수정/생성한 파일
- `assets/style.css`: `publication-badge`의 ellipsis/nowrap을 제거하고 긴 저널명이 badge 안에서 자연스럽게 줄바꿈되도록 변경했습니다.
- `index.html`: GitHub Pages cache busting을 위해 CSS/JS query version을 `20260613-0440`으로 갱신했습니다.
- `AGENT_LOG.md`: 저널 badge 줄바꿈 수정 기록을 추가했습니다.

### 구현한 기능
- `Journal of Emerging Technologies With Industri...`처럼 긴 저널명이 임의로 잘리지 않고, badge 안에서 줄바꿈되어 표시됩니다.
- 카드 폭을 넘는 긴 venue label은 단어 단위 또는 필요한 경우 내부 줄바꿈으로 처리됩니다.

### 설계 결정
- 저널 badge의 덜 둥근 형태는 유지하되, 정보 손실을 만드는 말줄임은 제거했습니다.
- 논문 데이터와 요약 생성 로직은 변경하지 않았습니다.

### 남은 작업
- 실제 긴 저널명 카드에서 줄바꿈 높이가 과하지 않은지 화면에서 확인합니다.

### 주의사항
- 이 수정은 OpenAI API를 호출하지 않습니다.
- 자동 논문 수집 파이프라인은 실행하지 않았습니다.

## 2026-06-13 23:03

### 변경 요약
- 논문 카드 상단의 저널/게재지 badge가 긴 이름에서 과하게 둥글고 어색해지는 문제를 수정했습니다.

### 수정/생성한 파일
- `assets/style.css`: `publication-badge`의 radius를 낮추고, 긴 저널명은 카드 폭 안에서 말줄임 처리되도록 조정했습니다. 모바일에서는 badge가 카드 폭을 넘지 않도록 제한했습니다.
- `index.html`: GitHub Pages cache busting을 위해 CSS/JS query version을 `20260613-0430`으로 갱신했습니다.
- `AGENT_LOG.md`: 저널 badge UI 조정 기록을 추가했습니다.

### 구현한 기능
- 긴 저널/학회명이 캡슐 형태로 늘어져 보이지 않고 compact한 라벨처럼 표시됩니다.
- 긴 publication label은 카드 밖으로 밀리지 않고 한 줄 말줄임 처리됩니다.

### 설계 결정
- 전체 badge 디자인은 유지하되 저널 badge만 별도 처리했습니다.
- 논문 제목, 태그, venue board 구조는 변경하지 않았습니다.

### 남은 작업
- 실제 모바일/데스크톱 화면에서 긴 저널명 badge의 가독성을 확인합니다.

### 주의사항
- 이 수정은 OpenAI API를 호출하지 않습니다.
- 논문 데이터나 자동 업데이트 파이프라인은 변경하지 않았습니다.

## 2026-06-13 22:50

### 변경 요약
- 모바일 헤더에서 제목, 제작자 credit, subtitle, 상태 pill이 뭉개지는 문제를 수정했습니다.
- 직전 contour/toolpath 헤더 배경이 산만해 보여 제거하고, 더 차분한 glow/diagonal 배경으로 낮췄습니다.

### 수정/생성한 파일
- `assets/style.css`: 헤더 contour gradient를 제거하고 opacity를 낮췄습니다. 모바일 전용 헤더 typography, creator credit, hero status, 배경 단순화 override를 추가했습니다.
- `index.html`: GitHub Pages cache busting을 위해 CSS/JS query version을 `20260613-0420`으로 갱신했습니다.
- `AGENT_LOG.md`: 모바일 헤더 및 배경 디자인 수정 기록을 추가했습니다.

### 구현한 기능
- 모바일에서 `AI Manufacturing and 3D/4D Printing Research` 제목이 더 넓은 폭에서 자연스럽게 줄바꿈됩니다.
- `Curated by Gyuwon Lee...` credit은 별도 줄의 작은 pill로 안정적으로 표시됩니다.
- 모바일 상태 pill은 여러 줄 허용, 작은 글자, 좁은 폭으로 조정했습니다.
- 모바일 배경은 grid/contour 없이 은은한 glow만 남겨 산만함을 줄였습니다.

### 설계 결정
- 본문 카드와 필터 UI는 건드리지 않고 헤더와 배경만 수정했습니다.
- contour 배경은 사용자 피드백상 별로였으므로 유지하지 않고 단순화했습니다.

### 남은 작업
- 배포 후 모바일에서 헤더가 겹치거나 뭉개지지 않는지 확인합니다.

### 주의사항
- 이 수정은 OpenAI API를 호출하지 않습니다.
- 새 논문 수집도 실행하지 않습니다.

## 2026-06-13 22:41

### 변경 요약
- 헤더 배경에 아주 은은한 toolpath/contour 느낌의 곡선 레이어를 추가했습니다.
- 모바일에서는 배경 장식 opacity를 낮춰 작은 화면에서 산만하지 않게 했습니다.

### 수정/생성한 파일
- `assets/style.css`: `.site-header::before`에 radial/repeating-radial gradient 기반 contour 레이어를 추가하고 모바일 override를 추가했습니다.
- `index.html`: GitHub Pages cache busting을 위해 CSS/JS query version을 `20260613-0410`으로 갱신했습니다.
- `AGENT_LOG.md`: 헤더 배경 contour 개선 기록을 추가했습니다.

### 구현한 기능
- 헤더에만 3D printing/toolpath를 연상시키는 희미한 곡선 레이어가 표시됩니다.
- 본문 논문 카드와 필터 패널 배경은 그대로 유지해 가독성을 보호했습니다.

### 설계 결정
- SVG나 이미지 파일을 추가하지 않고 CSS gradient만 사용했습니다. 정적 사이트 구조를 단순하게 유지하고 되돌리기 쉽게 하기 위해서입니다.
- 모바일에서는 장식 레이어를 단순화하고 opacity를 낮췄습니다.

### 남은 작업
- 배포 후 헤더 배경이 과하지 않고 본문 가독성을 해치지 않는지 확인합니다.

### 주의사항
- 이 수정은 OpenAI API를 호출하지 않습니다.
- 새 논문 수집도 실행하지 않습니다.

## 2026-06-13 22:34

### 변경 요약
- `Curated by Gyuwon Lee`에서 `by`와 `Gyuwon`이 붙어 `byGyuwon`처럼 보이는 문제를 수정했습니다.

### 수정/생성한 파일
- `assets/style.css`: `.creator-name`에 `margin-left: 0.22em`을 추가해 이름 앞 간격을 명시적으로 확보했습니다.
- `index.html`: GitHub Pages cache busting을 위해 CSS/JS query version을 `20260613-0400`으로 갱신했습니다.
- `AGENT_LOG.md`: 제작자 이름 간격 수정 기록을 추가했습니다.

### 구현한 기능
- 제작자 credit에서 `by`와 `Gyuwon Lee`가 시각적으로 분리되어 읽힙니다.

### 설계 결정
- HTML 문구는 유지하고 CSS margin만 추가했습니다. 문구 구조를 바꾸지 않고 시각적 붙음만 해결하기 위해서입니다.

### 남은 작업
- 배포 후 헤더에서 `Curated by Gyuwon Lee`가 자연스럽게 보이는지 확인합니다.

### 주의사항
- 이 수정은 OpenAI API를 호출하지 않습니다.
- 새 논문 수집도 실행하지 않습니다.

## 2026-06-13 22:27

### 변경 요약
- `Gyuwon Lee` 이름 하이라이트가 이름 영역보다 크게 튀어나와 보이는 문제를 줄였습니다.

### 수정/생성한 파일
- `assets/style.css`: `.creator-name` padding, border-radius, gradient 위치를 줄여 글자 하단에만 형광펜이 깔리도록 조정했습니다.
- `index.html`: GitHub Pages cache busting을 위해 CSS/JS query version을 `20260613-0390`으로 갱신했습니다.
- `AGENT_LOG.md`: 이름 highlight 미세 조정 기록을 추가했습니다.

### 구현한 기능
- 형광펜 효과가 이름 바깥으로 과하게 퍼지지 않고 글자 폭에 더 가깝게 표시됩니다.

### 설계 결정
- 강조를 유지하되 배경 면적을 줄이기 위해 padding을 `0 1px 1px`로 줄이고, gradient를 글자 하단 48~88% 범위로 제한했습니다.

### 남은 작업
- 배포 후 헤더에서 이름 highlight가 충분히 자연스러운지 확인합니다.

### 주의사항
- 이 수정은 OpenAI API를 호출하지 않습니다.
- 새 논문 수집도 실행하지 않습니다.

## 2026-06-13 22:20

### 변경 요약
- 사용자의 요청에 따라 `Export filtered results` action bar와 CSV/BibTeX/Markdown export 기능을 제거했습니다.
- `Gyuwon Lee` 이름 하이라이트가 너무 밋밋해 보여 highlight 면적과 대비를 조금 키웠습니다.

### 수정/생성한 파일
- `index.html`: export action bar를 제거하고 CSS/JS cache version을 `20260613-0380`으로 갱신했습니다.
- `assets/app.js`: export 버튼 참조, event listener, CSV/BibTeX/Markdown 생성 및 다운로드 helper를 제거했습니다.
- `assets/style.css`: export action bar 스타일을 제거하고 `.creator-name` highlight 스타일을 더 선명하게 조정했습니다.
- `AGENT_LOG.md`: export 제거와 creator name highlight 강화 내용을 기록했습니다.

### 구현한 기능
- 검색/필터 영역 아래의 export UI가 사라져 화면이 더 단순해졌습니다.
- 제작자 이름은 더 넓고 선명한 pastel green 형광펜 효과로 표시됩니다.

### 설계 결정
- 사용자가 불필요하다고 판단한 export workflow는 제거했습니다.
- 이름 강조는 텍스트 자체를 키우기보다 highlight 배경 면적, 색 농도, 약한 text-shadow만 조절해 과한 장식이 되지 않게 했습니다.

### 남은 작업
- 배포 후 export 영역이 사라지고 이름 강조가 충분히 보이는지 확인합니다.

### 주의사항
- 이 수정은 OpenAI API를 호출하지 않습니다.
- 새 논문 수집도 실행하지 않습니다.

## 2026-06-13 22:12

### 변경 요약
- 헤더 제작자 표기에서 `Gyuwon Lee` 이름 부분만 은은한 형광펜 느낌으로 하이라이트했습니다.

### 수정/생성한 파일
- `index.html`: `Gyuwon Lee` 텍스트를 `.creator-name` span으로 감쌌고 CSS/JS cache version을 `20260613-0370`으로 갱신했습니다.
- `assets/style.css`: `.creator-name` highlight 스타일과 dark mode 색상 보정을 추가했습니다.
- `AGENT_LOG.md`: 제작자 이름 highlight 변경을 기록했습니다.

### 구현한 기능
- 제작자 이름이 과하지 않은 pastel green highlighter 효과로 강조됩니다.

### 설계 결정
- 전체 credit pill이 아니라 이름만 강조했습니다. 헤더가 산만해지지 않도록 highlight opacity를 낮게 유지했습니다.

### 남은 작업
- 배포 후 헤더에서 이름 강조가 과하지 않은지 확인합니다.

### 주의사항
- 이 수정은 OpenAI API를 호출하지 않습니다.
- 새 논문 수집도 실행하지 않습니다.

## 2026-06-13 22:05

### 변경 요약
- 사용자의 요청에 따라 `Shortlist/Star` 기능을 제거했습니다.
- CSV/BibTeX/Markdown export 기능은 유지하고, action bar를 export 전용으로 단순화했습니다.

### 수정/생성한 파일
- `index.html`: shortlist count/hint/toggle을 제거하고 export 안내 문구만 남겼습니다. CSS/JS cache version을 `20260613-0360`으로 갱신했습니다.
- `assets/app.js`: shortlist 상태, localStorage 저장, 카드 별표 버튼, shortlist only 필터, export의 shortlisted 컬럼을 제거했습니다.
- `AGENT_LOG.md`: shortlist 제거 작업을 기록했습니다.

### 구현한 기능
- 검색/필터 아래 action bar는 현재 필터 결과를 CSV, BibTeX, Markdown으로 내보내는 기능만 제공합니다.

### 설계 결정
- 사용자가 필요 없다고 판단한 개인 shortlist workflow는 제거하고, 필터 결과 export는 연구 자료 이동에 유용하므로 유지했습니다.
- 브라우저에 과거 `shortlistedPapers` localStorage 값이 남아 있어도 더 이상 UI나 필터에 사용하지 않습니다.

### 남은 작업
- 배포 후 별표 버튼과 `Shortlist only` 버튼이 사라졌는지 확인합니다.

### 주의사항
- 이 수정은 OpenAI API를 호출하지 않습니다.
- 새 논문 수집도 실행하지 않습니다.

## 2026-06-13 21:58

### 변경 요약
- 논문 후보를 개인적으로 모아둘 수 있는 `Shortlist/Star` 기능을 추가했습니다.
- 현재 필터링된 논문 목록을 CSV, BibTeX, Markdown으로 내보내는 export 기능을 추가했습니다.

### 수정/생성한 파일
- `index.html`: 검색/필터 아래에 research action bar를 추가하고 CSS/JS cache version을 `20260613-0350`으로 갱신했습니다.
- `assets/app.js`: localStorage 기반 shortlist 저장, `Shortlist only` 필터, 카드 별표 버튼, CSV/BibTeX/Markdown export 로직, localStorage 안전 읽기 helper를 추가했습니다.
- `assets/style.css`: research action bar, export 버튼, star 버튼 스타일과 모바일 대응을 추가했습니다.
- `AGENT_LOG.md`: shortlist/export 기능 추가 내용을 기록했습니다.

### 구현한 기능
- 각 논문 카드에서 별표 버튼을 눌러 이 브라우저의 shortlist에 저장할 수 있습니다.
- `Shortlist only` 버튼으로 저장한 논문만 필터링해서 볼 수 있습니다.
- 현재 검색/필터 결과를 CSV, BibTeX, Markdown 파일로 다운로드할 수 있습니다.

### 설계 결정
- shortlist는 서버 없이 브라우저 `localStorage`에만 저장합니다. GitHub Pages 정적 사이트 구조를 유지하고, 사용자별 개인 선택이 저장소 데이터에 섞이지 않게 하기 위해서입니다.
- export는 현재 화면의 필터링 결과 `state.filtered`를 기준으로 동작합니다. 사용자가 보고 있는 논문 묶음을 그대로 발표/문서 작업으로 가져가기 쉽게 하기 위해서입니다.
- API, 논문 데이터, OpenAI 요약 pipeline은 변경하지 않았습니다.

### 남은 작업
- 배포 후 별표 저장, shortlist filter, 세 가지 export 버튼이 정상 동작하는지 브라우저에서 확인합니다.

### 주의사항
- 이 수정은 OpenAI API를 호출하지 않습니다.
- 새 논문 수집도 실행하지 않습니다.

## 2026-06-13 21:43

### 변경 요약
- 사이트 배경에 은은한 technical grid, radial glow, toolpath-like diagonal line 레이어를 추가했습니다.
- 헤더 영역에는 별도의 subtle gradient/glow를 더해 첫 화면 인상을 강화했습니다.

### 수정/생성한 파일
- `assets/style.css`: light/dark theme용 배경 변수와 body/header background layer를 추가했습니다.
- `index.html`: GitHub Pages cache busting을 위해 CSS/JS query version을 `20260613-0330`으로 갱신했습니다.
- `AGENT_LOG.md`: 배경 스타일 실험 내용을 기록했습니다.

### 구현한 기능
- 전체 배경에 아주 약한 격자와 대각선 라인을 표시해 computational design/toolpath 느낌을 줍니다.
- 다크모드에서는 blue/green glow를 조금 더 살리고, 본문 카드와 패널의 가독성은 유지했습니다.

### 설계 결정
- 논문 카드와 컨트롤 패널의 배경은 그대로 유지했습니다. 텍스트 가독성을 해치지 않기 위해 장식은 page background와 header에만 적용했습니다.
- 이미지나 SVG 파일을 추가하지 않고 CSS 레이어만 사용해 GitHub Pages 정적 구조를 단순하게 유지했습니다.

### 남은 작업
- 배포 후 다크/라이트 모드에서 배경이 과하지 않은지 확인합니다.

### 주의사항
- 이 수정은 OpenAI API를 호출하지 않습니다.
- 새 논문 수집도 실행하지 않습니다.

## 2026-06-13 21:36

### 변경 요약
- 헤더 아래의 상단 게재지 quick filter pill 영역을 제거했습니다.
- 아래 `Venues` 보드와 기능이 중복되어 게재지 필터 UI를 한 곳으로 정리했습니다.

### 수정/생성한 파일
- `index.html`: 상단 `.venue-nav` 마크업을 제거하고 CSS/JS cache version을 `20260613-0320`으로 갱신했습니다.
- `assets/app.js`: 상단 venue nav 생성/초기화/동기화 로직을 제거했습니다. 아래 venue board 필터 기능은 유지했습니다.
- `AGENT_LOG.md`: UI 중복 제거 작업을 기록했습니다.

### 구현한 기능
- 헤더는 제목, 제작자, 설명, 상태 요약만 보여주고 게재지 선택은 아래 `Venues` 보드에서만 수행합니다.

### 설계 결정
- `TARGET_VENUES`와 `activeTargetVenue`는 아래 venue board에서 계속 사용하므로 유지했습니다.
- 필터 기능 자체를 제거하지 않고 중복된 상단 진입점만 제거했습니다.

### 남은 작업
- 배포 후 헤더의 게재지 pill 영역이 사라졌는지 확인합니다.

### 주의사항
- 이 수정은 OpenAI API를 호출하지 않습니다.
- 새 논문 수집도 실행하지 않습니다.

## 2026-06-13 21:25

### 변경 요약
- UI 실험 패치를 적용했습니다. 사용자가 되돌릴 수 있도록 프론트엔드 중심 변경으로 한정했습니다.
- 상단 상태 요약, 카드 밀도 토글, 왼쪽 패널 accordion, Q5 요약 카드화, 관련성 설명 강조, hover/버튼 인터랙션을 개선했습니다.

### 수정/생성한 파일
- `index.html`: 상단 `hero-status` 한 줄 상태 요약과 `Compact/Comfort` 밀도 토글 버튼을 추가하고 CSS/JS cache version을 `20260613-0310`으로 갱신했습니다.
- `assets/app.js`: 카드 밀도 preference, sidebar collapse 상태 저장, hero status 렌더링, Q5 takeaway 강조 class, 버튼 위계 class, 한글/영문 버튼 라벨을 추가했습니다.
- `assets/style.css`: accordion sidebar, 더 넓은 논문 카드 grid, Q5 요약의 질문/답변 분리 디자인, relevance note 강조, hover micro-interaction, compact density mode, dark mode 대비 보정을 추가했습니다.
- `AGENT_LOG.md`: 이번 UI 실험 변경 사항을 기록했습니다.

### 구현한 기능
- 왼쪽 분야 패널의 caret 클릭으로 서브토픽을 접고 펼칠 수 있습니다.
- 상단에 `741 curated papers · 86 venues · 2024-2026 · updated ... KST` 형태의 요약 상태가 표시됩니다.
- `Compact/Comfort` 버튼으로 논문 카드 밀도를 전환할 수 있습니다.
- Q5 요약은 질문 라벨과 답변을 분리해 읽기 쉽게 표시하며, 마지막 takeaway는 별도 강조 블록처럼 보이게 했습니다.
- 논문 카드, venue, tag, 버튼 hover에 부드러운 이동/그림자/색상 전환을 추가했습니다.

### 설계 결정
- 데이터, 요약, OpenAI/API workflow는 건드리지 않았습니다. UI 실험이 마음에 들지 않을 경우 이 커밋만 되돌리면 됩니다.
- 카드 grid 최소 폭을 키워 요약 텍스트가 과도하게 좁아지지 않도록 했고, compact mode에서는 기존처럼 촘촘하게 볼 수 있게 했습니다.
- sidebar field 클릭은 기존처럼 필터로 유지하고, caret 클릭만 접기/펼치기로 분리했습니다.

### 남은 작업
- 로컬 브라우저에서 desktop/mobile 화면을 확인하고 필요하면 간격과 대비를 조정합니다.
- 검증 후 커밋/푸시하고 GitHub Pages 반영 여부를 확인합니다.

### 주의사항
- 이 수정은 OpenAI API를 호출하지 않습니다.
- 새 논문 수집도 실행하지 않습니다.

## 2026-06-13 20:55

### 변경 요약
- 사용자가 `Metadata summary` 203편에 대해 OpenAI Q5 요약 실행을 명시적으로 허가했습니다.
- 기존 `non_qa` 모드는 이미 Q5 형식인 fallback summary를 정확히 집지 못하므로, `metadata` refresh mode를 추가했습니다.

### 수정/생성한 파일
- `scripts/refresh_openai_summaries.py`: `REFRESH_MODE=metadata` 또는 `fallback`일 때 `summary_provider=fallback/metadata/metadata-based` 또는 `openai_summary_applied=false`인 논문만 OpenAI 요약 대상으로 선택하도록 추가했습니다.
- `.github/workflows/refresh-openai-summaries.yml`: 수동 workflow의 `refresh_mode` 선택지에 `metadata`를 추가하고 설명을 갱신했습니다.
- `AGENT_LOG.md`: OpenAI 실행 허가 범위와 안전장치 변경 내용을 기록했습니다.

### 구현한 기능
- 203편의 metadata/fallback summary만 대상으로 OpenAI 요약을 실행할 수 있는 수동 모드를 추가했습니다.

### 설계 결정
- `non_qa` 대신 `metadata` 모드를 새로 추가했습니다. 현재 fallback summary 203편은 이미 Q5 형식을 갖고 있지만 영어 요약이 없으므로, 형식 기준보다 provider 기준으로 선택하는 것이 정확합니다.
- 자동 업데이트 workflow는 계속 OpenAI API를 사용하지 않으며, 이번 작업은 별도 수동 refresh workflow에서만 수행합니다.

### 남은 작업
- 변경 사항을 커밋/푸시한 뒤 `Refresh OpenAI summaries` workflow를 `max_summaries=203`, `refresh_mode=metadata`, `dry_run=false`로 한 번만 실행합니다.
- 실행 후 repository variable `OPENAI_REFRESH_ENABLED`를 다시 `false`로 닫고, provider 분포가 `openai=741`, `fallback=0`인지 확인합니다.

### 주의사항
- API key, secret, token은 로그에 기록하지 않았습니다.
- 이번 허가는 현재 metadata summary 203편에 한정됩니다. 이후 새롭게 추가되는 논문은 사용자가 다시 허가하기 전까지 OpenAI 요약을 적용하지 않습니다.

## 2026-06-13 20:46

### 변경 요약
- 사이트 하단 footer에 문의 연락처 `lko9911@snu.ac.kr`을 추가했습니다.
- 언어 토글에 맞춰 연락처 라벨이 `Contact` / `문의`로 바뀌도록 처리했습니다.

### 수정/생성한 파일
- `index.html`: footer 정책 문구 아래에 contact line을 추가하고 CSS/JS cache version을 `20260613-0250`으로 갱신했습니다.
- `assets/app.js`: `contactLabel` UI 텍스트를 한글/영문에 추가하고 언어 전환 시 갱신되도록 연결했습니다.
- `assets/style.css`: footer 연락처 링크 스타일을 추가했습니다.
- `AGENT_LOG.md`: 연락처 추가 작업 기록을 남겼습니다.

### 구현한 기능
- 방문자가 사이트 하단에서 이메일 문의 주소를 확인하고 mailto 링크로 바로 연락할 수 있습니다.

### 설계 결정
- 연락처는 연구/운영 정보에 가까워 메인 헤더보다 footer의 정책/개발자 정보 영역에 배치했습니다.
- 이메일 주소는 공개 연락처로 표시하되, API key나 secret과 무관한 정보만 기록했습니다.

### 남은 작업
- 배포 후 공개 페이지에서 footer contact line이 보이는지 확인합니다.

### 주의사항
- 이 수정은 OpenAI API를 호출하지 않습니다.
- 새 논문 수집도 실행하지 않습니다.

## 2026-06-13 20:37

### 변경 요약
- `Robotic AM`을 별도 서브토픽/대표 태그에서 제거했습니다.
- 로봇 기반 적층제조 관련 표현은 더 넓은 `Robot-based Manufacturing`으로 흡수되도록 정리했습니다.

### 수정/생성한 파일
- `assets/app.js`: 왼쪽 패널의 `로봇틱스(생산제조)` 서브토픽에서 `로봇 AM`을 제거하고, `Robotic AM` 태그 라벨과 자동 감지 추가 로직을 제거했습니다.
- `scripts/summarize.py`: 향후 fallback 요약/태그 생성에서 `Robotic AM`이 새로 생성되지 않도록 TAG_MAP에서 제거했습니다.
- `index.html`: GitHub Pages 캐시 무효화를 위해 CSS/JS query version을 `20260613-0240`으로 갱신했습니다.
- `AGENT_LOG.md`: 이번 분류 정리 내용을 기록했습니다.

### 구현한 기능
- 왼쪽 패널은 `Robotics for Manufacturing` 아래에 `Manufacturing Automation`, `Robot-based Manufacturing`, `Others`만 표시합니다.
- 기존 논문에 `Robotic AM` 태그가 남아 있어도 대표 태그 UI에서는 표시하지 않습니다.

### 설계 결정
- 논문 데이터 원본은 수정하지 않았습니다. 기존 수집/요약 기록을 보존하고, UI 계층에서 중복 분류만 제거하기 위해서입니다.
- `robotic additive manufacturing`, `robotic 3D printing` 같은 표현은 별도 `Robotic AM`이 아니라 `Robot-based Manufacturing`으로 해석합니다.

### 남은 작업
- 배포 후 공개 페이지에서 `Robotic AM` 항목이 사라졌는지 확인합니다.

### 주의사항
- 이 수정은 OpenAI API를 호출하지 않습니다.
- 새 논문 수집도 실행하지 않습니다.

## 2026-06-13 20:29

### 변경 요약
- 왼쪽 분야/서브토픽 패널에서 `Robotics for Manufacturing`이 `Robotic AM`으로, `AI Manufacturing`이 `Machine Learning`으로 잘못 표시되는 라벨 정규화 버그를 수정했습니다.
- 실제 데이터 수집 결과는 유지하고, 표시 계층만 올바르게 보이도록 조정했습니다.

### 수정/생성한 파일
- `assets/app.js`: `displayLabel()`에서 메인 분야와 기존 카테고리 라벨은 태그 canonicalization보다 먼저 처리하도록 수정했습니다.
- `index.html`: GitHub Pages 캐시 무효화를 위해 CSS/JS query version을 `20260613-0230`으로 갱신했습니다.
- `AGENT_LOG.md`: 이번 표시 버그의 원인과 수정 내용을 기록했습니다.

### 구현한 기능
- 메인 분야명이 서브토픽 태그로 둔갑하지 않도록 표시 우선순위를 분리했습니다.
- `로봇틱스(생산제조)`는 영어 모드에서 `Robotics for Manufacturing`, `AI 생산제조`는 `AI Manufacturing`으로 안정적으로 표시됩니다.

### 설계 결정
- 논문 데이터 자체를 변형하지 않고 프론트엔드 라벨 표시 함수에서 해결했습니다. 기존 수집/요약/분류 데이터의 provenance를 보존하기 위해서입니다.
- 태그와 분야는 이름이 일부 겹치지만 UI 계층이 다르므로, 분야명은 태그 정규화 로직보다 먼저 번역합니다.

### 남은 작업
- 배포 후 공개 페이지에서 왼쪽 패널이 `Robotics for Manufacturing`, `AI Manufacturing`으로 표시되는지 확인합니다.

### 주의사항
- 이 수정은 OpenAI API를 호출하지 않습니다.
- 새 논문 수집도 실행하지 않으며, 현재 저장된 `data/papers.json`을 그대로 사용합니다.

## 2026-06-13 20:10

### 변경 요약
- `Robotics for Manufacturing` 분야에서 `Process Optimization` 서브토픽이 `Production / Manufacturing`의 `Process Optimization`과 중복되어 제거했습니다.
- 로봇이 생산/제조/조립/가공/용접/프린팅을 수행하는 논문을 분리하기 위해 `Robot-based Manufacturing` 서브토픽을 추가했습니다.
- 로봇 관련 쿼리만 대상으로 metadata update를 실행했습니다.

### 수정/생성한 파일
- `assets/app.js`: `Robotics for Manufacturing` 서브토픽을 `Manufacturing Automation`, `Robot-based Manufacturing`, `Robotic AM`으로 재구성했습니다.
- `assets/app.js`: `Robot-based Manufacturing`의 한글/영문 표시 label과 감지 규칙을 추가했습니다.
- `data/queries.json`: robot-based/robotic manufacturing, robotic fabrication, robot-assisted manufacturing, robotic assembly/machining/welding 계열 검색어를 추가했습니다.
- `scripts/summarize.py`: fallback tag generation에서 `Robot-based Manufacturing`을 인식하도록 태그 맵을 추가했습니다.
- `data/papers.json`, `data/archive_papers.json`, `data/site_meta.json`: OpenAI 없이 로봇 관련 metadata update 결과를 반영했습니다.
- `index.html`: JS/CSS cache-busting version을 갱신했습니다.
- `AGENT_LOG.md`, `PROJECT_STATUS.md`: 이번 구조 변경과 업데이트 결과를 기록했습니다.

### 구현한 기능
- 로봇 분야의 중복 `Process Optimization` 항목을 제거했습니다.
- 새 서브토픽 `Robot-based Manufacturing` / `로봇 기반 생산제조`를 추가했습니다.
- 원격 자동 업데이트 반영 후 최신 데이터 기준으로 로봇 관련 update를 다시 실행했으며, curated papers가 707편에서 741편으로 증가했습니다.
- 근사 검증 기준으로 `Robot-based Manufacturing` 후보 약 63편, `Robotic AM` 후보 약 30편이 분리됩니다.

### 설계 결정
- `Robotic AM`은 로봇 기반 적층제조/3D·4D printing에 더 특화된 항목으로 유지했습니다.
- `Robot-based Manufacturing`은 로봇이 제조, 생산, 제작, 조립, 가공, 용접, 프린팅을 수행하는 broader manufacturing 항목으로 분리했습니다.
- OpenAI는 호출하지 않았고, 새 논문은 fallback metadata summary로 추가했습니다.

### 남은 작업
- 새로 추가된 fallback 논문 중 사용자가 명시적으로 원할 경우에만 별도 OpenAI Q5 refresh를 실행할 수 있습니다.
- 실제 UI에서 `Robot-based Manufacturing` 카운트가 너무 넓거나 좁으면 감지 키워드를 조정할 수 있습니다.

### 주의사항
- API key, token, secret은 기록하지 않았습니다.
- 정기 업데이트의 `ALLOW_OPENAI_IN_UPDATE=false` 정책은 유지됩니다.

## 2026-06-13 13:54

### 변경 요약
- 태그가 한글/영문 모드에서 불안정하게 섞이는 문제를 개선했습니다.
- OpenAI가 생성한 자유 태그와 기존 fallback 태그가 1,000종 이상 섞여 있어, 화면 표시 단계에서 canonical 대표 태그만 통과시키도록 변경했습니다.

### 수정/생성한 파일
- `assets/app.js`: 한글/영문 태그 label을 보강하고, 자주 나오는 한글 자유 태그를 canonical tag로 매핑하는 `explicitCanonicalAlias()`를 추가했습니다.
- `assets/app.js`: `representativeTags()`와 `visibleTags()`에서 알 수 없는 자유 태그는 표시/필터에 노출하지 않도록 제한했습니다.
- `index.html`: JS/CSS cache-busting version을 갱신했습니다.
- `AGENT_LOG.md`: 이번 태그 표시 안정화 작업을 기록했습니다.

### 구현한 기능
- `적층 제조`, `디지털 트윈`, `액정 엘라스토머`, `복합재료`, `지속 가능성`, `금속`, `공정 최적화`, `제조 자동화` 등 자주 등장하는 한글 태그를 영문/한글 canonical label로 변환합니다.
- 영어 모드에서는 대표 태그가 `Additive Manufacturing`, `Digital Twins`, `LCE`, `Composites/Materials`처럼 영문으로 표시됩니다.
- 한글 모드에서는 같은 태그가 `적층 제조`, `디지털 트윈`, `LCE`, `복합재/소재`처럼 표시됩니다.

### 설계 결정
- `data/papers.json`의 원본 자유 태그를 대량 수정하지 않고, 프론트엔드 표시 계층에서 canonical tag만 보여주는 방식을 선택했습니다.
- 알 수 없는 자유 태그는 카드/필터에서 제외해 언어 혼합과 과도한 태그 증가를 막습니다.

### 남은 작업
- 실제 화면에서 추가로 어색한 태그가 보이면 `explicitCanonicalAlias()`에 alias를 더 추가하면 됩니다.

### 주의사항
- OpenAI API는 호출하지 않았습니다.
- 논문 데이터, 요약 내용, relevance score는 수정하지 않았습니다.

## 2026-06-13 13:43

### 변경 요약
- 사용자가 제시한 Nature, Science, Nature Materials, Science Advances 대표 논문들이 왜 사이트에 없거나 archive에 있었는지 조사했습니다.
- OpenAlex와 Crossref에는 대부분 정확한 DOI/메타데이터가 있었으므로 API 부재가 아니라 수집 쿼리와 relevance/archive 정책의 문제로 판단했습니다.
- 대표 논문 DOI를 seed list에 추가하고, seed DOI는 `curation_priority`로 메인 curated 목록에 남도록 파이프라인을 수정했습니다.

### 수정/생성한 파일
- `data/seed_dois.json`: 사용자가 제시한 대표 논문 DOI 14개를 추가했습니다.
- `data/queries.json`: volumetric printing, DLP photopolymer, wavelength-selective resin, thermoplastic crystallinity, keyhole instability, AM metals, two-photon liquid crystal 계열 검색어를 추가했습니다.
- `scripts/update_papers.py`: seed DOI는 일반 broad-query relevance 필터 대신 제목/연도/비논문 여부만 확인하고 `curation_priority=true`로 표시하도록 수정했습니다. priority seed는 최소 curated 점수 기준 이상을 보장합니다.
- `data/papers.json`: 14개 대표 DOI가 모두 curated 목록에 포함되도록 갱신했습니다.
- `data/archive_papers.json`: seed priority로 승격된 항목의 archive 상태를 갱신했습니다.
- `data/site_meta.json`: curated count와 raw/archive count를 갱신했습니다.
- `AGENT_LOG.md`: 이번 원인 조사와 수정 내용을 기록했습니다.

### 구현한 기능
- 사용자가 제시한 14개 DOI가 모두 `data/papers.json`에 포함됩니다.
- 기존에 archive에 있던 `Lithographic crystallinity regulation in additive fabrication of thermoplastics (CRAFT)`는 메인 curated 목록으로 승격되었습니다.
- `curation_priority` seed 논문은 relevance score가 낮게 계산되어도 archive로 숨겨지지 않습니다.

### 설계 결정
- Nature/Science 계열 대표 논문은 broad keyword search 상위 결과에 의존하지 않고 DOI seed로 고정 추적합니다.
- OpenAI는 호출하지 않았습니다. 새로 추가/승격된 항목 중 기존 OpenAI 요약이 없던 논문은 fallback metadata summary 상태로 남깁니다.
- 자동 업데이트도 계속 `ALLOW_OPENAI_IN_UPDATE=false` 정책을 유지합니다.

### 남은 작업
- 사용자가 원할 경우 새로 추가된 fallback summary 논문 10편만 별도 OpenAI Q5 refresh 대상으로 실행할 수 있습니다. 단, 이는 다시 명시 요청이 있을 때만 수행해야 합니다.
- 대표 논문 별 relevance score를 별도 curated weight로 더 세밀하게 조정할 수 있습니다.

### 주의사항
- API key, token, secret은 기록하지 않았습니다.
- seed DOI 추가는 출판사 크롤링이 아니라 OpenAlex/Crossref DOI 메타데이터 조회 기반입니다.

## 2026-06-13 13:30

### 변경 요약
- OpenAI Q5 요약 refresh 이후 모든 논문의 `relevance_score`가 `1/10`으로 표시되는 버그를 확인하고 복구했습니다.
- 원인은 OpenAI refresh가 기존 curated relevance score를 OpenAI 응답값으로 덮어쓴 것이었습니다.

### 수정/생성한 파일
- `data/papers.json`: OpenAI refresh 직전 커밋의 relevance score를 기준으로 539편 전체 점수를 복구했습니다.
- `scripts/refresh_openai_summaries.py`: 향후 OpenAI summary refresh가 `relevance_score`를 덮어쓰지 않도록 `SUMMARY_KEYS`에서 제외했습니다.
- `AGENT_LOG.md`: 이번 버그 원인과 복구 내용을 기록했습니다.

### 구현한 기능
- 점수 분포를 `5점 296편`, `6점 141편`, `7점 76편`, `8점 26편`으로 복구했습니다.
- OpenAI Q5 요약, 영어 요약, `summary_provider=openai`, `openai_summary_applied=true` 상태는 539편 전체에서 유지했습니다.

### 설계 결정
- 관련성 점수는 수집/분류 파이프라인의 curated score를 신뢰하고, OpenAI refresh는 요약/태그/카테고리/관련성 설명만 갱신하도록 제한했습니다.
- 점수는 사이트 필터와 정렬에 직접 영향을 주므로, 요약 모델 응답으로 일괄 덮어쓰지 않는 것이 안전합니다.

### 남은 작업
- 필요하면 `relevance_note_ko`도 curated scoring 기준에 맞춰 더 정량적인 설명으로 다시 생성할 수 있습니다.

### 주의사항
- OpenAI API는 이번 복구 작업에서 호출하지 않았습니다.
- API key, token, secret은 기록하지 않았습니다.

## 2026-06-13 13:26

### 변경 요약
- 사용자가 명시적으로 허용한 이번 1회에 한해 curated 논문 전체 OpenAI Q5 요약 refresh를 실행했습니다.
- 실행 직후 `OPENAI_REFRESH_ENABLED` repository variable을 다시 `false`로 닫아 이후 자동/수동 추가 실행을 차단했습니다.
- GitHub Actions run `27454740969`가 성공 완료되었고, Pages 배포까지 완료되었습니다.

### 수정/생성한 파일
- `data/papers.json`: GitHub Actions가 539편 전체에 OpenAI 기반 한국어/영어 Q5 요약을 반영했습니다.
- `data/site_meta.json`: `summaries_refreshed=539`, `summary_refresh_model=gpt-4o-mini`, `last_run_at_utc=2026-06-13T04:23:40Z`가 기록되었습니다.
- `AGENT_LOG.md`: 이번 수동 OpenAI refresh 실행 결과와 안전장치 상태를 기록했습니다.
- `PROJECT_STATUS.md`: 현재 요약 적용 상태를 갱신했습니다.

### 구현한 기능
- `summary_provider=openai`: 539/539편
- `openai_summary_applied=true`: 539/539편
- 한국어 Q5 요약 형식: 539/539편
- 영어 Q5 요약 형식: 539/539편

### 설계 결정
- 사용자가 명시적으로 요청한 이번 작업만 OpenAI API를 사용했습니다.
- 정기 `Update papers` workflow는 여전히 `ALLOW_OPENAI_IN_UPDATE=false`이며 `OPENAI_API_KEY`를 전달하지 않습니다.
- 수동 `Refresh OpenAI summaries` workflow도 `OPENAI_REFRESH_ENABLED=true`와 정확한 확인 문구가 있어야만 실행됩니다. 현재 변수는 다시 `false`입니다.

### 남은 작업
- 다음 신규 논문은 기본적으로 OpenAI 없이 metadata summary로 추가됩니다.
- 신규 논문에도 OpenAI Q5 요약을 적용하려면 사용자가 다시 명시적으로 요청해야 합니다.

### 주의사항
- 이번 refresh는 약 76분 걸렸습니다. 향후 대량 refresh는 100편 단위 batch 방식이 더 안정적일 수 있습니다.
- API key, token, secret은 기록하지 않았습니다.

## 2026-06-13 12:04

### 변경 요약
- 헤더 제작자 크레딧의 영문 이름 표기를 `Kyuwon`에서 `Gyuwon`으로 수정했습니다.
- `Now / Updated`에 표시된 `updated 11:31 KST`의 원인을 확인했습니다.

### 수정/생성한 파일
- `index.html`: 제작자 크레딧 이름을 `Gyuwon Lee`로 수정했습니다.
- `AGENT_LOG.md`: 이전 작업 로그에 남아 있던 이름 표기와 이번 확인 내용을 기록했습니다.

### 구현한 기능
- 사이트 헤더에 올바른 제작자 이름이 표시됩니다.

### 설계 결정
- `11:31 KST`는 `data/site_meta.json`의 `last_run_at_utc=2026-06-13T02:31:38Z`에서 변환된 값으로 확인했습니다.
- GitHub Actions run `27453956710`은 `workflow_dispatch` 이벤트이며 actor는 `lko9911`로 확인했습니다. 따라서 schedule이 아니라 수동 실행된 업데이트입니다.

### 남은 작업
- 필요하면 `Now / Updated` 라벨을 `Current time / Last collection`처럼 더 명확하게 바꿀 수 있습니다.

### 주의사항
- 해당 run은 논문 추가가 0개였지만, 수집 스크립트가 실행되었기 때문에 마지막 수집 시간이 갱신되었습니다.
- API key, token, secret은 기록하지 않았습니다.

## 2026-06-13 12:02

### 변경 요약
- 사이트 제목 옆에 제작자/큐레이터 크레딧을 작게 추가했습니다.
- 요청 문구를 영어로 간단하고 세련되게 표현해 헤더에 배치했습니다.

### 수정/생성한 파일
- `index.html`: H1 내부에 `creator-credit` 문구를 추가하고 CSS/JS cache-busting version을 갱신했습니다.
- `assets/style.css`: 제작자 크레딧 배지 스타일, 다크모드 대비, 모바일 줄바꿈 스타일을 추가했습니다.
- `AGENT_LOG.md`: 이번 헤더 크레딧 추가 작업을 기록했습니다.

### 구현한 기능
- 헤더 제목 옆에 `Curated by Gyuwon Lee, M.S. Student, Prof. Howon Lee Lab, SNU ME · with Codex` 문구가 작게 표시됩니다.
- 모바일에서는 제목 아래로 자연스럽게 내려가도록 구성했습니다.

### 설계 결정
- 연구실/소속/제작 도구를 모두 담되, 사이트의 academic tracker 분위기에 맞게 `Curated by` 표현을 사용했습니다.
- 크레딧은 주 제목보다 약하게 보이도록 작은 pill 형태로 처리했습니다.

### 남은 작업
- 실제 GitHub Pages 배포 후 모바일 화면에서 줄바꿈이 너무 길어 보이면 더 짧은 약칭으로 줄일 수 있습니다.

### 주의사항
- API key, token, secret은 기록하지 않았습니다.
- 이 변경은 UI 표시만 수정하며 논문 데이터와 업데이트 파이프라인에는 영향을 주지 않습니다.

## 2026-06-13 00:20

### 변경 요약
- 상단 통계 문구가 이해하기 어렵다는 피드백을 반영해 더 직관적인 표현으로 바꿨습니다.
- 시간 카드에서 현재 시간과 마지막 수집 시간을 함께 표시하던 방식을 제거하고, 마지막 수집 시간만 표시하도록 단순화했습니다.

### 수정/생성한 파일
- `assets/app.js`: 통계 라벨을 `표시 논문`, `수집 후보`, `마지막 수집`, `숨긴 후보` / `Shown Papers`, `Collected Candidates`, `Last Collection`, `Hidden Candidates`로 변경했습니다.
- `assets/app.js`: `renderUpdatedStat()`가 현재 시간을 섞어 보여주지 않고 마지막 수집 날짜와 KST 시간만 보여주도록 수정했습니다.
- `index.html`: 초기 통계 라벨과 CSS/JS cache-busting version을 업데이트했습니다.
- `AGENT_LOG.md`: 이번 통계 UI 문구 개선 작업을 기록했습니다.

### 구현한 기능
- 414는 기본 화면에 표시되는 curated 논문 수로 이해할 수 있게 했습니다.
- 2084는 자동 수집 후보 전체 수로 이해할 수 있게 했습니다.
- 1670은 낮은 관련성/중복 때문에 숨긴 후보 수로 이해할 수 있게 했습니다.

### 설계 결정
- `Curated`, `Raw`, `Archive` 같은 내부 용어보다 방문자가 이해하기 쉬운 한국어/영어 표현을 우선했습니다.
- 실시간 현재 시각은 사용자가 “수집이 실시간으로 돈다”고 오해할 수 있어 통계 카드에서는 제거했습니다.

### 남은 작업
- 필요하면 통계 아래에 짧은 설명 문장을 추가할 수 있습니다.

### 주의사항
- 이번 변경은 UI 문구와 시간 표시만 수정하며 데이터 분리 구조와 저작권 정책은 변경하지 않았습니다.

## 2026-06-13 00:10

### 변경 요약
- 자동 수집 후보 2084개를 메인 큐레이션 논문과 아카이브 후보로 분리했습니다.
- `data/papers.json`은 기본 사이트에 노출할 curated papers만 담도록 정리했고, 낮은 관련성/제목 중복 후보는 `data/archive_papers.json`으로 이동했습니다.
- 상단 통계를 `큐레이션 논문`, `전체 후보`, `숨김/아카이브`로 바꿔 2084와 실제 표시 논문 수의 의미를 분리했습니다.

### 수정/생성한 파일
- `data/papers.json`: `relevance_score >= 5`와 제목 중복 제거 기준을 통과한 414편만 유지했습니다.
- `data/archive_papers.json`: 낮은 관련성 및 제목 중복 후보 1670개를 보존했습니다.
- `data/site_meta.json`: `curated_count=414`, `raw_candidate_count=2084`, `archived_count=1670`, `hidden_low_relevance_count=1647`, `duplicate_archived_count=23`을 기록했습니다.
- `scripts/update_papers.py`: 이후 자동 수집도 curated/archive를 분리 저장하도록 변경했습니다.
- `.github/workflows/update-papers.yml`: 자동 커밋 대상에 `data/archive_papers.json`을 포함했습니다.
- `.github/workflows/update-papers.yml`: 수집 workflow에 60분 timeout을 추가하고 concurrency group을 `update-papers`로 분리했습니다.
- `.github/workflows/deploy-pages.yml`: Pages 배포 concurrency group을 `deploy-pages`로 분리해 오래 실행되는 수집 workflow가 배포를 막지 않도록 했습니다.
- `data/queries.json`: 너무 넓은 digital twin 검색어를 줄이고 additive manufacturing 맥락이 강한 검색어로 교체했습니다.
- `assets/app.js`: 상단 통계와 결과 문구를 raw/curated/archive 기준으로 표시하도록 수정했습니다.
- `index.html`: 초기 통계 라벨과 CSS/JS cache-busting version을 업데이트했습니다.
- `AGENT_LOG.md`: 이번 큐레이션/아카이브 분리 작업을 기록했습니다.

### 구현한 기능
- 기본 사이트에는 curated papers만 표시됩니다.
- 전체 raw 후보 수와 archive 숨김 수는 `data/site_meta.json` 기반 통계로 확인할 수 있습니다.
- 자동 수집 시 `relevance_score < 5` 항목과 제목 중복 loser는 archive로 이동합니다.
- 같은 제목의 여러 버전이 있을 경우 관련성 점수, repository 여부, venue/DOI 존재 여부, 연도를 기준으로 대표 항목을 고릅니다.

### 설계 결정
- 2084는 논문 수가 아니라 자동 수집 후보 레코드 수로 보고, Awesome-style 사이트의 메인 수는 curated count로 분리했습니다.
- 낮은 관련성 항목을 삭제하지 않고 archive에 보존해 나중에 기준 변경 시 복구할 수 있게 했습니다.
- `digital twin smart manufacturing`처럼 너무 넓은 쿼리는 폭증 원인이므로 제거했습니다.

### 남은 작업
- 새 curated 414편 중 분야와 게재지 분포를 화면에서 검수하면 좋습니다.
- 필요하면 archive 보기 토글을 UI에 추가할 수 있습니다.

### 주의사항
- 이번 변경은 PDF 저장, 출판사 크롤링, raw abstract 표시 정책을 변경하지 않습니다.
- `archive_papers.json`도 공개 정적 데이터이지만 DOI/메타데이터/AI 요약만 포함하며, 원문 초록이나 PDF는 저장하지 않습니다.

## 2026-06-12 23:50

### 변경 요약
- `AI Manufacturing` 사이드바에서 `Manufacturing Automation`이 두 번 표시되던 버그를 수정했습니다.
- 실제로는 `Design Automation` 항목이었지만, canonical topic 판별 순서 때문에 넓은 `automation` 규칙에 먼저 걸려 `Manufacturing Automation`으로 표시되고 있었습니다.

### 수정/생성한 파일
- `assets/app.js`: `canonicalTopicLabel()`에서 `Design automation` 판별을 일반 `Manufacturing automation` 판별보다 먼저 수행하도록 순서를 조정했습니다.
- `index.html`: GitHub Pages 캐시 갱신을 위해 CSS/JS 버전을 업데이트했습니다.
- `AGENT_LOG.md`: 이번 사이드바 중복 라벨 버그 수정 작업을 기록했습니다.

### 구현한 기능
- `AI Manufacturing` 아래의 중복 `Manufacturing Automation` 항목이 사라지고, 마지막 항목은 `Design Automation`으로 표시됩니다.
- 제조 자동화 키워드는 유지하되, `design automation`, `computational design`, `generative design`, `topology optimization`은 설계 자동화로 먼저 정규화됩니다.

### 설계 결정
- `automation`은 너무 넓은 단어라 구체적인 토픽인 `Design Automation`을 먼저 매칭해야 합니다.
- 기존 데이터 구조는 유지하고 프론트엔드 정규화 순서만 수정해 표시 버그를 해결했습니다.

### 남은 작업
- 공개 사이트 반영 후 사이드바에서 `Manufacturing Automation` 중복이 사라졌는지 확인합니다.

### 주의사항
- 이번 변경은 UI 라벨 정규화 로직만 수정하며 논문 데이터, API key, PDF/초록 정책은 변경하지 않았습니다.

## 2026-06-12 23:45

### 변경 요약
- 왼쪽 사이드바 서브토픽 카운트를 분야 내 대표 버킷 방식으로 되돌려, 각 분야의 서브토픽 합계가 분야 총 논문 수와 일치하도록 수정했습니다.
- 새로 추가한 `Self-driving Labs`, `Digital Twins` 계열 검색어로 Crossref 기반 수동 수집을 실행해 논문 데이터를 342편에서 428편으로 늘렸습니다.
- Crossref 결과에 섞인 `Review for`, `Decision letter`, `Author response`, 초청 발표 초록 등 비논문 항목을 제거하고, 향후 수집에서도 제외되도록 필터를 보강했습니다.

### 수정/생성한 파일
- `assets/app.js`: 사이드바 카운트를 포함형 카운트에서 대표 버킷 카운트로 변경하고, 구체적인 서브토픽이 먼저 배정되도록 순서를 조정했습니다.
- `scripts/fetch_crossref.py`: Crossref 검색 기본 정렬을 최신순에서 관련도순으로 변경해 비정상 미래 연도 항목이 상단을 막는 문제를 완화했습니다.
- `scripts/update_papers.py`: `UPDATE_QUERY_FILTER`, `SKIP_OPENALEX`, `SKIP_TARGET_VENUES`, `SEARCH_PER_PAGE`, `TARGET_VENUE_PER_PAGE` 실행 옵션을 추가하고 비논문 항목 필터를 보강했습니다.
- `data/papers.json`: 새 주제 중심 수동 수집 결과를 반영해 총 428편으로 업데이트했습니다.
- `data/site_meta.json`: 이번 수동 수집 결과 `papers_added=86`, `paper_count=428`을 기록했습니다.
- `index.html`: GitHub Pages 캐시 갱신을 위해 CSS/JS 버전을 업데이트했습니다.
- `AGENT_LOG.md`: 이번 카운트 수정 및 수동 수집 작업을 기록했습니다.

### 구현한 기능
- 사이드바에서 각 분야의 서브토픽과 `Others` 합계가 해당 분야 총 논문 수와 같아집니다.
- OpenAlex가 429 rate limit에 걸렸을 때도 `SKIP_OPENALEX=1`로 Crossref 기반 보강 수집을 수행할 수 있습니다.
- `UPDATE_QUERY_FILTER`로 새 토픽 검색어만 골라 빠르게 재수집할 수 있습니다.
- Crossref에서 논문이 아닌 peer-review 부속 항목이 들어오는 문제를 방지합니다.

### 설계 결정
- 서브토픽 카운트는 중복 포함 관계가 아니라 대표 버킷으로 표시해야 사용자가 총합을 이해하기 쉽다고 판단했습니다.
- `Robotic AM`, `Machine Learning`, `FDM`처럼 넓은 토픽은 뒤쪽에 배치하고, `Digital Twins`, `Self-driving Labs`, `Manufacturing Automation`, `DLP`처럼 구체적인 토픽을 먼저 배정합니다.
- Crossref는 `published` 정렬 시 2035/2121 같은 비정상 메타데이터가 상단에 나와, 기본 정렬을 `relevance`로 바꿨습니다.

### 남은 작업
- 새로 추가된 86편은 메타데이터 기반 자동 수집 결과이므로, 사용자가 보는 화면에서 관련성이 낮은 항목이 있는지 한 차례 수동 검수하면 좋습니다.
- OpenAlex rate limit이 풀리면 OpenAlex 기반으로 같은 주제의 누락 논문을 추가 보강할 수 있습니다.

### 주의사항
- 수동 수집은 `OPENAI_API_KEY`를 비운 상태로 실행했으므로 OpenAI 비용은 발생하지 않았습니다.
- 이번 수집도 공식 메타데이터 API만 사용했으며 PDF 저장, 출판사 크롤링, raw abstract 표시 정책은 변경하지 않았습니다.

## 2026-06-12 23:40

### 변경 요약
- 논문 자동 수집 workflow의 cron 실행 시각을 매시 정각에서 매시 17분으로 변경했습니다.
- GitHub Actions scheduled workflow가 정각 부하 시간대에 지연되거나 누락될 가능성을 줄이기 위한 조정입니다.

### 수정/생성한 파일
- `.github/workflows/update-papers.yml`: `cron`을 `0 * * * *`에서 `17 * * * *`로 변경했습니다.
- `AGENT_LOG.md`: 이번 자동 수집 주기 안정화 작업을 기록했습니다.

### 구현한 기능
- 자동 수집은 여전히 1시간마다 실행되지만, 실행 시각만 매시 17분으로 이동했습니다.

### 설계 결정
- 새 토픽을 추가해도 `data/papers.json`은 다음 `Update papers` workflow가 실행되어야 바뀝니다.
- GitHub Actions의 scheduled workflow는 정각에 몰리면 지연 또는 누락될 수 있으므로, 약간 비켜간 분 단위 실행이 더 안정적입니다.

### 남은 작업
- 다음 `Update papers` 실행 후 새 검색어로 실제 논문이 추가되는지 확인해야 합니다.
- 급하게 확인하려면 GitHub Actions의 `Update papers` workflow를 `workflow_dispatch`로 수동 실행하면 됩니다.

### 주의사항
- OpenAlex rate limit은 수동 검증 중 실제로 발생했지만, 현재 논문이 바로 늘지 않은 직접 원인은 새 주제 추가 이후 수집 workflow가 아직 실행되지 않은 점입니다.
- 이번 변경은 workflow 스케줄만 바꾸며 API key, secret, token은 기록하지 않았습니다.

## 2026-06-12 23:35

### 변경 요약
- 헤더 중앙 상단에 표시되던 주요 토픽 칩 목록을 제거했습니다.
- `All`, `Additive Manufacturing`, `Multi-material AM`, `FDM`, `DLP`, `Machine Learning` 등 상단 토픽 필터는 왼쪽 분야/서브토픽 패널과 기능이 중복되어 정리했습니다.

### 수정/생성한 파일
- `index.html`: `.topic-nav` 마크업을 제거하고 CSS/JS cache-busting version을 업데이트했습니다.
- `assets/app.js`: `FEATURED_TOPICS`, `activeTopic`, `buildTopicNav()`, 상단 토픽 필터 조건을 제거했습니다.
- `assets/style.css`: 사용되지 않는 `.topic-nav`, `.topic-pill` 스타일 참조를 제거했습니다.
- `AGENT_LOG.md`: 이번 UI 중복 제거 작업을 기록했습니다.

### 구현한 기능
- 상단 헤더에는 게재지 quick filter만 남고, 토픽 탐색은 왼쪽 패널과 드롭다운 필터로 통일됩니다.
- 언어 전환 시 제거된 토픽 칩을 다시 렌더링하지 않도록 관련 rebuild 호출도 삭제했습니다.

### 설계 결정
- 토픽 필터 기능은 왼쪽 패널에 이미 더 체계적으로 구현되어 있으므로, 중복 UI를 제거해 첫 화면을 덜 복잡하게 만들었습니다.
- 태그/서브토픽 드롭다운은 세부 검색용으로 유지했습니다.

### 남은 작업
- 실제 브라우저에서 헤더 영역이 너무 비어 보이지 않는지 확인하면 좋습니다.

### 주의사항
- 이번 변경은 프론트엔드 UI만 정리하며 논문 데이터, API key, PDF/초록 정책은 변경하지 않았습니다.

## 2026-06-12 23:30

### 변경 요약
- `AI 생산제조` / `AI Manufacturing` 분야에 `Digital Twins` / `디지털 트윈` 서브 토픽을 추가했습니다.
- 디지털 트윈, cyber-physical manufacturing, process twin 계열 표현을 프론트엔드 분류와 자동 수집 파이프라인에서 인식하도록 보강했습니다.

### 수정/생성한 파일
- `assets/app.js`: `AI 생산제조` 서브 토픽에 `Digital Twins`를 추가하고, 한글/영문 라벨, canonical topic, AI 분야 판별, 서브토픽 감지 키워드를 추가했습니다.
- `scripts/summarize.py`: 새 논문 요약/태그 생성에서 `Digital Twins` 태그를 인식하도록 태그 맵과 alias를 추가했습니다.
- `scripts/update_papers.py`: 디지털 트윈 및 cyber-physical 표현이 plausibility 필터를 통과할 수 있도록 키워드를 추가했습니다.
- `data/queries.json`: `digital twin additive manufacturing`, `digital twin 3D printing`, `cyber-physical additive manufacturing` 등 검색어를 추가했습니다.
- `index.html`: GitHub Pages 캐시 갱신을 위해 CSS/JS 버전을 업데이트했습니다.
- `AGENT_LOG.md`: 이번 디지털 트윈 토픽 추가 작업을 기록했습니다.

### 구현한 기능
- 사이드바에서 `Digital Twins`는 `AI Manufacturing` 아래에 표시됩니다.
- `digital twin`, `digital twins`, `virtual twin`, `cyber-physical`, `process twin`, `machine twin` 표현을 같은 토픽으로 정규화합니다.
- 다음 자동 업데이트부터 디지털 트윈 관련 제조/적층제조 논문 수집 가능성이 높아집니다.

### 설계 결정
- 디지털 트윈은 로봇틱스보다 AI 기반 제조 운영, 공정 모니터링, 가상 모델 기반 최적화와 더 가까우므로 `AI Manufacturing` 아래에 배치했습니다.
- 현재 저장된 342편에서는 디지털 트윈 계열 키워드가 0편으로 확인되어 기존 데이터를 억지로 재분류하지 않았습니다.
- Crossref 상위 검색 결과에는 비정상 미래 연도 및 무관 항목이 섞였으므로, 기존 연도/관련성 필터를 유지해 오염을 막습니다.

### 남은 작업
- 다음 자동 수집 후 `Digital Twins` 숫자가 실제로 증가하는지 확인해야 합니다.
- OpenAlex rate limit이 풀린 뒤 `digital twin additive manufacturing` 계열 검색 결과를 추가 검증하면 좋습니다.

### 주의사항
- 이번 변경은 공식 메타데이터 API 기반 검색어와 분류만 조정하며, 출판사 크롤링/PDF 저장/raw abstract 표시 정책은 변경하지 않았습니다.

## 2026-06-12 23:25

### 변경 요약
- `로봇 자율 실험` / `Autonomous Experimentation` 토픽명을 `Self-driving Labs` / `자율 실험실`로 정리했습니다.
- 해당 토픽을 로봇틱스 분야가 아니라 `AI 생산제조` 분야의 서브 토픽으로 이동했습니다.
- self-driving lab, autonomous laboratory, closed-loop experimentation, active learning, Bayesian optimization 계열 논문이 다음 자동 수집에서 걸릴 수 있도록 검색어와 필터를 보강했습니다.

### 수정/생성한 파일
- `assets/app.js`: 사이드바 taxonomy, 한글/영문 라벨, canonical topic alias, AI 분야 판별 조건, 서브토픽 감지 키워드를 수정했습니다.
- `scripts/summarize.py`: 새 논문 요약/태그 생성 시 `Self-driving Labs` 태그를 인식하도록 태그 맵과 alias를 정리했습니다.
- `scripts/update_papers.py`: self-driving lab 계열 논문이 plausibility 필터에서 누락되지 않도록 `materials discovery`, `materials synthesis`, autonomous lab, closed-loop experimentation, active learning, Bayesian optimization 표현을 추가하고, 비정상 미래 연도 메타데이터는 필터에서 제외되도록 보강했습니다.
- `data/queries.json`: self-driving lab/autonomous lab/closed-loop experimentation/materials discovery 관련 검색어를 추가했습니다.
- `index.html`: GitHub Pages 캐시 갱신을 위해 CSS/JS 버전을 업데이트했습니다.
- `AGENT_LOG.md`: 이번 토픽명 정리 및 수집 범위 보강 작업을 기록했습니다.

### 구현한 기능
- 사이드바에서 `Self-driving Labs`는 `AI Manufacturing` 아래에 표시됩니다.
- 기존 `Robotic autonomous experimentation` alias가 남아 있어도 화면에서는 `Self-driving Labs`로 정규화됩니다.
- 다음 자동 업데이트부터 self-driving lab 및 closed-loop experimentation 계열 논문 수집 가능성이 높아집니다.

### 설계 결정
- self-driving lab 문헌은 로봇 팔 자체보다 능동학습, 베이지안 최적화, closed-loop 실험 계획, 자동 재료 탐색에 가까우므로 `Robotics for Manufacturing`이 아니라 `AI Manufacturing` 아래에 배치했습니다.
- 현재 저장된 342편에서는 self-driving lab 계열 키워드가 0편으로 확인되었으므로, 기존 데이터를 억지로 재분류하지 않고 수집 쿼리와 필터를 보강했습니다.
- Crossref/Semantic Scholar 공개 메타데이터 검색에서는 2024년 이후 closed-loop experimentation 및 self-driving lab/materials discovery 계열 결과가 존재함을 확인했지만, Crossref total count와 일부 미래 연도 항목은 검색 품질이 낮아 정밀한 논문 수로 해석하지 않습니다.

### 남은 작업
- 다음 자동 수집 후 `Self-driving Labs` 숫자가 실제로 증가하는지 확인해야 합니다.
- 관련 없는 materials discovery 논문이 많이 들어오면 `_is_plausible()` 필터를 additive manufacturing 또는 manufacturing context 중심으로 다시 조정하세요.

### 주의사항
- 이번 변경도 공식 메타데이터 API 기반 수집 범위만 조정하며, 출판사 크롤링/PDF 저장/raw abstract 표시 정책은 변경하지 않았습니다.

## 2026-06-12 23:20

### 변경 요약
- 왼쪽 사이드바 서브 토픽 카운트가 대표 버킷 하나만 세던 문제를 수정했습니다.
- `Robotics for Manufacturing` 아래에서 모든 로봇 논문이 먼저 매칭되는 `Robotic AM`에만 들어가고, `Manufacturing Automation`과 `Process Optimization`이 0으로 보이던 문제를 해결했습니다.

### 수정/생성한 파일
- `assets/app.js`: `sidebarBucketCounts()`를 한 논문당 하나의 대표 버킷만 세는 방식에서, 해당 논문이 포함하는 모든 서브 토픽을 각각 카운트하는 방식으로 변경했습니다.
- `index.html`: GitHub Pages 캐시 갱신을 위해 CSS/JS 버전을 업데이트했습니다.
- `AGENT_LOG.md`: 이번 사이드바 카운트 수정 작업을 기록했습니다.

### 구현한 기능
- 사이드바 서브 토픽은 이제 상호 배타적인 분류가 아니라 포함 관계로 계산됩니다.
- `Others`는 어떤 서브 토픽에도 걸리지 않는 논문만 세도록 유지했습니다.
- 로컬 데이터 기준으로 로봇틱스 26편 중 `제조 자동화` 후보 5편, `공정 최적화` 후보 5편이 표시될 수 있도록 수정했습니다.

### 설계 결정
- 한 논문은 `Robotic AM`이면서 동시에 `Manufacturing Automation` 또는 `Process Optimization`일 수 있으므로, 서브 토픽 카운트 합계가 메인 분야 총합과 반드시 같을 필요는 없습니다.
- 사용자가 원하는 것은 대표 분류가 아니라 “해당 서브 토픽에 걸리는 논문 수”이므로 포함형 카운트가 더 적절합니다.

### 남은 작업
- 실제 브라우저에서 최신 JS 캐시가 반영된 뒤 로봇틱스 사이드바 숫자를 확인하면 좋습니다.

### 주의사항
- 이번 변경은 UI 카운트 방식만 바꾸며 저장 데이터, API key, PDF/초록 정책은 변경하지 않았습니다.

## 2026-06-12 23:15

### 변경 요약
- 왼쪽 분야 패널에서 `Robotics for Manufacturing` 같은 긴 라벨이 줄바꿈되며 숫자와 붙어 보이는 문제를 개선했습니다.
- 로봇틱스 분야에 `로봇 자율 실험` / `Autonomous Experimentation` 서브 토픽을 추가했습니다.
- `제조 자동화`가 0으로 보이던 원인을 검증하고, 자동화 관련 키워드 감지 범위를 넓혔습니다.

### 수정/생성한 파일
- `assets/style.css`: 왼쪽 패널 폭, 라벨 줄바꿈 방지, 라벨-숫자 간격을 조정했습니다.
- `assets/app.js`: 로봇 자율 실험 토픽과 영문/한글 라벨을 추가하고, 제조 자동화 분류 키워드를 확장했습니다.
- `data/queries.json`: 로봇 AM, 제조 자동화, closed-loop manufacturing, self-driving lab 계열 검색어를 추가했습니다.
- `scripts/summarize.py`: 새로 수집되는 논문 요약/태그 생성에서도 로봇 자율 실험과 제조 자동화 표현을 인식하도록 태그 맵을 보강했습니다.
- `index.html`: GitHub Pages 캐시 갱신을 위해 CSS/JS 버전을 업데이트했습니다.
- `PROJECT_STATUS.md`: 현재 342편 데이터 상태와 로봇틱스/제조 자동화 보강 내용을 최신 상태로 기록했습니다.
- `AGENT_LOG.md`: 이번 UI 및 분류 검증 작업을 기록했습니다.

### 구현한 기능
- 왼쪽 사이드바의 메인 분야 라벨은 한 줄로 표시되고, 숫자 배지는 더 안정적으로 떨어져 보입니다.
- `self-driving lab`, `autonomous experimentation`, `closed-loop experiment`, `robotic experiment` 계열 표현은 `로봇 자율 실험`으로 분류됩니다.
- `automation`, `automated`, `autonomous`, `closed-loop`, `monitoring`, `in-situ` 계열 표현은 `제조 자동화` 후보로 잡히도록 했습니다.
- 이후 자동 수집은 로봇 AM 및 제조 자동화 관련 검색어도 함께 조회합니다.

### 설계 결정
- `로봇 자율 실험`은 현재 수집 데이터에서 엄격한 키워드 기준으로는 0편이지만, 사용자가 원하는 연구 범위에 맞춰 taxonomy에 먼저 포함했습니다.
- `제조 자동화`는 논문 제목/요약/태그에서 쓰이는 표현이 다양하므로 좁은 `automation` 키워드만 쓰지 않고 관련 표현을 함께 감지합니다.
- PDF 저장, publisher crawling, raw abstract 표시 정책은 변경하지 않았습니다.

### 남은 작업
- 다음 자동 수집 후 로봇 자율 실험 관련 논문이 새로 들어오는지 확인하면 좋습니다.
- 수집량이 과도하게 늘어나면 `data/queries.json`의 로봇/자동화 검색어를 더 세분화할 수 있습니다.

### 주의사항
- 현재 데이터 검증 기준으로 로봇 관련 논문은 32편, 자동화 확장 키워드 후보는 8편, 엄격한 로봇 자율 실험 후보는 0편입니다.
- UI 변경은 정적 프론트엔드만 바꾸며 API key, secret, token은 사용하거나 기록하지 않았습니다.

## 2026-06-12 23:08

### 변경 요약
- 3D Printing 왼쪽 패널에서 FDM이 빠져 보이는 문제를 수정했습니다.
- FDM을 `3D 프린팅` 분야의 명시적 서브토픽으로 추가했습니다.
- 사이드바 서브토픽 카운트가 카드 표시용 대표 3개 태그에만 의존하지 않고, 전체 태그/서브토픽 신호를 보도록 수정했습니다.

### 수정/생성한 파일
- `assets/app.js`: `FIELD_SUBTOPICS["3D 프린팅"]`에 `FDM/Material extrusion`을 추가하고, `paperHasRepresentativeTopic()`의 매칭 후보를 확장했습니다.
- `index.html`: JS/CSS cache-busting version을 갱신했습니다.
- `AGENT_LOG.md`: 이번 FDM 사이드바 복구 작업을 기록했습니다.

### 구현한 기능
- 3D Printing 패널 아래에 FDM이 표시됩니다.
- FDM이 FGAM/MMAM 같은 대표 태그에 밀려도 사이드바 카운트에는 반영됩니다.
- 현재 데이터 기준 3D Printing 분야 안에서 FDM 신호가 있는 항목이 정상적으로 잡힙니다.

### 설계 결정
- 카드 배지는 여전히 대표 3개만 보여주되, 사이드바 필터/카운트는 더 넓은 topic signal을 사용하도록 분리했습니다.

### 남은 작업
- 실제 브라우저에서 왼쪽 패널 FDM 표시를 확인하면 좋습니다.

### 주의사항
- 이번 변경은 UI 분류/카운트 로직만 수정하며 raw abstract/PDF 저장 정책에는 영향을 주지 않습니다.

## 2026-06-12 23:01

### 변경 요약
- `Additive manufacturing` 태그 보강 후 왼쪽 `Manufacturing` 분야 카운트가 1로 줄어드는 문제를 수정했습니다.
- 대분야 분류가 태그에 과도하게 끌려가지 않도록 `deriveField()`에서 `paper.tags`를 제외했습니다.
- `additive manufacturing` 단독 표현만으로 3D Printing 분야에 들어가지 않도록 조정했습니다.
- 대표 태그 목록에 `Additive manufacturing`을 추가해 FDM 및 Functionally Graded AM 축과 함께 보이도록 했습니다.
- 깨져 있던 일부 `relevance_note_ko` 문장을 UTF-8 안전 방식으로 전체 재생성했습니다.

### 수정/생성한 파일
- `assets/app.js`: 대분야 분류 로직과 대표 태그 목록을 수정했습니다.
- `data/papers.json`: 342편의 `relevance_note_ko`를 정상 한국어 문장으로 재생성했습니다.
- `index.html`: JS/CSS cache-busting version을 갱신했습니다.
- `AGENT_LOG.md`: 이번 분류 복구 및 태그 노출 보강 작업을 기록했습니다.

### 구현한 기능
- `Manufacturing` 분야가 태그 정규화 때문에 1편으로 줄어드는 문제가 해결됩니다.
- `Additive Manufacturing`, `FDM`, `Functionally Graded AM`이 대표 태그 축에서 함께 보입니다.
- 관련성 설명 문장이 `? ??????`처럼 깨져 보이는 문제를 제거했습니다.

### 설계 결정
- 태그는 필터/카드 표시용으로 유지하고, 대분야 분류는 제목·venue·카테고리 중심으로 계산하도록 분리했습니다.
- `Additive manufacturing`은 너무 넓은 표현이므로 단독으로는 3D Printing으로 강제 분류하지 않습니다.

### 남은 작업
- 실제 브라우저에서 왼쪽 패널 카운트와 대표 태그 버튼 표시를 확인하면 좋습니다.

### 주의사항
- raw abstract/PDF 저장 정책은 변경하지 않았습니다.

## 2026-06-12 22:50

### 변경 요약
- `FDM/Material extrusion` 태그가 UI에서 `FDM`으로 표시되도록 간결화했습니다.
- 상단 대표 태그 목록에 FDM을 추가했습니다.
- `Additive manufacturing` 태그만 있던 논문 중 FDM/material extrusion/filament 신호가 있는 항목에는 `FDM/Material extrusion` 태그를 추가했습니다.

### 수정/생성한 파일
- `assets/app.js`: `FEATURED_TOPICS`에 `FDM/Material extrusion`을 추가하고, 한국어/영어 표시 라벨을 `FDM`으로 정리했습니다.
- `data/papers.json`: FDM 신호가 있는 기존 논문 4편에 FDM 태그를 추가했습니다.
- `scripts/summarize.py`: OpenAI/자동 태그 결과에서 `FDM / Material Extrusion` 표기도 canonical `FDM/Material extrusion`으로 정규화되도록 alias를 추가했습니다.
- `index.html`: JS/CSS cache-busting version을 갱신했습니다.
- `AGENT_LOG.md`: 이번 FDM/FGAM 태그 표시 보강 작업을 기록했습니다.

### 구현한 기능
- 카드와 필터에서 FDM이 짧고 명확한 태그로 보입니다.
- `Functionally Graded AM`은 기존 `FGAM` canonical 태그의 영어 표시로 유지됩니다.
- Additive Manufacturing 계열 중 FDM 신호가 있는 논문은 더 구체적으로 FDM 태그를 함께 가집니다.

### 설계 결정
- 저장값은 기존 canonical `FDM/Material extrusion`을 유지하고, 화면 표시만 `FDM`으로 줄였습니다.
- FGAM은 이미 `Functionally Graded AM`으로 표시되고 있어 저장값은 유지했습니다.

### 남은 작업
- 없음.

### 주의사항
- 이번 변경은 태그 표시/정규화만 수정하며 raw abstract/PDF 저장 정책에는 영향을 주지 않습니다.

## 2026-06-12 22:45

### 변경 요약
- 왼쪽 패널의 분야/서브토픽 표시가 한국어/영어 모드에 맞게 번역되도록 UI 문구를 보강했습니다.
- venue 보드 기준을 기존 2편 이상 개별 표시에서 `Core / 10편 이상 / Others` 구조로 변경했습니다.
- 한국어 모드의 `All venues`, `papers`, `Others` 같은 영어 잔여 UI 문구를 한국어로 정리했습니다.

### 수정/생성한 파일
- `assets/app.js`: venue 표시 기준, 한국어/영어 UI 문구, 10편 이상 venue 라벨을 수정했습니다.
- `index.html`: JS/CSS cache-busting version을 갱신했습니다.
- `AGENT_LOG.md`: 이번 사이드바/venue 표시 기준 변경을 기록했습니다.

### 구현한 기능
- 한국어 모드에서는 `전체 게재지`, `편`, `기타`, `10편 이상`처럼 표시됩니다.
- 영어 모드에서는 `All venues`, `papers`, `Others`, `10+ papers`처럼 표시됩니다.
- venue board는 core venue를 우선 표시하고, non-core venue는 10편 이상인 경우만 개별 표시하며 나머지는 Others로 묶습니다.

### 설계 결정
- Core venue는 기존 `TARGET_VENUES` 목록을 유지했습니다.
- 10편 이상 기준은 `VENUE_MIN_VISIBLE_COUNT = 10` 상수로 분리해 이후 쉽게 조정할 수 있게 했습니다.

### 남은 작업
- 실제 브라우저에서 언어 토글 후 사이드바 라벨과 venue board를 시각 확인하면 좋습니다.

### 주의사항
- 이번 변경은 프론트엔드 표시와 venue grouping 기준만 수정하며 데이터 수집, API key, raw abstract/PDF 정책에는 영향을 주지 않습니다.

## 2026-06-12 22:24

### 변경 요약
- 영어 모드에서 저자 목록이 `외 N명`으로 표시되던 문제를 수정했습니다.
- 영어 모드에서는 4명 이상 저자일 때 `et al.` 표기를 사용하도록 변경했습니다.

### 수정/생성한 파일
- `assets/app.js`: `formatAuthors()`가 현재 언어를 확인해 영어 모드에서는 `et al.`, 한국어 모드에서는 `외 N명`을 표시하도록 수정했습니다.
- `index.html`: JS/CSS cache-busting version을 갱신했습니다.
- `AGENT_LOG.md`: 이번 저자 표기 수정 작업을 기록했습니다.

### 구현한 기능
- 영어 모드 예시: `Rahul Chatterjee, Pinaki Das, Sayan Basak et al.`
- 한국어 모드 예시: `Rahul Chatterjee, Pinaki Das, Sayan Basak 외 5명`

### 설계 결정
- 영어권 학술 목록에서 가장 자연스럽고 compact한 `et al.` 표기를 사용했습니다.
- 데이터 자체는 바꾸지 않고 화면 표시 함수만 수정했습니다.

### 남은 작업
- 없음.

### 주의사항
- 이번 변경은 프론트엔드 표시만 수정하며 데이터 수집, API key, raw abstract/PDF 정책에는 영향을 주지 않습니다.

## 2026-06-12 22:21

### 변경 요약
- 논문 태그를 canonical 영어 태그로 통일하고, 화면 표시만 한국어/영어 모드에 따라 번역되도록 정리했습니다.
- 기존 `적층제조`, `문헌추적`, `메타데이터` 같은 generic 태그와 한글/영문 혼재 태그를 제거했습니다.
- 태그 필터와 카드 배지가 같은 canonical 기준을 쓰도록 프론트엔드 정규화 로직을 보강했습니다.

### 수정/생성한 파일
- `data/papers.json`: 342편 논문의 저장 태그를 canonical 태그 1~3개로 정리하고 관련성 설명의 태그 표기를 갱신했습니다.
- `assets/app.js`: `TAG_LABELS`를 추가해 한국어/영어 표시 라벨을 분리하고, `canonicalTopicLabel()`, `visibleTags()`, 태그 필터 매칭을 정리했습니다.
- `scripts/summarize.py`: 새로 생성되는 태그가 canonical 태그로 저장되도록 `TAG_MAP`, `TAG_ALIASES`, generic tag 제거 로직을 보강했습니다.
- `index.html`: JS/CSS cache-busting version을 갱신했습니다.
- `AGENT_LOG.md`: 이번 태그 정리 작업을 기록했습니다.

### 구현한 기능
- 저장 태그는 `4D printing`, `FGAM`, `LCE`, `Toolpath strategy` 같은 canonical 값만 사용합니다.
- 한국어 모드에서는 `4D 프린팅`, `기능성 구배`, `툴패스 전략`처럼 표시됩니다.
- 영어 모드에서는 `4D Printing`, `Functionally Graded AM`, `Toolpath Strategy`처럼 표시됩니다.
- 태그 필터에서 같은 개념이 한글/영어로 중복 표시되는 문제를 줄였습니다.

### 설계 결정
- 데이터 저장값은 영어 canonical로 통일하고, UI 표시만 번역하는 방식을 선택했습니다. 이후 자동 수집/필터/언어 전환을 안정적으로 유지하기 위해서입니다.
- `문헌추적`, `메타데이터`처럼 논문 주제를 설명하지 않는 태그는 제거했습니다.

### 남은 작업
- 향후 더 세밀한 태그 체계가 필요하면 canonical tag 목록을 별도 JSON 설정으로 분리할 수 있습니다.
- 브라우저에서 태그 필터 드롭다운의 최종 시각 표시를 한 번 더 확인하면 좋습니다.

### 주의사항
- 이번 변경은 태그 정규화와 표시 라벨 정리만 수행하며 raw abstract/PDF 저장 정책에는 영향을 주지 않습니다.

## 2026-06-12 22:09

### 변경 요약
- 영어 모드도 GPT가 작성한 영문 요약을 사용할 수 있도록 OpenAI 요약 파이프라인을 확장했습니다.
- 새 OpenAI 요약 결과에 `ai_summary_ko`와 `ai_summary_en`을 함께 생성하고 저장하도록 변경했습니다.
- 기존 논문 재요약 workflow가 5문항 한글 요약이 이미 있어도 `ai_summary_en`이 비어 있으면 재요약 대상으로 잡도록 조정했습니다.
- 1편 테스트 후 OpenAI가 `Topic`, `Problem` 같은 짧은 dict key를 반환하는 케이스를 확인해 정규화 로직과 프론트엔드 파서를 추가 보강했습니다.

### 수정/생성한 파일
- `scripts/summarize.py`: OpenAI 프롬프트가 한글/영문 5문항 요약을 함께 반환하도록 변경하고, `ai_summary_en` 정규화 로직을 추가했습니다.
- `scripts/update_papers.py`: `data/papers.json` 저장 schema에 `ai_summary_en`을 포함하고, 기존 논문 refresh 시에도 영문 요약을 병합하도록 수정했습니다.
- `scripts/refresh_openai_summaries.py`: 수동 OpenAI 재요약 대상 판단에 `ai_summary_en` 누락 여부를 포함했습니다.
- `assets/app.js`: 영문 요약 줄에서 `Topic`, `Problem` 라벨 뒤 구분자가 없어도 답변만 깨끗하게 추출하도록 파서를 보강했습니다.
- `index.html`: JS/CSS cache-busting version을 갱신했습니다.
- `data/papers.json`: 1편 테스트로 생성된 `ai_summary_en`을 `Topic -` 형식으로 정리하고, dict-like 한글 요약 문자열을 5문항 텍스트로 정규화했습니다.
- `data/site_meta.json`: OpenAI 1편 테스트 workflow 실행 시 갱신된 마지막 실행 시각을 반영했습니다.
- `README.md`: OpenAI 요약이 한글/영문을 함께 생성한다는 점과 schema 예시를 업데이트했습니다.
- `ARCHITECTURE.md`: 데이터 구조, 파이프라인, 저작권 정책 설명을 `ai_summary_ko`/`ai_summary_en` 기준으로 갱신했습니다.
- `PROJECT_STATUS.md`: 현재 상태와 다음 작업에 영문 GPT 요약 저장 지원을 반영했습니다.
- `AGENT_LOG.md`: 이번 영문 GPT 요약 파이프라인 확장 작업을 기록했습니다.

### 구현한 기능
- 새 논문 또는 수동 재요약 논문에 대해 GPT가 `Topic`, `Problem`, `Method`, `Key Result`, `Takeaway` 형식의 한글/영문 요약을 함께 생성합니다.
- 영어 UI는 저장된 `ai_summary_en`이 있으면 이를 우선 표시하고, 없는 경우 기존 메타데이터 기반 fallback을 유지합니다.
- `max_summaries=1`, `refresh_mode=non_qa`, `dry_run=false`로 OpenAI 1편 테스트를 실행했고, 영문 GPT 요약 저장을 확인했습니다.

### 설계 결정
- 한글 요약을 클라이언트에서 번역하지 않고 서버 측 업데이트 파이프라인에서 `ai_summary_en`을 별도 저장하도록 했습니다. 그래야 영어 모드도 초록을 반영한 고품질 요약을 안정적으로 보여줄 수 있습니다.
- 정기 수집 workflow에는 기존처럼 새 논문만 요약하게 두고, 전체 기존 논문 재요약은 수동 workflow로 분리해 OpenAI 비용이 매시간 반복되지 않도록 유지했습니다.

### 남은 작업
- 변경 사항 배포 후 `Refresh OpenAI summaries` workflow를 `max_summaries=1`, `refresh_mode=non_qa`, `dry_run=false`로 실행해 `ai_summary_en` 저장을 1편 테스트합니다.
- 전체 논문에 영문 GPT 요약을 채우려면 같은 workflow를 더 큰 `max_summaries` 값으로 수동 실행해야 합니다.

### 주의사항
- API key, secret, token은 로그나 데이터 파일에 기록하지 않습니다.
- raw abstract는 저장하거나 표시하지 않고, PDF도 다운로드하거나 저장하지 않는 정책을 유지합니다.
- `ai_summary_en` 생성은 OpenAI API 호출이므로 수동 재요약 실행 시 처리 편수만큼 비용이 발생할 수 있습니다.

## 2026-06-12 22:06

### 변경 요약
- 영어 모드에서 5문항 요약의 답변이 한국어로 그대로 표시되던 문제를 개선했습니다.
- 영어 모드에서는 같은 `Topic`, `Problem`, `Method`, `Key Result`, `Takeaway` 틀을 유지하되 영어 문장으로 표시하도록 했습니다.

### 수정/생성한 파일
- `assets/app.js`: 영어 모드용 `englishSummarySections()`를 추가하고, `ai_summary_en`이 있으면 우선 사용하도록 확장했습니다.
- `index.html`: JS/CSS cache-busting version을 갱신했습니다.
- `AGENT_LOG.md`: 이번 영어 요약 표시 보정 작업을 기록했습니다.

### 구현한 기능
- 한국어 모드와 영어 모드 모두 같은 5문항 카드 레이아웃을 사용합니다.
- 영어 모드는 한국어 저장 요약을 그대로 노출하지 않고 영어 표시 요약을 렌더링합니다.

### 설계 결정
- 아직 고품질 `ai_summary_en` 저장 필드는 없으므로, 영어 모드는 메타데이터 기반 안전 요약을 사용합니다.
- 향후 OpenAI batch에서 `ai_summary_en` 필드를 생성하면 프론트엔드는 이를 우선 표시할 수 있게 했습니다.

### 남은 작업
- 완전한 영문 고품질 요약을 원하면 OpenAI 요약 파이프라인에서 `ai_summary_en` 필드를 추가 생성하도록 확장해야 합니다.

### 주의사항
- 이번 변경은 프론트엔드 표시 로직만 수정하며 OpenAI 비용은 발생하지 않습니다.

## 2026-06-12 22:00

### 변경 요약
- 논문 요약 5문항 표준을 `Topic`, `Problem`, `Method`, `Key Result`, `Takeaway` 형식으로 변경했습니다.
- 기존 “내 연구/발표에 왜 필요한가?” 항목을 `Takeaway - 그래서 이 논문의 핵심 메시지는 무엇인가?`로 대체했습니다.
- 이미 저장되어 있던 번호형 요약 2편은 OpenAI를 다시 호출하지 않고 라벨만 새 형식으로 변환했습니다.

### 수정/생성한 파일
- `scripts/summarize.py`: OpenAI 프롬프트, fallback 요약, OpenAI 응답 정규화 라벨을 새 5문항 형식으로 변경했습니다.
- `assets/app.js`: 한글/영문 모드의 카드 질문 라벨을 `Topic`, `Problem`, `Method`, `Key Result`, `Takeaway`로 통일했습니다.
- `data/papers.json`: 기존 번호형 요약 2편의 라벨을 새 표준으로 변환했습니다.
- `README.md`: 요약 형식 설명과 schema 예시를 새 표준으로 갱신했습니다.
- `ARCHITECTURE.md`: 요약 구조 설명을 새 표준으로 갱신했습니다.
- `index.html`: JS/CSS cache-busting version을 갱신했습니다.
- `AGENT_LOG.md`: 이번 요약 표준 변경 작업을 기록했습니다.

### 구현한 기능
- 새 OpenAI 요약과 fallback 요약은 `Topic / Problem / Method / Key Result / Takeaway` 형식을 사용합니다.
- 프론트엔드의 한글/영문 모드는 동일한 5개 라벨을 표시합니다.

### 설계 결정
- 답변은 한국어로 유지하고, 질문 라벨은 논문 리뷰에 적합한 짧은 영문 키워드를 사용합니다.
- 기존 요약 내용은 재생성하지 않고 라벨만 변환해 불필요한 OpenAI 비용을 만들지 않았습니다.

### 남은 작업
- 전체 OpenAI 재요약 workflow를 실행하면 나머지 문단형 요약도 새 5문항 표준으로 생성됩니다.

### 주의사항
- 이번 변경 자체는 OpenAI API를 호출하지 않았습니다.
- raw abstract와 PDF는 저장하지 않았습니다.

## 2026-06-12 21:53

### 변경 요약
- OpenAI가 `ai_summary_ko`를 dict 객체가 아니라 dict처럼 생긴 문자열로 반환하는 케이스를 추가로 확인했습니다.
- 문자열 형태의 `{'1': '...', '2': '...'}` 응답도 5문항 줄바꿈 텍스트로 변환하도록 보강했습니다.

### 수정/생성한 파일
- `scripts/summarize.py`: `ast.literal_eval` 기반으로 dict/list 문자열 응답을 파싱한 뒤 표준 5문항 텍스트로 변환하도록 수정했습니다.
- `AGENT_LOG.md`: 이번 OpenAI 문자열 응답 정규화 보정을 기록했습니다.

### 구현한 기능
- OpenAI 응답이 dict, list, dict-like string 어느 형태여도 `ai_summary_ko`는 표준 5줄 텍스트로 저장됩니다.

### 설계 결정
- 프론트엔드가 아니라 저장 전 sanitizer에서 응답 변형을 흡수하도록 했습니다.

### 남은 작업
- 동일 1편 OpenAI 재요약 workflow를 다시 실행해 공개 `papers.json`의 요약이 5줄 텍스트로 저장되는지 확인해야 합니다.

### 주의사항
- 이번 수정 자체는 OpenAI API를 호출하지 않습니다.

## 2026-06-12 21:51

### 변경 요약
- OpenAI 1편 테스트는 인증에 성공했지만, 모델이 `ai_summary_ko`를 문자열 대신 JSON 객체 형태로 반환해 사이트 표시가 한 줄 dict처럼 보일 수 있는 문제를 확인했습니다.
- OpenAI 응답의 `ai_summary_ko`가 dict/list/string 어느 형태든 5문항 텍스트로 정규화하도록 수정했습니다.

### 수정/생성한 파일
- `scripts/summarize.py`: `_normalize_generated_summary()`를 추가하고 `_sanitize_generated()`에서 사용하도록 변경했습니다.
- `AGENT_LOG.md`: 이번 OpenAI 응답 정규화 보정 작업을 기록했습니다.

### 구현한 기능
- `{ "1": "...", "2": "..." }` 형태의 OpenAI 응답도 `1. 무엇에 관한 논문인가? ...` 형식의 줄바꿈 텍스트로 저장됩니다.
- list 형태 응답도 동일하게 5문항 텍스트로 변환합니다.

### 설계 결정
- 프론트엔드에서 dict 문자열을 해석하게 하지 않고, 데이터 저장 단계에서 표준 문자열 형식으로 정규화하기로 했습니다.
- 기존 `ai_summary_ko` schema를 유지합니다.

### 남은 작업
- 이 수정 사항을 배포한 뒤 동일 1편 OpenAI 재요약 테스트를 다시 실행해야 합니다.

### 주의사항
- 이번 수정 자체는 API 호출을 하지 않습니다. 재테스트 workflow 실행 시 1편 분량의 OpenAI 비용이 발생합니다.

## 2026-06-12 21:45

### 변경 요약
- 한국어/영어 모드에서 논문 요약 카드의 표시 틀이 달라지는 문제를 수정했습니다.
- 영어 모드가 저장된 요약 형식과 무관하게 자체 5문항 Q/A를 생성하던 동작을 제거했습니다.
- 이제 저장된 `ai_summary_ko`가 5문항 형식이면 양쪽 모드 모두 Q/A 블록을 사용하고, 문단형이면 양쪽 모드 모두 문단형 표시를 사용합니다.

### 수정/생성한 파일
- `assets/app.js`: `englishSummarySections()`를 제거하고 저장된 요약의 번호 구조를 기준으로 Q/A 렌더링 여부를 결정하도록 변경했습니다.
- `index.html`: JS/CSS cache-busting version을 갱신했습니다.
- `AGENT_LOG.md`: 이번 한영 요약 표시 틀 동기화 작업을 기록했습니다.

### 구현한 기능
- 한국어/영어 모드의 요약 카드 레이아웃이 같은 저장 데이터 형식을 기준으로 동작합니다.
- 기존 문단형 요약은 영어 모드에서도 Q/A처럼 보이지 않습니다.

### 설계 결정
- 아직 `ai_summary_en` 필드가 없으므로, 영어 모드에서 임의의 5문항 요약을 새로 만들지 않도록 했습니다.
- 고품질 영문 답변이 필요하면 OpenAI batch에서 `ai_summary_en` 필드를 별도로 생성하는 확장이 필요합니다.

### 남은 작업
- OpenAI API key를 올바르게 교체한 뒤 1편 테스트 재요약을 다시 실행해야 합니다.
- 장기적으로는 한글/영문 요약을 모두 저장하는 schema 확장을 검토할 수 있습니다.

### 주의사항
- 이번 변경은 프론트엔드 표시 로직만 수정하며 OpenAI API 호출 비용은 발생하지 않습니다.

## 2026-06-12 21:37

### 변경 요약
- 사용자가 OpenAI API key 준비를 완료했다고 알려 기존 논문 전체를 OpenAI 기반 5문항 요약으로 재생성할 수 있는 수동 batch 경로를 추가했습니다.
- 정기 수집 workflow와 OpenAI 전체 재요약 workflow를 분리해 비용이 매시간 반복 발생하지 않도록 했습니다.
- 한 번에 처리할 논문 수, 재요약 대상, dry-run 여부를 workflow input으로 제어하도록 했습니다.

### 수정/생성한 파일
- `scripts/summarize.py`: 요약 생성 결과가 OpenAI인지 fallback인지 임시 `_summary_provider`로 표시하도록 했습니다.
- `scripts/refresh_openai_summaries.py`: 기존 `data/papers.json` 항목을 OpenAI로 재요약하는 수동 batch 스크립트를 추가했습니다.
- `.github/workflows/refresh-openai-summaries.yml`: `workflow_dispatch` 전용 OpenAI 재요약 workflow를 추가했습니다.
- `README.md`: GitHub Actions에서 전체 OpenAI 재요약 workflow를 실행하는 방법을 문서화했습니다.
- `ARCHITECTURE.md`: 수동 OpenAI 재요약 파이프라인과 환경변수를 문서화했습니다.
- `PROJECT_STATUS.md`: 완료 기능과 다음 작업에 OpenAI batch 재요약 workflow를 반영했습니다.
- `AGENT_LOG.md`: 이번 OpenAI batch 재요약 기능 추가를 기록했습니다.

### 구현한 기능
- `Refresh OpenAI summaries` workflow에서 `max_summaries`, `refresh_mode`, `dry_run`을 입력받아 기존 논문을 재요약할 수 있습니다.
- `refresh_mode=non_qa`는 아직 5문항 형식이 아닌 논문만 재요약합니다.
- `max_summaries=400`을 사용하면 현재 342편 전체를 한 번에 처리할 수 있습니다.
- OpenAI key가 없으면 스크립트는 실패하지 않고 재요약을 건너뜁니다.

### 설계 결정
- 비용 안전성을 위해 이 작업은 cron에 연결하지 않고 수동 실행 전용 workflow로 분리했습니다.
- 초록은 OpenAlex DOI endpoint에서 임시로 읽어 요약 입력으로만 사용하고 `data/papers.json`에는 저장하지 않습니다.
- OpenAI 호출이 실패해 fallback으로 내려간 항목은 OpenAI 재요약 성공으로 집계하지 않도록 `_summary_provider`를 사용했습니다.

### 남은 작업
- GitHub Actions에서 `Refresh OpenAI summaries`를 수동 실행해 실제 342편 재요약을 수행해야 합니다.
- 실행 후 공개 `data/papers.json`에서 5문항 요약 개수가 전체 논문 수와 맞는지 확인해야 합니다.

### 주의사항
- API key, secret, token은 로그에 기록하지 않았습니다.
- 이 workflow를 `max_summaries=400`, `dry_run=false`로 실행하면 OpenAI API 비용이 발생합니다.
- PDF 다운로드나 출판사 웹사이트 크롤링은 수행하지 않습니다.

## 2026-06-12 21:12

### 변경 요약
- 5문항 요약이 데이터에 있어도 질문 문구 완전 일치 여부 때문에 Q/A 블록으로 렌더링되지 않을 수 있는 문제를 개선했습니다.
- 프론트엔드 요약 파서를 질문 문구가 아니라 `1.`부터 `5.`까지의 번호 기반으로 인식하도록 바꿨습니다.
- 사용자가 물어본 비용 문제를 확인하며, 기존 전체 논문을 OpenAI로 재요약하지 않는 한 이번 수정 자체에는 OpenAI 비용이 들지 않는다는 점을 기록했습니다.

### 수정/생성한 파일
- `assets/app.js`: 한국어 5문항 요약 파서를 번호 기반으로 완화했습니다.
- `index.html`: JS/CSS cache-busting version을 갱신했습니다.
- `AGENT_LOG.md`: 이번 Q/A 렌더링 파서 수정과 비용 관련 주의사항을 기록했습니다.

### 구현한 기능
- `1. ...`, `2. ...` 형식으로 저장된 요약은 질문 문구가 조금 달라도 카드에서 Q/A 블록으로 표시됩니다.

### 설계 결정
- 기존 `ai_summary_ko` 스키마를 유지하고 프론트엔드 파서를 더 견고하게 만드는 방식을 선택했습니다.
- 전체 논문 재요약은 별도 batch 작업으로 분리하는 것이 안전합니다.

### 남은 작업
- 기존 342편 전체를 5문항 형식으로 통일하려면 OpenAlex 초록을 다시 임시 입력으로 읽어 fallback 재요약하는 batch 작업을 별도로 수행할 수 있습니다.
- OpenAI 기반 고품질 전체 재요약은 비용이 발생하므로 명시적으로 선택한 경우에만 수행해야 합니다.

### 주의사항
- raw abstract와 PDF는 계속 저장하지 않습니다.
- API key, secret, token은 기록하지 않았습니다.

## 2026-06-12 21:09

### 변경 요약
- 왼쪽 사이드바의 Robotics for Manufacturing 서브토픽에서 `Path Planning`을 제거하고 `Process Optimization`으로 대체했습니다.
- `Design Automation` 신호가 로봇 키워드보다 먼저 `AI Manufacturing`으로 분류되도록 분야 판별 순서를 조정했습니다.
- path planning/trajectory 관련 신호가 공정 최적화 계열로도 잡히도록 서브토픽 판별을 보강했습니다.

### 수정/생성한 파일
- `assets/app.js`: `FIELD_SUBTOPICS`, `deriveField()`, `deriveSubtopics()` 분류 규칙을 수정했습니다.
- `index.html`: JS/CSS cache-busting version을 갱신했습니다.
- `AGENT_LOG.md`: 이번 사이드바 분류 조정 작업을 기록했습니다.

### 구현한 기능
- Robotics for Manufacturing 아래에는 `Robotic AM`, `Manufacturing Automation`, `Process Optimization`이 표시됩니다.
- `Design Automation`은 AI Manufacturing 아래로 더 우선적으로 분류됩니다.
- 기존에 Robotics 아래 `Path Planning 0`처럼 보이던 빈 항목이 사라집니다.

### 설계 결정
- 단순 표시명만 바꾸지 않고 분류 우선순위도 함께 조정했습니다. 그래야 카운트가 0으로 남는 문제를 줄일 수 있습니다.
- 로봇 논문 중 경로계획/trajectory 신호는 제조 공정 최적화 관점으로 묶어 표시합니다.

### 남은 작업
- 브라우저에서 실제 사이드바 표시를 최종 확인하면 좋습니다. 현재 환경에는 Node/브라우저 실행 도구가 없어 로컬 JS 런타임 검증은 제한적입니다.

### 주의사항
- 이번 변경은 UI 분류 규칙만 수정하며 데이터 수집, API key, raw abstract/PDF 정책에는 영향을 주지 않습니다.

## 2026-06-12 21:07

### 변경 요약
- 논문 요약의 표준 형식을 사용자가 제안한 5문항 Q/A 구조로 변경했습니다.
- 프론트엔드가 5문항 요약을 감지하면 카드 안에서 Q/A 블록으로 렌더링하도록 개선했습니다.
- 예시 논문 `Material articulation: Toward an ornamental thinking in digital tectonics`의 요약을 새 5문항 형식으로 갱신했습니다.

### 수정/생성한 파일
- `scripts/summarize.py`: OpenAI 프롬프트와 fallback 요약 생성기를 5문항 형식으로 변경했습니다.
- `assets/app.js`: `ai_summary_ko`의 5문항 형식을 파싱해 Q/A 블록으로 표시하는 렌더링 로직을 추가했습니다.
- `assets/style.css`: 요약 Q/A 블록의 spacing, border, 다크모드 대비 스타일을 추가했습니다.
- `data/papers.json`: DOI `10.21606/drs.2026.2363` 항목을 5문항 요약으로 갱신했습니다.
- `index.html`: CSS/JS cache-busting version을 갱신했습니다.
- `README.md`: 요약 형식과 API key가 없을 때의 fallback 요약 정책을 갱신했습니다.
- `ARCHITECTURE.md`: 5문항 요약 데이터/렌더링 구조를 문서화했습니다.
- `PROJECT_STATUS.md`: 현재 논문 수와 완료 기능 상태를 최신화했습니다.
- `AGENT_LOG.md`: 이번 요약 형식 변경 작업을 기록했습니다.

### 구현한 기능
- 새 논문 요약은 다음 질문에 답하도록 생성됩니다: 무엇에 관한 논문인가, 어떤 문제를 해결하려고 하는가, 어떤 방법을 쓰는가, 핵심 결과는 무엇인가, 내 연구/발표에 왜 필요한가.
- 구조화된 요약은 카드에서 작은 Q/A 리스트로 표시됩니다.
- 기존 문단형 요약이 남아 있는 논문은 paragraph fallback으로 계속 표시됩니다.

### 설계 결정
- `ai_summary_ko` 필드를 새로 쪼개지 않고 기존 필드 안에 번호가 붙은 5문항 텍스트를 저장했습니다. 기존 schema와 GitHub Pages 정적 렌더링을 유지하기 위해서입니다.
- 영어 모드에는 별도 `ai_summary_en` 필드가 아직 없으므로, 메타데이터 기반 5문항 영어 표시 요약을 안전한 fallback으로 제공합니다.
- raw abstract는 계속 저장하지 않고 요약 생성 입력으로만 사용합니다.

### 남은 작업
- 기존 159편 전체의 문단형 요약을 한 번에 5문항 형식으로 batch refresh하면 사이트 전체의 요약 품질이 더 균일해집니다.
- 별도 `ai_summary_en` 필드를 추가하면 영어 모드에서도 초록 기반 고품질 요약을 제공할 수 있습니다.

### 주의사항
- API key, secret, token은 기록하지 않았습니다.
- PDF 다운로드나 출판사 웹사이트 크롤링은 수행하지 않았습니다.
- 현재 환경에 Node가 없어 `node --check assets/app.js` 검증은 실행하지 못할 수 있습니다.

## 2026-06-12 18:48

### 변경 요약
- 초록 기반 fallback 요약이 “무슨 분야에 속한다”는 식으로 너무 분류 설명처럼 보이던 문제를 개선했습니다.
- `Material articulation: Toward an ornamental thinking in digital tectonics` 논문의 요약을 연구 대상, 접근 방식, 핵심 기여가 드러나도록 갱신했습니다.
- venue 카드의 긴 라벨과 `priority` 표현이 어색하게 보이던 UI를 짧고 안정적인 카드 디자인으로 조정했습니다.

### 수정/생성한 파일
- `scripts/summarize.py`: 초록에서 연구 대상, 접근 방식, 특징/기여를 추론하는 fallback 요약 함수를 추가하고 관련성 설명 문구를 완화했습니다.
- `data/papers.json`: DOI `10.21606/drs.2026.2363` 항목의 요약, 관련성 설명, 태그를 갱신했습니다.
- `assets/app.js`: venue 라벨을 `Core`, `2 or fewer papers`처럼 짧게 바꾸고 venue 카드 숫자 마크업을 분리했습니다.
- `assets/style.css`: venue 카드 숫자와 라벨 칩의 간격, 크기, 다크모드 대비를 조정했습니다.
- `index.html`: CSS/JS cache-busting version을 갱신했습니다.
- `AGENT_LOG.md`: 이번 요약 품질 및 UI 개선 작업을 기록했습니다.

### 구현한 기능
- fallback 요약이 초록 원문을 복사하지 않고, 논문의 연구 내용과 특징을 새 한국어 문장으로 설명하도록 개선했습니다.
- 특정 DRS 논문은 “대형 적층제조에서 장식을 재료 거동, 공정 흔적, 제작 논리가 드러나는 설계 요소로 해석한다”는 내용 중심으로 표시됩니다.
- venue board의 `priority` 라벨은 `Core`로 바꾸고, 기타 게재지 라벨은 짧은 표현으로 줄였습니다.

### 설계 결정
- OpenAlex가 제공하는 초록은 요약 입력으로만 사용하고 `data/papers.json`에는 저장하지 않았습니다.
- PDF 다운로드나 출판사 페이지 크롤링은 수행하지 않았습니다.
- 태그는 한국어 모드에서 자연스럽게 보이도록 한국어 중심으로 저장하고, 영어 모드에서는 `assets/app.js` 번역 테이블로 표시되게 했습니다.

### 남은 작업
- 기존에 생성된 다른 generic 요약들도 같은 방식으로 일괄 갱신하면 전체 카드 품질이 좋아질 수 있습니다.
- 현재 환경에는 Node가 없어 `node --check assets/app.js`를 실행하지 못했습니다. GitHub Pages 배포 후 브라우저에서 최종 UI 확인을 권장합니다.

### 주의사항
- raw abstract는 계속 저장/표시하지 않습니다.
- API key, secret, token은 기록하지 않았습니다.
- fallback 요약은 모델 API 비용 없이 동작하지만, 초록이 없는 논문은 여전히 제목/메타데이터 기반의 보수적 요약이 될 수 있습니다.

## 2026-06-12 18:43

### 변경 요약
- LCE(liquid crystal elastomer) 논문이 누락된 원인을 확인하고, 검색어와 합법적 메타데이터 수집 필터를 확장했습니다.
- OpenAlex DOI 메타데이터 기준으로 2024년 LCE/4D printing 관련 논문 3편을 `data/papers.json`에 추가했습니다.
- OpenAlex rate limit 상황에 대비해 429 retry/backoff 로직을 추가했습니다.
- 미래 연도 논문이 섞이지 않도록 현재 연도 이후 논문은 제외하도록 연도 필터를 강화했습니다.

### 수정/생성한 파일
- `data/queries.json`: LCE, 4D printing, direct ink writing, stimuli-responsive LCE 관련 검색어를 추가했습니다.
- `data/seed_dois.json`: LCE 관련 검증 DOI 3개를 seed DOI로 추가했습니다.
- `data/papers.json`: 2024년 LCE 관련 논문 3편을 추가했습니다.
- `data/site_meta.json`: 총 논문 수와 마지막 갱신 시각 메타데이터를 현재 데이터 상태에 맞게 갱신했습니다.
- `scripts/update_papers.py`: LCE, 4D printing, direct ink writing, soft actuator, metamaterial 표현을 관련성 필터에 반영하고 미래 연도 필터를 강화했습니다.
- `scripts/summarize.py`: LCE, 4D printing, metamaterials 태그 판별 키워드를 추가했습니다.
- `scripts/fetch_openalex.py`: OpenAlex 429 응답에 대한 재시도와 지수 backoff를 추가했습니다.
- `AGENT_LOG.md`: 이번 LCE 보강 작업의 원인, 변경 내용, 정책 주의사항을 기록했습니다.

### 구현한 기능
- LCE/4D printing 논문이 자동 수집 후보에 포함되도록 검색 범위를 확장했습니다.
- DOI 기반 seed 수집으로 누락 가능성이 큰 핵심 논문을 안정적으로 포함했습니다.
- 새로 추가한 논문도 기존 정책과 동일하게 raw abstract를 표시하거나 저장하지 않고, PDF도 다운로드/저장하지 않습니다.
- OpenAlex 일시적 rate limit이 있어도 workflow가 더 안정적으로 재시도할 수 있게 했습니다.

### 설계 결정
- 출판사 웹사이트 크롤링이나 PDF 다운로드 없이 OpenAlex DOI 메타데이터 API를 사용했습니다.
- LCE는 4D printing, direct ink writing, shape morphing, stimuli-responsive actuator 문헌과 함께 검색되므로 additive manufacturing 키워드만으로 제한하지 않도록 필터를 넓혔습니다.
- Crossref/OpenAlex에서 미래 연도 메타데이터가 섞일 수 있어 현재 연도 이후 항목은 제외하도록 했습니다.
- API key, secret, token은 로그나 코드에 기록하지 않았습니다.

### 남은 작업
- GitHub Actions 정기 실행 후에도 LCE 검색어가 충분히 작동하는지 다음 자동 갱신 결과를 확인하는 것이 좋습니다.
- LCE 하위 태그가 UI에서 과도하게 늘어나면 `assets/app.js`의 토픽 그룹 표현을 추가 정리할 수 있습니다.

### 주의사항
- raw abstract는 AI 요약 입력으로만 사용해야 하며 사이트나 JSON의 표시 필드로 저장하지 않습니다.
- PDF는 다운로드하거나 저장하지 않습니다.
- OpenAlex 검색 API가 429를 반환할 수 있으므로 지나치게 공격적인 수집 주기나 쿼리 수 증가는 피해야 합니다.

## 2026-06-12 19:55

### 변경 요약
- fallback 요약이 제목/메타데이터 기반 안내문처럼 보이던 문제를 개선했습니다.
- OpenAI API key가 없을 때도 초록이 제공되면 초록 내용을 바탕으로 새 한국어 요약문을 작성하도록 변경했습니다.
- 사용자가 지적한 `Material articulation: Toward an ornamental thinking in digital tectonics` 항목의 요약을 초록 기반 fallback 요약으로 갱신했습니다.

### 수정/생성한 파일
- `scripts/summarize.py`: `summarize_record(..., allow_openai=True)` 옵션을 추가했습니다.
- `scripts/summarize.py`: 초록 기반 fallback 요약 생성 로직과 키워드 기반 focus/method/outcome 추출 함수를 추가했습니다.
- `scripts/update_papers.py`: 기존 generic 요약이 있고 새 API 응답에 초록이 있으면 OpenAI 없이 fallback 요약으로 갱신하도록 변경했습니다.
- `data/papers.json`: DOI `10.21606/drs.2026.2363` 논문의 요약을 초록 기반 새 요약으로 갱신했습니다.
- `AGENT_LOG.md`: 이번 요약 품질 개선 작업을 기록했습니다.

### 구현한 기능
- 새 논문은 기존처럼 OpenAI key가 있으면 OpenAI 요약을 사용할 수 있습니다.
- 기존 generic 요약 refresh는 `allow_openai=False`로 수행되어 OpenAI 비용을 만들지 않습니다.
- 초록은 `_abstract` transient 입력으로만 사용하고, 저장 전 제거하는 정책을 유지합니다.
- fallback 요약은 초록 원문 문장을 복사하지 않고 focus/method/outcome을 새 한국어 문장으로 재구성합니다.

### 설계 결정
- 출판사 초록 원문을 사이트에 표시하거나 저장하지 않는 정책은 유지했습니다.
- 전체 기존 데이터 재요약은 시간이 오래 걸릴 수 있어, 우선 지적된 논문을 targeted refresh하고 이후 정기 수집 때 generic 요약을 점진적으로 갱신하도록 했습니다.
- 기존 논문 refresh에는 OpenAI를 쓰지 않아 예상치 못한 비용 증가를 막았습니다.

### 남은 작업
- 전체 기존 generic 요약을 한 번에 정리하려면 별도 batch refresh script를 만들고 API rate limit을 고려해 나누어 실행하는 것이 좋습니다.
- 더 높은 품질의 한영 요약을 원하면 향후 `ai_summary_en` 필드와 OpenAI 기반 batch 재요약 정책을 별도로 설계할 수 있습니다.

### 주의사항
- API key, secret, token은 기록하지 않았습니다.
- raw abstract와 PDF는 계속 저장/표시하지 않습니다.

## 2026-06-12 19:41

### 변경 요약
- venue 섹션의 설명 문구와 display rule 문구를 제거했습니다.
- UI가 충분히 카드/그룹 구조로 의미를 전달하므로 중복 설명을 줄였습니다.

### 수정/생성한 파일
- `index.html`: venue 섹션 header의 설명 paragraph를 제거하고 cache-busting version을 갱신했습니다.
- `assets/app.js`: `venuesDescription`, `venueRule` 텍스트와 해당 문구 렌더링/언어 전환 업데이트를 제거했습니다.
- `assets/style.css`: 더 이상 사용하지 않는 `.venue-rule` 스타일과 다크 모드 참조를 제거했습니다.
- `AGENT_LOG.md`: 이번 venue 설명 문구 제거 작업을 기록했습니다.

### 구현한 기능
- `Core venues and journals with at least two collected papers are shown individually; the rest are grouped as Others.` 문구가 더 이상 표시되지 않습니다.
- `Display rule: core venues and 2+ paper journals are shown individually; all others are grouped.` 문구가 더 이상 표시되지 않습니다.

### 설계 결정
- 설명 텍스트를 줄여 venue 카드 자체가 먼저 보이도록 했습니다.
- 사용하지 않는 CSS와 번역 키도 함께 제거해 유지보수 부담을 줄였습니다.

### 남은 작업
- 없음.

### 주의사항
- 이번 변경은 UI 텍스트 제거만 수행하며 데이터 수집/API 비용에는 영향이 없습니다.

## 2026-06-12 19:34

### 변경 요약
- 왼쪽 sidebar에서 메인 토픽 count와 subtopic count 합계가 맞지 않아 혼란스러운 문제를 개선했습니다.
- 각 메인 토픽 아래에 정의된 subtopic을 모두 표시하고, 어느 subtopic에도 배정되지 않은 논문은 `Others` bucket으로 묶도록 변경했습니다.

### 수정/생성한 파일
- `assets/app.js`: `SIDEBAR_OTHER_TOPIC`, `sidebarBucketCounts()`, `sidebarBucketForPaper()`, `sideSubtopicButton()`, `paperMatchesSidebarSubtopic()`을 추가했습니다.
- `assets/app.js`: sidebar subtopic count와 click filter가 동일한 bucket 기준을 사용하도록 변경했습니다.
- `assets/style.css`: 0개 subtopic의 disabled/empty 스타일과 다크 모드 empty hover 스타일을 추가했습니다.
- `index.html`: CSS/JS cache-busting version을 갱신했습니다.
- `AGENT_LOG.md`: 이번 sidebar bucket/count 정합성 개선 내용을 기록했습니다.

### 구현한 기능
- 메인 토픽 아래 모든 대표 subtopic을 표시합니다.
- count가 0인 subtopic도 흐리게 표시해 “현재 해당 논문 없음”을 알 수 있습니다.
- 각 field에서 대표 subtopic에 속하지 않은 논문은 `Others`로 표시합니다.
- `Others`를 클릭하면 해당 field 안에서 대표 subtopic에 배정되지 않은 논문만 필터링됩니다.
- 결과적으로 메인 토픽 count를 subtopic count들의 합으로 이해할 수 있습니다.

### 설계 결정
- `deriveSubtopics()`의 넓은 키워드 감지 대신 sidebar는 `representativeTags()` 기반 bucket을 사용합니다.
- 하나의 논문은 sidebar에서 한 field 안의 하나의 bucket에만 배정되도록 하여 count 해석을 단순하게 했습니다.
- 0개 subtopic을 숨기지 않고 disabled 상태로 남겨 사용자에게 전체 subtopic 구조를 보여줍니다.

### 남은 작업
- 실제 UI에서 `Others` 비율이 너무 크면 대표 subtopic 목록을 더 세분화할 수 있습니다.

### 주의사항
- 데이터 파일과 자동 수집 파이프라인은 변경하지 않았습니다.
- 이번 변경은 프론트엔드 sidebar 표시/필터 기준 조정이며 API 비용에는 영향이 없습니다.

## 2026-06-12 19:22

### 변경 요약
- 왼쪽 sidebar의 subtopic 목록을 대표 탐색용 토픽만 남기도록 정리했습니다.
- `MMAM`, `FGAM`, `DM filament`, `FDM/Material extrusion`처럼 서로 겹치는 3D 재료/압출 계열 토픽은 sidebar에서 제거했습니다.
- sidebar subtopic count를 넓은 키워드 감지 기준이 아니라 카드 대표 태그 기준으로 다시 계산하도록 변경했습니다.

### 수정/생성한 파일
- `assets/app.js`: `FIELD_SUBTOPICS`를 대표 토픽 중심으로 정리했습니다.
- `assets/app.js`: `paperHasRepresentativeTopic()`을 추가해 sidebar count와 sidebar click filter가 카드 대표 태그 기준을 따르도록 했습니다.
- `index.html`: CSS/JS cache-busting version을 갱신했습니다.
- `AGENT_LOG.md`: 이번 sidebar 대표 토픽 정리 내용을 기록했습니다.

### 구현한 기능
- sidebar에서 모든 논문에 붙어 보이던 `MMAM 100`, `FGAM 100`, `DM filament 100`, `FDM/Material extrusion 100`류의 중복 표시를 제거했습니다.
- sidebar count는 실제 카드에 대표 태그로 표시되는 논문 수와 더 가깝게 계산됩니다.
- subtopic을 클릭했을 때도 같은 대표 태그 기준으로 필터링합니다.

### 설계 결정
- 카드 내부에는 세부 대표 태그를 유지하되, 왼쪽 sidebar는 탐색을 위한 상위/대표 필터만 보여주도록 역할을 분리했습니다.
- `deriveSubtopics()`는 검색/필터 보조용으로 유지하고, sidebar 표시와 count는 `representativeTags()` 기반으로 좁혔습니다.

### 남은 작업
- 실제 배포 화면에서 sidebar count가 기대한 수준으로 줄었는지 확인하고, 너무 적게 잡히는 토픽은 대표 태그 규칙을 조정할 수 있습니다.

### 주의사항
- 데이터 파일과 자동 수집 로직은 변경하지 않았습니다.
- 이번 변경은 프론트엔드 표시/필터 기준 조정이며 API 호출 비용에는 영향이 없습니다.

## 2026-06-12 19:10

### 변경 요약
- 왼쪽 sidebar의 긴 분야 라벨과 숫자 count가 너무 붙어 보이는 문제를 개선했습니다.
- `Production / Manufacturing`, `Robotics for Manufacturing` 같은 긴 라벨에서도 숫자가 독립된 badge처럼 보이도록 정리했습니다.

### 수정/생성한 파일
- `assets/app.js`: sidebar field/subtopic 버튼의 라벨과 숫자를 `side-label`, `side-count` span으로 분리했습니다.
- `assets/style.css`: sidebar 버튼을 grid layout으로 변경하고 라벨/숫자 사이 간격, count badge 최소폭과 색상을 지정했습니다.
- `assets/style.css`: 다크 모드 active/hover 상태에서 sidebar count badge 대비를 개선했습니다.
- `index.html`: CSS/JS cache-busting version을 갱신했습니다.
- `AGENT_LOG.md`: 이번 sidebar count spacing 개선 내용을 기록했습니다.

### 구현한 기능
- 긴 sidebar 라벨과 숫자 count가 서로 붙지 않고 분리되어 표시됩니다.
- count는 최소 폭을 가진 pill badge로 표시되어 숫자 자리가 안정적으로 보입니다.
- 다크 모드에서 active/hover sidebar count도 밝은 badge + 어두운 숫자로 표시됩니다.

### 설계 결정
- 기존 `float: right` 방식 대신 CSS grid의 `minmax(0, 1fr) auto` 구조를 사용했습니다. 긴 라벨과 숫자 영역을 명확히 분리하기 위해서입니다.

### 남은 작업
- 실제 모바일 폭에서 sidebar가 접히는 구간의 count badge 간격을 추가 확인하면 좋습니다.

### 주의사항
- 이번 변경은 sidebar UI 마크업/스타일 조정이며 데이터 수집에는 영향을 주지 않습니다.

## 2026-06-12 19:02

### 변경 요약
- UI 라벨과 버튼 여백을 조정해 왼쪽 분야 패널과 venue pill이 덜 답답하게 보이도록 개선했습니다.
- 영어 라벨 `Production/Manufacturing`을 `Production / Manufacturing`으로 변경했습니다.
- 다크 모드에서 active venue pill의 숫자 배지 색상 대비를 개선했습니다.

### 수정/생성한 파일
- `assets/app.js`: 영어 번역 라벨 `Production / Manufacturing`으로 변경했습니다.
- `assets/style.css`: topic/venue pill과 sidebar field/subtopic 버튼의 padding, line-height, font-size를 조정했습니다.
- `assets/style.css`: 다크 모드 active venue pill 숫자 배지의 배경/글자색을 별도로 지정했습니다.
- `index.html`: CSS/JS cache-busting version을 갱신했습니다.
- `AGENT_LOG.md`: 이번 UI 조정 내용을 기록했습니다.

### 구현한 기능
- 왼쪽 분야 패널에서 긴 영어 라벨이 박스에 너무 꽉 차 보이는 문제를 줄였습니다.
- venue pill의 숫자 badge가 다크 모드 active 상태에서도 읽히도록 했습니다.

### 설계 결정
- 텍스트를 무리하게 키우기보다 padding과 line-height를 늘리고 font-size를 소폭 줄여 가독성과 밀도를 균형 있게 맞췄습니다.
- 다크 모드 active count badge는 밝은 배경 + 어두운 숫자로 고정해 클릭 상태에서도 명확한 대비를 유지합니다.

### 남은 작업
- 실제 모바일 화면에서 긴 venue 이름/field label이 자연스럽게 줄바꿈되는지 추가 확인하면 좋습니다.

### 주의사항
- 이번 변경은 UI 스타일과 라벨만 바꾸며, API 호출/비용/데이터 수집에는 영향을 주지 않습니다.

## 2026-06-12 18:46

### 변경 요약
- 카드 대표 태그에서 `MMAM`, `FGAM`, `DM filament`, `FDM/Material extrusion`이 중복 표시되지 않도록 분류 기준을 정리했습니다.
- 네 태그가 동시에 후보로 잡히더라도 카드에는 가장 적절한 대표 분류 하나만 표시됩니다.

### 수정/생성한 파일
- `assets/app.js`: `collapseMaterialExtrusionTags()`를 추가해 소재/압출 계열 중복 태그를 상호배타적으로 정리했습니다.
- `index.html`: JS/CSS cache-busting version을 갱신했습니다.
- `AGENT_LOG.md`: 이번 태그 분류 기준 변경을 기록했습니다.

### 구현한 기능
- `DM filament`, `FGAM`, `MMAM`, `FDM/Material extrusion`이 카드 대표 태그에 동시에 표시되지 않습니다.
- 분류 우선 기준은 논문 제목/venue/tags/categories/요약 메타데이터를 기반으로 합니다.
- `digital material`, `digital material filament`, `blended FDM` 신호가 있으면 `DM filament`를 우선 표시합니다.
- `functionally graded`, `functional gradient`, `graded`, `FGAM` 신호가 있으면 `FGAM`을 우선 표시합니다.
- `multi-material`, `multimaterial`, `MMAM` 신호가 있으면 `MMAM`을 우선 표시합니다.
- 위 신호 없이 FDM/material extrusion만 있으면 `FDM/Material extrusion`을 표시합니다.

### 설계 결정
- 검색/필터용 서브토픽은 유지하고, 카드에 보이는 대표 태그만 상호배타적으로 정리했습니다. 필터링 가능성은 유지하면서 카드 가독성과 분류 명확성을 높이기 위해서입니다.
- `data/papers.json`은 수정하지 않고 프론트엔드 표시 로직에서 해결했습니다.

### 남은 작업
- 향후 데이터 품질을 더 높이려면 Python 요약/분류 단계에서도 동일한 상호배타 규칙을 적용할 수 있습니다.

### 주의사항
- 이번 변경은 UI 표시 분류 기준 변경이며, API 호출이나 비용에는 영향을 주지 않습니다.
- raw abstract와 PDF는 계속 저장/표시하지 않습니다.

## 2026-06-12 18:38

### 변경 요약
- 사이트 기본 표시 모드를 영어 + 다크 모드로 변경했습니다.
- 영어 모드에서 논문 카드의 요약과 관련성 설명이 한글 그대로 보이던 문제를 개선했습니다.
- 영어 모드에서 일부 태그가 한국어로 남는 문제를 줄이기 위해 canonical tag와 번역 규칙을 보강했습니다.

### 수정/생성한 파일
- `assets/app.js`: 기본 `theme`을 `dark`, 기본 `language`를 `en`으로 변경했습니다.
- `assets/app.js`: 기존 방문자의 저장된 이전 기본값을 새 기본값으로 한 번 마이그레이션하는 `preferenceVersion` 로직을 추가했습니다.
- `assets/app.js`: 영어 모드용 `formatSummary()`, `formatRelevanceNote()`, `formatEnglishList()`를 추가했습니다.
- `assets/app.js`: 한국어/영어 혼합 태그를 대표 영어 라벨로 정규화하는 규칙을 보강했습니다.
- `index.html`: 초기 HTML lang, theme, 버튼 텍스트, subtitle, notice 문구, CSS/JS cache-busting version을 영어/다크 기본값에 맞게 변경했습니다.
- `AGENT_LOG.md`: 이번 언어/테마 기본값 및 영어 표시 개선 내용을 기록했습니다.

### 구현한 기능
- 새 방문자의 기본 화면은 영어 + 다크 모드입니다.
- 기존 방문자도 이번 preference version에서는 한 번 영어 + 다크 모드로 초기화됩니다. 이후 사용자가 토글로 바꾼 값은 다시 유지됩니다.
- 영어 모드에서는 저장된 `ai_summary_ko`를 그대로 표시하지 않고, 제목/연도/venue/대표 태그/관련성 점수 기반의 영어 표시 요약을 생성합니다.
- 영어 모드에서는 관련성 설명도 영어 문장으로 표시합니다.
- `툴패스`, `경로계획`, `공정 최적화`, `제조 자동화`, `설계 자동화`, `메타물질` 등 주요 태그가 영어 모드에서 영어로 표시되도록 보강했습니다.

### 설계 결정
- `data/papers.json`에는 현재 한국어 AI 요약만 저장되어 있으므로, 영어 모드에서는 원문 초록을 사용하지 않고 저장된 공개 메타데이터 기반의 새 영어 표시 문장을 클라이언트에서 생성합니다.
- 출판사 초록을 번역하거나 표시하지 않는 정책은 유지했습니다.
- 사용자가 직접 선택한 언어/테마는 preference version 마이그레이션 이후 다시 존중합니다.

### 남은 작업
- 완전한 고품질 영문 논문 요약을 저장하려면 향후 업데이트 파이프라인에서 `ai_summary_en` 필드를 생성하도록 확장할 수 있습니다.
- 현재 영어 요약은 metadata-based display summary이며, 한국어 AI 요약의 정밀 번역은 아닙니다.

### 주의사항
- API key, secret, token은 기록하지 않았습니다.
- 이번 변경은 프론트엔드 표시 로직 중심이며, OpenAI API 호출 비용을 추가로 발생시키지 않습니다.
- raw abstract와 PDF는 계속 저장/표시하지 않습니다.

## 2026-06-12 18:24

### 변경 요약
- 논문 카드에 표시되는 태그를 관련 대표 토픽 3개로 제한했습니다.
- 중복 의미를 갖는 카테고리/서브토픽/태그가 한 카드에 길게 반복 표시되는 문제를 줄였습니다.
- 4D 프린팅 서브토픽에 `LCE`와 `메타물질`을 추가했습니다.

### 수정/생성한 파일
- `assets/app.js`: `representativeTags()`, `canonicalTopicLabel()`, `normalizeTopicKey()`를 추가해 카드 표시용 대표 태그를 최대 3개로 정리했습니다.
- `assets/app.js`: 4D 프린팅 서브토픽 목록에 `LCE`, `메타물질`을 추가하고, LCE/liquid crystal elastomer/metamaterial 키워드 감지 규칙을 추가했습니다.
- `assets/app.js`: 영어 모드에서 `메타물질`이 `Metamaterials`로 표시되도록 번역 항목을 추가했습니다.
- `index.html`: CSS/JS cache-busting version을 갱신했습니다.
- `AGENT_LOG.md`: 이번 태그 표시 정책 변경을 기록했습니다.

### 구현한 기능
- 카드의 태그 라인은 대표 토픽 3개만 표시합니다.
- `MMAM`, `FGAM`, `DM filament`, `FDM/Material extrusion`, `DLP`, `LCE`, `메타물질`, `4D printing`, `Toolpath`, `Path Planning`, `Process Optimization`, `Manufacturing Automation`, `Design Automation`, `AI/ML` 등은 canonical label로 정리됩니다.
- 4D printing, LCE, liquid crystal elastomer, metamaterial 관련 논문은 4D 프린팅 분야/서브토픽에서 더 잘 잡히도록 했습니다.

### 설계 결정
- 검색/필터용 내부 토픽은 유지하고, 카드 표시만 대표 3개로 제한했습니다. 필터 기능을 줄이지 않으면서 카드 가독성을 높이기 위해서입니다.
- `data/papers.json`은 수정하지 않고 프론트엔드 표시 로직에서 태그를 정리했습니다. 자동 수집 파이프라인과 기존 데이터 schema에 영향을 주지 않기 위해서입니다.

### 남은 작업
- 실제 수집 데이터에서 LCE/metamaterial 논문이 늘어나면 검색어(`data/queries.json`)에도 관련 키워드를 추가할지 검토할 수 있습니다.

### 주의사항
- 이번 변경은 UI 표시와 분류 보조 규칙 변경이며, 출판사 초록/PDF 저장 정책에는 영향을 주지 않습니다.
- API key, secret, token은 기록하지 않았습니다.

## 2026-06-12 18:15

### 변경 요약
- 사이트 대표 제목에서 `Awesome` 문구를 제거했습니다.
- 제목을 더 담백한 `AI Manufacturing and 3D/4D Printing Research`로 정리했습니다.

### 수정/생성한 파일
- `index.html`: 브라우저 title과 H1에서 `Awesome`을 제거했습니다.
- `README.md`: README 대표 제목에서 `Awesome`을 제거했습니다.
- `AGENT_LOG.md`: 이번 제목 문구 변경 이력을 추가했습니다.

### 구현한 기능
- 사이트 첫 화면과 브라우저 탭에 `AI Manufacturing and 3D/4D Printing Research`가 표시됩니다.

### 설계 결정
- UI 구성은 Awesome-style 큐레이션 감각을 유지하되, 제목 자체는 프로젝트의 연구 트래커 성격이 더 직접적으로 드러나도록 간결하게 변경했습니다.

### 남은 작업
- GitHub Pages 배포 후 공개 URL에서 제목 반영 여부를 확인합니다.

### 주의사항
- 이번 변경은 제목 표시만 바꾸며, 데이터 수집/요약/API 비용에는 영향을 주지 않습니다.
- API key, secret, token은 기록하지 않았습니다.

## 2026-06-12 18:12

### 변경 요약
- 논문 카드 상단에 `ICLR 2026`, `arXiv 2025`, `Nat. Commun. 2024`처럼 게재지/플랫폼과 연도를 함께 보여주는 publication label을 추가했습니다.
- 기존 `venue`와 `year` 메타데이터를 기반으로 표시용 라벨을 생성하며, 원본 venue 정보는 카드 meta 줄에 계속 표시합니다.

### 수정/생성한 파일
- `assets/app.js`: `formatPublicationLabel()`을 추가하고, 카드 상단 첫 badge가 연도만이 아니라 축약 venue + 연도를 표시하도록 변경했습니다.
- `assets/style.css`: publication label 전용 스타일과 다크 모드 대비 스타일을 추가했습니다.
- `index.html`: CSS/JS cache-busting version을 갱신했습니다.
- `AGENT_LOG.md`: 이번 UI 표시 변경 내용을 기록했습니다.

### 구현한 기능
- arXiv 계열 venue는 `arXiv 2024`처럼 표시합니다.
- ICLR, ICML, NeurIPS, CVPR, ICRA, IROS 같은 주요 conference venue가 데이터에 들어오면 축약명 + 연도로 표시합니다.
- Nature Communications, Additive Manufacturing 등 기존 주요 저널도 `Nat. Commun. 2025`, `Addit. Manuf. 2026`처럼 compact하게 표시합니다.
- venue 문자열이 정확히 일치하지 않아도 `arxiv`, `learning representations`, `neurips` 등 주요 패턴을 부분 매칭해 축약합니다.

### 설계 결정
- `data/papers.json` schema를 바꾸지 않고 프론트엔드에서 표시용 라벨을 계산했습니다. 기존 자동 수집 파이프라인과 중복 제거 로직에 영향을 주지 않기 위해서입니다.
- 원문 venue 문자열은 보존하고, 카드 상단에만 읽기 쉬운 축약 라벨을 추가했습니다.

### 남은 작업
- 필요하면 venue 축약 사전에 `SIGGRAPH`, `CHI`, `RSS`, `CoRL`, `T-RO`, `RA-L` 등을 추가할 수 있습니다.
- 학회명 normalization을 Python 수집 단계에서도 저장 필드로 만들지 여부는 추후 결정할 수 있습니다.

### 주의사항
- 이번 변경은 공개 메타데이터의 표시 방식만 바꾸며, 출판사 초록/PDF 저장 정책에는 영향을 주지 않습니다.
- API key, secret, token은 기록하지 않았습니다.

## 2026-06-12 17:56

### 변경 요약
- GitHub Actions 수집은 성공했지만 GitHub Pages 공개 사이트가 이전 `site_meta.json`을 계속 보여주는 현상을 확인했습니다.
- 원격 `main`에는 `34ff160 Update paper metadata` 커밋이 생성되어 `data/site_meta.json`이 `2026-06-12T06:29:37Z`로 갱신되었고, 논문 수가 145편에서 156편으로 증가했음을 확인했습니다.
- Pages URL은 여전히 `2026-06-12T04:59:53Z` 데이터를 서빙하고 있어, 데이터 수집과 Pages 배포 사이의 연결을 보강했습니다.

### 수정/생성한 파일
- `.github/workflows/update-papers.yml`: 데이터 업데이트/커밋 후 GitHub Pages artifact를 업로드하고 직접 배포하는 단계를 추가했습니다.
- `AGENT_LOG.md`: 이번 원인 분석과 workflow 보강 내용을 기록했습니다.
- `ARCHITECTURE.md`: 업데이트 workflow와 Pages 반영 구조의 최신 동작을 문서화했습니다.
- `PROJECT_STATUS.md`: 현재 데이터 상태와 Pages 반영 지연 이슈/개선 사항을 기록했습니다.

### 구현한 기능
- 매시간 업데이트 workflow가 끝난 뒤 `actions/configure-pages`, `actions/upload-pages-artifact`, `actions/deploy-pages`로 GitHub Pages를 직접 배포합니다.
- 데이터 커밋을 만든 `GITHUB_TOKEN` push가 별도 deploy workflow를 트리거하지 않아도, 같은 workflow 안에서 공개 사이트가 최신 데이터로 배포됩니다.

### 설계 결정
- GitHub Actions의 `GITHUB_TOKEN`이 만든 커밋이 별도 push workflow를 항상 트리거하지 않을 수 있으므로, update workflow 내부에서 Pages 배포까지 직접 수행하도록 했습니다.
- 기존 `.github/workflows/deploy-pages.yml`은 일반 push와 수동 배포용으로 유지하고, 정기 수집 후 배포는 `update-papers.yml`에서 처리합니다.
- 새 논문이 없어도 `site_meta.json`은 실행 시각을 갱신하므로, Pages도 매 실행 후 최신 실행 시각을 반영해야 합니다.

### 남은 작업
- 다음 scheduled run 또는 수동 `workflow_dispatch` 실행 후 Pages URL의 `data/site_meta.json`이 최신 시간으로 바뀌는지 확인해야 합니다.
- GitHub Pages 설정이 Actions 배포 방식인지 branch 배포 방식인지 저장소 Settings에서 최종 확인하면 좋습니다.

### 주의사항
- API key, secret, token은 로그에 기록하지 않았습니다.
- GitHub Pages 반영은 GitHub 내부 캐시와 배포 지연 때문에 수집 커밋보다 몇 분 늦을 수 있습니다.
- 현재 공개 Pages 데이터가 늦게 보이는 것은 비용 문제가 아니라 배포/캐시 반영 문제입니다.

## 2026-06-12 15:15

### 변경 요약
- 사이트 제목과 대표 설명을 현재 범위에 맞게 변경했습니다.
- 기존 MMAM/FGAM 중심 제목에서 생산·제조, 3D/4D 프린팅, 로봇틱스, AI 제조를 포괄하는 연구 트래커 제목으로 재정의했습니다.
- 언어 전환 시 표시되는 한글/영문 부제와 README 대표 문구도 함께 정리했습니다.

### 수정/생성한 파일
- `index.html`: 문서 title, meta description, eyebrow, H1, subtitle, CSS/JS cache busting version을 갱신했습니다.
- `assets/app.js`: 한글/영문 subtitle UI 텍스트를 새 프로젝트 범위에 맞게 수정했습니다.
- `README.md`: 프로젝트 대표 제목과 첫 설명 문장을 수정했습니다.
- `AGENT_LOG.md`: 이번 제목/포지셔닝 변경 이력을 추가했습니다.

### 구현한 기능
- 사이트 첫 화면과 브라우저 탭 제목이 `Awesome AI Manufacturing and 3D/4D Printing Research`로 표시되도록 변경했습니다.
- 한글 모드에서는 생산·제조, 3D/4D 프린팅, 로봇틱스, AI 제조 분야를 위한 큐레이션 저장소라는 설명이 표시됩니다.
- 영어 모드에서는 manufacturing, 3D/4D printing, robotics, AI-driven production을 포괄하는 research tracker 설명이 표시됩니다.

### 설계 결정
- `Awesome` 스타일의 큐레이션 정체성은 유지하되, 특정 소재/공정 중심 제목보다 넓은 제조 연구 트래커로 읽히도록 제목을 확장했습니다.
- 기존 데이터 수집 정책, API 사용 방식, 저작권 정책은 변경하지 않았습니다.
- CSS/JS query version을 올려 GitHub Pages 캐시가 오래된 문구를 계속 보여줄 가능성을 줄였습니다.

### 남은 작업
- 실제 GitHub Pages 반영은 push 후 Pages 배포/캐시 갱신 시간에 따라 몇 분 지연될 수 있습니다.
- 향후 필요하면 repository 이름 또는 GitHub Pages slug도 새 제목과 맞게 바꿀 수 있습니다.

### 주의사항
- API key, secret, token은 기록하지 않았습니다.
- 이번 변경은 UI/문서의 제목과 설명만 바꾼 것이며, 논문 수집 범위나 비용 구조에는 영향을 주지 않습니다.

## 2026-06-12 10:19

### 변경 요약
- GitHub Pages용 정적 Awesome-style 논문 큐레이션 사이트의 초기 구현을 생성했습니다.
- OpenAlex, Crossref, 선택적 Semantic Scholar, 선택적 OpenAI 요약 생성을 포함한 Python 업데이트 파이프라인을 추가했습니다.
- 저작권 정책상 raw abstract와 PDF를 저장하지 않는 데이터 흐름을 코드와 문서에 명시했습니다.

### 수정/생성한 파일
- `index.html`: 헤더, 안내 문구, 통계, 검색/필터 UI, 논문 목록 영역을 가진 정적 페이지를 생성했습니다.
- `assets/style.css`: academic Awesome-list 스타일의 반응형 레이아웃과 카드/배지/버튼 스타일을 구현했습니다.
- `assets/app.js`: `data/papers.json` 로딩, 검색, 카테고리 필터, 연도 필터, 정렬, 통계, citation 복사 기능을 구현했습니다.
- `data/papers.json`: 초기 빈 논문 데이터 배열을 생성했습니다.
- `data/queries.json`: 기본 검색어 배열을 생성했습니다.
- `scripts/fetch_openalex.py`: OpenAlex Works API 조회와 메타데이터 정규화를 구현했습니다.
- `scripts/fetch_crossref.py`: Crossref Works API 조회와 메타데이터 정규화를 구현했습니다.
- `scripts/enrich_semantic_scholar.py`: `SEMANTIC_SCHOLAR_API_KEY`가 있을 때 DOI 기반 선택적 보강을 구현했습니다.
- `scripts/summarize.py`: OpenAI 기반 한글 요약 생성과 API key가 없을 때의 fallback 요약/태그/카테고리/관련성 점수 생성을 구현했습니다.
- `scripts/update_papers.py`: 검색어 순회, API 호출, 중복 제거, 새 논문 요약, transient abstract 제거, `papers.json` 저장을 orchestration합니다.
- `requirements.txt`: `requests`, `openai` 의존성을 추가했습니다.
- `.github/workflows/update-papers.yml`: 매시 실행, 수동 실행, 데이터 변경 시 자동 커밋 workflow를 추가했습니다.
- `README.md`: 프로젝트 목적, 데이터 출처, 저작권 정책, API key, 로컬 실행, Pages 배포, 수동 수정, 검색어 수정, 한계점을 한글로 문서화했습니다.
- `ARCHITECTURE.md`: 전체 구조, 프론트엔드, 데이터, Python 파이프라인, GitHub Actions, 환경변수, 저작권 정책을 설명했습니다.
- `PROJECT_STATUS.md`: 완료/부분 구현/미구현 기능, 알려진 문제, 다음 작업 순서를 정리했습니다.
- `AGENT_LOG.md`: 현재 작업 기록과 인수인계 정보를 생성했습니다.

### 구현한 기능
- GitHub Pages에서 동작하는 빌드 없는 정적 웹사이트
- 논문 카드에 제목, 저자, 연도, venue, DOI/source 링크, source API, 카테고리, 태그, 관련성 점수, 한글 AI 요약, 마지막 업데이트 표시
- 키워드 검색, 카테고리 필터, 연도 필터, 관련성/최신/제목 정렬
- 상단 통계: 전체 논문 수, 카테고리 수, 최신 업데이트 날짜, 이번 주 추가 논문 수
- OpenAlex와 Crossref 기반 최소 수집 파이프라인
- Semantic Scholar 선택적 보강
- OpenAI 선택적 한글 요약 생성
- OpenAI key가 없을 때 abstract 원문을 복사하지 않는 fallback 요약
- DOI 우선 중복 제거, DOI가 없으면 normalized title 중복 제거
- 새 논문이 없으면 GitHub Actions가 실패하지 않는 자동 업데이트

### 설계 결정
- 출판사 웹사이트 크롤링 대신 OpenAlex/Crossref/Semantic Scholar 공식 API만 사용했습니다.
- PDF는 다운로드하지 않고 저장 필드 `pdf_stored`를 항상 `false`로 둡니다.
- API abstract는 `_abstract` transient 필드로만 전달하고 저장 직전 제거합니다. raw abstract를 표시하지 않는 이유는 출판사 초록 문장의 재게시 위험을 줄이고, 사이트가 AI가 새로 작성한 한글 요약만 제공하도록 하기 위해서입니다.
- `OPENAI_API_KEY`가 없어도 자동 업데이트가 멈추지 않도록 fallback 요약을 만들었습니다. 이 fallback은 제목과 메타데이터 기반으로 작성되어 초록 문장을 복사하지 않습니다.
- 새 논문이 없는 실행도 정상 상태이므로 workflow가 실패하지 않게 했습니다. 정기 실행에서 변경 없음은 오류가 아니라 기대 가능한 상태입니다.
- 클라이언트 코드는 `papers.json`만 읽고 모든 API key는 GitHub Actions 환경변수로만 사용합니다.

### 남은 작업
- 실제 API 실행으로 `data/papers.json`을 채우고 결과 품질을 검수해야 합니다.
- 관련 없는 논문이 많이 들어오면 `_is_plausible` 필터와 검색어를 조정해야 합니다.
- Source 열기 버튼은 현재 DOI URL을 사용하므로 API별 source landing URL을 별도 필드로 확장할 수 있습니다.
- 브라우저에서 GitHub Pages 배포 화면과 모바일 반응형을 확인하면 좋습니다.

### 주의사항
- API key, secret, token 값은 문서나 로그에 기록하지 마세요.
- `data/papers.json`에 raw abstract 또는 PDF 경로를 추가하지 마세요.
- 자동 커밋은 `data/papers.json` 변경 시에만 수행됩니다.
- OpenAI 요약은 새 논문에 대해서만 생성됩니다. 기존 논문의 요약을 재생성하려면 해당 항목을 수동으로 제거하거나 별도 재요약 스크립트를 추가해야 합니다.

## 2026-06-12 10:20

### 변경 요약
- 로컬 Windows PowerShell에서 실제 업데이트 스크립트를 실행하던 중 유니코드 논문 제목 출력이 CP949 인코딩에서 실패하는 문제를 발견하고 수정했습니다.

### 수정/생성한 파일
- `scripts/update_papers.py`: 실행 시작 시 `sys.stdout` 인코딩을 UTF-8로 재설정하도록 수정했습니다.
- `AGENT_LOG.md`: 검증 중 발견한 문제와 수정 내용을 기록했습니다.

### 구현한 기능
- 유니코드 하이픈, 특수기호, 비영문 논문 제목이 로그에 포함되어도 Windows 콘솔에서 업데이트가 중단되지 않도록 했습니다.

### 설계 결정
- 논문 제목을 손실 변환하지 않고 UTF-8 출력 환경을 우선 설정했습니다. GitHub Actions의 Ubuntu 환경에도 무해한 변경입니다.

### 남은 작업
- 업데이트 스크립트를 다시 실행해 실제 API 수집과 `data/papers.json` 저장까지 검증해야 합니다.

### 주의사항
- 이 변경은 출력 인코딩만 다루며, 저장 데이터의 UTF-8 정책은 그대로 유지됩니다.

## 2026-06-12 10:21

### 변경 요약
- 실제 OpenAlex/Crossref API를 사용해 업데이트 파이프라인을 실행했고 `data/papers.json`에 9편의 논문을 저장했습니다.
- 저장 데이터 정책과 로컬 정적 서버 응답을 검증했습니다.
- 현재 프로젝트 상태 문서를 실제 데이터 상태에 맞게 갱신했습니다.

### 수정/생성한 파일
- `data/papers.json`: API 검색 결과 9편을 사용자 요구 스키마에 맞춰 저장했습니다.
- `PROJECT_STATUS.md`: 현재 논문 수, 검증 결과, 알려진 큐레이션 품질 이슈, 다음 작업 순서를 갱신했습니다.
- `AGENT_LOG.md`: 실제 실행 및 검증 기록을 추가했습니다.

### 구현한 기능
- 로컬에서 `python scripts/update_papers.py` 실행 성공을 확인했습니다.
- `python -m py_compile`로 Python 스크립트 문법 검사를 통과했습니다.
- `data/papers.json`에 `_abstract` transient 필드가 남지 않는지 확인했습니다.
- 모든 저장 항목의 `raw_abstract_displayed=false`, `pdf_stored=false`를 확인했습니다.
- `python -m http.server 8000`으로 로컬 정적 서버를 띄우고 `index.html`, `data/papers.json` HTTP 200 응답을 확인했습니다.

### 설계 결정
- 초기 데이터가 완전히 비어 있으면 UI는 동작하지만 큐레이션 사이트로 바로 확인하기 어렵기 때문에, 공식 메타데이터 API를 한 번 실행해 seed 데이터를 생성했습니다.
- 일부 넓은 주제의 논문이 포함될 수 있음을 문서화하고, 다음 작업자가 검색어와 필터를 조정하도록 인수인계했습니다.

### 남은 작업
- 수집된 9편을 사람이 검수해 이 저장소의 핵심 범위와 맞지 않는 항목을 제거하거나 필터를 강화해야 합니다.
- 브라우저 자동화 도구가 현재 세션에 노출되지 않아 스크린샷 기반 검증은 수행하지 못했습니다. 로컬 서버와 HTTP 응답 검증은 완료했습니다.

### 주의사항
- 로컬 확인용 서버는 `http://localhost:8000`에서 실행 중이며 프로세스 ID는 `16360`입니다.
- 다음 에이전트가 같은 포트를 사용하려면 기존 서버 프로세스를 종료하거나 다른 포트를 선택하세요.

## 2026-06-12 10:22

### 변경 요약
- 업데이트 스크립트를 같은 데이터 상태에서 재실행해 새 논문이 없는 경우에도 성공 종료되는지 확인했습니다.

### 수정/생성한 파일
- `AGENT_LOG.md`: 새 논문 없음 경로 검증 결과를 추가했습니다.

### 구현한 기능
- `python scripts/update_papers.py` 재실행 결과 `Added 0 new papers`, `No changes in data/papers.json`로 정상 종료됨을 확인했습니다.

### 설계 결정
- 정기 실행에서 새 논문이 없는 상황은 오류가 아니므로, workflow가 실패하지 않는 현재 동작을 유지합니다.

### 남은 작업
- 실제 GitHub Actions 환경에서 secrets 설정 후 수동 실행으로 동일 동작을 확인하면 됩니다.

### 주의사항
- 새 논문이 없을 때 자동 커밋 단계는 `git diff --quiet -- data/papers.json` 조건으로 건너뜁니다.

## 2026-06-12 10:23

### 변경 요약
- 원격 GitHub 저장소 `lko9911/GPT_Paper_research`에 초기 사이트 구현을 커밋하고 push했습니다.
- GitHub Pages 배포를 자동화하기 위한 별도 workflow와 Python 캐시 제외 규칙을 추가했습니다.

### 수정/생성한 파일
- `.gitignore`: Python 캐시, 가상환경, `.env` 파일이 커밋되지 않도록 추가했습니다.
- `.github/workflows/deploy-pages.yml`: `main` 브랜치 push 또는 수동 실행 시 정적 사이트를 GitHub Pages로 배포하는 workflow를 추가했습니다.
- `AGENT_LOG.md`: 원격 push와 배포 workflow 추가 내용을 기록했습니다.

### 구현한 기능
- GitHub Actions 기반 Pages 배포 경로를 추가했습니다.
- 캐시 파일이 이후 커밋에 포함되지 않도록 방지했습니다.

### 설계 결정
- GitHub 저장소 Settings에서 branch 배포를 수동 설정하지 않아도 동작할 가능성이 높은 `actions/configure-pages`, `actions/upload-pages-artifact`, `actions/deploy-pages` 조합을 사용했습니다.

### 남은 작업
- GitHub 저장소의 Pages 설정이 GitHub Actions 배포를 허용하는지 확인해야 합니다.
- 이미 올라간 `scripts/__pycache__` 파일은 다음 커밋에서 제거해야 합니다.

### 주의사항
- GitHub Pages URL은 배포 workflow가 성공한 뒤 `https://lko9911.github.io/GPT_Paper_research/` 형태로 접근할 수 있습니다.

## 2026-06-12 10:24

### 변경 요약
- `BunnySoCrazy/Awesome-3D-Generation`의 큰 방향인 topic navigation, 카테고리별 compact list, pill형 링크/태그 구조를 참고해 UI를 재설계했습니다.
- 원본 사이트의 시각 요소나 데이터 구조를 복제하지 않고, MMAM/FGAM 논문 트래커에 맞는 독립적인 정보 구조로 바꿨습니다.

### 수정/생성한 파일
- `index.html`: 상단 topic navigation과 태그 필터 select를 추가하고, 깨져 보이던 한글 문자열을 UTF-8 기준으로 다시 정리했습니다.
- `assets/app.js`: featured topic 필터, 태그 필터, 카테고리별 그룹 렌더링, 태그 클릭 필터링, compact paper row 렌더링을 구현했습니다.
- `assets/style.css`: 카드형 UI를 카테고리 섹션 + 논문 row + 우측 score/link rail 구조로 재설계했습니다.
- `AGENT_LOG.md`: UI 참고 방향과 변경 사항을 기록했습니다.

### 구현한 기능
- 상단 topic pill 클릭으로 MMAM, FGAM, DM filament, 계산설계 등 주요 태그를 빠르게 필터링합니다.
- 카테고리별로 논문 목록이 묶여 Awesome-list처럼 훑어보기 쉬워졌습니다.
- 각 논문은 제목, 메타데이터, 요약, 관련성 설명, category/tag, score, year, Paper/DOI/Copy Cite 링크를 compact하게 표시합니다.
- 태그 badge를 클릭하면 해당 태그로 필터링됩니다.

### 설계 결정
- 참고 레포처럼 topic-first 탐색과 compact listing 감각은 가져오되, visual preview table은 사용하지 않았습니다. 이 프로젝트는 PDF/이미지 미리보기를 저장하지 않는 정책이 있으므로 텍스트 기반 큐레이션이 더 적합합니다.
- Paper 링크는 DOI URL로 연결하여 원문 접근을 공식 DOI/source로 유도합니다.

### 남은 작업
- GitHub Pages 배포 후 실제 공개 URL에서 UI 렌더링을 확인해야 합니다.
- 브라우저 기반 시각 검증 도구가 없으면 HTTP 응답과 정적 파일 검증으로 대체합니다.

### 주의사항
- 참고 사이트를 그대로 복사하지 말라는 요구에 맞춰 색상, 레이아웃, 데이터 표현, 텍스트를 독립적으로 구성했습니다.

## 2026-06-12 10:25

### 변경 요약
- 사용자의 요청에 따라 주제별 행, 게재지별 열로 논문 분포를 볼 수 있는 매트릭스 UI를 추가했습니다.
- 게재지 필터를 추가하고, 매트릭스 셀 클릭으로 해당 주제와 게재지 조합을 바로 필터링할 수 있게 했습니다.

### 수정/생성한 파일
- `index.html`: 게재지 필터 select와 `Topic x Venue` 매트릭스 섹션을 추가했습니다.
- `assets/app.js`: venue 수집, 상위 venue column 생성, 주제 x 게재지 matrix 렌더링, matrix cell 클릭 필터, matrix filter 해제 기능을 구현했습니다.
- `assets/style.css`: matrix table, count cell, active cell, responsive horizontal scroll 스타일을 추가했습니다.
- `AGENT_LOG.md`: 이번 매트릭스 기능 구현 내용을 기록했습니다.

### 구현한 기능
- 행은 카테고리/주제, 열은 게재지로 구성된 논문 수 분포표를 표시합니다.
- 셀의 숫자를 클릭하면 해당 주제와 게재지 조합에 맞는 논문만 아래 목록에 표시됩니다.
- `매트릭스 필터 해제` 버튼으로 matrix 기반 필터를 초기화할 수 있습니다.
- 게재지별 select 필터를 검색 UI에 추가했습니다.
- 게재지가 많아질 경우 상위 8개 게재지를 열로 보여주고 나머지는 `Other venues`로 묶도록 설계했습니다.

### 설계 결정
- 현재 데이터는 9편이고 게재지가 모두 1편씩이지만, 앞으로 자동 수집으로 열이 늘어날 수 있어 기본 상한을 8개로 설정했습니다.
- 매트릭스는 전체 데이터 분포를 보여주고, 검색/태그/연도 필터와 조합되어 아래 목록을 좁히는 탐색 도구로 사용됩니다.

### 남은 작업
- 실제 배포 후 공개 URL에서 matrix UI가 표시되는지 확인해야 합니다.
- 논문 수가 많아지면 venue alias 정규화 규칙을 추가해 같은 학회/저널의 표기 차이를 합칠 수 있습니다.

### 주의사항
- venue 값은 OpenAlex/Crossref 메타데이터 품질에 의존합니다. 비어 있으면 `Venue unknown`으로 표시됩니다.

## 2026-06-12 10:26

### 변경 요약
- 사용자가 지적한 2030년 논문 항목을 조사했고, 출판연도가 아니라 원문 저장소의 embargo 종료일이 메타데이터에 섞인 값으로 판단해 수정했습니다.
- 미래 연도 같은 비정상 publication year가 다시 저장되지 않도록 방어 로직을 추가했습니다.

### 수정/생성한 파일
- `data/papers.json`: DOI `10.7273/000007857` 항목의 year를 2030에서 2025로, venue를 `Open MIND`에서 `Washington State University Dissertation`으로 보정했습니다. 요약과 관련성 설명에서도 2030 표현을 제거했습니다.
- `scripts/update_papers.py`: 저장 전 publication year가 1900 미만이거나 현재 연도보다 1년을 초과하면 비정상 값으로 보고 `None` 처리하는 `_safe_year` 함수를 추가했습니다.
- `AGENT_LOG.md`: 데이터 품질 이슈와 수정 내용을 기록했습니다.

### 구현한 기능
- 잘못된 미래 연도 메타데이터가 사이트에 표시되지 않도록 했습니다.
- 수동 검수로 확인된 학위논문 메타데이터를 보정했습니다.

### 설계 결정
- 학술 메타데이터 API가 embargo date, online ahead date, deposit date 등을 publication year처럼 잘못 전달할 수 있으므로, 현재 연도보다 1년 이상 미래인 값은 표시하지 않는 보수적 정책을 적용했습니다.
- 사용자가 이미 본 잘못된 항목은 실제 출처 확인 후 2025년 학위논문으로 수동 보정했습니다.

### 남은 작업
- 향후 데이터 품질을 더 높이려면 DOI별 Crossref/OpenAlex/Semantic Scholar 값을 비교해 연도 충돌 시 더 신뢰도 높은 값을 선택하는 로직을 추가할 수 있습니다.

### 주의사항
- 원문 저장소에 PDF 항목이 있더라도 이 프로젝트는 PDF를 다운로드하거나 저장하지 않습니다.

## 2026-06-12 10:27

### 변경 요약
- 사용자의 요청에 따라 자동 조사 범위를 2025년 이후로 고정하고, 논문을 가져오는 기준을 문서화했습니다.
- Science/Nature 계열 게재지도 공식 메타데이터 API에서 검색되고 주제 기준을 만족하면 포함될 수 있음을 명확히 했습니다.

### 수정/생성한 파일
- `scripts/update_papers.py`: `SINCE_YEAR` 환경변수와 기본값 `2025`를 추가하고, OpenAlex/Crossref 호출에 시작 연도 필터를 전달하도록 수정했습니다.
- `.github/workflows/update-papers.yml`: GitHub Actions 실행 환경에 `SINCE_YEAR: "2025"`를 명시했습니다.
- `README.md`: 조사 범위, 논문 수집 기준, Science/Nature 포함 가능 조건을 추가했습니다.
- `ARCHITECTURE.md`: 업데이트 파이프라인과 환경변수 설명에 `SINCE_YEAR`를 추가했습니다.
- `PROJECT_STATUS.md`: 2025년 이후 수집 기준과 Science/Nature 계열 처리 방침을 기록했습니다.
- `data/papers.json`: PowerShell 인코딩 영향으로 깨져 있던 수동 보정 요약 문장을 UTF-8 한글 문장으로 복구했습니다.
- `AGENT_LOG.md`: 이번 기준 변경과 검증 내용을 기록했습니다.

### 구현한 기능
- 기본적으로 2025년 이후 논문만 수집합니다.
- 2025년 이전 논문은 `_is_plausible` 단계에서 제외됩니다.
- 현재 연도보다 1년을 초과하는 미래 연도는 비정상 메타데이터로 버립니다.
- 공식 API에서 검색되는 모든 게재지를 대상으로 하며 Science, Nature 같은 특정 출판사를 배제하지 않습니다.

### 설계 결정
- 게재지 이름으로 포함 여부를 결정하지 않고, 연구 주제와 연도 기준으로 포함 여부를 판단합니다. 고급 저널만 따로 크롤링하면 저작권/접근 정책 리스크가 커지기 때문입니다.
- Science/Nature 논문도 DOI와 메타데이터 API를 통해 들어오는 경우만 포함합니다.

### 남은 작업
- 원한다면 `target_venues.json` 같은 파일을 추가해 Science, Nature, Nature Communications, Advanced Materials 등 관심 게재지를 우선 표시하거나 별도 필터로 강조할 수 있습니다.

### 주의사항
- 메타데이터 API에는 embargo date나 잘못된 미래 연도 값이 섞일 수 있어 방어 로직이 필요합니다.

## 2026-06-12 10:28

### 변경 요약
- Nature, Science, Additive Manufacturing 계열 게재지를 우선 추적 대상으로 추가했습니다.
- 프론트엔드 JS의 한글 UI 문자열을 UTF-8 기준으로 다시 정리했습니다.

### 수정/생성한 파일
- `index.html`: 상단에 우선 추적 게재지 navigation을 추가했습니다.
- `assets/app.js`: `TARGET_VENUES` 목록, target venue chip, target venue 필터링, 우선 게재지 count 표시, 축약 venue 이름 표시를 구현했습니다.
- `assets/style.css`: 우선 게재지 pill 스타일을 추가했습니다.
- `data/queries.json`: Additive Manufacturing, Nature, Science 조합 검색어를 추가했습니다.
- `README.md`: 우선 추적 게재지 목록을 문서화했습니다.
- `PROJECT_STATUS.md`: 우선 추적 게재지 상태와 다음 개선 작업을 기록했습니다.
- `AGENT_LOG.md`: 이번 변경 내용을 기록했습니다.

### 구현한 기능
- Nature, Nature Communications, Nature Materials, Nature Reviews Materials, Science, Science Advances, Science Robotics, Additive Manufacturing을 별도 칩으로 보여줍니다.
- 각 칩에는 현재 수집된 논문 수가 표시됩니다.
- 칩을 클릭하면 해당 게재지 논문만 필터링됩니다.
- 게재지 select에도 우선 추적 게재지가 포함됩니다.

### 설계 결정
- 특정 출판사 사이트를 직접 크롤링하지 않고 공식 메타데이터 API에서 검색되는 항목만 포함합니다.
- 지금 단계에서는 source ID 고정 검색보다 검색어 보강과 UI 강조를 먼저 적용했습니다. OpenAlex source ID 기반 검색은 다음 단계에서 더 정확하게 추가할 수 있습니다.

### 남은 작업
- Nature/Science/Additive Manufacturing 논문을 더 정확히 모으려면 OpenAlex Sources API로 source ID를 고정한 venue-specific 검색을 추가하세요.

### 주의사항
- 현재 데이터에 해당 게재지 논문이 없으면 칩 count가 0으로 표시됩니다. 0은 배제가 아니라 아직 수집 결과가 없다는 뜻입니다.

## 2026-06-12 10:29

### 변경 요약
- 사용자가 지정한 `BunnySoCrazy/Awesome-3D-Generation`의 실제 `index.html` UI 방향을 참고해, 현재 사이트를 gallery-style awesome list에 더 가깝게 재구성했습니다.
- 그대로 복제하지 않고, 이 프로젝트의 저작권 정책에 맞게 이미지 미리보기 대신 자동 생성 preview tile을 사용했습니다.

### 수정/생성한 파일
- `index.html`: 중앙 정렬 헤더 폭을 넓히고, 본문을 sticky sidebar + content 레이아웃으로 변경했습니다. `side-topic-nav`, `side-venue-nav` 빠른 탐색 영역을 추가했습니다.
- `assets/app.js`: sidebar navigation 생성, 카테고리별 anchor id 생성, paper row 렌더링을 gallery card 렌더링으로 변경, preview tile initials 생성 기능을 추가했습니다.
- `assets/style.css`: 참고 UI의 핵심 감각인 넓은 페이지, sticky sidebar, section title left accent, auto-fill card grid, hover lift/scale, preview area, card content/link layout을 우리 디자인으로 재작성했습니다.
- `AGENT_LOG.md`: UI 재구성 의도와 변경 내용을 기록했습니다.

### 구현한 기능
- 왼쪽 sidebar에서 카테고리 섹션으로 빠르게 이동할 수 있습니다.
- 왼쪽 sidebar에서 Nature/Science/Additive Manufacturing 등 우선 게재지 필터를 바로 적용할 수 있습니다.
- 논문 목록은 카테고리별 grid card로 표시됩니다.
- 각 카드 상단에는 PDF/이미지 대신 카테고리 약어, 연도, 관련성 점수를 보여주는 preview tile이 표시됩니다.
- 카드 hover 시 살짝 떠오르는 gallery interaction을 적용했습니다.

### 설계 결정
- 참고 사이트의 실제 preview image 카드는 그대로 가져오지 않았습니다. 이 프로젝트는 PDF, 출판사 이미지, 원문 초록을 호스팅하지 않는 정책이 있으므로, 이미지 대신 메타데이터 기반 preview tile을 생성하는 방식이 더 안전합니다.
- 참고 UI의 구조적 특징인 header, sidebar, section, card grid, link pill만 우리 데이터 모델에 맞게 재해석했습니다.

### 남은 작업
- 브라우저 자동화 도구가 현재 세션에 노출되지 않아 스크린샷 기반 시각 검증은 수행하지 못했습니다. 배포 후 실제 브라우저에서 card grid와 sidebar 스크롤을 확인하면 좋습니다.

### 주의사항
- `assets/app.js`는 Node가 설치되어 있지 않아 `node --check`로 문법 검사를 수행할 수 없습니다. 정적 훅과 로컬 HTTP 응답 검증으로 대체했습니다.

## 2026-06-12 10:30

### 변경 요약
- 사용자가 논문이 표시되지 않는다고 알려주어 프론트엔드 렌더링 문제를 조사했습니다.
- JS 파일은 내려오고 데이터도 정상 제공되지만, optional chaining 같은 최신 JS 문법이 일부 브라우저/검증 환경에서 스크립트 실행을 막을 수 있음을 확인했습니다.

### 수정/생성한 파일
- `assets/app.js`: optional chaining `?.`, `Array.prototype.at`, `String.prototype.replaceAll`, `Array.prototype.flatMap` 사용을 제거하고 더 호환성 높은 문법으로 변경했습니다.
- `assets/style.css`: 필수 기능이 아닌 CSS `:has()` 선택자를 제거했습니다.
- `AGENT_LOG.md`: 표시 오류 원인과 수정 내용을 기록했습니다.

### 구현한 기능
- 구형 또는 제한된 브라우저 환경에서도 JS가 파싱되고 논문 렌더링이 실행될 가능성을 높였습니다.
- Python `esprima` 파서로 `assets/app.js` 문법 검사를 통과했습니다.
- 로컬 HTTP 서버에서 `index.html`과 `assets/app.js` 응답을 확인했습니다.

### 설계 결정
- 최신 문법의 간결함보다 GitHub Pages 방문자의 브라우저 호환성을 우선했습니다.
- 논문이 표시되지 않는 장애를 막기 위해 렌더링 경로의 optional chaining과 최신 prototype 메서드를 제거했습니다.

### 남은 작업
- 공개 Pages 배포 후 실제 URL에서 사용자가 논문 카드가 보이는지 확인해야 합니다.

### 주의사항
- Node가 설치되어 있지 않아 `node --check`는 계속 사용할 수 없습니다. 대신 `esprima` 기반 문법 검사를 사용했습니다.

## 2026-06-12 10:31

### 변경 요약
- 사용자가 sidebar `Venues`가 실제 기능을 하지 않는다고 지적해 UX를 수정했습니다.
- 우선 추적 게재지에 현재 논문이 0편이면 클릭 가능한 필터처럼 보이지 않도록 비활성화했습니다.
- sidebar `Venues`에는 실제 데이터에 존재하는 모든 게재지를 표시하고 클릭 시 필터링되도록 변경했습니다.

### 수정/생성한 파일
- `assets/app.js`: 실제 venue count 목록 생성, sidebar venue 필터링, All venues 버튼, 0개 우선 게재지 비활성화, venue priority 판별 함수를 추가했습니다.
- `assets/style.css`: 비활성 venue pill 스타일을 추가했습니다.
- `AGENT_LOG.md`: 이번 UX 수정 내용을 기록했습니다.

### 구현한 기능
- sidebar `Venues`에서 현재 수집된 게재지별 논문 수를 볼 수 있습니다.
- 실제 게재지를 클릭하면 해당 venue 논문만 표시됩니다.
- `All venues`를 클릭하면 venue 필터를 해제합니다.
- Nature/Science/Additive Manufacturing 등 우선 추적 게재지는 논문이 0편이면 disabled 상태로 표시됩니다.

### 설계 결정
- 0개 우선 게재지 칩을 숨기지 않고 비활성화했습니다. 사용자가 해당 게재지가 추적 대상임은 알 수 있고, 동시에 현재는 결과가 없다는 것도 알 수 있기 때문입니다.

### 남은 작업
- 공개 Pages 배포 후 sidebar venue 필터가 보이는지 확인해야 합니다.

### 주의사항
- 현재 데이터의 venue는 모두 1편씩이라 sidebar venue 필터는 각 게재지별로 1편씩 표시할 가능성이 큽니다.

## 2026-06-12 10:34

### 변경 요약
- 사용자가 Nature/Science/Additive Manufacturing에 논문이 없는 이유를 물어, 기존 파이프라인이 venue 이름을 검색어에 섞는 수준이었고 실제 저널 내부 검색을 하지 않았음을 확인했습니다.
- OpenAlex source ID 기반 우선 게재지 검색을 추가했습니다.
- 2024년 이후 기준으로 업데이트를 실행해 우선 게재지 논문 12편을 추가했습니다.

### 수정/생성한 파일
- `data/target_venues.json`: Nature, Nature Communications, Nature Materials, Nature Reviews Materials, Science, Science Advances, Science Robotics, Additive Manufacturing의 OpenAlex source ID를 저장했습니다.
- `scripts/fetch_openalex.py`: `source_id` 인자를 추가해 `primary_location.source.id` 필터로 특정 게재지 내부 검색을 지원하도록 수정했습니다.
- `scripts/update_papers.py`: 일반 검색 후 `data/target_venues.json`을 순회하며 우선 게재지 내부 검색을 수행하도록 확장했습니다.
- `data/papers.json`: 우선 게재지 검색 결과 12편을 추가해 총 22편이 되었습니다.
- `README.md`: 우선 게재지 목록이 source ID 기반으로 검색된다는 설명을 추가했습니다.
- `ARCHITECTURE.md`: target venue 검색 단계를 파이프라인 설명에 추가했습니다.
- `AGENT_LOG.md`: 이번 원인 분석과 구현 내용을 기록했습니다.

### 구현한 기능
- 우선 게재지별 OpenAlex source ID 검색
- Nature Communications, Science, Additive Manufacturing 등에서 공식 API 메타데이터 기반 논문 수집
- 기존 DOI/title 중복 제거와 저작권 정책 유지

### 설계 결정
- 저널 페이지를 직접 크롤링하지 않고 OpenAlex source ID를 사용했습니다. 이 방식은 공식 메타데이터 API만 사용하면서도 특정 게재지 안의 논문을 정확히 찾을 수 있습니다.
- venue별 검색은 API 호출 수를 과도하게 늘리지 않도록 기본 검색어 앞쪽 6개만 사용합니다.

### 남은 작업
- target venue별 검색어를 별도 파일로 세분화하면 Nature/Science 계열의 관련 없는 논문 유입을 더 줄일 수 있습니다.
- 새로 추가된 12편의 관련성을 사람이 검수하면 큐레이션 품질이 좋아집니다.

### 주의사항
- 현재 target venue count는 Additive Manufacturing 9편, Nature Communications 2편, Science 1편입니다.

## 2026-06-12 10:35

### 변경 요약
- 사용자가 `툴패스 계획`, `그래프 탐색 / 경로 계획 알고리즘`, `툴패스`, `경로계획`처럼 카테고리와 태그가 중복 노출되는 문제를 지적해 개선했습니다.

### 수정/생성한 파일
- `assets/app.js`: 표시용 태그에서 카테고리와 동일하거나 의미가 겹치는 태그를 숨기는 `visibleTags` 로직을 추가했습니다.
- `scripts/summarize.py`: 새로 생성되는 요약/태그에서도 카테고리와 중복되는 태그를 제거하도록 `_dedupe_tags` 로직을 추가했습니다.
- `data/papers.json`: 기존 22편의 태그를 중복 제거 규칙으로 정리했습니다.
- `AGENT_LOG.md`: 이번 태그 중복 개선 내용을 기록했습니다.

### 구현한 기능
- 카드에 카테고리와 같은 태그가 반복 표시되지 않습니다.
- `툴패스`는 `툴패스 계획` 카테고리가 있을 때 숨깁니다.
- `경로계획`은 `그래프 탐색 / 경로 계획 알고리즘` 카테고리가 있을 때 숨깁니다.
- `MMAM`, `FGAM`, `재료분포`, `퍼지 감소`, `AI/ML`도 각각 대응 카테고리와 중복되면 숨깁니다.

### 설계 결정
- 데이터 스키마의 `categories`와 `tags`는 유지하되, UI에서는 중복 태그를 숨기고 데이터 생성 단계에서는 새 중복을 줄이는 이중 방어를 적용했습니다.

### 남은 작업
- 향후 더 많은 논문이 들어오면 태그 alias 목록을 추가로 확장할 수 있습니다.

### 주의사항
- 중복 태그를 숨기더라도 검색 haystack에는 표시용 태그가 반영되므로, 카테고리/태그 필터 설계를 계속 관찰해야 합니다.

## 2026-06-12 10:36

### 변경 요약
- 사용자가 Nature Communications DOI `10.1038/s41467-024-47480-5` 논문이 검색되지 않는 문제를 제기했습니다.
- 원인은 OpenAlex venue 검색이 최신순 상위 일부만 가져와 2024 핵심 논문이 최신 2026 논문 뒤로 밀린 것이었습니다.
- 검색 순위에 의존하지 않도록 seed DOI 직접 조회 기능을 추가하고 해당 논문을 추가했습니다.

### 수정/생성한 파일
- `data/seed_dois.json`: 중요 논문 DOI 목록을 추가하고 `10.1038/s41467-024-47480-5`를 등록했습니다.
- `scripts/fetch_openalex.py`: DOI로 OpenAlex works endpoint를 직접 조회하는 `fetch_openalex_by_doi` 함수를 추가했습니다.
- `scripts/update_papers.py`: seed DOI를 먼저 조회하고 기존 중복 제거/요약/저장 파이프라인에 태우도록 수정했습니다.
- `data/papers.json`: `3D printing with a 3D printed digital material filament for programming functional gradients` 논문을 추가했습니다.
- `README.md`: 자동 검색에서 누락되는 중요 논문은 `data/seed_dois.json`에 DOI를 추가하는 방식으로 보완할 수 있음을 문서화했습니다.
- `ARCHITECTURE.md`: seed DOI 조회 단계를 파이프라인 설명에 추가했습니다.
- `AGENT_LOG.md`: 이번 누락 원인과 수정 내용을 기록했습니다.

### 구현한 기능
- DOI 기반 강제 포함 후보 조회
- 검색 순위에서 밀리는 핵심 논문 보완
- 기존 저작권 정책 유지: abstract 저장 없음, PDF 저장 없음

### 설계 결정
- 특정 Nature 페이지를 크롤링하지 않고 DOI를 통해 OpenAlex 공식 메타데이터를 조회했습니다.
- seed DOI는 사람이 중요 논문을 알고 있을 때 사용하는 보완 경로로 설계했습니다.

### 남은 작업
- 핵심 분야 논문을 추가로 알고 있다면 `data/seed_dois.json`에 DOI를 계속 추가하면 됩니다.

### 주의사항
- seed DOI도 `_is_plausible`의 주제/연도 필터를 통과해야 저장됩니다.

## 2026-06-12 10:37

### 변경 요약
- 사용자의 UI 요청에 따라 왼쪽 floating 패널은 분야 선택 전용으로 정리하고, 게재지는 본문에서 별도 보드로 볼 수 있게 변경했습니다.

### 수정/생성한 파일
- `index.html`: sidebar에서 Venues nav를 제거하고, 본문에 `게재지별 보기` 섹션과 `venue-board`를 추가했습니다.
- `assets/app.js`: sidebar 분야 선택 버튼, venue board 렌더링, venue card 클릭 필터링 로직을 추가했습니다.
- `assets/style.css`: venue section, venue board, venue card 스타일을 추가했습니다.
- `AGENT_LOG.md`: 이번 UI 구조 변경을 기록했습니다.

### 구현한 기능
- 왼쪽 floating 패널에서는 분야/카테고리만 선택합니다.
- 본문 `게재지별 보기` 섹션에서 실제 게재지별 논문 수를 볼 수 있습니다.
- 게재지 카드를 클릭하면 아래 논문 목록이 해당 게재지로 필터링됩니다.
- `All venues` 카드로 게재지 필터를 초기화할 수 있습니다.

### 설계 결정
- 분야 선택과 게재지 선택을 분리해 탐색 목적을 명확히 했습니다.
- 게재지는 별도 보드로 제공해 Nature/Science/Additive Manufacturing 같은 우선 게재지와 실제 수집 게재지를 더 넓게 볼 수 있게 했습니다.

### 남은 작업
- 공개 Pages 배포 후 좌측 분야 패널과 게재지 보드가 의도대로 표시되는지 확인해야 합니다.

### 주의사항
- sidebar 분야 버튼은 category select와 동기화됩니다. 게재지 보드는 venue select 또는 priority venue 필터와 동기화됩니다.

## 2026-06-12 10:38

### 변경 요약
- 사용자가 “가져올 수 있는 것을 다 가져오되 100편을 넘으면 하지 말라”고 요청했습니다.
- 먼저 dry-run으로 확장 수집 후보를 확인했고, 총 50편으로 100편 이하임을 확인한 뒤 실제 수집을 수행했습니다.
- 기존 23편에서 27편을 추가해 총 50편이 되었습니다.

### 수정/생성한 파일
- `scripts/update_papers.py`: 일반 검색 per-page와 target venue 검색 per-page를 50으로 확대하고, target venue 검색은 전체 검색어를 사용하도록 변경했습니다. `MAX_TOTAL_PAPERS` 기본값 100을 추가했습니다.
- `.github/workflows/update-papers.yml`: GitHub Actions 환경변수 `MAX_TOTAL_PAPERS: "100"`을 추가했습니다.
- `data/papers.json`: 확장 수집 결과 27편을 추가했습니다.
- `README.md`: 자동 수집 총량 상한 100편 설명을 추가했습니다.
- `ARCHITECTURE.md`: `MAX_TOTAL_PAPERS` 환경변수 설명을 추가했습니다.
- `AGENT_LOG.md`: 이번 확장 수집 기록을 추가했습니다.

### 구현한 기능
- 확장 수집 기준에서 총량 100편 제한을 적용합니다.
- OpenAlex 일반 검색과 우선 게재지 검색을 더 넓게 가져옵니다.
- 2024년 이후, DOI/title 중복 제거, raw abstract/PDF 저장 금지 정책은 유지합니다.

### 설계 결정
- 100편 제한을 코드와 GitHub Actions 환경변수 양쪽에 명시했습니다.
- 너무 많은 논문을 무작정 가져오지 않도록 상한을 유지하면서, 현재 범위에서는 가능한 후보를 더 넓게 수집했습니다.

### 남은 작업
- 새로 추가된 27편 중 주제 적합성이 낮은 항목은 사람이 검수해 제거하거나 `_is_plausible` 필터를 더 엄격하게 조정할 수 있습니다.

### 주의사항
- 현재 데이터 분포는 총 50편, 2024년 6편, 2025년 22편, 2026년 22편입니다.

## 2026-06-12 10:39

### 변경 요약
- 사용자의 요청에 따라 `Topic x Venue / 주제별 게재지 분포` 매트릭스 섹션을 제거했습니다.

### 수정/생성한 파일
- `index.html`: matrix section HTML을 제거했습니다.
- `assets/app.js`: matrix 렌더링, matrix 필터 상태, matrix cell 클릭 필터링 관련 코드를 제거했습니다.
- `assets/style.css`: matrix table, matrix count, matrix section 스타일을 제거했습니다.
- `AGENT_LOG.md`: 이번 제거 작업을 기록했습니다.

### 구현한 기능
- 페이지에서 `Topic x Venue / 주제별 게재지 분포`가 더 이상 표시되지 않습니다.
- `게재지별 보기` 보드는 유지됩니다.

### 설계 결정
- 게재지 탐색은 별도 venue board로 충분히 제공되므로, 복잡한 matrix UI는 제거해 화면 밀도를 낮췄습니다.

### 남은 작업
- 공개 Pages 배포 후 matrix 섹션이 사라졌는지 확인해야 합니다.

### 주의사항
- matrix 기반 필터 기능도 함께 제거되었습니다. 분야 필터는 왼쪽 패널, 게재지 필터는 venue board와 select로 수행합니다.

## 2026-06-12 10:40

### 변경 요약
- 사용자의 요청에 따라 UI의 큰 분야 체계를 `생산/제조`, `3D 프린팅`, `로봇틱스(생산제조)`, `AI 생산제조` 네 축으로 재구성했습니다.

### 수정/생성한 파일
- `index.html`: 카테고리 라벨을 분야 라벨로 변경하고, 결과 그룹 설명을 `Papers by Field`로 수정했습니다.
- `assets/app.js`: `FIELD_ORDER`와 `deriveField` 함수를 추가해 논문을 네 큰 분야로 자동 분류하도록 변경했습니다. 왼쪽 분야 선택 패널, 분야 필터, 논문 그룹 제목이 큰 분야 기준으로 동작합니다.
- `AGENT_LOG.md`: 이번 분야 체계 변경 내용을 기록했습니다.

### 구현한 기능
- 왼쪽 floating 패널은 네 큰 분야 기준으로 논문 수를 보여줍니다.
- 분야 필터도 네 큰 분야 기준으로 동작합니다.
- 논문 목록 그룹도 네 큰 분야 기준으로 묶입니다.
- 기존 세부 카테고리와 태그는 카드 내부 보조 badge로 유지됩니다.

### 설계 결정
- 기존 세부 카테고리 데이터를 삭제하지 않고 UI에서만 큰 분야를 파생했습니다. 자동 요약/분류 데이터는 그대로 보존하면서 탐색 UX만 단순화하기 위해서입니다.
- 큰 분야 분류는 제목, venue, tag, 기존 category를 이용한 휴리스틱으로 계산합니다. AI와 로봇틱스는 3D 프린팅보다 우선 분류합니다.

### 남은 작업
- 사람이 보기에 어색하게 분류된 논문이 있으면 `deriveField` 규칙을 더 조정할 수 있습니다.

### 주의사항
- 현재 로컬 계산 기준 분포는 3D 프린팅 25편, 생산/제조 16편, AI 생산제조 6편, 로봇틱스(생산제조) 3편입니다.

## 2026-06-12 10:32

### 변경 요약
- 사용자의 요청에 따라 논문 카드의 이미지/preview 영역을 제거했습니다.
- 연도와 관련성 점수는 카드 상단의 작은 텍스트 badge로 이동했습니다.

### 수정/생성한 파일
- `assets/app.js`: `preview-tile` 렌더링과 `previewInitials` 함수를 제거하고 `card-topline` badge를 추가했습니다.
- `assets/style.css`: preview tile 스타일을 제거하고 card topline badge 스타일을 추가했습니다.
- `AGENT_LOG.md`: 이번 UI 단순화 작업을 기록했습니다.

### 구현한 기능
- 논문 카드는 이제 이미지 없이 텍스트 중심으로 표시됩니다.
- 카드 상단에는 연도와 관련성 점수만 compact하게 표시됩니다.

### 설계 결정
- 이미지/preview 영역을 제거하면 참고 사이트와는 다소 달라지지만, 이 프로젝트의 저작권 정책과 논문 큐레이션 목적에는 더 적합합니다.

### 남은 작업
- 공개 Pages 배포 후 카드가 이미지 없이 정상 표시되는지 확인해야 합니다.

### 주의사항
- 향후 이미지가 필요하더라도 출판사 figure, PDF thumbnail, abstract image를 저장하지 않는 정책은 유지해야 합니다.

## 2026-06-12 10:33

### 변경 요약
- 사용자의 요청에 따라 자동 조사 시작 연도를 2024년으로 변경했습니다.
- 프론트엔드 기본 정렬을 관련성 점수순에서 최신순으로 변경했습니다.
- 2024년 이후 기준으로 업데이트 스크립트를 실행해 새 논문 1편을 추가했습니다.

### 수정/생성한 파일
- `scripts/update_papers.py`: 기본 `SINCE_YEAR`를 2025에서 2024로 변경했습니다.
- `.github/workflows/update-papers.yml`: GitHub Actions 환경변수 `SINCE_YEAR`를 `2024`로 변경했습니다.
- `index.html`: 정렬 select의 기본 옵션을 `최신순`으로 변경했습니다.
- `README.md`: 조사 범위 설명을 2024년 이후로 수정했습니다.
- `ARCHITECTURE.md`: 파이프라인 시작 연도와 환경변수 설명을 2024로 수정했습니다.
- `PROJECT_STATUS.md`: 완료 기능의 조사 범위를 2024년 이후로 수정했습니다.
- `data/papers.json`: 2024년 이후 기준 재수집으로 새 논문 1편을 추가했습니다.
- `AGENT_LOG.md`: 이번 조사 범위 변경과 검증 내용을 기록했습니다.

### 구현한 기능
- 자동 수집은 이제 2024년 이후 논문을 대상으로 합니다.
- 웹사이트의 기본 정렬은 최신순입니다.
- 로컬에서 `SINCE_YEAR=2024 python scripts/update_papers.py` 실행을 완료했습니다.

### 설계 결정
- 시작 연도는 코드 기본값과 GitHub Actions 환경변수를 둘 다 변경했습니다. 로컬 실행과 CI 실행이 서로 다른 범위를 쓰지 않도록 하기 위해서입니다.

### 남은 작업
- 2024년 논문이 실제로 들어오는지 다음 정기 업데이트 결과를 관찰해야 합니다. 현재 데이터에는 2025년과 2026년 항목만 있습니다.

### 주의사항
- 2024년 이후 범위이므로 2024, 2025, 2026 항목이 모두 포함될 수 있습니다.
## 2026-06-12 13:00

### 변경 요약
- 사용자 요청에 따라 왼쪽 패널을 큰 분야와 서브 토픽 구조로 개편했습니다.
- 논문 총량 100편 제한을 제거하고, OpenAlex/Crossref 공식 API 페이징으로 수집 범위를 확장했습니다.
- 실제 네트워크 수집을 실행해 `data/papers.json`을 50편에서 145편으로 늘렸습니다.
- UI 한글 문자열 일부가 깨져 있던 문제를 `index.html`과 `assets/app.js`에서 복구했습니다.
- API rate limit을 고려해 GitHub Actions의 1회 실행 페이지 예산과 sleep 값을 명시했습니다.

### 수정/생성한 파일
- `index.html`: 깨진 한글 문구를 복구하고 왼쪽 패널 제목을 `분야 및 서브 토픽`으로 변경했습니다.
- `assets/app.js`: `생산/제조`, `3D 프린팅`, `로봇틱스(생산제조)`, `AI 생산제조` 분야 분류와 서브 토픽 필터를 구현했습니다.
- `assets/style.css`: 분야/서브 토픽 사이드바와 서브 토픽 badge 스타일을 추가했습니다.
- `scripts/fetch_openalex.py`: OpenAlex cursor pagination과 DOI `/pdf` suffix 정리를 추가했습니다.
- `scripts/fetch_crossref.py`: Crossref cursor pagination과 DOI suffix 정리를 추가했습니다.
- `scripts/update_papers.py`: 논문 총량 제한 제거 상태를 유지하고 페이지당 수집량을 200으로 확장했습니다.
- `.github/workflows/update-papers.yml`: `API_SLEEP_SECONDS`, `OPENALEX_MAX_PAGES`, `CROSSREF_MAX_PAGES`를 추가해 Actions timeout/rate limit 위험을 낮췄습니다.
- `data/papers.json`: 공식 메타데이터 API로 수집한 논문을 145편까지 확장하고, `/pdf`가 붙은 DOI 중복 1건을 정리했습니다.
- `README.md`: 최신 수집 정책 업데이트를 문서화했습니다.
- `ARCHITECTURE.md`: API 페이징과 실행 예산 정책을 문서화했습니다.
- `PROJECT_STATUS.md`: 현재 총 논문 수, 완료 기능, 알려진 rate limit 이슈를 기록했습니다.
- `AGENT_LOG.md`: 이번 작업 기록을 추가했습니다.

### 구현한 기능
- 왼쪽 사이드바에서 큰 분야를 선택하면 해당 분야 논문만 표시됩니다.
- 큰 분야 아래 서브 토픽을 선택하면 분야와 서브 토픽 조건이 함께 적용됩니다.
- 태그 필터에서도 서브 토픽을 선택할 수 있습니다.
- 논문 카드에는 기존 카테고리/태그와 함께 계산된 서브 토픽 badge가 표시됩니다.
- OpenAlex/Crossref 검색은 한 페이지만 가져오지 않고 공식 API pagination을 사용할 수 있습니다.

### 설계 결정
- `data/papers.json`의 전체 논문 수에는 상한을 두지 않았습니다.
- 다만 GitHub Actions는 1시간마다 실행되고 timeout/rate limit이 있으므로 실행 1회당 page budget을 둡니다. 이는 전체 수집량 제한이 아니라 운영 안정성을 위한 장치입니다.
- 출판사 사이트를 직접 크롤링하지 않고, PDF도 저장하지 않으며, raw abstract는 저장/표시하지 않는 기존 정책을 유지했습니다.
- 큰 분야는 기존 저장 카테고리를 삭제하지 않고 UI 계산값으로 도출합니다. 기존 세부 카테고리는 카드 badge로 보존합니다.
- DOI가 `/pdf`로 끝나는 경우 링크 품질을 위해 suffix를 제거합니다. PDF를 다운로드하거나 저장한 것은 아닙니다.

### 남은 작업
- 더 깊은 전체 수집을 원하면 `OPENALEX_MAX_PAGES`와 `CROSSREF_MAX_PAGES`를 높이고 `API_SLEEP_SECONDS`도 함께 늘려 수동 실행하세요.
- OpenAlex 429가 반복되면 target venue 검색을 여러 workflow job 또는 날짜 구간으로 나누는 개선이 필요합니다.
- 일부 느슨한 검색어는 주변 제조/3D 프린팅 논문까지 포함할 수 있으므로 relevance rule을 연구실 기준에 맞게 더 조정할 수 있습니다.

### 주의사항
- API key, secret, token은 로그나 클라이언트 코드에 기록하지 않았습니다.
- 이번 네트워크 수집 중 OpenAlex 429 rate limit이 일부 발생했지만 workflow가 실패하지 않도록 fetch 실패는 로그만 남기고 계속 진행하는 구조입니다.
- raw abstract가 표시되지 않는 이유는 출판사 초록 원문 재게시 위험을 피하기 위해서입니다.
- PDF를 저장하지 않는 이유는 저작권 파일 호스팅 위험을 피하고 DOI/source 링크를 통해 원문 확인을 유도하기 위해서입니다.
- 로컬 브라우저 자동화 도구는 이번 세션에서 노출되지 않아 HTTP 200 응답, JS 파서, Python py_compile, 데이터 정책 검증으로 대체했습니다.
## 2026-06-12 13:11

### 변경 요약
- 상단 통계의 `분야 수` 표시를 `서브토픽 수`로 변경했습니다.
- 표시 숫자도 큰 분야 4개가 아니라 현재 논문들에서 계산되는 고유 서브 토픽 개수를 세도록 변경했습니다.

### 수정/생성한 파일
- `index.html`: 통계 라벨을 `서브토픽 수`로 변경했습니다.
- `assets/app.js`: `updateStats()`에서 `deriveSubtopics()` 결과의 고유 개수를 계산하도록 변경했습니다.
- `AGENT_LOG.md`: 이번 변경 기록을 추가했습니다.

### 구현한 기능
- 상단 통계 카드가 실제 서브 토픽 규모를 보여줍니다.

### 설계 결정
- 기존 DOM id `stat-categories`는 HTML/JS 변경 범위를 줄이기 위해 유지했습니다. 사용자에게 보이는 라벨과 값은 서브토픽 기준입니다.

### 남은 작업
- 없음.

### 주의사항
- JS 문법 검증은 `esprima`로 통과했습니다.
## 2026-06-12 13:16

### 변경 요약
- 상단 통계가 `서브토픽 수`만 표시하던 방식을 `분야 / 서브토픽` 구조로 바로잡았습니다.
- 사용자가 의도한 4개 큰 분야 안의 여러 토픽 구조가 보이도록 숫자를 `분야 개수 / 서브토픽 개수` 형식으로 표시합니다.

### 수정/생성한 파일
- `index.html`: 통계 라벨을 `분야 / 서브토픽`으로 변경했습니다.
- `assets/app.js`: `updateStats()`에서 큰 분야 개수와 서브토픽 개수를 함께 계산해 표시하도록 변경했습니다.
- `AGENT_LOG.md`: 이번 정정 사항을 기록했습니다.

### 구현한 기능
- 상단 통계 카드가 예를 들어 `4 / 18`처럼 큰 분야와 하위 토픽 규모를 함께 보여줍니다.

### 설계 결정
- 왼쪽 패널의 계층 구조와 상단 통계의 표현을 맞추기 위해 단일 서브토픽 수보다 `분야 / 서브토픽` 조합 표현을 선택했습니다.

### 남은 작업
- 없음.

### 주의사항
- 기존 DOM id `stat-categories`는 변경하지 않았습니다. 기능상 의미는 이제 `분야 / 서브토픽`입니다.
## 2026-06-12 13:18

### 변경 요약
- 상단 우선 게재지 pill에서 수집 논문이 0편인 venue를 숨기도록 개선했습니다.
- `게재지별 보기` 섹션을 `게재지 필터`로 정리하고, 큰 카드 영역과 compact 기타 게재지 리스트로 나누었습니다.
- venue dropdown에서도 실제 수집된 게재지만 표시되도록 정리했습니다.

### 수정/생성한 파일
- `assets/app.js`: `buildVenueNav()`가 0편 venue를 건너뛰도록 수정하고, `renderVenueBoard()`를 주요 게재지와 기타 게재지 compact 리스트 구조로 변경했습니다.
- `assets/style.css`: venue pill count badge, 주요 venue card, 기타 venue chip/list 스타일을 추가했습니다.
- `index.html`: 섹션 제목과 설명 문구를 더 명확하게 수정했습니다.
- `AGENT_LOG.md`: 이번 UI 개선 기록을 추가했습니다.

### 구현한 기능
- 상단에는 `All venues`와 실제 논문이 있는 우선 게재지만 표시됩니다.
- 아래 게재지 필터는 `All venues`, 주요 게재지, 기타 게재지 상위 항목으로 나뉘어 덜 난잡하게 보입니다.
- 기타 게재지 chip도 클릭하면 기존 카드와 동일하게 논문 목록을 필터링합니다.

### 설계 결정
- 0편 venue를 보여주면 사용자가 “왜 없지?”라는 노이즈를 먼저 보게 되므로 기본 UI에서는 숨겼습니다.
- 전체 venue를 완전히 숨기지 않고, 실제 수집된 기타 게재지는 compact list로 남겨 탐색 가능성을 유지했습니다.

### 남은 작업
- 필요하면 기타 게재지 리스트에 `더 보기/접기` 인터랙션을 추가할 수 있습니다.

### 주의사항
- `Additive manufacturing`처럼 대소문자가 다른 venue명은 기존 normalize 기반 매칭으로 우선 게재지에 포함됩니다.
- JS 문법 검증과 로컬 HTTP 200 확인을 완료했습니다.
## 2026-06-12 13:21

### 변경 요약
- 상단 통계의 두 번째 카드가 다시 `서브토픽 수`만 표시하도록 수정했습니다.
- 게재지 영역에서 기타 게재지 긴 목록을 완전히 제거하고, 주요 게재지 카드만 남겼습니다.

### 수정/생성한 파일
- `index.html`: 통계 라벨을 `서브토픽 수`로 변경하고, venue 섹션 제목/설명을 `주요 게재지` 중심으로 수정했습니다.
- `assets/app.js`: venue board에서 기타 게재지 목록 생성 로직과 `venueChip()` 함수를 제거했습니다.
- `assets/style.css`: 기타 게재지 compact list/chip 스타일을 제거했습니다.
- `AGENT_LOG.md`: 이번 정정 사항을 기록했습니다.

### 구현한 기능
- 통계 숫자는 고유 서브토픽 개수만 보여줍니다.
- 게재지 보드에는 `All venues`와 실제 논문이 있는 주요 게재지 카드만 표시됩니다.
- 기타 전체 게재지는 별도 긴 리스트로 펼치지 않고, 상단 필터 드롭다운을 통해 선택하도록 정리했습니다.

### 설계 결정
- 사용자가 화면에서 긴 venue 목록을 읽어야 하는 부담을 줄이기 위해 기타 게재지 preview를 제거했습니다.
- 주요 게재지 탐색과 전체 venue 탐색을 분리했습니다. 빠른 탐색은 카드, 세부 탐색은 드롭다운이 담당합니다.

### 남은 작업
- 필요하면 venue 드롭다운에도 검색형 combobox를 붙일 수 있습니다.

### 주의사항
- JS 문법 검증을 통과했습니다.
- 한글 문구는 UTF-8 기준으로 정상 포함되어 있음을 확인했습니다.
## 2026-06-12 13:26

### 변경 요약
- 게재지 보드를 너무 줄였던 문제를 보완해 기준 기반 표시 방식으로 변경했습니다.
- 핵심 타깃 venue와 데이터에서 2편 이상 반복 등장한 관련 학술지를 함께 표시하도록 했습니다.
- preprint/repository/unknown 계열 venue는 보드에서는 제외하고, 전체 드롭다운에서만 선택 가능하게 유지했습니다.

### 수정/생성한 파일
- `index.html`: 게재지 표시 기준 설명을 추가했습니다.
- `assets/app.js`: `shouldShowDiscoveredVenue()`와 `isNonJournalVenue()`를 추가해 venue 보드 표시 기준을 구현했습니다.
- `assets/style.css`: venue 표시 기준 안내 문구 스타일을 추가했습니다.
- `AGENT_LOG.md`: 이번 기준 변경을 기록했습니다.

### 구현한 기능
- 보드에 `All venues`, 핵심 타깃 venue, 관련성이 높은 반복 등장 학술지가 표시됩니다.
- 현재 데이터 기준 보드에는 Additive Manufacturing, Nature Communications, Science와 Polymers, IJAMT, Machines, Rapid Prototyping Journal 등 관련 venue가 함께 표시됩니다.

### 설계 결정
- 기준은 `핵심 타깃 venue` 또는 `2편 이상 반복 등장 + 제조/소재/기계/로봇/프린팅 관련 venue명`으로 잡았습니다.
- `Venue unknown`, `arXiv`, `Research Square`, `ChemRxiv`, repository, dissertation, proceedings 계열은 학술지 보드 노이즈를 줄이기 위해 제외했습니다.
- 제외된 venue도 데이터에서 삭제하지 않고 드롭다운 필터로 접근 가능하게 유지했습니다.

### 남은 작업
- venue 품질 기준을 더 엄밀하게 하려면 ISSN 기반 source type 또는 OpenAlex source metadata를 저장하는 개선이 필요합니다.

### 주의사항
- JS 문법 검증을 통과했습니다.
- 현재 기준은 데이터 기반 휴리스틱이며, 학술지 등급 평가를 의미하지 않습니다.
## 2026-06-12 13:29

### 변경 요약
- 게재지 보드 기준을 사용자 요청에 맞춰 `2편 이상 개별 표시 + 그 외 묶음`으로 변경했습니다.
- 2편 미만이거나 학술지로 보기 어려운 출처는 개별 카드로 펼치지 않고 `그 외` 카드에 묶었습니다.

### 수정/생성한 파일
- `index.html`: 게재지 기준 설명을 `2편 이상 개별 표시, 나머지 그 외 묶음`으로 수정했습니다.
- `assets/app.js`: venue board 표시 기준을 count 기반으로 바꾸고 `그 외` 그룹 필터를 추가했습니다.
- `assets/style.css`: `그 외` venue 카드가 일반 카드와 구분되도록 muted/dashed 스타일을 추가했습니다.
- `AGENT_LOG.md`: 이번 변경 내용을 기록했습니다.

### 구현한 기능
- 2편 이상 수집된 학술지는 개별 카드로 표시됩니다.
- 나머지는 `그 외` 카드 하나로 묶이며, 카드에는 `2편 이하의 학술지` badge가 표시됩니다.
- `그 외` 카드를 누르면 해당 묶음에 포함된 논문만 필터링됩니다.
- 위쪽 venue quick pill도 2편 이상 기준으로 맞췄습니다.

### 설계 결정
- `Venue unknown`, `arXiv`, `Research Square`, repository 계열은 논문 수가 2편 이상이어도 학술지 카드로는 표시하지 않고 그 외로 묶습니다.
- 전체 venue 접근성은 드롭다운 필터에 남겨두었습니다.

### 남은 작업
- 더 엄밀한 학술지 판별이 필요하면 OpenAlex source type/ISSN metadata를 저장하는 방식으로 개선할 수 있습니다.

### 주의사항
- 현재 데이터 기준 개별 표시 venue는 11개이고, 그 외 그룹은 64개 venue/77편 논문입니다.
- JS 문법 검증을 통과했습니다.
## 2026-06-12 13:34

### 변경 요약
- 게재지 보드에 `Others` 카드를 같은 카드 그룹 안에 표시하도록 정리했습니다.
- 핵심 게재지는 1편이어도 개별 표시하고, 2편 이상 수집된 일반 학술지도 개별 표시하며, 나머지는 `Others`로 묶습니다.

### 수정/생성한 파일
- `assets/app.js`: venue board를 `핵심 게재지 + 2편 이상 학술지 + Others` 순서로 렌더링하도록 수정했습니다.
- `index.html`: venue 기준 설명 문구를 새 구조에 맞게 수정했습니다.
- `AGENT_LOG.md`: 이번 변경 내용을 기록했습니다.

### 구현한 기능
- `Others` 카드가 `All venues`, `Nat. Commun.`, `Science`, `Additive Manufacturing` 등과 같은 영역에 표시됩니다.
- `Others` 카드에는 `2편 이하의 학술지` badge가 표시됩니다.
- `Others`를 클릭하면 묶인 venue의 논문만 필터링됩니다.

### 설계 결정
- Nature/Science/Additive Manufacturing 계열 같은 핵심 타깃 venue는 1편이어도 개별 표시합니다.
- 일반 venue는 2편 이상일 때 개별 표시하고, 나머지는 Others로 묶어 화면 밀도를 낮춥니다.

### 남은 작업
- 없음.

### 주의사항
- 현재 데이터 기준 Others에는 63개 venue, 76편 논문이 묶입니다.
- JS 문법 검증을 통과했습니다.
## 2026-06-12 13:37

### 변경 요약
- `3D 프린팅` 분야의 서브토픽에 `DLP`를 추가했습니다.
- 큰 분야에 `4D 프린팅`을 새로 추가했습니다.
- 4D/DLP 관련 키워드 기반 분류 규칙을 추가했습니다.

### 수정/생성한 파일
- `assets/app.js`: `FIELD_ORDER`, `FIELD_SUBTOPICS`, featured topics, `deriveField()`, `deriveSubtopics()`를 수정했습니다.
- `AGENT_LOG.md`: 이번 분류 체계 변경을 기록했습니다.

### 구현한 기능
- `4D printing`, `4D-printed`, `4D print` 계열 논문은 큰 분야 `4D 프린팅`으로 분류됩니다.
- `DLP`, `digital light processing`, `vat photopolymerization`, `stereolithography`, `SLA` 계열 논문은 `DLP` 서브토픽으로 표시됩니다.
- `4D 프린팅`에는 `4D printing`, `Active materials`, `Shape morphing`, `Stimuli-responsive` 서브토픽을 추가했습니다.

### 설계 결정
- 4D 관련 논문은 AI/3D/로봇 키워드보다 먼저 판별해 별도 큰 분야로 빠지게 했습니다.
- DLP는 독립 큰 분야가 아니라 3D 프린팅 내부 공정/방식 서브토픽으로 배치했습니다.

### 남은 작업
- DLP 범위를 더 넓히려면 `projection micro-stereolithography`, `two-photon polymerization` 같은 광중합 세부 키워드를 추가할 수 있습니다.

### 주의사항
- 현재 데이터 기준 4D 관련 논문은 3편, DLP/vat photopolymerization 관련 논문은 2편이 탐지됩니다.
- JS 문법 검증을 통과했습니다.
## 2026-06-12 13:58

### 변경 요약
- 자동 갱신 실행 시각을 사이트에서 확인할 수 있도록 `data/site_meta.json` 메타데이터를 추가했습니다.
- GitHub Actions가 새 논문이 없어도 마지막 실행 시각을 커밋할 수 있도록 workflow를 수정했습니다.
- 프론트엔드 상단 통계의 `최신 업데이트`가 마지막 파이프라인 실행 시각을 KST로 표시하도록 변경했습니다.

### 수정/생성한 파일
- `data/site_meta.json`: 마지막 실행 UTC 시각, 날짜, 논문 수, 추가 논문 수, 수집 시작 연도, 데이터 출처를 저장하는 메타 파일을 추가했습니다.
- `scripts/update_papers.py`: 실행 시작 시각을 UTC ISO timestamp로 기록하고 `site_meta.json`을 매번 갱신하도록 수정했습니다.
- `.github/workflows/update-papers.yml`: 자동 커밋 대상에 `data/site_meta.json`을 추가했습니다.
- `assets/app.js`: `site_meta.json`을 fetch하고 `last_run_at_utc`를 KST 표시로 변환해 상단 통계에 보여주도록 수정했습니다.
- `README.md`, `ARCHITECTURE.md`, `PROJECT_STATUS.md`: 갱신 시각 메타데이터 정책을 문서화했습니다.
- `AGENT_LOG.md`: 이번 변경 기록을 추가했습니다.

### 구현한 기능
- 사이트 상단의 `최신 업데이트`가 논문별 날짜가 아니라 마지막 자동 갱신 실행 시간을 표시합니다.
- 표시 형식은 `YYYY-MM-DD HH:mm KST`입니다.
- 새 논문이 없어도 workflow 실행 시각이 남습니다.

### 설계 결정
- 논문 데이터와 실행 메타데이터를 분리하기 위해 `papers.json`에 전역 필드를 섞지 않고 `site_meta.json`을 별도로 만들었습니다.
- `last_run_at_utc`는 UTC로 저장하고, 브라우저에서 KST로 변환합니다.
- `site_meta.json` 로딩 실패 시 기존 논문 `last_updated` 날짜를 fallback으로 사용합니다.

### 남은 작업
- 필요하면 `papers_added`를 UI에 추가해 마지막 실행에서 몇 편이 추가되었는지도 표시할 수 있습니다.

### 주의사항
- `site_meta.json`은 자동 실행 때마다 바뀌므로 GitHub Actions가 매시간 커밋을 만들 수 있습니다.
- JS 문법 검증과 Python py_compile을 통과했습니다.
## 2026-06-12 14:00

### 변경 요약
- 상단 `최신 업데이트` 카드에서 날짜만 보이던 표시를 날짜와 시간이 함께 보이도록 개선했습니다.
- 날짜와 시간을 한 줄에 밀어 넣지 않고 날짜/시간 두 줄로 렌더링해 카드 안에서 잘리지 않게 했습니다.

### 수정/생성한 파일
- `assets/app.js`: `renderUpdatedStat()`을 추가하고 `formatRunTime()`이 날짜와 시간을 분리해서 반환하도록 수정했습니다.
- `assets/style.css`: `stat-datetime` 스타일을 추가해 날짜와 시간이 안정적으로 표시되도록 했습니다.
- `data/site_meta.json`: 현재 배포 기준 마지막 실행 시각을 갱신했습니다.
- `AGENT_LOG.md`: 이번 표시 개선 기록을 추가했습니다.

### 구현한 기능
- `최신 업데이트` 카드가 `2026-06-12`와 `13:59 KST`처럼 날짜와 시간을 함께 표시합니다.
- `site_meta.json`이 없거나 로딩 실패하면 기존 날짜 fallback을 유지합니다.

### 설계 결정
- 날짜/시간을 두 줄로 나누어 작은 통계 카드에서도 잘리지 않게 했습니다.
- 저장은 UTC, 표시는 KST 원칙을 유지했습니다.

### 남은 작업
- 없음.

### 주의사항
- JS 문법 검증을 통과했습니다.
## 2026-06-12 14:02

### 변경 요약
- 사용자가 최신 업데이트 시간 표시가 아직 보이지 않는다고 알려주어, 정적 asset 캐시 문제를 줄이기 위한 cache-busting query를 추가했습니다.

### 수정/생성한 파일
- `index.html`: `assets/style.css`와 `assets/app.js` 로드 URL에 `v=20260612-1402`를 추가했습니다.
- `AGENT_LOG.md`: 이번 캐시 무효화 변경 기록을 추가했습니다.

### 구현한 기능
- GitHub Pages 또는 브라우저가 이전 JS/CSS를 계속 사용하는 상황을 줄입니다.
- 최신 업데이트 시간 표시 코드가 포함된 새 `app.js`를 더 확실히 불러오게 됩니다.

### 설계 결정
- 빌드 도구가 없는 정적 사이트이므로 파일명 해시 대신 query string 버전을 사용했습니다.

### 남은 작업
- 향후 CSS/JS 변경이 있을 때 버전 query를 함께 갱신하면 캐시 문제를 줄일 수 있습니다.

### 주의사항
- 배포된 `data/site_meta.json`에는 현재 `2026-06-12T04:59:53Z`, 즉 `2026-06-12 13:59 KST`가 들어 있습니다.
## 2026-06-12 14:07

### 변경 요약
- 우측 상단에 다크/라이트 모드 토글과 한글/영문 UI 토글을 추가했습니다.
- 사용자의 선택을 `localStorage`에 저장해 새로고침 후에도 유지되도록 했습니다.
- 정적 UI 라벨과 주요 동적 라벨이 언어 설정에 따라 바뀌도록 했습니다.

### 수정/생성한 파일
- `index.html`: 헤더 우측 상단에 `theme-toggle`, `language-toggle` 버튼을 추가하고 CSS/JS cache-busting 버전을 갱신했습니다.
- `assets/style.css`: 다크 테마 CSS 변수, 토글 버튼 스타일, 주요 패널/카드 다크 모드 보정 스타일을 추가했습니다.
- `assets/app.js`: UI 번역 사전, 테마/언어 상태 관리, `localStorage` 저장, 정적/동적 문구 갱신 로직을 추가했습니다.
- `AGENT_LOG.md`: 이번 기능 추가를 기록했습니다.

### 구현한 기능
- `Dark` 버튼을 누르면 다크 모드와 라이트 모드를 전환합니다.
- `EN`/`KO` 버튼을 누르면 주요 UI 문구가 영문/한글로 전환됩니다.
- 논문 제목, 저자, venue, DOI, AI 요약은 원 데이터 보존을 위해 번역하지 않습니다.
- 토글 상태는 브라우저에 저장됩니다.

### 설계 결정
- 빌드 도구 없는 GitHub Pages 정적 사이트이므로 CSS 변수와 vanilla JavaScript로 구현했습니다.
- 논문 메타데이터 자체를 번역하지 않고, 탐색 UI/라벨 중심으로만 언어 전환합니다.
- 캐시 문제를 줄이기 위해 `style.css`와 `app.js` query version을 `20260612-1412`로 갱신했습니다.

### 남은 작업
- 더 완전한 영문 모드를 원하면 카테고리/서브토픽 명칭 자체도 영문 별칭으로 표시하는 매핑을 추가할 수 있습니다.

### 주의사항
- JS 문법 검증과 로컬 HTTP 200 확인을 완료했습니다.
## 2026-06-12 14:16

### 변경 요약
- 사용자가 우측/사이드 패널의 분야 및 서브토픽명이 영어 모드에서 바뀌지 않는 문제를 지적해 표시명 번역 매핑을 추가했습니다.
- 영어 모드에서 분야 패널, 그룹 제목, 카테고리/태그 드롭다운, badge가 영어 표시명을 사용하도록 수정했습니다.

### 수정/생성한 파일
- `assets/app.js`: `LABEL_TRANSLATIONS`와 `displayLabel()`을 추가하고 동적 라벨 렌더링 지점에 적용했습니다.
- `index.html`: CSS/JS cache-busting 버전을 `20260612-1420`으로 갱신했습니다.
- `AGENT_LOG.md`: 이번 수정 기록을 추가했습니다.

### 구현한 기능
- 영어 모드에서 `생산/제조`는 `Production/Manufacturing`, `3D 프린팅`은 `3D Printing`, `4D 프린팅`은 `4D Printing` 등으로 표시됩니다.
- 서브토픽과 기존 카테고리 badge도 가능한 범위에서 영어로 표시됩니다.
- 내부 필터 값은 한국어 원키를 유지하므로 기존 필터 로직은 그대로 동작합니다.

### 설계 결정
- 데이터 자체를 수정하지 않고 UI 표시명만 변환했습니다.
- 번역되지 않은 전문 약어와 고유명사는 그대로 유지합니다.

### 남은 작업
- 더 완전한 영문 모드를 원하면 모든 자동 생성 태그에 대한 별칭을 계속 보강할 수 있습니다.

### 주의사항
- JS 문법 검증과 로컬 HTTP 200 확인을 완료했습니다.
## 2026-06-12 14:25

### 변경 요약
- 전체 UI의 글자 크기, 카드 밀도, 반응형 레이아웃을 재조정했습니다.
- 기존 기능을 유지하면서 더 polished한 academic dashboard 느낌이 나도록 visual refinement CSS layer를 추가했습니다.

### 수정/생성한 파일
- `assets/style.css`: 타이포 스케일, 카드/필터/통계/venue/paper card spacing, hover 효과, 모바일 레이아웃을 조정하는 refinement layer를 추가했습니다.
- `index.html`: CSS/JS cache-busting 버전을 `20260612-1430`으로 갱신했습니다.
- `AGENT_LOG.md`: 이번 UI 최적화 기록을 추가했습니다.

### 구현한 기능
- 헤더 H1과 부제 크기를 줄여 첫 화면 정보 밀도를 개선했습니다.
- 왼쪽 분야 패널 폭을 넓히고 서브토픽 글자 크기와 행간을 정리했습니다.
- 통계 카드, 필터 폼, venue 카드, 논문 카드의 글자 크기와 padding을 통일했습니다.
- 논문 카드 grid 최소 폭을 키워 제목/요약이 덜 답답하게 보이도록 했습니다.
- 모바일에서는 통계가 2열, 필터가 1열로 안정적으로 접히도록 보정했습니다.

### 설계 결정
- 기존 CSS를 대규모로 재작성하지 않고 하단 override layer로 덧씌웠습니다. 기능 리스크를 줄이기 위해서입니다.
- decorative 요소는 과하게 추가하지 않고 배경에 아주 약한 수직 그라데이션과 그림자 계층만 사용했습니다.
- 카드 radius는 기존 지침에 맞춰 8px 이하를 유지했습니다.

### 남은 작업
- 실제 브라우저 스크린샷 기준으로 더 미세한 줄바꿈/높이 조정이 필요할 수 있습니다.

### 주의사항
- JS 문법 검증과 로컬 HTTP 200 확인을 완료했습니다.
## 2026-06-12 14:35

### 변경 요약
- 다크 모드에서 일부 색 대비가 어색한 문제를 개선했습니다.
- 다크 전용 contrast pass를 추가해 배경, 패널, 버튼, badge, notice, 입력창, 링크 버튼의 색을 일관되게 조정했습니다.

### 수정/생성한 파일
- `assets/style.css`: 다크 모드 색상 변수와 컴포넌트별 대비 보정 스타일을 추가했습니다.
- `index.html`: CSS/JS cache-busting 버전을 `20260612-1438`로 갱신했습니다.
- `AGENT_LOG.md`: 이번 다크 모드 색상 보정 기록을 추가했습니다.

### 구현한 기능
- 다크 모드에서 notice, badge, card topline, form input, venue/topic pill, link button의 텍스트 대비가 더 안정적으로 보입니다.
- active/hover 상태가 과하게 밝거나 탁하게 보이지 않도록 blue/green/amber 계열을 다크 팔레트에 맞췄습니다.
- placeholder와 muted text 색상을 어두운 배경에서 읽기 쉬운 수준으로 조정했습니다.

### 설계 결정
- 기존 라이트 모드 색상은 건드리지 않고 `:root[data-theme="dark"]` override만 추가했습니다.
- 색상은 pure black이 아니라 deep navy 계열을 사용해 눈부심을 줄였습니다.

### 남은 작업
- 실제 브라우저에서 특정 카드/배지가 여전히 튀면 해당 컴포넌트별로 추가 미세 조정할 수 있습니다.

### 주의사항
- JS 문법 검증과 로컬 HTTP 200 확인을 완료했습니다.
## 2026-06-12 14:46

### 변경 요약
- 사용자가 상단 시간이 13시에서 멈춰 보인다고 지적해, 현재 시각과 마지막 수집 실행 시각을 분리해서 표시하도록 변경했습니다.
- `현재 / 갱신` 카드가 현재 KST 시각을 1분마다 갱신하고, 작은 글씨로 마지막 수집 실행 시각을 함께 보여줍니다.

### 수정/생성한 파일
- `assets/app.js`: `renderUpdatedStat()`을 현재 시각 기준으로 렌더링하도록 수정하고, 1분마다 `updateStats()`를 다시 호출하는 timer를 추가했습니다.
- `index.html`: CSS/JS cache-busting 버전을 `20260612-1446`으로 갱신했습니다.
- `AGENT_LOG.md`: 이번 변경 내용을 기록했습니다.

### 구현한 기능
- 상단 카드가 `현재 날짜`와 `현재 HH:mm KST`를 실시간에 가깝게 표시합니다.
- 같은 줄에 `수집 HH:mm KST`로 마지막 자동 수집 실행 시각을 표시합니다.

### 설계 결정
- `site_meta.json`의 시간은 실시간 시계가 아니라 마지막 수집 실행 시각이므로, UI에서 두 의미를 분리했습니다.
- 초 단위 갱신은 불필요하다고 판단해 1분 단위 갱신으로 구현했습니다.

### 남은 작업
- GitHub Actions의 `Update papers` cron 실행이 최근 기록에 보이지 않아, 필요하면 Actions 설정/스케줄 활성화 여부를 별도로 확인해야 합니다.

### 주의사항
- JS 문법 검증을 통과했습니다.
## 2026-06-13 00:30

### 변경 요약
- 상단 통계 영역을 방문자용 핵심 지표인 `논문수` 1개만 표시하도록 단순화했습니다.
- raw candidates와 archived hidden 수치는 메인 화면에서 빼고, 하단 footer의 작은 운영 정보로 이동했습니다.
- 숨긴 후보는 삭제가 아니라 메인 큐레이션 화면에서 제외된 공개 archive 데이터라는 의미를 유지했습니다.

### 수정/생성한 파일
- `index.html`: 상단 통계 카드 4개를 1개로 줄이고, footer에 `ops-note` 영역을 추가했으며 CSS/JS cache-busting 버전을 갱신했습니다.
- `assets/app.js`: 상단 통계는 `data/papers.json`에 표시되는 논문 수만 렌더링하고, raw/archive/last collection 정보는 footer 운영 정보로 렌더링하도록 수정했습니다.
- `assets/style.css`: 1개 통계 카드 레이아웃과 footer 운영 정보 스타일을 추가했습니다.
- `AGENT_LOG.md`: 이번 UI 정보 구조 변경 기록을 추가했습니다.
- `PROJECT_STATUS.md`: 현재 상태 설명을 상단 통계 단순화 기준으로 갱신했습니다.

### 구현한 기능
- 방문자에게 보이는 상단 수치는 현재 사이트에 실제 표시되는 curated paper 수만 보여줍니다.
- 운영자는 하단에서 수집 후보 수, 숨김 archive 수, 마지막 수집 시간을 계속 확인할 수 있습니다.
- 언어 전환 시 footer 운영 정보도 한국어/영어로 함께 바뀝니다.

### 설계 결정
- raw/archive 수치를 삭제하지 않고 footer에 낮은 우선순위로 둔 이유는 큐레이션 품질 감사와 다음 작업 인수인계에 필요하기 때문입니다.
- `archive_papers.json`은 공개 GitHub Pages 데이터 파일로 남아 있으므로 "비공개"가 아니라 "메인 목록에서 숨김"에 가깝습니다.
- 상단에서 후보/숨김 숫자를 제거한 이유는 방문자가 실제 논문 수와 후보 수를 혼동하지 않게 하기 위해서입니다.

### 남은 작업
- archive 데이터를 완전히 비공개로 만들려면 GitHub Pages 배포 대상에서 `data/archive_papers.json`을 제외하고 별도 비공개 저장소나 artifact로 옮기는 추가 설계가 필요합니다.

### 주의사항
- API key, token, secret은 기록하지 않았습니다.

## 2026-06-13 00:45

### 변경 요약
- 상단 통계에서 너무 많은 정보를 제거해 화면이 휑해진 문제를 수정했습니다.
- 방문자에게 필요한 `논문수`와 `현재 / 갱신` 시간 카드는 상단에 다시 표시하고, raw/archive 운영 숫자만 footer에 유지했습니다.

### 수정/생성한 파일
- `index.html`: `stat-updated` 카드를 복원하고 CSS/JS cache-busting 버전을 갱신했습니다.
- `assets/app.js`: `현재 KST 시각`과 `마지막 수집 시각`을 함께 렌더링하도록 `renderUpdatedStat()`을 다시 연결했습니다.
- `assets/style.css`: 상단 통계 카드 2개가 덜 비어 보이도록 flex gap과 카드 폭을 조정했습니다.
- `AGENT_LOG.md`: 이번 정정 작업을 기록했습니다.

### 구현한 기능
- 상단에는 현재 표시 논문 수와 실시간 KST 현재 시각, 마지막 수집 시간이 표시됩니다.
- 수집 후보 수와 archive hidden 수는 footer 운영 정보에만 표시됩니다.

### 설계 결정
- `Raw Candidates`와 `Archived Hidden`은 방문자에게 혼동을 주므로 상단에서 제외했습니다.
- 업데이트/현재 시각은 사이트 신뢰도와 자동 갱신 상태 확인에 중요하므로 상단에 유지했습니다.

### 남은 작업
- 브라우저에서 카드 간격이 더 어색하면 통계 영역을 2열 grid 또는 compact strip 형태로 추가 조정할 수 있습니다.

### 주의사항
- API key, token, secret은 기록하지 않았습니다.

## 2026-06-13 00:55

### 변경 요약
- 상단 통계가 `논문수`와 `현재 / 갱신` 두 카드만 있어 화면이 휑해 보이는 문제를 개선했습니다.
- raw/archive 운영 숫자는 footer에 유지하면서, 공개적으로 의미 있는 `게재지 수`와 `조사연도` 카드를 상단에 추가했습니다.

### 수정/생성한 파일
- `index.html`: `stat-venues`, `stat-years` 카드를 추가하고 CSS/JS cache-busting 버전을 갱신했습니다.
- `assets/app.js`: 현재 표시 논문 기준 게재지 수와 연도 범위를 계산해 상단 카드에 렌더링하도록 수정했습니다.
- `assets/style.css`: 상단 통계를 4열 grid로 복원해 빈 공간을 줄였습니다.
- `AGENT_LOG.md`: 이번 UI 보강 기록을 추가했습니다.

### 구현한 기능
- 상단 카드: `논문수`, `게재지`, `조사연도`, `현재 / 갱신`.
- 후보/숨김 같은 운영용 숫자는 계속 footer 운영 정보에만 표시됩니다.

### 설계 결정
- `게재지`와 `조사연도`는 방문자에게도 유용한 공개 지표라 상단에 적합하다고 판단했습니다.
- raw candidate와 archive hidden 수는 실제 표시 논문 수와 혼동될 수 있어 상단에는 복원하지 않았습니다.

### 남은 작업
- 카드명이 더 마음에 들지 않으면 `게재지`를 `수록 게재지`, `조사연도`를 `연도 범위`처럼 다듬을 수 있습니다.

### 주의사항
- API key, token, secret은 기록하지 않았습니다.

## 2026-06-13 01:10

### 변경 요약
- 마우스 이벤트가 단조롭다는 피드백을 반영해 UI interaction polish layer를 추가했습니다.
- 논문 카드, venue 카드, 사이드바 토픽, 필터 입력, 버튼, 태그의 hover/focus/active 상태를 더 쫀득하게 조정했습니다.

### 수정/생성한 파일
- `index.html`: CSS/JS cache-busting 버전을 `20260613-0060`으로 갱신했습니다.
- `assets/style.css`: motion 변수, hover lift, press feedback, focus ring, subtle gradient overlay, link shine, reduced-motion 대응을 추가했습니다.
- `AGENT_LOG.md`: 이번 UI interaction 개선 기록을 추가했습니다.

### 구현한 기능
- 논문 카드 hover 시 살짝 떠오르고 제목 색이 바뀌며 배경에 약한 highlight가 생깁니다.
- venue 카드와 사이드바 항목 hover/active 상태가 더 명확하게 반응합니다.
- 버튼과 태그는 hover lift, active press, focus-visible ring을 지원합니다.
- `prefers-reduced-motion: reduce` 사용자는 움직임이 거의 제거됩니다.

### 설계 결정
- 학술 큐레이션 사이트의 차분한 성격을 유지하기 위해 큰 애니메이션 대신 1-3px 이동, 짧은 easing, 미세한 그림자 변화 중심으로 구현했습니다.
- 다크모드 대비가 깨지지 않도록 기존 CSS 변수와 `color-mix()`를 사용했습니다.

### 남은 작업
- 실제 브라우저에서 움직임이 과하거나 약하면 duration과 translate 값을 더 조정할 수 있습니다.

### 주의사항
- API key, token, secret은 기록하지 않았습니다.

## 2026-06-13 01:25

### 변경 요약
- OpenAI 사용량이 예상보다 크게 발생한 원인을 조사했습니다.
- 정기 `Update papers` workflow에서 raw 후보 수집 단계에 OpenAI 요약기가 켜질 수 있었던 비용 리스크를 차단했습니다.
- 앞으로 OpenAI 요약은 수동 `Refresh OpenAI summaries` workflow에서 curated papers 대상으로만 실행하는 운영 원칙으로 정리했습니다.

### 수정/생성한 파일
- `scripts/update_papers.py`: `ALLOW_OPENAI_IN_UPDATE=true`가 명시된 경우에만 정기 업데이트 중 OpenAI 호출을 허용하도록 변경했습니다. 기본값은 비활성화입니다.
- `.github/workflows/update-papers.yml`: 정기 업데이트 job에서 `OPENAI_API_KEY`와 `OPENAI_MODEL` 전달을 제거하고 `ALLOW_OPENAI_IN_UPDATE=false`를 명시했습니다.
- `.github/workflows/refresh-openai-summaries.yml`: 수동 요약 workflow의 `max_summaries` 설명을 비용 통제 중심으로 명확히 수정했습니다.
- `AGENT_LOG.md`: 비용 사고 원인과 방지책을 기록했습니다.
- `PROJECT_STATUS.md`: OpenAI 호출 정책과 비용 방어 상태를 갱신했습니다.
- `ARCHITECTURE.md`: 수집 파이프라인과 요약 파이프라인의 분리 원칙을 문서화했습니다.

### 구현한 기능
- 정기 metadata 수집은 OpenAI API key가 repository secret에 있어도 기본적으로 OpenAI를 호출하지 않습니다.
- OpenAI 요약은 별도 수동 workflow에서만 실행됩니다.
- 실수로 정기 workflow에 key가 다시 전달되어도 코드 기본값이 OpenAI 호출을 막습니다.

### 설계 결정
- 비용이 발생하는 AI 요약은 후보 수집/필터링 이후의 curated papers에만 적용해야 합니다.
- raw candidates와 archive candidates는 무료 fallback 요약/점수로만 처리하고, 필요 시 나중에 수동으로 curated 항목만 재요약합니다.

### 남은 작업
- GitHub Actions에서 이미 실행 중인 이전 scheduled run은 권한 토큰 없이 이 환경에서 취소할 수 없습니다. 필요하면 GitHub Actions UI에서 현재 실행 중인 `Update papers`를 수동 취소하세요.
- 향후 `refresh_openai_summaries.py`에 예상 비용 출력과 hard cap을 추가하면 더 안전합니다.

### 주의사항
- API key, token, secret은 기록하지 않았습니다.
- 이번 변경은 향후 실행 비용 방지용이며, 이미 발생한 OpenAI usage를 되돌리지는 않습니다.

## 2026-06-13 01:40

### 변경 요약
- 사용자의 절대 규칙을 반영했습니다: OpenAI API는 사용자가 명시적으로 요구할 때만 사용하며, 새로 업데이트되는 모든 논문에는 적용하지 않습니다.
- OpenAI가 적용되지 않은 논문을 사이트에서 바로 알아볼 수 있도록 논문 카드에 요약 출처 배지를 추가했습니다.
- 데이터 파일에 `summary_provider`와 `openai_summary_applied` 필드를 추가했습니다.

### 수정/생성한 파일
- `data/papers.json`: 현재 curated 414편 모두 `summary_provider: fallback`, `openai_summary_applied: false`로 표시했습니다.
- `data/archive_papers.json`: 기존 영문 OpenAI 요약 흔적이 있는 archive 항목은 `openai_summary_applied: true`, 나머지는 `false`로 표시했습니다.
- `data/site_meta.json`: OpenAI 정기 업데이트 비활성화 정책 메타데이터를 추가했습니다.
- `assets/app.js`: 논문 카드 상단에 `OpenAI 미적용` / `OpenAI 요약` 배지를 렌더링하도록 추가했습니다.
- `assets/style.css`: 요약 출처 배지의 라이트/다크 모드 스타일을 추가했습니다.
- `index.html`: CSS/JS cache-busting 버전을 `20260613-0070`으로 갱신했습니다.
- `.github/workflows/refresh-openai-summaries.yml`: 수동 OpenAI workflow가 명시 문구 없이는 실패하도록 안전 입력을 추가했습니다.
- `scripts/update_papers.py`: 새 논문 저장 시 요약 출처 필드를 보존하도록 수정했습니다.
- `scripts/refresh_openai_summaries.py`: 실제 OpenAI 요약 적용 시 `summary_provider: openai`, `openai_summary_applied: true`를 기록하도록 수정했습니다.
- `PROJECT_STATUS.md`: OpenAI 절대 규칙과 UI 표시 상태를 갱신했습니다.
- `ARCHITECTURE.md`: OpenAI 사용 정책 및 요약 출처 필드를 문서화했습니다.

### 구현한 기능
- 새로 업데이트되는 논문은 OpenAI를 사용하지 않습니다.
- OpenAI가 적용되지 않은 논문은 카드 상단에 `OpenAI 미적용` 배지로 표시됩니다.
- 사용자가 명시적으로 요구하지 않으면 수동 OpenAI workflow도 실행되지 않습니다.

### 설계 결정
- OpenAI 적용 여부는 추측 가능한 UI 상태가 아니라 데이터 필드로 명시 저장합니다.
- 정기 업데이트와 OpenAI 요약은 완전히 분리된 운영 경로로 유지합니다.

### 남은 작업
- 사용자가 나중에 명시적으로 요청하면 curated 논문 일부 또는 전체에 대해서만 OpenAI 요약을 실행할 수 있습니다.

### 주의사항
- API key, token, secret은 기록하지 않았습니다.
- 현재 curated 414편의 OpenAI 적용 수는 0편입니다.

## 2026-06-13 01:55

### 변경 요약
- 논문 카드 hover 애니메이션을 더 풍성하게 개선했습니다.
- 카드가 뜨는 느낌에 더해 내부 제목, topline, summary, tag, link 영역이 미세하게 따라 움직이도록 했습니다.

### 수정/생성한 파일
- `index.html`: CSS/JS cache-busting 버전을 `20260613-0080`으로 갱신했습니다.
- `assets/style.css`: paper-card 전용 final hover layer를 추가했습니다.
- `AGENT_LOG.md`: 이번 마우스 인터랙션 개선 기록을 추가했습니다.

### 구현한 기능
- 논문 카드 hover 시 더 큰 lift, scale, shadow가 적용됩니다.
- 카드 내부에 radial/linear highlight overlay가 부드럽게 나타납니다.
- 제목과 요약 블록, 태그, 링크 영역이 작은 시차감을 갖고 움직입니다.
- 다크모드용 shadow와 highlight 대비를 별도로 보정했습니다.

### 설계 결정
- hover 효과는 논문 카드에만 강화하고, 전체 사이트의 학술적 톤은 유지했습니다.
- 기존 CSS 뒤쪽 refinement가 hover를 덮어쓰고 있어 파일 후반에 final layer로 배치했습니다.

### 남은 작업
- 실제 브라우저에서 움직임이 과하면 `translateY(-5px)`와 `scale(1.008)` 값을 낮추면 됩니다.

### 주의사항
- API key, token, secret은 기록하지 않았습니다.
- 작업 중 `data/papers.json`, `data/site_meta.json`에 별도 변경이 감지되었지만 이번 UI 커밋에는 포함하지 않았습니다.

## 2026-06-13 02:10

### 변경 요약
- 전체 UI가 가운데에 몰려 보인다는 피드백을 반영해 데스크톱 wide layout을 확장했습니다.
- 큰 화면에서는 헤더, venue nav, sidebar, 본문 grid가 좌우 공간을 더 적극적으로 사용합니다.

### 수정/생성한 파일
- `index.html`: CSS/JS cache-busting 버전을 `20260613-0090`으로 갱신했습니다.
- `assets/style.css`: 1200px 이상과 1560px 이상 화면에 대한 wide layout pass를 추가했습니다.
- `AGENT_LOG.md`: 이번 레이아웃 확장 기록을 추가했습니다.

### 구현한 기능
- `.wide-shell` 최대 폭을 큰 화면에서 1760px까지 확장했습니다.
- 데스크톱 헤더와 venue nav를 왼쪽 정렬로 바꿔 공간이 덜 비어 보이도록 했습니다.
- sidebar 폭과 main content 간격을 넓혔습니다.
- 논문 카드 grid가 큰 화면에서 4열 이상 자연스럽게 펼쳐지도록 조정했습니다.
- 필터와 venue 카드도 넓은 화면에서 더 여유 있게 배치됩니다.

### 설계 결정
- 모바일/태블릿 레이아웃은 기존 breakpoint를 유지하고, 1200px 이상에서만 넓은 레이아웃을 적용했습니다.
- 카드 자체를 크게 키우기보다 grid 폭을 넓혀 좌우 공간 활용을 개선했습니다.

### 남은 작업
- 실제 브라우저에서 1440px/1920px 기준 카드 열 수가 너무 많거나 적으면 `--grid-min` 값을 다시 조정할 수 있습니다.

### 주의사항
- API key, token, secret은 기록하지 않았습니다.
- 로컬에 남아 있던 `data/papers.json`, `data/site_meta.json` 변경은 이번 UI 커밋에 포함하지 않을 예정입니다.

## 2026-06-13 02:20

### 변경 요약
- 이전 wide layout 변경이 뒤쪽 CSS refinement에 의해 덮이는 문제를 수정했습니다.
- 논문 패널이 실제로 좌우 화면 폭을 더 많이 쓰도록 파일 맨 끝에 final desktop width override를 추가했습니다.

### 수정/생성한 파일
- `index.html`: CSS/JS cache-busting 버전을 `20260613-0100`으로 갱신했습니다.
- `assets/style.css`: 1200px 이상과 1680px 이상에서 `.wide-shell`, `.main-layout`, `.paper-group`을 최종 override로 확장했습니다.
- `AGENT_LOG.md`: 이번 레이아웃 수정 기록을 추가했습니다.

### 구현한 기능
- 큰 화면에서 좌우 margin을 `20px` 이하로 줄였습니다.
- sidebar는 280px로 유지하고, 나머지 폭을 논문 패널에 더 몰아줍니다.
- 논문 grid 최소 폭을 280px, 초대형 화면에서는 270px로 낮춰 더 많은 카드 열을 표시합니다.
- `content`, `paper-list`, `paper-group`의 `max-width` 제한을 제거했습니다.

### 설계 결정
- 기존 CSS 레이어가 많아 중간 위치의 width 규칙이 덮였기 때문에, 이번에는 파일 마지막에 final override를 배치했습니다.
- 논문 카드 자체를 무리하게 넓히는 대신 카드 열 수를 늘려 데스크톱 공간 활용을 높였습니다.

### 남은 작업
- 실제 1920px 화면에서 카드가 너무 촘촘하면 `--grid-min`을 290px 정도로 되돌릴 수 있습니다.

### 주의사항
- API key, token, secret은 기록하지 않았습니다.
- 로컬에 남아 있는 `data/papers.json`, `data/site_meta.json` 변경은 이번 UI 커밋에 포함하지 않습니다.

## 2026-06-13 09:23

### 변경 요약
- `Additive Manufacturing with Graded Bio-Polymer Composites`가 DOI는 있지만 venue가 `Venue unknown`으로 표시되는 원인을 확인했습니다.
- OpenAlex 레코드는 venue가 비어 있었고, Crossref DOI 메타데이터에는 `ROB|ARCH2024 – Robotic Fabrication in Architecture, Art and Design`가 `container-title`로 존재했습니다.
- 기존 레코드와 새 후보가 DOI로 병합될 때 비어 있는 venue/year/authors를 보강하도록 업데이트 파이프라인을 수정했습니다.

### 수정/생성한 파일
- `scripts/fetch_crossref.py`: DOI 직접 조회 함수 `fetch_crossref_by_doi`를 추가했습니다.
- `scripts/update_papers.py`: 기존 레코드 병합 시 비어 있는 venue/year/authors를 후보 메타데이터로 채우고, venue가 비어 있으면 Crossref DOI 조회로 한 번 더 보강하도록 수정했습니다.
- `AGENT_LOG.md`: venue unknown 원인과 수정 내용을 기록했습니다.

### 구현한 기능
- OpenAlex에서 venue가 비어 들어온 논문도 Crossref에 DOI 메타데이터가 있으면 이후 업데이트에서 venue를 보강할 수 있습니다.
- 기존 DOI 중복 병합 시 source만 합치던 동작을 확장해 메타데이터 누락 필드를 보완합니다.

### 설계 결정
- 출판사 페이지를 크롤링하지 않고 Crossref 공식 API의 `container-title`만 사용했습니다.
- PDF나 원문 초록은 저장하지 않았습니다.

### 남은 작업
- 현재 로컬 `data/papers.json`, `data/site_meta.json`에는 별도 변경이 남아 있어 이번 스크립트 수정 커밋에는 포함하지 않습니다.
- 다음 정기 업데이트 또는 별도 데이터 정리 커밋에서 해당 DOI의 venue 값을 반영할 수 있습니다.

### 주의사항
- API key, token, secret은 기록하지 않았습니다.
- Crossref DOI 보강은 rate limit을 피하기 위해 venue가 비어 있고 DOI가 있는 기존 레코드에 한정했습니다.

## 2026-06-13 09:27

### 변경 요약
- 논문 카드의 `No OpenAI` / `OpenAI 미적용` 뱃지가 일반 방문자에게 의미가 모호한 문제를 개선했습니다.
- OpenAI 미사용 상태를 `Metadata summary` / `메타데이터 요약`으로 바꾸고, hover tooltip에 설명을 추가했습니다.

### 수정/생성한 파일
- `assets/app.js`: summary provider 라벨을 `AI summary` / `Metadata summary` 및 한국어 대응 문구로 변경하고 title 설명을 추가했습니다.
- `assets/style.css`: 메타데이터 요약 뱃지를 경고색이 아닌 중립 정보성 색상으로 조정했습니다.
- `index.html`: CSS/JS cache-busting 버전을 `20260613-0130`으로 갱신했습니다.
- `AGENT_LOG.md`: 이번 뱃지 문구 및 스타일 변경 기록을 추가했습니다.

### 구현한 기능
- OpenAI API를 사용하지 않은 논문은 `Metadata summary` / `메타데이터 요약`으로 표시됩니다.
- OpenAI API로 생성된 논문은 `AI summary` / `AI 요약`으로 표시됩니다.
- 뱃지에 마우스를 올리면 해당 요약 방식의 의미를 확인할 수 있습니다.

### 설계 결정
- `No OpenAI`는 내부 비용/운영 정책처럼 보일 수 있어, 방문자 관점에서 요약의 생성 근거를 설명하는 이름으로 바꿨습니다.
- 메타데이터 기반 요약은 문제가 있는 상태가 아니므로 노란 경고색 대신 중립색을 사용했습니다.

### 남은 작업
- 없음.

### 주의사항
- API key, token, secret은 기록하지 않았습니다.
- 이번 변경은 UI 표시만 바꾸며 OpenAI API 호출은 발생하지 않습니다.

## 2026-06-13 09:37

### 변경 요약
- 핸드폰 화면에서 헤더, topic 패널, 통계/필터, 논문 카드가 뭉개지는 문제를 모바일 전용 CSS로 개선했습니다.
- 데스크톱 레이아웃은 유지하고 `max-width: 760px` 이하에서만 단일 컬럼 읽기 흐름으로 전환했습니다.
- 모바일 topic 패널의 숫자 badge가 오른쪽 밖으로 밀려 보이지 않는 문제를 해결하기 위해 카운트를 라벨 옆에 배치했습니다.

### 수정/생성한 파일
- `assets/style.css`: 모바일 전용 레이아웃 override, sidebar/topic panel 폭 보정, 카드 1열 배치, 모바일 버튼/태그 줄바꿈 규칙을 추가했습니다.
- `index.html`: CSS/JS cache-busting 버전을 `20260613-0143`으로 갱신했습니다.
- `AGENT_LOG.md`: 모바일 UI 개선과 검증 내용을 기록했습니다.

### 구현한 기능
- 모바일에서 좌측 패널이 본문 위로 이동하고, topic/subtopic 목록은 한 줄에 하나씩 안정적으로 표시됩니다.
- 논문 카드는 모바일에서 1열로 표시되며, DOI/Paper/Copy Cite 버튼은 터치하기 쉬운 폭으로 표시됩니다.
- 상단 venue chip은 가로 스크롤 가능한 pill row로 표시되어 작은 화면에서 줄이 과도하게 늘어나지 않습니다.

### 설계 결정
- 데스크톱의 넓은 grid 레이아웃은 그대로 두고, 모바일 breakpoint만 강하게 override했습니다.
- 모바일에서는 오른쪽 끝 정렬 카운트보다 가독성과 잘림 방지를 우선해 카운트 badge를 라벨 옆에 표시했습니다.
- hover 애니메이션은 터치 화면에서 불필요한 레이아웃 흔들림을 줄이기 위해 모바일에서 비활성화했습니다.

### 남은 작업
- 실제 iOS Safari/Android Chrome에서 한 번 더 수동 확인하면 좋습니다.

### 주의사항
- API key, token, secret은 기록하지 않았습니다.
- 검증용으로 생성한 headless Chrome 스크린샷과 임시 프로필 폴더는 커밋 전에 삭제했습니다.
- 로컬에 남아 있는 `data/papers.json`, `data/site_meta.json` 변경은 이번 UI 커밋에 포함하지 않습니다.

## 2026-06-13 09:40

### 변경 요약
- 사용자가 매시 17분 업데이트가 멈춘 이유를 문의해 GitHub Actions 최근 실행 상태를 확인했습니다.
- `Update papers` workflow는 수집 단계는 성공했지만, 장시간 실행 중 main 브랜치에 UI 커밋이 추가되어 `Commit changed data` 단계에서 push가 실패한 것으로 확인했습니다.
- 이후 동일한 push reject가 반복되지 않도록 데이터 커밋 후 `git pull --rebase --autostash origin main`을 수행한 뒤 push하도록 수정했습니다.

### 수정/생성한 파일
- `.github/workflows/update-papers.yml`: 데이터 자동 커밋 후 최신 main을 rebase하고 push하도록 변경했습니다.
- `AGENT_LOG.md`: 업데이트 정지 원인과 workflow 보강 내용을 기록했습니다.

### 구현한 기능
- 업데이트 workflow가 오래 실행되는 동안 UI/문서 커밋이 먼저 main에 들어가도, 데이터 커밋 단계에서 최신 main을 반영한 뒤 push를 재시도할 수 있습니다.

### 설계 결정
- 수집 전이 아니라 커밋 직후 rebase를 수행했습니다. 수집 결과를 잃지 않으면서 원격 main의 최신 UI 변경을 함께 반영하기 위해서입니다.
- `--autostash`를 사용해 rebase 중 작업 트리 변경이 있을 때도 안전하게 처리하도록 했습니다.

### 남은 작업
- 다음 정기 실행 또는 수동 `workflow_dispatch` 실행에서 정상 커밋/배포되는지 확인하면 좋습니다.

### 주의사항
- API key, token, secret은 기록하지 않았습니다.
- 이번 변경은 workflow 안정성 수정이며 OpenAI API 호출과 무관합니다.

## 2026-06-13 10:34

### 변경 요약
- 사용자가 매시 17분 실행이 애매하다고 요청해 논문 자동 업데이트 cron을 정각 실행으로 변경했습니다.

### 수정/생성한 파일
- `.github/workflows/update-papers.yml`: `cron: "17 * * * *"`를 `cron: "0 * * * *"`로 변경했습니다.
- `AGENT_LOG.md`: 스케줄 변경 이유와 내용을 기록했습니다.

### 구현한 기능
- GitHub Actions `Update papers` workflow가 매시간 정각 기준으로 예약 실행됩니다.

### 설계 결정
- 사용자가 직관적으로 이해하기 쉬운 정각 실행을 우선했습니다.
- GitHub Actions cron은 정각 설정이어도 실제 시작은 GitHub 큐 상태에 따라 지연될 수 있습니다.

### 남은 작업
- 다음 정각 실행이 생성되는지 확인하면 좋습니다.

### 주의사항
- API key, token, secret은 기록하지 않았습니다.
- 이번 변경은 스케줄만 바꾸며 OpenAI API 호출과 무관합니다.

## 2026-06-13 10:38

### 변경 요약
- 사용자가 OpenAI 토큰 사용량 증가를 우려해 자동 업데이트 차단 상태를 재확인했습니다.
- `Update papers` workflow는 `ALLOW_OPENAI_IN_UPDATE: "false"`이며 `OPENAI_API_KEY`를 주입하지 않아 OpenAI API를 호출할 수 없음을 확인했습니다.
- 추가 안전장치로 수동 `Refresh OpenAI summaries` workflow도 repository variable `OPENAI_REFRESH_ENABLED=true`가 설정되어 있지 않으면 실행 단계에서 차단되도록 변경했습니다.

### 수정/생성한 파일
- `.github/workflows/refresh-openai-summaries.yml`: explicit phrase 외에 `OPENAI_REFRESH_ENABLED` repository variable guard를 추가했습니다.
- `AGENT_LOG.md`: OpenAI 비용 차단 확인과 추가 guard 내용을 기록했습니다.

### 구현한 기능
- 정기/수동 논문 수집 workflow에서는 OpenAI API를 사용하지 않습니다.
- OpenAI 요약 refresh workflow는 명시 문구와 별도로 repo variable을 켜야만 실행됩니다.

### 설계 결정
- 사용자의 “OpenAI API는 요구할 때만” 규칙을 더 강하게 보장하기 위해, 수동 workflow에도 이중 잠금장치를 추가했습니다.
- API key, secret, token 값은 로그에 기록하지 않았습니다.

### 남은 작업
- OpenAI 대시보드의 증가분이 이 저장소 외 다른 API 사용 또는 Codex/ChatGPT 사용량인지 계정/프로젝트 단위에서 확인해야 합니다.

### 주의사항
- 기존 대시보드 누적 토큰은 과거 실행 기록과 다른 OpenAI 사용량을 포함할 수 있습니다.
- 이번 변경은 OpenAI 호출을 발생시키지 않습니다.

## 2026-06-13 11:13

### 변경 요약
- 정각 cron(`0 * * * *`)에서 11:00 KST scheduled run이 생성되지 않은 것을 확인한 뒤, 사용자의 요청에 따라 논문 자동 업데이트 시간을 다시 매시 17분으로 되돌렸습니다.

### 수정/생성한 파일
- `.github/workflows/update-papers.yml`: `cron: "0 * * * *"`를 `cron: "17 * * * *"`로 변경했습니다.
- `AGENT_LOG.md`: 정각 실행이 GitHub schedule에서 누락된 이유와 17분 복귀 결정을 기록했습니다.

### 구현한 기능
- GitHub Actions `Update papers` workflow가 다시 매시간 17분 기준으로 예약 실행됩니다.

### 설계 결정
- 정각은 직관적이지만 GitHub Actions 큐가 몰려 scheduled run 생성이 누락될 수 있어, 상대적으로 덜 몰리는 17분 실행으로 되돌렸습니다.

### 남은 작업
- 다음 12:17 KST 전후 scheduled run이 생성되는지 확인하면 좋습니다.

### 주의사항
- API key, token, secret은 기록하지 않았습니다.
- 논문이 새로 추가되지 않아도 workflow가 성공하면 `data/site_meta.json`의 `last_run_at_utc`가 갱신되어야 합니다.

## 2026-06-13 11:37

### 변경 요약
- 사용자가 “정확한 시각”보다 “주기적으로 실제 업데이트가 돌아가는 것”이 목표라고 정리해, 자동 논문 업데이트 주기를 1시간마다에서 6시간마다로 변경했습니다.

### 수정/생성한 파일
- `.github/workflows/update-papers.yml`: `cron: "17 * * * *"`를 `cron: "17 */6 * * *"`로 변경했습니다.
- `AGENT_LOG.md`: 6시간 주기 변경 이유와 운영 방식을 기록했습니다.

### 구현한 기능
- GitHub Actions `Update papers` workflow가 UTC 기준 0, 6, 12, 18시 17분에 실행됩니다.
- KST 기준으로는 대략 03:17, 09:17, 15:17, 21:17에 실행됩니다.

### 설계 결정
- 논문 큐레이션 사이트에는 매시간 업데이트보다 6시간 주기가 API 부담과 운영 안정성 면에서 적절하다고 판단했습니다.
- GitHub schedule은 특정 슬롯이 스킵될 수 있으므로, 너무 촘촘한 실행 여부를 UI에서 계속 확인하는 부담을 줄이는 방향을 택했습니다.

### 남은 작업
- 다음 15:17 KST 전후 scheduled run이 생성되는지 확인하면 좋습니다.

### 주의사항
- API key, token, secret은 기록하지 않았습니다.
- OpenAI API는 정기 업데이트에서 여전히 사용하지 않습니다.

## 2026-06-13 11:40

### 변경 요약
- 사용자가 업데이트가 됐는지, 밀렸는지, 실패했는지 직접 확인할 수 있는 Markdown 상태 파일을 요청했습니다.
- `UPDATE_STATUS.md`와 `data/update_status.json`을 추가하고, `Update papers` workflow가 성공/실패 여부와 관계없이 마지막에 상태 파일을 갱신하도록 구성했습니다.

### 수정/생성한 파일
- `scripts/write_update_status.py`: GitHub Actions 환경변수와 `data/site_meta.json`을 읽어 `UPDATE_STATUS.md`, `data/update_status.json`을 생성하는 스크립트를 추가했습니다.
- `.github/workflows/update-papers.yml`: `Update papers`, `Commit changed data`, `Deploy to GitHub Pages` 단계에 id를 부여하고, 마지막에 `Write update status` 및 `Commit update status` 단계를 추가했습니다.
- `UPDATE_STATUS.md`: 사용자가 바로 확인할 수 있는 공개 Markdown 상태 파일을 추가했습니다.
- `data/update_status.json`: 프론트엔드나 외부 도구가 읽을 수 있는 상태 JSON을 추가했습니다.
- `AGENT_LOG.md`: 상태 파일 도입 이유와 동작 방식을 기록했습니다.

### 구현한 기능
- workflow가 시작되어 끝까지 도달하면 성공/실패/스킵 여부가 `UPDATE_STATUS.md`에 기록됩니다.
- 마지막 성공 수집 시간, curated paper 수, raw candidate 수, archive 수, 마지막 성공 run의 추가 논문 수를 확인할 수 있습니다.
- GitHub schedule 자체가 생성되지 않은 경우에는 이 파일이 바뀌지 않으므로, “해당 슬롯이 스킵됐음”을 간접적으로 확인할 수 있습니다.

### 설계 결정
- 상태 파일은 데이터 변경 여부와 별개로 항상 별도 커밋되도록 구성했습니다.
- 사람이 바로 읽기 쉬운 Markdown과 기계가 읽기 쉬운 JSON을 함께 제공합니다.
- OpenAI 사용 여부는 상태 파일에 `disabled`로 명시했습니다.

### 남은 작업
- 다음 scheduled 또는 workflow_dispatch 실행 후 `UPDATE_STATUS.md`가 자동 갱신되는지 확인하면 좋습니다.

### 주의사항
- API key, token, secret은 기록하지 않았습니다.
- workflow가 GitHub에 의해 아예 생성되지 않은 경우에는 어떤 step도 실행되지 않으므로 상태 파일 역시 갱신되지 않습니다.

## 2026-06-13 02:30

### 변경 요약
- 헤더 영역은 다시 중앙 정렬로 돌리고, 저작권/요약 정책 안내 문구는 footer의 개발자/운영 정보 영역으로 이동했습니다.

### 수정/생성한 파일
- `index.html`: 헤더의 두 notice 문단을 제거하고 footer의 `developer-notes` 영역으로 이동했습니다. CSS/JS cache-busting 버전을 `20260613-0110`으로 갱신했습니다.
- `assets/style.css`: 헤더/venue nav 최종 중앙 정렬 override와 footer 개발자 노트 스타일을 추가했습니다.
- `AGENT_LOG.md`: 이번 헤더/푸터 정보 구조 변경을 기록했습니다.

### 구현한 기능
- 상단 첫 화면에는 제목, 부제, venue chip만 중앙 배치됩니다.
- 정책 문구는 페이지 하단 개발자/운영 정보 칸에서 확인할 수 있습니다.

### 설계 결정
- 기존 `.notice` 클래스를 footer로 이동해 한/영 전환 로직을 유지했습니다.
- 넓은 화면 레이아웃은 유지하되, hero 성격의 헤더만 중앙 정렬로 복원했습니다.

### 남은 작업
- footer 운영 정보가 너무 길어 보이면 접이식 details UI로 바꿀 수 있습니다.

### 주의사항
- API key, token, secret은 기록하지 않았습니다.
- 로컬에 남아 있는 `data/papers.json`, `data/site_meta.json` 변경은 이번 UI 커밋에 포함하지 않습니다.

## 2026-06-13 02:40

### 변경 요약
- 헤더 제목/부제/venue chip 블록이 wide layout 규칙에 의해 왼쪽으로 밀리는 문제를 수정했습니다.
- 파일 맨 끝에 absolute final header alignment override를 추가해 모든 화면 폭에서 헤더 블록을 중앙 정렬로 고정했습니다.

### 수정/생성한 파일
- `index.html`: CSS/JS cache-busting 버전을 `20260613-0120`으로 갱신했습니다.
- `assets/style.css`: `.site-header`, `.site-header .wide-shell`, `.venue-nav` 최종 중앙 정렬 override를 추가했습니다.
- `AGENT_LOG.md`: 이번 헤더 중앙 정렬 수정 기록을 추가했습니다.

### 구현한 기능
- `AI Manufacturing Research Tracker`, H1, subtitle, venue chip 전체가 중앙에 정렬됩니다.
- 큰 화면에서도 venue chip row가 `flex-start`로 돌아가지 않습니다.

### 설계 결정
- 기존 CSS에 여러 refinement layer가 있어 중간 위치의 규칙이 다시 덮였습니다. 따라서 이번 정렬은 파일 마지막에 배치했습니다.

### 남은 작업
- 없음.

### 주의사항
- API key, token, secret은 기록하지 않았습니다.
- 로컬에 남아 있는 `data/papers.json`, `data/site_meta.json` 변경은 이번 UI 커밋에 포함하지 않습니다.
## 2026-06-13 11:58

### 변경 요약
- 게재지 보드가 너무 복잡해 보인다는 피드백에 따라 core venue 이외의 모든 게재지를 `Others` 하나로 묶도록 단순화했습니다.
- 기존의 `10편 이상` 중간 노출 기준과 `270 venues` 같은 세부 venue 수 표시는 제거했습니다.

### 수정/생성한 파일
- `assets/app.js`: venue 보드 렌더링 기준을 `Core + Others`로 변경하고, `Others` 클릭 시 core가 아닌 모든 논문이 필터링되도록 수정했습니다.
- `index.html`: 브라우저 캐시가 이전 JavaScript를 사용하지 않도록 asset version을 갱신했습니다.
- `AGENT_LOG.md`: 이번 UI 기준 변경의 이유와 내용을 기록했습니다.

### 구현한 기능
- `Nature`, `Nature Communications`, `Nature Materials`, `Nature Reviews Materials`, `Science`, `Science Advances`, `Science Robotics`, `Additive Manufacturing` 같은 core venue만 개별 표시합니다.
- core venue가 아닌 모든 논문은 `Others` 카드에 논문 수만 표시합니다.
- `Others` 필터는 venue 수나 10편 이상 여부와 무관하게 모든 non-core venue 논문을 포함합니다.

### 설계 결정
- venue 목록은 탐색 UI이므로 너무 많은 세부 정보를 노출하기보다, 사용자가 바로 이해할 수 있는 `Core / Others` 구조를 우선했습니다.
- 세부 venue 수는 데이터 디버깅에는 유용하지만 일반 사용자 UI에서는 노이즈가 커서 숨겼습니다.

### 남은 작업
- 필요하면 추후 개발자용 하단 정보 또는 별도 JSON에서 non-core venue 개수를 확인할 수 있게 분리할 수 있습니다.

### 주의사항
- 이 변경은 표시/필터 UI 기준만 바꾸며 `data/papers.json`의 논문 데이터나 수집 파이프라인은 수정하지 않습니다.
- API key, token, secret은 기록하지 않았습니다.

## 2026-06-14 15:22

### Change Summary
- Raised relevance scores for broader manufacturing-focused digital twin papers that were still scored too low.
- Updated 113 current records with clear manufacturing/smart manufacturing/AM/robotics/process-optimization digital-twin signals from relevance score 5 to 7.

### Edited Files
- `scripts/summarize.py`: generated summaries now receive a minimum score of 7 whenever the source metadata matches the manufacturing digital twin rule, even if the exact curated `Digital Twins` tag is not present.
- `data/papers.json`: updated current manufacturing-focused digital twin records and score text to `7/10`.

### Design Notes
- This is a score calibration change, not a sidebar taxonomy expansion.
- The `Digital Twins` sidebar count still uses exact curated `Digital Twins` tags, while relevance scoring now recognizes broader in-scope manufacturing DT papers.

### Follow-up
- Review individual high-value manufacturing DT papers later if some should be promoted above 7.

## 2026-06-14 15:10

### Change Summary
- Raised relevance scoring for curated manufacturing-focused `Digital Twins` papers.
- Updated the 14 currently curated `Digital Twins` records from relevance score 5 to 7.

### Edited Files
- `scripts/summarize.py`: manufacturing-focused digital twin fallback/generated summaries now receive a minimum relevance score of 7.
- `data/papers.json`: updated current curated `Digital Twins` records and their score text from `5/10` to `7/10`.

### Design Notes
- After narrowing Digital Twins to curated manufacturing DT papers, the remaining set is intentionally closer to the tracker scope and should not sit at the lowest visible relevance tier.
- Generic/non-manufacturing digital twin papers remain excluded from the sidebar topic.

### Follow-up
- If some DT papers should be tiered higher than 7, review them individually after checking abstracts/full metadata.

## 2026-06-14 14:58

### Change Summary
- Fixed the visible `Digital Twins` sidebar count not changing after data cleanup.
- The sidebar and tag filter now count `Digital Twins` only when a paper has the exact curated `Digital Twins` tag, instead of counting every title-derived manufacturing digital-twin signal.

### Edited Files
- `assets/app.js`: made `Digital Twins` representative/sidebar/filter matching use `paperHasCuratedDigitalTwinTag()`.
- `index.html`: bumped the app script cache version for GitHub Pages.

### Design Notes
- The previous count stayed high because `deriveSubtopics()` inferred Digital Twins from titles and old metadata even after direct tag cleanup.
- This keeps broad title search available while making the sidebar topic count reflect curated DT membership.

### Follow-up
- If more DT papers should be included, add the exact `Digital Twins` tag during curation rather than relying on automatic title inference.

## 2026-06-14 14:42

### Change Summary
- Further narrowed `Digital Twins` to manufacturing-focused digital twins only.
- Removed `Digital Twins` tags from 7 more current papers that were urban, generic semantic modelling, logistics, pharma supply chain, AHU, or city-platform topics.

### Edited Files
- `assets/app.js`: requires both a digital-twin signal and a manufacturing/3D-printing/4D-printing/robotics/automation domain signal before showing or filtering `Digital Twins`.
- `scripts/summarize.py`: filters generated and fallback `Digital Twins` tags through the same manufacturing-focused rule.
- `scripts/update_papers.py`: rejects generic digital-twin candidates unless they also match the manufacturing-focused context.
- `data/papers.json`: reduced current direct `Digital Twins` tags from 21 to 14.
- `index.html`: bumped the app script cache version for GitHub Pages.

### Design Notes
- The intended scope is now production/manufacturing, 3D/4D printing, manufacturing automation, robotic manufacturing, and closely related industrial process digital twins.
- Generic city, mobility, healthcare/pharma, agriculture, indoor/AHU, and broad semantic digital-twin papers are no longer included under the Digital Twins topic.

### Follow-up
- Existing summary prose may still mention older Digital Twins reasoning until those records are regenerated.

## 2026-06-14 14:20

### Change Summary
- Audited and tightened the `Digital Twins` classification.
- Removed false-positive `Digital Twins` tags from 26 current papers that did not have an explicit digital-twin signal in title or venue.

### Edited Files
- `assets/app.js`: narrowed Digital Twins UI classification to explicit digital twin/twinning signals and stopped mapping `cyber-physical` alone to Digital Twins.
- `scripts/summarize.py`: removed the `cyber-physical` alias/keyword from Digital Twins tag generation.
- `scripts/update_papers.py`: stopped using `cyber-physical` alone as a digital-twin collection signal.
- `data/papers.json`: removed 26 false-positive `Digital Twins` tags.
- `index.html`: bumped the app script cache version for GitHub Pages.

### Design Notes
- Digital Twins is now treated as a narrower topic: `digital twin(s)`, `digital twinning`, `virtual twin`, `real-to-twin`, `twin-enabled`, `twin-driven`, `process twin`, or `machine twin`.
- Broad `cyber-physical` papers can still be relevant to manufacturing, but they are no longer automatically shown under Digital Twins.

## 2026-06-14 22:08

### Change Summary
- Changed the scheduled paper metadata update interval from every 6 hours to every 12 hours.

### Edited Files
- `.github/workflows/update-papers.yml`: changed the cron schedule from `17 */6 * * *` to `17 */12 * * *` and updated the status description passed to `scripts/write_update_status.py`.
- `AGENT_LOG.md`: recorded the schedule change.

### Operating Notes
- The workflow can still be run manually through `workflow_dispatch`.
- In KST, the scheduled runs are now approximately 09:17 and 21:17.
- This change does not affect OpenAI usage, paper data, summaries, or GitHub Pages UI.

### Follow-up
- None.

## 2026-06-14 21:55

### Change Summary
- Added an explicit operations and copyright policy for the paper tracker.
- Strengthened the OpenAI summary prompt so English summaries must avoid close paraphrase of publisher/OpenAlex abstract wording, not only verbatim copying.
- Linked the new policy document from `README.md`.

### Edited Files
- `OPERATIONS_POLICY.md`: new operating policy covering data sources, update workflow, OpenAI usage, public repository rules, and abstract copyright safety.
- `scripts/summarize.py`: added stronger instructions against abstract sentence order reuse, long noun-phrase reuse, and 8+ word overlap in `ai_summary_en`.
- `README.md`: added a pointer to the new operations/copyright policy.
- `AGENT_LOG.md`: recorded this policy update.

### Audit Context
- Local audit found no stored raw abstract field in current `data/papers.json` or `data/archive_papers.json`.
- All checked records had `raw_abstract_displayed=false` and `pdf_stored=false`.
- A sample comparison against OpenAlex abstracts found that some existing `ai_summary_en` entries share long technical phrases with abstracts, so future summaries must be treated under a stricter close-paraphrase policy.

### Operating Rule
- Copyright safety is not only "do not store abstracts." AI summaries, especially English summaries, must be newly synthesized and should not closely follow publisher abstract wording, sentence order, or long phrase chains.
- Existing high-overlap English summaries should be considered candidates for selective rewrite or temporary conservative fallback if the site is hardened further.

### Follow-up
- Add an automated summary-overlap audit before future bulk OpenAI refreshes.
- Consider selectively regenerating existing `ai_summary_en` entries with high abstract overlap.

### Follow-up
- If needed, rerun OpenAI summaries later for the cleaned papers so old summary text no longer mentions Digital Twins in the narrative.

## 2026-06-14 10:10

### Change Summary
- Added `Multi-material AM` to the Production / Manufacturing sidebar subtopics.

### Edited Files
- `assets/app.js`: updated `FIELD_SUBTOPICS["생산/제조"]` to include the existing `MMAM` canonical tag.
- `index.html`: bumped the app script cache version for GitHub Pages.

### Design Notes
- Reused the existing `MMAM` canonical tag so the displayed Korean/English labels and filtering behavior stay consistent.

### Follow-up
- None.

## 2026-06-14 10:02

### Change Summary
- Added `Functionally Graded AM` and `Additive Manufacturing` to the 3D Printing sidebar subtopics.

### Edited Files
- `assets/app.js`: updated `FIELD_SUBTOPICS["3D 프린팅"]` to include `Additive manufacturing` and `FGAM`.
- `index.html`: bumped the app script cache version for GitHub Pages.

### Design Notes
- Reused the existing canonical tags and labels, so Korean/English display names and filtering remain consistent with the current taxonomy.

### Follow-up
- None.

## 2026-06-14 09:53

### Change Summary
- Added a browser tab favicon for the GitHub Pages site.

### Edited Files
- `assets/favicon.svg`: new compact research/manufacturing themed SVG icon.
- `index.html`: linked the SVG favicon in the document head.

### Design Notes
- Used an SVG favicon so it remains crisp across browser tab and bookmark sizes without adding multiple raster assets.

### Follow-up
- None.

## 2026-06-14 09:47

### Change Summary
- Made the Papers stat delta line more explicit so the user can tell which number is from the latest update and which is weekly.

### Edited Files
- `assets/app.js`: changed the compact stat note to labels such as `이번 업데이트 +20 · 주간 신규 +793`.
- `index.html`: bumped asset cache versions for GitHub Pages.

### Design Notes
- Kept the weekly amount inside the Papers card instead of restoring a separate stat card, avoiding another large `793` tile while preserving the weekly count.

### Follow-up
- None.

## 2026-06-14 09:40

### Change Summary
- Simplified the headline stats panel after the weekly-added count duplicated the total paper count.
- Removed the separate "recent 7 days" stats card and folded new-paper deltas into the Papers card.

### Edited Files
- `index.html`: removed the weekly stats card and bumped asset cache versions.
- `assets/app.js`: renders latest-run and weekly deltas as a compact note under the total paper count; hides the weekly count when it equals the total.
- `assets/style.css`: restored the stats grid to four cards.

### Design Notes
- The current dataset has all 793 papers within the weekly window, so showing another 793 was visually redundant.
- The Papers card now shows the total as the primary number, with a small delta line such as `recent run +20`; weekly additions appear only when they add useful information.

### Follow-up
- None.
# 2026-06-16 09:41
## 변경 요약
- 논문 업데이트 시간을 KST 10:17/22:17, 즉 12시간 주기로 변경했습니다.
- 업데이트가 실행 중일 때 사이트 상단 `Now / Updated` 패널에서 `updating now`/`업데이트 중` 상태를 볼 수 있도록 했습니다.
- 마지막 시도가 실패 또는 취소된 경우에도 같은 패널에서 `last attempt failed/cancelled`를 볼 수 있도록 했습니다.

## 수정/생성한 파일
- `.github/workflows/update-papers.yml`: cron을 `17 1,13 * * *`로 변경했고, workflow 시작 직후 `UPDATE_STATUS.md`와 `data/update_status.json`을 `in_progress` 상태로 먼저 커밋하는 step을 추가했습니다.
- `scripts/write_update_status.py`: 새 cron의 KST 표시를 `10:17`, `22:17`로 바꾸고 `update_phase` 필드를 기록하도록 수정했습니다.
- `assets/app.js`: `data/update_status.json`을 읽고, `Now / Updated` 패널에 업데이트 진행/실패/취소/확인 상태를 표시하도록 수정했습니다.
- `index.html`: GitHub Pages 캐시 무효화를 위해 `assets/app.js` query version을 `20260616-0100`으로 갱신했습니다.
- `AGENT_LOG.md`: 이번 변경 사항과 설계 결정을 기록했습니다.

## 구현한 기능
- scheduled update가 시작되면 긴 수집 작업이 끝나기 전에도 사이트가 `업데이트 중` 상태를 표시할 수 있습니다.
- update가 실패하거나 취소되면 사용자는 마지막 성공 수집 시간과 마지막 시도 상태를 동시에 볼 수 있습니다.
- `Now / Updated` 패널은 현재 시각, 마지막 성공 수집 시각, 마지막 update attempt 상태를 함께 표시합니다.

## 설계 결정
- `UPDATE_STATUS.md`와 `data/update_status.json`은 Actions가 실제 상태를 기록하는 파일로 유지합니다. 로컬에서 성공 상태를 수동으로 조작하지 않았습니다.
- workflow 시작 상태를 별도 커밋으로 먼저 push합니다. 정적 GitHub Pages 사이트는 서버 실시간 상태를 직접 볼 수 없으므로, 공개 JSON 파일을 갱신하는 방식이 가장 단순하고 투명합니다.
- OpenAI scheduled update는 계속 비활성화되어 있습니다.

## 검증 결과
- 현재 `data/update_status.json` 기준 표시 예상: `last attempt cancelled`
- `scripts/write_update_status.py` 문법 검증 통과
- `data/update_status.json` JSON 검증 통과
- `git diff --check` 통과

## 남은 작업
- 다음 10:17 또는 22:17 KST scheduled run에서 사이트가 `updating now`를 표시하는지 확인합니다.
- run 종료 후 `UPDATE_STATUS.md`와 `data/update_status.json`이 success/failure/cancelled 상태로 다시 갱신되는지 확인합니다.

## 주의사항
- OpenAI API는 사용하지 않았습니다.
- 논문 데이터 파일은 수정하지 않았습니다.
- raw abstract 또는 PDF 저장/표시는 하지 않았습니다.

# 2026-06-16 09:37
## 변경 요약
- 정기 논문 업데이트가 누락됐는지 확인했습니다.
- `UPDATE_STATUS.md`와 GitHub Actions run `27564111702` 확인 결과, 2026-06-16 03:27 KST에 체크된 scheduled run이 `cancelled` 상태였습니다.
- 원인은 논문 업데이트 job이 기존 `timeout-minutes: 60` 제한을 초과했기 때문입니다.

## 수정/생성한 파일
- `.github/workflows/update-papers.yml`: `Update papers` job timeout을 60분에서 180분으로 늘렸습니다.
- `AGENT_LOG.md`: 이번 원인 분석과 변경 사항을 기록했습니다.

## 구현한 기능
- 12시간 주기 업데이트가 검색어/target venue 검색량 때문에 1시간을 넘겨도 중간 취소되지 않도록 했습니다.

## 설계 결정
- 현재 검색어가 60개 이상이고 OpenAlex/Crossref 및 target venue 검색을 수행하므로, 60분 제한은 안정적인 정기 업데이트에 부족하다고 판단했습니다.
- API 호출량을 즉시 줄이지 않고 timeout을 180분으로 늘렸습니다. 사용자가 원한 것은 주기적인 누락 없는 업데이트이며, OpenAI API는 scheduled update에서 계속 비활성화되어 있으므로 비용 증가는 없습니다.
- `UPDATE_STATUS.md`는 Actions가 쓰는 상태 파일이므로 로컬에서 성공 상태로 조작하지 않았습니다.

## 남은 작업
- 다음 scheduled run 또는 수동 `workflow_dispatch` 실행 후 `UPDATE_STATUS.md`가 `success`로 갱신되는지 확인해야 합니다.
- 업데이트 시간이 여전히 길면 target venue 검색을 더 효율화하거나 query batch를 나누는 개선이 필요합니다.

## 주의사항
- OpenAI API는 사용하지 않았습니다.
- 논문 데이터 파일은 수정하지 않았습니다.
- raw abstract 또는 PDF 저장/표시는 하지 않았습니다.

# 2026-06-15 15:27
## 변경 요약
- `DLP` 안에 `SLA`, `vat photopolymerization`, `stereolithography`가 섞여 있던 문제를 분리했습니다.
- 논문별 태그가 한글/영문/약어로 흔들리던 문제를 전체 점검하고 핵심 canonical tag로 정규화했습니다.
- `SLA`는 `SLAM`, `translaminar`, `translation` 같은 단어에 잘못 걸리지 않도록 단어 경계 기반으로만 판정하도록 했습니다.

## 수정/생성한 파일
- `assets/app.js`: 3D Printing 하위 토픽에 `SLA`, `Vat photopolymerization`을 추가하고, `DLP` 표시명을 `Digital Light Processing (DLP)`로 바꿨습니다. DLP/SLA/vat 판정 로직도 분리했습니다.
- `scripts/summarize.py`: 새 논문 요약/분류 시 `DLP`, `SLA`, `Vat photopolymerization`이 분리 저장되도록 TAG_MAP과 alias를 보강했습니다.
- `data/papers.json`: 기존 873편의 태그를 전체 점검해 핵심 alias를 canonical tag로 통합했습니다.
- `index.html`: GitHub Pages 캐시 무효화를 위해 `assets/app.js` query version을 `20260615-0140`으로 갱신했습니다.
- `AGENT_LOG.md`: 이번 변경 사항과 검증 결과를 기록했습니다.
- `PROJECT_STATUS.md`: 현재 태그 정책을 갱신했습니다.

## 구현한 기능
- `DLP`는 `digital light process`, `digital light processing`, `digital light projection`, `DLP` 신호만 사용합니다.
- `SLA`는 `stereolithography`, `stereo lithography`, 독립 약어 `SLA`만 사용합니다.
- `Vat photopolymerization`은 `vat photopolymerization/photopolymerisation/polymerization/polymerisation` 명시 신호만 사용합니다.
- `적층 제조`, `디지털 트윈`, `4D 프린팅`, `머신러닝`, `소프트 로봇`, `복합재료`, `액정 엘라스토머` 등 흔들리던 태그를 canonical tag로 통합했습니다.
- 너무 넓거나 의미가 약한 `재료 과학`, `제조 기술`, `기술 발전`, `응용`, `제조`, `제조업`, `효율성`, `혁신` 태그는 카드/필터용 태그에서 제거했습니다.

## 검증 결과
- 현재 논문 수: 873편
- `data/papers.json` JSON 검증 통과
- `scripts/summarize.py` 문법 검증 통과
- `git diff --check` 통과
- 정규화 후 주요 태그 카운트:
  - Additive manufacturing: 431
  - Digital Twins: 161
  - 4D printing: 105
  - MMAM: 97
  - Soft robotics: 87
  - Machine learning: 86
  - DLP: 24
  - SLA: 3
  - Vat photopolymerization: 8
- 수정 후 로컬 데이터 기준 예상 3D Printing 하위 카운트:
  - Multi-material AM: 81
  - Functionally Graded AM: 20
  - Volumetric AM: 54
  - Digital Light Processing (DLP): 11
  - Stereolithography (SLA): 3
  - Vat Photopolymerization: 2
  - FDM: 18
  - Toolpath Strategy: 15
  - Material Switching: 2
  - Additive Manufacturing: 89
  - Others: 1

## 설계 결정
- `DLP`, `SLA`, `Vat photopolymerization`은 서로 관련된 vat photopolymerization 계열이지만, UI에서는 사용자가 공정별로 볼 수 있도록 분리했습니다.
- `SLA`는 짧은 약어라 substring matching을 쓰지 않고 정규식 단어 경계를 사용합니다.
- `photopolymerization`이라는 일반 단어만으로는 DLP나 vat로 분류하지 않습니다. 명시적인 `vat photopolymerization` 또는 DLP/SLA 신호가 있을 때만 해당 태그를 붙입니다.
- 데이터 태그는 최대 6개 제한을 유지하고, canonical topic을 우선 배치했습니다.

## 남은 작업
- GitHub Pages 반영 후 왼쪽 패널에서 DLP/SLA/Vat photopolymerization이 분리되어 보이는지 확인합니다.
- 아직 남아 있는 일부 한글 세부 태그(`스마트 재료`, `로봇 공학`, `경로 계획` 등)는 필요하면 다음 라운드에서 canonical tag로 더 통합할 수 있습니다.

## 주의사항
- OpenAI API는 사용하지 않았습니다.
- raw abstract 또는 PDF 저장/표시는 하지 않았습니다.
- 이번 변경은 기존 논문 텍스트/요약이 아니라 태그 정규화와 프론트엔드 분류 규칙 변경입니다.

# 2026-06-15 15:20
## 변경 요약
- 사용자가 다시 확인한 `3D Printing > Multi-material AM 286` 과카운트 문제를 재조사했습니다.
- 실제 원인은 `categories`였습니다. 현재 데이터에서 `다중재료 적층제조` category가 690편에 붙어 있어, sidebar subtopic 판정에 category를 사용하면 거의 모든 3D Printing 논문이 `MMAM`으로 먼저 배정되었습니다.
- sidebar subtopic 판정에서 categories를 제외하고, 제목/venue/실제 tags만 사용하도록 수정했습니다.

## 수정/생성한 파일
- `assets/app.js`: `paperHasRepresentativeTopic()`, `deriveSubtopics()`, `collapseMaterialExtrusionTags()`에서 category 기반 subtopic 판정을 제거했습니다.
- `index.html`: GitHub Pages 캐시 무효화를 위해 `assets/app.js` query version을 `20260615-0130`으로 갱신했습니다.
- `AGENT_LOG.md`: 이번 진짜 원인과 수정 기준을 기록했습니다.
- `PROJECT_STATUS.md`: sidebar count 정책을 갱신했습니다.

## 구현한 기능
- `다중재료 적층제조` 같은 broad category가 `MMAM` 하위 버킷을 과점하지 않도록 했습니다.
- 3D Printing 하위 토픽 카운트가 실제 제목/venue/tags 기반으로 분산되도록 했습니다.

## 검증 결과
- 수정 후 로컬 데이터 기준 예상 3D Printing 하위 카운트:
  - Multi-material AM: 81
  - Functionally Graded AM: 19
  - Volumetric AM: 54
  - DLP: 16
  - FDM: 18
  - Toolpath Strategy: 12
  - Material Switching: 2
  - Additive Manufacturing: 94
  - Others: 1
- `python -m json.tool data/papers.json` 통과
- `git diff --check` 통과

## 설계 결정
- categories는 broad curation label로 보고, sidebar의 세부 subtopic bucket 근거에서는 제외합니다.
- sidebar subtopic count는 제목, venue, canonical tags만 사용합니다.
- categories는 paper card metadata와 broad filtering/context에는 남길 수 있지만, 세부 topic count를 결정하면 과카운트가 발생합니다.

## 남은 작업
- GitHub Pages 반영 후 사용자가 보던 `Multi-material AM 286`이 `81` 전후로 내려오는지 확인합니다.

## 주의사항
- OpenAI API는 사용하지 않았습니다.
- data file은 수정하지 않았습니다.
- raw abstract 또는 PDF 저장/표시는 하지 않았습니다.

# 2026-06-15 15:17
## 변경 요약
- 3D Printing 하위에서 `Multi-material AM`이 288편으로 과도하게 카운팅되고, `FDM`, `Additive Manufacturing` 등이 0으로 보이는 문제를 조사했습니다.
- 원인은 프론트엔드의 `deriveSubtopics()`와 material-extrusion 대표 태그 선택 로직이 `ai_summary_ko`, `relevance_note_ko`까지 분류 근거로 사용했기 때문이었습니다.
- 요약/관련성 문장은 설명용 텍스트이므로, sidebar bucket 및 대표 태그 판정에서 제외했습니다.

## 수정/생성한 파일
- `assets/app.js`: `deriveSubtopics()`와 `collapseMaterialExtrusionTags()`가 제목, venue, 실제 tags, categories만 사용하도록 수정했습니다.
- `index.html`: GitHub Pages 캐시 무효화를 위해 `assets/app.js` query version을 `20260615-0120`으로 갱신했습니다.
- `AGENT_LOG.md`: 이번 원인 분석과 수정 기준을 기록했습니다.

## 구현한 기능
- 요약문에 `MMAM 관점`, `다중재료 트래커` 같은 문구가 있어도 그것만으로 MMAM 서브토픽에 들어가지 않도록 했습니다.
- 3D Printing 하위 토픽 카운트가 실제 메타데이터/태그 기반으로 분산되도록 했습니다.

## 검증 결과
- 수정 후 로컬 데이터 기준 예상 3D Printing 하위 카운트:
  - Multi-material AM: 81
  - Functionally Graded AM: 19
  - Volumetric AM: 54
  - DLP: 16
  - FDM: 18
  - Toolpath Strategy: 12
  - Material Switching: 2
  - Additive Manufacturing: 94
  - Others: 1
- `python -m py_compile scripts/summarize.py` 통과
- `python -m json.tool data/papers.json` 통과
- `git diff --check` 통과

## 설계 결정
- 논문 요약과 관련성 설명은 사용자에게 보여주는 해석 텍스트이며, 카운트/필터링의 1차 근거로 쓰지 않습니다.
- 카운트/필터링은 제목, venue, canonical tags, categories 같은 안정적인 메타데이터 기반 신호로 제한합니다.

## 남은 작업
- GitHub Pages 반영 후 왼쪽 패널의 3D Printing 하위 카운트가 위 예상치와 비슷하게 보이는지 확인합니다.

## 주의사항
- OpenAI API는 사용하지 않았습니다.
- raw abstract 또는 PDF 저장/표시는 하지 않았습니다.
- 데이터 파일은 이번 수정에서 변경하지 않았습니다.

# 2026-06-15 15:13
## 변경 요약
- `MMAM` 서브토픽 카운트가 원본 `tags`에 `MMAM`이 없는 논문까지 포함하는 이유를 검증했습니다.
- 원인은 왼쪽 패널이 raw tag count가 아니라 제목/메타데이터 기반 파생 topic count를 사용하기 때문이었습니다.
- 사용자 혼선을 줄이기 위해, 제목/메타데이터에 명시적으로 `multi-material`, `multimaterial`, `multi material` 신호가 있는 기존 논문에는 `MMAM` canonical tag를 데이터에 추가했습니다.

## 수정/생성한 파일
- `data/papers.json`: 100편의 태그를 정규화했습니다. `MMAM` 86건, `Volumetric AM` 7건, `Soft robotics` 12건을 명시적 메타데이터 신호 기반으로 보강했고 일부 alias를 canonical tag로 통합했습니다.
- `scripts/summarize.py`: 향후 OpenAI/fallback 요약 결과에서 `Multi-material AM`, `Multimaterial`, `multi-material` 등이 다시 분산되지 않도록 `MMAM` alias를 추가했습니다.
- `AGENT_LOG.md`: 이번 검증과 정규화 기준을 기록했습니다.

## 구현한 기능
- MMAM 서브토픽에 잡히는 논문은 데이터의 `tags`에도 `MMAM`이 들어가도록 맞췄습니다.
- 기존 논문 중 메타데이터상 MMAM 신호가 있는데 `MMAM` 태그가 없는 항목은 0건으로 정리되었습니다.
- JSON schema 및 저작권 정책 필드(`raw_abstract_displayed=false`, `pdf_stored=false`)를 유지했습니다.

## 설계 결정
- `MMAM`을 삭제하지 않았습니다. 제목에 `multi-material` 또는 `multimaterial`이 명시된 논문은 이 트래커의 핵심 축과 직접 연결되므로 유지 가치가 높다고 판단했습니다.
- 다만 raw tag와 topic count가 다르게 보이는 혼선을 줄이기 위해 데이터 태그를 canonical topic과 일치시켰습니다.
- 태그는 최대 6개 제한을 유지했습니다.

## 검증 결과
- 현재 논문 수: 873편
- `MMAM` 태그 보유 논문: 97편
- 제목/메타데이터에 MMAM 신호가 있으나 `MMAM` 태그가 없는 논문: 0편
- `python -m json.tool data/papers.json` 통과
- `python -m py_compile scripts/summarize.py` 통과
- `git diff --check` 통과

## 남은 작업
- GitHub Pages 반영 후 MMAM 서브토픽 카운트와 논문 카드 태그가 직관적으로 일치하는지 화면에서 확인합니다.
- 필요하면 `Additive Manufacturing`, `적층 제조`, `디지털 트윈` 등 다른 broad/alias 태그도 같은 방식으로 데이터 레벨에서 추가 정규화할 수 있습니다.

## 주의사항
- OpenAI API는 사용하지 않았습니다.
- raw abstract 또는 PDF 저장/표시는 하지 않았습니다.

# 2026-06-15 15:08
## 변경 요약
- 논문 카드에 표시되는 대표 태그가 너무 넓거나 중복되는 문제를 정리했습니다.
- `Deep Learning`, `Reinforcement Learning`, `딥러닝`, `강화 학습` 등은 이 트래커 관점에서 `Machine Learning`으로 통합했습니다.
- `소프트 로봇`, `소프트 액추에이터`, `Soft Robotics` 등은 `Soft robotics`로 통합했습니다.

## 수정/생성한 파일
- `assets/app.js`: 대표 태그 우선순위와 low-signal 태그 목록을 추가하고, 카드 표시 태그 정렬/선택 로직을 개선했습니다.
- `scripts/summarize.py`: 정기 업데이트 및 수동 요약 정규화에서 중복 AI/soft robotics 태그가 다시 생기지 않도록 alias를 보강했습니다.
- `index.html`: GitHub Pages 캐시 무효화를 위해 `assets/app.js` query version을 `20260615-0110`으로 갱신했습니다.
- `AGENT_LOG.md`: 이번 태그 정리 기준과 주의사항을 기록했습니다.

## 구현한 기능
- 논문 카드 대표 3개 태그에서 `Additive Manufacturing`, `Review`, `Sustainability`, `Digital fabrication`, `Material behavior`, `Reusability` 같은 low-signal 태그는 구체 태그가 충분할 때 뒤로 밀리도록 했습니다.
- 핵심 토픽인 `MMAM`, `FGAM`, `Volumetric AM`, `Soft robotics`, `LCE`, `Digital Twins`, `Self-driving Labs`가 카드 태그에서 우선적으로 보이도록 했습니다.
- `Deep Learning`과 `Reinforcement Learning`은 별도 대표 태그로 분산되지 않고 `Machine Learning`으로 합쳐지도록 했습니다.
- soft robotics 계열 한글/영문 표현이 `Soft robotics` canonical tag로 합쳐지도록 했습니다.

## 설계 결정
- broad tag를 완전히 삭제하지 않고 카드 표시에서만 후순위로 두었습니다. 필터나 broad bucket 용도로는 여전히 쓸 수 있기 때문입니다.
- 한 논문당 대표 태그는 계속 3개만 표시합니다. 긴 태그 나열은 사용자가 논문의 핵심을 파악하는 데 오히려 방해된다고 판단했습니다.
- `Deep Learning`, `Reinforcement Learning`은 발표/문헌 추적 수준에서는 `Machine Learning` 하위 표현으로 충분하다고 판단했습니다.

## 남은 작업
- 실제 GitHub Pages 반영 후 논문 카드에서 broad 태그가 과도하게 보이지 않는지 화면 확인이 필요합니다.
- 필요하면 `Sustainability`나 `Review`를 완전히 숨길지, 또는 venue/field에 따라 조건부로 보일지 추가 조정할 수 있습니다.

## 주의사항
- OpenAI API는 사용하지 않았습니다.
- 논문 데이터 파일은 수정하지 않았고, 표시/정규화 규칙만 수정했습니다.
- raw abstract 또는 PDF 저장/표시는 하지 않았습니다.

# 2026-06-15 15:00
## 변경 요약
- 왼쪽 패널의 분야 내부 서브토픽 구성이 현재 873편 데이터에 적절한지 검증했습니다.
- 새로 수집 범위에 들어온 `Volumetric AM`, `Soft robotics` 논문들이 기존 서브토픽 구조에서 `Others` 또는 다른 분야로 묻히는 문제를 수정했습니다.
- broad topic이 세부 topic을 먼저 잡아먹지 않도록 왼쪽 패널의 서브토픽 순서를 재정렬했습니다.

## 수정/생성한 파일
- `assets/app.js`: 분야별 서브토픽 목록, 태그 라벨, canonical alias, 프론트엔드 분야/서브토픽 파생 규칙을 보정했습니다.
- `index.html`: GitHub Pages 캐시 무효화를 위해 `assets/app.js` query version을 `20260615-0100`으로 갱신했습니다.
- `AGENT_LOG.md`: 이번 검증과 설계 결정을 기록했습니다.
- `PROJECT_STATUS.md`: 현재 taxonomy 상태와 남은 점검 포인트를 갱신했습니다.

## 구현한 기능
- `Volumetric AM`을 3D 프린팅 분야의 공식 서브토픽으로 추가했습니다.
- `Soft robotics`를 로봇틱스(생산제조) 분야의 공식 서브토픽으로 추가했습니다.
- `additive manufacturing`만 포함된 volumetric AM 논문이 생산/제조로 빠지지 않고 3D 프린팅으로 분류되도록 했습니다.
- soft robotic finger/gripper/fin-ray/pneumatic actuator 논문이 topology optimization 등의 단어 때문에 AI 생산제조로 먼저 빠지지 않도록 분류 우선순위를 조정했습니다.
- 3D 프린팅 서브토픽은 `MMAM`, `FGAM`, `Volumetric AM`, `DLP`, `FDM`, `Toolpath`, `Material Switching`을 먼저 보여주고, broad fallback인 `Additive Manufacturing`은 뒤로 보냈습니다.

## 설계 결정
- 왼쪽 패널 카운트는 한 논문을 여러 서브토픽에 중복 집계하지 않고, 분야 안에서 처음 매칭되는 하나의 bucket에 넣는 구조를 유지했습니다. 총합이 분야 논문수와 맞아야 사용자가 이해하기 쉽기 때문입니다.
- 따라서 broad label은 뒤에 두고, 세부적인 연구 축을 앞에 두는 방식이 적절하다고 판단했습니다.
- `MMAM`은 생산/제조보다는 3D 프린팅의 세부 축으로 보는 것이 더 자연스러워 3D 프린팅 쪽으로 이동했습니다.
- `Manufacturing Automation`은 로봇틱스와 AI 생산제조 양쪽에 남겼지만, 로봇틱스에서는 `Soft robotics` 다음에 배치해 자동화 성격의 로봇 논문이 0으로 보이지 않도록 했습니다.

## 검증 결과
- 로컬 데이터 기준 총 논문 수는 873편입니다.
- 변경 후 예상 분야별 집계:
  - Production / Manufacturing: 140
  - 3D Printing: 297
  - 4D Printing: 130
  - Robotics for Manufacturing: 97
  - AI Manufacturing: 209
- `Volumetric AM` 태그 논문 52편은 모두 3D Printing 분야로 배치됩니다.
- `Soft robotics` 태그 논문 50편 중 대부분은 Robotics for Manufacturing으로 배치되며, 일부는 4D/AI/AM 키워드 우선순위 때문에 다른 분야에 남습니다.
- `AI Manufacturing`의 `Others`가 여전히 큰데, 이는 한국어 태그/요약 기반 AI 신호와 기존 digital twin 보수 분류 정책이 섞인 결과입니다. 다음 개선 시 AI 서브토픽을 더 세분화할 수 있습니다.

## 남은 작업
- 브라우저 자동화 도구와 `node`가 현재 환경에서 사용 가능하지 않아 실제 화면 렌더링/JS 문법 체크는 수행하지 못했습니다.
- GitHub Pages 반영 후 왼쪽 패널에서 `Volumetric AM`, `Soft Robotics`, `Manufacturing Automation` 카운트가 의도대로 보이는지 화면에서 확인해야 합니다.
- AI 생산제조의 `Others`가 큰 원인을 별도 샘플링해 `AI process monitoring`, `Physics-informed ML`, `Quality prediction` 같은 하위 토픽을 추가할지 결정할 수 있습니다.

## 주의사항
- OpenAI API는 사용하지 않았습니다.
- 데이터 파일은 수정하지 않았고, 프론트엔드 분류/표시 규칙만 수정했습니다.
- `index.html`의 app script version은 브라우저/GitHub Pages 캐시가 이전 taxonomy 로직을 계속 사용하는 상황을 막기 위한 변경입니다.
- raw abstract 또는 PDF 저장/표시는 하지 않았습니다.
- OpenAI API는 사용하지 않았습니다.

## 2026-06-17 11:51
### 변경 요약
- OpenAlex / Crossref source overlap 결과를 Excel에서 바로 볼 수 있도록 별도 통합 워크북을 생성했습니다.
- 사용자가 요청한 `only_OpenAlex`, `only_Crossref`, `both` 구분을 후보 레코드, 중복 제거 논문, 게재지 단위로 각각 분리했습니다.

### 수정/생성한 파일
- `reports/source_overlap_openalex_crossref_groups.xlsx`: `Summary`, `Records_*`, `Papers_*`, `Venues_*` 시트로 구성된 Excel 보고서를 생성했습니다.
- `AGENT_LOG.md`: 이번 보고서 생성 작업과 검증 결과를 기록했습니다.

### 구현한 기능
- `Records_OpenAlex_only`, `Records_Crossref_only`, `Records_Both`: 전체 3,075개 collected candidate 기준 source 구분을 제공합니다.
- `Papers_OpenAlex_only`, `Papers_Crossref_only`, `Papers_Both`: DOI 우선, DOI가 없으면 normalized title 기준으로 중복 제거한 논문 단위 source 구분을 제공합니다.
- `Venues_OpenAlex_only`, `Venues_Crossref_only`, `Venues_Both`: venue/journal/proceedings 단위 source 구분을 제공합니다.
- 각 시트에 필터 가능한 Excel table, freeze pane, 기본 열 너비, 요약 시트를 추가했습니다.

### 설계 결정
- `OpenAlex only`와 `Crossref only`는 전 세계 API coverage의 절대적 부재가 아니라, 현재 수집 파이프라인과 3,075개 후보 데이터셋에서 어느 source로 관측되었는지를 뜻하도록 Summary 시트에 명시했습니다.
- 전체 후보 기준과 실제 논문 단위 기준을 혼동하지 않도록 `Records`와 `Papers`를 별도 시트로 나누었습니다.
- 기존 CSV 보고서를 근거 데이터로 사용했고, API를 새로 호출하지 않았습니다.

### 남은 작업
- 필요하면 `OpenAlex only venue` 중 Crossref exact match가 있는 항목을 DOI-level Crossref enrichment로 보강하는 후속 파이프라인을 만들 수 있습니다.
- Crossref-only 운영으로 전환할 경우, core manufacturing venue list와 Crossref ISSN 기반 수집 규칙을 별도 설계해야 합니다.

### 주의사항
- OpenAI API는 사용하지 않았습니다.
- API key, secret, token은 기록하지 않았습니다.
- `reports/~$openalex_only_venues_crossref_check.xlsx`는 Excel이 만든 임시 잠금 파일로 보이며 이번 작업에서는 수정하지 않았습니다.

## 2026-06-17 12:02
### 변경 요약
- 사용자가 실제로 원한 대상인 `OpenAlex-only venues with no Crossref journal match`만 따로 볼 수 있는 Excel 보고서를 생성했습니다.
- 이전 source grouping workbook과 달리, 이번 파일은 Crossref journal lookup 결과가 `no_crossref_journal_match`인 93개 venue만 분리합니다.

### 수정/생성한 파일
- `reports/openalex_only_venues_no_crossref_journal_match.xlsx`: OpenAlex-only venue 중 Crossref journal match가 없는 93개 항목 전용 Excel 보고서를 생성했습니다.
- `AGENT_LOG.md`: 이번 subset 보고서 생성 작업과 검증 결과를 기록했습니다.

### 구현한 기능
- `Summary` 시트에 OpenAlex-only venue 428개 중 exact match 332개, possible match 3개, no match 93개라는 핵심 수치를 정리했습니다.
- `No_Crossref_Journal_Match` 시트에 원본 lookup CSV의 전체 열을 보존한 상세 목록을 넣었습니다.
- `Top_No_Match_Compact` 시트에 venue, record count, curated/archive count, example titles 중심의 읽기 쉬운 목록을 추가했습니다.

### 설계 결정
- 이 파일은 API coverage 자체의 전역 진실을 증명하는 목적이 아니라, 현재 프로젝트의 collected dataset에서 OpenAlex-only로 관측되고 Crossref journal endpoint에서 journal title match가 없던 venue를 빠르게 검토하기 위한 목적입니다.
- repository, preprint server, institutional source, conference/proceedings 성격의 source title을 Crossref-centered 운영에서 제거하거나 별도 그룹화할 후보로 보기 쉽게 만들었습니다.

### 남은 작업
- 93개 no-match venue 중 실제로 유지할 가치가 있는 proceedings/preprint source와 제거할 noisy source를 수동 정책으로 나눌 수 있습니다.
- Crossref-centered pipeline으로 전환할 경우 이 목록을 exclusion 또는 low-priority venue rule의 근거로 사용할 수 있습니다.

### 주의사항
- OpenAI API는 사용하지 않았습니다.
- 새 API 호출 없이 기존 `reports/openalex_only_venues_crossref_check.csv`를 기반으로 생성했습니다.
- API key, secret, token은 기록하지 않았습니다.

## 2026-06-17 12:03
### 변경 요약
- `openalex_only_venues_no_crossref_journal_match.xlsx`에서 `Top_No_Match_Compact`라는 오해 소지가 있는 시트명을 제거했습니다.
- compact 시트가 top-N 샘플이 아니라 93개 전체 목록임을 명확히 했습니다.

### 수정/생성한 파일
- `reports/openalex_only_venues_no_crossref_journal_match.xlsx`: `Top_No_Match_Compact`를 `All_No_Match_Compact`로 변경하고 Summary 설명을 보강했습니다.
- `AGENT_LOG.md`: 시트명 변경과 검증 결과를 기록했습니다.

### 구현한 기능
- `No_Crossref_Journal_Match`와 `All_No_Match_Compact` 모두 Crossref journal match가 없는 93개 venue 전체를 표시합니다.

### 설계 결정
- 사용자가 “top”이 아니라 전체 목록을 원했기 때문에, 시트명과 설명에서 top/sample 뉘앙스를 제거했습니다.

### 남은 작업
- 필요하면 93개 전체 항목을 repository/preprint/proceedings/institutional/noisy-source로 수동 분류하는 별도 검토 시트를 추가할 수 있습니다.

### 주의사항
- OpenAI API는 사용하지 않았습니다.
- 새 API 호출 없이 기존 Excel 파일의 시트명과 설명만 수정했습니다.

## 2026-06-17 12:14
### 변경 요약
- Crossref-only venue에 대해 OpenAlex source lookup을 수행하여, 반대 방향의 coverage sanity check 보고서를 생성했습니다.
- OpenAlex-only/no-Crossref-match 보고서와 동일한 논리로 `Crossref-only venues with no OpenAlex source match`를 분리했습니다.

### 수정/생성한 파일
- `reports/crossref_only_venues_openalex_check.csv`: Crossref-only 427개 venue 전체에 대한 OpenAlex source lookup 상세 결과를 저장했습니다.
- `reports/crossref_only_venues_openalex_check.md`: 조회 결과 요약과 no-match/possible-match 목록을 Markdown으로 기록했습니다.
- `reports/crossref_only_venues_no_openalex_source_match.xlsx`: OpenAlex source match가 없는 202개 Crossref-only venue 전용 Excel 보고서를 생성했습니다.
- `AGENT_LOG.md`: 이번 OpenAlex source lookup 및 보고서 생성 작업을 기록했습니다.

### 구현한 기능
- Crossref-only venue 427개를 OpenAlex `/sources` 검색 API로 확인했습니다.
- 결과를 `exact_openalex_source_match`, `possible_openalex_source_match`, `no_openalex_source_match`, `lookup_error`로 분류했습니다.
- 최종 결과는 exact match 218개, possible match 7개, no match 202개, lookup error 0개입니다.
- Excel 파일에는 `Summary`, `No_OpenAlex_Source_Match`, `All_No_Match_Compact` 시트를 넣었고, compact 시트도 전체 202개 no-match venue를 표시합니다.

### 설계 결정
- `Crossref-only`는 현재 프로젝트의 collected dataset에서 Crossref로만 관측되었다는 의미이며, OpenAlex lookup은 venue/source-title 단위의 sanity check로 제한했습니다.
- paper-level DOI coverage를 증명하는 작업이 아니므로 Summary와 Markdown에 해당 해석을 명시했습니다.
- OpenAlex lookup에는 API key를 사용하지 않았고, `mailto`와 User-Agent를 포함해 polite pool 방식으로 조회했습니다.

### 남은 작업
- Crossref-only no-match 202개 venue 중 실제 제조 분야에서 유지할 가치가 있는 book/proceedings/source와 제거할 source를 수동 정책으로 나눌 수 있습니다.
- Crossref-only 운영으로 전환할 경우, 이 목록을 OpenAlex 누락 위험 분석의 근거로 사용할 수 있습니다.

### 주의사항
- OpenAI API는 사용하지 않았습니다.
- PDF, 출판사 초록 원문, API key, secret, token은 저장하거나 표시하지 않았습니다.
- `reports/_crossref_only_openalex_lookup_cache.json`은 중간 조회 재시작용 캐시라 커밋하지 않습니다.

## 2026-06-17 12:24
### 변경 요약
- `reports/` 폴더에 Excel 보고서가 많아져서 불필요한 중간 산출물을 정리했습니다.
- 최종 판단에 필요한 Excel 파일은 유지하고, 오래된 broad/intermediate Excel 파일을 제거하기 시작했습니다.

### 수정/생성한 파일
- `reports/source_overlap_analysis.xlsx`: broad summary Excel이 `source_overlap_openalex_crossref_groups.xlsx`와 역할이 겹치므로 제거했습니다.
- `AGENT_LOG.md`: 보고서 정리 기준과 남은 잠금 파일 이슈를 기록했습니다.

### 구현한 기능
- 현재 유지하는 핵심 Excel 보고서는 다음 세 가지입니다.
- `reports/source_overlap_openalex_crossref_groups.xlsx`: OpenAlex only / Crossref only / both 전체 그룹 보기.
- `reports/openalex_only_venues_no_crossref_journal_match.xlsx`: OpenAlex-only 중 Crossref journal match가 없는 venue 전체 보기.
- `reports/crossref_only_venues_no_openalex_source_match.xlsx`: Crossref-only 중 OpenAlex source match가 없는 venue 전체 보기.

### 설계 결정
- CSV와 Markdown 보고서는 감사 추적과 재검증을 위해 유지했습니다.
- Excel 임시 잠금 파일과 중간 조회 캐시는 추적하지 않기로 했습니다.

### 남은 작업
- `reports/openalex_only_venues_crossref_check.xlsx`는 현재 Excel에서 열려 있어서 삭제가 막혔습니다. 사용자가 해당 Excel 창을 닫으면 제거할 수 있습니다.
- `reports/~$openalex_only_venues_crossref_check.xlsx` 역시 Excel 잠금 파일이므로 원본 workbook이 닫히면 함께 사라지거나 삭제할 수 있습니다.

### 주의사항
- OpenAI API는 사용하지 않았습니다.
- 열려 있는 Excel 프로세스를 강제로 종료하지 않았습니다.

## 2026-06-17 13:21
### 변경 요약
- 이전 `Only OpenAlex / Only Crossref` 표가 현재 dataset provenance 기준이라 실제 API coverage와 다를 수 있음을 확인하고, paper-level API verification을 다시 수행했습니다.
- OpenAlex-only paper는 Crossref에서 DOI/title로 재조회했고, Crossref-only paper는 OpenAlex에서 DOI/title로 재조회했습니다.
- venue는 기존 source-title lookup 결과를 normalized venue name으로 다시 매핑해 정확한 confirmed/possible/no-match 집계를 계산했습니다.

### 수정/생성한 파일
- `reports/api_source_coverage_verified.xlsx`: 실제 API 재조회 기반의 verified coverage count와 상세 paper/venue 행을 담은 Excel 보고서를 생성했습니다.
- `AGENT_LOG.md`: 검증 방식, 결과 숫자, 주의사항을 기록했습니다.

### 구현한 기능
- DOI가 있는 논문은 DOI API lookup을 confirmed match 기준으로 사용했습니다.
- DOI가 없는 논문은 normalized title exact/near-exact match만 confirmed로 보고, high-similarity match는 possible로 분리했습니다.
- paper-level verified 결과:
  - confirmed both: all papers 2798, site papers 1265
  - confirmed OpenAlex-only with no Crossref match: all papers 241, site papers 82
  - confirmed Crossref-only with no OpenAlex match: all papers 34, site papers 9
  - possible both: all papers 1, site papers 1
  - lookup error: all papers 1, site papers 0
- venue-level verified 결과:
  - confirmed both: all venues 761, site venues 406
  - confirmed OpenAlex-only with no Crossref journal match: all venues 93, site venues 62
  - confirmed Crossref-only with no OpenAlex source match: all venues 202, site venues 53
  - possible both: all venues 10, site venues 4
  - lookup error: all venues 0

### 설계 결정
- “real number”는 source provenance가 아니라 API 재조회 기준으로 계산했습니다.
- confirmed count에는 DOI match와 strict normalized-title/source-title match만 포함했습니다.
- possible match는 confirmed truth에 넣지 않고 별도 행으로 분리했습니다.
- `curated_records > 0`을 site-visible/site thing 기준으로 유지했습니다.

### 남은 작업
- `api_source_coverage_report.xlsx`가 Excel에서 열려 있어 바로 덮어쓰지 않고 `api_source_coverage_verified.xlsx`를 별도 생성했습니다. 사용자가 Excel 파일을 닫으면 최종 보고서를 하나로 통합할 수 있습니다.

### 주의사항
- OpenAI API는 사용하지 않았습니다.
- Crossref와 OpenAlex 공식 API만 사용했고, PDF나 publisher abstract는 수집하지 않았습니다.
- `_paper_api_coverage_lookup_cache.json`은 재조회 중간 캐시이므로 커밋하지 않습니다.

## 2026-06-17 13:45
### 변경 요약
- 논문 카드에 corresponding author, 상세 author chip, venue quality signal을 표시할 수 있도록 시스템을 확장했습니다.
- OpenAlex의 `authorships.is_corresponding` 및 authorship/institution metadata를 저장하도록 OpenAlex fetcher와 저장 schema를 확장했습니다.
- IF/Q 분류는 공식 JCR/Scopus 데이터를 자동 추정하지 않고, 비공식 open proxy/수동 core venue label로 분리했습니다.

### 수정/생성한 파일
- `scripts/fetch_openalex.py`: OpenAlex work metadata에서 `author_details`, `corresponding_authors`, OpenAlex work/source ID, venue metrics를 정규화하도록 확장했습니다.
- `scripts/update_papers.py`: 새 author/venue metric 필드를 저장하고 merge하며 `journal_quality` label을 생성하도록 확장했습니다.
- `scripts/enrich_openalex_metadata.py`: 기존 `data/papers.json` / `data/archive_papers.json`의 누락된 OpenAlex author/venue metadata를 DOI 기준으로 보강하는 수동 스크립트를 추가했습니다.
- `.github/workflows/enrich-openalex-metadata.yml`: OpenAI 없이 OpenAlex metadata만 보강하는 수동 GitHub Actions workflow를 추가했습니다.
- `assets/app.js`: paper card에 corresponding author, 상세 author chip, venue signal을 렌더링하고 author/institution 검색이 가능하도록 확장했습니다.
- `assets/style.css`: corresponding author, author chip, venue signal UI 스타일을 추가했습니다.
- `index.html`: GitHub Pages cache busting을 위해 CSS/JS version query를 갱신했습니다.
- `data/papers.json`: smoke test로 5개 curated paper에 OpenAlex author/venue metadata를 보강했습니다.
- `PROJECT_STATUS.md`: author/venue quality metadata 상태와 IF/Q 정책을 문서화했습니다.
- `ARCHITECTURE.md`: OpenAlex enrichment 구조와 official IF/quartile 정책을 문서화했습니다.
- `AGENT_LOG.md`: 이번 구현 작업, 검증 결과, 남은 작업을 기록했습니다.

### 구현한 기능
- Corresponding author가 OpenAlex에 제공되면 카드에서 `Corresponding`으로 강조 표시합니다.
- Author chip은 최대 6명까지 표시하고, tooltip에 author position 및 대표 institution을 담습니다.
- 상세 author/institution/ORCID/OpenAlex author ID는 검색 haystack에도 포함됩니다.
- `journal_quality`는 다음 방식으로 보수적으로 생성합니다.
  - Nature/Science/Advanced Materials 등은 `High-impact general journal`.
  - Additive Manufacturing, Manufacturing Letters 등 core venue는 `Core manufacturing journal`.
  - arXiv/Zenodo/Figshare/ChemRxiv/Research Square 등은 `Repository / preprint source`.
  - OpenAlex source metric이 있을 때는 `OpenAlex citation impact` proxy label을 사용합니다.
- 공식 `official_jif`와 `official_quartile`은 licensed JCR/Scopus 데이터가 없으면 `null`로 유지합니다.

### 설계 결정
- Corresponding author는 추정하지 않고 OpenAlex가 제공하는 `authorships.is_corresponding` 값만 신뢰합니다.
- Crossref author metadata는 affiliation/ORCID coverage가 불완전하므로 corresponding author의 주 source로 사용하지 않았습니다.
- JIF/Q는 공개 API로 임의 추정하면 오해가 크기 때문에 UI에는 `Venue signal`이라고 표시하고, 공식 IF/Q 필드는 비워두었습니다.
- 전체 기존 데이터 보강은 rate limit을 고려해 별도 manual workflow로 분리했습니다.

### 검증 결과
- `python -m py_compile scripts/fetch_openalex.py scripts/update_papers.py scripts/enrich_openalex_metadata.py` 통과.
- `OPENALEX_ENRICH_MAX=5 python scripts/enrich_openalex_metadata.py` smoke test 통과.
- 현재 `data/papers.json` 1357편 중 5편에 `author_details`, `corresponding_authors`, `journal_quality`가 채워졌습니다.
- JS 정적 sanity check에서 새 함수가 1회씩 존재하고 brace count가 균형을 이룸을 확인했습니다.

### 남은 작업
- 전체 기존 논문에 author/venue metadata를 채우려면 GitHub Actions의 `Enrich OpenAlex metadata` workflow를 `max_records=0`, `force=false`로 수동 실행합니다.
- 공식 Q/IF가 필요하면 JCR/Scopus 등 licensed source에서 `data/journal_metrics.csv` 또는 API integration을 추가해야 합니다.
- 현재 세션에서는 browser automation runtime이 노출되지 않아 실제 브라우저 visual QA는 수행하지 못했습니다.

### 주의사항
- OpenAI API는 사용하지 않았습니다.
- PDF, publisher abstract, API key, secret, token은 저장하거나 표시하지 않았습니다.
- IF/Q는 공식 값처럼 표시하지 않도록 `Venue signal`로만 표현했습니다.

## 2026-06-17 13:52
### 변경 요약
- 논문 카드의 author 표시를 사용자가 요청한 명시적 문장형 라벨로 변경했습니다.
- 기존 `Corresponding` badge 대신 `Corresponding author: ...`, author chip 영역에는 `Authors: ...` 라벨을 표시하도록 바꿨습니다.

### 수정/생성한 파일
- `assets/app.js`: `renderCorrespondingAuthors`와 `renderAuthorDetails`의 출력 문구를 명시적 라벨 형태로 변경했습니다.
- `assets/style.css`: `.author-line` 기반 라벨/칩 레이아웃으로 스타일을 조정했습니다.
- `index.html`: GitHub Pages cache busting query를 `20260617-author-labels`로 갱신했습니다.
- `AGENT_LOG.md`: 이번 UI 라벨 변경을 기록했습니다.

### 구현한 기능
- Corresponding author가 있으면 `Corresponding author: Name` 형태로 표시합니다.
- Author 상세 정보가 있으면 `Authors:` 라벨 뒤에 author chip을 표시합니다.
- 아직 OpenAlex author detail이 없는 논문도 기존 `authors` 배열을 사용해 `Authors:` 라인을 표시할 수 있습니다.

### 설계 결정
- 사용자가 원하는 명확한 reading format을 우선해 chip-only UI보다 문장형 label을 앞에 두었습니다.
- Corresponding author는 여전히 OpenAlex가 제공한 값만 표시하고 추정하지 않습니다.

### 남은 작업
- 전체 논문에 author detail을 채우려면 `Enrich OpenAlex metadata` workflow를 수동 실행해야 합니다.

### 주의사항
- OpenAI API는 사용하지 않았습니다.

## 2026-06-17 12:34
### 변경 요약
- 여러 Excel/CSV/Markdown 보고서를 하나의 최종 Excel 보고서로 통합했습니다.
- 사용자가 보고서 폴더에서 한 파일만 보기를 원했기 때문에 중간 산출물과 감사용 CSV/MD 보고서를 제거했습니다.

### 수정/생성한 파일
- `reports/api_source_coverage_report.xlsx`: API source coverage 분석을 모두 담은 단일 최종 Excel 보고서를 생성했습니다.
- `reports/source_overlap_openalex_crossref_groups.xlsx`: 단일 최종 보고서와 중복되므로 제거했습니다.
- `reports/openalex_only_venues_no_crossref_journal_match.xlsx`: 단일 최종 보고서와 중복되므로 제거했습니다.
- `reports/crossref_only_venues_no_openalex_source_match.xlsx`: 단일 최종 보고서와 중복되므로 제거했습니다.
- `reports/crossref_only_venues_openalex_check.csv`: 단일 최종 보고서에 내용이 포함되어 제거했습니다.
- `reports/crossref_only_venues_openalex_check.md`: 단일 최종 보고서에 내용이 포함되어 제거했습니다.
- `reports/openalex_only_venues_crossref_check.csv`: 단일 최종 보고서에 내용이 포함되어 제거했습니다.
- `reports/openalex_only_venues_crossref_check.md`: 단일 최종 보고서에 내용이 포함되어 제거했습니다.
- `reports/source_overlap_analysis.md`: 단일 최종 보고서에 내용이 포함되어 제거했습니다.
- `reports/source_overlap_records_all_3075.csv`: 단일 최종 보고서에 내용이 포함되어 제거했습니다.
- `reports/source_overlap_title_matches.csv`: 단일 최종 보고서에 내용이 포함되어 제거했습니다.
- `reports/source_overlap_unique_papers.csv`: 단일 최종 보고서에 내용이 포함되어 제거했습니다.
- `reports/source_overlap_venues.csv`: 단일 최종 보고서에 내용이 포함되어 제거했습니다.
- `AGENT_LOG.md`: 단일 보고서 통합 및 정리 기준을 기록했습니다.

### 구현한 기능
- `api_source_coverage_report.xlsx`에는 다음 시트를 포함했습니다.
- `Summary`: 전체 source coverage 핵심 숫자와 해석 기준.
- `Papers_Source_Groups`: deduped paper 기준 OpenAlex only / Crossref only / both.
- `Venues_Source_Groups`: venue/source-title 기준 OpenAlex only / Crossref only / both.
- `OpenAlexOnly_NoCrossref`: OpenAlex-only 중 Crossref journal match가 없는 93개 venue.
- `CrossrefOnly_NoOpenAlex`: Crossref-only 중 OpenAlex source match가 없는 202개 venue.
- `All_OpenAlex_Check`: OpenAlex-only 428개 venue의 Crossref lookup 전체 결과.
- `All_Crossref_Check`: Crossref-only 427개 venue의 OpenAlex lookup 전체 결과.

### 설계 결정
- 사용자가 “only one file”을 원했기 때문에, 사람이 볼 최종 보고서는 `api_source_coverage_report.xlsx` 하나로 통합했습니다.
- 원본 CSV/MD 감사 파일은 Git history에 남아 있으므로 현재 작업 폴더에서는 제거했습니다.
- 단일 Excel 안에 상세 원본 수준의 행을 포함해, 별도 CSV 없이도 검토 가능하게 했습니다.

### 남은 작업
- `reports/openalex_only_venues_crossref_check.xlsx`는 현재 Excel에서 열려 있어서 Windows가 삭제를 막고 있습니다. 사용자가 해당 Excel 창을 닫으면 이 파일과 `reports/~$openalex_only_venues_crossref_check.xlsx` 잠금 파일을 삭제해 완전히 한 파일만 남길 수 있습니다.

### 주의사항
- OpenAI API는 사용하지 않았습니다.
- 열려 있는 Excel 프로세스를 강제로 종료하지 않았습니다.
## 2026-06-18 14:05
### Change Summary
- Added a separate manual AML recommendation engine without modifying the existing 6-hour keyword update workflow.
- Integrated optional AML recommendation display into the website without changing the existing paper fetch paths.

### Modified / Created Files
- `.github/workflows/aml-recommendation-manual.yml`: new manual-only workflow using `workflow_dispatch`; no schedule, push, or pull_request trigger.
- `.gitignore`: added private/raw/cache/embedding/log/PDF/environment-file ignore rules.
- `scripts/aml_common.py`: shared AML paths, scoring helpers, normalization, public-output helpers.
- `scripts/generate_aml_profile.py`: deterministic AML profile generation with optional AI profile generation disabled by default.
- `scripts/build_aml_seed_embeddings.py`: OpenAI seed embedding cache under `data/private/`.
- `scripts/collect_aml_candidates.py`: candidate collection from existing local paper pool and optional OpenAlex/Crossref search.
- `scripts/score_aml_recommendations.py`: deterministic scoring, optional AI judge/reason, public-safe output generation.
- `scripts/run_aml_recommendation_pipeline.py`: orchestration entry point for the manual workflow.
- `index.html`: added an optional AML recommendations section.
- `assets/app.js`: added optional fetch/render for `public/data/aml_recommended_papers.json`; existing `data/papers.json`, `data/site_meta.json`, and `data/update_status.json` fetch paths remain unchanged.
- `assets/style.css`: added small AML section/card styling.
- `README.md`, `ARCHITECTURE.md`, `PROJECT_STATUS.md`: documented manual AML workflow, OpenAI usage policy, public/private outputs, and seed file requirement.

### Implemented Features
- AML recommendation pipeline runs manually only.
- OpenAI embeddings are used when an API key is available, but OpenAI is not used as the primary paper search engine.
- OpenAI relevance judge and OpenAI reason rewriting are optional and disabled by default.
- Template-based recommendation reasons are used by default.
- Private outputs are written under ignored `data/private/`.
- Public output path is `public/data/aml_recommended_papers.json`.

### Design Decisions
- `.github/workflows/update-papers.yml` was inspected and intentionally not modified.
- The current website fetch paths must not move: `data/papers.json`, `data/site_meta.json`, and `data/update_status.json`.
- The AML section is hidden if `public/data/aml_recommended_papers.json` does not exist, preserving existing site behavior.
- The required repository seed file `data/seed/aml_seed_papers_core_enriched.json` is currently absent. The scripts support `AML_SEED_PATH` for local testing but default to the required path.

### Remaining Work
- Add the real AML seed file at `data/seed/aml_seed_papers_core_enriched.json`.
- Run `Actions > AML Recommendation Manual > Run workflow`.
- Review the generated `public/data/aml_recommended_papers.json` before publishing if using collection modes.

### Notes / Cautions
- A smoke test used local `private/aml_seed_papers_core_enriched.json` only through `AML_SEED_PATH`; generated public/profile test files were removed and private seed data was not committed.
- OpenAI API was not used in the smoke test because no key was present.
- Do not commit `data/private/`, embeddings, logs, raw API payloads, PDFs, or `.env` files.

## 2026-06-18 09:57
### Change Summary
- Removed the `Metals/Alloys` keyword/subtopic from the tracker taxonomy and collection logic.
- Cleaned existing stored paper metadata so `Metals/Alloys` no longer appears as a tag/category.

### Modified / Created Files
- `assets/app.js`: Removed `Metals/Alloys` from sidebar subtopics, card tag priority, label maps, tag inference rules, and broad production/manufacturing keyword checks.
- `data/queries.json`: Removed the metals-specific query `mechanical behaviour additively manufactured metals`.
- `data/papers.json`: Removed existing `Metals/Alloys` values from stored `tags` / `categories`.
- `data/archive_papers.json`: Removed metal/alloy raw tag values from archived `tags` / `categories`.
- `index.html`: Bumped asset cache query version to `20260618-no-metals`.
- `AGENT_LOG.md`: Recorded this taxonomy cleanup.

### Implemented Features
- The UI no longer shows `Metals/Alloys` as a sidebar subtopic or card tag.
- New frontend tag inference no longer assigns `Metals/Alloys`.
- Scheduled collection no longer uses the metals-only query.

### Design Decisions
- Paper titles and summaries were not edited, because those describe the actual paper content.
- Only structured topic fields (`tags`, `categories`) and collection keywords were changed.

### Remaining Work
- After deployment, visually confirm that `Metals/Alloys` no longer appears in filters or paper cards.

### Notes / Cautions
- This does not block legitimate metal-related papers from appearing when they match other tracker topics such as AM, MMAM, FGAM, process optimization, DLP, digital twins, or toolpath strategy.
- OpenAI API was not used.

## 2026-06-18 09:54
### Change Summary
- Removed the Compact/Comfort density mode and kept the site on the default comfortable card layout.

### Modified / Created Files
- `index.html`: Removed the density toggle button and bumped asset cache versions.
- `assets/app.js`: Removed density state, localStorage handling, toggle event handling, and density UI labels.
- `assets/style.css`: Removed compact-density CSS overrides.
- `AGENT_LOG.md`: Recorded this density-mode cleanup.

### Implemented Features
- The public UI now has only the theme toggle in the header toolbar.
- Paper cards always use the comfortable/default spacing.

### Design Decisions
- Density switching was removed entirely instead of hidden, because the user no longer needs compact mode.
- Default CSS is the comfortable layout, so no replacement setting is necessary.

### Remaining Work
- Recheck the deployed GitHub Pages page after cache refresh.

### Notes / Cautions
- This does not affect data collection, OpenAI usage, or paper metadata.

## 2026-06-18 09:50
### Change Summary
- Converted the public site and summary generation path to English-only.
- Removed the Korean language toggle and stopped reading Korean summary fields in the frontend.
- Changed new OpenAI/manual summary generation to produce English Q5 summaries only.

### Modified / Created Files
- `index.html`: Removed the language toggle, cleaned static UI copy to English, and bumped asset cache versions.
- `assets/app.js`: Fixed language state to English, removed Korean-mode branches, stopped displaying/searching `ai_summary_ko` and `relevance_note_ko`, and normalized UI labels to English.
- `scripts/summarize.py`: Changed OpenAI prompt and fallback summary output to English-only `ai_summary_en` / `relevance_note_en`.
- `scripts/update_papers.py`: Stopped writing new Korean summary fields during scheduled metadata updates.
- `scripts/refresh_openai_summaries.py`: Changed manual OpenAI refresh to target English summaries only.

### Implemented Features
- English-only UI with no visible Korean mode switch.
- English-only Q5 summary generation for future OpenAI refreshes.
- Metadata fallback summaries remain available without OpenAI and are also English-only.

### Design Decisions
- Existing historical `ai_summary_ko` fields in `data/papers.json` were not deleted to avoid a large data-only churn, but the frontend and new scripts no longer use them.
- Scheduled updates still do not call OpenAI. OpenAI refresh remains manual-only and user-approved.
- The site now treats `ai_summary_en` as the canonical summary display field.

### Remaining Work
- If desired later, run a separate cleanup script to remove historical Korean summary fields from stored JSON data.
- Perform browser visual QA after the next GitHub Pages deployment.

### Notes / Cautions
- Do not reintroduce automatic OpenAI calls into scheduled update workflows.
- Do not display publisher abstracts or store PDFs.
- Tests run: `python -m py_compile scripts/summarize.py scripts/update_papers.py scripts/refresh_openai_summaries.py`, `git diff --check`, and static JS reference checks for removed Korean-mode fields.

## 2026-06-27 09:17
### Change Summary
- Added journal/conference publication-type classification and venue-trust filtering.
- Moved low-trust or unsupported venues out of the active website dataset into the archive layer.
- Regenerated active indexes, detail chunks, CSV/XLSX exports, and AML recommendation output using the new trusted-venue rule.

### Modified / Created Files
- `scripts/update_papers.py`: Added `_venue_classification`, `publication_type`, `venue_trust`, and `venue_trust_reason`; low-trust venues now archive as `low_venue_trust`.
- `scripts/full_rebuild_crossref_dataset.py`: Preserved the same venue classification fields during Crossref full rebuild exports.
- `scripts/build_split_data.py`: Added `publication_type` and `venue_trust` to lightweight index records for frontend filtering/display.
- `scripts/aml_common.py`: Added matching trusted-publication classification for AML recommendations.
- `scripts/score_aml_recommendations.py`: Prevented low-trust AML candidates from being published to `public/data/aml_recommended_papers.json`.
- `assets/app.js`: Displayed publication type labels such as `Journal` and `Conference` in paper cards.
- `data/papers.json`: Rebuilt active dataset after venue filtering.
- `data/archive_papers.json`: Archived low-trust venue records while preserving traceability.
- `data/papers_index.json`, `data/detail_manifest.json`, `data/details/*`: Rebuilt active lazy-load data.
- `data/archive_papers_index.json`, `data/archive_detail_manifest.json`, `data/archive_details/*`: Rebuilt archive lazy-load data.
- `data/papers.csv`, `data/papers.xlsx`: Regenerated exports from the active trusted dataset.
- `data/site_meta.json`: Added/updated hidden low-venue-trust counts.
- `public/data/aml_recommended_papers.json`: Rewrote AML public recommendations with venue-trust metadata.
- `AGENT_LOG.md`: Recorded this venue-quality cleanup.

### Implemented Features
- Active site papers are now classified as journal articles or trusted conference proceedings.
- Low-trust venue records, repository/preprint records, book/chapter records, unknown venues, and non-allowlisted proceedings are hidden from the main site list.
- Trusted conference allowlist includes selected manufacturing/robotics/HCI venues such as ICRA, IROS, RoboSoft, CASE, CHI, and ACM computational fabrication proceedings.
- AML recommendations use the same venue-trust gate before publication.

### Design Decisions
- Records were archived rather than permanently deleted so the filtering decision remains reversible.
- General journal articles with named venues are trusted by default unless they match local low-trust markers.
- Conferences are stricter than journals: only allowlisted reputable venues remain visible.
- Preprints and repositories are hidden from the main curated layer because the user requested cleaner trusted journal/conference coverage.

### Remaining Work
- If the lab wants additional conference venues displayed, extend the trusted conference allowlist in both `scripts/update_papers.py` and `scripts/aml_common.py`.
- Visually verify the deployed site after GitHub Pages refresh.
- Consider adding a dedicated UI filter for `Journal` versus `Conference` if the user wants explicit browsing by publication type.

### Notes / Cautions
- Active dataset after filtering: 1,587 records; archive dataset: 541 records.
- Active publication types: 1,575 journal articles and 12 trusted conference proceedings.
- Active low-trust venue count: 0.
- Archive reasons after rebuild: 488 `low_venue_trust`, 48 `duplicate_title`, and 5 `low_relevance`.
- AML public recommendations after filtering: 545 records with 0 low-trust venue records.
- OpenAI, Crossref, and OpenAlex APIs were not called for this cleanup; only local JSON/CSV/XLSX regeneration was performed.

## 2026-06-27 09:33
### Change Summary
- Moved `Journal` / `Conference` publication-type text out of the venue label and into a separate paper-card badge.

### Modified / Created Files
- `assets/app.js`: Rendered `publication_type` as a separate `publication-type-badge`; restored venue label text to venue/year only.
- `assets/style.css`: Added light/dark styling for the new publication-type badge.
- `index.html`: Bumped CSS/JS cache query versions for deployment.
- `AGENT_LOG.md`: Recorded this UI adjustment.

### Implemented Features
- Paper cards now show publication type separately from the journal or conference name.
- Venue labels remain compact and readable, for example `Nat. Commun. 2026`.

### Design Decisions
- Publication type is a small outlined badge so it helps scanning without competing with the venue badge.
- No data files or API workflows were changed.

### Remaining Work
- Visually verify the badge spacing after GitHub Pages deployment.

### Notes / Cautions
- OpenAI, Crossref, and OpenAlex APIs were not called.

## 2026-06-27 09:45
### Change Summary
- Fixed sidebar subtopic counting/filtering so clicked subtopics use the same representative-topic logic as the displayed paper cards.

### Modified / Created Files
- `assets/app.js`: Added `sidebarTopics` to each paper runtime cache and made sidebar matching use representative tags instead of broad hidden tag inference.
- `index.html`: Bumped CSS/JS cache query versions for deployment.
- `AGENT_LOG.md`: Recorded this sidebar filtering fix.

### Implemented Features
- Sidebar subtopic counts and clicked paper results now use the same paper-to-subtopic bucket.
- Papers should no longer appear under a sidebar topic only because of broad hidden tags that are not representative of the card.

### Design Decisions
- Kept the exact one-bucket-per-field behavior so subtopic counts remain understandable and sum cleanly inside each main field.
- The global tag dropdown still uses the broader canonical tag set; this fix targets the left sidebar only.

### Remaining Work
- Visually test a few sidebar topics after deployment, especially broad topics such as `MMAM`, `Machine Learning`, and `Process Optimization`.

### Notes / Cautions
- OpenAI, Crossref, and OpenAlex APIs were not called.

## 2026-06-27 10:02
### Change Summary
- Removed `Material Switching` / purge-related keywords from collection, classification, sidebar aggregation, and structured paper tags.

### Modified / Created Files
- `assets/app.js`: Removed `Material Switching` from sidebar subtopics, tag labels, canonical aliases, representative tag priority, and frontend subtopic inference.
- `data/queries.json`: Removed material-switching and purge-reduction collection queries.
- `scripts/update_papers.py`: Removed material switching / purge as relevance topic terms for future updates.
- `scripts/summarize.py`: Removed the material-switching category, keyword map, tag map, aliases, fallback tags, and score boosts for future summaries.
- `scripts/aml_common.py`: Removed material switching from AML recommendation profile terms.
- `scripts/collect_aml_candidates.py`: Removed material switching from AML candidate signal matching.
- `scripts/generate_aml_profile.py`: Removed material switching from generated profile interests and high-relevance criteria.
- `data/papers.json`, `data/archive_papers.json`, `public/data/aml_recommended_papers.json`: Removed material-switching/purge values from structured `categories`, `tags`, and `matched_topics`.
- `data/papers_index.json`, `data/archive_papers_index.json`, `data/details/*`, `data/archive_details/*`: Rebuilt split website data.
- `data/papers.csv`, `data/papers.xlsx`: Regenerated exports from the cleaned active dataset.
- `index.html`: Bumped CSS/JS cache query versions for deployment.
- `AGENT_LOG.md`: Recorded this keyword removal.

### Implemented Features
- `Material Switching` no longer appears as a left-sidebar subtopic or representative card tag.
- Existing structured paper metadata no longer contributes material-switching/purge values to tag or sidebar aggregation.
- Future scheduled/manual metadata updates no longer use material-switching/purge queries or classification boosts.

### Design Decisions
- Paper titles and scientific summary sentences were not edited just because they mention material switching; those are paper content, not tracker keywords.
- Only structured filtering/aggregation fields and future keyword logic were changed.

### Remaining Work
- After deployment, confirm the left sidebar and tag dropdown no longer expose `Material Switching` or purge-related labels.

### Notes / Cautions
- OpenAI, Crossref, and OpenAlex APIs were not called.
- Active paper count remains 1,587; this cleanup changes topic/tag visibility, not venue trust filtering.

## 2026-06-27 10:13
### Change Summary
- Removed `Toolpath Strategy` / toolpath-related keywords from collection, classification, sidebar aggregation, and structured paper tags.

### Modified / Created Files
- `assets/app.js`: Removed `Toolpath` / `Toolpath strategy` from sidebar subtopics, tag labels, canonical aliases, representative tag priority, field inference, and frontend subtopic inference.
- `data/queries.json`: Removed the toolpath-specific collection query.
- `scripts/update_papers.py`: Removed `toolpath` as a relevance topic term for future updates.
- `scripts/summarize.py`: Removed the toolpath category, keyword map, tag map, aliases, fallback tags, score boost, and old fallback text branches.
- `scripts/aml_common.py`: Removed toolpath-related AML recommendation profile terms.
- `scripts/collect_aml_candidates.py`: Removed toolpath from AML candidate search and signal matching.
- `scripts/generate_aml_profile.py`: Removed toolpath-aware design from generated profile interests and high-relevance criteria.
- `data/papers.json`, `data/archive_papers.json`, `public/data/aml_recommended_papers.json`: Removed toolpath-related values from structured `categories`, `tags`, and `matched_topics`.
- `data/papers_index.json`, `data/archive_papers_index.json`, `data/details/*`, `data/archive_details/*`: Rebuilt split website data.
- `data/papers.csv`, `data/papers.xlsx`: Regenerated exports from the cleaned active dataset.
- `index.html`: Bumped CSS/JS cache query versions for deployment.
- `AGENT_LOG.md`: Recorded this keyword removal.

### Implemented Features
- `Toolpath Strategy` no longer appears as a left-sidebar subtopic or representative card tag.
- Existing structured paper metadata no longer contributes toolpath-related values to tag or sidebar aggregation.
- Future scheduled/manual metadata updates no longer use toolpath-specific queries or classification boosts.

### Design Decisions
- `Path Planning` / graph-search style topics were left intact because the request targeted `Toolpath Strategy`, not all path-planning concepts.
- Paper titles and scientific summary sentences were not broadly rewritten just because they mention toolpath; those are paper content, not tracker keywords.

### Remaining Work
- After deployment, confirm the left sidebar and tag dropdown no longer expose `Toolpath Strategy` or `Toolpath`.

### Notes / Cautions
- OpenAI, Crossref, and OpenAlex APIs were not called.
- Active paper count remains 1,587; this cleanup changes topic/tag visibility, not venue trust filtering.

## 2026-06-27 10:23
### Change Summary
- Changed the left sidebar to show only main fields by default, with subtopics collapsed until a field is opened.

### Modified / Created Files
- `assets/app.js`: Added a sidebar collapse version and default-collapsed field state; clicking a collapsed main field now opens its subtopics while applying the field filter.
- `index.html`: Bumped CSS/JS cache query versions for deployment.
- `AGENT_LOG.md`: Recorded this sidebar behavior change.

### Implemented Features
- The left panel is shorter on first load because all field subtopic groups are collapsed by default.
- Users can click a main field to expand its subtopics and browse deeper.
- The existing caret collapse/expand behavior remains available.

### Design Decisions
- Existing local sidebar state is reset once with `SIDEBAR_COLLAPSE_VERSION` so previously expanded panels do not keep the sidebar long after deployment.
- No paper data, collection workflow, or API behavior was changed.

### Remaining Work
- After deployment, visually confirm the left sidebar starts compact on desktop and mobile.

### Notes / Cautions
- OpenAI, Crossref, and OpenAlex APIs were not called.

## 2026-06-27 10:31
### Change Summary
- Merged `Inverse Design` into `Machine Learning` as a unified AI-manufacturing topic.

### Modified / Created Files
- `assets/app.js`: Removed `Inverse Design` as a standalone sidebar subtopic/tag label and remapped inverse-design text signals to `Machine learning`.
- `scripts/summarize.py`: Removed standalone `Inverse Design` tag generation and moved inverse-design keywords into `Machine learning`.
- `data/papers.json`, `data/archive_papers.json`: Replaced structured `Inverse Design` category/tag/matched-topic values with `Machine learning`.
- `data/papers_index.json`, `data/archive_papers_index.json`, `data/details/*`, `data/archive_details/*`: Rebuilt split website data.
- `data/papers.csv`, `data/papers.xlsx`: Regenerated exports from the cleaned active dataset.
- `index.html`: Bumped CSS/JS cache query versions for deployment.
- `AGENT_LOG.md`: Recorded this taxonomy merge.

### Implemented Features
- `Inverse Design` no longer appears as a separate left-sidebar subtopic or representative tag.
- Papers with inverse-design signals are now grouped under `Machine Learning`.
- Existing structured metadata has no remaining standalone `Inverse Design` values.

### Design Decisions
- Kept inverse-design search queries in `data/queries.json` because they are useful for finding ML/design papers; only the displayed taxonomy was merged.
- Paper titles and summary prose were not rewritten when they mention inverse design as paper content.

### Remaining Work
- After deployment, confirm `AI Manufacturing > Machine Learning` includes the previous inverse-design papers and `Inverse Design` no longer appears as a filter item.

### Notes / Cautions
- OpenAI, Crossref, and OpenAlex APIs were not called.
- Active paper count remains 1,587; this cleanup changes taxonomy display, not collection count.

## 2026-06-27 10:39
### Change Summary
- Fixed AML recommendation cards so they also show the separate `Journal` / `Conference` publication-type badge.

### Modified / Created Files
- `assets/app.js`: Passed `publication_type`, `venue_trust`, and `venue_trust_reason` through `amlRecommendationToPaper()`.
- `index.html`: Bumped CSS/JS cache query versions for deployment.
- `AGENT_LOG.md`: Recorded this AML card display fix.

### Implemented Features
- AML recommendation cards now use the same publication-type badge rendering as normal paper cards.
- Existing AML recommendation data already had publication-type metadata, so no data rebuild was required.

### Design Decisions
- Reused the existing card renderer instead of adding a separate AML-specific badge path.
- No collection or recommendation scoring behavior was changed.

### Remaining Work
- After deployment, visually confirm AML recommendation cards show `Journal` or `Conference` before the venue badge.

### Notes / Cautions
- OpenAI, Crossref, and OpenAlex APIs were not called.

## 2026-06-28 09:20
### Change Summary
- Tightened the public site and AML recommendations to journal articles only.
- Removed all conference proceedings from active public paper lists, even if the conference venue had previously been allowlisted as trusted.

### Modified / Created Files
- `scripts/update_papers.py`: Changed curated-candidate eligibility so only `publication_type == journal_article` with non-low venue trust can remain active.
- `scripts/aml_common.py`: Changed AML public recommendation eligibility so only journal articles are published.
- `data/papers.json`: Rebuilt active public data as journal articles only.
- `data/archive_papers.json`: Moved non-journal active records into the archive layer.
- `data/papers_index.json`, `data/archive_papers_index.json`, `data/details/*`, `data/archive_details/*`: Rebuilt split website data.
- `data/papers.csv`, `data/papers.xlsx`: Regenerated exports from the journal-only active dataset.
- `data/site_meta.json`: Updated active/archive/paper counts after journal-only filtering.
- `public/data/aml_recommended_papers.json`: Removed non-journal AML recommendation records.
- `AGENT_LOG.md`: Recorded this journal-only policy change.

### Implemented Features
- Main site active records now contain only `journal_article` publications.
- AML recommendation records now contain only `journal_article` publications.
- Conference proceedings, preprints, repositories, books/chapters, unknown venues, and unsupported publication types are excluded from the public active layer.

### Design Decisions
- Non-journal records were archived rather than permanently deleted so the decision remains reversible.
- Existing `Conference` badge rendering remains in the UI for defensive compatibility, but active public data should no longer produce it.

### Remaining Work
- After deployment, verify no `Conference` badge appears in normal paper cards or AML recommendation cards.

### Notes / Cautions
- OpenAI, Crossref, and OpenAlex APIs were not called.
- Active public paper count after filtering: 1,512 journal articles.
- AML recommendation count after filtering: 740 journal articles.

## 2026-06-28 09:34
### Change Summary
- Tightened journal-only filtering further by excluding non-paper journal content such as corrections, errata, editorials, retractions, and publisher corrections.

### Modified / Created Files
- `scripts/update_papers.py`: Expanded `_is_non_research_output()` and archived matching journal records as `non_research_output`.
- `scripts/aml_common.py`: Added `is_non_research_output()` and excluded matching records from public AML recommendations.
- `data/papers.json`: Rebuilt active data after removing non-paper journal content.
- `data/archive_papers.json`: Archived removed correction/editorial/erratum records.
- `data/papers_index.json`, `data/archive_papers_index.json`, `data/details/*`, `data/archive_details/*`: Rebuilt split website data.
- `data/papers.csv`, `data/papers.xlsx`: Regenerated exports from the stricter active dataset.
- `data/site_meta.json`: Updated active/archive/paper counts and `hidden_non_research_output_count`.
- `public/data/aml_recommended_papers.json`: Removed correction/erratum records from AML recommendations.
- `AGENT_LOG.md`: Recorded this stricter journal-paper policy.

### Implemented Features
- Active public data now excludes records whose titles start with terms such as `Correction`, `Author Correction`, `Erratum`, `Editorial`, `Corrigendum`, `Retraction`, and similar non-paper outputs.
- AML recommendations use the same non-paper exclusion rule.

### Design Decisions
- Review and perspective-style research articles remain allowed, because they are legitimate journal-paper content.
- Removed records are archived rather than permanently deleted.

### Remaining Work
- After deployment, verify no correction/editorial/erratum records appear in normal cards or AML recommendation cards.

### Notes / Cautions
- OpenAI, Crossref, and OpenAlex APIs were not called.
- Active public paper count after filtering: 1,502 journal papers.
- AML recommendation count after filtering: 737 journal papers.

## 2026-06-28 09:42
### Change Summary
- Removed the redundant `Journal` publication-type badge from paper cards now that all public records are journal papers.

### Modified / Created Files
- `assets/app.js`: Removed publication-type badge rendering and the unused `publicationTypeLabel()` helper.
- `assets/style.css`: Removed light/dark styling for `.publication-type-badge`.
- `index.html`: Bumped CSS/JS cache query versions for deployment.
- `AGENT_LOG.md`: Recorded this UI cleanup.

### Implemented Features
- Paper cards now show only the venue/year badge, summary-provider badge, score badge, and other meaningful badges.
- AML recommendation cards follow the same simplified card header.

### Design Decisions
- Kept `publication_type` metadata in JSON and runtime objects for internal validation and future filtering, but removed it from the visible card UI.
- No paper data, collection workflow, or recommendation scoring behavior was changed.

### Remaining Work
- After deployment, visually confirm the card header no longer shows a `Journal` badge.

### Notes / Cautions
- OpenAI, Crossref, and OpenAlex APIs were not called.
## 2026-06-29 13:18
### 변경 요약
- 학위논문/대학 dissertation 항목은 저널 논문 사이트의 범위가 아니므로 수집 및 AML 추천 공개 후보에서 제외되도록 방어 규칙을 추가했습니다.
- 현재 공개 데이터와 AML 추천 공개 데이터에는 학위논문 후보가 남아 있지 않음을 확인했습니다.

### 수정/생성한 파일
- `scripts/update_papers.py`: `dissertation`, `doctoral thesis`, `master thesis`, `PhD thesis`, `university dissertation`, `electronic thesis`, `ETD` 계열을 low-trust `thesis_or_dissertation`으로 분류하고 curated paper에서 제외하도록 보강했습니다.
- `scripts/aml_common.py`: AML 추천 후보 점수화/공개 필터에서도 같은 thesis/dissertation 판별 규칙을 적용했습니다.
- `AGENT_LOG.md`: 이번 필터 보강과 검증 결과를 기록했습니다.

### 구현한 기능
- Crossref type 또는 venue/title/DOI 텍스트에 학위논문 신호가 있으면 `publication_type = thesis_or_dissertation`, `venue_trust = low`로 분류합니다.
- 학위논문으로 판별된 항목은 일반 curated paper와 AML 추천 공개 목록에 들어가지 않습니다.

### 설계 결정
- 현재 사이트는 저널 논문 중심으로 운영하기로 했으므로, 학위논문은 archive/비공개 후보로만 남기고 공개 UI에서는 제외합니다.
- `repository` 판정보다 `thesis/dissertation` 판정을 먼저 적용해 제외 이유가 더 명확하게 남도록 했습니다.

### 남은 작업
- 다음 자동/수동 업데이트 이후에도 공개 데이터에 thesis/dissertation 후보가 0개인지 재확인하면 좋습니다.

### 주의사항
- 현재 `data/papers.json`, `data/papers_index.json`, `public/data/aml_recommended_papers.json` 검사 결과 학위논문 후보는 0개였습니다.
- OpenAI API는 호출하지 않았습니다.
## 2026-07-07 10:14
### 변경 요약
- 논문 업데이트 방식을 full rebuild 교체 방식에서 `기존 active 논문 유지 + 새 Crossref 결과 추가/갱신` 방식으로 변경했습니다.
- OpenAI 요약이 적용된 기존 논문은 비용이 들어간 자산이므로, Crossref 검색 결과에서 일시적으로 빠져도 공개 데이터에서 삭제되지 않도록 했습니다.
- 이미 줄어든 최신 데이터도 복구하기 위해 `32bb8fe` 시점의 1502편 active 논문과 최신 1451편 active 논문을 DOI/title 기준으로 병합했습니다.

### 수정/생성한 파일
- `scripts/full_rebuild_crossref_dataset.py`: incremental Crossref merge 로직을 추가하고, 기존 active 논문 보존/신규 논문 추가/기존 논문 갱신 통계를 `site_meta.json`에 기록하도록 변경했습니다.
- `data/papers.json`: 기존 1502편과 최신 신규 19편을 병합해 1520편으로 복구했습니다.
- `data/archive_papers.json`: active로 복구된 논문을 제외하고 기존 archive와 신규 archive를 병합했습니다.
- `data/papers.csv`, `data/papers.xlsx`: 복구된 active 데이터 기준으로 재생성했습니다.
- `data/papers_index.json`, `data/details/`, `data/detail_manifest.json`: GitHub Pages 초기 로딩/상세 로딩용 split data를 재생성했습니다.
- `data/archive_papers_index.json`, `data/archive_details/`, `data/archive_detail_manifest.json`: archive split data를 재생성했습니다.
- `data/site_meta.json`: `collection_mode = manual_restore_incremental_union`, `paper_count = 1520`, `papers_added = 19`, 기존 보존/신규 추가 통계를 기록했습니다.
- `UPDATE_STATUS.md`, `data/update_status.json`: 현재 복구 상태와 논문 수가 보이도록 갱신했습니다.
- `AGENT_LOG.md`: 이번 정책 변경과 복구 작업을 기록했습니다.

### 구현한 기능
- 기존 active 논문은 다음 업데이트에서 기본 보존됩니다.
- 새 Crossref 결과가 기존 DOI/title과 일치하면 메타데이터는 갱신하되 OpenAI 요약, 태그, 관련성 점수 등 유료 요약 결과는 보존합니다.
- 새 DOI/title이면 active 논문으로 추가합니다.
- Crossref 결과에서 잠시 사라진 기존 논문은 `not_seen_in_latest_crossref_run = true`로 표시할 수 있지만, 공개 데이터에서는 유지합니다.

### 설계 결정
- Crossref relevance 결과는 실행마다 흔들릴 수 있으므로, 공개 사이트의 논문 목록을 Crossref 최신 검색 결과와 1:1로 교체하지 않기로 했습니다.
- `papers_added`는 이제 full rebuild 총량이 아니라 실제 신규 추가 수를 의미합니다.
- OpenAI API는 호출하지 않았고, 기존 저장 요약만 보존했습니다.

### 남은 작업
- 다음 scheduled update 이후 `collection_mode = incremental_crossref_merge`와 `papers_added`가 실제 신규 논문 수로 기록되는지 확인하세요.
- 필요하면 UI에서 `not_seen_in_latest_crossref_run`를 개발자용/숨김 상태로 표시할 수 있습니다.

### 주의사항
- 이번 복구 기준 old ref는 `32bb8fe`입니다.
- 복구 결과: old active 1502편, 최신 active 1451편, 신규 current-only 19편, 최종 active 1520편입니다.
