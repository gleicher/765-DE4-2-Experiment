# Design Exercise 4-2 — instructor review example

This is an AI-created example for private instructional review, not a student submission. The numbered responses follow the Canvas survey.

## 1. Critique of the supplied visualization

The connected dots make the within-state range easy to see, and the blue/orange endpoints clearly distinguish maximum and minimum county median household income. Ordering the selected states by their maximum/minimum ratio helps communicate the intended comparison. The ratio labels add useful information because the length of each gray line encodes a dollar difference, not that ratio.

The main weakness is the claim about “income inequality.” Variation among county medians does not measure inequality among households: a county can have a high median and substantial internal inequality. The title should say “County median household income varies within states,” and the caption should describe the maximum/minimum ratio as a measure of between-county variation. The caption also says “times larger,” which is ambiguous; “3.78 times as high” would be clearer. Because only selected states are displayed, the caption’s lowest/highest claims need a clearly defined universe and evidence that all states were considered. States with different numbers of counties also have different opportunities to produce extreme values, making the range a limited comparison.

I would retain the endpoint comparison, use horizontal rows to make state labels easier to follow, rename the legend to “Highest county median” and “Lowest county median,” label the income axis in dollars, and shorten the caption. Adding the median county and an interquartile range would communicate more than two extremes. The chart should identify its data source and explain selection explicitly. These changes would preserve the useful comparison while making its interpretation more defensible.

## 2. Story/Question 1

How did the female–male life expectancy gap change from 1990 to 2023 in six selected countries? France, Sweden, and the United States show substantial narrowing, India shows widening, and Russia and Japan have similar endpoints despite changes between them.

## 3. First visualization for Story 1

Upload `figures/01_life_gap_lines.png`.

## 4. Rationale for the first visualization

Small multiples give each country its own panel while sharing the same time range and 0–14-year vertical scale. This prevents Russia’s larger gap from obscuring the smaller gaps and makes relative magnitudes comparable. I compute female minus male life expectancy so the gap is directly visible instead of requiring viewers to subtract two curves. Annual lines preserve the timing of changes: Russia’s large fluctuations contrast with Sweden’s steadier narrowing. Endpoint labels make the current size of each gap easy to read. The caption identifies the source and states that these are deliberately selected examples, not a global sample. The figure describes estimated differences and does not attribute them to a cause.

## 5. Second visualization for Story 1

Upload `figures/02_life_gap_dumbbell.png`.

## 6. Rationale for the alternate visualization

A horizontal dumbbell compares 1990 and 2023 on a common positional scale. Open orange circles and filled blue circles distinguish the years using both fill and color. The connecting segment shows the size of the endpoint change; signed labels explicitly identify widening or narrowing. Sorting countries by their 2023 gap makes the current ordering immediate. A zero-based axis anchors the magnitude of the gap. The caption warns that this is an endpoint comparison, so a short segment should not be interpreted as stability throughout the period.

## 7. Comparison of the Story 1 visualizations

The small multiples are better for understanding trajectories. For example, Russia’s nearly unchanged endpoints conceal a pronounced rise and subsequent fall, and Japan’s gap also rose before narrowing. Their weakness is that comparing countries requires looking across panels, and exact endpoint differences are not directly labeled. The dumbbell is better for comparing current gaps and net change quickly, but it deliberately loses the intervening history. I would use the lines for a discussion of change over time and the dumbbell for a compact summary. Together they show why an endpoint comparison can be accurate yet incomplete.

## 8. Story/Question 2

In Wisconsin in 2023, how often did net migration offset natural population loss, and how did the pattern differ between metro and nonmetro counties? Migration offset natural loss in 41 of the 51 counties with negative natural change; natural loss was much more common among nonmetro counties.

## 9. First visualization for Story 2

Upload `figures/03_wisconsin_scatter.png`.

## 10. Rationale for the first visualization

The scatterplot positions each county by natural change and net migration, both measured per 1,000 residents. Rates allow counties of different sizes to be compared. The vertical zero line separates natural loss from natural gain; the shaded negative side reinforces this distinction. The dashed line represents natural change plus net migration equal to zero. Within the shaded area, points above the diagonal have enough net migration to offset natural loss. Metro and nonmetro counties use different shapes as well as colors. Three labels give recognizable examples without overwhelming the other points: Adams has substantial natural loss and migration gain, Dane has both components positive, and Milwaukee has migration loss. All 72 counties fit within the displayed range. The caption distinguishes this two-component balance from official population change, which also includes a residual.

## 11. Second visualization for Story 2

Upload `figures/04_wisconsin_counts.png`.

## 12. Rationale for the alternate visualization

