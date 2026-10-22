# Design Exercise 4-2 answers (numbered to match the Canvas questions)

Figure files are in `answers/figures/`.

## 1. Critique (no CLO)

The design is a dumbbell chart that shows, for 16 states, the highest and lowest county median household income in 2021, with the max/min ratio labeled above each pair. Its strengths: the blue/orange dots and the gray connector make the within-state spread easy to see, the "1.01x ... 3.78x" labels give the key number directly, and the caption explains what the dots and lines mean. The story is clear and the chart is easy to read.

Weaknesses: (1) The title ("Income inequality varies across states") is generic and states no finding. (2) The claim is about inequality, but the max/min ratio of county medians is a poor inequality measure. It depends on two extreme, often tiny, counties, and says nothing about spread within counties or about the rest of the distribution. The wording should be "the gap between the richest and poorest county". (3) The y-axis starts at 0K, which wastes the bottom third of the plot, and a dumbbell does not need a zero baseline. (4) The states are ordered by ratio, but the order looks arbitrary (WY, AK, ND ...), and the selection of 16 states ("top 5, bottom 5, and 6 additional") is explained only in the caption. A reader cannot tell why those six were picked. (5) Labels collide with marks ("3.78x" touches the VA dot, "1.01x" and the WY dot overlap), and the legend title "Measure Names" is Tableau's default, not a human label. (6) The state codes appear both on the axis and under or over the dots, which is redundant. A better version would sort by ratio or gap, trim the axis, name the legend "Highest-income county / Lowest-income county", and state a finding in the title.

## 2. Story/Question 1 (Life Expectancy)

Women outlive men in almost every country, but is that female advantage shrinking or growing, and does it follow the same path everywhere? (World Bank data, 1960-2023.)

## 3. Visualization 1 (upload)

`answers/figures/q1a_gap_lines.png`

## 4. Rationale for Visualization 1

I computed one number per country-year, the female-minus-male gap in life expectancy, so the story is a single comparable line per country and not two lines per country. A line chart is the natural encoding for change over time. I chose eight countries on purpose instead of plotting all of them: Russia and Ukraine (the largest gaps), Japan, the United States and China (large, familiar countries with steady gaps), India and Bangladesh (gap flips from negative to positive) and Nigeria (gap shrinking toward zero). Together they show the range of trajectories. A dashed reference line at zero marks "men and women equal", so the crossing in India and Bangladesh is easy to see. I labeled each line at its end instead of using a legend, to avoid matching colors to a key. I used a standard categorical palette, a plain white background with light gridlines, and a title that states the finding. The caption notes that the 1971 Bangladesh spike is a data artifact of the war year, so it is not read as a real trend.

## 5. Visualization 2 for Question 1 (upload)

`answers/figures/q1b_gap_dumbbell.png`

## 6. Rationale for Visualization 2 (Question 1 alternate)

This version drops the time axis and compares only two moments, 1960 and 2023, for 18 countries. Each country is a row with a blue dot (1960) and an orange dot (2023) joined by a line, so the length and direction of the connector is the change. Rows are sorted by the 2023 gap, so the countries with the biggest female advantage are at the top and the pattern (Eastern Europe up top, Gulf states and West Africa at the bottom) reads as a ranking. I picked the five smallest and seven largest 2023 gaps (excluding regional aggregates) plus seven big countries for reference, so the extremes are shown without being a data dump. A dashed zero line and a two-color legend for the years complete it.

## 7. Compare the two Question 1 visualizations

The line chart (1A) shows the whole path, so it reveals timing: Russia's jump after 1990, the Ukraine jump in 2022, and India and Bangladesh crossing zero. Its cost is that only eight countries fit before the chart gets crowded, and the end labels needed manual nudging. The dumbbell (1B) shows many more countries and ranks them, so it is better for "who is highest and who has changed most", but it only shows two years and hides anything that happened in between (for example Russia's drop and rise, and the US gap shrinking and then flattening). The line chart is better for the "how" and the dumbbell for the "where". I would use the dumbbell for a quick overview and the line chart to explain the specific cases.

## 8. Story/Question 2 (Census)

Do counties with more college-educated adults have lower unemployment, and is that relationship the same in metro, nearby rural and remote rural counties?

## 9. Visualization 1 for Question 2 (upload)

`answers/figures/q2a_scatter.png`

## 10. Rationale for Visualization 1

