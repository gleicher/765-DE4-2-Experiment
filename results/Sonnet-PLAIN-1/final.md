The answers, six figures and work files are all done. I looked at every figure after rendering and fixed overlapping labels and clipped titles.

**Files**
- `answers/answer.md`: numbered 1–20 to match the Canvas order. Q1 is the critique of `reference/images/to-critique.png`.
- `answers/figures/`:
  - `q1a_shocks_small_multiples.png`
  - `q1b_depth_vs_recovery.png`
  - `q2a_education_lines.png`
  - `q2b_education_distributions.png`
  - `q3_gender_gap_1960_vs_2023.png`
  - `q4_migration_tile_map.png`
- `answers/sources.txt`: I opened no web pages. It says so and lists the original 765-25 course pages and the data repo, in case you want to cite them.
- `work/make_figures.py`: one script that draws all six figures.
- `work/README.md`: regenerate with `/opt/anaconda3/envs/p314/bin/python -I work/make_figures.py`. There are no manual steps.

**Stories**
- **Q1 (life expectancy):** how deep are single-year life-expectancy collapses, and how long do countries take to recover? This uses the Our World in Data file. Version A is small multiples with the loss shaded. Version B is a scatter of depth against years to recover.
- **Q2 (census):** how did the gap in bachelor's-degree attainment between big-metro and rural counties change from 1990 to 2019-23? Version A is lines by rural-urban county code (the median gap grew from 4 to 11 points). Version B shows every county as a dot, with quartile bars and median arrows.
- **Story 3 (World Bank):** a scatter of the female-minus-male life-expectancy gap in 1960 against 2023. The female advantage grew in 142 countries and shrank in 70.
- **Story 4 (state census data):** a tile-grid map with three bars per state for net domestic migration in 2021, 2022 and 2023.

**Data notes**
- `full_census_dataset.csv` is actually comma-separated and latin-1 encoded, although the readme says tab-separated. `aggregate_census_dataset.csv` is tab-separated.
- Five countries with erratic life-expectancy series (Central African Republic, South Sudan, Somalia, Lebanon, Eritrea) are excluded from Q1. This is stated on the figures and in the answers.

**Before you submit**
- Answer 20 discloses that Claude (Sonnet 5.5, via Claude Code) wrote the code, designs and text, and says you should review them before submitting.
- The Q1 critique is written from the saved chart as my own critique, so you may want to put it in your own words.
- Answer 7 ("Compare your two visualizations that answer Question 1") is the cell I'd read twice, since it carries the pros and cons.
