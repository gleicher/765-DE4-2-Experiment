# Design Exercise 4-2 answers (numbered to match Canvas)

**1. Critique (not in the CLO)**

I looked at the "Income inequality varies across states" dumbbell chart. What works: the dumbbell is a good choice for showing a min/max range per state, the orange/blue pair is colorblind safe, and the caption tells you how to read it and what the extremes are. The "1.01x ... 3.78x" ratios on top are a nice touch since they put a number on the length of each line.

What doesn't work: (a) the states are sorted by the ratio but the axis doesn't say so, and the ratio is the actual message while the y axis shows dollars, so you have to compare line lengths by eye on a scale where the same dollar gap means different ratios. Plotting the ratio itself (or sorting and labeling it) would be more direct. (b) The y axis starts at 0K even though no county is below about 30K, so the top third of the chart is dead space. (c) Only 16 of 50 states are shown, picked as "top 5, bottom 5 and 6 interesting ones" and the reader can't tell which is which, so the selection looks arbitrary. (d) Several labels collide with marks (3.78x runs into its dot, WY's two dots overlap). (e) The title is vague, "Measure Names" in the legend is leftover Tableau text, and the spread between the richest and poorest county is not really "inequality" (it ignores how many people live in each county), so the claim is stronger than the data.

**2. Story/Question 1 (life expectancy)**

Have countries that started with the lowest life expectancy in 1960 caught up with the richer ones, or is the gap between rich and poor countries still there? (World Bank data, both sexes.)

**3. Visualization 1 for Question 1**

Upload: `figures/q1_viz1_catchup_scatter.png`

**4. Rationale for Visualization 1**

I used a scatterplot of 1960 life expectancy against years gained by 2023, one dot per country. Putting the gain (not the 2023 value) on the y axis makes the catch-up pattern obvious: the cloud slopes down, so the countries that began lowest gained the most. I removed the World Bank regional/income aggregates so every dot is an actual country. Everything is gray except a few countries I picked on purpose: South Korea, China and the Maldives (blue) as big catch-up cases, and Lesotho, Eswatini, Central African Republic, Russia and Ukraine (orange) as ones that sit well below the trend because of HIV/AIDS or the post-Soviet mortality crisis. The dashed trend line gives the reader a baseline for judging who is above and below. Color is used only to separate "highlighted" from "everyone else", and the caption says why each one was picked.

**5. Visualization 2 for Question 1**

Upload: `figures/q1_viz2_income_gap_lines.png`

**6. Rationale for Visualization 2**

This one answers the same question at the group level instead of the country level. It is a line chart of the four World Bank income groups over 1960 to 2023, with the area between the high-income and low-income lines shaded. I put the gap itself into the picture (vertical bars labeled 27, 23 and 16 years) so the reader doesn't have to subtract. Lines are directly labeled at the right with their 2023 values, so there is no legend to look up. I used a colorblind-safe palette with distinct hues, and annotated the two things that would otherwise look like errors: the 1960 dip in the upper-middle group (China's famine) and the 2020 COVID dip.

**7. Comparison of the two Question 1 visualizations**

The scatterplot shows individual countries, so you can see the spread and the exceptions (Lesotho, Russia), and it makes the catch-up pattern very clear. But it only compares two years, so it hides what happened in between, and it needs a bit of work to read ("gain vs. start" is a derived quantity). The line chart shows the whole timeline, has an obvious headline number (the gap shrank from 27 to 16 years) and is easier for a general audience, and it also shows that the narrowing was slow between the 1970s and 2000. Its downside is that it relies on group averages (aggregates dominated by big countries) and hides individual countries entirely, and the "income group" labels are today's classification applied to 1960. I think the line chart is better for a newspaper and the scatter for a more analytical audience.

**8. Story/Question 2 (census)**

Did the rise in college degrees since 1990 happen equally across urban and rural counties, or did big-city counties pull ahead?

**9. Visualization 1 for Question 2**

Upload: `figures/q2_viz1_education_lines.png`

**10. Rationale for Visualization 1 (Q2)**

