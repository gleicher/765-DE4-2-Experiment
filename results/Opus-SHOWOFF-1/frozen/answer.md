# Design Exercise 4-2: Canvas answers

Figures are in `answers/figures/`. Each is a single static PNG with its own title, labels, legend and caption:

| Canvas Q | File |
|---|---|
| 3 | `figures/q1a_gap_arc.png` |
| 5 | `figures/q1b_gap_heatmap.png` |
| 9 | `figures/q2a_components_by_rucc.png` |
| 11 | `figures/q2b_county_quadrants.png` |
| 15 | `figures/q3_fifty_to_seventy.png` |
| 18 | `figures/q4_two_recessions.png` |

---

## 1. Critique (not part of the CLO)

**What it is trying to say.** For a selection of states, the chart compares the richest and poorest county (by 2021 median household income) and labels the ratio between them. The claim is that "income inequality varies across states", from Wyoming (1.01x) to Virginia (3.78x).

**What works.** A range (dumbbell) chart is a sensible choice: one vertical bar per state with the two extremes marked shows the spread directly. Sorting by the ratio gives the eye a clear left-to-right progression. The y-axis starts at zero, the ratio labels give the exact number the title is about, and the caption explains the encoding and how states were chosen, so the image mostly works without outside explanation.

**Problems, roughly from most to least serious.**

1. *The measure does not support the claim.* The range across counties is not income inequality. It ignores inequality within counties, gives a 600-person county the same weight as a 2-million-person one, and depends mechanically on how many counties a state has. Texas (254 counties) and Georgia (159) get many more chances at an extreme value than Delaware (3) or New Hampshire (10). In the course's current county data (2022 incomes), the rank correlation between a state's county count and its max/min ratio is about 0.57. The chart cannot separate "more unequal" from "has more counties".
2. *Some values look wrong.* Wyoming's 23 counties span only 1.01x ($62–63K). In the 2022 data, Wyoming's counties span $53.5K–$127.7K (2.4x), and Alaska and North Dakota are also around 2x rather than 1.1x. A one-year change does not explain gaps that large. I suspect a filtering or aggregation error, for example a state-level row or a few counties surviving a filter. The most striking end of the story is the least trustworthy part of the chart.
3. *Encoding mismatch.* Bars are sorted and labeled by the **ratio**, but bar length shows the **dollar difference**. So Alabama (2.83x) has a shorter bar than California (2.77x), and the bars do not grow steadily from left to right even though the labels do. A log-scaled y-axis would fix this: bar length would then be proportional to the ratio, and the sort order, the labels and the bar lengths would all agree.
4. *Selection is unexplained in the picture.* "Top 5, bottom 5 and 6 additional interested states" are merged into one sorted row with nothing to show which group each state is in or why the six were chosen. Showing all 50 states (or all 50 in grey with the interesting ones highlighted) would avoid any suspicion of cherry-picking, and it still fits on a page.
5. *Tool defaults left in.* "Measure Names", "Max."/"Min.", the "State" header strip, and Tableau's default blue/orange all read as unfinished. The state codes appear twice (under the orange dots and on the x-axis). The "1.01x" label collides with the Wyoming dots. The title states a truism ("varies") rather than the finding.

**How I would improve it.** Retitle it with the finding ("Virginia's richest county earns 3.8x its poorest; Delaware's only 1.2x"). Use a log scale. Include all states, with a light marker for each state's own median county. Add a small note or encoding (e.g., dot size) for the number of counties, so readers can judge the count confound. Re-check the low-ratio states against the raw data. Better still, if the question really is inequality, use a population-weighted spread such as the gap between the 10th- and 90th-percentile county weighted by households. Overall this is a reasonable, standard design with a clear caption, held back by a measure that doesn't match its claim and some data values that look wrong.

---

## 2. Story / Question 1 (Life expectancy)

Women outlive men almost everywhere, but is their lead simply growing as the world gets healthier? No. Across 217 countries since 1960, the female advantage widens as life expectancy rises, peaks at about 6 years when overall life expectancy is in the low 70s, and then narrows in the healthiest countries. Some countries, such as Russia and other former Soviet states, sit far above this pattern.

