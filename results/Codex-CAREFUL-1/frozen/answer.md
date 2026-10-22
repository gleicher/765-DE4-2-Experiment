# Design Exercise 4-2

Draft answers below follow the Canvas question numbers. Questions 3, 5, 9, 11, 15, and 18 are image uploads. Review the draft in your own words before submitting, particularly the critique and rationales; the course policy asks for your judgments and requires attribution of AI assistance.

## 1. Critique

The paired dots make each state's minimum and maximum county median household income easy to compare. Blue and orange distinguish the endpoints, and the connecting lines show the dollar spread. The ratio labels add a useful second way to compare states: California has a large dollar gap, but Alabama has a slightly larger maximum-to-minimum ratio. Sorting by that ratio helps reveal the pattern.

The main problem is the title's use of “income inequality.” Differences between county median incomes describe geographic variation; they do not measure inequality among households within a state. I would title it “County median household incomes vary more in some states.” The caption should also say “times as high,” rather than “times larger,” to make the ratios unambiguous. The caption explains that these are selected states, but “states we were interested in” does not explain the extra six choices, and the graphic does not distinguish them from the extremes. I would identify those groups or show all states. Finally, I would remove the duplicate state labels beneath the orange points and rename the legend “Highest county median” and “Lowest county median.” A horizontal version could make the labels easier to scan while preserving the useful range encoding.

## 2. Story/Question 1

Between 1990 and 2023, did the female–male life expectancy gap narrow in France, Sweden, Hungary, the United States, Poland, and Japan, and did narrowing accompany rising life expectancy for both sexes? These illustrative countries show that improvement in overall longevity does not imply the same change in the sex gap everywhere.

## 3. First visualization for Story 1

Upload: `figures/01_life_gap_trajectories.png`

## 4. Rationale

Small multiples separate the countries so twelve lines do not become a crowded overlay. Every panel uses the same time and life expectancy scales, allowing comparisons of both levels and trajectories. Consistent colors identify female and male estimates; the lightly shaded space between them makes the gap visible without adding a third line. Country titles and the 1990-to-2023 gap labels provide quick entry points into the story.

The annual values also show what the endpoints alone miss, including temporary declines and rebounds. Most of these countries combined rising life expectancy with a narrowing gap, while Japan's gap was nearly unchanged. These six countries illustrate contrasts rather than represent the entire world.

## 5. Alternate visualization for Story 1

Upload: `figures/02_life_gap_endpoints.png`

## 6. Rationale

The dumbbell chart isolates the quantity of interest: female life expectancy minus male life expectancy. Hollow dots mark 1990 and filled blue dots mark 2023, so year is recognizable through both fill and the legend. Horizontal position provides a common, zero-based scale for comparing gap sizes; the connectors emphasize each country's change.

Ordering the countries by change brings the biggest reductions to the top. The change column makes direction explicit, and the endpoint labels allow exact comparisons to the displayed precision. France's gap narrowed by about 2.4 years, whereas Japan's changed by only about +0.1 year. Changes are calculated before rounding, so Japan's two displayed endpoints can both read 6.0.

## 7. Comparison of Story 1 designs

The small multiples give more context: whether both sexes improved, when changes occurred, and whether a smooth endpoint comparison hides reversals. Their limitation is that the gap must be judged as a distance between two lines, and comparing six panels takes effort. The dumbbell chart makes the gap and its change much easier to rank, but removes the absolute lifespan levels and everything between the two years. I would use the trajectory view for explaining the pattern and the dumbbell for a quick summary.

## 8. Story/Question 2

By 2023, had employed-resident totals returned to their 2007 levels in fixed groups of metro and nonmetro counties? The nonmetro total remained below its baseline, while both metro groups finished above theirs.

## 9. First visualization for Story 2

Upload: `figures/03_employment_lines.png`

## 10. Rationale

Indexing each group's summed employed-resident count to 100 in 2007 allows relative growth to be compared despite the groups' different sizes. The dashed baseline makes the meaning of “recovered” concrete. Annual lines show the common downturns as well as the later divergence, and direct labels avoid making readers repeatedly consult a legend.

The nonmetro series receives a contrasting orange color. Its 2023 index is 96.6, versus 108.4 and 115.6 for the two metro groups. The county cohort and its 2013 rural–urban classification are held fixed, so annual changes are not caused by swapping counties between groups. The caption distinguishes employed residents from employment rates and jobs located in a county; this chart does not establish why the groups diverged.

## 11. Alternate visualization for Story 2

Upload: `figures/04_employment_heatmap.png`

## 12. Rationale

Rows represent the same three fixed county groups and columns represent individual years. A diverging scale centered on zero separates years above the 2007 baseline from years below it. The symmetric color limits make positive and negative departures comparable, while printed percentages keep the reader from relying on color alone.

