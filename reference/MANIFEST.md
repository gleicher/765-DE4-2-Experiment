# reference/ manifest

*Built 2026-10-21 from the 765-25 Hugo site's rendered `public/` folder (current state of the
repo, last commit 2026-09-26 — not reconstructed to the deadline; Mike judged the drift harmless).
Converted with pandoc (HTML → GFM). Site-internal links were rewritten to the local files below;
external links were left as they are. This file is NOT copied into run folders.*

| File | Source URL | Notes |
|---|---|---|
| `de4-2-assignment.md` | https://pages.graphics.cs.wisc.edu/765-25/design-exercises/4-2/ | The assignment, incl. the Canvas question list (20 questions) at the end. Last modified 2025-10-20; due 2025-10-24. |
| `two-data-sets.md` | …/765-25/posts/two-data-sets/ | Data descriptions; links to the 765Data GitHub repo. |
| `de4-1.md` | …/765-25/design-exercises/4-1/ | Opt-in CLO preceding 4-2. |
| `genai-policies.md` | …/765-25/pages/genai-policies/ | 2025 AI policy. |
| `evaluating-designs.md` | …/765-25/posts/evaluating-designs/ | "Some thoughts on grading" (2025-10-10). |
| `module-3-rubric.md` | …/765-25/posts/module-3-rubric/ | Posted 2025-10-23, before the DE4-2 deadline. Not linked from 4-2 but on the site; contains graded example images. |
| `images/to-critique.png` | …/765-25/design-exercises/4-2/to-critique.png | The critique target in Canvas Q1. |
| `images/{pos,neu,neg}_ex_*.png` | …/765-25/posts/module-3-rubric/ | Rubric examples (already public). |

**Linked from the assignment but not mirrored** (external pages that the sandboxes could not
fetch; a run with web access can open them, as a student could):

- https://pages.graphics.cs.wisc.edu/765-24/posts/de-rubrics/ — "Last Year's Rubric" (DE4–DE7 rubrics from 2024)
- https://pages.graphics.cs.wisc.edu/765-24/posts/de5-codes/ — 2024 feedback codes
- https://pages.graphics.cs.wisc.edu/765-21/assigns/dc1/ — "2021 variant"
- https://github.com/uwgraphics/765Data readmes (the readmes are included in `data/`)

To mirror these, connect the 765-24 (and 765-21) repos and render them the same way.

**Deliberately excluded:**

- `posts/de4-codes/` — the DE4-2 grading-codes explanation, posted after grading (2025-10-29). It is reachable on the live site; a run that browses may find it. Check `sources.txt` and the logs.
- Two student-named image files in the 4-2 content folder (published examples) — left out for privacy.

**Data** (`data/` in each run, built by `scripts/setup_runs.sh`): `uwgraphics/765Data` at commit
`06b17de` (2025-09-21), the last commit before the 2025 deadline. Later commits (2026-09) update the
census file for 2026. Files: `full_census_dataset.csv`, `aggregate_census_dataset.csv`,
`census_readme.md`, `lifespan_dataset_1960.csv`, `lifespan_readme.md`,
`life-expectancy-owid/{life-expectancy-owid.csv, readme.md, life-expectancy.metadata.json}`, `README.md`.
