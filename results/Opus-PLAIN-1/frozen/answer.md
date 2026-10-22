# Design Exercise 4-2: Answers (numbered to match the Canvas survey)

Figures are in `answers/figures/`:

| Canvas Q | File |
|---|---|
| 3 | `figures/q1a_pandemic_setback_small_multiples.png` |
| 5 | `figures/q1b_pandemic_setback_scatter.png` |
| 9 | `figures/q2a_population_change_components_bars.png` |
| 11 | `figures/q2b_population_change_components_heatmap.png` |
| 15 | `figures/q3_education_urban_rural_gaps.png` |
| 18 | `figures/q4_life_expectancy_50_to_70.png` |

---

## 1. Critique (not part of the CLO)

**The design.** A dumbbell chart ("Income inequality varies across states"). For each of 16 states it plots the highest and lowest county median household income (2021), joins them with a gray bar, labels the max/min ratio above each pair, and sorts the states by that ratio.

**What works (good).**
- The dumbbell form fits a two-values-per-category comparison, and sorting by the ratio makes the ranking easy to read from left to right.
- The ratio labels give the exact number the title is about, and the caption tells you how to read the chart and states the main finding (WY lowest, VA highest).
- The y-axis starts at zero, the gridlines are light, and the clean layout lets the dots stand out.

**What is ugly (weak choices).**
- **The encoding doesn't match the measure.** The story is the *ratio* max/min, but the chart shows absolute dollars on a linear scale, so the most visible feature, bar length, is the *difference*. On a linear axis CA (2.77x) gets a longer bar than AL (2.83x), and NH's bar (1.15x) is visibly longer than DE's (also 1.15x). The ratio is carried only by the small text labels. Plotting income on a log scale would make bar length match the ratio, and the sort order would then show up visually, not just in the numbers.
- **Selection.** "Top 5, bottom 5 and 6 additional interested states" is arbitrary, and the reader can't tell which states belong to which group. Showing all 50 states (a dumbbell chart with 50 rows fits on a page) would avoid the cherry-picking.
- **Leftover tool defaults.** The legend title "Measure Names" with "Max./Min.", the "State" header, and the lack of a legend tied to the ratio labels all look like unedited Tableau. The blue/orange identity legend could be replaced by direct labels ("highest county", "lowest county") on the first pair. The state labels move between the bottom of the bar and the axis, which is redundant.
- **The title is vague.** "Income inequality varies across states" doesn't say what was found. Something like "Virginia's richest county earns 3.8x its poorest; Wyoming's barely differs" states the result.

**What is bad (likely wrong or misleading).**
- **The measure is mislabeled.** The max/min ratio of *county medians* measures how much counties within a state differ, not "income inequality" (which concerns how income is distributed among households). It is also driven by a single extreme county and grows with the number of counties: Delaware has 3 counties and Texas has 254, so the comparison is biased before any data is shown.
- **The data look wrong.** A 1.01x ratio across Wyoming's 23 counties (and 1.12x across Alaska's ~30 boroughs) is implausible. In this year's county file, the 2022 medians give WY ≈ 2.4x, AK ≈ 2.7x and ND ≈ 2.1x, so the three "most equal" states are probably a filtering or aggregation error. When the headline result depends on an outlier like that, the designer should check the data before publishing.

**Suggested redesign.** Show all states as a dot or dumbbell chart on a log-income axis, sorted by ratio, and mark each state's county count, or use a measure that is less sensitive to outliers (such as the 90th/10th percentile county). Keep the good caption.

---

## 2. Story/Question 1 (Life Expectancy)

How far back did the COVID-19 pandemic push each country's life expectancy, measured in *years of progress erased*, and had countries recovered by 2023? In some countries (Jamaica, Cuba, Mexico, Paraguay, the US) the 2020–22 low matched levels last seen 20–39 years earlier, yet 184 of 214 countries were back at or above their 2019 level by 2023.

## 3. Visualization 1 for Question 1

`figures/q1a_pandemic_setback_small_multiples.png`

## 4. Rationale (Q1, visualization 1)