The stacked horizontal bars reduce each county to one of three mutually exclusive categories: nonnegative natural change, natural loss offset by migration, or natural loss not offset. This answers “how often” more directly than counting dots. Segment labels report the exact counts, and total group sizes appear in the row labels. Nonmetro counties account for 40 of the 51 counties with natural loss, and migration offsets loss in 31 of those 40. Metro counties have 11 with natural loss, 10 of which are offset. I use county counts rather than population weighting because the question concerns counties. The count axis and totals make the unequal group sizes explicit; these are not percentages of Wisconsin residents. Category colors encode population-change status in this figure, as indicated by its own legend.

## 13. Comparison of the Story 2 visualizations

The scatterplot preserves the magnitude of both components and shows how far a county lies above or below the balance threshold. It also reveals that natural loss and strong migration gain can occur together. However, overlapping points and the diagonal threshold make precise counting difficult. The bars provide an immediate tally and clear group comparison, but hide county identities, magnitudes, and within-category variation. They also require attention to the different group totals when comparing proportions. I prefer the scatterplot for investigating individual counties and the bars for summarizing the statewide pattern.

## 14. Story/Question 3

How did labor-force-weighted unemployment rates differ between counties classified as metro and nonmetro over 2000–2023? Their broad trends were similar, but the metro rate rose more sharply in 2020; by 2023 both groups were near 3.6%.

## 15. Visualization for Story 3

Upload `figures/05_unemployment_lines.png`.

## 16. Rationale for Visualization 3

Two lines on the same time and rate axes make shared movement and periods of divergence easy to compare. A zero-based percentage axis preserves the scale of the changes; subdued horizontal gridlines support reading values. The 2020 rise is visible against the full history rather than shown in isolation. Direct labels identify the final rates, with a legend supporting identification throughout the series. I sum unemployed people and civilian labor force within each group, then divide; averaging county rates would give a small county the same influence as a large one. The caption states that groups use a fixed 2023 rural–urban classification, so these lines do not represent historical classification changes. Available matched observations are used each year, and the caption identifies this as a calculated county series rather than an official national estimate. Missing counties and boundary changes limit strict comparisons over time.

## 17. Story/Question 4

By 2023, had six selected countries regained their 2019 life expectancy, and did their intervening declines follow the same pattern? India, Sweden, France, and Brazil were above their 2019 levels, while Japan and the United States remained below; the timing and magnitude of the declines differed.

## 18. Visualization for Story 4

Upload `figures/06_life_recovery_heatmap.png`.

## 19. Rationale for Visualization 4

The heatmap subtracts each country’s 2019 both-sexes life expectancy from its annual values. This gives the countries a common baseline and focuses attention on recovery instead of differences in absolute longevity. Red means below the baseline and blue means above; the scale is symmetric around zero so equal gains and losses have equal color strength. Numeric labels provide precision beyond the color encoding, including Brazil’s small positive 2023 difference. Rows are ordered by 2023 change, which makes the recovery comparison immediate, while columns preserve annual sequence. Including the zero-valued 2019 column makes the baseline explicit. The six countries are illustrative selections, and the caption avoids treating contemporaneous declines as proof of a particular cause. This figure shows changes in life expectancy at birth, not observed lifespans of people born in these years.

## 20. Tools, processing, and AI disclosure

This complete example was created by OpenAI Codex at the instructor’s request for private instructional review. Codex selected the stories, examined the saved assignment and critique image, wrote the Python script, computed derived measures, generated the six figures, inspected rendered output, and drafted the critique and rationales. The conceptual choices and writing are AI-generated; they should not be represented as independently produced student work. No human CLO participation or peer feedback is claimed.

Tools used: Python 3.14 in the existing `p314` conda environment; pandas for reading and transforming data; NumPy for derived classifications; Matplotlib for static charts; and Pillow for a review contact sheet. No packages were installed and no external pages were opened. The saved course materials and supplied data were the only information sources.

The supplied life expectancy CSV was reshaped by country, year, and sex. Story 1 uses female minus male estimates for six named countries in 1990–2023. Story 4 uses both-sexes estimates for six countries in 2019–2023 and subtracts each country’s 2019 estimate. No regional aggregates were mixed into either selected-country comparison. Country selections illustrate contrasting patterns and do not support worldwide prevalence claims.

The supplied census file was read as comma-separated with CP1252 decoding; its actual format differs from the tab-separated description in the readme. County rows were selected using a nonmissing 2023 Rural–urban Continuum Code; state and national total rows were excluded. Codes 1–3 define metro and 4–9 define nonmetro. The Wisconsin figures use all 72 counties and the provided 2023 natural-change and net-migration rates. The classification uses their sum, not official population change. The national unemployment figure excludes Puerto Rico, retains available county observations with both unemployed and positive civilian labor-force counts, and computes 100 × sum(unemployed) / sum(labor force) within each group each year. It uses fixed present-day groups and is descriptive.

The source script and derived tables are preserved in `work/`. `work/README.md` explains regeneration. All six upload files are single-page PNGs with embedded titles, units, captions, and source information.
