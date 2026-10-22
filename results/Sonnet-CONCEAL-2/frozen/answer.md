# Design Exercise 4-2 answers

Numbers match the Canvas questions.

## 1. Critique

The question is a good one (does income inequality inside a state vary a lot?) and the dumbbell idea fits it: each state's max and min county are connected by a line. Things that work: the ratio labels (1.01x to 3.78x) give the actual answer, and the caption explains what the dots are. The problems:

- The title ("Income inequality varies across states") is vague and doesn't state the finding. "Virginia's richest county has 3.8x the median income of its poorest" would be better.
- The states are sorted by ratio, but the y axis is absolute dollars, so the thing being sorted by (the ratio) is not what the position encodes. A long line is not the same as a high ratio. Look at AL versus GA. A log scale or plotting the ratio directly would fix this.
- The chart is a gap between the max and min counties of a state, and that is a bad summary of inequality. It depends on two extreme counties, which can be tiny, so it says nothing about how most people live. It also isn't inequality between households, and the title and caption call it that.
- Blue and orange are used for max and min, but the legend says "Measure Names" (a Tableau default). The labels for min dots and the ratio labels sit in different places and the 3.78x label collides with the VA dot.
- Only 16 states are shown, picked as "top 5, bottom 5 and 6 others". That is not a clear rule and it isn't obvious why those 6 are included. The y axis starts at 0K which wastes the bottom third of the chart.
- Gray gridlines and lines are fine, but the chart is very tall, with a lot of empty space.

Overall: right idea, but the encoding doesn't match the ratio claim and the title doesn't tell the story.

## 2. Story / Question 1 (Life Expectancy)

Women live longer than men, but is that gap still growing? I looked at the female minus male life expectancy gap from 1960 to 2023 and asked whether it keeps widening as countries get richer, or whether it peaks and then shrinks.

## 3. Visualization 1 (Question 1)

Upload: `figures/q1_vis1_gap_by_income_group.png`

## 4. Rationale for Visualization 1

A line chart is the obvious choice for a gap over 64 years. I used the World Bank income groups instead of 200+ countries so there are only four lines, which can be directly labeled instead of using a legend. The y axis is the gap itself (female minus male) rather than two separate life expectancy lines, because the gap is what I want the viewer to read. I annotated the high-income peak (7.5 years in 1994) because that is where the story turns, and I labeled the 1971 spike in the lower-middle group so people don't read it as real (it is a war-year artifact, I believe from Bangladesh, but that is my guess about the cause and I haven't checked it). Colors are a categorical set, kept distinct for the two groups that cross near 2017. The axis starts at zero, which makes the size of the gaps honest.

## 5. Visualization 2 (Question 1 alternate)

Upload: `figures/q1_vis2_gap_dumbbell_countries.png`

## 6. Rationale for Visualization 2

Income groups hide individual countries, so the alternate shows 20 large countries. Each row is a dumbbell from the 1960 gap (gray) to the 2023 gap, and a tick shows the peak value with the year. Color on the 2023 dot marks whether the country is more than half a year below its own peak (red) or still near it (blue). The reader sees the per-country peak-then-fall pattern directly and can see which countries are exceptions (India, Pakistan, China, South Africa). I sorted by the 2023 gap so the rows are in order, and the vertical zero line shows where men outlived women in 1960.

## 7. Comparison for Question 1

The line chart is easier to read and gives the trend over time, but it only shows groups, so it can't tell you whether a given country follows the pattern. It also hides the 2020 and 1971 oddities unless you annotate. The dumbbell chart shows specific countries and the peak, which is the main point, but it only shows three time points (1960, peak, 2023) and the choice of 20 countries is mine, so it could be cherry-picked. It also needs more explanation (three symbols) than the lines. If I could only use one, I'd use the line chart for a general audience and the dumbbell for a reader who wants to look up a country.

## 8. Story / Question 2 (Census)

Do counties with more college-educated adults have lower unemployment, and did that relationship hold up during the 2020 pandemic?

## 9. Visualization 1 (Question 2)

Upload: `figures/q2_vis1_unemployment_by_education_tier.png`

## 10. Rationale for Visualization 1

