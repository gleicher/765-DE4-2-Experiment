# Design Exercise 4-2 — instructor-requested example

This response was created for the instructor’s private review, not as a student submission. The numbered sections follow the Canvas survey. Each upload section identifies one standalone PNG.

## 1. Critique

The provided chart makes county income ranges easy to compare: the paired dots use a common dollar axis, the connecting lines make the ranges visible, and the max/min labels add relative disparity to the absolute-dollar comparison. Its restrained colors consistently distinguish the two endpoints. The caption also explains that these are county medians, which is essential context.

The main weakness is the leap from **variation between county median incomes** to **income inequality within states**. These extrema do not describe the distribution of household incomes; a state could have similar county medians and considerable inequality within every county. Extrema also depend on the number and boundaries of counties and are sensitive to a single unusual county. The claim that Virginia has the highest inequality is therefore stronger than this measure supports. The chart shows only selected states, so a claim about a national maximum requires verification beyond the displayed subset.

There are two competing measures: connector length encodes a dollar difference, while the ordering and labels emphasize a ratio. California’s larger dollar range but smaller ratio than Alabama illustrates why the distinction matters. I would title it “Selected states differ in the range of their county median incomes,” explicitly label the ordering “sorted by maximum/minimum ratio,” and rename the legend “Highest county median” and “Lowest county median.” Horizontal paired dots would give the state names stable row positions instead of placing them below variable-height endpoints. A separate aligned ratio column would preserve the relative comparison without suggesting that line length encodes it. I would retain a clear dollar scale, replace “Measure Names,” identify the data source and county coverage, and state the selection rule precisely. If the underlying data were available, displaying the county median distribution alongside the extrema would reveal whether each long range represents widespread variation or one exceptional county.

## 2. Story/Question 1

Does a narrowing female–male life expectancy gap necessarily accompany improving life expectancy? Sweden, Japan, Russia, and South Africa show how the same gap statistic can conceal very different male and female trajectories between 1990 and 2023.

## 3. First visualization for Story 1

Upload: [01_life_levels.png](figures/01_life_levels.png)

## 4. Rationale for the first visualization

Small multiples preserve absolute levels and annual trajectories without an eight-line tangle. All four panels share the same scales, so the lower life expectancy levels in South Africa and Russia remain visible rather than disappearing through panel-specific scaling. Consistent blue and orange lines identify sex, and the lightly filled distance between them makes the changing gap visible without substituting gap size for wellbeing. Endpoint gap labels support a quick comparison.

The contrasting cases are deliberate: Sweden narrows its gap through larger male gains; Japan’s endpoint gap is almost unchanged despite gains for both sexes; Russia’s similar endpoint gap hides substantial intermediate widening; South Africa’s early narrowing accompanies steep losses, especially among women. Annual lines prevent those endpoints from becoming the entire story. The caption identifies the selection as illustrative and avoids attributing these patterns to causes that the file does not measure.

## 5. Alternate visualization for Story 1

Upload: [02_life_changes.png](figures/02_life_changes.png)

## 6. Rationale for the alternate

Paired change dots turn “which sex changed more?” into a direct position comparison. Zero separates improvement from deterioration; the connector shows the difference between female and male changes. A blue dot farther right means the female advantage narrowed, whether both dots are positive or both negative. This makes the distinction between Sweden’s gains and South Africa’s losses particularly clear.

The two periods use a common 2005 checkpoint, chosen to separate the early decline and subsequent recovery visible in South Africa and Russia. Both panels retain identical horizontal scales and country order. Signed values help readers check close comparisons. These are endpoint changes over unequal-duration intervals, not annualized growth rates: the labels explicitly give the periods, and the intended comparison is between sexes within each period.

## 7. Comparison of Story 1 designs

The annual lines are better for understanding levels, reversals, and timing. They show why similar endpoint gaps can hide a dramatic history, but estimating which sex gained more requires comparing slopes and distances. The change dots answer that comparison immediately and clearly distinguish convergence through gains from convergence through losses. They sacrifice absolute lifespan and all within-period fluctuations, and their result depends on the chosen checkpoint. I would use the line version to introduce the story and the change version for a focused discussion of what “closing a gap” means.

## 8. Story/Question 2

When a county has more deaths than births, does net migration offset that natural loss, and how does the answer differ between metro and nonmetro counties in 2023? Among natural-loss counties, the offset share is 68% in metro counties and 49% in nonmetro counties.

## 9. First visualization for Story 2

Upload: [03_county_components.png](figures/03_county_components.png)

## 10. Rationale for the first visualization

The scatterplot separates two demographic components that an overall population change could conceal. Rates per 1,000 make counties of very different sizes comparable. The vertical zero line identifies natural loss, and the diagonal represents the migration rate needed to exactly offset it. Thus a county with negative natural change can sit above the diagonal and still have a nonnegative component sum.

Matched metro/nonmetro panels support comparison without asking readers to distinguish overlapping groups. Colors encode the outcome rather than county identity; gray de-emphasizes counties outside the central natural-loss question. The annotations give exact numerators and denominators, so dot density is not mistaken for a percentage. A stated viewing window keeps 39 extreme counties from compressing the main pattern; each panel reports its omitted count, and all counties remain in the statistics. The caption distinguishes the two-component sum from official total change, which can include a residual.

## 11. Alternate visualization for Story 2

Upload: [04_county_outcomes.png](figures/04_county_outcomes.png)

## 12. Rationale for the alternate

