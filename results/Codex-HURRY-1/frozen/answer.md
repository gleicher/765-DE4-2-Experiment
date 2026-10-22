# Design Exercise 4-2 — AI-assisted draft

These answers and figures were generated with Codex. Review the calculations, make the design judgments your own, and revise the critique to reflect your opinion before submitting, consistent with the saved course AI policy. The critique below assumes the non-CLO option; if you participated in CLO, replace question 1 with your actual reviewer’s name and assessment.

## 1. Critique

The paired endpoints make each state’s county-income range easy to see. Blue and orange distinguish the maximum and minimum, the connectors associate them, and the ratio annotations offer a second way to compare disparities. The ordering roughly progresses from smaller to larger ratios, helping the broad pattern emerge.

The title and caption overstate what is measured. A range of county median household incomes measures differences between county medians, not household income inequality within each state. A state can have similar county medians and still have considerable inequality among households. Extremes also depend on how many counties a state has, and the chart does not show the distribution between the two endpoints. The selected states exclude much of the country; “top 5, bottom 5, and 6 additional interested states” needs a clearer selection explanation, including whether “top” means ratio or income.

I would retitle it “County median household incomes vary within selected states,” identify the currency as U.S. dollars, replace “Measure Names” with a descriptive legend, and label the ratios explicitly as maximum divided by minimum. Horizontal rows sorted by ratio would make state labels easier to scan. Adding a distribution of county medians, or at least the number of counties behind each range, would give the endpoints context. I would retain the paired-dot encoding because its common position scale is effective.

## 2. Story/question 1

How has the female advantage in life expectancy changed in France, Japan, the United States, Sweden, Brazil, and South Africa? Their trajectories differ: four of these countries had smaller gaps in 2023 than in 1990, while Japan and Brazil had larger gaps.

## 3. Upload: first visualization for story 1

Upload **[01_life_gap_trajectories.png](figures/01_life_gap_trajectories.png)**.

## 4. Rationale: first visualization for story 1

Six small-multiple line charts show female minus male life expectancy for every available year from 1960 through 2023. Shared axes support comparisons of both the gap’s magnitude and its shape without the occlusion of six overlapping lines. The zero baseline gives the difference a clear interpretation, and country titles and endpoint labels avoid reliance on a detached legend. Markers identify 1990 and 2023, linking this view to the alternate design. The selected countries provide contrasting trajectories rather than a representative sample; the figure says so. Plotting the difference emphasizes the sex gap, while deliberately giving up information about absolute life expectancy.

## 5. Upload: alternate visualization for story 1

Upload **[02_life_gap_endpoints.png](figures/02_life_gap_endpoints.png)**.

## 6. Rationale: alternate visualization for story 1

A horizontal paired-dot chart compares 1990 with 2023 on one common position scale. Hollow gray dots identify 1990, filled teal dots identify 2023, and connecting segments emphasize the direction and size of change. Sorting by the 2023 gap makes the current ranking immediately visible. A signed change column supplies precise differences without requiring readers to subtract coordinates. The axis starts at zero, and the caption defines the direction of movement. The six countries and gap calculation are identical to the first design.

## 7. Compare the life expectancy designs

The line-chart small multiples reveal timing and reversals, especially South Africa’s sharp intermediate narrowing and subsequent widening. Their weakness is that endpoint ranking and precise changes require scanning several panels. The paired-dot view makes the 1990–2023 comparison compact and easy to rank, including the nearly unchanged Japanese gap. It hides all intervening years, so it could suggest a simple change where the actual trajectory is complex. The line view is better for understanding history; the paired-dot view is better for comparing two reference periods.

## 8. Story/question 2

How did county bachelor’s-degree attainment change from 1990 to 2019–23 across the nine 2023 rural–urban county types? The median rose in every type, with the largest gain in counties belonging to the largest metropolitan areas, while substantial variation remains within types.

## 9. Upload: first visualization for story 2

Upload **[03_education_medians.png](figures/03_education_medians.png)**.

## 10. Rationale: first visualization for story 2

The paired-dot chart emphasizes the change in median county attainment, using a common percentage axis and a signed percentage-point gain column. County types appear in their code order, keeping metro size and the adjacent/nonadjacent nonmetro pairs together. Long row labels explain the types without requiring outside documentation. The sample contains only counties with valid values for both periods, preventing changing coverage from creating an apparent difference. Each county receives equal weight, and the caption distinguishes the median of county percentages from a population-wide attainment rate. Both periods use the same 2023 classification; the figure identifies 2019–23 as a pooled estimate rather than a single-year measurement.

## 11. Upload: alternate visualization for story 2

Upload **[04_education_distributions.png](figures/04_education_distributions.png)**.

## 12. Rationale: alternate visualization for story 2

