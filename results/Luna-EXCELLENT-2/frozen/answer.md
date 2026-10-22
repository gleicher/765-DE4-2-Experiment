# Design Exercise 4-2 — Canvas responses

**1. Critique of the provided “Income inequality varies across states” visualization**

The paired minimum and maximum dots connected by a line make each displayed state’s county-income range easy to scan, and the max/min ratio gives a compact sense of relative spread. The caption also helps explain what the marks represent. However, the title sounds like a state-wide comparison while only 16 states appear; the selection rule for the “additional interested states” is unclear, and the state order does not reveal a ranking. More importantly, a county minimum-to-maximum range is a fragile measure of income inequality: one unusual county can dominate it, and it says nothing about the distribution’s middle. The ratio can also make states with different income levels seem directly comparable when their absolute spreads differ. Several ratio labels crowd together, while the zero-based vertical scale uses space without helping compare the gaps. I would include all states or state an explicit selection rule, sort by a defensible spread measure, and show a robust interval such as the 10th–90th percentile alongside a median. That would retain the useful range comparison while representing typical counties more faithfully.

**2. Story/Question 1**

Among the country and regional series in the World Bank life-expectancy file, how did the sharpest 2019–21 declines recover by 2023? Did the six deepest declines return to their 2019 levels?

**3. Visualization 1**

[Figure 1 — Six largest declines as indexed small multiples](figures/01_life_expectancy_recovery_small_multiples.png)

**4. Rationale for Visualization 1**

Each small multiple uses that series’ 2019 value as zero, so the viewer can compare the size and timing of losses without confusing a country’s starting level with its subsequent change. A shared vertical scale preserves comparability across panels. The red 2021 point marks the trough in this selected set, the teal endpoint shows 2023, and the dashed zero line makes return to baseline visible. The selection is explicit: the six largest 2019–21 declines among series with complete values. Five had reached or exceeded their 2019 level by 2023; Lebanon remained slightly below. This focused view gives the recovery sequence room to breathe, while the caption notes that these are reporting entities and that the pattern is descriptive rather than a causal estimate.

**5. Visualization 2**

[Figure 2 — All reporting series, shock versus endpoint](figures/02_life_expectancy_recovery_overview.png)

**6. Rationale for Visualization 2**

This scatterplot answers the same question with a broader frame. Each point compares a series’ 2019–21 change with its net 2019–23 change; the horizontal zero line separates loss from no loss, and the vertical zero line distinguishes series that ended below or at/above baseline. Color makes the endpoint status legible, while gold rings connect the six largest declines from Figure 1 to the full set. The callout reports that 228 of 265 complete reporting series (86%) were at or above their 2019 level by 2023. Labels draw attention to several exceptions, including West Bank and Gaza, whose large later decline is not attributed to the pandemic in the chart.

**7. Compare the two visualizations for Question 1**

Figure 1 is stronger for understanding *how* the six deepest declines unfolded: the annual path shows that most of the rebound happened by 2022. Its limitation is its narrow, deliberately selected set. Figure 2 shows how those cases fit within all 265 complete reporting series and makes the share returning to baseline immediately apparent. Its two-change encoding compresses five years into endpoints, so it cannot show when recovery occurred. The small multiples emphasize trajectory and magnitude; the scatterplot emphasizes coverage and outcome.

**8. Story/Question 2**

When a county has natural population decrease, how often does net migration restore positive population change—and does that differ from metropolitan counties to the most rural counties?

**9. Visualization 1**

[Visualization 1 for Question 2 — Natural change and net migration rates](figures/03_q2_migration_natural_change.png)

**10. Rationale for Visualization 1**

Each county is a point, with natural change on the horizontal axis and net migration on the vertical axis. The dashed diagonal marks where the rates sum to zero: a county above it has positive total population change, including counties where migration offsets natural decrease. Color and shape distinguish metro, nonmetro-town, and rural RUCC groups. This keeps the underlying rate magnitudes visible and lets viewers inspect the spread and exceptions, not only group averages. The axis ranges focus on the dense center; edge triangles mark counties beyond those limits. Counties are equally weighted, so this describes county patterns rather than the experience of the average resident.

