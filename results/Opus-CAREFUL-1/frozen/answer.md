# Design Exercise 4-2: Answers (numbered to match the Canvas survey)

Figures are in `answers/figures/`:

| Canvas Q | File |
|---|---|
| 3 | `figures/q1a_gap_lines.png` |
| 5 | `figures/q1b_gap_trajectories.png` |
| 9 | `figures/q2a_unemployment_lines.png` |
| 11 | `figures/q2b_unemployment_shocks.png` |
| 15 | `figures/q3_population_components.png` |
| 18 | `figures/q4_covid_setback.png` |

---

## 1. Critique (not part of the CLO)

The design is a dumbbell (range) chart. For 16 states it shows the highest and lowest county median household income in 2021 (blue and orange dots), joined by a gray line, with the max/min ratio printed above each pair. The states are sorted by that ratio. The question is clear enough: which states have the biggest gap between their richest and poorest counties? A range chart suits that question, and sorting by the ratio makes the left-to-right increase easy to read. The caption is good. It explains the encoding and states the result (WY lowest at 1.01x, VA highest at 3.78x).

The main problem is that the chart encodes one measure and sorts and labels by another. The length of each line shows the *dollar difference*, but the order and the printed numbers are the *ratio*. So the eye sees CA (a long line, 2.77x) and AL (a shorter line, 2.83x) ranked in an order the lines seem to contradict, and FL and WI look about the same even though their ratios are 2.08x and 1.68x. If the ratio is the story, use a log y-axis (equal ratios then get equal lengths) or plot the ratio directly. Second, max/min is a fragile summary that depends on how many counties a state has. Delaware has 3 counties and Texas has 254, so Texas has many more chances at an extreme. One outlier county decides the whole value, and the chart hides how many counties each state has and where the rest fall. Plotting every county as a faint dot behind the range, or noting the county count under each state, would fix this. Third, the WY value of 1.01x deserves a check. In the 2022 column of our data, Wyoming's counties range from about $54K to $128K (2.4x), so a near-zero range points to a filtering or data problem, and it is the point the caption leads with. Fourth, "income inequality" overclaims. These are medians of whole counties, so the chart shows geographic variation *between* counties, not inequality among households.

Smaller details: the legend title "Measure Names" and the "State" header are Tableau defaults and should be "County with highest / lowest median income". Direct labels on the first pair would remove the need for a legend at all. The y-axis starts at 0, which wastes a third of the plot. Dot plots don't need a zero baseline. The state abbreviation appears twice (under the orange dot and on the axis). The choice of "6 additional interested states" is never explained, so the reader can't tell whether the middle of the chart is representative. The title "Income inequality varies across states" names the topic but not the finding. Something like "Virginia's richest county earns nearly 4x its poorest; Wyoming's barely differs" would tell the story. Overall: a reasonable standard design with a clear caption, held back by the length/ratio mismatch and a summary statistic that hides most of the data.

---

## 2. Story/Question 1 (Life Expectancy)

Women almost everywhere outlive men, but has that advantage changed over time, and in the same direction everywhere? Since 1960 the female-male gap has *converged*. It has shrunk in the regions where it was largest (North America, Europe & Central Asia), grown in the regions where it was smallest or negative (South Asia, the Middle East & North Africa), and the regions now sit much closer together (a spread of about 3 years instead of almost 8).

## 3. Visualization 1 for Question 1

`figures/q1a_gap_lines.png`

## 4. Rationale for Visualization 1

- **Plot the gap itself, not two lines per region.** If female and male life expectancy were drawn as two lines per region, the 4-8 year gap would be a thin sliver on a 40-85 year scale and couldn't be compared across regions. Plotting the difference (female minus male) turns the quantity I care about into position on a common axis, which is the most accurate channel.
- **World Bank regions instead of countries.** With 200+ countries a line chart turns into spaghetti. The seven geographic aggregates are already in the data, so I didn't need to add a country-to-region mapping. I left out the income-group and other overlapping aggregates.
- **Emphasis by color, context in gray.** Only the four regions that carry the story get color: the two "shrinking" regions in warm colors (orange and yellow) and the two "growing" ones in cool colors (blue and green). The other three are thin gray lines, and the world is a thicker black reference. The point is to show convergence from both directions, not to make every region equally loud.
- **The zero line is meaningful.** I shaded the area below zero and labeled it "men outlive women". That makes the South Asia reversal (men outlived women until 1981) visible without reading numbers.
- **Direct labels with the 2023 value** at the right end of each line instead of a legend, so there's no back-and-forth lookup.
- **Annotations describe plateaus, not spikes.** The raw series has one-year spikes (1968 in North America, 1971 in South Asia, 1994 in Europe). I annotated typical levels ("~7.6 years through the 1970s") rather than single peaks so the text doesn't overstate, and I labeled the 1971 spike (Bangladesh war) so it doesn't look like an error. COVID-19 years are lightly shaded because the gap blips up there.
- The title states the finding, the subtitle gives the key number (the spread fell from 7.7 to 3.3 years), and the caption explains what the lines are and where the data comes from.

