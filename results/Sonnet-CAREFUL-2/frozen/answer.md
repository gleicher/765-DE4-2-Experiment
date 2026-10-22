# Design Exercise 4-2: answers (numbered to match the Canvas questions)

*Instructor-requested example response (not a student submission).*

## 1. Critique (no CLO)

The design is a dumbbell chart of the maximum and minimum county median household income in 16 states, with the max/min ratio printed above each pair. It has a good idea at its core: a dumbbell is a sensible encoding for "how far apart are the extremes", and the ratio labels turn the gap into a number that can be compared across states. The caption also says what the dots and lines mean.

The problems are mostly about whether the chart actually delivers the title. "Income inequality varies across states" is a very weak claim, and the chart does not really measure inequality. The gap between the richest and poorest county's median income is driven by a single outlier county at each end, and it ignores how many people live in each county. Virginia's 3.78x, for example, is likely driven by a small independent city at one end and a wealthy Washington, D.C., suburb at the other. A reader could take the chart as saying that Virginia is the most unequal state when it only says that Virginia has the most extreme pair of counties.

The ordering is also a problem. The x axis is sorted by the ratio, but this is not stated anywhere except in the caption, and the vertical axis shows dollars. The reader has to look at the pale gray line lengths and then read a small label to see the ratio, so the encoding for the claimed message (the ratio) is the weakest one in the picture. Sorting by ratio and encoding the ratio directly (for example, as a bar or a dot on its own scale) would be more direct. The y axis starts at zero, which pushes all the points into the upper two thirds of the plot and makes the lines look long. That is not wrong for a dumbbell, but it does not help.

On details: the blue and orange legend titled "Measure Names" is leaked Tableau default text and should say "Highest county" and "Lowest county". The labels for the minimum dots sit below the dot while the ratio sits above the maximum, which makes it harder to match the state name with its pair. The caption is long, and it is the only place that explains the selection of the "top 5, bottom 5, and 6 additional interested states". The 6 additional states are not distinguished from the top and bottom ones, so the sampling is unclear. The title would be much stronger if it stated the finding, for example "Virginia's richest county is 3.8 times its poorest; Wyoming's are nearly equal."

In short, a reasonable standard design with a mildly misleading story and several Tableau leftovers. With a clearer measure (such as an interquartile range or a population-weighted comparison), a sorted layout and a finding-style title, it would be a good chart.

## 2. Story / Question 1 (Life Expectancy)

Women outlive men almost everywhere, but is that advantage shrinking? Using the World Bank sex-specific life expectancy for 1960-2023, I ask how the female-minus-male gap has changed over time and whether the change is the same in different countries. The answer is no: it narrowed in the US and parts of western Europe, grew sharply in Russia and other post-Soviet states, and went from negative to positive in South Asia.

## 3. Visualization 1 for Question 1

`figures/q1_primary_gender_gap_lines.png`

## 4. Rationale for Visualization 1

The question is about change over time, so I used a line chart with year on the x axis and the gap (female minus male life expectancy) on the y axis. Showing the gap directly, rather than two separate lines for men and women, makes the quantity I care about the one that is read from position. There are about 215 countries, which would be unreadable if all were colored, so I drew every country as a thin light gray line to give context and the range, and then picked five countries to highlight in color with direct labels instead of a legend: Russia (largest and most dramatic swing), the United States (decline), Japan (stable), India (from negative to positive), and South Africa (HIV/AIDS). I annotated two features on the chart rather than leaving them to the caption: Russia's 1994 peak of 14.2 years and India's crossing of zero. I used a zero line because the sign of the gap matters. Colors come from the Okabe-Ito colorblind-safe palette. I removed regional and income aggregates (e.g., "World", "Arab World") by keeping only the countries that appear as real countries in the second data set, so that the gray background represents countries only. The title states the finding, and the caption gives specific numbers.

## 5. Visualization 2 for Question 1

`figures/q1_alt_gender_gap_dotplot.png`

## 6. Rationale for Visualization 2 (Question 1 alternate)

