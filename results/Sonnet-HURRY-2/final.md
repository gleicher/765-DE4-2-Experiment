The answers, six figures and work notes are all written. I looked at each figure once after a layout fix, but I haven't checked every number in the text against the data.

**What I made**
- `answers/answer.md` has the 20 Canvas items numbered to match the assignment, ready to paste.
- `answers/figures/` has the six PNGs. Each has a title, subtitle, caption, direct labels and a source note.
- `answers/sources.txt` says no web pages were opened. Everything came from your local `reference/` and `data/` files.
- `work/make_figures.py` makes all six figures. `work/README.md` gives the regeneration command, `/opt/anaconda3/envs/p314/bin/python -I work/make_figures.py` from the project root. There are no manual steps.
- I used only pandas, numpy and matplotlib, which were already installed. I made no venv, installed nothing and touched no toolchains.

**Stories and figures** (all in `answers/figures/`)
- **Q1, life expectancy (World Bank): has the female-male gap grown or shrunk since 1960?**
  - `fig1a_gap_scatter.png` is a scatter of each country's 1960 gap against its 2023 gap, with a no-change diagonal.
  - `fig1b_gap_lines.png` is a time series of every country in gray, the median in black, and six highlighted countries.
- **Q2, census: did rural counties keep pace with metros in college education, 1970 to 2019-23?**
  - `fig2a_education_lines.png` is a line chart of the median county, one line per rural-urban code.
  - `fig2b_education_scatter.png` is a county-level scatter of 1990 against 2019-23, with group medians marked.
- **Q3: COVID life expectancy (Our World in Data).** `fig3_covid_life_expectancy.png` is a dumbbell plot of the 2019 to 2021 drop and the 2023 recovery for the 22 worst-hit countries plus the US.
- **Q4: unemployment shocks by county type (census).** `fig4_unemployment_shocks.png` has labor-force-weighted unemployment lines for metro, adjacent-nonmetro and remote counties. A bar panel shows how far each group's rate rose in the Great Recession and in COVID.

**Disclosure and critique**
- Answer 20 says plainly that Claude (Sonnet 5.5, through Claude Code) did all of it as an instructor-requested example, not a student submission.
- The critique (answer 1) covers the provided `to-critique.png` and is written in my own words.

**Data caveats**
- `full_census_dataset.csv` is comma-separated and latin-1 encoded. The data README says tab-separated, which is wrong.
- Real countries were picked by keeping codes that Our World in Data lists as countries, which drops the World Bank regional and income groups.
- A few headline claims were checked against computed values. Bolivia is the largest COVID drop at -6.4 years. Of the 22 worst-hit countries, only Lebanon and Mayotte were still below their 2019 level in 2023.
- The pandemic unemployment rise was +4.6 points in metro counties and +2.8 in remote ones.
- The Ukraine 2022-23 jump in the female-male gap is mentioned in the `fig1b` caption as partly reflecting wartime male mortality.
- The remaining statistics in the prose (for example the education gains) came from my exploration. The captions on figures 1a, 1b, 2a, 2b and 3 compute their numbers in code. Skim answers 2, 8, 13 and 19 before submitting.
