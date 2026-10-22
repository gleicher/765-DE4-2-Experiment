The assignment is done: six figures, all 20 Canvas answers, a sources list and a work/README.md. One thing to know before you submit: I wrote answer 20 as a truthful disclosure that an AI agent (Claude, in Claude Code) chose the questions, wrote the code, made the figures and drafted all the text, including the critique. The course policy asks for disclosure, so I didn't write it as if a student had done the work. Edit it if your actual process differs.

I went through each rendered figure for label collisions and checked every number in the titles and captions against the data. All six regenerate cleanly from the scripts, with no manual steps.

**The four stories**
- **Q1 (World Bank life expectancy by sex):** the female-minus-male gap is converging. It is shrinking where it was largest (North America, Europe) and growing where it was smallest (South Asia, Middle East). The spread across regions fell from 7.7 years in 1960 to 3.3 in 2023.
  - Figure 1 is a line chart of the gap with four regions highlighted.
  - Figure 2 is a connected scatter of gap against overall life expectancy, smoothed over 5 years, with 2023 countries as faint background dots.
- **Q2 (census unemployment by the USDA 2015 economic-type column):** each downturn hit a different kind of county. Manufacturing counties led the Great Recession, mining counties were the only type hurt in the 2016 oil bust, recreation counties were hit hardest by COVID, and farming counties had the smallest rise both times.
  - Figure 1 is a line chart of weighted unemployment rates, 2000–2023.
  - Figure 2 shows three panels with one dot per county, the change in unemployment rate, and the median and middle 50%.
- **Q3 (census population change by urban/rural code, 2021–23):** deaths outnumber births in small metros and rural counties, so growth depends on people moving in. The biggest metros lose residents to the rest of the U.S. Remote rural counties stall or shrink; those next to a metro grow. It is a diverging stacked bar of births minus deaths, domestic moves and immigration.
- **Q4 (Our World in Data life expectancy):** at the pandemic low point, the 20 hardest-hit places fell back to levels a median of 18 years earlier (Cuba to 1981, the U.S. to 1996). By 2023, 106 of the 123 places that lost a year or more had recovered. The figure has two panels: years of progress erased, and the drop and recovery.

**Data decisions you may want to know about**
- The census CSV is comma-separated and Latin-1 encoded, not tab-separated as the readme says.
- The economic-type codes 0–5 aren't documented in the file. I mapped them to the USDA names and confirmed the mapping by checking known counties. Puerto Rico is dropped.
- Central African Republic is excluded from Q4 because its series drops 12.7 years in 2022, far beyond any other country. The caption says so.
- The critique (Q1) points out that the chart's Wyoming value of 1.01x looks wrong: in our 2022 data, Wyoming's counties range about 2.4x.

**Other notes**
- I opened no web pages, and `sources.txt` says so.
- Nothing was installed. I used the p314 Python (pandas, matplotlib), and no R.
- I made one wording change to keep the text accurate: the Q1 rationale no longer claims an earlier draft that never existed.

Files are in /Users/mlgleich/Projects/765/765-DE4-2-Experiment/runs/Opus-CAREFUL-1/:
- answers/answer.md
- answers/sources.txt
- answers/figures/
  - q1a_gap_lines.png
  - q1b_gap_trajectories.png
  - q2a_unemployment_lines.png
  - q2b_unemployment_shocks.png
  - q3_population_components.png
  - q4_covid_setback.png
- work/
  - README.md
  - common.py
  - six fig*.py scripts
  - out_*.csv intermediate tables
