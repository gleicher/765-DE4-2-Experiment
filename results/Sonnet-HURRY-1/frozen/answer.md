# Design Exercise 4-2 answers (numbered by Canvas order)

Note for Mike: these were drafted by an AI assistant (Claude). Please read and edit into your own words, and keep the disclosure in answer 20. Answer 1 depends on whether you were in the CLO.

## 1. Critique (non-CLO version)

The design is a dumbbell-style plot of the maximum and minimum county median household income within each state, with the ratio printed above each pair. Its strengths: the vertical position encoding is accurate and easy to compare, the ratio labels give the "inequality" number directly, and states are sorted by ratio so the pattern reads left to right. The caption explains what the dots and lines mean.

Problems: (1) The title ("Income inequality varies across states") is a topic, not a finding, and the measure is not really income inequality. Max/min of county medians says how different the richest and poorest county are, not how unequal people's incomes are within a state. The caption should say so. (2) Using the max and min is fragile: one tiny or unusual county sets the ratio, and county population is ignored, so a 3.78x gap in VA may involve very few people at the extremes. A median or interquartile range of counties, or a population-weighted view, would be more robust. (3) Only 16 hand-picked states ("top 5, bottom 5, and 6 additional") are shown, with no stated reason for the extra six, so the audience cannot tell whether the selection is cherry-picked. (4) The axis starts at 0 and the chart is very tall and narrow, leaving the lower third empty; the blue/orange "Max/Min" legend is redundant with the direct labels and is off in the corner. State labels are duplicated (under the orange dots and on the x axis), and the ratio label "3.78x" collides with the blue dot for VA. (5) Blue and orange are fine for color vision, but the gray connector lines are heavy and compete with the dots; a thinner line, or sorting by the gap size with a ratio shown as a second small chart, would help. (6) There is no hint of which county is the max or min, which is the natural follow-up question.

## 2. Story/Question 1 (Life Expectancy)

Women outlive men in almost every country, but how has that female-male life expectancy gap changed since 1960, and is it moving the same way everywhere? (It grew in most countries, shrank in a few, and went from negative to positive in South Asia.)

## 3. Visualization 1 (Q1 primary)

Upload `answers/figures/q1_a_gap_scatter.png`

## 4. Rationale, Visualization 1

I wanted to show change for every country at once, not just a handful, so each country is a dot with its 1960 gap on x and its 2023 gap on y. The diagonal means "no change", so position relative to it directly answers the question: above the line the women's advantage grew, below it shrank. I shaded the two sides lightly and labeled them in words so the viewer does not have to decode the diagonal. Most countries are muted gray, and I highlighted and labeled only the largest shifts in orange (Ukraine, Russia, Pakistan, Iran, Bangladesh, Thailand, Cameroon, Nigeria) and gave a few reference countries (US, Japan, Latvia, Georgia, Qatar) dark labels. The dotted zero lines show the striking left-hand cluster where men outlived women in 1960 (Pakistan, India, Bangladesh, Iran) but women do now. I removed regional aggregates (the World Bank file mixes in "World", "Arab World", etc.) so every dot is a country, and used identical axis units on both axes so the diagonal is a true 45 degree line. The caption gives source, unit definition and the "descriptive only" caveat.

## 5. Visualization 2 (Q1 alternate)

Upload `answers/figures/q1_b_gap_lines.png`

## 6. Rationale, Visualization 2

This version targets a more general audience and shows time explicitly rather than just endpoints. Each line is the female minus male gap from 1960 to 2023 for six chosen countries, drawn against a gray band for the middle half of all countries and a dashed median, so the viewer can see how unusual each story is. I chose countries to represent distinct patterns: the largest rises (Ukraine, Russia, with the 1994 peak annotated), a South Asian reversal (Pakistan and India, from men outliving women to a gap of 3 to 5 years), a decline (United States, 7.4 years in 1980 to 5.3 now) and a stable case (Japan). Lines are labeled directly at the right instead of using a legend, and color is used only to identify countries. The zero line is drawn because crossing it is part of the story. A short annotation explains the one spot where the viewer would otherwise ask "what happened?". The 1971 spike in Pakistan is in the source data and I left it in rather than smoothing it.

## 7. Comparison of the two Q1 visualizations

The scatterplot shows all 213 countries, so it is better at answering "is this common?": most points are above the diagonal, a few below, and it makes outliers easy to find. It also compresses time into two endpoints, so it hides the path (the Soviet-era spike, the 2020 dip) and requires the viewer to read a diagonal reference line, which is harder for a general audience. The line chart is easier to read and shows timing and non-monotonic changes, and the median band gives context, but it can only show a few countries, the choice of those countries is mine, and lines for countries near each other (US, Japan, Pakistan) are close together at the right end. I would use the line chart for a newspaper and the scatterplot for a scientific audience or as an overview.

## 8. Story/Question 2 (Census)

Has the share of adults with a college degree risen in the US since 1990, and did big metro counties and rural counties rise equally, or has the gap between them widened?

## 9. Visualization 1 (Q2 primary)

Upload `answers/figures/q2_a_education_lines.png`

## 10. Rationale, Visualization 1

