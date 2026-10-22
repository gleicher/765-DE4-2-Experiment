# DE 4-2 answers (numbered to match the Canvas survey questions)

> **Note before pasting (not part of any answer):** The course GenAI policy
> (reference/genai-policies.md) says the work you turn in should come from you, the critique
> (Q1) should be your own opinion, and AI help must be disclosed. Everything below, including the
> figures, was drafted by an AI assistant (Claude). Q20 discloses that. If you rewrite or change
> things yourself, update Q20 so it still describes accurately who did what.

---

## 1. Critique (not part of the CLO)

**Design critiqued:** "Income inequality varies across states", a dot-and-line (dumbbell) chart of
the highest and lowest county median household income (2021) in 16 selected states, labeled with
the max/min ratio.

**What works.** The dumbbell is a good fit for a range comparison: each state's spread is one
vertical segment, and the two colored endpoints separate "richest county" from "poorest county"
right away. Sorting the states by the ratio gives the chart a clear direction from left to
right, and printing the ratio above each bar gives the exact numbers without making the reader
read them off the axis. The caption explains the encoding and the selection rule (top 5, bottom 5,
plus 6 others), which is honest about the subsetting.

**Problems.**
1. *The measure doesn't match the claim.* The max/min ratio of county medians says more about
   **how many counties a state has** and how different its extremes are than about "income
   inequality". Wyoming (23 counties), Delaware (3 counties) and Alaska score "equal", while
   Virginia (133 counties and independent cities, including very rich D.C. suburbs and poor
   Appalachian counties) and Texas (254 counties) score "unequal". The range of a sample grows with
   the sample size, so this ranking is largely a county-count ranking. It also ignores population:
   a county of 1,000 people counts as much as one of 1 million. A population-weighted spread such
   as an interquartile range, or showing every county as a dot, would be a fairer test of the
   claim. At minimum, the title should say "range of county median incomes", not "inequality".
2. *The sorting key isn't the visual key.* The states are ordered by ratio, but the eye reads
   segment **length** (the dollar difference). Alabama (2.83×, about $55K apart) has a much shorter
   segment than California (2.77×, about $90K apart), and Florida (2.08×) has a shorter segment
   than Washington (1.96×), so the picture and the order disagree. Either plot the ratio itself (e.g., a log-scale y-axis,
   where equal ratios have equal lengths) or sort by the difference.
3. *Labels and details.* The state labels hang below the orange dots at different heights while
   the same abbreviations appear on the x-axis, so they are redundant and cluttered. "Measure
   Names: Max./Min." is leftover Tableau UI text and should read "Richest county / Poorest county".
   The "State" header at the top is also tool chrome. Starting the axis at 0 isn't required for a
   dot plot and leaves a lot of empty space below $30K. Blue/orange is a safe choice for color
   vision deficiency, but the orange dots carry the labels, which pulls attention to the
   minimums.
4. *Selection.* "6 additional interested states" is arbitrary. The viewer can't tell whether the
   middle states are representative. Showing all 50 states (it fits as a horizontal dot plot)
   would remove the cherry-picking question and let readers find their own state.

**Overall:** a standard design (SD) built with care (sorted, annotated, captioned), but the story
it claims (inequality) isn't what it measures (range of county medians, driven by county count),
and its sort order doesn't match what the eye compares. The fixes are a different statistic,
log scale or sort-by-length, cleaned-up legend text, and all states.

---

## 2. Story / Question 1 (Life Expectancy)

Women outlive men in nearly every country. Has that female advantage changed since 1960, and is
it the same everywhere? (Answer: the typical gap has held at about 4–5 years, but South Asia
started with men outliving women, the former Soviet bloc grew 10–14 year gaps, and wars cause
short spikes.)

## 3. Visualization 1 (primary)

`answers/figures/q1a_gender_gap_lines.png`

## 4. Rationale (Q1 primary)

- **Encode the story variable directly.** The question is about the *gap*, so I computed
  female − male life expectancy and plotted that one number instead of two lines per country.
  A zero line, labeled "below 0 = men outlive women", turns the sign of the gap into a visible
  threshold.