The uninterrupted orange nonmetro row supports the main finding: its employed-resident total stayed below 2007 in every later year shown. Metro rows shift toward blue as their totals rise above the baseline. County counts and the caption specify the aggregation, and the year order preserves the chronology. Values are rounded to whole percentages to keep the grid readable.

## 13. Comparison of Story 2 designs

The line chart is better for judging the size and timing of changes, including the sharp 2020 dip. Its direct endpoint labels also make the final comparison immediate. The heatmap is better for scanning which groups were above or below baseline in each year and makes the nonmetro group's persistent shortfall especially obvious. It trades continuous shape and precise differences for a compact annual summary; color and whole-percent rounding can obscure small changes. Both summarize group totals, so neither reveals county-level variation within a group.

## 14. Story/Question 3

Among counties with more deaths than births in 2023, how often was net migration large enough to offset that natural loss, and how did this vary across the nine rural–urban codes? The offset share was higher in the three metro categories than in any of the nonmetro categories.

## 15. Visualization for Story 3

Upload: `figures/05_migration_offsets.png`

## 16. Rationale

The 100% stacked horizontal bars use a common denominator within each row: counties whose natural change rate was negative. Teal represents the share where net migration exceeded that loss; light gray represents the remainder. Aligning the teal segments at zero makes their lengths easy to compare. The metro/nonmetro divider supplies a broad comparison while retaining all nine codes rather than compressing them into two averages.

Percent labels and the count column show both relative frequency and sample size. For example, code 1 has 123 offsets among 164 natural-decline counties, about 75%, compared with 184 of 466, about 39%, in code 9. Each county counts equally; this is a question about the frequency of a county condition, not the share of Americans affected. The caption defines the rate calculation and notes that residual population change is excluded, so the chart does not label these cases as observed total population growth.

## 17. Story/Question 4

How different were the 1960 starting points of seven countries that had relatively similar life expectancy by 2023? Their lifespan spread shrank from 19.2 to 3.2 years, with South Korea and Chile gaining much more than Sweden.

## 18. Visualization for Story 4

Upload: `figures/06_lifespan_catchup.png`

## 19. Rationale

A labeled scatterplot puts each country's 1960 value on the horizontal axis and its 2023 value on the vertical axis. The broad horizontal spread and narrow vertical cluster make the contrast between starting points and contemporary outcomes visible in one view. Direct labels remove the need for seven colors, and each label gives the gain explicitly: South Korea gained about 29.6 years, versus Sweden's 10.3.

The spread annotation quantifies the convergence within this selected set. The axes deliberately use different ranges to keep the remaining 2023 differences readable, and the caption explains that choice. These countries were chosen to illustrate similar recent outcomes, not sampled to estimate worldwide convergence. The chart compares only endpoints and does not identify a cause of the gains.

## 20. Tools, processing, and AI disclosure

These figures were made with Python 3.14 in the existing `p314` environment, using pandas and NumPy for data processing and Matplotlib for static PNG output. Pillow was used to assemble a contact sheet for visual inspection. No packages were installed, and no outside data were added. The course assignment, rubric, policy, dataset notes, and critique image were read from the supplied local files; no websites were opened.

The World Bank file was pivoted by country, year, and sex. Female–male gaps and endpoint changes were calculated from the supplied estimates without smoothing. The trajectory and gap figures use the same six illustrative countries; the endpoint scatter uses seven explicitly selected countries and the “Both” category.

The county file was read as comma-separated text with Windows-1252 encoding, despite its readme's tab-separated warning. FIPS identifiers were retained as strings. Puerto Rico and rows without valid relevant rural–urban codes were excluded. Employment totals use 3,097 counties/equivalents with all 2007–2023 employment values present; seven otherwise eligible incomplete series were removed. Counties were assigned to fixed 2013-code groups, employed-resident counts were summed within each group, and those sums were divided by each group's 2007 total. No county rates were averaged for this calculation.

The migration figure uses 3,106 counties/equivalents with valid 2023 codes and both required rates. It retains negative-natural-change counties as the denominator and counts an offset when natural change rate plus net migration rate is greater than zero. This calculation uses the supplied rounded rates, omits residual change, and weights counties equally. Plotting tables and an audit summary are saved in `work/`.

**AI disclosure:** OpenAI Codex provided substantial assistance: it proposed the stories and chart designs, wrote and ran the data-processing and plotting script, inspected figure layouts, and drafted this critique and the written responses. This is an AI-assisted draft, not an independently authored student submission. The course policy requires my own judgments and responsibility for the submitted work, so I need to review the charts and revise the critique and explanations to reflect my understanding before submission.
