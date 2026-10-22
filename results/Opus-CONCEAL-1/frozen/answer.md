# DE 4-2 answers (numbered to match the Canvas survey)

## 1. Critique

(I was not part of the CLO, so this is the critique of the provided example: "Income inequality varies across states.")

This is a dumbbell chart. For each of 16 states, it shows the highest and lowest county median household income (2021), with a gray bar between them and the max/min ratio printed above. The basic form fits the story well. Two dots and a line show a range clearly, and sorting the states by ratio makes the main message (WY low, VA high) obvious immediately. The caption explains the encoding, and the ratio labels give exact numbers, which is useful.

My biggest problem is with what's being measured. The max/min ratio of county medians isn't really "income inequality." It's how much the richest county differs from the poorest county, and it's driven by two extreme counties. It also depends heavily on how many counties a state has. Delaware has 3 counties and Texas has 254, so Texas is almost guaranteed a wider range. The Wyoming value also looks off to me. A 1.01x ratio across 23 counties is hard to believe, and in this year's version of the data (2022 incomes) I get about 2.4x for Wyoming. I'd want to check that before building the story around it.

Design details:
- The bars are sorted by ratio, but the y-axis is linear dollars. The ratio is the quantity the reader is supposed to compare, so a log scale (or plotting the ratio itself) would make the bar lengths match the numbers. Right now CA (2.77x) looks longer than AL (2.83x).
- The y-axis starts at 0, which leaves the bottom third empty. Zero isn't meaningful for a range chart like this.
- Tableau defaults are left in: the "State" header at the top, "Measure Names" as the legend title, and "Max."/"Min." as labels. "Highest county" / "Lowest county" would read better.
- The state selection ("top 5, bottom 5, and 6 additional interested states") isn't shown in the chart, so the reader can't tell which states are extremes and which were picked by hand. Either show all 50, or visually separate the groups.
- Some labels collide (VA's 3.78x runs into its dot), and the title is plain, while it could state the finding.

What I'd try: show every county as a small dot on a log-income axis for each state (a strip plot), sorted by the spread. Then the reader sees the whole distribution and not only the two extremes, and states with few counties are obvious.

## 2. Story/Question 1 (Life Expectancy)

Women outlive men almost everywhere, but in Russia and its European neighbors (Ukraine, Belarus, the Baltics) the gap is about twice the world norm. How has that gap changed since 1960, and is it driven by women living longer or men dying younger?

## 3. Visualization 1 (Question 1)

`figures/q1a_gender_gap_lines.png`

## 4. Rationale for Visualization 1

This is a line chart of one derived variable, female minus male life expectancy, from 1960 to 2023. The story is a comparison against "normal," so instead of drawing 200 gray spaghetti lines I summarized the rest of the world as a median line plus a 10th-90th percentile band. That makes the comparison simple: the red lines sit above the gray band for basically the entire period. Russia is the thickest, highest-contrast line because it's the main case. The other five European ex-Soviet countries are thin light red lines, so you can see that Russia isn't a one-off. The Caucasus/Central Asian republics act differently (their gap is closer to normal), and drawing all 9 of them made the chart a mess, so I collapsed them into one dashed median line. I still didn't want to drop them silently.

I added a few annotations for events that line up with the big swings: the 1985-87 anti-alcohol campaign (the gap shrinks), 1991 (vertical reference line), the 1994 peak with the actual male and female values, and Ukraine's jump in 2023. The rules say we can use background knowledge as long as we don't add data, and the caption says so. Lines are labeled directly at the right edge, so you don't have to keep going back to the legend. The title states the finding.

## 5. Visualization 2 (Question 1 alternate)

`figures/q1b_gender_gap_small_multiples.png`

## 6. Rationale for Visualization 2

The first chart shows that the gap is big but hides why. A gap can grow because women gain or because men lose. So this version goes back to the two underlying variables: small multiples with women's and men's life expectancy as separate lines and the gap shaded between them. The top row is four former Soviet republics. The bottom row has comparison countries, including Poland, which was in the Soviet bloc but not the USSR, so it's a kind of control. All panels share the same y-axis, so you can compare the shaded area across panels just by looking. The numbers in 1994 and 2019 give the gap size so you don't have to estimate it.

The pattern jumps out: in Russia and Latvia the male line drops sharply in the early 1990s while the female line barely changes, so the shaded area balloons. In the bottom row both lines rise together, with a fairly constant band. Colors are orange for women and blue for men, direct-labeled in the first panel. Panel titles are red for ex-USSR and black for comparison countries, so the two groups are separated by more than just which row they're in.

## 7. Compare the two visualizations for Question 1

The line chart is better for the "how big and how unusual" part. It has all 15 former Soviet republics against the entire rest of the world on one axis, and the events can be annotated on a single timeline. Its weakness is that the gap is a derived number, so you can't see what's behind it. It also takes some reading to understand the band and the dashed median.

The small multiples are better for the "why" part. You can see that it's men's life expectancy collapsing, not women's improving. They're also more concrete, since people understand "Russian men lived to 58" better than "the gap was 14 years." The downside is that there are only eight countries, the rest-of-world context is gone, and comparing across panels is less precise than comparing lines on one axis. I think the line chart works better as the main figure and the small multiples as the follow-up.

## 8. Story/Question 2 (Census)

Where does population growth come from in different kinds of places? In 2021-2023, did big metros, smaller metros, and rural counties grow (or shrink) for different reasons: births vs. deaths, people moving in from elsewhere in the US, and immigration?

## 9. Visualization 1 (Question 2)

`figures/q2a_components_by_rucc.png`

## 10. Rationale for Visualization 2-1

Population change breaks down into three components (natural change, domestic migration, international migration) that add up to the net. Some are positive and some negative, so I used a diverging stacked bar: positive pieces stack to the right of zero, negative pieces to the left, and a black diamond marks the net. I grouped counties by the 2023 rural-urban continuum code (9 categories, most urban to most rural), pooled all counties in each group, and divided by the group's population. The bars are per 1,000 residents per year, so a group of 589 tiny counties can be compared to a group containing LA. On the right I put the net value, the number of counties, and the group's share of US population. Big metros are 57% of the population, so their pattern matters more for the country even though the bars look the same size.

Rows are ordered by the code and split into metro and nonmetro with a rule. That makes the trend visible as you read down: purple (natural change) moves from positive to strongly negative, while orange (domestic migration) is negative only for the largest metros. I used three distinct hues, since the components are categories rather than ordered values, and checked that they're distinguishable. Two short notes point out the two main patterns, and the title states the takeaway.

## 11. Visualization 2 (Question 2 alternate)

`figures/q2b_county_scatter.png`

## 12. Rationale for Visualization 2-2

The first chart pools counties, which can hide how typical each pattern is. This one shows every county: a scatter of natural change rate (x) vs. domestic migration rate (y), split into metro and nonmetro panels with the same axes. The two zero lines split the plot into four quadrants, each with a clear meaning ("more deaths, but gaining movers," etc.). I labeled each quadrant with the percent of counties and the percent of people in it. That's the core of the story: 84% of nonmetro counties have more deaths than births, and most of them sit in the upper-left quadrant (gaining movers). Meanwhile 47% of metro residents live in the lower-right quadrant (more births, but losing movers), which is where the big core counties are. I labeled a few of those (LA, Cook, Brooklyn, Harris, Maricopa) so people have something familiar to anchor on.

Dot area is proportional to population, with partial transparency for overplotting. The axis limits are cropped to keep the main cloud readable. About 1% of counties are pinned to the edge, and the caption says so. The panels use different colors, so they can't be mistaken for each other.

## 13. Compare the two visualizations for Question 2

The stacked bar is simpler and more complete. It includes international migration, shows how the components add up to the net, and covers all nine categories in order. But it's an aggregate. One huge county can dominate a group, and you can't tell whether a bar describes most counties or a few big ones.

The scatter fixes that by showing all 3,106 counties, and the quadrant percentages say how common each pattern is. It also exposes the variation (some rural counties are losing on both counts) and lets you spot specific places. The costs: it drops international migration (only two axes), it collapses nine categories into metro/nonmetro, and it takes longer to read. The bars answer "what's the typical recipe for growth in each kind of place"; the scatter answers "how many counties actually follow it."

## 14. Story/Question 3

How long does it take a country to go from a life expectancy of 50 to 70? Did countries that started later make the climb faster than the early pioneers, and which countries still haven't made it? (Our World in Data long-run life expectancy.)

## 15. Visualization 3

`figures/q3_fifty_to_seventy.png`

## 16. Rationale for Visualization 3

I reduced each country's life expectancy curve to two events: the year it first reached 50 and the year it first reached 70. The scatter plots the start year (x) against how many years the climb took (y), so a downward trend means "later starters were faster," and that's visible right away: Norway took 93 years, many 1950s starters took 25-50, Japan took 17.

The hard part was countries that haven't reached 70 yet. Dropping them would make the trend look better than it is, so I kept them as hollow red triangles at "years so far." Those are lower bounds, and they fall exactly on the dashed "years elapsed up to 2023" line. That line works as a boundary: no country can be above it. So the triangles show which countries are still climbing. They're mostly in sub-Saharan Africa, and some crossed 50 back in the 1950s and 60s. That's the "but not all of them" part of the title.

The historical data is irregular, so I only counted a crossing when there's an observation within 5 years before it. Otherwise a gap from 1900 to 1950 would give a fake crossing date. Countries already above 50 when their record starts are also excluded. The caption explains both rules, plus the fact that "first reached" ignores later dips (Zimbabwe, South Africa). I labeled a selection of well-known countries and both extremes rather than everything.

## 17. Story/Question 4

Were the Great Recession and the 2020 pandemic recession hard on the same states? How did each state's jump in unemployment compare between the two, and how long did each spike last? (State-level census data.)

## 18. Visualization 4

`figures/q4_unemployment_two_recessions.png`

## 19. Rationale for Visualization 4

This is a compound design with two aligned views. On the left, a heatmap of unemployment rate for each state and year (2000-2023). A heatmap fits 51 rows x 24 years on one page, and it shows the time shape well: the Great Recession is a wide dark band from 2009 to roughly 2013, while the pandemic is a single dark column in 2020 that's gone a year or two later. On the right, a dumbbell chart for each state compares the size of the two shocks: the Great Recession rise (2009-11 peak minus 2007) and the pandemic rise (2020 minus 2019).

The ordering carries most of the message. States are sorted by how much bigger their pandemic jump was than their Great Recession jump, so states hit harder in 2020 (Hawaii, Massachusetts, New York) are at the top, and those hit harder in 2009-11 (the Southeast, Arizona, Idaho, Utah) are at the bottom. Nevada and Michigan, which got hammered both times, are in the middle. The US row sits separately at the top as a reference. The colormap is one sequential scale (yellow to dark red) with binned steps so the colors are easier to read. The dumbbell colors (gray = Great Recession, red = pandemic) are labeled at the top and on the panel itself. The caption points out that these are annual averages, so the April 2020 peak is smoothed.

## 20. How I made these

**Disclosure: these visualizations and this write-up were made by an AI (Claude Code, Anthropic's coding agent), not by me.** It chose the stories, did the data processing, wrote the plotting code, and drafted all of the text above, including the rationales and the critique. This needs to be disclosed under the course GenAI policy.

Tools: Python (pandas, numpy, matplotlib) in a conda environment. All the code is in one script (`work/make_figures.py`). There's no manual editing of the images.

Data processing:
- Life expectancy (World Bank): pivoted to one row per country-year with male/female columns, computed female minus male, and removed World Bank aggregate codes (regions, income groups, "World," etc.). "Rest of world" = all non-ex-USSR countries, summarized by year as a median and 10th/90th percentiles.
- Life expectancy (OWID): removed aggregates (OWID_ codes and rows without a code). For each country, found the first year at or above 50 and at or above 70, and only kept a crossing if the previous observation was 5 years or fewer earlier.
- County data: the file is actually comma-separated and needed latin-1 encoding. Dropped state/US rows, Puerto Rico, and old counties with no 2021-23 data (e.g., the 8 old Connecticut counties, replaced by planning regions). Averaged 2021-2023 counts of natural change, domestic migration, and international migration, divided by mean population, times 1,000. Grouped by the 2023 rural-urban continuum code (metro = codes 1-3).
- State unemployment: used the aggregate (state-level) file, dropped Puerto Rico (no 2020 value), and computed the two recession rises.

Event annotations in the life expectancy charts (anti-alcohol campaign, USSR breakup, war in Ukraine) come from general knowledge, not added data.