- **Show everyone, emphasize a few.** All 217 countries are drawn as faint gray lines, so the reader
  sees the full spread and the outliers (war spikes) without a legend. On top of them, a gray band
  (middle 50% of countries) and a black median line give the "typical" answer: flat at around 5
  years. Three countries are drawn in color because each one is a different kind of exception:
  Russia (gap far above typical), India (starts below zero and crosses it), and the United States
  (a familiar reference whose gap narrowed). Keeping to three colors keeps them distinct, and the
  palette was checked for color-vision-deficiency separation.
- **Direct labels, no legend.** Each highlighted line is labeled at its right end, with short
  leader lines so the labels don't collide.
- **Annotations carry the story.** Short notes explain the exceptions: Russia 1994 (post-Soviet male
  mortality crisis), India's crossing around 1982, and the largest war spikes (Cyprus 1974,
  Bosnia 1993, Ukraine 2023). I used background knowledge only to *label* these events, not as
  added data.
- **Title states the finding**, the subtitle states what is plotted, and the caption gives the key
  numbers (median 4.1 → 5.0; five countries below zero in 1960, none in 2023) and the data source,
  so the image stands alone.
- Regional and income aggregates (e.g., "World", "High income") were removed, so every line is a
  country.

## 5. Visualization 2 (alternate)

`answers/figures/q1b_male_vs_female_paths.png`

## 6. Rationale (Q1 alternate)

- **A different encoding of the same story:** male life expectancy on x and female on y, with
  equal scales. The gap becomes the distance above the solid diagonal (women = men), and dashed
  guides mark +5, +10 and +15 years. This keeps *both* sexes' levels visible, which the gap chart
  hides.
- **Connected-scatter paths for the same three countries** (same colors as Viz 1, so the two
  pieces read as a pair) show *how* each gap changed. Russia's path loops left (men's life
  expectancy fell from about 64 to 58 while women's held near 72), so its gap grew because men
  lost ground, not because women gained. India's path starts below the diagonal and crosses it.
  The U.S. path runs nearly parallel to the diagonal. Squares mark 1960, large circles 2023, and
  small dots each decade, so direction and speed can be read.
- **Context without clutter:** every other country is a small gray dot, hollow for 1960 and filled
  for 2023. The shift up and to the right, with every 2023 dot above the diagonal, shows the global
  pattern at a glance.
- Labels with leader lines give the exact values at the key points (e.g., Russia 1994: men 57.6,
  women 71.7). A "how to read" note sits in the empty lower-right area. The axes start at 40
  rather than 0 to give the data more room; this is fine because position, not length, encodes
  the values.

## 7. Compare the two Q1 visualizations

- **Viz 1 (gap over time)** is the better *answer to the question as asked*. Time is explicit, the
  typical gap and its spread are easy to read (flat band near 5), and the outliers and their timing
  (1974, 1993, 1994, 2023) stand out. Its weakness: a gap alone can't tell you *why* it changed.
  Did men get worse or women get better? It also needs a derived quantity (female − male) that a
  general reader must be told about.
- **Viz 2 (male vs. female paths)** shows the mechanism. Russia's gap grew because men's life
  expectancy fell, and India's flipped because women's rose faster. It also keeps the absolute
  levels, so you see that the gap grows as countries get longer-lived. Its weaknesses: time is
  only implicit (along the path), reading distance-from-diagonal takes more effort than reading a
  y-value, small gap differences (4 vs. 5 years) are hard to see, and only a few paths can be shown
  before it becomes a tangle. Viz 2 suits a more analytical audience. Viz 1 is the one for a
  general reader.

---

## 8. Story / Question 2 (Census)

How did the 2020 pandemic change unemployment in urban vs. rural U.S. counties, and did the
difference last? (Answer: for 20 years rural counties had higher unemployment than big metros;
in 2020 the order flipped, with the largest metros spiking most, and by 2022 every type of county
was back to about the same rate.)

## 9. Visualization 1 (primary)

`answers/figures/q2a_unemployment_rural_urban_lines.png`

## 10. Rationale (Q2 primary)