- **The key idea is a derived measure that turns a drop into time.** A 3-year drop in life expectancy is abstract. "Back to 1992" is concrete. For each country I find the lowest value in 2020–22 and the latest earlier year that was at or below it. The orange arrow draws that move literally, a horizontal line from the pandemic low back along the country's own history, so the viewer sees "erased decades" instead of reading it.
- **Small multiples of line charts** (one country per panel) keep each history readable. Overlaying 16 lines would make the arrows impossible to follow.
- **Selection and ordering serve the story.** The 16 panels are the countries that lost at least 2 years and were pushed back furthest, sorted by years erased. The criterion is stated in the caption so it doesn't look cherry-picked.
- **Every panel spans the same 13 years on the y-axis** (each with its own offset), so the depth of the dip and the slope of earlier progress can be compared across panels even though the levels differ (Fiji ~65, Andorra ~84).
- **Color is used sparingly and means one thing each:** black for the history and the 2019 point, orange only for the pandemic low and the arrow, blue for 2023. The first panel labels the three dots directly, so no separate legend is needed.
- **Each panel has a one-line text summary** ("lost 3.1 yrs of life exp. = 37 yrs of progress"), so the exact numbers are there without crowding the plot.
- The caption explains a nuance the figure shows: countries whose progress had stalled (Jamaica, Cuba) lose many "years of progress" for a modest drop. It also documents the exclusion (Central African Republic's implausible series) and the source.

## 5. Visualization 2 for Question 1

`figures/q1b_pandemic_setback_scatter.png`

## 6. Rationale (Q1, visualization 2)

- **The view covers every country** rather than a selection: one dot for each of 214 countries. This answers "how common?" directly, which the small multiples can't.
- **The two axes are the two sides of the setback.** x = life expectancy lost (2019 minus the 2020–22 low); y = years of progress erased. Putting them against each other shows that they are related but not the same, which is the interesting part. The callout points out that Botswana's larger 3.9-year drop erased only 4 years of (rapid) gains, while Jamaica's 2.4-year drop erased 39 years of slow progress.
- **Color encodes the recovery question** with only two categorical hues: blue = back at or above 2019 by 2023, orange = still below. Counts are given in the legend and the subtitle.
- **Labels are selective:** about 20 countries, chosen as extremes or as familiar reference points (US, India, Russia, Japan), each with a dark ring so it's clear which dot the label belongs to. Every other dot is unlabeled.
- **The vertical zero line** separates countries with no pandemic drop. Years erased are integers, so dots are jittered vertically by at most ±0.35 years, and the caption says so.

## 7. Compare the two Question 1 visualizations

- **Small multiples (1):** *Pros:* the "back to year X" idea is shown, not just stated. Each country's whole trajectory gives context (Bosnia's and Lebanon's war-era crashes, Bulgaria's 1990s stagnation), and recovery is visible as the climb to the blue dot. It works well for a general audience. *Cons:* it covers only 16 hand-picked (if rule-based) countries, so it can't show how typical this was, and comparing values across panels means reading separate axes.
- **Scatter (2):** *Pros:* complete and quantitative. Every country, both measures, and recovery status appear in one view. It shows how common setbacks were (74 countries lost ≥10 years of progress) and that loss and setback are different things. *Cons:* "years of progress erased" is abstract here because the arrow-through-history idea is gone, so the viewer has to trust the definition in the axis label. It also hides the trajectories and shows recovery only as yes/no.
- In short, (1) explains the concept and makes the story memorable, and (2) shows its extent. I'd lead with (1) for a newspaper audience and use (2) for a report or journal.

---

## 8. Story/Question 2 (Census)

Where does population growth come from in different kinds of US counties? From mid-2020 to mid-2023, the largest metros (1M+) lost residents to domestic migration and grew only through births and immigration. Rural and small-town counties had more deaths than births every year and depended on people moving in from elsewhere in the US, which happened mostly in counties next to a metro.

## 9. Visualization 1 for Question 2

`figures/q2a_population_change_components_bars.png`

## 10. Rationale (Q2, visualization 1)

