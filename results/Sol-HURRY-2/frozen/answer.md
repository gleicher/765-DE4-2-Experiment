# Instructor example: Design Exercise 4-2

This is a complete AI-generated example for private instructional review of the past assignment, not a student submission. No CLO participation is assumed.

## 1. Critique

The supplied visualization makes within-state differences in county median household income easy to see. Its paired points and connecting segments use a common position scale, so readers can compare both endpoints and absolute ranges. The blue/orange distinction is redundant with vertical position, and the ratio annotations support comparisons that the dollar scale alone would not show. The caption explains the selection of states and identifies the county-level unit.

The principal weakness is the interpretation of “income inequality.” A range between county median household incomes measures geographic variation in medians; it does not measure the distribution of household incomes within a state. A state could have similar county medians yet substantial inequality among households. Likewise, more counties provide more opportunities for extreme medians, so these ranges are sensitive to county structure. “WY has the lowest” and “VA has the highest” need a clear statement that these rankings concern this particular county-median ratio, and the scope of states compared needs to be explicit. The selected states cannot establish a complete national pattern on their own.

The ratios appear to determine the order, but the order and its metric are not labeled. The title could say “County median household incomes vary more within some states.” I would use horizontal paired points with a clearly labeled ascending max/min-ratio order, replace “Measure Names” with “County median household income,” label the axis in dollars, and shorten the caption. If the goal is to describe the typical county distribution rather than extremes, I would add an interquartile range or show the full distribution. The zero baseline is defensible, but the large empty region below the minimum could be reduced for this point-and-range chart with explicit ticks. These changes would preserve its useful comparison while making the claim more precise.

## 2. Story/Question 1

How did the female–male life expectancy gap change from 1990 to 2023 in Chile, Japan, and the United States? It narrowed in Chile and the U.S., while Japan’s endpoint gap remained close to six years.

## 3. First visualization for Story 1

Upload: [01_life_gap_trends.png](figures/01_life_gap_trends.png)

## 4. Rationale

The line chart shows the derived female-minus-male gap on a shared year and years-of-life scale. This directly answers the question without requiring readers to subtract two sex-specific curves mentally. Three selected countries provide contrasting trajectories without creating a crowded global plot. Continuous lines show reversals and timing: the endpoints alone conceal intermediate widening, narrowing, and recent fluctuations. Direct endpoint labels identify countries without repeated trips to a legend. A zero baseline gives the magnitude of the advantage context; the same 0–8-year scale applies to all three countries. The title states the finding, and the caption identifies the source, selection, and descriptive scope. These are illustrative country comparisons, not evidence about how common each pattern is globally.

## 5. Alternate visualization for Story 1

Upload: [02_life_gap_endpoints.png](figures/02_life_gap_endpoints.png)

## 6. Rationale

The paired-point chart reduces the same story to its two endpoints. Each country has one row, both dates use the same horizontal scale, and gray connectors make the amount and direction of change visible. The date legend and numeric labels avoid ambiguity when Japan’s points nearly overlap. Signed change labels emphasize that Chile fell by 2.51 years, the U.S. by 1.70 years, and Japan increased by only 0.07 years. Display precision aids comparison without asserting that the estimates have no uncertainty. A zero-based axis and a caption saying that intervening years are omitted keep the simplified presentation interpretable.

## 7. Comparison for Story 1

The line chart is better for understanding the path: Japan’s gap widened and then narrowed, while the U.S. and Chile experienced recent reversals. Its costs are greater visual complexity and less convenient exact endpoint comparison. The paired-point chart is faster for comparing net changes and has clear numerical labels, but it can make nonmonotonic histories look like simple transitions. I would use the line chart for a discussion of change over time and the paired points for a concise endpoint summary.

## 8. Story/Question 2

Did county bachelor’s-or-higher attainment rise from 2000 to 2019–23, and how did its levels and within-county gains differ across 2023 rural–urban county groups? Typical shares rose in all three groups, with larger median gains in metro counties.

## 9. First visualization for Story 2

Upload: [03_education_levels.png](figures/03_education_levels.png)

## 10. Rationale

The paired-point chart compares the median county share in each period for three clearly named groups: metro codes 1–3 and two nonmetro code bands, 4–7 and 8–9. The nonmetro bands summarize the supplied classification rather than introducing outside geography. A common percent axis permits comparisons of both starting levels and later levels. The same counties contribute to both dates; county counts are labeled. Equal county weighting matches a question about the typical county, rather than the typical resident. The 2019–23 points retain their actual multiyear label instead of pretending to be measurements from one year. Holding 2023 classification fixed avoids changing group membership between dates, although it does not describe the counties’ historical classification. The caption states these choices. It is a descriptive comparison of reported estimates, with no claim of statistical significance.

## 11. Alternate visualization for Story 2

Upload: [04_education_change_distribution.png](figures/04_education_change_distribution.png)

## 12. Rationale

