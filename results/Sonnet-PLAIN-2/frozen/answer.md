Numbering follows the Canvas survey order. Figure files are in `answers/figures/`.

## 1. Critique (no CLO; critique of the provided example, "Income inequality varies across states")

What works: the dumbbell (max and min county median income per state, joined by a line) is a sensible encoding. Position on a shared axis makes the min-to-max range easy to read. The ratio labels (1.01x to 3.78x) give a second, derived measure. The caption defines the dots and the lines, and the ordering by ratio gives a clear left-to-right progression.

What does not work: (1) The title says "inequality", but the chart only shows the extreme counties' medians. One rich and one poor county say little about inequality within a state, and the range depends heavily on how many counties a state has (Wyoming and Delaware have few counties, Virginia has many independent cities). (2) The x-axis has no title, and the state names appear both on the axis and as labels under the orange dots. This repeats information and is cluttered. (3) The "Measure Names" legend with "Max." and "Min." is Tableau default wording, and the Tableau UI wording leaks into the figure. The y-axis starts at 0 and wastes space below about 25K. (4) The selection (top 5, bottom 5, and 6 "interesting" states) is subjective, and the caption says so only at the very end. (5) The "3.78x" label collides with the VA dot, and the WY dots overlap. (6) Blue/orange is a fine colorblind-safe pairing, but the grey connector is heavier than needed. Suggestions: plot all states, sorted by ratio, use a dot plot with a log axis or plot the ratio directly, and retitle it "How far apart are a state's richest and poorest counties?".

## 2. Story/Question 1 (Life Expectancy)

Women outlive men almost everywhere, but has the female advantage in life expectancy grown or shrunk since 1960, and does it differ by country? (It has widened in most places, but narrowed in the US and in several African countries and Kuwait, and it is exceptionally large in Eastern Europe.)

## 3. Visualization 1 for Question 1

`figures/q1_a_gap_over_time.png`

## 4. Rationale for Visualization 1

The question is about change over time, so I used lines with year on the x-axis. I plotted the single quantity that answers the question, the female-minus-male gap, instead of two life-expectancy curves, so a viewer reads one number per country-year, and the zero line has a clear meaning ("equal"). All countries appear as thin grey lines, which gives context and shows the spread (the focus-plus-context strategy), and I highlighted a small set with distinct colors and direct end labels instead of a legend: Russia and Ukraine (huge gaps), the US (shrinking), India (from negative to positive), Nigeria (nearly closed), China, and the dashed black world line (almost flat at 4 to 5 years, so "the average hides divergent paths"). Three short annotations point the viewer to the main events (Russia in the 1990s, the US decline after 1970, India crossing zero). Title states the finding; subtitle defines the measure; caption gives the data source, how aggregates were handled, and a number or two. Aggregates (income groups, regions) were excluded from the grey lines.

## 5. Visualization 2 for Question 1

`figures/q1_b_gap_1960_vs_2023.png`

## 6. Rationale for Visualization 2 (Question 1 alternate)

This version drops the time axis and compares just two years: each country is a dot with its 1960 gap on x and its 2023 gap on y. The identity diagonal turns "did it grow or shrink?" into "above or below the line", which is a simple position judgment. I shaded the two half-planes and labeled them in words, and colored the dots by whether the change exceeded one year (orange widened, grey about the same, blue narrowed) to make the three groups pop out without reading values. Labels were added for a deliberately chosen set of countries (Ukraine, Russia, Lithuania, US, India, Nigeria, Togo, Kuwait, and others) so the viewer can anchor on familiar places. This design gives a country-by-country picture of where change happened, which lines cannot show clearly with 200 series.

## 7. Compare the two visualizations for Question 1

The line chart (A) shows the whole history, including timing: the Soviet-era divergence, the early-1990s spike, the US decline, the 2022 jump in Ukraine. It shows only a few countries clearly, and the grey lines are a tangle (spikes from small territories), so the viewer cannot find a particular country or see the overall pattern of change across countries. The scatterplot (B) shows every country at once with a clear summary of direction and size of change (most dots above the diagonal, a cluster below), and countries are easy to locate. It loses everything between the two years (a country could have risen and fallen again, as Russia did) and it needs the viewer to understand a diagonal reference line, which is a less familiar chart for a general audience. A is better for a newspaper audience and for time stories; B is better for a scientific audience and for the distribution of change.

## 8. Story/Question 2 (Census)

Between 1990 and 2019-23, did college education grow equally across the US, or did metropolitan counties pull ahead of rural ones? (All county types gained, but the largest metro counties gained 16.6 points versus 8 to 9 for most rural types, so the urban-rural gap in college attainment roughly doubled.)

## 9. Visualization 1 for Question 2

`figures/q2_a_education_by_county_type_dumbbell.png`

## 10. Rationale for Visualization 1

The summary unit is the USDA Rural-Urban Continuum Code (nine ordered county types), so each type gets a row, in the natural order from big metro to remote rural. A dumbbell with an open dot for 1990 and a filled dot for 2019-23 shows both levels and the change as the length of the segment, and the aligned numeric labels let the viewer read exact values. A separate "Gain (pts)" column makes the key comparison (+16.6 for big metros against +8 to +10 for most rural types) a direct read. Color separates metro (blue) from nonmetro (orange) with a dotted divider, so the main contrast is visible at a glance. I used medians per county rather than means, because county percentages are skewed, and I say in the caption that they are not population-weighted. The title states the finding, and the caption gives the 15%-to-32% versus 11%-to-20% example and the gap growth (4 to 11 points).

