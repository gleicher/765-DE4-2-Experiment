# Instructor-requested example: Design Exercise 4-2

This is an AI-created example for private instructional review, not a student submission. The six figures use a restrained worksheet appearance and operations that are plausible in Tableau; the actual rendering tool was Python/Matplotlib.

## 1. Critique

I use the supplied critique image rather than claiming participation in the CLO. The linked dots effectively show the range of county median household incomes within each selected state: a common dollar axis makes the endpoints comparable, and the gray connector makes the distance easy to follow. The consistent blue maximum/orange minimum encoding works well. Sorting by the displayed maximum/minimum ratio helps reveal the range of relative disparities, while the endpoint positions retain information about absolute income levels. Direct ratio labels and the explanation below the chart make it usable without interaction.

The main issue is the claim about “income inequality.” A maximum/minimum ratio of county medians measures geographic variation in typical household income, not the distribution of incomes among individual households. The title and caption should call it disparity among county median incomes. The maximum and minimum also depend on how many counties a state has and are sensitive to unusual counties. They cannot establish that Wyoming has the least household income inequality or Virginia the most. The caption describes selected states, but “highest” and “lowest” need an explicit comparison universe and a reproducible selection rule for the six extra states.

I would rename the legend “County median household income” and label the colors “Highest county median” and “Lowest county median,” add a dollar sign to the axis, and explain exactly how the states were selected. The state labels need appear only once; placing them at both the bottom axis and the orange dots is redundant. A horizontal layout would give the state names a stable location and leave room to name the endpoint counties. I would retain the range marks and ratio labels, but revise the title to “County median household income disparities in selected states, 2021,” provide the data source, and state that this is not a household-level inequality measure.

## 2. Story/Question 1

How did life expectancy change from 2019 through 2023 in Mexico, Argentina, Brazil, the United States, Chile, and Canada, and which had returned to or exceeded their own 2019 level by 2023?

## 3. First visualization for Story 1

Upload [q1_primary.png](figures/q1_primary.png).

## 4. Rationale for first visualization

Each country occupies its own pane, with year on the horizontal axis and both-sex life expectancy on a shared vertical scale. This separates six trajectories that would otherwise overlap, while preserving comparisons of their absolute levels. Lines show the sequence of annual estimates; small dots identify the observations. The common scale begins at 68 years because these are positions and changes rather than bars encoding magnitude from zero. The axis makes that scale explicit.

A dashed reference line shows each country's 2019 level, turning “recovery” into a specific comparison. Endpoint labels make the last observation readable. Countries are ordered by their greatest shortfall from 2019 within 2020–2023, deepest first; the heatmap uses the same order. Mexico falls about 4.78 years below its baseline in 2021, then exceeds it in 2023. Canada and the United States remain below their baselines. The selection is deliberate and manageable rather than representative of all American countries; the caption states that limit. These annual observations describe changes without attributing their causes.

## 5. Second visualization for Story 1

Upload [q1_alternate.png](figures/q1_alternate.png).

## 6. Rationale for alternate visualization

Country is on rows and 2020–2023 on columns. Each cell contains life expectancy minus that country's 2019 value. A red–blue diverging palette has a meaningful center at zero and symmetric limits of −5 and +5 years; red means below baseline and blue means above. Direct signed labels give exact changes to two decimal places, so interpretation does not depend on color precision. Those decimals reflect the supplied estimates, not an assertion of measurement certainty.

Subtracting each baseline removes differences in starting level and makes relative shortfalls the focus. Mexico's 2021 loss is the most conspicuous cell; the final column shows the four positive changes and the two remaining shortfalls together. Omitting the identically zero 2019 column saves space, while the title and legend explain the baseline. This is a simple calculated field and a highlight-table design rather than a complex spatial construction.

## 7. Comparison of Story 1 visualizations

The line panes better communicate trajectories, absolute longevity levels, and the different timings of the lowest observations. They require the viewer to compare a point with a country-specific reference line to assess recovery. The heatmap makes cross-country shortfalls and final recovery status faster to scan, and its labels make exact baseline-relative comparisons easy. It hides absolute levels and emphasizes discrete cells over the continuity of time. I prefer the line panes for a first introduction to these countries and the heatmap for a reader primarily comparing the severity and persistence of their declines. Both show the same countries, years, sex aggregation, and estimates.

## 8. Story/Question 2

How did the mean county share of adults with a bachelor's degree or higher change from 2000 to 2019–2023 across the nine 2023 rural–urban continuum codes? Every code rises, but the highest county-average attainment remains in code 1.

## 9. First visualization for Story 2

Upload [q2_primary.png](figures/q2_primary.png).

## 10. Rationale for first visualization

A row for each rural–urban code contains gray and blue dots for the two periods, connected with a neutral line. Position on the same percentage axis communicates attainment, while the connecting distance communicates change. Percentage-point gain labels answer the change question directly, without confusing percentage-point increases with percentage increases. Code order follows the supplied classification, rather than sorting away the metro/nonmetro grouping.

The measure is the arithmetic mean of county percentages, with each county equally weighted; it describes county averages, not the percentage of all adults in a group. I retain the same 3,089 counties/county-equivalents with both education measures and a valid code, excluding Puerto Rico and state-level rows. Group sample sizes appear beside the labels. The caption specifies that codes 1–3 are metro and 4–9 nonmetro, and that 2023 classifications are held fixed when grouping the older observations. It also distinguishes a pooled 2019–2023 estimate from a single-year measure. Code 1 gains about 10.7 points, compared with roughly 6.2–7.1 points across codes 4–9.

## 11. Second visualization for Story 2

