# Design Exercise 4-2 answers (numbered as in Canvas)

## 1. Critique (not in the CLO)
The design ("Income inequality varies across states") shows, for 16 states, the maximum and minimum county median household income as blue and orange dots joined by a gray line, with the max/min ratio printed above each pair. What works: the dumbbell is a sensible way to show a range per state, the ratio labels give the "inequality" number directly, and the caption explains the encoding and the selection (top 5, bottom 5, 6 extras). Problems: (1) The states are ordered by ratio, but the x-axis is an unlabeled-order categorical axis, so the ordering logic is only discoverable from the caption. (2) The vertical axis starts at 0K and the lower third of the plot is empty, wasting space. (3) The ratio of max to min county income is a weak, outlier-driven measure of inequality. It says nothing about the spread among most counties, and it ignores county population, so a tiny county can define a state. It also measures between-county difference, not income inequality among people. The title overclaims. (4) Blue/orange are labeled with the generic "Measure Names" legend (Tableau default) instead of "Highest county / Lowest county". (5) The ratio labels collide with dots (3.78x overlaps the VA dot), and the min labels (state codes) are redundant with the x-axis. (6) Mixing absolute dollars (position) and a ratio (text) makes the two stories compete. A better version would sort states, label the legend meaningfully, trim the axis or use a log scale so the ratio is visible as the length, and encode county count or population.

## 2. Story / Question 1 (Life Expectancy)
Women outlive men almost everywhere, but has that female advantage grown or shrunk since 1960, and where? (The gap widened in 112 of 213 countries, most dramatically in the former USSR, and narrowed in 48, including the US and several oil-rich or West African states.)

## 3. Visualization 1 (upload)
`answers/figures/fig1a_gap_scatter.png`

## 4. Rationale, Visualization 1
Each country is one point, with the 1960 female-minus-male gap on x and the 2023 gap on y. A dashed "no change" diagonal makes the question answerable at a glance: above the line the gap grew, below it the gap shrank. I colored points by direction of change (orange wider, blue narrower, gray within 1 year, a threshold that filters out noise) and labeled the end-of-spectrum cases and recognizable countries (Ukraine, Russia, India, the US, Japan, Togo, UAE) with leader lines placed to avoid overlap. The corner labels name the two regions of the plot so the viewer needs no legend. I removed World Bank regional and income aggregates so each dot is a real country. The title states the finding, and the caption gives the definition of "gap," the counts, and the source. Both axes use the same scale so the diagonal is a true 45 degrees.

## 5. Visualization 2 (upload)
`answers/figures/fig1b_gap_lines.png`

## 6. Rationale, Visualization 2 (Question 1 alternate)
This version shows the time dimension directly: a line for the female-male gap in every country (light gray), the median country in thick black, and six highlighted countries picked for contrasting trajectories (Ukraine and Russia rising, the US falling, Japan drifting up, India crossing from negative to positive, Togo collapsing). The gray "spaghetti" gives context for how typical or unusual the highlighted stories are, while the direct end labels (with the 2023 value) replace a legend. A zero line is marked "men live longer than women." The black median line carries the headline that the typical gap barely changed after 1990. It is aimed at a general-audience reader who thinks in time series.

