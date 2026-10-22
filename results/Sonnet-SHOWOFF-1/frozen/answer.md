# Design Exercise 4-2 answers

Numbering follows the Canvas survey questions. Figure files are in `answers/figures/`.

## Canvas Q1: Critique (non-CLO version)

I critiqued the provided "Income inequality varies across states" chart (a dumbbell chart of the highest and lowest county median household income in 16 states).

**What works.** The dumbbell is a sound choice for showing a range per state: position on a common scale, with a line whose length is the spread. The ratio labels (1.01x to 3.78x) turn the spread into one comparable number, and the states are sorted by that ratio, so the main pattern (spread grows left to right) is easy to see. Blue/orange is colour-blind safe and the caption does explain what the dots and lines mean.

**What does not.**
1. *The title and the data do not match.* The title says "inequality", but the max/min ratio of county medians is not inequality. It says nothing about how incomes are distributed among people, and it depends heavily on how many counties a state has and on a single extreme county. Wyoming's "lowest inequality" reflects only a handful of similar counties. A title like "The richest county's median income is 1x to 3.8x the poorest county's, depending on the state" would be accurate.
2. *The selection of states looks arbitrary.* The caption says "top 5, bottom 5 and 6 additional interested states", but the viewer cannot tell which are which, or why those six. All 50 states would fit in this layout, or the selection should be marked.
3. *Label collisions and default leftovers.* The "3.78x" label collides with the Virginia marker, and the Wyoming dots overlap. The legend title is the Tableau default "Measure Names" with "Max."/"Min." and the axis is labelled "Median Household Income 2021" without saying county medians. The State header is redundant. The long gray caption is far from the data and is hard to read.
4. *Space.* The axis starts at 0K, so the lower 25% of the chart is empty (nothing is below ~$30K). Dot position does not need a zero baseline, so this wastes space. A tall portrait chart with 16 columns is also an unusual use of space.
5. *Vertical dumbbells make the ratio hard to read.* The ratio is a multiplicative quantity, but the lengths are shown as differences on a linear axis, so an equal ratio at a high income looks longer than at a low income. A log axis, or plotting the ratio directly, would be a better match.

**Suggested improvement.** Plot all states as horizontal dumbbells on a log income axis sorted by ratio, mark state median income, state the number of counties, and retitle the chart to describe what is actually measured.

*(If you were in the CLO, replace this with the name of the person who critiqued you and a one-sentence rating of how helpful it was. I have no information about that, so I did not make one up.)*

---

## Canvas Q2: Story/Question 1 (Life Expectancy)

Women outlive men in almost every country, but has the size of that gap followed one common trajectory since 1960? No: it has taken at least four paths: it exploded and then shrank in post-Soviet states, rose and then fell in wealthy countries, flipped from negative to positive in South Asia, and nearly vanished in the Gulf and West Africa.

## Canvas Q3: Visualization 1 for Question 1

Upload: `answers/figures/q1_fig1_gap_small_multiples.png`

## Canvas Q4: Rationale for Visualization 1

The measure is the female-minus-male life expectancy gap (from the World Bank Male and Female series), which makes the question about one quantity per country-year instead of two curves. Showing *the gap* lets a viewer read directly where women live longer (above the black zero line) and where they do not.

Design choices: (1) Small multiples, one panel per pattern, with shared axes so the four panels are directly comparable; (2) in every panel the whole world is drawn as pale gray lines (the ~200 other countries) plus a dashed median line, so the highlighted countries are always seen against the global context instead of floating alone; (3) a few countries per group in a bright colour with direct labels instead of a legend (labels are nudged apart so they do not overlap); (4) small annotations on the single most striking points (Russia's 14.2-year peak in 1994 and Pakistan's 1960 negative gap); (5) a heavy zero line labelled "men = women"; (6) a colour-blind-safe palette (Okabe-Ito based), and the same colours are reused in my second visualization so the two can be read together. I removed aggregates (regions, income groups) and the few countries with very noisy gap series from the gray background. The groupings are my own descriptive labels, not an official classification, and the caption says so. The title states the finding rather than naming the variables.

## Canvas Q5: Visualization 2 for Question 1 (alternate)

Upload: `answers/figures/q1_fig2_gap_dumbbell.png`

## Canvas Q6: Rationale for Visualization 2

