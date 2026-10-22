# Design Exercise 4-2 — example responses

## 1. Critique of the supplied example

The chart makes the county-income spread within each selected state easy to see: the paired endpoint dots and connecting line separate each state’s minimum and maximum county median income, and the ratio labels give a quick sense of the span. The title, axis, legend, and caption make the marks understandable without interaction.

The main limitation is the selection. The caption says the chart includes the five highest, five lowest, and six “interested” states, so the display mixes an extreme-based sample with an unexplained discretionary sample. It cannot support a broad comparison of state income patterns. The min–max range is also sensitive to one unusual county and hides the distribution of all counties in between; it is a measure of county median-income spread, not a complete measure of household income inequality. The arbitrary state order makes comparisons harder, and the ratio labels are easier to interpret if their numerator and denominator are stated directly.

I would include all states, sort them by median county income or by max-to-min ratio, and use a box plot or a compact distribution plot so the viewer can see the middle counties as well as the extremes. I would describe the result as “spread in county median household income” and state whether counties are weighted equally.

## 2. Story/Question 1

Across six countries with contrasting trajectories, how large is the female-minus-male life-expectancy gap, and how has it changed since 1960?

## 3. Visualization 1

[01_life_expectancy_gap_over_time.png](figures/01_life_expectancy_gap_over_time.png)

## 4. Rationale for Visualization 1

I calculated female life expectancy minus male life expectancy for each country-year and used a line chart so the direction and timing of change are visible. The zero reference line distinguishes years when the male estimate is higher from years when the female estimate is higher. Six countries make the paths readable while giving contrasting histories: India starts below zero, while the Russian Federation has a much wider gap than the other selected countries. The caption says that the selection is not representative of the world, so the chart does not imply a global average.

## 5. Visualization 2

[02_life_expectancy_gap_2023.png](figures/02_life_expectancy_gap_2023.png)

## 6. Rationale for Visualization 2

This sorted horizontal bar chart uses the same female-minus-male calculation, but focuses on the latest common year, 2023. Starting the bars at zero makes the size comparison honest, sorting makes the ranking immediate, and end labels let the reader compare the gaps without estimating values from the axis. Russia’s 10.7-year gap is largest among these six; India’s 3.1-year gap is smallest.

## 7. Compare the two visualizations for Question 1

The line chart answers the “how did it change?” part better: it shows that country gaps have different histories and that a single recent ranking would hide them. Its six lines take more effort to compare, especially where the values are close. The sorted bar chart answers “how large is the gap now?” more directly and gives precise values, but it removes the history and can make the selected countries look like a general ranking. The figures work together because one gives temporal context and the other gives a clear endpoint comparison.

## 8. Story/Question 2

Among U.S. counties and county equivalents, how does adult bachelor’s attainment relate to median household income, and is that relationship different between metropolitan and nonmetropolitan counties?

## 9. Visualization 1

[03_census_education_income_scatter.png](figures/03_census_education_income_scatter.png)

## 10. Rationale for Visualization 1

Each dot is a county or county equivalent, positioned by its 2019–23 adult bachelor’s attainment and 2023 median household income. Color separates metro from nonmetro counties, while within-group trend lines and Spearman correlations summarize the direction and strength of the association. The positive association appears in both groups and is stronger among metro counties (ρ = .71, n = 1,156) than nonmetro counties (ρ = .55, n = 1,949). The scatter retains county-level variation that an aggregate chart would hide; the caption also makes clear that these are unweighted county comparisons and do not establish causation.

## 11. Visualization 2

[04_census_income_by_education_quartile.png](figures/04_census_income_by_education_quartile.png)

## 12. Rationale for Visualization 2

I divided counties into four pooled groups by bachelor’s attainment, from lowest (Q1) to highest (Q4), then plotted each group’s median attainment against its median household income, separately for metro and nonmetro counties. The paired lines make the overall upward pattern and the income difference between metro and nonmetro groups easy to compare, while aggregation reduces the overlap in the first chart. The caption states that the points are group medians; they are not individual counties. This summary is easier to read but conceals the within-group spread and outliers shown by the scatterplot.

## 13. Compare the two visualizations for Question 2

The scatterplot is better for seeing variation, overlap, and unusual counties, and it shows the association directly at the county level. Its dense cloud makes individual comparisons difficult. The quartile summary is cleaner and makes the broad pattern and metro/nonmetro separation easier to see, but its four groups hide how much counties vary within each group. The two views use the same measures and status split while making different tradeoffs between detail and summary.

## 14. Story/Question 3

In 2023, how often did net migration offset natural population decline across counties, and how did the two components combine?

## 15. Visualization 3

[05_census_migration_vs_natural_change.png](figures/05_census_migration_vs_natural_change.png)

## 16. Rationale for Visualization 3

The scatterplot places natural change on the horizontal axis and net migration on the vertical axis, with zero reference lines to divide increases from decreases in each component. Color distinguishes metro and nonmetro counties. The upper-left quadrant answers the main question: 1,555 of the 3,105 counties with both rates present had negative natural change but positive net migration in 2023. The full valid rate range is shown, including extreme counties, and the caption avoids attributing a cause to migration.

## 17. Story/Question 4

Did county bachelor’s attainment rise similarly in metropolitan and nonmetropolitan areas from 1990 to 2019–23, or did the gap between their county medians widen?

## 18. Visualization 4

[06_census_attainment_gap_over_time.png](figures/06_census_attainment_gap_over_time.png)

## 19. Rationale for Visualization 4

The line chart uses the four available survey periods as ordered categories and plots the median county share of adults with a bachelor’s degree or higher for metro and nonmetro counties. Both series rise, but the gap between the medians widens from 2.9 percentage points in 1990 to 7.5 points in 2019–23. Direct labels at the end of each line make the latest values clear. The caption identifies the multi-year survey periods and notes that counties, rather than residents, are weighted equally.

## 20. How I made the visualizations

I used the supplied course data files and local assignment references. I used Python 3.14 from the `p314` environment, pandas for filtering, reshaping, summaries, and calculated fields, and Matplotlib to create the six static PNGs. I did not use Tableau; I used conventional worksheet-style encodings such as rows/columns, color, sorting, group summaries, trend lines, and zero reference lines, with restrained formatting. No packages were installed. I did not consult external web pages.

OpenAI Codex (GPT-6) assisted with choosing the stories, analyzing the local data, writing the figure-generation code and chart text, drafting these responses, and critiquing the supplied example. I reviewed the generated images and checked the reported descriptive values against the local files. The images are AI-assisted examples prepared at the instructor’s request, not student-authored Tableau work.
