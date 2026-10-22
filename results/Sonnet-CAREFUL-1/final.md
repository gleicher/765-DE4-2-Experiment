The answers and six figures are done. I checked every figure visually except the final tweak to the Cook County label in q4, which I regenerated but didn't re-view.

**Files**
- `answers/answer.md`: numbered 1–20 to match the Canvas order. Q1 is the critique of the provided Tableau chart. Q2–Q7 are story 1 (Life Expectancy), Q8–Q13 story 2 (Census), Q14–Q16 viz 3, Q17–Q19 viz 4, and Q20 how it was made. The figure files are named in the upload questions.
- `answers/figures/`:
  - `q1_a_gap_scatter.png`
  - `q1_b_gap_lines.png`
  - `q2_a_education_lines.png`
  - `q2_b_education_dumbbell.png`
  - `q3_covid_losses.png`
  - `q4_migration.png`
- `answers/sources.txt`: I opened no web pages. It lists the three course pages the saved `reference/` files came from and the data sources.
- `work/README.md` plus the scripts `common.py` and `fig1.py` to `fig4.py`. To regenerate, run `for f in fig1 fig2 fig3 fig4; do /opt/anaconda3/envs/p314/bin/python $f.py; done` from `work/`. There are no manual steps.

**The four stories**
1. **Life expectancy, female advantage since 1960:**
   - **Finding:** The female–male gap widened in 128 of 213 countries and narrowed in 55. The median gap rose from 4.1 to 5.0 years.
   - **Designs:** The first figure is a scatter of 1960 gap vs 2023 gap, and the second is gap trajectories for six countries over a band for the middle 80% of countries.
2. **Census, college attainment by county type:**
   - **Finding:** The median large-metro county went from 15% to 32% with a bachelor's degree. Small-town and rural counties went from about 10% to 19%, so the gap grew from about 4 to 12.5 points.
   - **Designs:** The first figure is lines for four county groups, and the second is a dumbbell for all nine county-type codes.
3. **Life expectancy, COVID losses 2019 to 2021 and recovery by 2023:**
   - **Finding:** 84% of countries lost life expectancy. 8 of the 10 biggest losers are in Latin America, and 23 of the top 25 were back at 2019 levels by 2023.
   - **Design:** One chart for the 25 biggest losers, with 2019, 2021 and 2023 marked for each country.
4. **Census, net domestic migration 2021–23 vs county size:**
   - **Finding:** The 49 counties of 1M+ people lost about 25 residents per 1,000, while counties of 25k–500k gained about 18 per 1,000.
   - **Design:** A scatter of all counties plus a bar summary by county size.

**Things you may want to change**
- **Aggregates:** The World Bank file includes regional and income aggregates. I removed them by keeping only country codes that appear in the Our World in Data file.
- **Region grouping:** The Latin America grouping in viz 3 is my own hand-picked list of countries.
- **Census file:** It needed latin-1 encoding, and I dropped the state and US summary rows.
- **AI disclosure:** Q20 includes a line saying the work was done with Claude. Edit it to match what you want to disclose.