## 7. Compare the two Question 1 visualizations
The scatter (Viz 1) compares two moments for every country and makes "grew vs shrank" immediate; it reveals the clusters and outliers and gives a count of each. It hides the path: a country that rose then fell looks unchanged. Labeling is also limited because the middle is dense. The line chart (Viz 2) shows the path and the timing of events (the Soviet collapse, India's crossover), and the median line gives a clear baseline, but it is cluttered, since 215 lines overlap and noisy small-country series produce spikes; only a handful of countries can be read precisely. The scatter is better for a quantitative summary and the line chart is better for telling stories about particular countries. Reading the diagonal distance in the scatter takes a bit more learning than following a line.

## 8. Story / Question 2 (Census)
Every kind of U.S. county became more educated since 1970, but did rural counties keep pace with metros? (No: the college-degree gap between big metro and remote rural counties roughly tripled from 1990 to 2019-23.)

## 9. First visualization for Question 2 (upload)
`answers/figures/fig2a_education_lines.png`

## 10. Rationale for the first Question 2 visualization
Line chart of the median county's share of adults with four years of college or more, one line per USDA Rural-Urban Continuum Code (nine codes), over six census periods from 1970 to 2019-23. The nine codes are ordered, so I used a sequential color ramp from big metro (purple) to rural (yellow-green) and labeled each line directly at its end with the code description and its final value, which removes the need for a legend. Medians reduce the effect of tiny counties. The y-axis starts at zero so the divergence is not exaggerated. The fan-out shape is the story. The title states the finding and the caption notes the definitional change between 1980 and 1990 and the number of counties.

## 11. Second visualization for Question 2 (upload)
`answers/figures/fig2b_education_scatter.png`

## 12. Rationale for the second Question 2 visualization
A county-level scatterplot of the education share in 1990 versus 2019-23 (3,164 counties), with a no-change diagonal. Points are translucent so the dense lower-left cluster stays readable, and colored by three collapsed county types (metro, nonmetro next to a metro, remote nonmetro) rather than nine so the colors remain distinguishable. Large outlined circles mark each group's median with direct text labels giving the before and after values and the gain. This view shows the distribution rather than only the medians, so the viewer can see that nearly all counties gained and that metro counties start a little higher, end much higher, and have a longer upper tail.

## 13. Compare the two Question 2 visualizations
The line chart makes the divergence over six time points visible and lets each of nine county types be traced, but it only shows medians, so it hides within-group variation, and the nine similar colors are harder to tell apart in the middle. The scatter shows all 3,164 counties and the spread, and the median markers connect to the lines version, but it has only two time points, overplotting in the dense corner, and no ordering among the three groups beyond color. The line chart is better for the trend; the scatter is better for honesty about variation and for spotting unusual counties.

## 14. Story / Question 3
Which countries lost the most life expectancy in the COVID-19 pandemic (2019 to 2021), and had they recovered by 2023? (Life Expectancy data, Our World in Data.)

## 15. Visualization for Question 3 (upload)
`answers/figures/fig3_covid_life_expectancy.png`

## 16. Rationale for Visualization 3
A dumbbell (Cleveland-style) plot of the 22 countries with the largest drop between 2019 and 2021, plus the US for reference (bold label). Each row has a red dot for the change in 2021 versus 2019 and a blue dot for 2023 versus 2019, joined by a gray bar, with a vertical line at 0 labeling the 2019 level. Using change relative to 2019 puts all countries on a common baseline so both the size of the loss and whether it was recovered are position judgments. Sorting by the size of the drop produces a readable ranking, and the red value labels give exact numbers. Red/blue conveys "low point/after." The caption names the two countries that had not recovered and the data caveat. The title states the main finding.

## 17. Story / Question 4
How did the two big job-market shocks of the century (the Great Recession and COVID-19) hit metro versus non-metro U.S. counties? (Census data.)

## 18. Visualization for Question 4 (upload)
`answers/figures/fig4_unemployment_shocks.png`

## 19. Rationale for Visualization 4
Two linked panels. On the left, labor-force-weighted unemployment rates, 2000-2023, in three county groups (metro, nonmetro next to a metro, remote nonmetro) with the two shocks shaded and the key values annotated. On the right, a grouped bar chart of the percentage-point rise from the last pre-shock year to the peak in each shock, in the same colors. The bars make the main contrast easy to compare, which is hard to judge from the lines: the Great Recession lifted all groups similarly, with the highest levels next to metros, while the pandemic spike was much larger in metro counties (+4.6 points vs +2.8 remote). Weighting by labor force avoids letting tiny counties dominate, and three groups (instead of nine) keep the color encoding clear.

## 20. How these were made (AI disclosure)
These answers and all six figures were produced by an AI assistant (Claude, model Sonnet 5.5, via Claude Code), working for the course instructor as an instructor-requested worked example for private review. This is not a student submission. The AI chose the questions, wrote the Python script (pandas, numpy, matplotlib, run with the p314 conda Python) that processed the data and drew the figures, inspected the rendered images, revised the layouts, and wrote all text including this critique. No human drew or wrote the content. Data processing: used the saved data files only (no external data); removed World Bank aggregates by keeping countries that OWID lists with ISO codes; for the census data, kept counties with a 2023 Rural-Urban Continuum Code, grouped codes into metro (1-3), nonmetro adjacent (4, 6, 8), and remote (5, 7, 9) for some figures; used medians for education and labor-force-weighted means for unemployment; no joins with outside data. The script is work/make_figures.py.
