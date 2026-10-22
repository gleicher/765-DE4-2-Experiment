# Design Exercise 4–2 — Canvas responses

**Review note:** This is an AI-produced submission draft, with the contribution disclosed in answer 20. The supplied course policy requires the student’s own decisions and opinions; review the designs and rewrite the critique and rationales to reflect your understanding before submitting. Question 1 uses the non-CLO option because no CLO participation details were provided. PNGs below are the upload files; matching SVGs are available for sharper scaling.

## 1. Critique of the supplied visualization

The dumbbell design makes the county-income range within each displayed state easy to see: two points on one dollar scale, joined by a quiet connector. The blue/orange distinction is readable, and the ratio labels allow proportional comparison alongside the absolute dollar difference. The caption usefully identifies the endpoints as the maximum and minimum **county median household incomes**, rather than individual households’ incomes.

The central problem is the headline’s claim about “income inequality.” A range of county medians measures differences between counties; it cannot describe the distribution of household incomes within a state. Counties also differ in population, and a single extreme county determines either endpoint. The number of counties is absent, so readers cannot assess that sensitivity. The caption’s “highest” and “lowest” language should clarify whether it refers to all states or the selected subset. Including six “interested states” alongside the extremes without explaining their selection makes the scope ambiguous.

I would retitle it **“County median incomes span different ranges across selected states.”** I would specify dollars and year in the axis, replace “Measure Names / Max. / Min.” with “Highest / lowest county median,” and show county counts. Keeping the ordered dumbbells is reasonable if range is the intended question. If the intended question is the typical spread between counties, I would add an interquartile interval and median for each state, retaining faint endpoint dots. This would reveal whether the long connector represents a broad distribution or a single unusual county, without claiming to measure household inequality. The critique identifies a mismatch between the statistic and the claim, rather than rejecting a useful encoding.

## 2. Story / Question 1 — Life expectancy

Between 1990 and 2023, did longer total life expectancy coincide with a smaller female–male gap in India, China, Japan, the United States, South Africa, and Russia? All six improved in total life expectancy, but the gap widened substantially in India and China, narrowed in the United States and South Africa, and changed little in Japan and Russia.

## 3. Upload: first visualization for Story 1

[01a_life_trajectories.png](figures/01a_life_trajectories.png)

## 4. Rationale: Story 1, first visualization

The small multiples show the full annual male and female trajectories, so “improvement” is not reduced to a straight line between two endpoints. The panels share identical year and life-expectancy scales. This permits comparisons of both absolute levels and the distance between the two sex-specific curves. Teal and orange retain the same meaning in every panel; the pale ribbon makes the gap visible without replacing the two actual series.

Endpoint labels report 2023 levels, while the short 1990 → 2023 gap annotation answers the comparison directly. The common vertical range includes South Africa’s intervening trough, avoiding a misleading impression of uninterrupted improvement. Countries were deliberately selected as contrasting cases, not a random or globally representative sample. The caption makes that limit explicit. The figure supports a nuanced conclusion: longer lives and convergence between sexes are separate outcomes.

## 5. Upload: alternate visualization for Story 1

[01b_life_endpoints.png](figures/01b_life_endpoints.png)

## 6. Rationale: Story 1, alternate

The alternate directly juxtaposes the two outcomes in aligned rows. The left panel measures the female–male gap in years, with hollow 1990 and filled 2023 points. The connector’s direction and signed change label reveal widening versus narrowing. Rows are ordered by the original gap, so their order is meaningful rather than alphabetical. The right panel uses zero-based bars to show the gain in **both-sex** life expectancy for exactly the same countries.

Separate labeled axes keep a gap and a total gain from being conflated, despite both being measured in years. This design makes the main counterexample immediate: India and China have the largest total gains in the selection, yet their sex gaps widen. The bars use the dataset’s reported “Both” series, not an unweighted average of male and female estimates. The footer states the tradeoff: endpoint comparison suppresses intervening reversals.

## 7. Comparison of the Story 1 designs