This version targets a reader who wants to compare countries directly and does not need every year. It is a Cleveland-style dot plot with one row per country and three dots per row for 1960, 1990 and 2023, connected by a gray line. I chose 18 countries to cover the patterns (post-Soviet, rich countries that peaked and narrowed, East Asia, Latin America, South Asia/Iran, and sub-Saharan Africa) and sorted the rows by the 2023 gap so the current ranking reads from top to bottom. A zero line separates a male advantage from a female one, which makes it easy to see that India, Pakistan, Bangladesh and Iran had to cross it. The colors are ordered from light blue (earliest) to gray to vermilion (latest) so the reader can see the direction of travel without a legend lookup. The caption points to the three groups of countries, so the picture can stand alone.

## 7. Compare the two visualizations for Question 1

The line chart shows the whole trajectory: timing matters, and you can see the sudden jump in Russia in the early 1990s, the slow decline in the US and the dip in South Africa. The gray background also shows how typical or unusual the highlighted countries are. The cost is that only five countries are readable, it is hard to compare specific values between two countries, and the gray tangle (including some noisy lines from very small countries) is cluttered. The dot plot is cleaner and makes ranking and exact comparison easy for 18 countries, and the zero crossings are very clear, but it only samples three years, so it hides the timing and the 1994 peak, and the choice of countries is mine. I think the line chart is the better primary graphic for the "how has it changed" question; the dot plot is better for a short, print-style summary.

## 8. Story / Question 2 (Census)

Did the Great Recession and the 2020 pandemic hit unemployment differently in big-city and rural counties? Using the USDA county data (rural-urban continuum codes and yearly unemployment, 2000-2023), I compare how much unemployment rose in each type of county in each downturn. The answer: the pandemic shock grew with the size of the place, while in the Great Recession the metro and nearby rural counties rose by similar amounts and only the most remote counties were spared.

## 9. Visualization 1 for Question 2

`figures/q2_primary_unemployment_lines.png`

## 10. Rationale for Visualization 1 (Question 2)

A line chart of the yearly unemployment rate is the natural way to show two downturns on one timeline. The nine rural-urban continuum codes are too many lines to read, so I grouped them into four: large metro, other metro, nonmetro adjacent to a metro area, and nonmetro remote. Rates are pooled (total unemployed divided by total labor force in the group) rather than averaged across counties, so that a tiny county does not count the same as Los Angeles County. I used a blue pair for metro and an orange/vermilion pair for nonmetro so the metro/nonmetro split is obvious but the subgroups are still distinguishable. Gray bands mark the two downturns, and the two annotations carry the story: large metros jump to 8.6% in 2020 (+5.0 points), while in 2009-10 the metro-adjacent rural counties peak highest (10.3%). A note in the plot says the groups converge at 3.6-3.7% by 2023. The legend sits in the empty bottom-left region so that the lines are not labeled at crowded endpoints. The y axis starts at 2% rather than 0 because the interest is in the differences between lines, which is acceptable for a line chart.

## 11. Visualization 2 for Question 2

`figures/q2_alt_unemployment_change_strip.png`

## 12. Rationale for Visualization 2 (Question 2)

The line chart pools counties and so hides the spread within each type. This second view shows every county. The left panel shows the change in unemployment rate from 2007 to 2009 and the right panel from 2019 to 2020, with one row for each of the nine rural-urban codes (kept ungrouped so that the reader can see a gradient), ordered from the largest metro areas at the top to the most rural at the bottom. Each county is a jittered dot, with the median (white circle), the middle half of counties (black bar) and the median value printed in a fixed column at the right. I used the same x axis in both panels so the two downturns can be compared directly, and a dashed line separates metro from nonmetro rows. Blue is used for metro and vermilion for nonmetro, consistent with the first figure. The title states the finding: remote rural counties rose least both times, and in 2020 the rise shrinks steadily with the size of the place (+3.4 to +1.5 points).

## 13. Compare the two visualizations for Question 2

The line chart is better for the overall story and for timing: it shows the whole 24 years, the recovery, the convergence in 2023, and the difference between the two events at a glance, and it is easy for a general audience to read. It is also the only one that shows the actual level of unemployment. But pooling hides variation, and four groups are a simplification of nine codes. The strip chart shows every county and the full distribution, uses all nine codes and exposes the gradient in 2020, and shows that the groups overlap a lot (the differences in medians are modest compared with the spread). However, it shows only changes between two pairs of years, not levels or recovery, is denser, and takes more effort to read because a viewer has to understand medians and interquartile bars. I would give the first to a newspaper audience and the second to a more technical one.