## 5. Visualization 2 for Question 1 (alternate)

`figures/q1b_gap_trajectories.png`

## 6. Rationale for Visualization 2

- **A connected scatterplot instead of a time series.** The x-axis is overall life expectancy (both sexes) and the y-axis is the female-male gap, and each region traces a path from 1960 to 2023. This adds a variable the first chart lacks: it shows the gap *relative to how long people live*, which suggests why the regions converge. The paths form an arch. The gap grows as life expectancy rises from about 45 to about 70, and it shrinks only in the longest-lived regions (North America and Europe hook downward at the right).
- **Time is still readable:** an open circle marks 1960, small dots mark each decade, and a filled circle marks the end. A small key explains the markers.
- **Smoothing.** Connected scatterplots get very noisy with one-year spikes, so I used a centered 5-year moving average and said so in the caption. The end point is the 2021-23 average.
- **Context layer.** Every individual country in 2023 is a faint gray dot. This shows that the regional paths sit inside the real spread, and it shows the outliers the regional averages hide: Russia, Belarus, Latvia, Ukraine and West Bank & Gaza with gaps of 9-13 years. I labeled a few of them.
- **Same color for each region as in Visualization 1**, so the two designs can be read together. Gray regions get leader-line labels to avoid overlaps.
- Two short annotations with arrows explain how to read the paths ("rich regions … now moving down", "poorer regions climb up and to the right"), since this chart type is less familiar than a line chart.

## 7. Compare the two visualizations for Question 1

The line chart (1) is the better chart for the literal question, "is the gap changing over time, and is it changing the same way everywhere?" Time is on the x-axis, the convergence is visible at a glance, the zero line makes the South Asia reversal obvious, and nearly anyone can read it. Its weakness is that it shows only the gap. You can't see that the regions whose gap shrinks are also the ones with the longest lives, so the convergence looks like a coincidence.

The connected scatterplot (2) adds that missing variable and suggests a pattern: the gap first widens and then narrows as life expectancy rises, and different regions are at different points along that arch. It also shows individual countries, which (1) can't do without clutter. The costs: time is shown only by markers, so it's harder to say *when* something happened (the 1981 crossover in South Asia is precise in (1) and approximate in (2)). The design needs a key and annotations to explain how to read it, and smoothing was required, which hides the real one-year shocks. I'd use (1) for a general audience and (2) for readers who want to see *why* the gap might be converging.

---

## 8. Story/Question 2 (Census)

Do economic downturns hit all kinds of county economies equally? No. Using the USDA county economic types, each of the last three downturns hit a different kind of county hardest. Manufacturing counties spiked first in the Great Recession (and recreation counties stayed high longest), mining counties were the only type hurt by the 2016 oil-price collapse, and recreation counties were hit hardest by COVID-19 in 2020. Farming counties had the smallest increase both times.

## 9. Visualization 1 for Question 2

`figures/q2a_unemployment_lines.png`

## 10. Rationale for Visualization 1

- **Group by economic type, not by state or urban/rural.** The census file includes the USDA 2015 economic typology (farming, mining, manufacturing, government, recreation, nonspecialized). The question is about *what a county's economy depends on*, so this is the right grouping, and it's a variable I hadn't seen used in class.
- **Weighted aggregation.** For each type and year I computed total unemployed / total labor force across all counties of that type. Averaging county rates would let a 500-person county count as much as Los Angeles. This method gives the actual unemployment rate of the people living in those counties. The caption says this.
- **Line chart over 24 years**, because this is change over time and the story is about *when* each type peaks. The three downturns are shaded and labeled along the bottom, so the eye goes straight to them.
- **Color only for the four types that carry the story** (manufacturing, recreation, mining, farming). Nonspecialized and government counties are gray, and the dotted black line is all counties combined. The legend is ordered by the story, not alphabetically, and it shows the number of counties in each type, because "mining" is only 220 counties and readers should know that.
- **Annotations at the specific points that support the claims**: manufacturing's 10.7% in 2009, recreation's 10.9% in 2010, mining's 2016 rise (the only type that went up that year), recreation's 9.1% in 2020 (2.4x its 2019 rate), and farming's 5.1%.
- **The y-axis starts at zero** so the size of the spikes isn't exaggerated.
- The title gives the main claim, and the subtitle gives one sentence per downturn.

