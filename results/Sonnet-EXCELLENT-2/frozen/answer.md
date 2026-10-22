# Design Exercise 4-2 answers (numbered to match the Canvas survey)

Figure files are in `answers/figures/`.

## 1. Critique (Income inequality varies across states)

The strongest part of this chart is its dumbbell structure: a state's maximum and minimum county median income share one vertical position axis, so the length of each grey line shows the spread directly, and the "x times" labels give the ratio. The title states a finding rather than a topic, and the caption explains the encoding.

The weaknesses are in the choices behind the data. First, the story depends on an extreme-value statistic: the max and min of county medians are single counties, often tiny or unusual, and the spread says little about inequality within a typical state. A state with one rich suburb and one poor rural county looks "unequal" even if almost everyone lives near the middle, and the chart never shows population, so a reader cannot tell whether the extremes matter. Second, "income inequality" is a misnomer: these are differences between county medians (geographic disparity), not household inequality. Third, the 16 states were chosen by a mix of top 5, bottom 5 and "interested" states; the x-axis order (by ratio) is not obvious to a reader and the selection leaves out most of the country. Fourth, a ratio is labeled on top but the vertical encoding is absolute dollars, so the eye compares length (difference) while the label reports a ratio; for states with different income levels these disagree (compare AL and CA). A log axis or plotting the ratio directly would match the claim. Fifth, the blue/orange legend is Tableau's default "Measure Names", which is jargon; direct labels such as "richest county" and "poorest county" would be better, and the axis starts at 0 although the data live between 30K and 150K, which wastes about half the plot area. The labels on points sometimes collide with the dots (WY, VA), and the "states of interest" are never named. Overall: clear and readable, but the design answers a narrower question than the title promises.

## 2. Story/Question 1 (life expectancy)

Is women's life-expectancy advantage a fixed feature of every country, or does it rise and fall as countries get healthier, and which countries break the common pattern?

## 3. Visualization 1 for Question 1

`figures/q1_primary_connected_scatter.png`

## 4. Rationale, Visualization 1

The key decision was to put life expectancy, not time, on the x-axis. The story is about a country's stage of health, and time hides it: countries reached the same life expectancy decades apart (South Korea in 1988, Brazil in 2002, India in 2017). Plotting female minus male gap against both-sex life expectancy lines all countries up on a common "development" axis, and a thick median curve then shows the shape directly: the gap rises until life expectancy is about 70, then declines. All 217 countries (aggregates removed) are drawn as thin grey paths so the reader sees the spread and the noise, and six countries are highlighted in a colorblind-safe palette with hollow start (1960) and filled end (2023) markers and direct labels instead of a legend. I chose countries that behave differently: the United States and South Korea (peaked, then narrowed), Brazil (near peak), India (rising from a negative gap), Nigeria (shrinking toward zero), and Russia (very large and still large). A zero line and a vertical line at 70 anchor interpretation; the caption notes that spikes in the grey paths are war or epidemic years.

## 5. Visualization 2 for Question 1

`figures/q1_alternate_small_multiples.png`

## 6. Rationale, Visualization 2

This version asks the same question in calendar time and by country. A 3 x 3 grid of small multiples (shared axes) gives each of nine countries its own panel: shaded area and line for the female-minus-male gap, and a grey line for the median across all countries as a constant reference, so each country is judged against the typical case rather than against the other panels. A dot marks each country's peak year, and the panel title reports the peak and 2023 values and the life-expectancy range, so the numbers behind the story are readable. Only two colors are used: blue for ordinary cases, red-orange for Russia, which is the one case that needs separate emphasis. Shared y-axes make the Russian gap (up to 14 years) and the Nigerian collapse comparable to the others. Countries were chosen to span narrowing (US, Germany, South Korea), near-peak (Japan, Brazil, China), rising (India), and outliers (Russia, Nigeria).

## 7. Comparison of the two Question 1 visualizations

The connected scatter shows the general law (an inverted-U in the median) and lets 217 countries appear at once, so the claim "this is a pattern across the world, not a hand-picked example" is visible. Its cost is legibility: time is implicit in the path direction, paths cross, and the reader must trace a line to learn when anything happened. It also depends on the reader accepting life expectancy as a stand-in for development. The small multiples are far easier to read per country, with years on the axis, peak annotations and a shared median baseline, and they make comparison between countries concrete. But they show only nine countries, so the "typical" pattern is carried by the grey median line and the reader must trust my selection, and the link between the gap and life-expectancy level is only given in text. I would use the scatter for a scientific audience asking about the relationship and the small multiples for a general audience asking what happened in specific countries.

## 8. Story/Question 2 (census)

Everyone's college attainment rose from 1990 to 2019-23, but did the gap between metropolitan and rural counties shrink or widen, and are rural counties catching up?

## 9. Visualization 1 for Question 2

`figures/q2_primary_scatter.png`

## 10. Rationale, Visualization 1