- **Aggregate correctly.** For each of five rural–urban groups (USDA 2023 Rural-Urban Continuum
  Codes 1 | 2–3 | 4–5 | 6–7 | 8–9) I summed unemployed persons and labor force across counties and
  divided, giving each group's true unemployment rate. Averaging county rates would let a
  1,000-person county count as much as Los Angeles.
- **Ordinal groups → one-hue ramp.** Rurality is ordered, so the five lines use light → dark blue
  (most rural lightest, largest metro darkest) instead of unrelated hues. The two ends of the scale
  (the comparison in the title) are drawn thicker and labeled in bold. Labels sit at the 2020 peak,
  where the order of the lines *is* the story.
- **The 24-year window gives context:** the Great Recession (when all groups rose together) is a
  natural comparison for the pandemic. Both periods are shaded and labeled.
- **The bottom panel makes the flip explicit:** large-metro rate minus most-rural rate, as bars
  around zero. The five lines are close together in most years. The difference panel shows the
  sign change in 2020–21 at a glance, and its two colors repeat the dark/light identity of the two
  groups.
- Title gives the finding, the caption gives the numbers (3.5% → 8.6% vs. 4.2% → 6.5%) and
  the method notes (code groups, Connecticut's change from counties to planning regions, data
  source).

## 11. Visualization 2 (alternate)

`answers/figures/q2b_unemployment_county_strips.png`

## 12. Rationale (Q2 alternate)

- **Show the counties, not just group totals.** Each of 3,102 counties is a dot, placed by its
  change in unemployment rate (2019 → 2020), in five rows by rurality (same blue ramp as Viz 1).
  Jitter spreads overlapping dots, and dot area is proportional to labor force, so the large
  urban labor markets stand out (Los Angeles +7.8, Cook +6.7 points) while small counties stay
  visible.
- A black bar (middle 50%) with a median tick and value summarizes each row, so the
  group-to-group shift (+3.4 for large metro down to +1.8 for rural) is readable on top of the
  cloud.
- **The second panel answers "did it last?"** It shows the change 2019 → 2022 on the *same
  horizontal scale* (the panel is narrower because its range is smaller), so the collapse back to
  zero can be compared directly with the spike.
- Zero lines in both panels anchor "no change". The x-axis label states that positive = worse. A
  key under the subtitle explains dot size and the bars. Dots beyond the axis range are pinned to
  the edge (noted in the caption) rather than dropped.

## 13. Compare the two Q2 visualizations

- **Viz 1 (group lines + difference bars)** tells the story over time. The reader sees that the
  rural-higher pattern held for 20 years, *including* the Great Recession, which makes the 2020
  reversal surprising. It's precise and compact, but it hides the variation inside each group: a
  line for "rural" could be a few counties with huge spikes or all counties rising a bit.
- **Viz 2 (county strips)** shows that the shift is a shift in the *whole distribution*. Most
  large-metro counties rose 2–5 points while many rural counties barely moved, so the result isn't
  driven by a few outliers. It also shows the wide overlap between groups (rurality explains part of
  the story, not all of it). It loses the long-run context. Only 2019, 2020 and 2022 appear, so
  the "rural used to be worse" half of the story is gone. It's also denser to read and is best for
  an analytical audience. Viz 1 is better for a general audience.

---

## 14. Story / Question 3

After 2020, did Americans move away from big counties, and did immigration offset the loss?
(Census data: net domestic vs. net international migration, mid-2020 to mid-2023, by county
population size.)

## 15. Visualization 3

`answers/figures/q3_migration_by_county_size.png`

## 16. Rationale (Q3)

- **Grouping by county population (9 size classes)** turns 3,100 noisy county values into a clear
  gradient from smallest to largest. I summed people within each class, so the bars are real
  numbers of net migrants, which answers "where did people go?"
- **Paired horizontal bars around a zero line.** Domestic (orange) and international (blue) bars
  side by side in each row show the opposite pattern: domestic migration goes from positive to
  strongly negative as counties get bigger, while international migration grows with size. The
  zero line makes gains vs. losses obvious, and the rows run small → large from top to bottom.
  Color here marks identity (two kinds of migration), not good/bad.
