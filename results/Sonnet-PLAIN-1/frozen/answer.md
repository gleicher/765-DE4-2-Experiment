# Design Exercise 4-2 answers (numbered to match the Canvas survey)

Figures are in `answers/figures/`.

## 1. Critique (the to-critique.png chart, "Income inequality varies across states")

What works: a dumbbell (max and min county median income per state, joined by a line) is a sensible form for "how far apart are the extremes", and the line length gives the spread directly. States are sorted by the ratio, which makes the left-to-right increase easy to follow, and the points are labelled directly rather than needing a legend lookup.

Problems:
- The title ("varies across states") is vague. It does not say what the reader should learn, e.g. "Virginia's richest county has a median income 3.8x its poorest; Wyoming's counties are nearly identical."
- The thing the author cares about, the ratio, is only given as small text labels. The line length encodes the difference in dollars, not the ratio, so the sort order (by ratio) and what the line lengths show (dollar differences) disagree: Alabama's 2.83x line is shorter than Wyoming-to-Virginia style comparisons would suggest, and a high-income state can have a long line with a modest ratio. Plotting the ratio itself (or using a log axis) would match encoding to message.
- The y axis starts at 0K, so the lower third of the plot is empty. A 25K-160K range would use the space.
- Some labels collide with marks (the "3.78x" label overlaps the Virginia dot, and the WY dots overlap), and state names sit below the orange dots and again on the x axis, which is redundant.
- The legend uses the Tableau default title "Measure Names" and "Max./Min."; it should say "County with the highest / lowest median household income". Blue/orange is fine for colour-blind readers, but the grey connector is heavy.
- The selection is arbitrary ("top 5, bottom 5 and 6 additional interested states") and is explained only in the caption; there is no marker for which states are the extremes. The ordering of the x axis is never stated.
- The claim is "income inequality", but the gap between the richest and poorest county median is not inequality in the usual sense (it ignores within-county spread and is sensitive to tiny counties). "Spread of county incomes" would be more accurate.
- The caption is long and grammatically awkward, and the whole image is very tall; it would fit a page better wider.

## 2. Story/Question 1 (Life Expectancy)

When life expectancy collapses in a single year (war, genocide, famine, disaster), how deep is the drop and how long does it take a country to get back to where it was? (Our World in Data, 1950-2023.)

## 3. Visualization 1 (Q1 primary)

`answers/figures/q1a_shocks_small_multiples.png`

## 4. Rationale for visualization 1

I wanted the viewer to see each collapse as a shape, not just a number, so I used small multiples: one panel per event, all on the same vertical scale (5-85 years) so depths are comparable by eye. A dashed line marks the level the year before the drop, and the area between the curve and that line is shaded from the drop until the old level is regained, so "how long to recover" is the width of the shaded area and "how deep" is its height. The shading and the panel subtitle are coloured by recovery time (teal = within 5 years, red = more than 10 years or not yet), which turns the answer into a visible split: ten panels are teal, four are red. I selected the events deliberately rather than plotting everything: one-year falls of 5+ years that total 9+ years at the trough, and I dropped five countries with three or more such drops (Central African Republic, South Sudan, Somalia, Lebanon, Eritrea) because their series are erratic rather than a single event. Panels are ordered by depth, each is titled with country and year, and the caption defines the rule and notes Palestine 2023 cannot be judged because the data ends.

## 5. Visualization 2 (Q1 alternate)

`answers/figures/q1b_depth_vs_recovery.png`

## 6. Rationale for visualization 2 (Q1 alternate)

This version drops the time series and summarises each event as one dot: x = years of life expectancy lost, y = years until the old level returned. This answers the "how deep vs how long" question directly and lets the viewer test the obvious assumption that deeper drops take longer to recover from. Shaded bands mark "fast rebound" (5 years or less) and "slow rebound" (over 10), the colour is the same as in version 1 so the two read as a pair, and events that have not recovered by the end of the data (Palestine 2023) get a different marker (X) on a separate "not yet" row instead of a made-up number. Every dot is labelled directly with country and year (label positions were adjusted by hand in the code to avoid overlaps), and the title states the finding: deeper drops do not mean slower recoveries.

## 7. Comparison of the two Q1 visualizations

Version 1 (small multiples) shows the full story of each event, including the shape of the collapse, whether there were repeated hits (Equatorial Guinea has two dips) and the long-run trend afterwards. Its weakness is that comparing across events means scanning 14 panels, and exact recovery times are only readable from the subtitle text. Version 2 (scatter) makes the cross-event comparison immediate (the two clusters and the lack of a depth-recovery relationship are visible at a glance) and is much more compact, but it throws away the time series, so the viewer cannot see what the drop looked like or what happened afterwards, and the recovery metric (return to the pre-drop level) is a single number that has to be explained in the caption. Version 1 suits readers who want the stories; version 2 suits readers who want the pattern.

## 8. Story/Question 2 (Census)

Has the growth in college education reached all kinds of places equally? How has the gap in bachelor's-degree attainment between big-city counties and the most rural counties changed from 1990 to 2019-23?

## 9. Visualization 1 (Q2 primary)

`answers/figures/q2a_education_lines.png`

## 10. Rationale for the first Q2 visualization

