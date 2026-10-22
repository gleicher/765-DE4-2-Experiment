# Design Exercise 4-2 — instructor-requested example

## 1. Critique

The chart’s connected maximum and minimum dots make the range of county median household incomes easy to compare, and the ratio labels help explain the size of each range. The title overstates the measure: the maximum-to-minimum ratio of county medians is a range across counties, not a general measure of household income inequality. Only 16 states are shown, including six described as “interested,” so the chart does not support conclusions about all states; the state order also does not reveal a clear comparison rule. I would rename it to describe the county-median range and either show all states sorted by the ratio or state a reproducible selection rule. The zero-based income axis also compresses the differences, though the ratio labels partly address that.

## 2. Story/Question 1

How has the female life-expectancy advantage changed since 1960 across the World Bank’s geographic aggregates, and where does the gap remain largest? The worldwide gap grew modestly, while the size and direction of change varied by region.

## 3. First visualization for Question 1

Image file: `answers/figures/q1_life_expectancy_region_trend.png`

## 4. Rationale for the first visualization

I calculated female minus male life expectancy so the gap is a single measure with a meaningful zero: positive values favor women. Putting year on the horizontal axis makes long-term change easy to follow, while color separates the World estimate from seven geographic aggregates. I made the World line heavier and darker to keep the worldwide comparison prominent. The full line chart also shows when regional changes occurred, which is useful context that a two-date comparison would lose.

## 5. Second visualization for Question 1

Image file: `answers/figures/q1_life_expectancy_region_endpoints.png`

## 6. Rationale for the alternate visualization

This dot-range view keeps the same female-minus-male measure but puts regions into rows and uses endpoint markers for 1960 and 2023. Connecting each pair makes both the direction and size of change visible; sorting by the 2023 value makes the current regional gaps easier to compare. The negative South Asia estimate in 1960 remains visible, rather than forcing all values above zero.

## 7. Compare the two visualizations for Question 1

The line chart is stronger for following the timing of change and seeing that the worldwide gap was fairly steady after its earlier rise. Its eight series take more effort to compare precisely. The endpoint view makes the 1960-to-2023 changes and current regional ordering easier to compare, but hides the paths between those years. Both show the World estimate increasing from about 4.0 to 4.9 years; North America is an exception among the regional aggregates, narrowing from about 6.4 to 5.2 years.

## 8. Story/Question 2

Across U.S. counties, how does bachelor’s-degree attainment relate to unemployment, and is that pattern different between metro and nonmetro counties? The county-level association is negative in both groups, but the distributions overlap substantially.

## 9. First visualization for Question 2

Image file: `answers/figures/q2_census_education_unemployment_scatter.png`

## 10. Rationale for the first visualization

Each county is one mark, with bachelor’s attainment on the horizontal axis and the 2023 unemployment rate on the vertical axis. Color separates metro counties (2023 continuum codes 1–3) from nonmetro counties (codes 4–9). The fitted lines summarize the direction of the association within each group; their similar slopes and the overlapping point clouds show that settlement type does not neatly separate counties. I use an equal-weight county view and describe the relationship as an association, not a causal effect.

## 11. Second visualization for Question 2

Image file: `answers/figures/q2_census_education_unemployment_boxplots.png`

## 12. Rationale for the alternate visualization

This view groups counties into four attainment quartiles, then compares the unemployment distributions in separate metro and nonmetro panes. Median lines and interquartile boxes make the broad pattern visible without requiring a viewer to trace thousands of points. Outlier marks are omitted to keep the central distributions legible; the caption defines the whiskers. The shared vertical scale supports direct comparison between the two panes.

## 13. Compare the two visualizations for Question 2

The scatterplot retains each county and makes the broad negative association, overlap, and unusual cases visible. Its dense cloud makes individual values hard to read. The boxplots reduce the data to distributions, making the general decline in unemployment medians across attainment bands easier to compare between metro and nonmetro counties. They hide county-level relationships and outliers, so they are less useful for seeing the spread of individual observations. Together they show a modest county-level pattern rather than a sharp dividing line.

## 14. Story/Question for Visualization 3

In 2023, how often did positive net migration accompany negative natural population change across counties? About half of the counties with both measures reported had positive net migration and negative natural change, showing how migration can coincide with natural decrease.

## 15. Visualization 3

Image file: `answers/figures/q3_census_population_change_components.png`

## 16. Rationale for Visualization 3

I put net migration rate on the horizontal axis and natural change rate on the vertical axis, with zero reference lines to separate gains from losses in each component. The lower-right quadrant directly identifies counties where positive migration accompanies negative natural change. Color shows metro status, while equal-sized marks keep county counts visible instead of letting population size dominate the view. The axes focus on the central range and the caption reports the number of counties outside it.

## 17. Story/Question for Visualization 4

Among the entities with the largest declines in life expectancy from 2019 to 2021, how much had recovered by 2023? The rebound was substantial in most of this selected group, but not uniform.

## 18. Visualization 4

Image file: `answers/figures/q4_life_expectancy_pandemic_dips.png`

## 19. Rationale for Visualization 4

I selected the twelve entities with the largest 2019–2021 declines among those with values in all three years, then plotted their 2019, 2021, and 2023 estimates on a common life-expectancy scale. Rows keep entity names readable; colored points distinguish the three years, and connectors reveal the dip and rebound. The World estimate is included in the subtitle as context. Selecting the largest declines focuses the chart, so this view does not represent all countries or prove that the pandemic caused the changes.

## 20. How I made the visualizations

I used OpenAI ChatGPT for question selection, data exploration, Python code, design decisions, and drafting the rationales and critique. I used Python 3.14 from the `p314` environment, with pandas for data processing and Matplotlib for the six static PNG figures. Inputs were the local course-provided Census and World Bank lifespan CSV files. I did not use Tableau or open any outside webpages.

For Question 1, I filtered to the World and seven World Bank geographic aggregates, paired female and male records by year, and calculated female minus male life expectancy. For Question 2, I used records with both bachelor’s attainment (2019–23) and unemployment (2023); I classified continuum codes 1–3 as metro and 4–9 as nonmetro. The alternate view groups attainment into four sample quartiles. For Question 3, I used records with both 2023 population-change rates and displayed the central range noted in the figure caption. For Question 4, I selected the twelve largest 2019–2021 declines among records with values in 2019, 2021, and 2023.

The script is `work/make_figures.py`. From this run folder, regenerate all figures with:

```sh
MPLCONFIGDIR=work/.mpl-cache /opt/anaconda3/envs/p314/bin/python work/make_figures.py
```

No manual edits or additional processing steps are needed after running the script.
