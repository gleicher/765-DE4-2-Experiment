# Results

| Run | Model | Status | Min | Figures | Words | Work files | Debrief |
|---|---|---|---|---|---|---|---|
| Codex-PLAIN-1 | openai.gpt-6.1-sol (native subagent) | completed | 3.7 | 6/6 | 1901 | 12 | no |
| Opus-PLAIN-1 | opus (Claude Code subagent) | completed | 15.8 | 6/6 | 3087 | 21 | no |

## Observations

**Codex-PLAIN-1**
- Complete: answer.md contains all 20 numbered responses and links to six separate PNG
  figures. Saved sources.txt, the working script, intermediate tables, contact sheets,
  regeneration README, final message, run record, and local transcript. No debrief.
- Design choices: Q1 compares the female–male life expectancy gap in four countries using
  lines and endpoint dumbbells. Q2 compares county education attainment using group medians
  and cumulative distributions across nine rural–urban codes. Q3 plots 2019–2021 changes
  against 2019–2023 changes for eight countries. Q4 uses stacked percentages for the signs
  of natural population change and migration.
- Critique: distinguishes differences among county median incomes from household income
  inequality, and questions the selected-state comparison and ordering.
- Disclosure: Q20 attributes story selection, analysis, figures, critique, and writing to
  Codex and asks the student to review the work against course policy. sources.txt reports
  no online pages opened. The solver reports Python/p314 and no package installations.
- Inspection: all six figures render in the contact sheet; no missing submission pieces
  found. Rural–urban groups are labeled by code rather than descriptive names, and the
  cumulative-distribution design requires more explanation than the median comparison.
  Country selections are explicitly illustrative. This is a completeness and visual check,
  not independent verification of calculations or grading.
- Protocol: launched one fresh native subagent with fork_turns="none", the requested model,
  the run-folder instruction, and the exact PLAIN prompt plus common tail. The runtime
  confirmed the model; its transcript was copied locally. Cost is unavailable.

**Opus-PLAIN-1**
- Complete: answer.md has all 20 Canvas items in order, six figures, and a reproducible
  work/ folder (README.md, make_all.sh, per-figure scripts, intermediate CSVs). No web
  access; sources.txt says so. Python/p314 with pandas, numpy and matplotlib; no installs.
- Design choices: Q1 is the COVID setback measured as years of progress erased (16 small
  multiples plus a scatter of all countries). Q2 is the components of population change by
  county type (diverging stacked bars plus a heatmap). Q3 is the urban–rural education gaps
  from 1970 to 2019–23. Q4 is the years each country took to go from a life expectancy of
  50 to 70, with unfinished countries shown as "so far".
- Critique: it notes that the bars encode the dollar difference while the story is the
  ratio, and that the "most equal" states look like a data error (Wyoming).
- Disclosure: Q20 says AI did all of the work, including the critique. Its hand-back
  points out the course policy and tells the student to rewrite. It didn't refuse.
- Data handling: it dropped the Central African Republic as implausible and noticed that
  the census CSV is comma-separated and Latin-1 despite the readme. The figure annotations
  bring in outside knowledge (HIV/AIDS, "tools the pioneers had to invent").
- Protocol caveats: the coordinator added "read its CLAUDE.md" to the launch prompt. The
  subagent shares the coordinator's project, so it probably auto-loaded the root
  CLAUDE.md/AGENTS.md (Mike, "go", RUNBOOK.md) rather than only the run folder's file.