## 11. Visualization 2 for Question 2 (alternate)

`figures/q2b_unemployment_shocks.png`

## 12. Rationale for Visualization 2

- **Shift from "rate over time" to "size of the shock, county by county."** Each panel is one downturn, and each dot is one county, placed by how much its unemployment rate changed (percentage points) from the year before the downturn to its peak (2007 to 2010, 2014 to 2016, 2019 to 2020). This shows the *distribution*, which the aggregate lines in Visualization 1 hide. It answers "is this true of typical counties of this type, or just a few big ones?"
- **Small multiples with a shared x-axis.** Using the same scale makes the three downturns comparable in size. The oil bust was small and local next to the other two, and the shared scale shows that honestly.
- **Same rows and colors as Visualization 1**, so the two charts read as a pair.
- **A median tick and an interquartile bar** on top of the dots give a quick summary. Each median is printed above its tick, and the largest increase in each panel is bold. The jittered dots are kept faint so the summary marks stand out. A small key in the corner explains the marks.
- **The zero line** shows directly that in 2014-16 almost every type *improved* (dots left of zero) while mining moved right. That is the clearest view of "mining was alone in the oil bust".
- **County-level unweighted medians** were a deliberate choice here, to complement the weighted rates in Visualization 1. The two methods agree on the story, which makes it more believable.

## 13. Compare the two visualizations for Question 2

The line chart (1) is better for showing *timing*: when each type peaked, how long recovery took (recreation counties stayed highest until 2016), and how the types compare overall. It is also familiar and easy to read. But it shows one number per type per year, weighted by population, so a few big counties could drive a line, and the 2016 mining bump looks small even though it is the key evidence.

The distribution chart (2) gives up the timeline. It shows only three before/after comparisons, and I had to pick the endpoint years, which is a judgment call. In return it shows that the pattern holds for the *typical county* of each type, shows how much counties within a type vary (the recession spread for farming counties is wide), and makes the mining story clear because it is the only row on the positive side of zero. It is denser and needs a key. The two work best together: (1) tells you when, and (2) tells you how widespread.

---

## 14. Story/Question 3

Where does U.S. population growth come from, and how does that differ between cities and rural areas? In 2021-2023, deaths outnumbered births in most small-metro and rural counties, so their growth depended entirely on people moving in. The largest metros were the opposite: they lost residents to the rest of the country and grew only through births and international immigration. Among rural counties, being next to a metro area made the difference: adjacent counties attracted domestic movers and grew, while remote ones stalled or shrank. (Census data)

## 15. Visualization for Question 3

`figures/q3_population_components.png`

## 16. Rationale for Visualization 3

- **Diverging stacked bars of the components of change.** Population change = natural change (births minus deaths) + domestic migration + international migration. These parts can be positive or negative, so I stacked positive parts to the right of zero and negative parts to the left, with a black dot showing the net sum. You can see what makes up the total and where it ends up in one row. A plain stacked bar would be invalid here because the parts have different signs.
- **Rates per 1,000 residents, pooled over 2021-2023.** Raw counts would just show that big metros are big. I summed each component over the three years and divided by summed population, so small counties with noisy single years don't distort it. I left out 2020 because its estimates cover only part of a year.
- **The 9 Rural-Urban Continuum categories**, ordered from most to least urban and split into a metro and a nonmetro group with a visual gap. Keeping all 9 (instead of just metro/nonmetro) is what reveals the adjacent-versus-remote pattern: categories 7 and 9 are the only ones that shrank, and I marked them "remote: shrinking".
- **Consistent component colors.** Natural change is blue, international migration is green, and domestic migration is orange. Domestic migration gets the most attention-grabbing color because it is the deciding factor in the story.
- **Context columns on the right**: total population (so readers know category 1 is 188M people and category 9 is 4.5M), the number of counties, and the share of counties where deaths exceeded births (45% even in big metros, about 90% in the smallest adjacent counties). These answer the obvious follow-up questions without another chart.
- **A direct "net" label** at the end of each bar, plus one short annotation for the big-metro row, which is the counterintuitive part.
- The caption explains the computation and notes that I left out the Census Bureau's small "residual" term.

