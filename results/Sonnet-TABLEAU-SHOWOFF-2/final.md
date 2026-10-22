The six figures, the Canvas answers, a sources file and the work README are all in place. I did not use Tableau. The figures are matplotlib and pandas images (p314 Python) styled to look like Tableau worksheets, and answer 20 says so, along with the AI disclosure. I viewed each PNG and fixed layout and caption errors. I did not re-open `q1b` after the last small edit, which removed a stray "Year" label.

Stories and figures, all in `/Users/mlgleich/Projects/765/765-DE4-2-Experiment/runs/Sonnet-TABLEAU-SHOWOFF-2/answers/figures/`:
- **Q1, life expectancy: is the female advantage changing, and is it the same everywhere?**
  - `q1a_gender_gap_lines.png`: lines of the female-minus-male gap by income group. The high-income gap peaked at 7.5 years in 1994 and fell to 5.7. The groups now sit between 3.8 and 5.7.
  - `q1b_gender_gap_highlight_table.png`: highlight table of income groups and regions by decade.
- **Q2, census: did the 2020 pandemic hit big-city and rural unemployment differently?**
  - `q2a_unemployment_lines.png`: lines for three county groups, 2000-2023.
  - `q2b_unemployment_change_bars.png`: the 2019 to 2020 change for each of the nine rural-urban codes.
  - Nonmetro counties had the higher rate every year from 2000 to 2019. In 2020 large-metro counties went from 3.5% to 8.6%, against 4.1% to 7.0% for nonmetro.
- **Q3, census: has the metro-rural education gap narrowed or widened?**
  - `q3_education_dumbbell.png`: dumbbell plot of bachelor's-degree share, 1990 vs 2019-23, by rural-urban code. The gap between the largest metro and most remote rural counties grew from 13 to 20 points, even though the rural share roughly doubled.
- **Q4, life expectancy: how much did the pandemic take, and was it recovered?**
  - `q4_covid_life_expectancy_drop.png`: the 15 countries with the largest 2019 to 2021 drop. 14 of the 15 were back at or above their 2019 level by 2023; Lebanon was not.

`answers/answer.md` has answers 1-20 numbered as in Canvas. Answer 1 is a critique of the sample dumbbell figure in `reference/images/to-critique.png`.

Things to know before you use it:
- The data files carry no region field for countries, so the Latin America point in answer 19 comes from outside knowledge. The answer says so.
- The USDA rural-urban code descriptions used as axis labels also come from my own knowledge, not from the saved pages.
- I removed World Bank aggregate rows by a hand-written list of codes, leaving 217 countries for Q4. 17 counties with no 2023 rural-urban code are excluded, and the captions say so.
- Unemployment and degree shares are pooled across counties (sums, not averages of county rates). For degree shares, adult counts are recovered as degree-holder count divided by percent.
- `answers/sources.txt` records that no web pages were opened.

To regenerate, run `/opt/anaconda3/envs/p314/bin/python -I work/make_figs.py` from the run folder. Details are in `work/README.md`, and intermediate tables are in `work/intermediate/`. Nothing was installed and no virtual environment was created.