The alternate drops time as an axis and compares only two moments, 1960 and 2023, using a dumbbell chart: an open circle for 1960, a filled circle for 2023, and a printed number for the change. The four groups from the first chart are kept (same colours), stacked as labelled blocks (25 countries in all), and sorted within each block by their 2023 gap. This makes it a "ranking plus change" design for readers who want exact values and country names. Using position along one common scale makes both the size and direction of change easy to read: the South Asian bars cross the zero line, the Gulf/West African bars all point left, and the post-Soviet bars point right and start high. Direction labels, the zero line and a small legend (open = 1960, filled = 2023) keep the chart self-explanatory.

## Canvas Q7: Compare the two visualizations for Question 1

*Small multiples (Viz 1).* Pros: shows the *shape* of the story, including timing (the 1990s post-Soviet surge, the 1970s-80s peak in wealthy countries, the 2020 Ukraine jump), and shows each country against all other countries. Cons: lines in a panel overlap (labels must be crowded at the right edge), exact values are hard to read, the gray background adds visual noise, and it only shows eight to ten countries per panel.

*Dumbbell (Viz 2).* Pros: very easy to read exact values, to compare countries and to see direction and size of change; countries can be named in a clean list, so it is better for looking something up. Cons: hides everything between 1960 and 2023 (e.g., that Russia's gap peaked in 1994 and has fallen since; the endpoints alone suggest a steady rise), and the choice of two end years can mislead for noisy series (Pakistan's 1960 value is an outlier). It also gives no global context.

I would use Viz 1 for a general reader and Viz 2 as a companion for people who want the numbers.

---

## Canvas Q8: Story/Question 2 (Census)

Is higher education spreading evenly across America, or has a gap opened between metro and rural counties since 1970, and how big is it for the typical county compared with the typical resident?

## Canvas Q9: Visualization 1 for Question 2

Upload: `answers/figures/q2_fig1_education_gap_lines.png`

## Canvas Q10: Rationale for Visualization 1

A line chart with six time points (1970 to 2019-23) and four lines, one for each of four county types (the USDA 2023 Rural-Urban Continuum Code collapsed from 9 categories to 4: metro, small cities, small towns, most rural). Because the main message is *change over time and divergence*, lines are the standard, effective choice. Each line is a *pooled* share (total degree holders divided by total adults, which I back-computed from the count and percentage columns), so large counties count in proportion to their adults rather than every county counting once. Choices to emphasize the story: (1) direct labels instead of a legend, with start and end values; (2) two double-headed arrows with "Gap: 6 pts" (1970) and "Gap: 18 pts" (2019-23) to make "tripled" a visible fact; (3) a dashed guide showing that rural counties today (19%) have only reached the level that metro counties had around 1984; (4) ordered, distinct colours for an ordered variable, with the extremes (metro and rural) the most contrasting; (5) the y axis starts at 0% so slopes are honest. The caption explains the pooling, the grouping, the slight change in definition between 1970/80 ("four years of college") and later years ("bachelor's degree"), and which counties were excluded.

## Canvas Q11: Visualization 2 for Question 2 (alternate)

Upload: `answers/figures/q2_fig2_education_county_distributions.png`

## Canvas Q12: Rationale for Visualization 2

The first chart shows pooled averages, which hide the variation among counties. This chart shows every county (one dot, about 3,100) for the same four county types, comparing 1970 (faint) with 2019-23 (dark) side by side, with a bar for the middle 50% and a white tick plus label for the median. This is a different encoding (distribution strip plot, a data-rich "show all points" view) and a different question: how different is the *typical county*, and how much overlap is there? Dots are jittered and semi-transparent to handle overplotting. Two callouts (the highest-education rural county, San Miguel County, CO at 65%, and the lowest-education metro county, Butler County, KY at 10%) show that the categories overlap heavily. The title states the finding: the median rural county trails the median metro county by 8 points, not 18, because the pooled gap in the first chart is driven by large, highly educated metro counties holding most of the adults.

## Canvas Q13: Compare the two visualizations for Question 2

The line chart is simpler and faster to read; it gives one clear message (the gap has tripled, rural is decades behind) and is best for a general audience. But it hides how much counties vary and weights places by population, so it can overstate the divide for the *typical county*. The distribution chart shows spread, overlap and outliers, and corrects that impression (the median gap is 8 points), but it only shows two years, has many dots that are visually busy, and is harder for non-technical readers to decode (what do the bars mean?). The two are complementary: the first answers "what is the experience of the typical resident?", the second answers "how different is the typical county, and is there overlap?".