## 3. Visualization 1 for Question 1

`answers/figures/q1a_gap_arc.png`

## 4. Rationale (Question 1, primary)

*Design type: adapted / compound standard design (connected scatterplot over a context cloud).*

- **The key choice is the x-axis.** I plotted the gap against **overall life expectancy** rather than calendar year. Countries develop at very different times, so a time-axis view of 217 countries is a tangle. Putting each country at its own stage of health makes a shared pattern appear: an arc.
- **Three layers, each with a job.** (1) Every country-year (≈13,800 points) as faint grey dots gives context and honesty: readers can see the spread and the outliers. (2) A bold black **median curve with an interquartile band**, computed in 2-year bins of life expectancy, states the pattern. (3) Four **coloured trails** turn the cross-sectional arc into actual country histories, so the viewer sees that individual countries really move along it.
- **Choosing the four countries.** Each shows a different way through the arc. Sweden follows the typical path. South Korea follows the same arc compressed in time. India started *below zero* (men outlived women in 1960) and is still on the rising side. Russia shows that the arc is a tendency, not a law. A very different trail would have been a data dump.
- **Time stays readable on a non-time axis.** Open circle = 1960, small dots = each decade, filled circle = 2023, plus a small key. Selected years are labelled directly. Trails are smoothed over 3 years so annual noise doesn't hide the direction.
- **Colour.** Categorical hues from a colour-blind-checked palette, used only for the four highlighted countries. Everything else is grey, so colour means "look here". The identity of each trail never depends on colour alone: every trail is directly labelled, and the side panel repeats the colour swatch beside the name.
- **Reference line and wording.** A zero line labelled "Women outlive men / Men outlive women" makes the sign of the gap explicit. The title states the finding. The side panel gives one quantitative sentence per country. The caption gives the source, excluded aggregates, binning rules, and a reminder that this is descriptive, not causal.

## 5. Visualization 2 for Question 1

`answers/figures/q1b_gap_heatmap.png`

## 6. Rationale (Question 1, alternate)

*Design type: adapted / compound design (heatmap with columns re-indexed by life expectancy, plus marginal bars and a dumbbell).*

- **Same story, different encoding.** Instead of positions and trails, the gap is encoded as **colour in a grid**. Rows are 43 large countries from every region. Columns are **2-year bins of overall life expectancy**, not years, so each row reads left to right as that country got healthier. This "align by stage of health instead of by date" idea is what makes the arc visible country by country: rows darken towards the middle (≈65–78) and, for most of the healthiest countries, lighten again at their right-hand end.
- **The staircase is information.** Sorting rows by 2023 life expectancy (in four labelled tiers) means each row's right edge is where that country has got to. The row's left edge is where it started in 1960. The shape of the blank area itself shows how far each country has come.
- **Marginal bar chart on top.** It gives the median gap for *all* 217 countries in each column, the same "typical curve" as Visualization 1, coloured with the same scale. The reader gets the overall pattern without having to average 43 rows by eye.
- **Peak markers and a right-hand dumbbell.** A ring marks the column where each country's gap was widest. The dumbbell compares that widest gap with the actual 2023 gap, which answers the follow-up "how much has it narrowed?" (Netherlands 6.4 → 2.9, Sweden 5.9 → 3.3, Russia 13.2 → 10.7).
- **Colour scale.** A **stepped** (binned) diverging scale: blue for the rare negative cells (men outliving women: South Asia in the 1960s–80s), a neutral grey around 0–2, then a single-hue light-to-dark orange-red for a growing female lead. One-year steps are used where most values sit (2–8 years) so differences are readable, with wider steps at the extremes. Blank cells mean "this country was never at this level", which I explain in the caption.
- **COVID handling.** Cells use 1960–2019, so the temporary 2020–21 spike in male deaths doesn't create artificial peaks. The 2023 values in the dumbbell show where things stand now.

## 7. Compare the two visualizations for Question 1

**Visualization 1 (connected scatter)** is the better choice for showing the *shape* of the relationship and the outliers. Position on a common scale is the most accurate encoding, so readers can read off "peak ≈ 6.2 years at ≈ 71" and see exactly how far Russia sits above the curve. The grey cloud shows *all* the data. The trails make the over-time story concrete. Its weaknesses: it can only follow a handful of countries before it tangles, the selection of four is mine, and connected scatterplots take a moment to learn (hence the marker key).

