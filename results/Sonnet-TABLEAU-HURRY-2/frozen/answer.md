# Design Exercise 4-2 answers (numbered to match the Canvas questions)

Figures are in `answers/figures/`. Figure files: `q1_a_gap_scatter.png`, `q1_b_gap_lines.png`,
`q2_a_unemployment_lines.png`, `q2_b_unemployment_bars.png`, `q3_state_migration.png`, `q4_education_income.png`.

## 1. Critique (not in the CLO)

The design is a dumbbell chart: for each of 16 states the blue dot is the maximum county median household income, the orange dot is the minimum, a gray line joins them, and the label is the max/min ratio. Good: the dumbbell makes the within-state spread easy to see, the ratio labels give a precise number, the states are sorted by ratio so the pattern rises left to right, and the caption explains the encoding and states the extremes (WY 1.01x, VA 3.78x). Problems: (1) The title ("Income inequality varies across states") is vague and does not state the finding, and a max/min ratio of county medians is a weak measure of inequality (it depends on one tiny and one huge county, not on the income distribution), so calling it "inequality" overreaches. (2) The state selection ("top 5, bottom 5 and 6 additional interested states") is arbitrary and only explained at the end of the caption; the viewer cannot tell why those states are shown. (3) The legend uses Tableau's default "Measure Names / Max. / Min." and the axis title is only "State" at the top, so it feels like a default worksheet. (4) Several labels collide with marks (the 3.78x label touches the VA dot, WY's two dots overlap, and the min labels sit on the state letters), and the y axis starts at 0K although no data are below 30K, which wastes about a fifth of the plot and compresses the differences. Improvements: a title that states the finding, a clearer measure (for example the ratio of the 90th to the 10th percentile county, or a population-weighted measure), a consistent and explained selection rule, a truncated axis starting near 20K, and non-overlapping labels.

## 2. Story/Question 1 (Life Expectancy)

Has women's life-expectancy advantage over men (female minus male life expectancy at birth) grown since 1960, and is the change the same everywhere? It grew in about two-thirds of countries (142 of 213, median gap 4.1 years in 1960 and 5.0 in 2023), but some countries (Ukraine, Russia, Pakistan) widened sharply while others (Nigeria, Cameroon, the Gulf states) narrowed.

## 3. Visualization 1 for Question 1

Upload `answers/figures/q1_a_gap_scatter.png`

## 4. Rationale for Visualization 1

I wanted to compare each country with itself at two times, so each country is one dot with the 1960 gap on x and the 2023 gap on y, and a dashed 45-degree reference line marks "no change". Position along a common scale makes it easy to see which side of the line a country falls on, and the whole distribution (most dots above the line) answers the "two-thirds" question at a glance. I built a simple calculated field (gap in 2023 greater than gap in 1960) and used it for color, with blue for wider and orange for narrower, so the split is encoded redundantly with position. I limited the data to real countries (World Bank regional aggregates removed) and to countries with data in both years, and I labeled only the notable outliers (Ukraine, Russia, Latvia, Pakistan, India, Nigeria, Cameroon, the UAE, and a few well-known countries for context) so the chart is not cluttered. The title states the finding, axes are in years, the legend is titled, and the caption gives the count and the key examples.

## 5. Visualization 2 for Question 1

Upload `answers/figures/q1_b_gap_lines.png`

## 6. Rationale for Visualization 2 (Question 1 alternate)

The alternate shows the same story as a time series so the viewer can see when and how the gap changed, not just the endpoints. The x axis is year, the y axis is the gap (female minus male) in years, and a zero reference line marks where men would live longer. A thick gray line shows the median of all countries as the baseline (4.1 years in 1960, about 5.3 around 1990, 5.0 in 2023), and six highlighted countries in a standard categorical palette show the contrast: Russia and Ukraine rise to 10-13 years (Russia peaked at 14.2 in 1994, annotated), the United States rises to 8.1 in 1968 and then falls to 5.3, India goes from negative to positive, and Nigeria nearly closes. Lines are labeled directly at their right end with the 2023 value, which avoids a legend lookup, and the rest of the countries are not shown to avoid a spaghetti chart. The caption defines the gap and explains the highlighted countries.

## 7. Comparison of the two Question 1 visualizations