Paired box plots retain the same matched counties, periods, code order, and equal county weighting while exposing variation hidden by the median-only design. Teal consistently denotes the later period. Boxes show the middle 50%, median lines show the center, and whiskers show the 10th–90th percentiles. Omitting outer points visually avoids clutter; those counties remain in the calculations, and the caption states the convention explicitly. Sample sizes below the codes reveal unequal group sizes. A divider separates metro from nonmetro counties, and the caption decodes the nine categories so the image stands alone.

## 13. Compare the Census designs

The paired-dot design answers “how much did the median change?” directly and offers readable category descriptions and numerical gains. It hides the spread of counties in each group. The box-plot design shows that county types overlap, and that the upward shift is visible across the middle of the distributions rather than only at the median. Its codes and box conventions require more explanation, and exact differences are harder to read. Neither design shows individual counties’ paired changes: the periods use a matched sample, but connecting group medians does not establish that every county improved.

## 14. Story/question 3

How did female and male life expectancy in South Africa recover after their post-1990 lows? Both exceeded their 1990 levels by 2023, despite a large intervening decline and another visible dip near 2021.

## 15. Upload: visualization for story 3

Upload **[05_south_africa_recovery.png](figures/05_south_africa_recovery.png)**.

## 16. Rationale: visualization for story 3

Two directly labeled lines show absolute life expectancy, complementing the gap-only views in story 1. A common years axis allows readers to see the decline and recovery for both sexes. Annotated markers identify each sex’s own lowest year after 1990: 2005 for women (55.5 years) and 2004 for men (51.9). Endpoint labels give 2023 levels without a legend lookup. All annual estimates are shown without smoothing, preserving the later dip. The vertical axis begins at 40 years to make the changes legible; these are position-encoded lines, and the clearly labeled scale prevents an implied zero baseline. The caption avoids attributing the changes to causes that the supplied data cannot establish.

## 17. Story/question 4

Among counties with more deaths than births in 2023, how often was net migration sufficient to offset that natural decrease? It was sufficient in 1,152 of 2,150 counties (about 54%), although the balance varied widely.

## 18. Upload: visualization for story 4

Upload **[06_migration_balance.png](figures/06_migration_balance.png)**.

## 19. Rationale: visualization for story 4

The scatterplot places natural change and net migration on separate axes, both measured per 1,000 residents. Zero reference lines identify the signs of the components, while the diagonal marks where they sum to zero. A county left of the vertical line but above the diagonal has enough net migration to offset natural decrease. Small translucent points reduce overlap, and color supplies context about metro versus nonmetro classification. The main panel zooms in on the dense pattern; a full-range inset displays every valid observation and explicitly reports that 75 counties fall outside the main view. Counts use all 3,106 counties with valid rates, including those outside the zoom. The numerical callout makes the main answer accessible without counting dots. The caption distinguishes a component balance from official population change, which can include residual adjustments; it does not claim causal migration effects.

## 20. Tools, processing, and AI disclosure

OpenAI Codex assisted with selecting stories, analyzing the supplied data, writing Python plotting code, checking rendered figures, and drafting these answers and the critique. This is an AI-generated draft requiring my review and revision before submission; the design choices and critique should reflect my own judgments. No external web pages were opened and no external data were added.

The figures were produced with Python 3.14 in the existing `p314` conda environment, using pandas, NumPy, and Matplotlib. Pillow was used to assemble a contact sheet for visual inspection. Shell commands read the saved references and managed output files. No packages were installed and no toolchains were changed.

For life expectancy, the supplied World Bank CSV was pivoted by country, year, and sex. The female–male gap was calculated by subtraction, with no averaging across countries, interpolation, or smoothing. The endpoint chart compares 1990 with 2023. South Africa’s minima were found separately for each sex over 1990–2023.

The county CSV was read as comma-separated Windows-1252 text; this differs from the saved readme’s delimiter warning. FIPS identifiers were read as strings. Puerto Rico and any aggregate identifiers ending in `000` were excluded, and records were restricted to valid 2023 rural–urban codes 1–9. Education uses 3,087 counties with valid values in both 1990 and 2019–23. Medians and distribution summaries give every county equal weight. A median gain is the difference between the two period medians, not the median of individual county gains. Current county types were held fixed for both periods, so this is a comparison by 2023 classification, not a reconstruction of historical metro boundaries.

The migration figure uses 3,106 counties with valid supplied 2023 natural-change and net-migration rates. Natural decrease means a natural-change rate below zero; offset means the sum of the two rates is above zero. Rates were not recomputed from population counts. All plots are descriptive and make no causal claims.

The retained script, summary tables, plotting extract, and regeneration instructions are in `work/`. All six uploads are separate static PNG images with titles, labels, and source/method captions.
