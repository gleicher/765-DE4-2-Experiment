# Design Exercise 4-2

Prepared with substantial AI assistance; the disclosure is in answer 20. Answer 1 uses the supplied non-CLO critique option. The image links identify the six separate files to upload.

## 1. Critique

The paired dots and connecting lines make each state’s range of county median household incomes easy to see. Consistent colors separate the maximum and minimum, and the ratio labels offer a second way to compare disparities. The year and caption help explain the measurements.

The main problem is the interpretation: a range of county medians measures geographic differences between counties, not income inequality among households within a state. Two states could have similar county medians but very different household income distributions. The title and caption should say “County median household income varies within states.” The claim that Virginia has the highest inequality also needs to be limited to the selected states and this particular measure. The selection includes “6 additional interested states,” but the selection rule is unclear; showing all states or naming the reason for each selected state would make the comparison more trustworthy.

The ordering is not consistently by ratio, absolute range, or income level, so the viewer must search for the extremes. I would use horizontal dumbbells sorted by max/min ratio, label the county associated with each endpoint, and rename the legend to “Highest county median” and “Lowest county median.” I would retain dollar positions and ratio annotations, because a large absolute gap and a large relative gap are different findings. Darker caption text, less repetition of state labels, and a source note would improve readability and credibility. Finally, extremes depend on how many counties a state contains; a middle-50% interval would help show whether the range reflects broad variation or just two unusual counties.

## 2. Story / Question 1

How did the female advantage in life expectancy change from 1980 to 2023 in France, the United States, Sweden, and Japan? The gap narrowed in the first three countries but grew in Japan, with different paths along the way.

## 3. First visualization for Story 1

Upload [01_life_gap_lines.png](figures/01_life_gap_lines.png).

## 4. Rationale

The line chart uses year horizontally and female minus male life expectancy vertically, turning two sex-specific measurements into the quantity the question asks about. A shared scale makes the size and trajectory of each gap comparable. Four selected countries keep the chart readable while contrasting a sustained decline in Sweden, a later decline in France, a decline followed by a partial reversal in the United States, and an initial widening in Japan. Direct endpoint labels give country names and 2023 values without requiring a separate legend. The vertical scale starts at zero, so the visual difference does not exaggerate the remaining advantage. The caption identifies the calculation and selection limits: these countries illustrate variation rather than represent the world.

## 5. Second visualization for Story 1

Upload [02_life_gap_dumbbells.png](figures/02_life_gap_dumbbells.png).

## 6. Rationale

Each country occupies one row, with a hollow dot for 1980 and a colored dot for 2023. Horizontal position encodes the same female advantage as the line chart, and the connecting segment makes the endpoint change easy to read. The symbols distinguish the years even without color. Endpoint values and signed change labels make both the final gap and the direction of change explicit. Keeping the same country colors across the pair connects the two designs. The arrangement makes Japan’s rightward change stand out against the three leftward changes. The caption warns that the design omits intervening fluctuations.

## 7. Comparison of Story 1 designs

The line chart is better for understanding timing and reversals: Japan’s gap widened and then partly narrowed, while the United States had a recent rebound. It retains every annual value but requires the viewer to follow crossings and estimate changes. The dumbbells are better for comparing the endpoints and reading the signed change quickly; Sweden’s gap fell by about 2.77 years, while Japan’s grew by about 0.64. They sacrifice the trajectories and can make a complicated path look like a simple transition. I would use the lines for a reader investigating change over time and the dumbbells for a concise summary of the net result.

## 8. Story / Question 2

How did the distribution of county bachelor’s-degree attainment change between 2000 and 2019–23 across the nine 2023 rural–urban continuum codes? Every group’s median rose, but substantial differences between groups and among counties remain.

## 9. First visualization for Story 2

Upload [03_education_medians.png](figures/03_education_medians.png).

## 10. Rationale

The connected-dot chart summarizes each code group with its median county percentage, placing both periods on a common horizontal scale. Percentages make counties of different population sizes comparable, and medians avoid allowing a handful of unusually high-attainment counties to dominate the summary. All nine groups appear in code order, with their sample sizes shown. The same counties contribute to both periods within each group, and the 2023 classification is held fixed. Gray and teal identify the earlier and later period; signed percentage-point labels show the magnitude of the group’s change. Code 1 rises from 20.2% to 32.2%, while code 8 rises from 11.5% to about 17.4%. These are changes in group medians, not medians of individual county changes. The caption makes clear that the unit is the equally weighted county, not the average resident, and that 2019–23 is a pooled estimate.

## 11. Second visualization for Story 2

Upload [04_education_distributions.png](figures/04_education_distributions.png).

## 12. Rationale

The small multiples show empirical cumulative distributions for the same county samples. At any attainment percentage, the vertical value is the share of counties at or below that percentage. A curve farther right therefore indicates higher attainment. Common axes, code order, and consistent period colors allow comparisons across all nine panels. Unlike a median alone, the curves reveal spread and tails: counties within a single classification have widely different attainment levels. The instruction above the panels explains how to read the less familiar encoding. Keeping counties equally weighted matches the first design and answers a geographic question rather than a population-weighted one. No smoothing or fitted distribution is applied.