This is a county-level scatterplot of 1990 versus 2019-23 college share, with a dashed "no change" diagonal. The point is that each county is its own before/after pair, so we can see both the average shift and the spread. Color separates three groups from the 2023 USDA Rural-urban Continuum Code (metro 1-3, nonmetro with urban population 4-7, most rural 8-9), and large diamonds mark each group's median so the main message does not depend on picking out individual dots. Dot area is proportional to 2020 population, so the many tiny rural counties do not visually outweigh the populous metro counties; transparency handles overplotting. Because everything lies above the diagonal, the reader sees at once that nearly every county gained, and because the metro cloud sits above and to the right of the others, that the already-educated places gained more (about 13 points at the median versus about 9 for the most rural). The one labeled outlier, San Miguel County, Colorado (a ski resort), shows that rural counties can rise sharply when amenity migration changes who lives there. Connecticut is excluded because its county boundaries changed.

## 11. Visualization 2 for Question 2

`figures/q2_alternate_range_dumbbell.png`

## 12. Rationale, Visualization 2

The alternate gives up individual counties to compare the nine USDA county types directly. Each row is one Rural-urban Continuum category, ordered from the largest metro areas to the most remote rural counties. Within a row, a grey bar (middle half of counties) and dot (median) show 1990, a blue bar and dot show 2019-23, and an arrow with a bold number gives the change in the median. Distributions are on the same horizontal axis starting at zero so lengths are comparable. The ordered rows make the main contrast, a +16 point gain at the top versus +8 to +9 for the rural rows, readable from the numbers alone; the bars show that the metro distribution is both higher and much wider in 2019-23. The title states the headline: the median gap between code 1 and code 9 counties grew from about 4 to about 11 points. I added short, plain-language row labels rather than raw codes.

## 13. Comparison of the two Question 2 visualizations

The scatter keeps every county, so it shows the within-group variation and rural outliers that a median cannot, and it conveys "everyone is above the line". But it is dense, with heavy overlap in the 10-25% region, and the group medians are what carry the actual finding. The range dumbbell is much easier to read and to cite: there are nine rows, each with a before, an after and a change, and the effect size per county type is explicit. Its cost is that it hides individual counties and the relationship between a county's own 1990 and later values (a high-gain county in a "rural" row is invisible), and the IQR bars understate the outliers. The unweighted medians treat tiny and large counties alike, which both figures share. The scatter is better for exploration, the dumbbell for communication.

## 14. Story/Question 3

Does having a more educated county protect against unemployment, and did that protection hold in both the 2008-09 recession and the 2020 pandemic?

## 15. Visualization 3

`figures/q3_unemployment_by_education.png`

## 16. Rationale, Visualization 3

I grouped about 3,200 counties into quartiles by their 1990 college share (fixed before the period shown so groups do not change with outcomes) and computed each group's unemployment rate as total unemployed divided by total labor force, which weights by county size. The upper panel is a line chart, 2000-2023, with the Great Recession and 2020 shaded. Education is encoded with one blue hue from light (least educated) to dark (most educated), the right choice for an ordered variable, and the lines are labeled directly. The lower panel gives the key quantity, least-educated minus most-educated unemployment, as bars so the reader does not have to subtract two lines by eye: positive in every year through 2019 (peaking at +2.7 points in 2009), negative in 2020 and 2021 (-0.7 in 2020). The annotation draws attention to the 2020 peak, where third-quartile counties had the highest rate (8.8% versus 7.3% for the least educated). The caption warns this is correlational: educated counties are also more metropolitan, and 2020 hit service-heavy metro economies.

## 17. Story/Question 4

Which countries lost the most life expectancy in the COVID years, and have they recovered by 2023? Is recovery related to how large the loss was?

## 18. Visualization 4

`figures/q4_covid_recovery_arrows.png`

## 19. Rationale, Visualization 4

Each row is a country, and an arrow runs from its 2021 life-expectancy change (relative to 2019) to its 2023 change, with the 2019 level as a bold vertical reference line. This encodes both quantities on one common scale and makes recovery the visible length and direction of the arrow. Blue arrows end at or above 2019, orange arrows end below it, and a number column on the right gives the 2023 value, so color is redundant with position and text. I deliberately did not plot all 217 countries: the top block shows countries among the largest 2019-21 losses (Bolivia, Paraguay, Mexico, Peru, Ecuador, Colombia, South Africa, plus India for its population), all of which recovered; the lower block gives contrast cases with small dips that remain below 2019 (Germany, Canada, the United States, Singapore, Japan, Thailand), plus North Macedonia and Libya. West Bank and Gaza is included as an honest outlier whose 2023 fall is from war rather than COVID, as the caption says. The selection is explicit and described, and the title makes the surprising point: the size of the 2021 loss does not predict who is still below 2019.

## 20. How the visualizations were made, and AI disclosure

All six figures, the code, and this written text were produced by an AI assistant (Claude, Anthropic; the Claude Code agent), at the request of the course instructor, as a complete example response for the instructor's private instructional review. This is not a student submission and no student wrote or claimed it. The AI chose the questions, wrote the code, made the figures, inspected the rendered images and fixed layout problems, and wrote all of the answers including the critique. The tools were Python 3.14 (pandas, numpy, matplotlib) from the p314 environment, using the course data files only (World Bank life expectancy by sex, 1960-2023; USDA county census data). No web pages were opened and no outside data were added. Data processing: pivoted the life-expectancy file to Female/Male/Both and computed gap = female minus male; removed regional and income aggregates by name (217 countries remain); removed the national and state rows from the county file; excluded Connecticut from the 1990 versus 2019-23 comparison because its counties changed; took medians, quartiles of 1990 college share, and labor-force-weighted unemployment rates. The scripts are in `work/` (see `work/README.md`).