**Visualization 2 (re-indexed heatmap)** scales to **43 countries at once**, so the reader can check that the arc is not just four hand-picked examples. It shows which countries break the pattern (Viet Nam, Kazakhstan, Russia and Ukraine are dark across their whole row). The dumbbell adds a direct "peak vs now" comparison. Its weaknesses: colour is less precise than position, so differences of half a year are hard to judge; binning by life expectancy hides *when* things happened; and it needs more explanation (the subtitle has to explain the unusual column choice).

In short, Visualization 1 is better for a general audience and for the headline. Visualization 2 is the "show me it holds generally" view for a more analytical reader. Together, one gives the curve and the other shows how widely it holds.

---

## 8. Story / Question 2 (Census)

Where does each kind of US county's recent population growth come from? Between 2021 and 2023, the biggest metros grew only through births and immigration while Americans moved out. Rural counties are the mirror image: deaths outnumber births in five out of six of them, and most of those are refilled by Americans moving in from elsewhere in the country.

## 9. Visualization 1 for Question 2

`answers/figures/q2a_components_by_rucc.png`

## 10. Rationale (Question 2, primary)

*Design type: standard design done carefully (aligned small-multiple diverging bar charts).*

- **Decomposition as the organising idea.** Population change = births − deaths + domestic migration + international migration. I gave each component its own panel, laid out left to right with "+" and "=" in the panel titles, so the figure reads like the equation. This is better than a diverging stacked bar: every bar starts from a common zero, so components can be compared exactly, and the sign of each one stays visible.
- **Rows are the full urban-to-rural range.** All nine 2023 Rural-Urban Continuum Codes, with their meanings spelled out (not just "RUCC 6"), grouped under METRO / NONMETRO brackets with a gap between the groups. Each row shows its number of counties and population, so the reader knows that row 1 is 187M people while row 9 is 4.5M.
- **Rates, population-weighted.** Raw counts would just show "big places are big". I used per-1,000-residents-per-year rates computed for each group as a whole (sum of component ÷ sum of population). That answers "what is happening to people in this kind of place", and an unweighted mean would let tiny counties dominate.
- **Colour encodes polarity only**: blue adds people, red removes them (a diverging pair, stated in the subtitle). The total-change panel is a neutral dark grey on a light panel background, to mark it as the sum rather than another component. Every bar has a signed value label, so colour is never the only cue.
- **Text does the guiding.** The title states the finding. Each panel has a one-line takeaway under its title ("Deaths outnumber births in every nonmetro group", "Americans leave the 1M+ metros for smaller places"…). The caption documents the formula, the years, and the exclusions: Puerto Rico has no components data, and 17 retired Alaska/Connecticut units have no 2023 code.

## 11. Visualization 2 for Question 2

`answers/figures/q2b_county_quadrants.png`

## 12. Rationale (Question 2, alternate)

*Design type: compound / adapted design (small-multiple quadrant scatterplots with a shared background).*

- **County level, not group averages.** Each of 3,106 counties is a dot at (natural change, net domestic migration), so the figure shows the *distribution* behind the averages in Visualization 1. Dot area = population.
- **Quadrants are the story.** The zero lines divide the plane into four meaningful situations, each labelled in plain words ("deaths > births, but Americans move in", "shrinking both ways"…) with the **share of that panel's counties** in big type. The top-left quadrant, the "refilled" situation, is shaded, and its number is largest in the rural panel (52%; with the 31% shrinking both ways, that makes 83% ≈ five in six with natural decrease).
- **Small multiples with a grey "everyone else" layer.** One panel each for big metros, smaller metros and nonmetro, using the same axes. All other counties are repeated in light grey, so every panel can be compared against the whole country without overplotting 3,000 coloured dots in one chart. A median cross per panel shows the cloud moving left (more deaths) from metro to rural.
- **Colour** carries identity only (three categorical hues, the maximum my palette check allows for a scatter), and every panel is titled, so colour is never needed to tell them apart.
- **It shows something Visualization 1 can't.** In the big-metro panel the *median* county gains domestic movers (+5.5), while a few huge core counties (Los Angeles, Cook, Brooklyn, labelled) lose many. The aggregate "Americans leave big metros" is really "Americans leave the giant core counties for their suburbs". I state this in the subtitle.
- **Honest handling of extremes.** Axes are trimmed to the range where the data is dense, and the caption says that a few extreme small counties are pinned to the panel edge rather than dropped.