A line chart is the natural form for change over four time points. I grouped the 3,165 counties with complete data into the nine USDA Rural-Urban Continuum categories (2023 codes), took the median county in each, and drew one line per category. Colour carries the ordered category: blues for metropolitan, then green, orange and brown as counties become more rural and remote, so the colour order matches the vertical order at the right edge. Lines are labelled directly at the right end (with leader lines and nudging to avoid overlap) instead of using a legend, and I made the most urban (1) and most remote (9) lines thicker and bold and added annotations for the gap in 1990 (4 points) and in 2019-23 (11 points) so that the story, that the lines fan out, is explicit. The title states the conclusion and the caption gives the exact start and end values, notes that medians are of counties (not weighted by population), and that this is descriptive, not causal.

## 11. Visualization 2 (Q2 alternate)

`answers/figures/q2b_education_distributions.png`

## 12. Rationale for visualization 2 (Q2 alternate)

The line chart shows only medians, which hides the large variation between counties inside each category. This version shows every county as a dot for 1990 (grey) and 2019-23 (blue), side by side for each of the nine categories, with a thick bar for the middle 50% of counties, a tick for the median, and an orange arrow for how the median moved. Grey-to-blue encodes time and keeps the same category order as version 1. A light background band separates metropolitan from nonmetropolitan counties. Points are small and semi-transparent to cope with 3,000+ points (overplotting), and jittered horizontally. The title and caption state the takeaway: all categories shifted up, but large-metro counties also spread out much more (some counties reach about 65%), while remote rural counties mostly sit between 15% and 25%.

## 13. Comparison of the two Q2 visualizations

The line chart is simpler and gets its message (the gap fans out from 4 to 11 points) across in seconds; it also handles the intermediate years (2000, 2008-12). Its weakness is that it shows only one number per group, so it cannot tell whether the median is typical of counties in the group, and the nine lines are close together. The distribution chart shows spread, overlap between categories and the long upper tail, and reveals that the rich-poor gap is partly driven by a minority of highly educated metro counties, which the medians hide. But it only shows two time points, is busier, and the dots are hard to read exactly. They complement each other: the lines give the trend, the dots give the context.

## 14. Story/Question 3 (Visualization 3, Life Expectancy World Bank data)

Women live longer than men almost everywhere, but has the size of that gap grown or shrunk between 1960 and 2023, and where?

## 15. Visualization 3

`answers/figures/q3_gender_gap_1960_vs_2023.png`

## 16. Rationale for visualization 3

Each point is a country: x = the female-minus-male life expectancy gap in 1960, y = the gap in 2023. A dashed y = x line is the key reference: above it the female advantage grew (142 of 212 countries), below it it shrank (70). I tinted the two sides and labelled them in plain words, so that the chart reads without explanation. Colour (a sequential scale) adds a third variable, a country's average 2023 life expectancy, which shows that the countries with the smallest gaps are often low-life-expectancy countries (Togo, Nigeria, Niger, Mali) or Gulf states. A scatter of two time points avoids the clutter of 200 line charts. I labelled only the notable countries: those with negative gaps in 1960 (Pakistan, India, Bangladesh), the largest 2023 gaps (Ukraine, Russia, Belarus, Lithuania, Kazakhstan) and the smallest (Togo, Nigeria, Kuwait), plus some well-known countries for orientation (US, Japan, China, Sweden, South Korea). World Bank regional and income-group aggregates were removed so only countries remain. The title and caption say it directly: the gap has been reshuffled, not uniformly widened or narrowed.

## 17. Story/Question 4 (Visualization 4, Census state data)

After the pandemic, where did Americans move, and did the shifts that began in 2021 last through 2023? (Net domestic migration, 2021-2023, by state.)

## 18. Visualization 4

`answers/figures/q4_migration_tile_map.png`

## 19. Rationale for visualization 4

I used a tile-grid map: each state is a same-size square placed roughly where it is on the map. This avoids the problem that a real map gives huge visual weight to large, sparsely populated states and makes small eastern states invisible, and it needs no outside geometry. Inside every tile there are three small bars for 2021, 2022 and 2023, going up and teal if more people arrived than left, down and orange if the reverse, all on a single shared scale (per 1,000 residents), so both the size and the trend are comparable between states. The tile background and the number in the corner give the three-year average (green tint above +3, orange below -3, grey between) so that the overall pattern is visible at a glance. The title names the finding: the Mountain West surge (ID, MT, UT, NV, AZ) faded, the Southeast (SC, NC, TN, FL, DE) kept gaining, and NY, CA, IL kept losing. A "how to read a tile" key is on the figure. Puerto Rico is omitted because it has no estimate.

## 20. How the visualizations were made

All six figures were made with Python 3.14 (pandas for data handling, numpy, matplotlib for the drawing), in a single script (`work/make_figures.py`); there was no manual editing. AI disclosure: the analysis, code, story choices, figure designs and this text were produced by Claude (Claude Code, model Sonnet 5.5) at the request of the student, who should review and take responsibility for them before submitting.

Data processing: 
- Q1 (Our World in Data file): kept countries (dropping regions), 1950 onward; found one-year drops of 5+ years in life expectancy; kept episodes where the total loss at the trough (within four years) was 9+ years; excluded five countries with three or more such drops; recovery = first year after the trough at or above the level of the year before the drop.
- Q2 (full census file, which is comma-separated and latin-1 despite the readme): kept counties with a 2023 Rural-Urban Continuum Code and all four bachelor's-degree percentages (3,165 counties); took medians and quartiles by code.
- Q3 (World Bank file): pivoted Sex to columns, computed Female minus Male for 1960 and 2023, removed non-country aggregates by matching codes to the Our World in Data country list.
- Q4 (state-level census file): used Domestic Migration Rate 2021-2023 for the 50 states and DC and laid out a hand-made tile-grid.
No outside data was added.