- **Counts and rates together.** Bars show totals (so the 1.5 million net domestic loss from the 16
  counties of 2M+ people is visible), and a small table on the right gives rates per 100 residents
  plus the number of counties per class, so readers can see that the effect is not just "bigger
  counties have more people".
- Two annotations state the headline numbers (−2.8 M domestic and +1.8 M international for
  counties of 500k+), and the title states the conclusion ("refilled them only partly").
- The caption explains the July–June migration year and the time window. The 2020 column was left
  out because it only covers April–June 2020.

## 17. Story / Question 4

How long did it take countries to climb from a life expectancy of 50 to 70 years, and did
countries that started later climb faster? (OWID long-run data.)

## 18. Visualization 4

`answers/figures/q4_climb_50_to_70.png`

## 19. Rationale (Q4)

- **Derived variables that answer the question.** For each country I found the first year its life
  expectancy reached 50 and the first year it reached 70, interpolating between observations
  because historical series are irregular. The scatter plots *when the climb started* (x) against
  *how long it took* (y). The long OWID history (back to the 1700s for some countries) makes this
  question possible.
- **Handle countries that haven't arrived.** Countries still below 70 can't be dropped (that would
  bias the result toward success), and they can't be plotted as finished. They're drawn as hollow
  orange triangles at "years so far", which places them exactly on a dashed line that marks 2023.
  The line is labeled, so the reader can see that these countries' true times can only be longer.
  This censoring is the second half of the story ("has stalled for others").
- **Selective labels.** About 14 countries are named with their year counts, chosen as reference
  points (Norway, Sweden, U.S.), extremes (Japan 17, Oman 19, Philippines 73) and the populous
  latecomers (China, India, Bangladesh, Nigeria). Named points let the reader connect the pattern
  to places they know without labeling all 173.
- An in-plot note and the caption give the before-1925 vs. mid-century ranges and the "6 of 45"
  fact. The caption also explains the interpolation and that early dates are approximate.

## 20. How I made these visualizations (tools, processing, AI disclosure)

**AI disclosure:** These visualizations, the code that produced them, and the drafts of these
written answers (including the critique) were produced by an AI coding assistant, **Claude
(Anthropic), running in Claude Code**, working from my copies of the assignment pages and the
course data files. The AI chose the stories, wrote the analysis and plotting code, made the
figures, and drafted the rationales.

**Tools:** Python 3.14 with pandas (data processing) and matplotlib (all charts), in a conda
environment. A palette validator script (part of the assistant's data-visualization guidance) was
used to check the categorical colors for color-vision-deficiency separation. All scripts are in
`work/` (one script per figure plus a shared `common.py`), and the figures can be regenerated by
running them. No manual editing of the images.

**Data processing:**
- *World Bank life expectancy* (Q1): reshaped Female/Male/Both rows into one row per
  country-year. Gap = Female − Male. Removed regional and income aggregates by their World Bank
  codes (e.g., WLD, HIC, SSF), leaving 217 countries.
- *USDA county data* (Q2, Q3): read the file as Latin-1, dropped state and national summary rows
  (FIPS ending in 000) and Puerto Rico. Grouped counties by 2023 Rural-Urban Continuum Code
  (falling back to the 2013 code for Connecticut's eight former counties, which carry the
  labor-force data). Group unemployment rate = sum of unemployed / sum of labor force. Q2 alt uses
  each county's own rate change. Q3 sums 2021–2023 domestic and international migration (July
  2020–June 2023) and divides by the 2020 population estimate for rates. Counties are grouped into
  9 population classes.
- *OWID life expectancy* (Q4): kept entities with ISO country codes (plus Kosovo), dropped
  aggregates. Computed the interpolated first year reaching 50 and 70 for the 173 countries whose
  first recorded value was below 50. Countries not yet at 70 are shown as censored (years
  climbing through 2023).
- No outside data was added. Event names in annotations (e.g., post-Soviet mortality crisis,
  HIV/AIDS, wars) come from general knowledge.