I used the nine USDA rural-urban continuum codes as an ordered category and a sequential (viridis) color scale from dark (largest metros) to light (most rural), because the categories are ordered. Four time points (1990, 2000, 2008-12, 2019-23) are connected by lines to show trend. Lines are labeled directly at the right, in the same colors, in order of final value, so no legend is needed. The vertical axis is a percentage of adults (25+), pooled over counties so big counties count in proportion to their adult population (a simple average of county percentages would let tiny counties dominate). I emphasized the story by thickening the top and bottom lines, adding the 1990 gap (13 percentage points) and the 2019-23 gap (20 points) as text, and by an arrow at the end. Everyone rises, but the lines fan out. The caption states the definition and that the 2023 codes are applied to all periods.

## 11. Visualization 2 (Q2 alternate)

Upload `answers/figures/q2_b_education_scatter.png`

## 12. Rationale, Visualization 2

Here the unit is the county: each dot is one county, 1990 attainment on x and 2019-23 on y, with a no-change diagonal. Nearly all counties are above the line, so everyone gained. I collapsed the nine codes into three groups (metro; nonmetro adjacent to a metro; nonmetro not adjacent) so color has few levels and stays readable, and used low-opacity small dots to deal with overplotting among 3,000+ counties. Large diamonds mark the pooled average of each group with direct labels ("Metro 22% to 37%", nonmetro 12% to 22% and 13% to 23%), which carry the headline numbers. Metro counties sit up and to the right, and the vertical distance from the diagonal is larger for them, which shows that places that started ahead gained more.

## 13. Comparison of the two Q2 visualizations

The line chart is the clearest for the story of trend and the widening gap, uses the full ordered nine categories, and gives the numbers over time. It hides the variation inside each category and only shows aggregate values. The scatterplot shows the spread within each group, outliers, and the overlap between groups (many nonmetro counties do better than many metro ones), which the line chart cannot, and it supports the "gained the most" comparison with the diagonal. But it only has two time points, is dense in the lower left where most counties are, and uses unweighted dots, which visually over-represents the many tiny rural counties compared with the diamonds, which are population-weighted. The line chart is better as a headline figure and the scatter as a complement that shows that the averages hide a lot of overlap.

## 14. Story/Question 3

Did the 2020 pandemic shock raise unemployment differently in metro and rural counties, and how does it compare with the Great Recession? (Census data)

## 15. Visualization 3

Upload `answers/figures/q3_unemployment_pandemic.png`

## 16. Rationale, Visualization 3

A line chart is the right form for a rate over 24 years. I grouped counties into three types so there are only three lines that can be directly labeled (no legend), with the same color mapping as the education scatterplot. Rates are pooled (total unemployed / total labor force) so big counties are weighted properly. Two gray bands mark the Great Recession and 2020 to give the viewer context to compare the two shocks, and an annotation gives the 2019-to-2020 increase for each group (metro +4.6 points, nonmetro adjacent +3.0, nonmetro not adjacent +2.8). The y axis starts at zero so the spike sizes are honest. The visible stories are that counties next to metros had the highest unemployment in the Great Recession (10.3% in 2010), that in 2020 metro areas jumped the most (to 8.2%), and that all groups converge to about 3.6% by 2023. The caption notes that this is descriptive and not causal.

## 17. Story/Question 4

How often does a country's life expectancy fall from one year to the next, and when and where were the biggest falls? (Our World in Data life expectancy)

## 18. Visualization 4

Upload `answers/figures/q4_owid_drops.png`

## 19. Rationale, Visualization 4

The design has two aligned panels sharing a year axis. The top panel is the share of countries whose life expectancy fell each year, which answers "how often" and makes the COVID years (68% in 2020 and 71% in 2021, versus about 11% in a typical year) stand out in red. The bottom panel shows every country-year's change as a dot, with all ordinary years in light gray so they provide context, and drops of 5 years or more in red with size encoding the size of the drop. I labeled only drops of 13 years or more (Rwanda 1994, Cambodia 1975, Somalia 1991, etc.) so the labels are readable, and the caption explains the choice. Color and size are used redundantly for emphasis, not for a separate variable. I did not name causes in the chart because the data do not contain them. The caption warns that some of the largest drops (Central African Republic 2009) may reflect estimation uncertainty in the source. I used the long OWID time range (from 1950), not the World Bank file, so earlier events are included.

## 20. How the visualizations were made

All six figures were made with Python (the p314 conda environment, version 3.14) using pandas for data processing and matplotlib for the charts, in one script (`work/make_figs.py`) that reads only the course-provided data files. Data processing: World Bank life expectancy was pivoted from tall to wide by sex to compute female minus male, and regional aggregates were removed by keeping only country codes that also have an ISO code in the OWID file. Census data was read as latin-1; state and national rows were dropped; counties were grouped using the 2023 rural-urban continuum codes (metro 1-3, nonmetro adjacent 4/6/8, nonmetro not adjacent 5/7/9); education and unemployment shares are pooled (sums of counts divided by sums of totals). OWID changes were computed as year-over-year differences for consecutive years, countries (rows with ISO codes) only. No outside data was added. AI disclosure: the analysis, code, figure design, and the text of these answers, including the critique, were generated by an AI assistant (Claude, Anthropic, via Claude Code) at my request, and I reviewed them before submitting. [Mike: edit this to say what you actually did yourself.]