The boxplots use each county’s later share minus its 2000 share, in percentage points. This focuses on the change underlying the first chart and reveals variation that group medians hide. The common axis, zero reference, and median labels make group comparisons easy: median gains are 8.8 points for metro counties and about 6.3 and 6.2 for the two nonmetro bands. Boxes show the middle half of counties, while whiskers and remaining points preserve the tails instead of silently removing exceptional counties. County counts and a definition of the boxplot are embedded in the image. The group order and sample match the first visualization.

## 13. Comparison for Story 2

The paired-point chart gives the clearest overview of the rise in attainment and the persistent difference in typical levels across county types. It does not show whether all counties improved. The boxplots reveal overlap, negative changes, and the greater typical metro gain, but require more explanation and do not show baseline attainment. The median of within-county differences is not necessarily the difference between the two period medians; the charts deliberately answer those complementary aspects of the same question. Neither figure represents a population-weighted national attainment rate.

## 14. Story/Question 3

How did life expectancy in six selected countries depart from its own 2019 level during 2020–23? Mexico and South Africa had large deficits in 2021 but exceeded their 2019 values by 2023, while Japan and the U.S. remained slightly below theirs.

## 15. Visualization for Story 3

Upload: [05_life_recovery_heatmap.png](figures/05_life_recovery_heatmap.png)

## 16. Rationale

Subtracting each country’s 2019 value makes deviations comparable despite differing baseline lifespans. Rows identify selected countries and columns preserve chronological order. A diverging color scale centered at zero separates below-baseline estimates from above-baseline estimates; symmetric limits of ±5 years prevent unequal visual emphasis. Every cell also carries a signed numerical value, so color is not the only route to the data. This matrix makes the large 2021 deficits and subsequent recovery visible in one compact image. The country selection provides varied examples, not a representative sample. The caption makes that scope explicit and avoids attributing every change to the pandemic or any other cause. Recovery means returning to a fixed baseline, not catching up to an unobserved expected growth trend.

## 17. Story/Question 4

Among U.S. counties with more deaths than births in 2023, how often did net migration exceed that natural population loss? In this sample, 1,152 of 2,150 such counties—53.6%—had a positive sum of the natural-change and migration rates.

## 18. Visualization for Story 4

Upload: [06_migration_offset_scatter.png](figures/06_migration_offset_scatter.png)

## 19. Rationale

A scatterplot puts two demographic components on common per-1,000-resident units, avoiding raw-count comparisons between differently sized counties. The vertical zero line identifies natural-loss counties. The diagonal, migration = −natural change, provides the exact offset threshold: points to the left of zero and above the diagonal are highlighted in teal. Gray points preserve the rest of the sample for context. Small transparent markers reduce overplotting; the legend gives group counts and the subtitle states the main result. All valid observations remain visible, including extreme rates, although they compress the central cloud. The embedded caption distinguishes the sum of these two components from total population change, which may include residual adjustments. The result counts counties equally and does not mean that 53.6% of residents live in these counties.

## 20. Tools, processing, and AI disclosure

This instructor-requested example was produced by OpenAI Codex, an AI assistant. The AI read the supplied assignment, grading guidance, dataset documentation, and critique image; selected all four stories and country/group subsets; wrote the critique, rationales, comparisons, and disclosure; wrote and ran the processing and plotting code; and visually inspected a contact sheet of the figures. The AI contribution includes the substantive analysis and the complete written response, not just grammar editing or programming help. No student-authored design decisions or independent instructor verification are claimed.

Tools: the existing p314 Python interpreter (`/opt/anaconda3/envs/p314/bin/python`), pandas for CSV loading and transformations, NumPy for numerical operations, Matplotlib for six static PNG figures, and Pillow for a visual inspection contact sheet. Shell commands were used to read local files and run scripts. No packages were installed and no external data were added. No web pages were opened; `sources.txt` records this.

Processing: the supplied life expectancy file was pivoted by country, year, and sex. Female minus male expectancy was computed for Chile, Japan, and the U.S. for 1990–2023. Both-sex values for Japan, Sweden, the U.S., Chile, Mexico, and South Africa were compared with each country’s 2019 value. These explicit named-country subsets exclude regional aggregates.

The county file is actually comma-separated and needs CP1252 decoding, despite the supplied README describing tabs. FIPS strings were padded to five digits. Rows needed a valid 2023 rural–urban code from 1 to 9, and Puerto Rico was excluded. Numeric conversions use missing values for unparseable entries. Education analysis keeps only counties with both attainment shares (3,089 counties), holds 2023 groups fixed, calculates unweighted county medians, and computes each county’s percentage-point gain. Migration analysis keeps both 2023 rates (3,106 counties), uses negative natural change to identify loss, and uses a strictly positive component sum to identify offset. No imputation, causal modeling, outside joins, or uncertainty intervals were added. Rates and reported estimates are used as supplied.

The reproducible script, processed CSVs, numerical summary, and inspection contact sheet are in `work/`. `work/README.md` explains regeneration. Each image includes its own title, labels, source, and relevant limitations.
