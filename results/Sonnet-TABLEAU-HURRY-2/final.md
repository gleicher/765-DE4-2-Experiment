The example response is done: answers to Canvas questions 1-20, six figures, and the work files. I checked each figure by eye and fixed overlapping labels, clipped legends and long titles.

Tableau is not installed and I did not use it. I drew the figures in Python (pandas and matplotlib, via p314) to look like Tableau worksheets. They use the Tableau 10 palette, light gridlines, a left-aligned title, a legend at the right and a caption under the chart. Each design uses only operations Tableau offers: aggregation, color, labels, sorting, a Top-N filter, reference lines, trend lines and simple calculated fields. The disclosure answer (Q20) says all of this, that an AI produced the work at your request, and that it is not a student submission. I installed nothing and created no virtual environment.

**Stories and figures** (all in `answers/figures/`)
- **Q1 (life expectancy, World Bank file, 213 countries):** has women's life-expectancy advantage grown since 1960?
  - `q1_a_gap_scatter.png` plots each country's 1960 gap against its 2023 gap, with a no-change reference line. The gap grew in 142 of 213 countries (67%).
  - `q1_b_gap_lines.png` shows the gap over time for six highlighted countries, with the all-country median as a baseline. The median went from 4.1 years in 1960 to 5.0 in 2023.
- **Q2 (census):** did the 2020 unemployment spike hit metro counties harder than rural ones?
  - `q2_a_unemployment_lines.png` shows unemployment by year for three county groups. Metro rose 4.6 points (3.6% to 8.2%); the most rural rose 2.4.
  - `q2_b_unemployment_bars.png` shows the 2019-to-2020 increase for each of the nine rural-urban continuum codes, from +5.1 down to +2.1.
- **Q3:** `q3_state_migration.png` shows the top and bottom 10 states for net domestic migration per 1,000 residents, 2020-2023. Idaho is +57 and New York is -44.
- **Q4:** `q4_education_income.png` plots county bachelor's-degree share against median income. Dots are colored metro/nonmetro and sized by population, with a trend line per type.

**Answers and sources**
- `answers/answer.md` is numbered 1-20 to match the Canvas questions. Q1 is my own critique of the sample figure (the `to-critique.png` dumbbell chart).
- `answers/sources.txt` says no web pages were opened.
- `work/README.md` explains the tools and how to regenerate the figures. There are no manual steps.

**Regenerate the figures**
```
/opt/anaconda3/envs/p314/bin/python -I work/make_figures.py
```

**Data quirks** (also in `work/README.md`)
- `full_census_dataset.csv` is comma-separated and Latin-1 encoded, although the readme says tab-separated. The aggregate file is the tab-separated one.
- The migration chart excludes Puerto Rico and Connecticut. The Connecticut data is unusable: the old counties and the new planning regions each have values missing in different columns.
- One county reporting 0% bachelor's share is dropped from the scatter.
- The USDA definitions for continuum codes 4-9 aren't in the data files, so the charts label them only as "nonmetro" and say higher codes are less urban.

Before you paste anything, skim the Q1 critique and the numbers quoted in the rationales.
