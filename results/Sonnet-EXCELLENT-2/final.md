I made all six figures and the written answers, plus the code and a README for regenerating them.

All paths are under `/Users/mlgleich/Projects/765/765-DE4-2-Experiment/runs/Sonnet-EXCELLENT-2/`.

**Written answers**
- `answers/answer.md` is numbered 1–20 to match the Canvas questions. It includes the critique of the "Income inequality varies across states" chart, the two comparisons, and the disclosure.
- The disclosure says the AI wrote everything at your request, as an instructor example and not a student submission.
- `answers/sources.txt` says no web pages were opened.

**Figures** (in `answers/figures/`)
- **Q1, life expectancy (World Bank, sex-split):** the story is that women's advantage rises as life expectancy rises, then shrinks for the longest-lived countries, with Russia and Nigeria as exceptions.
  - `q1_primary_connected_scatter.png` plots the female-minus-male gap against both-sex life expectancy, with 217 grey country paths, a median curve, and six highlighted countries.
  - `q1_alternate_small_multiples.png` is a 3×3 grid of gap over time for nine countries, each against the median country.
- **Q2, census:** the story is that nearly every county gained in college attainment from 1990 to 2019-23, but the metro lead over rural counties widened.
  - `q2_primary_scatter.png` is a county scatter of 1990 against 2019-23 college share, with dot size for population and group medians.
  - `q2_alternate_range_dumbbell.png` shows the nine county types with middle-half bars, medians and change labels. The median gap between the largest-metro and most remote rural counties went from about 4 to about 11 points.
- **Q3, `q3_unemployment_by_education.png`:** unemployment by quartile of 1990 college share, with a bar panel of the least-educated minus most-educated gap. The gap is positive every year through 2019 and peaks at +2.7 points in 2009. In 2020 it flips to −0.7, and the third quartile is hit hardest.
- **Q4, `q4_covid_recovery_arrows.png`:** arrows from each country's 2021 to 2023 life expectancy relative to 2019, for a deliberately selected set of countries. The countries with the biggest 2021 losses (Latin America, South Africa, India) are back at or above 2019. Germany, Canada and the US, which lost less, are still below.

**Work files:** `work/README.md` has the regeneration commands; the other files in `work/` are the scripts that build the figures. I used only pandas, numpy and matplotlib from the existing `p314` environment, with no installs, no virtual environment and no manual steps. To regenerate, run `fig_q1.py` and `fig_rest.py` from `work/` with `/opt/anaconda3/envs/p314/bin/python`.

**Caveats**
- The USDA county-type labels in Q2 (for example "Urban 20k+, next to metro") are my paraphrase of the codes from memory, and the figure caption says so. Please check them against the USDA definitions if you cite them.
- Connecticut is excluded from the Q2 comparison because its counties changed.
- West Bank and Gaza appears in the Q4 figure as an outlier and is flagged in the caption as war, not COVID.
- The country and county selections in Q1 and Q4 are deliberate, and the captions say so.