## 11. Visualization 2 for Question 2

`figures/q2_b_education_1990_vs_2019_scatter.png`

## 12. Rationale for Visualization 2

This version shows every county (3,165) as a dot: 1990 share on x, 2019-23 share on y, with the identity line as "no change" and dotted +15 and +30 point guides. Color shows metro versus nonmetro, and dot area shows 2020 population, so the viewer sees that the big, populous metro counties sit high and to the right, with larger gains, while small nonmetro counties cluster in the lower left. Transparency handles the overplotting, and the diamond markers give the median of each group so the eye has a summary. The title says the main finding (almost every county gained, the gains were biggest where the starting point was highest) and the caption gives medians of gains for high and low starters and notes that 27 counties lost share.

## 13. Compare the two visualizations for Question 2

The dumbbell chart (A) is cleaner and easier to read: nine rows, exact values and gains printed, and the message (metro pulled ahead) is obvious in seconds. It hides the within-group variation, so a viewer may think every metro county is at 32%, and it relies on medians. The scatterplot (B) shows the full distribution, the outliers (small, rich counties such as college towns), and the population weighting through size, and it exposes that the urban-rural split is a tendency and not a clean partition, because the two clouds overlap heavily. The price is that it is harder to read, because the viewer must understand the diagonal, there is overplotting in the lower left, and the main message takes longer to see. A suits a general audience; B suits an audience that wants to see the data.

## 14. Story/Question 3

(Census data) How did unemployment respond to the Great Recession and to the 2020 pandemic in different kinds of counties? The recession raised unemployment by about 4 to 5 points in every county type, but the 2020 pandemic spike was much steeper in big metropolitan counties (+5.1 points) than in remote rural counties (+2.8).

## 15. Visualization for Question 3

`figures/q3_unemployment_shocks_by_county_type.png`

## 16. Rationale for Visualization 3

A compound design with two panels. The left panel is a line chart of the labor-force-weighted unemployment rate from 2000 to 2023 for four county groups (large metro, other metro, nonmetro adjacent to a metro area, nonmetro remote), with the two shocks shaded and labeled, so the viewer sees when they happened and how similar the curves are. Nine separate codes would be unreadable, so I merged them into four ordered groups (blue for metro and orange/brown for nonmetro, with a lighter shade for the less urban member of each pair). The right panel answers the comparison that is hard to see on the left: a dot pair per group giving the rise in the rate for each shock (open = 2007 to 2010, filled = 2019 to 2020), with values printed. The two panels share colors, so the viewer connects them. I only used counties that have data in all 24 years (3,082) so the groups do not change composition over time. The Great Recession dates come from common knowledge, not from added data, and the caption says that.

## 17. Story/Question 4

(Life expectancy data) Which countries lost the most life expectancy in the first two pandemic years, and had they recovered by 2023?

## 18. Visualization for Question 4

`figures/q4_covid_life_expectancy_heatmap.png`

## 19. Rationale for Visualization 4

A heatmap table is a good fit because the question has two dimensions to read, which country and which year, and the reader wants the pattern of dip then rebound. Each cell is the change in life expectancy versus 2019, with a diverging red-blue colormap centered on zero (red = loss, blue = gain) and the value printed in each cell so that it can be read exactly. I selected the 25 countries with the largest loss in 2020 or 2021 and sorted them by their worst loss, so the biggest drops are at the top and the color gradient comes out as a clear column pattern: the deep reds in 2021, near-neutral colors in 2022, and blue in 2023. I added the world average as a separated, bold last row for reference (it lost 1.7 years in 2021, much less than the hardest-hit countries). The figure also shows the exceptions that did not recover (North Macedonia, Lebanon). I omitted very small territories (Andorra, Gibraltar, and so on) because their estimates are noisy. The title states the finding and the caption notes the selection rule.

## 20. How I made these visualizations (tools and AI disclosure)

I (Claude Code, an AI coding assistant made by Anthropic; model Sonnet 5.5) made all of this work at the request of the course instructor, as an example response for the instructor's private instructional review. It is not a student submission. The AI chose the stories, did all of the data processing, wrote all of the code, designed and revised the six figures after looking at the rendered images, and wrote every answer above, including the critique in answer 1 (which is the AI's opinion). No human did the design or writing; the instructor supplied the assignment and authorized the example.

Tools: Python 3.14 (conda environment p314) with pandas for data processing and matplotlib for the figures; no other tools and no interactive tools. Data processing: the World Bank life-expectancy file was pivoted from tall to wide by Sex to compute the female-minus-male gap; regional and income aggregates (for example "World", "OECD members") were excluded from country-level charts by a name filter (the "World" row was used only as a reference); in the Census county file, counties without a 2023 Rural-Urban Continuum Code or without the needed values were dropped from each chart (counts are in each caption); county-type groups for Q3 were pooled by summing unemployed and labor force; changes were computed relative to 2019 for Q4. No outside data were added. The scripts and a README are in `work/`.