---

## 17. Story/Question 4

How much progress did COVID-19 undo, and was it regained? For the 20 places with the largest pandemic-era drops, life expectancy at the low point fell back to a level last seen a median of 18 years earlier (Cuba to its 1981 level, Mexico and Paraguay to 1992). Even the United States fell back to its 1996 level. Yet by 2023, 106 of the 123 places that lost a year or more were back at or above their 2019 level. (Life expectancy data, Our World in Data version)

## 18. Visualization for Question 4

`figures/q4_covid_setback.png`

## 19. Rationale for Visualization 4

- **Re-express the drop in calendar years.** A drop of "4.8 years of life expectancy" is hard to picture. "Mexico was sent back to its 1992 level" is much more vivid. For each country I found the trough (the minimum of 2020-2022) and then the last year before 2019 when life expectancy was that low. The left panel draws a bar from that year to 2019, on a real calendar axis, so the bar length is "years of progress erased". This is an adapted range/dumbbell chart.
- **A second panel for magnitude and recovery.** The calendar measure alone would mislead, because countries that were improving slowly before 2019 (Cuba) lose more calendar years for the same drop. So the right panel shows the actual change against 2019, in years of life expectancy: a red dot at the trough and a blue diamond for 2023. Most diamonds sit just right of zero, which shows "recovered" at a glance. The exceptions (Andorra and Lebanon, still below 2019) stand out. The two panels share rows, so each country is one line across.
- **Selection and sorting.** I show the 20 largest drops (selection by size of the shock) sorted by years erased, so the left panel reads as a clean ranking. The World and the United States are added below a gap in gray italics as reference points that most readers relate to.
- **Color is used sparingly.** Red means loss and blue means recovery, and the same colors are used for the dots in the right panel and its key.
- **An outlier handled openly.** The Central African Republic's series drops 12.7 years in 2022, far beyond any other country. It isn't clearly a pandemic effect, so I excluded it and said so in the caption instead of letting it set the scale.
- The subtitle gives the summary numbers for the whole dataset (123 places lost a year or more, 106 recovered), so the chart's claim isn't based only on the 20 shown.

---

## 20. How these visualizations were made (tools, data processing, AI disclosure)

**Tools.** All six figures were made in Python (pandas for data processing, matplotlib for plotting, in a conda Python 3.14 environment). Each figure is its own script in `work/` and writes its PNG directly. There were no manual edits to the images. All titles, annotations, captions and labels are drawn by the scripts.

**Data processing.**
- *Census (Q2, Q3):* I read `full_census_dataset.csv`, which in this copy is comma-separated, Latin-1 encoded, and has comma thousands separators. I dropped Puerto Rico. For Q2 I mapped the numeric `Economic typology 2015` codes to their USDA names (0 nonspecialized, 1 farming, 2 mining, 3 manufacturing, 4 federal/state government, 5 recreation; I checked the codes against known counties, e.g. Williams Co., ND = mining and Teton Co., ID = recreation) and dropped the 20 counties without a type. I computed labor-force-weighted unemployment rates per type per year (visualization 1) and county-level changes in unemployment rate (visualization 2). For Q3 I summed natural change, domestic migration and international migration over 2021-2023 per 2023 Rural-Urban Continuum code and divided by summed population estimates to get per-1,000 yearly rates.
- *World Bank life expectancy (Q1):* I pivoted the tall file to get female, male and both-sexes values per country and year and computed female minus male. I used the seven World Bank geographic region aggregates plus "World" for the lines. For the background dots in visualization 2 I removed all aggregate codes (regions, income groups, etc.) to keep only countries. Visualization 2 uses a centered 5-year moving average.
- *Our World in Data life expectancy (Q4):* I kept entities with ISO codes (dropping OWID regional aggregates except "World" as a reference) that have complete data 1950-2023. For each, I found the 2020-22 minimum, the last pre-2019 year at or below it, and the change from 2019 to 2023. I excluded the Central African Republic as an outlier (explained in the caption).
- Intermediate tables written by the scripts are saved as CSV files in `work/` (`out_*.csv`).

**AI disclosure.** These visualizations and this write-up were produced with an AI coding agent (Anthropic's Claude, running in Claude Code). It explored the data, chose the questions, wrote the Python scripts, checked the rendered images and revised them, and drafted the text answers, including the critique. No other outside data or web sources were used.