## 13. Compare the two visualizations for Question 2

**Visualization 1** gives the cleanest answer to "where does growth come from?" One glance shows the mirror image (big metros: + natural, − domestic, + international; rural: − natural, + domestic). Exact values are labelled, and the nine-level continuum shows that the change is gradual, not just a two-way metro/rural split. But it is aggregated: it can't show variation within a group, and it can suggest that every big-metro county is losing people to other parts of the US.

**Visualization 2** gives up exact component values and the international-migration piece. In return it shows the **variation across counties**, how common each situation is (quadrant shares), and the core-versus-suburb nuance that the aggregate hides. It is busier and needs the reader to learn a quadrant layout, and with only three groups it loses the fine nine-level gradient.

The primary is better for a newspaper-style "here's the pattern". The alternate is better for an analyst asking "is this true of typical counties, or driven by a few big ones?" Used together, the second confirms the first for rural America and refines it for the big metros.

---

## 14. Story / Question 3

Do countries that reach a life expectancy of 50 later get to 70 faster? Mostly yes: pioneers like Norway and Sweden took 60–90 years, and Japan took 17. But the speed-up peaked with countries that reached 50 in 1930–49 (about 35 years). Groups that reached 50 after 1965 are going slower, and most of them have not reached 70 yet. (Our World in Data long-run life expectancy.)

## 15. Visualization for Question 3

`answers/figures/q3_fifty_to_seventy.png`

## 16. Rationale for Visualization 3

*Design type: compound design (annotated scatterplot plus Kaplan–Meier "time-to-milestone" curves sharing one colour encoding).*

- **Derived measures.** The data is raw life-expectancy series. I derived two numbers per country: the (interpolated) year it first reached 50, and the years it took to go from 50 to 70. This turns a pile of 236 time series into one comparable quantity, the speed of the health transition, which is what the question is about. I only counted a crossing if the observations either side were at most 10 years apart, because pre-1950 data is sparse for many countries. Countries already above 50 at their first observation are left out, because their crossing year is unknown.
- **Handling countries that haven't arrived yet.** Ignoring countries that haven't reached 70 would hide exactly the slow cases and make recent groups look fast. So (a) in the scatter they are hollow triangles at "years so far", which places them on the edge of a shaded **"not yet observable"** region (any dot above y = 2023 − x would end in the future), and (b) the right panel uses a **Kaplan–Meier estimate**, a standard way to handle "still waiting" cases, giving the share of each group that has reached 70 after N years. The caption explains this in plain language.
- **Why two panels.** The scatter shows individual countries and lets me label the memorable ones (Norway 93 years, Japan 17, Oman and Maldives ≈ 19–24, Guyana 72). The curves give the group-level answer, which you can't read from a cloud of 160 dots. The two panels share an **ordinal colour scale** (light = reached 50 early, dark = recently), so the panels are linked without needing a second legend. The scatter's x-position already shows the year, so colour there mainly makes the link.
- **Reading the right panel.** A curve further left means a faster group. The 1930–49 group (mid-blue) is furthest left. The two most recent groups start fast but level off below 60% and 35%. A 40-year reference line helps comparison. The title states the two-part finding. The subtitle gives the key numbers.

---

## 17. Story / Question 4

Is rural unemployment always worse than in big cities, and did the two big shocks of the period (the Great Recession and COVID-19) hit the same places? For twenty years (2000–2019), rural (nonmetro) unemployment ran above the big metros'. In the Great Recession every kind of county saw a similar 4–5 point rise. COVID reversed the usual pattern: the 2020 jump was largest in metros of 1M+ (+5.1 points) and fell almost step by step to the most remote counties (+2.2).

## 18. Visualization for Question 4

`answers/figures/q4_two_recessions.png`