The small multiples are stronger for understanding **how** the trajectories unfolded. They expose South Africa’s long decline and recovery, Russia’s fluctuations, and recent dips. Their weakness is that comparing gap changes across panels requires some visual subtraction, partly helped by the annotations.

The aligned endpoint design is stronger for the specific comparison between overall gains and convergence. It makes the widening in India and China and narrowing in the United States immediately readable, with less visual effort. It sacrifices the timing and shape of change: an endpoint gain can conceal a serious intervening decline. I would choose the alternate for a concise comparative argument and the first figure for an audience that needs the historical context.

## 8. Story / Question 2 — Census

How do natural change, domestic migration, and international migration combine across the nine 2023 rural–urban county classes? In the largest metro class, international inflow more than offsets domestic outflow; several nonmetro classes gain domestically despite natural population loss, but the component balance remains negative for codes 7 and 9.

## 9. Upload: first visualization for Story 2

[02a_growth_components.png](figures/02a_growth_components.png)

## 10. Rationale: Story 2, first visualization

A shared horizontal zero line distinguishes positive inflows from losses without requiring viewers to decipher a mixed-sign stacked bar. Each class receives three slightly separated dot-and-stem marks, with consistent colors for natural change, domestic migration, and international migration. The outlined diamond reports their sum. Class order preserves the continuum’s structure, with a divider between metro codes 1–3 and nonmetro codes 4–9; county counts make the aggregation scope visible.

Rates are computed from **summed component counts divided by the group’s mean 2022–2023 population**, multiplied by 1,000. This compares demographic intensity rather than rewarding classes simply for having more people. It also avoids giving a small county the same weight as a large one. A complete-case panel of 3,106 county records is used for every component. The diamond is explicitly a three-component sum, excluding the dataset’s estimation residual; it is not labeled as exact reported population growth.

## 11. Upload: alternate visualization for Story 2

[02b_growth_balance.png](figures/02b_growth_balance.png)

## 12. Rationale: Story 2, alternate

The alternate transforms the accounting relationship into a plane: natural change is horizontal and net migration is vertical. A hollow point starts at domestic migration; a vertical arrow adds international migration, ending at combined migration. Arrow length therefore represents the international contribution. Number labels identify all nine classes, while color separates metro from nonmetro.

The dashed diagonal is the exact threshold where natural change plus migration equals zero. Endpoints above it have a positive component sum, so the viewer can see whether migration offsets natural loss without adding three numbers mentally. The light background reinforces this region. The sidebar works through codes 1 and 9 using the same rounded rates shown by the marks: code 1 reverses its migration sign; code 9’s inflow does not cover its natural decline. The caption defines the marks, denominator, county coverage, and exclusion of the residual, so the alternate stands alone.

## 13. Comparison of the Story 2 designs

The component plot is easier for reading each contribution independently and comparing the size of international inflow across classes. Its zero baseline makes signed values unambiguous. However, the viewer must combine components to understand the balance; the diamond helps but is a fourth mark per row.

The balance-plane design is more effective for the question **“Does inflow cover natural loss?”** Its diagonal turns that calculation into a spatial test, and its arrows reveal how international migration changes the result. It requires more explanation, uses numeric class labels rather than full row labels, and is less convenient for exact component comparisons. The first design is the better reference chart; the alternate better communicates the accounting mechanism.

## 14. Story / Question 3

How did the composition of adult educational attainment change from 1990 to 2019–23 in metro counties and two nonmetro code groups? Bachelor’s-or-higher attainment rose in all three groups, while the metro advantage over codes 8–9 widened from 11.9 to 18.0 percentage points.

## 15. Upload: visualization for Story 3

[03_education_composition.png](figures/03_education_composition.png)

## 16. Rationale: Story 3

Paired 100% stacked bars show a complete educational composition rather than isolating college attainment. Four mutually exclusive categories sum to 100%, making this a valid part-to-whole encoding. The bachelor’s-or-higher category sits at the right edge of every bar; its lengths can be compared from a shared boundary. Neutral shades keep the earlier categories visible, while the strongest teal emphasizes the story’s focal category. Interior percentage labels support exact comparisons without making viewers chase a legend for values.