The scatter plot covers all 213 countries and directly answers "how many countries widened vs. narrowed", and the reference line makes the comparison easy; its weakness is that it only uses two years, so it hides the path between them (for example the U.S. rise and fall, or Russia's spike in 1994), and the axes (a 1960 value against a 2023 value of the same quantity) take a moment to understand for a general reader. The line chart is more familiar and shows timing and turning points, and the median baseline gives context, but it can only show a handful of countries chosen by me, so it does not show how common each pattern is, and the labels at the right need care to avoid overlap. I would use the scatter for a scientific audience that wants the whole distribution and the line chart for a newspaper audience that wants stories about specific countries.

## 8. Story/Question 2 (Census)

Did the 2020 pandemic spike in unemployment hit urban (metro) counties harder than rural counties? Yes: from 2019 to 2020 the unemployment rate rose 4.6 percentage points in metro counties (3.6% to 8.2%) but only 2.4 points in the most rural counties, and all groups were back near 3.6% by 2022.

## 9. Visualization 1 for Question 2

Upload `answers/figures/q2_a_unemployment_lines.png`

## 10. Rationale for Visualization 1 (Question 2)

A line chart of the unemployment rate by year (2015 to 2023) is the standard design for change over time, and it shows the 2020 spike, the recovery, and the fact that by 2022 the groups converge. Because 3,000+ counties are too many to draw and counties vary hugely in size, I aggregated: I grouped counties by the 2023 Rural-urban Continuum Code into three groups (Metro, codes 1-3; smaller nonmetro, 4-7; most rural nonmetro, 8-9) and computed the group rate as total unemployed divided by total civilian labor force (not the average of county rates, which would overweight tiny counties). Three lines in blue, orange and green are easy to tell apart, the 2020 peak values are labeled, and a dashed vertical reference line marks 2020. I started the y axis at 0% so the heights of the spike are honest, and used only counties with complete data for 2015-2023 (3,094 counties, noted in the caption).

## 11. Visualization 2 for Question 2

Upload `answers/figures/q2_b_unemployment_bars.png`

## 12. Rationale for Visualization 2 (Question 2)

The alternate focuses on the single quantity that answers the question: the increase in the unemployment rate from 2019 to 2020 (a calculated difference) for each of the nine Rural-urban Continuum Codes, shown as sorted-by-code horizontal bars with the value labeled on each bar. Bars on a common zero baseline make the size of the differences easy to compare (+5.1 points for code 1, down to +2.1 for code 9). I kept all nine codes rather than my three groups so the viewer can see the gradient and its small exceptions (codes 4 and 5 are slightly higher than code 3), and I kept the group colors from the first chart (blue for metro, orange for smaller nonmetro, green for most rural) so the two charts read as a pair. Labels name the metro-size categories for codes 1-3; for codes 4-9 I only say nonmetro since the data files do not define them, and the caption says higher codes are less urban.

## 13. Comparison of the two Question 2 visualizations

The line chart shows the whole time period, so it also shows that metro counties had the lowest unemployment before 2020, the highest peak, and a full convergence by 2022; that context is lost in the bar chart. However, reading the size of the gap between the lines at the peak requires comparing vertical distances between points, and nine codes would make the lines messy, so it uses three coarse groups. The bar chart answers the specific question more directly, with exact values and the gradient across all nine codes, but it only shows one change (2019 to 2020) and hides recovery. The bar chart is the better one for the headline, and the line chart is the better one for context.

## 14. Question/Story for Visualization 3

Which states gained the most (and lost the most) residents from domestic migration between 2020 and 2023, relative to their size? (Census data.)

## 15. Visualization 3

Upload `answers/figures/q3_state_migration.png`

## 16. Rationale for Visualization 3

I summed the county-level domestic migration estimates for 2020-2023 to the state level and divided by the state's 2020 census population (per 1,000 residents), because raw counts would just show that big states (Texas, Florida, California, New York) have big numbers. Showing the top 10 and bottom 10 states (a Top N filter) keeps the chart readable instead of listing all 50, and a sorted horizontal bar chart with state abbreviations on the axis gives the easy-to-read ranking. Blue for gains and orange for losses (with a zero line and labeled values) separates the two directions at a glance; Idaho (+57 per 1,000) and New York (-44) are the extremes. Puerto Rico and Connecticut are excluded because their county-level data are not comparable (Connecticut's counties were replaced by planning regions), and the caption says so.

## 17. Question/Story for Visualization 4

Is a county's level of education related to its median household income, and is the relationship the same in metro and nonmetro counties? (Census data.)

## 18. Visualization 4

Upload `answers/figures/q4_education_income.png`

## 19. Rationale for Visualization 4

A scatter plot is the standard way to show a relationship between two numeric variables across many items, with one dot per county (3,095 counties). The x axis is the percent of adults with a bachelor's degree or higher (2019-23) and the y axis is median household income (2023). I added color for metro (Rural-urban Continuum Codes 1-3) versus nonmetro (4-9), a size encoding for 2020 population so that large counties are not visually equal to tiny ones, and partial transparency to handle overplotting. A separate linear trend line for each type shows the main finding: each additional percentage point of college graduates goes with about $1,191 more median income in metro counties and $916 in nonmetro counties, so the relationship is positive in both but steeper in metro areas (overall correlation 0.73). The title states the finding, and the caption notes that this is correlation, not causation, and that one county reporting 0% was dropped.

## 20. How the visualizations were made (disclosure)

These visualizations and this write-up were produced by an AI assistant (Claude, a large language model from Anthropic, running as Claude Code), at the request of the course instructor, as an example response for the instructor's private review. They are not a student submission and no student did the analysis. I did not use Tableau, even though the figures are styled to look like Tableau worksheets and are designed to be buildable with standard Tableau operations (aggregation, color, labels, sorting, Top N filter, reference lines, trend lines and simple calculated fields). The charts were drawn with Python (pandas and matplotlib, run with the p314 environment's Python 3.14); the script is `work/make_figures.py`. Data processing: for life expectancy I used the World Bank file (`lifespan_dataset_1960.csv`), kept only countries (dropping World Bank regional and income-group aggregates, using the country codes in the Our World in Data file as the list of real countries), and calculated the gap as female minus male life expectancy. For the census data I used `full_census_dataset.csv` (which is comma-separated, despite the readme), grouped counties by the 2023 Rural-urban Continuum Code, computed rates as sums of unemployed divided by sums of the labor force, summed county migration to states, and dropped counties with missing values for the relevant fields (and Puerto Rico and Connecticut for the migration chart). No outside data were added. No web pages were consulted.