---

## Canvas Q14: Question/story for Visualization 3

COVID-19 cut life expectancy in most countries between 2019 and 2021. Which countries lost the most, how much did each regain by 2023, and which are still below their 2019 level? (World Bank life expectancy data.)

## Canvas Q15: Visualization 3

Upload: `answers/figures/q3_fig1_covid_loss_recovery.png`

## Canvas Q16: Rationale for Visualization 3

A scatter plot where each dot is a country, x = change 2019 to 2021 and y = change 2021 to 2023. The key design decision is the diagonal: a country on the line y = -x regained exactly what it lost, so the line separates countries now above their 2019 level (blue wash, 185 countries) from those still below it (red wash, 31). This turns a fuzzy question ("did they recover?") into a visual judgment about position relative to a line. A third variable, 2019 life expectancy, is encoded by colour using a perceptually ordered sequential palette (viridis), which shows the biggest losers (Bolivia, Paraguay, Mexico, Guyana, Peru) had mid-range life expectancy while the lowest-life-expectancy countries changed little. I labelled only a small, deliberately chosen set of countries (the biggest losses, a few large countries, and the conflict-related outliers West Bank and Gaza and Libya, which are below the line for reasons unrelated to the pandemic) to avoid clutter. I removed aggregates and the Central African Republic, whose reported +26-year change looks like a data artifact, and said so in the caption. The title states the result. The country names allow the title's claim about Latin America to be checked, but I did not add region data.

## Canvas Q17: Question/story for Visualization 4

Two recessions, two geographies: in which states was unemployment higher in the Great Recession (worst year 2008-12) than in the pandemic year 2020, and in which was it the other way round? (Census state-level data.)

## Canvas Q18: Visualization 4

Upload: `answers/figures/q4_fig1_unemployment_tile_map.png`

## Canvas Q19: Rationale for Visualization 4

A tile-grid map (a schematic with one equal-size tile per state, which keeps small eastern states visible and avoids the large-area bias of a choropleth) in which each tile contains a small line chart of the state's annual unemployment rate from 2000 to 2023. All tiles share the same y scale (0 to 14.5%) so they can be compared directly, and a dotted line in each tile shows the national rate as a reference. The two crisis moments are marked with a blue dot (Great Recession peak) and an orange dot (2020), and the tile background is tinted by whichever was higher (42 states blue, 9 states orange), so the answer to the question appears as a map pattern: the Sun Belt and Rust Belt states are blue, while Hawaii, New York, Massachusetts, Louisiana, Pennsylvania, Alaska, New Mexico, New Hampshire and North Dakota are orange. The values are printed on each tile for exact reading. A larger annotated example (Nevada) serves as the legend for how to read a tile. This is a compound design (map layout plus small multiples of lines). The caption warns that annual averages smooth the 2020 spike and so understate COVID's effect, and notes that Puerto Rico is omitted because it has no 2020 value.

## Canvas Q20: How I made these visualizations

All charts were made in Python 3.14 using pandas (data processing) and matplotlib (drawing), with no manual image editing. Data processing: (1) World Bank life expectancy: pivoted the tall file to one row per country-year with Male, Female and Both; computed the gap as Female minus Male; removed regional and income-group aggregates by pattern-matching names; removed the Central African Republic from the COVID chart. (2) Census: read the county file (latin-1 encoding) and the tab-separated state file; grouped the 9-level 2023 Rural-Urban Continuum Code into four levels; for education, back-computed each county's number of adults as degree holders divided by the percent with a degree, then pooled the counts within county types; compared 1970 "four years of college or more" with later "bachelor's degree or higher" (noted in the caption). (3) State unemployment: compared each state's maximum annual rate in 2008-12 with its 2020 rate. No external data were added. The scripts are in `work/` with a README.

**AI disclosure (please edit to match what you actually did):** I used Claude Code (an Anthropic AI model, Sonnet) as an AI assistant to choose the stories, write the plotting code, produce the figures and draft this text. If you are submitting this under your own name, per the course's generative-AI policy you should review it, edit it into your own words, and say clearly that an AI tool generated the code and draft wording.