## 14. Story / Question for Visualization 3

Education and place: did college attainment rise everywhere between 1990 and 2019-23, and did the gap between big-city and rural counties widen? (Census data)

## 15. Visualization 3

`figures/q3_education_scatter.png`

## 16. Rationale for Visualization 3

I used a scatterplot of each county's share of adults with a bachelor's degree or higher in 1990 (x) against 2019-23 (y), with a dashed "no change" line. Every point above the line gained, and the vertical distance above the line is the size of the gain; this lets the reader see that all counties gained and also the gradient of how much. Color shows the same four rural-urban groups used elsewhere in the set, and bubble area shows the county population so that the large metro counties, where most people live, stand out, while the many small rural counties are drawn small and with transparency to reduce overplotting. The large outlined dots mark each group's median county, and the labels give the 1990 and 2019-23 values (for example, large metro 15% to 31%, remote nonmetro 12% to 20%). This turns the scatter into the finding: the gap between the large metro and remote medians grew from about 3 to 11 points. The labels are placed away from the dense cloud with leader lines and a white background so they are readable. The title states the finding and the caption explains the encodings and gives the source and the number of counties.

## 17. Story / Question for Visualization 4

Did the COVID-19 pandemic reverse the long rise in life expectancy, and have countries recovered? (Life Expectancy, Our World in Data)

## 18. Visualization 4

`figures/q4_covid_life_expectancy.png`

## 19. Rationale for Visualization 4

This is a scatterplot of each country's life-expectancy loss from 2019 to 2021 (x) against its rebound from 2021 to 2023 (y). The dashed diagonal is the line of full recovery (rebound exactly equals the loss), so the position relative to a single reference line answers the question "back to 2019 or not?" for every country at once. I shaded the two sides of the line (green above, orange below) and colored the dots to match, and added a direct text note in each region instead of relying on a legend alone. Most points fall at or above the line, which makes the headline "most countries recovered" visible in one glance, and the points' distance from the origin tells how hard each country was hit. I labeled a small set of recognizable cases (Bolivia, Mexico, Peru and Paraguay as the largest drops; the United States, India, Russia and South Africa as large countries; Japan, China and Germany as nearly unaffected; and Libya and Palestine as the outliers below the line) rather than all 235. I used the Our World in Data series because it has data through 2023 and long histories; I excluded the Central African Republic because its 2019 value is implausible (31.5 years) and would compress the axes. I used the same green/vermilion colors that are colorblind-safe in the Okabe-Ito set.

## 20. How the visualizations were made

All six figures were made with a single Python script (`work/make_figures.py`), using pandas for data processing and matplotlib for drawing, run with the `p314` conda environment's Python. No other tools were used and no packages were installed. Data processing: the World Bank file was pivoted from tall to wide to compute female minus male life expectancy, and restricted to countries by matching country codes against the Our World in Data file (this removes regional and income aggregates). For the census data, I dropped the national and state rows, grouped the nine 2023 rural-urban continuum codes into four groups (large metro, other metro, nonmetro adjacent, nonmetro remote), computed pooled unemployment rates as total unemployed divided by total civilian labor force, and used the percent of adults with a bachelor's degree or higher for the education chart. 17 counties without a rural-urban code (Alaska, Connecticut and one in Montana) were omitted. For the life expectancy loss and rebound I used the OWID series for 2019, 2021 and 2023 and dropped the Central African Republic. No outside data were added.

**AI disclosure:** This work was produced entirely by an AI assistant (Claude, Sonnet 5.5, run through Claude Code), at the request of the course instructor, as an example response for the instructor's private review; it is not a student submission. The AI chose the stories, wrote the code, designed the figures, checked the results by viewing the rendered images and fixed layout and wording problems, and wrote all of the text above, including the critique. The instructor directed the task (complete the assignment to an A-level standard) but did not supply the designs or text.