I collapsed the nine USDA rural-urban codes into four groups (large metro, other metro, small-town nonmetro, rural) to keep the chart readable, and plotted the median county's bachelor's-degree share at the four time points the data has. Lines are directly labeled with start and end values, and the main takeaway (the large metro vs. rural gap going from 5 to 13 points) is written on the chart. Colors go from blue for the most urban to orange for the most rural, in an order that matches the vertical order of the lines. The x axis has the four census periods evenly spaced as labeled categories, which is slightly misleading about time spacing, so I mention the approximate timing in the caption. I used medians because county percentages are skewed.

**11. Visualization 2 for Question 2**

Upload: `figures/q2_viz2_education_scatter.png`

**12. Rationale for Visualization 2 (Q2)**

This shows the same story at the county level. Each circle is a county (3,165 of them), with 1990 attainment on x and 2019-23 on y, and circle area is 2020 population so large counties stand out. The dashed y = x line makes "growth" a distance above the line, and almost every county is above it. The group medians are drawn as black-outlined diamonds so the pattern from the line chart is still visible. Transparency helps with the heavy overplotting in the lower left. The cloud has a slope above 1, meaning counties that started high gained more points, which is the same divergence story seen as a spread rather than a gap between averages.

**13. Comparison of the two Question 2 visualizations**

The line chart is simple and the message is read in a few seconds, but it hides the variation inside each group (there is a lot of overlap between groups, which the scatter shows clearly) and only four lines are shown. The scatter shows all the counties, the outliers, and population size, and supports the claim that nearly every county improved. But it is busier, the overplotting in the lower-left makes the groups hard to separate, and the reader has to understand the diagonal reference line. If I could only give one to a general reader I'd use the line chart; for someone who wants to check the claim I'd use the scatter.

**14. Question/story for Visualization 3**

Was the 2020 pandemic a bigger unemployment shock than the Great Recession, and did that differ from state to state?

**15. Visualization 3**

Upload: `figures/q3_unemployment_tilemap.png`

**16. Rationale for Visualization 3**

Since the question is about 51 places over 24 years, I used a tile-grid map with one small line chart per state. This keeps rough geography (so regional patterns, like the Northeast, jump out) without Alaska and Hawaii shrinking or small eastern states vanishing like on a real choropleth. All tiles share the same 0 to 16% scale so heights can be compared. In each tile I marked only two points, the 2008-12 peak (blue square) and 2020 (orange dot), and colored the whole tile by which one is higher, so the answer to the question is a color you can scan. The headline says how many states there are (9). A mini key tile (Nevada) explains how to read it. The caveat that annual averages understate the spring 2020 spike is in the caption.

**17. Question/story for Visualization 4**

Where did people move after 2020: did large metro counties lose residents to the rest of the country?

**18. Visualization 4**

Upload: `figures/q4_domestic_migration.png`

**19. Rationale for Visualization 4**

I used horizontal bars for each of the nine USDA rural-urban categories, so the labels can be written out in full and the category order (big metro to remote rural) reads top to bottom. The left panel shows net domestic migration per 1,000 residents over 2021 to 2023, and the right panel shows the raw number of people, because the two tell different stories: rural counties have the highest rates, but the absolute loss from the largest metros (about 1.9 million) is about the same size as what all the other county types gained combined (roughly 1.9 million). The two panels share the same y axis. Bars are colored with the same four groups as Question 2 (so the colors have a consistent meaning across my figures), and values are written on the bars. The zero line is emphasized so the sign is easy to see.

**20. How I made the visualizations**

All six figures were made in Python (pandas for the data processing and matplotlib for the charts), run from a single script. Processing: for the county analyses I dropped the US and state rows from the full census file; I grouped the 2023 rural-urban continuum codes into four groups for the Q2 figures, took medians of county percentages, and for Q4 summed domestic migration for 2021 to 2023 by code and divided by 2020 population. For life expectancy I used the World Bank file (Both sexes), removed regional and income aggregates for the country-level scatter, and kept the income-group aggregates for the line chart. For Q3 I used the state-level census file and compared each state's 2008-12 maximum unemployment rate to its 2020 rate. I used an AI tool (Claude Code, Anthropic) to help plan the stories, write the plotting code, and draft the text.