## 13. Comparison of Story 2 designs

The connected medians provide the fastest overview and the most direct comparison of the typical county in each group. Their weakness is that very different distributions can share a median. The cumulative curves reveal whether the shift extends across much of a group and expose overlap between groups; they also allow readers to inspect thresholds other than the median. They take longer to learn and scan, and exact median changes are harder to read. The two designs thus tell the same story at different levels of detail: a concise summary and a distribution-level check.

## 14. Story / Question 3

Among eight selected countries, how did the 2019–2021 change in life expectancy relate to whether 2023 life expectancy exceeded the 2019 baseline? Large early losses did not necessarily leave a country below its baseline in 2023: India exceeded it, whereas the United States remained below it.

## 15. Visualization for Story 3

Upload [05_life_recovery_scatter.png](figures/05_life_recovery_scatter.png).

## 16. Rationale

The scatterplot gives each selected country a point whose horizontal position shows its 2019–2021 change and whose vertical position shows its 2019–2023 change. Both measurements share the same baseline, so the viewer can compare the early setback with the later position without mentally subtracting absolute life expectancies. The horizontal zero reference directly answers whether the baseline was regained, while the vertical reference separates early losses from early gains. Color redundantly identifies the 2023 result, and direct country labels support specific comparisons. India and the United States provide a clear contrast; Japan demonstrates that a nearly unchanged early endpoint does not guarantee a higher 2023 endpoint. The caption limits the finding to the selected countries and distinguishes descriptive changes from an estimate of pandemic effects. Very small positive changes, such as China’s, should be read as near-baseline values rather than strong evidence of improvement.

## 17. Story / Question 4

How often did natural population decrease coexist with nonnegative net migration in 2023, and how did that combination vary across rural–urban county codes? It was the largest category in codes 2–9, reaching about 63% of counties in code 6, but was less common in code 1.

## 18. Visualization for Story 4

Upload [06_population_components.png](figures/06_population_components.png).

## 19. Rationale

The stacked bars classify each county by the signs of natural change and net migration, producing four mutually exclusive categories that sum to 100% within each code group. A percentage scale allows comparison despite unequal county counts; the counts beside the code labels retain that context. The natural-decrease/migration-gain category is highlighted in gold, while the remaining colors distinguish the other combinations. Code order aligns this figure with the education designs. Segment labels provide the larger proportions; narrower segments remain visible without crowded text. Because internal segments lack a common starting position, the design favors the overall mix over extremely precise comparison of the gold segments. Importantly, a positive migration component might be too small to offset natural losses: the caption explicitly avoids interpreting the sign combination as total population growth. Zeros are assigned to the nonnegative categories, as stated in the figure.

## 20. Tools, processing, and AI disclosure

These materials were produced with substantial assistance from OpenAI Codex. Codex proposed and selected the stories, wrote the Python figure-generation script, calculated summaries, designed and rendered the figures, inspected the outputs, and drafted the critique and written answers. They should not be represented as independently authored work; the student should review the reasoning and figures and make their own final decisions in accordance with the course’s AI policy.

The tools were Python 3.14 in the existing `p314` conda environment, pandas for reading and transforming data, NumPy for arrays and classification, Matplotlib for static PNG figures, and Pillow for a contact sheet used during visual checking. Shell tools were used to read local instructions and reference files. No packages were installed, toolchains changed, or external data added. No online pages were opened.

For the life expectancy figures, the supplied World Bank CSV was pivoted by country, year, and sex. Story 1 subtracts male from female life expectancy for each year from 1980 through 2023 and compares those endpoints in the alternate design. Story 3 uses the supplied “Both” series and subtracts 2019 from the 2021 and 2023 values. Country selections are deliberate contrasts, not a representative or random sample. No regional aggregate series are used.

The supplied Census file is comma-separated in this copy, despite the README’s tab-separated warning. It was read using CP1252 encoding, and FIPS identifiers were preserved as strings. Puerto Rico and rows whose FIPS code ends in 000 were excluded; only rows with a valid 2023 rural–urban continuum code from 1 through 9 were retained. This yielded 3,106 county or county-equivalent rows in the 50 states and DC. The education comparison uses 3,089 rows with both attainment percentages; it holds the 2023 group classification fixed and computes unweighted medians and empirical cumulative distributions. It compares 2000 with the pooled 2019–23 estimate, without claiming annual precision or correcting for changes in county boundaries. The population-component chart uses all 3,106 retained rows with both 2023 components, classifies their signs, and divides category counts by each code group’s county count. No interpolation, smoothing, regression, or causal modeling was used.

The reproducible script, intermediate tables, and tool instructions are retained in `work/`. All six figures are separate single-page PNGs with embedded titles, labels, source notes, and interpretation limits.