Upload [q2_alternate.png](figures/q2_alternate.png).

## 12. Rationale for alternate visualization

Grouped bars use the same complete county set and equal-county means as the paired-dot chart. The two bars for each code make the old and new attainment levels familiar to read. A zero baseline preserves the meaning of bar lengths. The code order, gray/blue period colors, and directly printed percentages are consistent with the companion chart.

The common vertical axis makes the higher code-1 level and the increases in all groups visible. Grouped bars could be built with code on columns, the two period measures side by side, and period on color. I avoid stacking the two periods because they are separate estimates rather than parts of a total. The caption identifies aggregation, geography, the fixed classification, and the pooled later period so that a reader does not mistake the chart for population-weighted educational attainment or a rural-to-urban transition analysis.

## 13. Comparison of Story 2 visualizations

The paired dots make the gain the main feature: the connecting distance and printed percentage-point change are immediately visible. They also accommodate county counts beside the row labels. The grouped bars emphasize the absolute attainment levels and offer a familiar zero-based encoding, with values printed on each bar. However, bar height differences require mental subtraction to compare gains, and eighteen bars use more visual space than eighteen dots. I prefer paired dots for this change question and grouped bars for readers asking about levels in each period. Neither chart reveals within-code distributions or weights counties by their adult populations.

## 14. Story/Question 3

Between 2000 and 2023, were life expectancy gains larger for females or males in twelve selected countries, and how large were those gains? The direction differs across countries: five have larger female gains and seven larger male gains.

## 15. Visualization for Story 3

Upload [q3.png](figures/q3.png).

## 16. Rationale for Story 3

Each country is one labeled point, positioned by its male gain horizontally and female gain vertically. Both axes use the same units and limits with equal aspect ratio, so the dashed equality line supports an honest comparison. Orange points above the line have larger female gains; blue points below it have larger male gains. Position communicates the magnitudes, and color reinforces which gain is larger. The measure is a simple endpoint difference, 2023 minus 2000, separately for each sex.

India has large gains for both sexes, with a greater female gain; France has a greater male gain. Distance from the equality line indicates the change in the female-minus-male life expectancy gap. This is not a comparison of absolute longevity and does not imply males live longer in blue countries. Twelve countries spanning several world regions keep the labels readable and include different magnitudes and directions. The caption states that this is a purposive selection with no claim of global representativeness. Only endpoint gains are shown, so the chart does not claim steady improvement between them.

## 17. Story/Question 4

Among counties with more deaths than births in 2023, how often was net migration sufficient to offset that natural population loss, and did this differ between metro and nonmetro counties?

## 18. Visualization for Story 4

Upload [q4.png](figures/q4.png).

## 19. Rationale for Story 4

Two 100% stacked horizontal bars compare metro and nonmetro counties with negative natural change. Net migration is classified as sufficient if it is at least the absolute size of that natural loss; otherwise it is either positive but insufficient or zero/negative. These mutually exclusive categories partition each group's counties. The blue category starts at the same zero baseline in both bars, making the main comparison direct: 67.4% of metro versus 48.8% of nonmetro counties have migration sufficient to offset the loss. The gray category is aligned with the right edge, making its comparison easy as well; the middle category needs its printed percentage because it lacks a common starting position.

Labels give percentages and group denominators: 592 metro and 1,563 nonmetro counties, totaling 2,155 complete records. Equal county weighting answers “how often among counties,” rather than measuring the number of people affected. Restricting the denominator to counties with natural loss keeps the comparison focused. I use the supplied counts rather than rounded rates to classify the offset, combine domestic and international net migration through the supplied net-migration field, and use 2023 rural–urban codes. The caption specifies that residual population adjustments are excluded, so offsetting natural loss is not presented as a definitive classification of observed total population growth.

## 20. Tools, processing, and AI disclosure

This example was created by OpenAI Codex, an AI coding assistant, at the instructor's request for private instructional review. The AI selected the questions, explored and calculated the data summaries, wrote the plotting code, produced and inspected the figures, wrote the critique and rationales, and prepared this answer. No student-authored analysis or Tableau authorship is claimed.

Actual tools used were the shell, Python 3.14 in `/opt/anaconda3/envs/p314/bin/python`, pandas, NumPy, Matplotlib, Pillow (for an inspection montage), and the assistant's local image-viewing tool. Tableau was not used. The designs were chosen to resemble conventional Tableau worksheets through panes, fields on axes, filtering, arithmetic means, endpoint differences, reference comparisons, mark labels, color, and percent-of-total bars. No packages were installed or toolchains changed. No outside data or online pages were used; the assignment, rubric, critique image, and documentation were read from the supplied local reference files.

The World Bank CSV was filtered to explicitly named countries, relevant years, and sex categories; aggregate regions were not included. Both-sex estimates were taken directly from the supplied “Both” rows, not reconstructed by averaging male and female values. Life expectancy calculations subtract the 2019 baseline or the 2000 endpoint. The census CSV required CP1252 decoding; FIPS identifiers were retained as zero-padded strings. State-level rows with FIPS ending in `000` and Puerto Rico were excluded, while county-equivalents in the 50 states and DC were retained. The education comparison uses pairwise-complete records and equal-county means for each valid 2023 code. The migration comparison uses complete natural-change/net-migration counts and codes, filters natural change below zero, classifies offset status, and divides category counts by the metro/nonmetro group totals. No missing values were imputed, and no population weighting or external joins were performed.

The reproducible script and analysis CSVs are preserved in `work/`. `work/README.md` gives the regeneration command and maps the chart operations to a possible Tableau workflow. The six independent PNGs include titles, units, interpretation, limitations, and source captions; none relies on tooltips.
