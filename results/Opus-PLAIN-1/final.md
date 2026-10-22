I finished the assignment. The six figures are in `answers/figures/`, and `answers/answer.md` has answers 1–20, numbered to match the Canvas questions. Every figure comes from a script in `work/`, and `work/make_all.sh` rebuilt all six from scratch without errors. I looked at each rendered image and fixed the label collisions I found. I didn't open any web pages, so `answers/sources.txt` says that and lists the local reference files I used.

**Stories and figures:**
- **Q1, life expectancy (World Bank data):** how far back COVID pushed each country, counted as years of progress erased, and whether it had recovered by 2023. For example, Jamaica's 2020–22 low matched 1980, Mexico's matched 1992 and the US's matched 1996. Even so, 184 of 214 countries were back at or above their 2019 level by 2023.
  - `q1a_pandemic_setback_small_multiples.png`: 16 small line charts, each with an arrow from the pandemic low back to the year with the same level.
  - `q1b_pandemic_setback_scatter.png`: every country, plotting life expectancy lost against years of progress erased, colored by whether it recovered.
- **Q2, census:** where population growth comes from in each type of county, July 2020 – June 2023. Large metros lose residents to moves within the US and grow from births and immigrants. Rural counties have more deaths than births and depend on people moving in, mostly when they are next to a metro.
  - `q2a_population_change_components_bars.png`: stacked bars going left for losses and right for gains, with a marker for the net change.
  - `q2b_population_change_components_heatmap.png`: the same breakdown year by year, with values printed in each cell.
- **Q3, census:** `q3_education_urban_rural_gaps.png`. Between 1970 and 2019–23 the urban–rural gap in adults without a high-school diploma shrank from 16 to 2 points. The gap in college degrees grew from 7 to 21 points.
- **Q4, life expectancy (Our World in Data):** `q4_life_expectancy_50_to_70.png`. The early countries took 45–95 years to go from a life expectancy of 50 to 70, while later ones often took 17–40. The chart also shows the 58 countries that reached 50 but not yet 70 as "years so far", so the late starters don't look faster than they are.
- **Q1 (critique):** I wrote it with good, ugly and bad points and a suggested redesign. Two main points:
  - The bars show the dollar difference while the story is the ratio.
  - Its "most equal" states look like a data error: Wyoming's 1.01x would be about 2.4x using this year's 2022 county data.

**Before you submit:**
- **AI disclosure (Q20):** I wrote it to say that Claude Code explored the data, chose the stories, wrote the code, made the figures and drafted all the text, including the critique. The course policy says your assignments should come from you and that critiques should be your own opinion. Treat the stories, rationales and especially the critique as drafts to review and rewrite, and change the Q20 wording if you change how the work was done.
- **Data quirks** (also in `work/README.md`):
  - `full_census_dataset.csv` is really comma-separated and Latin-1 encoded, even though the readme says tab-separated.
  - I dropped the Central African Republic from Q1 because its World Bank numbers are implausible (31.5 → 50.6 → 18.8 → 57.4).
  - I removed the World Bank's regional and income groups by keeping only codes Our World in Data uses for real countries.
- **Outside knowledge:** two notes in the figures go beyond the data, which the assignment allows. Q4 says HIV/AIDS held back southern Africa, and it says later countries "caught up with tools the pioneers had to invent".

**Tools:** Python from `p314` with pandas, numpy and matplotlib. I installed nothing and changed no toolchains. There are no manual steps; `work/README.md` explains how to regenerate everything.

Files are in `/Users/mlgleich/Projects/765/765-DE4-2-Experiment/runs/Opus-PLAIN-1/`:
- `answers/answer.md`
- `answers/sources.txt`
- `answers/figures/` (6 PNGs)
- `work/README.md`
- `work/make_all.sh`
- `work/intermediate/` (computed CSVs)