**11. Visualization 2**

[Visualization 2 for Question 2 — Population-change outcomes by RUCC](figures/04_q2_population_change_by_rucc.png)

**12. Rationale for Visualization 2**

The 100% stacked bars recast each county’s two rates as one of four outcomes: population decline because natural decrease was not offset; decline because migration erased natural increase; growth because migration offset natural decrease; or growth because natural increase remained positive. Bars compare these shares across all nine RUCC codes, and sample sizes appear at right. The callout compares metro RUCC 1 and most-rural RUCC 9: among counties with natural decrease, migration restored growth in 76% and 41%, respectively. This design gives up rate magnitude to make the frequency of each outcome easy to compare.

**13. Compare the two visualizations for Question 2**

Figure 3 preserves the continuous rates and shows exactly how close a county lies to the zero-growth boundary; it also exposes outliers and overlap among place types. Its many points make exact group frequencies harder to judge. Figure 4 answers “how often?” more directly and keeps all counties visible in the denominator, but it bins rate pairs into four categories and treats a barely positive outcome like a large gain. Together they show both the mechanism and how often it leads to growth.

**14. Story/Question 3**

From 1960 to 2023, did the female life-expectancy advantage widen or narrow as life expectancy rose, and is the gap change associated with the size of the overall gain?

**15. Visualization 3**

[Visualization 3 — Life-expectancy gain and change in the female–male gap](figures/05_visualization3_life_sex_gap.png)

**16. Rationale for Visualization 3**

Each point represents a reporting series with complete 1960 and 2023 values. The horizontal axis shows the gain in both-sex life expectancy; the vertical axis shows how the female-minus-male gap changed. The zero line separates a widening from a narrowing advantage, while color makes that split visible. Labels identify some of the largest expansions and contractions rather than implying a uniform trend. In 182 of 263 complete series (69%), the gap widened; the correlation between overall gain and gap change is weak (Pearson *r* = 0.11). The chart is descriptive and retains aggregate series, as noted in its caption.

**17. Story/Question 4**

Did counties with lower bachelor’s attainment catch up between 1990 and 2019–23, or did the typical-county metro–rural difference widen when counties are grouped by their 2023 Rural–Urban Continuum Code?

**18. Visualization 4**

[Visualization 4 — Bachelor’s attainment medians and ranges by RUCC](figures/06_visualization4_census_bachelors_attainment.png)

**19. Rationale for Visualization 4**

The connected points compare the median county bachelor’s attainment in 1990 and 2019–23 across all nine 2023 RUCC groups; thick vertical marks show each group’s interquartile range. Comparing medians focuses the story on a typical county without letting the largest counties dominate, while the ranges show substantial within-group variation. Attainment rose in every group, but the median gap between RUCC 1 and RUCC 9 grew from 3.9 to 10.6 percentage points. The classification caveat matters: the data provides 2023 RUCC codes, which I use to group both attainment endpoints; this does not reconstruct each county’s historical urban/rural status.

**20. How I made the visualizations**

I used Python 3.14 from the curated `p314` environment with pandas, NumPy, and Matplotlib. The script in `work/make_figures.py` reads the course-provided World Bank and USDA county files and writes the six PNGs to `answers/figures/`. For life expectancy, it pivots the supplied long table to compare annual endpoints, calculate changes from 2019, and derive the female–male gap. For census data, it keeps five-digit county FIPS rows, converts the relevant measures to numeric, adds the natural-change and net-migration rates for the growth boundary, classifies counties into the four outcome categories, and summarizes attainment medians and interquartile ranges by 2023 RUCC. I used no outside data and did not browse external pages.

OpenAI Codex (GPT-6) contributed the analysis, story selection, chart designs, Python code, figures, written rationales, critique, and this disclosure response at the instructor’s direction for private instructional review. This is an instructor-requested example, not a student submission. No packages were installed. The figures are generated automatically; the only manual step is to review them and upload the six image files separately where Canvas asks for them.