## 19. Rationale for Visualization 4

*Design type: compound design (line chart + aligned difference bars + dumbbell plot).*

- **Three linked views, one question.** (1) *Line chart* of unemployment rates, 2000–2023, for three county groups, which gives the context and both recessions. (2) *Difference bars* directly below, sharing the same x-axis: rural minus big-metro rate. The lines are close together, and their gap is the story, so I plotted the gap itself instead of making readers subtract two lines by eye. Orange (rural worse) for 18 years, then a sudden blue (big metros worse) in 2020–21. (3) A *dumbbell* across all nine RUCC codes comparing the rise in each recession (2007→2010 vs 2019→2020). It shows the steady COVID gradient and the flat Great Recession pattern at full resolution.
- **Weighting.** Rates are total unemployed ÷ total labour force for each group, so each group's rate is the rate a typical *worker* in that group faced, not an average of county percentages.
- **Consistency with Question 2.** The same blue/aqua/orange hues mean the same county groups as in Visualization 2B, and the same 2023 RUCC labels and exclusions are used, so the census figures read as one set.
- **Emphasis.** Recession periods are shaded in all three panels. The two contrasting moments (2010 and 2020) get dots and short numeric annotations. The dumbbell uses a distinct shape *and* colour for the two recessions (grey square vs red circle) with a legend, so it works without colour. The dumbbell's text panel states the two results in numbers. The title states the reversal.
- **Caveats in the caption.** 2023 codes are applied to all years. Puerto Rico and retired AK/CT units are excluded. Annual averages hide the April 2020 peak, which makes the 2020 jumps conservative.

---

## 20. How I made these visualizations (tools, data processing, AI disclosure)

**Tools.** All six figures were made in **Python 3.14** (the conda `p314` environment) with **pandas** (data wrangling), **NumPy**, **matplotlib** (all plotting, layout, annotation), and **seaborn** (only for its "mako" colour ramp in Visualization 3). There were no manual steps: each figure is produced by one script in `work/`, and `work/README.md` explains how to regenerate them. Fonts: Helvetica Neue (Arial Unicode MS as a fallback for symbols).

**Data processing.**
- *World Bank life expectancy (Q1):* reshaped male/female/both into one row per country-year and computed the gap as female − male. Dropped the 49 World Bank regional/income aggregates (217 countries remain). Binned by overall life expectancy (2-year bins; medians shown only for bins with ≥60 country-years). Smoothed trails with a 3-year rolling mean. The heatmap uses 1960–2019 means per country per bin, so COVID spikes don't create peaks. The 43 heatmap countries were chosen by me to cover all regions.
- *Our World in Data long-run life expectancy (Q3):* dropped regional aggregates (entities without codes, and OWID_ codes). For each country, found the first year it reached 50 and 70 by linear interpolation between observations, accepted only when the observations either side were ≤10 years apart. Countries already ≥50 at their first observation were excluded (160 countries remain). Computed Kaplan–Meier curves by hand (no survival-analysis library) for six groups based on when each country reached 50.
- *USDA county data (Q2, Q4):* read the county CSV (latin-1 encoding). Removed US/state summary rows (FIPS ending in 000), Puerto Rico (no population-component data), and 17 retired Alaska/Connecticut units with no 2023 code, leaving 3,106 counties. Q2: summed natural change, domestic and international migration and total change over 2021–2023, divided by the July 2020 population estimate, ÷3, ×1000. Group rates are weighted by population (sums ÷ sums). Q4: unemployment rate per group = sum of unemployed ÷ sum of civilian labour force for each year. 2023 RUCC codes are applied to all years. No outside data was added; the meanings of the RUCC codes are general knowledge of the USDA classification.

**AI disclosure.** These visualizations, the data-processing code, and the written answers (including the critique) were produced by an AI agent, **Claude (Anthropic) running in Claude Code**, from my instructions. It chose the stories, wrote and ran the Python scripts, checked each rendered figure and revised the layouts, and drafted all of the text above (including the critique). *[Student: edit this paragraph to describe accurately what you did yourself and how you used the AI. The course GenAI policy asks that the critique and the work come from you, with the AI credited for its help.]*