Shares are calculated from the four summed attainment counts, so they describe adults represented in the data, not an average county. The same 3,087 complete counties appear in both periods. Holding their 2023 classifications fixed prevents a classification change from silently moving a county between groups, but does not imply that a county was metro in 1990. The footer states this convention and identifies 2019–23 as a five-year estimate. The annotation makes the widening bachelor’s-share gap explicit; the bars also show the large decline in the below-high-school share. The design describes changing composition, not people’s individual educational transitions.

## 17. Story / Question 4

Among five selected countries with life-expectancy declines after 1990, does a deeper trough imply a longer wait to regain the 1990 level? Rwanda’s 35.6-year deficit was followed by a six-year threshold recovery, while Russia’s much smaller 4.4-year deficit took 17 years; depth and waiting time do not align consistently in these cases.

## 18. Upload: visualization for Story 4

[04_recovery_calendar.png](figures/04_recovery_calendar.png)

## 19. Rationale: Story 4

A calendar heatmap aligns all five countries on the same annual timeline and subtracts each country’s own 1990 baseline. This focuses attention on relative decline and recovery instead of confusing recovery with differences in starting life expectancy. A symmetric diverging scale places zero at its neutral center, uses red for deficits and blue for improvements, and assigns the same color to the same difference everywhere. The fixed scale preserves the exceptional magnitude of Rwanda’s trough instead of normalizing it away.

A ring marks each country’s minimum during 1990–2023; a square marks the first subsequent year at or above its 1990 baseline. The adjacent text states both the deficit and the elapsed time from trough to threshold crossing. This connects magnitude, timing, and duration in one reading path. The heatmap also retains later setbacks, so “recovered” does not imply permanently recovered. Recovery is deliberately defined as regaining a fixed historical level, not regaining a counterfactual trend. The selected cases support a descriptive comparison; they do not establish a general statistical relationship or identify causes of the declines.

## 20. Tools, processing, and AI disclosure

**Tools:** OpenAI Codex was used to read the supplied materials, explore the data, propose the stories, write the analysis and plotting code, generate and inspect the figures, and draft these answers, including the proposed critique. Python 3.14 in the existing `p314` environment, pandas, NumPy, Matplotlib, and Pillow were used. No packages were installed and no toolchains changed. No outside datasets were added. All references were supplied local files; no web pages were opened.

**Processing:** The World Bank CSV was read as UTF-8 and its redundant index column removed. Country codes identified actual selected country records, excluding regional aggregates. Male/female trajectories used annual 1990–2023 estimates. Endpoint gaps were female minus male; total gains used the reported both-sex series. Recovery used both-sex estimates, subtracting 1990 levels, finding each 1990–2023 minimum, and then locating the first subsequent year at or above the baseline. Missing values were not interpolated.

The county CSV required CP1252 decoding. State/national summary rows were excluded by FIPS, Puerto Rico was excluded, and U.S. states plus DC were retained. The demographic analysis used complete records for all three components, both population estimates, and the 2023 classification. Component rates were recomputed from summed counts and the mean 2022–2023 population. Natural change and migration were signed; the component total excluded the separate residual. Education used a balanced panel with all four attainment counts in both periods, grouped by fixed 2023 codes (1–3, 4–7, 8–9). Category counts were summed before percentages were calculated. No county medians or percentages were summed or treated as population totals.

**Production and checks:** All six pages were drawn with Matplotlib and exported as PNG and SVG. Image previews were inspected with Pillow and the image viewer. Computed tables are preserved as CSVs, with checks for row counts, unique identifiers, category sums, complete annual series, and independently recomputed recovery metrics. The plotting script checks text bounds to catch off-page labels. All scripts, derived data, the preview sheet, and regeneration instructions are in `work/`. There were no manual edits to the exported figures.

**Authorship:** This draft contains substantial AI-generated intellectual and written content. It should not be submitted unchanged as independently authored student work under the supplied course policy. The student should make and understand the final design decisions, provide their own critique, and retain accurate disclosure of the AI contribution.