- **Diverging stacked bars** are the natural fit for "components that add up to a net change, some positive and some negative." Gains extend right of zero and losses extend left, so the sign of each component is read from position, and the black diamond shows where they net out. The net value is also printed in a right-hand column.
- **Rows are the nine USDA Rural-Urban Continuum codes in their natural order** (most urban to most rural), split into labeled Metro and Nonmetro groups, so the change from top to bottom is the story. Under each row label, gray text gives the number of counties and the population, a reminder that the 1M+ metros hold 188M people and the most remote rural class holds 4.5M.
- **Rates per 1,000 residents (population-weighted totals)** make county classes of very different sizes comparable. Weighting by population avoids letting thousands of tiny counties dominate.
- **Three years combined (July 2020 – June 2023)** gives a stable picture. The year-by-year version is visualization 2.
- **Color:** three distinct categorical hues for the three components (identity, not magnitude), with white gaps between segments. The legend sits under the chart, and short direct callouts state the three findings (big metros, remote vs. adjacent, rural natural decrease) right next to the bars they describe.
- The title states the finding, not just the topic.

## 11. Visualization 2 for Question 2

`figures/q2b_population_change_components_heatmap.png`

## 12. Rationale (Q2, visualization 2)

- **A heatmap with a diverging color scale** (orange = losing people, blue = gaining, neutral gray-white = zero) shows the same three components year by year, plus a net-change block. It shows that the pattern holds in every year rather than being an artifact of adding up three years.
- **Layout:** rows are the same nine county classes (with shorter labels and a metro/nonmetro divider). Columns are grouped by component, with the three years side by side inside each group, so the eye can read across years (consistency) or down rows (the urban-rural gradient).
- **Each cell shows its value** because a heatmap is partly a lookup table and color alone is hard to read precisely. The net columns are in bold. The diverging scale is symmetric and capped at ±9 so the zero midpoint stays neutral and loss/gain read as opposites.
- It shows things the bar chart can't: big metros' domestic losses shrank each year (−3.9 → −2.8) while international migration tripled (+1.5 → +4.6), turning the 1M+ metros' net change from negative in 2020–21 to +4.7 in 2023. Natural decrease in rural counties appears every year.
- The caption explains the census July–June year convention and the RUCC definitions.

## 13. Compare the two Question 2 visualizations