The 100% stacked bars ask how common each outcome is rather than how large its rates are. Keeping all nine RUCC categories reveals variation hidden by a binary metro/nonmetro split. The gray segment gives the share without natural loss; teal and red partition those with natural loss into offset and unoffset outcomes. Their combined share communicates the prevalence of natural loss. The right-hand column uses a different, explicitly labeled denominator: offset counties divided by all natural-loss counties.

A shared 0–100% baseline, county counts, and the separator after code 3 make comparison and coverage legible. I preserve the categorical code order instead of implying equal numerical steps in rurality. The irregular nonmetro pattern matters: offset shares are not a smooth decline from code 4 through code 9. Colors match the scatterplot, and the image includes its own definitions and exclusions.

## 13. Comparison of Story 2 designs

The scatterplot explains the demographic balance and preserves magnitude: two offset counties might have very different rates. It also exposes spread and unusual combinations, but overlap makes prevalence hard to judge, and its window excludes some extreme positions. The bars include every county and make outcome shares explicit, with more detailed geographic categories. They discard rate magnitudes, and middle segments lack a common starting position, so the conditional percentages are supplied in an aligned column. Both treat counties equally; neither estimates the fraction of residents living in each outcome category.

## 14. Story/Question 3

Across ten selected countries, did large life expectancy losses by 2021 necessarily leave larger deficits in 2023, and did male and female recovery agree? Mexico and India exceeded their 2019 baselines for both sexes, while Germany and the United States remained below theirs despite smaller 2021 losses.

## 15. Visualization for Story 3

Upload: [05_life_recovery.png](figures/05_life_recovery.png)

## 16. Rationale for Visualization 3

The heatmaps subtract each country’s sex-specific 2019 baseline, focusing attention on loss and recovery rather than the large underlying differences in absolute lifespan. Separate sex panels share the same row order and a symmetric, zero-centered color scale. This lets readers scan one year across countries or follow a row through time, then compare the corresponding row in the other panel. Signed cell values keep small deviations readable when their colors are almost neutral.

Ordering rows by the 2019–2021 loss in the supplied “Both” estimate makes the contrast with 2023 easy to see without sorting the sexes differently. The selection includes different timing patterns: Japan’s deficits appear later, while South Africa and Russia have opposite signs for male and female changes by 2023. I label this as a comparison of selected cases, not a global ranking, and do not interpret departures from 2019 as effects caused solely by the pandemic. The baseline answers whether the earlier level was regained; it cannot answer whether a country regained its pre-2020 trajectory.

## 17. Story/Question 4

Did metro and nonmetro counties converge in educational attainment from 2000 to 2019–23, or does the answer depend on the attainment threshold? The gap between median counties shrank for the share without a high school diploma but grew for the share with a bachelor’s degree or higher.

## 18. Visualization for Story 4

Upload: [06_education_thresholds.png](figures/06_education_thresholds.png)

## 19. Rationale for Visualization 4

Two attainment thresholds prevent “education improved” from becoming an overly simple account of geographic convergence. Aligned panels and identical percentage axes make the quantities comparable; the beneficial direction differs explicitly by panel, since less noncompletion and more degree attainment indicate improvement. Paired time colors keep the date comparison consistent in both groups.

Medians represent a typical county without allowing large counties to dominate. The interquartile segments show county variation and overlap, which a four-value summary would hide; they are distribution ranges, not uncertainty intervals. Labels and the caption quantify the different conclusions: the median difference shrinks from 3.6 to 1.9 percentage points without a diploma, but grows from 4.7 to 7.7 points for bachelor’s attainment. I use complete cases at both dates and hold 2023 metro classification fixed, reducing changes in composition across the comparison. This describes county distributions, not individual educational progress, national adult shares, or differences in the same individuals over time. The recent estimates cover five years rather than one Census year.

## 20. Tools, processing, and AI disclosure

This is an instructor-authorized example generated by OpenAI Codex. Codex read the local assignment and reference material, explored the data, selected the four questions and subsets, wrote and ran the plotting code, inspected the rendered images, adjusted their layouts, and drafted all written responses, including the critique. These substantive contributions are AI-generated; this document does not claim student authorship or independent human analysis.

The tools were Python 3.14 in the existing `p314` environment, pandas for reading and transforming data, NumPy for classification and arrays, and Matplotlib for six static PNGs. Shell commands managed the files, and the image viewer supported visual layout checks. No packages were installed, no external data were added, and no online pages were opened.

The World Bank file was pivoted into country/year rows with separate sex columns. Four complete country series were selected for Story 1; changes were calculated from 1990, 2005, and 2023 endpoints. Story 3 used ten countries and subtracted each sex’s own 2019 value from 2020–2023. Its rows were ordered using the supplied combined-sex 2021 change. No regional aggregate was treated as a country, no observations were imputed, and lines were not smoothed.

The county file is comma-separated in this local copy, despite its README’s tab-separated warning; it was read with CP1252 encoding and FIPS identifiers retained as strings and padded to five digits. Puerto Rico and 17 records without 2023 RUCC were excluded, leaving 3,106 county/county-equivalent records. Codes 1–3 define metro and 4–9 nonmetro. Natural loss was defined as a negative supplied natural-change rate; an offset was a nonnegative sum of supplied natural-change and net-migration rates, using their available precision. Both rates were complete for the eligible counties. Story 4 retained counties with both periods’ education percentages, leaving 3,089 records for each threshold, and computed unweighted medians and quartiles. The two plots use supplied rates and percentages, rather than averaging counts with different denominators.

All scripts and derived summaries remain in `work/`; `work/README.md` gives regeneration instructions. The six figures carry their own units, source notes, selection rules, and relevant limitations.