A scatter plot is the standard way to show a relationship between two quantitative measures, here the share of adults with a bachelor's degree or higher (2019-23) and the 2023 unemployment rate, with each county as a mark. I colored the counties by a three-way rural-urban group built from the 2023 Rural-urban Continuum Code (metro 1-3, nonmetro adjacent 4/6/8, nonmetro not adjacent 5/7/9), so that the urban/rural dimension is explicit. I sized the circles by 2020 population so that big counties are visible and tiny counties do not dominate, and made them semi-transparent to cope with overplotting in the crowded 10-30% range. A linear trend line for each group shows that all three slope downward (correlation about -0.29 within each group, roughly -0.03 to -0.05 points of unemployment per additional percentage point of graduates). I cut the axis at 12% unemployment to remove a few extreme outliers and said so in the caption.

## 11. Visualization 2 for Question 2 (upload)

`answers/figures/q2b_bars.png`

## 12. Rationale for Visualization 2

This is a summary view for a general audience. Counties are binned into four education quartiles, and a grouped bar chart shows the median unemployment rate for each rural-urban group in each quartile, with the values printed on the bars. Bars on a zero baseline make the differences easy to compare, and the same three colors are used as in the scatter plot so the two figures are consistent. Medians are used instead of means because county unemployment rates are skewed by small counties. The bars show a steady decline: from about 3.8-4.1% in the lowest-education quartile to about 3.0-3.1% in the highest, in every group.

## 13. Compare the two Question 2 visualizations

The scatter plot shows every county, so you can see the spread, the overlap between groups, the outliers and the population sizes, and the trend lines give the slope. But it is busy, and the overplotting hides the differences between the groups. The bar chart is much easier to read and gives exact numbers, but it hides the within-group variation (medians only), loses the population information, and depends on the arbitrary choice of quartiles. It also exposes a quirk that the scatter hides: in the third quartile, remote rural counties have a lower median (2.6%) than metro counties (3.5%). The scatter plot is better for the analyst and the bar chart for a quick public message.

## 14. Story/Question 3

Did the 2009 recession and the 2020 pandemic affect unemployment differently in metro, nearby rural and remote rural counties? (Census data.)

## 15. Visualization 3 (upload)

`answers/figures/q3_unemployment_time.png`

## 16. Rationale for Visualization 3

A line chart of the yearly unemployment rate, 2000-2023, with one line per rural-urban group. The rate is computed as total unemployed divided by total labor force for the group (not an average of county rates), so large counties count in proportion to their size. Two dotted vertical reference lines at 2009 and 2020 point the viewer to the two shocks, and the title states the two findings: in 2020 the metro rate jumped to 8.2% against about 7% elsewhere, while in 2009-2010 the nonmetro-adjacent counties peaked highest (10.3%, against 9.7% for metro and 9.1% for remote counties). I kept the colors from the Question 2 figures so that groups are consistent, and used a legend to the right because the lines converge at the end and direct labels would overlap.

## 17. Story/Question 4

Which states gained residents from other states in 2021-2023, and which lost them? (Census data.)

## 18. Visualization 4 (upload)

`answers/figures/q4_migration_states.png`

## 19. Rationale for Visualization 4

A sorted horizontal bar chart of each state's net domestic migration per 1,000 residents, averaged over 2021, 2022 and 2023. I used the per-1,000 rate, not the raw count, so that small states can be compared with large ones, and averaged three years to smooth out one-year noise. Bars are colored by sign (blue = net gain, red = net loss) on a zero line, and sorted so the winners and losers are at opposite ends; the values are printed on the bars so that the figure can be read without hovering. The tall format fits all 50 states plus DC so that no state is hidden, and the title names the extremes (Idaho gained 16.8 per 1,000, New York lost 13.6).

## 20. How I made these visualizations

All of the work was done by an AI assistant (Claude, model Sonnet 5.5, in Claude Code) at the instructor's request, as an example response and not a student submission. The assistant read the assignment and data files, chose the stories, wrote the analysis and figure code, checked the output images, and wrote this text. Tableau was NOT used (it is not installed in this environment). The figures were made with Python (pandas, numpy, matplotlib) and styled to look like Tableau worksheets (Tableau 10 palette, Arial, light gridlines, side legends). Data processing: the World Bank file was pivoted so that female and male are columns and the gap computed per country-year (regional aggregates were excluded from the Question 1B selection); county data were read with latin-1 encoding and grouped by 2023 Rural-urban Continuum Code; counties with missing education or unemployment values were dropped from Question 2; unemployment rates for Question 3 were computed as summed unemployed over summed labor force; and state migration used the 2021-2023 rates from the state-level file, averaged. No outside data were added. The script is `work/make_figures.py`.