- **Bars (1)** make the main contrast obvious at a glance. Length and direction show which components push up and which push down, and the diamond shows the net, so a general reader gets "metros grow from births + immigrants, rural from movers" in seconds. But it collapses three years into one number, and reading the exact value of a middle segment in a stacked bar is hard.
- **Heatmap (2)** adds time and precise values, and shows consistency (or change, as with immigration's rise) across years. Its weakness is that color is a less accurate channel than length, so the viewer has to read the numbers to compare closely, and it doesn't show how the components add to the net (the net is a separate block rather than the sum the viewer sees). It's denser and better for an analytic audience.
- Both use the same row order and the same orange-for-loss / blue-for-gain logic, so they can be shown together: (1) as the headline and (2) as the supporting detail.

---

## 14. Question/Story for Visualization 3

Has the education gap between urban and rural America closed or widened since 1970? It depends on the level. The rural shortfall in high-school completion has almost disappeared (a 16-point gap became 2 points), but the college gap tripled (from 7 to 21 points), as big metros pulled far ahead.

## 15. Visualization 3

`figures/q3_education_urban_rural_gaps.png`

## 16. Rationale (Visualization 3)

- **Two panels, side by side, with a shared y-axis (0–65%)** so that the two gaps are compared on the same scale. The contrast between the two panels is the story: the left gap narrows, the right gap widens.
- **Line charts** for change over six survey periods, with x positions at the real years (the 5-year ACS periods at their midpoints), so the irregular spacing doesn't distort rates of change.
- **Four county groups** (large metro; smaller metro; nonmetro with a town of 5k+; rural), made from the 9 RUCC codes, keep the chart readable. Because the groups are ordered, I used a single-hue blue ramp (dark = most urban) instead of unrelated hues, so the order of the lines matches the order of the legend.
- **The shaded band between the most urban and the most rural line is the gap itself**, with orange double-headed arrows and the gap in points at 1970 and 2019–23. That makes the "16 → 2" vs. "7 → 21" comparison something you see, not something you work out.
- The lines are direct-labeled at the right end (no separate legend box), and a short annotation in each panel states its finding. The caption covers the definitions (1970/80 "four years of college", fixed 2023 RUCC codes, population weighting).

---

## 17. Question/Story for Visualization 4

Did countries that started later climb from a life expectancy of 50 to 70 faster than the pioneers? Mostly yes. The early countries (Norway, Sweden, the US) needed 45–95 years, while later ones often did it in 17–40 (Japan 17, South Korea 32, China 32). But 58 countries that reached 50 have still not reached 70, some after 60+ years, so catching up was not guaranteed.

## 18. Visualization 4

`figures/q4_life_expectancy_50_to_70.png`

## 19. Rationale (Visualization 4)

- **This is a derived "time to milestone" view** rather than another set of life-expectancy lines. Using the long historical OWID series, I interpolate the year each country first reached 50 and 70. The scatter puts *when* a country started (x) against *how long* the climb took (y), which turns 160 long, irregular time series into one readable pattern: the cloud slopes downward from the 19th-century pioneers to the post-war fast followers.
- **Censoring is shown, not hidden, which I think is the most important design decision.** Leaving out countries that haven't reached 70 would make late starters look faster than they really are. Instead, those 58 countries appear as hollow orange circles at "years so far" with small up-arrows (meaning "at least this long"). They all sit on the diagonal "data end in 2023" line, and the region above it is shaded as not yet observable. This makes the limit of the data part of the picture, and shows the second half of the story: a large group (many in southern Africa) has been stuck for 50–70 years.
- **Encoding:** position for both quantities. Filled blue vs. hollow orange separates "finished" from "still climbing" by both color and shape, so it doesn't rely on color alone. About 20 labels are chosen for famous or extreme cases.
- **Three short annotations** (pioneers, fast followers, still waiting) guide the reader through the pattern. The caption states the inclusion rules (observations at most 10 years apart around each crossing; countries already above 50 in their first record are omitted).
- This adds variety to the set: Q1 uses small multiples and a scatter, Q2 diverging bars and a heatmap, Q3 paired line charts, and Q4 is an adapted scatter with censored data.

---

## 20. How I made these visualizations

**Tools:** Python 3.14 with pandas and numpy for data processing and matplotlib for all six figures. Each figure is produced entirely by a script (no manual editing). The scripts are in `work/`, and `work/make_all.sh` regenerates every figure. **AI disclosure:** this assignment was done with an AI coding agent, Claude Code (Anthropic Claude). It explored the data, proposed the stories, wrote the analysis and plotting code, made the figures, and drafted this text, including the critique. Before submitting, I need to review, check, and revise these answers so the work reflects my own judgment, as the course GenAI policy requires.

**Data processing:**
- *Life expectancy (World Bank, Q1):* removed regional and income aggregates by keeping only codes that OWID uses for real countries. Used both sexes. For each country I computed the 2019 value, the minimum in 2020–22, the latest pre-2019 year with a value at or below that minimum ("setback year"), and the change from 2019 to 2023. Central African Republic was excluded because its series is implausible (31.5 → 50.6 → 18.8 → 57.4).
- *Life expectancy (OWID, Q4):* countries only. The first year at or above 50 and at or above 70 is linearly interpolated between the bracketing observations, accepted only if they are at most 10 years apart and the country has a recorded value below the threshold. Countries that reached 50 but not 70 by 2023 are kept as right-censored.
- *Census (Q2, Q3):* the county file is actually comma-separated and Latin-1 encoded. I kept only county rows (dropping the state and US summary rows), for the 50 states + DC (Puerto Rico excluded), and grouped counties by the 2023 Rural-Urban Continuum Code. Q2: summed natural change, domestic migration and international migration for 2021–2023 (census years run July–June) and divided by the group's starting population, per 1,000. Q3: summed education counts by group for 1970–2019/23 to get population-weighted shares (1970/1980 "four years of college" stands in for "bachelor's or higher"), using 2023 codes for all years. No outside data were added.
