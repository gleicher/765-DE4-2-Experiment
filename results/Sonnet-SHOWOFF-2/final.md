The example response is finished: all 20 Canvas answers and six figures. I opened each figure after rendering and fixed the label collisions and wrong claims I found. I only skimmed the final `fig1b` re-render, which fixed a subtitle that overlapped the axis. Your manual check should cover that one first.

**Files**
- Answers: `/Users/mlgleich/Projects/765/765-DE4-2-Experiment/runs/Sonnet-SHOWOFF-2/answers/answer.md`. Headings are numbered 1–20 to match the Canvas order. Q1 is a critique of the Tableau figure `reference/images/to-critique.png`, written for a non-CLO student. Q20 discloses plainly that Claude (Sonnet 5.5) did everything at your request, as a private instructor example and not a student submission.
- Figures (PNG, about 2200 px wide, each with title, labels, legend and caption), all in `.../answers/figures/`:
  - `fig1a_gender_gap_trajectories.png`
  - `fig1b_gender_gap_arrows.png`
  - `fig2a_unemployment_flip_lines.png`
  - `fig2b_unemployment_county_change.png`
  - `fig3_college_divergence.png`
  - `fig4_global_setbacks.png`
- `answers/sources.txt` says no web pages were opened. It lists the local reference pages and data sources for citing.
- Code is in `work/` (`common.py` and one script per figure, plus two intermediate CSVs). `work/README.md` has the regeneration commands. There are no manual steps.

**Stories**
- Q1: the female-minus-male life expectancy gap, 1960–2023 (World Bank). `fig1a` draws every country as a gray line with seven highlighted; `fig1b` is an arrow chart of 31 countries from 1960 to 2023.
- Q2: the rural-urban unemployment penalty flipped in 2020. `fig2a` is labor-force-weighted lines for four county settings with a rural-minus-metro gap bar panel. `fig2b` is county-level strip plots comparing the Great Recession with the pandemic.
- Q3: the gap in college attainment between metro and rural counties widened from 1990 to 2019–23. The typical big-metro lead over remote rural counties grew from 4.1 to 11.4 points. `fig3` is a county scatter plus per-setting arrows.
- Q4: COVID-19 was broad but not deep as a setback in life expectancy (Our World in Data, 1950–2023). 58 and 72 of 236 countries had drops of a year or more in 2020 and 2021, against about 3 in a typical year. Only 6 of the 76 large setbacks (5+ years lost) bottomed out in 2020–21, none deeper than 6.4 years. `fig4` is a bar panel plus a severity and recovery dot plot.

**Things to know**
- `full_census_dataset.csv` is comma-separated and Latin-1 encoded, despite the data README calling it tab-separated.
- I corrected claims that did not match the numbers while drafting. The `fig2b` title now reads "Both downturns hit cities harder, but the pandemic hit them much harder" because medians rose less in rural counties in both periods. `fig3` says the metro lead "roughly tripled" and not that remote counties "barely moved".
- Country selections in `fig1a`/`fig1b` are my judgment, and the captions say so.
- No packages were installed, no environment was created, and nothing outside `answers/` and `work/` was changed. Only pandas, numpy and matplotlib in `p314` were used.
