The example response is finished. `answers/answer.md` has all 20 Canvas answers, numbered to match, and six figures are in `answers/figures/`. I viewed each figure once it was rendered and fixed overlapping labels, truncated titles and several wrong numbers in captions.

**Figures and stories**
- **Q1 (life expectancy, World Bank):** is women's lead over men shrinking? The finding is that it fell in the US, grew in Russia and the post-Soviet states, and went from negative to positive in South Asia.
  - `q1_primary_gender_gap_lines.png` is a line chart of the female-minus-male gap, with 5 countries highlighted over a gray background of all countries.
  - `q1_alt_gender_gap_dotplot.png` is a dot plot of 18 countries for 1960, 1990 and 2023.
- **Q2 (census, unemployment):** how did the Great Recession and the 2020 pandemic hit big-city and rural counties?
  - `q2_primary_unemployment_lines.png` is a line chart of pooled unemployment rates for four rural-urban groups, 2000-2023.
  - `q2_alt_unemployment_change_strip.png` is a county-level strip plot of unemployment-rate change in 2007-09 and 2019-20, with all nine rural-urban codes.
  - In 2020 the rise shrinks steadily with the size of the place, from +3.4 points in big metros to +1.5 in the most remote counties. In 2009 most groups rose by a similar amount, and the most remote counties rose least.
- **Q3 (census, education):** `q3_education_scatter.png` plots each county's bachelor's-degree share in 1990 against 2019-23. Every county gained, and the gap between the median large-metro and remote county grew from about 3 to 11 points.
- **Q4 (Our World in Data life expectancy):** `q4_covid_life_expectancy.png` plots each country's 2019-21 loss against its 2021-23 rebound, with a full-recovery diagonal. 211 of 235 countries are back above their 2019 level.

**Disclosure and critique**
- **Q20 disclosure:** it states plainly that Claude (Sonnet 5.5, via Claude Code) did all of the work at the instructor's request, as an example response and not a student submission.
- **Q1 critique:** Canvas question 1 is the critique, and I wrote it on `reference/images/to-critique.png`, the Virginia income dumbbell chart.

**Data choices**
- The Central African Republic is excluded from Q4 because its 2019 value (31.5 years) is implausible, and this is noted on the figure.
- 17 counties with no rural-urban code (Alaska, Connecticut and one in Montana) are omitted from the census charts.
- Regional and income aggregates are removed from the World Bank data by keeping only countries that also appear in the Our World in Data file.
- The Q2/Q3 text uses my own knowledge of what the rural-urban continuum codes mean. That is a mild outside-knowledge use.

**Sources and tools**
- `answers/sources.txt` says no web pages were opened.
- Everything was drawn with pandas and matplotlib in `p314`, and nothing was installed. `work/README.md` gives the regenerate command, `/opt/anaconda3/envs/p314/bin/python -I work/make_figures.py`, run from the project root. There are no manual steps.

Files are in `/Users/mlgleich/Projects/765/765-DE4-2-Experiment/runs/Sonnet-CAREFUL-2`:
- answers/answer.md
- answers/sources.txt
- answers/figures/
- work/make_figures.py
- work/README.md
- work/gender_gap_by_country_year.csv
- work/unemployment_rate_by_group.csv
