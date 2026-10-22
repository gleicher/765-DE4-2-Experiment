## 1. Critique

The connected dots make the range of county median incomes easy to compare, and the blue/orange distinction is consistent. The ratio labels also help: California has a larger dollar range than Alabama, but Alabama has the larger ratio. That is a useful distinction that the line lengths alone would miss.

My main concern is the claim about “income inequality.” This shows variation between county medians, not inequality between households. A county could have substantial household inequality that its median completely hides. The title and caption should say “county median incomes” and qualify the conclusions as applying to the selected states. The selection of “additional interested states” is also vague, so I cannot tell why these cases were included or whether the extremes are national extremes.

I would use horizontal dumbbells with state names on the left, rename the legend to “Highest-income county” and “Lowest-income county,” and label the axis in dollars. Sorting explicitly by the maximum/minimum ratio would make the sequence easier to understand. A short caption could explain that these are unweighted county extremes and can depend heavily on how many counties a state has.

## 2. Story/Question 1

How did the female advantage in life expectancy change between 1990 and 2023 in eight selected countries? France and the United States narrowed their gaps, while India and China widened theirs.

## 3. First visualization for Story 1

Upload: `figures/01_life_gap_dumbbell.png`

## 4. Rationale

The dumbbells put the two years on a common horizontal scale, so the connection shows both the direction and size of the change. I sorted countries by change rather than alphabetically to group narrowing and widening gaps. Gray marks the earlier year and blue marks the later one; the change column gives the numerical difference without making viewers subtract endpoints. I kept the selection to eight contrasting cases so the labels stay readable and made clear that these are examples, not a representative country sample.

## 5. Alternate visualization for Story 1

Upload: `figures/02_life_gap_scatter.png`

## 6. Rationale

Here each country is positioned by its gap in 1990 and its gap in 2023. Equal axis scales make the diagonal a meaningful reference: below it means the gap narrowed, and above it means it widened. The shaded regions and direct labels make that comparison visible without consulting a legend. This design also shows that Russia's gap remains much larger than the others, while India's relatively small initial gap increased substantially. The points use unrounded values, which matters for countries close to the diagonal.

## 7. Comparison

The dumbbell is easier for looking up a country and estimating its change, especially with the numerical change column. It also makes the ordering of changes explicit. The scatterplot is better for seeing the overall relationship between starting and ending gaps, including which countries stayed near the no-change line. Its main weakness is that change must be judged relative to a diagonal, and nearby points need carefully placed labels. I would choose the dumbbell for a general audience and the scatterplot for comparing patterns across countries.

## 8. Story/Question 2

Among US counties with more deaths than births in 2023, how often was net migration enough to offset that natural decrease? Migration offset the loss in about 67% of metro counties and 49% of nonmetro counties.

## 9. First visualization for Story 2

Upload: `figures/03_migration_cumulative.png`

## 10. Rationale

I divided net migration by deaths minus births, so a value of one means migration exactly offsets natural decrease. The cumulative curves let viewers compare the full distributions rather than just the two headline percentages. The threshold line connects the distributions to the question: about 33% of metro counties and 51% of nonmetro counties fall below it. A symmetric logarithmic scale preserves negative migration values while keeping large ratios from compressing the useful part of the chart. The caption explains that scale and the county-based denominator.

## 11. Alternate visualization for Story 2

Upload: `figures/04_migration_stacked.png`

## 12. Rationale

The stacked bars turn the offset threshold into three understandable outcomes: no migration gain, a gain too small to offset natural decrease, and a gain large enough to offset it. Giving both bars the same total width supports comparison despite their different county counts. I put the successful-offset category at the right edge, where its boundary is easy to compare, and included counts as well as percentages. This avoids implying that the larger nonmetro group represents a larger share of the US population.

## 13. Comparison

The stacked bars communicate the main result faster and distinguish unsuccessful migration gains from actual migration losses. They hide how far counties are above or below the threshold. The cumulative plot keeps that information and shows how the two distributions differ, but the ratio and mixed linear/logarithmic scale take more explanation. I would use the stacked bars to introduce the finding and the cumulative plot when the audience wants to examine the distribution behind it.

## 14. Story/Question 3

Did China and India converge in life expectancy after 1980, and was the pattern similar for women and men? The gap narrowed for both, but China's advantage remained larger among women in 2023.

## 15. Visualization for Story 3

Upload: `figures/05_china_india_lines.png`

## 16. Rationale

Separate panels for women and men keep four trajectories from competing in one plot. Both panels share the same year range and vertical scale, so the differences between countries can be compared across sexes. Consistent country colors and direct endpoint values support quick identification. The annotations give the 1980 and 2023 country gaps, while the full trajectories show that convergence was not a smooth process. I retained the earlier years for context rather than starting the chart at the comparison baseline.

## 17. Story/Question 4

How did county distributions of bachelor's-degree attainment change from 2000 to 2019–23 in metro and nonmetro counties? Both moved upward, but the difference between their county medians increased from 4.7 to about 7.7 percentage points.

## 18. Visualization for Story 4

Upload: `figures/06_education_boxplots.png`

## 19. Rationale

Boxplots show the middle of each county distribution without reducing the comparison to a single average. The common percentage scale makes the upward shifts and the overlap between groups visible; median labels make the central comparison precise. I grouped the periods within each metro category and left extra space between categories. Only counties with education data in both periods are included, so changing coverage does not drive the comparison. Each county receives equal weight, which answers a question about places rather than the educational attainment of the average resident.

## 20. Tools and processing

These figures were made with Python in the existing `p314` environment, using pandas and NumPy for processing and Matplotlib for plotting. Pillow was used to assemble a preview sheet for checking the layouts. I used the supplied World Bank life expectancy file and county Census/USDA file; no outside data were added and no webpages were opened.

For the life expectancy figures, the sex rows were pivoted by country and year, and the female–male gaps were calculated by subtraction. The paired designs use eight explicitly selected countries and the same two years. The China/India figure uses the full annual female and male series.

For the county figures, Puerto Rico and records without a valid 2023 rural–urban continuum code were excluded. Codes 1–3 were grouped as metro and 4–9 as nonmetro. The migration figures retain counties with negative natural change and complete relevant fields; the ratio is net migration divided by the absolute natural decrease. The education figure retains counties with values in both periods and uses the supplied adult attainment percentages. All county summaries give each county equal weight. The Census file was read as comma-separated with CP1252 encoding despite the readme's tab-separated warning.

OpenAI Codex assisted with the story selection, data analysis, plotting code, visual checks, and drafting these responses. The figures and written rationales are AI-assisted drafts; I need to review the interpretations and wording before submitting them as my work. Scripts, intermediate tables, and regeneration instructions are retained in `work/`.
