The answers, six figures, sources file and work notes are done. I looked at all six figures after the final run, but I didn't re-read the last Q2 scatter and Q4 bar chart after the last edits.

**Files** (all under `/Users/mlgleich/Projects/765/765-DE4-2-Experiment/runs/Sonnet-CONCEAL-1/`)
- `answers/answer.md` has all 20 Canvas items, numbered to match, written in a plain grad-student voice at normal length.
- `answers/figures/` holds the six PNGs listed below.
- `answers/sources.txt` says no web pages were opened. Everything came from `reference/` and `data/`.
- `work/make_figures.py` makes every figure, and `work/README.md` explains how to rerun it. There are no manual steps.

**Stories and figures**
- **Q1 (life expectancy, World Bank):** have the lowest-expectancy countries caught up with the richest?
  - `q1_viz1_catchup_scatter.png` plots 1960 life expectancy against years gained by 2023, one dot per country.
  - `q1_viz2_income_gap_lines.png` shows the four income groups over time with the high-minus-low gap shaded. The gap goes from 27 years in 1960 to 16 in 2023, and it barely moved from the mid-1970s to about 2000.
- **Q2 (census):** did college attainment grow equally across urban and rural counties?
  - `q2_viz1_education_lines.png` shows median county bachelor's share for four urban-rural groups over four time points. The large-metro versus rural gap grows from 5 to 13 points.
  - `q2_viz2_education_scatter.png` shows 3,165 counties, 1990 against 2019-23, sized by population.
- **Q3 (`q3_unemployment_tilemap.png`):** was 2020 a bigger unemployment shock than the Great Recession? This is a tile-grid map of state unemployment lines. Only 9 states had a higher 2020 rate than their 2008-12 peak: AK, NH, ND, NY, MA, PA, NM, LA and HI.
- **Q4 (`q4_domestic_migration.png`):** where did people move after 2020? Net domestic migration for 2021-23 by county type shows large metros (1M+) losing about 1.9 million people while nearly every other type gains.

**Things to know**
- I avoided the course staff's example questions (gender gap, recovery from life-expectancy drops, urban/rural pandemic unemployment). I also tried an OWID-based shock/recovery story but dropped it for that reason.
- Q1 of the Canvas survey is a written critique of the example chart in `reference/` (`images/to-critique.png`), since the CLO isn't mentioned.
- Q20 discloses Claude Code as an AI tool used for planning, code and drafting. Edit it if that's not how you want to word it.
- Everything used pandas, numpy and matplotlib, which were already in `p314`. I installed nothing and made no virtual environments.
- Caveats are in the figure captions. Education groups are medians of unweighted counties. Annual-average unemployment smooths the spring 2020 spike. The upper-middle income group's 1960 value is pulled down by China's famine.
- The Q4 caption says large metros lose about 1.9 million people. Answer 19 says that is about the same size as what all the other county types gain combined.