I split counties into thirds by their 2019-23 bachelor's degree share and plotted the median unemployment rate for each third from 2000 to 2023. Lines let the reader see that the ordering (low education = high unemployment) holds in almost every year, including the Great Recession, which I shaded. I used orange for lowest and blue for highest with a neutral gray for the middle, and direct labels at the line ends. The 2020 annotation points out that the highest-education third jumped above the middle one. I used medians instead of means because counties vary a lot in size and there are outliers. Note that this is correlation only; I fixed the education groups using 2019-23 data and applied them to earlier years.

## 11. Visualization 2 (Question 2)

Upload: `figures/q2_vis2_scatter_2019_2020.png`

## 12. Rationale for Visualization 2

The first chart uses medians of groups, so the alternate shows every county. Two scatterplots (2019 and 2020) share the y axis so they can be compared directly, with bachelor's share on x and unemployment on y. I added a least squares line to each so the change in slope (-0.51 versus -0.23 points per 10 points of bachelor's share) is visible. Dot area is county population and color is metro versus nonmetro, which shows that the big 2020 jumps are mostly large metro counties. Transparency is used because of overplotting around 15-25% bachelor's.

## 13. Comparison for Question 2

The line chart is clear and shows 24 years including two recessions, but it reduces 3,000 counties to three medians and relies on my choice of thirds. The scatterplots show spread, outliers and the metro/nonmetro split, but only cover two years and the overplotting makes it hard to see the density in the lower left. The slope numbers help, but a regression line on skewed data should not be over-interpreted. I think the first is better for telling the story quickly and the second is better for checking whether the story is honest.

## 14. Question / Story for Visualization 3

How much life expectancy did countries lose in the pandemic (2019 to 2021), and had they recovered by 2023? (Life expectancy data, both sexes.)

## 15. Visualization 3

Upload: `figures/q3_vis_covid_life_expectancy.png`

## 16. Rationale for Visualization 3

A dumbbell chart for 18 large countries, with the change from 2019 on the x axis. The red dot is 2021 and the blue dot is 2023, and the gray bar between them is the recovery. Using the change from 2019 puts every country on the same baseline, so different starting life expectancies don't matter. Countries are sorted by the 2021 drop so the worst hit are at the bottom and the plot reads as a ranking. The zero line is emphasized because it is the "recovered" line. I chose countries from different regions and sizes; this is a selection, not a sample, so the title only says what is shown. Using the same colors as the second life expectancy chart would have been confusing, so I picked red/blue to mean time (2021 versus 2023), not a category.

## 17. Question / Story for Visualization 4

Did the 2020 jump in unemployment differ between urban and rural counties?

## 18. Visualization 4

Upload: `figures/q4_vis_unemployment_jump_by_rucc.png`

## 19. Rationale for Visualization 4

The y axis is the 9 USDA Rural-Urban Continuum Codes (ordered from large metro to remote rural, so the order is meaningful) and the x axis is the change in unemployment rate from 2019 to 2020. I show every county as a jittered dot, because the groups differ a lot in size, and put the median and interquartile range on top, with the median value written at the right. Blue is metro and orange is nonmetro to reinforce the split in the code definition. This makes the pattern clear: big metros jump about 3.4 points and remote rural counties about 1.5, though the trend is not perfectly smooth (code 4 is higher than 3). I mention that the spread within each group is large and overlaps, so the group differences are modest compared to the within-group variation. I clipped x at 10, and the caption says 7 counties are above this.

## 20. How I made these

All of the work (choosing the questions, writing the code, designing and revising the charts, and writing these answers) was done by an AI assistant, Claude (Anthropic, Sonnet 5.5), working at the instructor's request as a worked example for the instructor's private review, not as a student submission. A person did not draw or write any of this. I used Python (pandas and matplotlib in the p314 environment) in scripts kept in `work/`. Data processing: I used the World Bank life expectancy file (pivoted wide by sex to compute female minus male, and "Both" for the pandemic chart) and the county census file (read as latin1, Puerto Rico dropped, counties with missing values dropped for the relevant charts, education thirds with `qcut` on the 2019-23 bachelor's share, medians and quartiles per group). No data was added from outside sources. I looked at the rendered images and revised titles, labels and annotations several times after finding overlaps and claims that the data did not support. No other AI tools were used, and no interactive tools like Tableau.
