# Design Exercise 4-2: answers (numbered to match the Canvas survey)

Figure files are in `answers/figures/`. Each is a single-page PNG with its own title, labels, legend and caption.

---

## 1. Critique (not part of the CLO)

The design to critique is the Tableau dot-and-line chart titled "Income inequality varies across states" (county median household income, 2021, maximum vs minimum within 16 states).

**What works.** The dumbbell form is a sensible choice for showing a range: the vertical gray line makes the spread easy to compare across states, the y axis starts at zero so the length of each line is honest, and the "1.01x ... 3.78x" labels turn the spread into a single readable number. The caption states the idea in plain words.

**What does not work.**
1. *The title claims more than the chart shows.* A max-to-min ratio of county median incomes is not income inequality. It says nothing about how unequal households are within a county, and it is driven by two single counties per state (often tiny ones, or in Virginia an independent city next to a wealthy suburb). That is a statement about geographic disparity in median income, and the title and caption should say so.
2. *No population weighting or context.* A county of 2,000 people counts as much as one of 2,000,000, so the extremes are probably the least representative counties. The chart gives no hint of how many people live in the highest and lowest counties, or how many counties each state has (Wyoming and Delaware have very few, so a small ratio is nearly guaranteed).
3. *The selection is arbitrary and hidden.* "Top 5, bottom 5, and 6 additional interested states" appears only in the fine print. The reader cannot tell why NY, FL or IL are present, and the x axis is silently sorted by ratio, which is not labeled. A reader may think the states are in a geographic or alphabetical order.
4. *Encoding redundancy and clutter.* The ratio is encoded three ways (line length, vertical position and a text label), while the thing the title is about, the ratio, has no encoding of its own that can be compared directly. Because the lines start at different heights, comparing ratios by eye is hard: a 2x ratio at a high income level looks longer than a 3x at a low one. Plotting the ratio (or log of income) would fix this.
5. *Label and legend problems.* "3.78x" collides with the VA dot, the "1.01x" label sits on top of the WY marker, and the legend title "Measure Names" is the Tableau default and would mean nothing to a reader. Blue and orange are used for max and min with no semantic reason, and the large empty area below 30K wastes about a fifth of the plot.
6. *Presentation.* The image is very tall and the caption is a long paragraph beneath the axis; a short subtitle that gives the finding ("the richest county in Virginia has 3.8 times the median income of the poorest") would do more work.

**How I would improve it.** Sort and label states by the ratio, plot the ratio (or both on a log scale), show all states in a small, light form with the selected states emphasized, use a population-weighted spread such as the 90th to 10th percentile of residents rather than the two extreme counties, and retitle it "Median income varies widely between counties within a state."

---

## 2. Story / Question 1 (Life Expectancy)

Is the female advantage in life expectancy a stable fact of nature? Using the World Bank sex-specific data for 1960 to 2023, how has the female-minus-male gap moved in different countries, and where did it grow or shrink the most?

## 3. First visualization for Story 1

Upload `answers/figures/fig1a_gender_gap_trajectories.png`

## 4. Rationale for visualization 1

The question is about change over time for many countries at once, so I plot the gap (female minus male life expectancy at birth) as a line for every one of 215 countries, in light gray, so the viewer sees the whole distribution and its narrow central band. I then lift out one thick black line for the median country and seven colored lines for countries that carry the story: Russia and Ukraine (largest gaps), India, Pakistan and Bangladesh (negative gaps that turned positive), and the United States and Japan as familiar reference points. This is a focus-plus-context strategy: the gray lines show that the selected countries are genuinely unusual, and the colored ones give the reader something to hold on to. I plotted the gap directly rather than two life expectancy curves, because the question is about the difference, and a difference is hard to judge from two separate lines. A zero line with a tinted band for "men outlive women" makes the sign change obvious, and I labeled each highlighted line at its right end with its 2023 value, avoiding a legend that would force looking back and forth. Annotations mark the two clearest events (the Russian peak of 14.2 years in 1994 and India's deficit until the early 1980s). I removed World Bank aggregates (regions, income groups) because they are not countries and would double count, and I note in the caption that single-year spikes (for example 1971 for Bangladesh and Pakistan) are war-year estimates. Colors are chosen to be distinguishable under color vision deficiency and carry no meaning beyond identity; the title states the finding.

## 5. Second visualization for Story 1

Upload `answers/figures/fig1b_gender_gap_arrows.png`

## 6. Rationale for visualization 2 (Question 1 alternate)

The alternate answers the same question with a different encoding: instead of the whole time path, it compares only two moments, 1960 and 2023, for 31 selected countries. Each country is a row, an open circle marks the 1960 gap, and an arrow ends at the 2023 gap, so the length and direction of the arrow is the change. Color gives a redundant direction code (rust for widened, blue for narrowed, gray for within 0.5 years), and the number beside each arrow gives the exact change. Rows are sorted by the 2023 gap so the viewer reads a ranking and the arrows' starting points scatter around it. The zero line separates "men live longer" from "women live longer," which makes India, Pakistan, Bangladesh and Iran visibly cross it. The countries are populous countries plus post-Soviet states and Mongolia, which I chose to keep the figure readable, and I say in the caption that this is a judgment selection. This version is aimed at a general reader, such as a newspaper audience, who wants a ranked list of who changed most.

## 7. Comparison of the two Story 1 visualizations

**Visualization 1 (trajectories).** Pros: shows the whole 63-year path, so you can see when things happened (the 1990s Soviet jump, the slow rise in South Asia, the 2021 dip); shows all countries, so the claim "these are unusual" is checked rather than asserted; the median line gives a reference. Cons: dense, and the gray spaghetti is hard to read for any particular country; only seven countries are identifiable; one-year spikes distract; it takes more effort to read exact values.

**Visualization 2 (arrows).** Pros: very easy to read and rank; exact change printed; the zero crossing and direction of change are immediate; works at small sizes. Cons: only two years, so it hides timing (it cannot show that Russia's gap peaked in 1994 and then fell), and 1960 and 2023 are both affected by single-year noise; only 31 countries appear and the selection is mine; arrows from low to high starting points make it harder to compare the absolute level of change.

Together they are complementary: the first shows when and how, the second shows who and how much. If I could use only one for a general audience it would be the second; for an analyst, the first.

---

## 8. Story / Question 2 (Census)

Did the pandemic change who bears the burden of unemployment? Comparing urban and rural US counties from 2000 to 2023, were rural counties always worse off, and what happened in 2020?

## 9. First visualization for Story 2

Upload `answers/figures/fig2a_unemployment_flip_lines.png`

## 10. Rationale for visualization 2.1

A compound design with two linked panels sharing the same time axis. The top panel is a line chart of the unemployment rate for four county settings (largest metro areas; other metro; small urban nonmetro; rural nonmetro), built by adding up unemployed people and civilian labor force across all counties in the group, so each line is a true rate for the people in those counties instead of an average of county rates (which would give a county of 500 people as much weight as Los Angeles). Collapsing the nine Rural-Urban Continuum Codes to four groups keeps the lines distinguishable, and a sequential dark-to-light blue to orange order encodes how urban each group is, so the viewer sees the ordering without reading a legend. Gray bands mark the Great Recession and the pandemic so the reader can tie the shocks to the lines without outside knowledge. The bottom panel plots the difference, rural minus largest metro, as bars, because the story is about the sign of that difference, which is much harder to see from two nearly parallel lines. Bars are rust when rural is worse off and blue when the big metros are, so the 2020 and 2021 reversal stands out as the only blue bars. I annotated the key numbers (8.6% vs 6.5% in 2020) and added the note that by 2022 the four groups converge at 3.7%. The title states the conclusion.

## 11. Second visualization for Story 2

Upload `answers/figures/fig2b_unemployment_county_change.png`

## 12. Rationale for visualization 2.2

The first chart aggregates counties; this one asks whether the pattern is visible in the individual counties and whether it is unique to the pandemic. It uses two side-by-side strip plots (a jittered dot for every county, about 3,100) on a shared scale, one for the Great Recession (2007 to 2010) and one for the pandemic (2019 to 2020). Rows are the nine Rural-Urban Continuum Codes in their natural order, from big metros to remote rural counties, with thin separators for the metro, urban and rural families. The horizontal position is the change in unemployment rate in percentage points, so the viewer compares the same quantity across rows and across panels. A black bar marks the median county in each row (a robust summary that is not affected by the very large and very small counties) and a diamond marks the labor-force-weighted group change (where the people are). Showing both is deliberate: the median describes the typical county, the diamond describes the typical person, and where they disagree (big metros, where the weighted change is larger) the chart shows why. Semi-transparent small dots keep overplotting readable. The pandemic panel uses the accent color to link it to the "event" color in the first chart. Direct labels give the medians for the two ends of the scale.

## 13. Comparison of the two Story 2 visualizations

**Visualization 2.1 (lines plus gap bars).** Pros: shows 24 years, so the baseline (rural worse for two decades) and the reversal are both visible; the gap panel makes the sign change unmistakable; population-weighted rates mean it reflects people. Cons: it hides variation within a group, so a reader could think every rural county behaved the same; with four groups, the nine-category detail is lost; it shows levels, not how much each county was hit.

**Visualization 2.2 (county strips).** Pros: shows the spread and overlap between settings (many rural counties were hit as hard as some metro counties); compares two downturns directly on one scale; reveals the gradient across all nine categories. Cons: it shows only two start and end years, so it cannot show the baseline or timing; it needs more explanation (median vs weighted); and the key fact, that the order of the *levels* reversed, is only implied through change, not shown directly.

The two supplement each other: 2.1 is the headline, 2.2 is the evidence that it is not an artifact of grouping.

---

## 14. Story / Question 3

Did the growth in college education spread evenly across US counties? Comparing the share of adults with a bachelor's degree in 1990 and in 2019 to 2023 for each county, how did the gap between metropolitan and remote rural counties change?

## 15. Visualization for Story 3

Upload `answers/figures/fig3_college_divergence.png`

## 16. Rationale for visualization 3

This is a compound design with two views of the same data. The left panel is a scatterplot of every county, 1990 on x and 2019 to 2023 on y, with circle area proportional to population and color showing the four settings. A dashed identity line (no change) and two dotted lines (+10 and +20 points) let the viewer read the gain as the vertical distance above the diagonal, which is much easier than comparing two separate histograms; the points almost all lie above the line, so the viewer sees the general rise (only 27 of 3,165 counties lost ground), and the blue circles climbing furthest above the line show where the gains were largest. The right panel summarizes the typical county in each of the nine settings as an arrow from its 1990 median to its 2019 to 2023 median, with the gain printed at the arrowhead, so the ordering from metro to remote rural is explicit. I put the two together because the scatterplot answers "does this hold for individual counties and is it about population?" while the arrows answer "what is the typical difference?" The title and subtitle give the main number: the lead of the typical big-metro county over the typical remote rural county went from 4.1 to 11.4 points, nearly tripling. I label only the most extreme county (Arlington County, VA) to avoid clutter. Color uses the same sequence as the other census figures to keep the visual language consistent.

---

## 17. Story / Question 4

How common are setbacks in life expectancy, and was COVID-19 unusual? Across all countries since 1950, how many suffered a drop each year, and how severe and long-lasting were the biggest ones?

## 18. Visualization for Story 4

Upload `answers/figures/fig4_global_setbacks.png`

## 19. Rationale for visualization 4

I used the Our World in Data series because it covers every country annually from 1950 and has no gaps, so a count of countries per year is fair. The design is two stacked panels sharing a year axis. Panel A is a bar chart of how many of 236 countries lost at least one year of life expectancy in each year, with a dashed line for the typical year (3 countries) and the two COVID years (58 and 72) in the accent color. The bars are gray except those two so the answer to "was COVID unusual?" is visible before reading anything; I label only the bars I want you to compare, and annotate the earlier clusters (the 1970s and 1990s) in plain words. Panel B asks the second question, how deep and how long, by plotting each large setback (5 or more years of life expectancy lost in an uninterrupted decline) as a dot: x is the year of the trough, y is the years lost on a log axis (because losses range from 5 to 40 years), and color is the time to recover, from gold (3 years or less) to dark red (11 years or more or not yet recovered). I labeled the famous events (Rwanda 1994, Cambodia, Lebanon, the HIV/AIDS countries) and the small group of COVID-era dots, which shows the finding: COVID was broad but rarely among the deepest. The legend sits below the plot. I made the caption explain the definition of a setback and the data caveats (some Central African Republic estimates are extreme).

---

## 20. How I made these visualizations (tools, processing, AI disclosure)

**AI disclosure (please read).** These answers and figures were produced entirely by an AI system, Claude (model Sonnet 5.5, run through Claude Code), not by a student. They were created at the instructor's explicit request, as a private example response to this assignment for instructional review; they are not a student submission. The AI chose the stories, designed and coded all six visualizations, ran the data processing, and wrote every answer in this document, including the critique, which is the AI's own opinion of the provided example and not the opinion of a student. The instructor supplied the assignment text and the data, and asked for the result. No person other than the instructor reviewed or edited the content before this document was written.

**Tools.** Python 3.14 (the shared `p314` conda environment) with pandas and numpy for data handling, and matplotlib for all drawing. Fonts: Arial. No other software, no web data, no data other than the two supplied data sets. All code is in `work/`.

**Data processing.**
- *World Bank life expectancy* (`lifespan_dataset_1960.csv`): pivoted from tall to wide by sex, gap = Female minus Male. World Bank aggregates (income groups, regions) were removed by keeping only entities whose three-letter code appears as a country in the Our World in Data file; 215 countries and territories remain.
- *Census* (`full_census_dataset.csv`): read as Latin-1 (the file is not UTF-8). Counties were assigned to four settings using the 2023 Rural-Urban Continuum Code (1; 2 to 3; 4 to 7; 8 to 9); 17 areas without a 2023 code were dropped. Unemployment rate for a group = sum of Unemployed / sum of Civilian labor force over its counties with both values present. County changes use the supplied Unemployment rate columns. College share uses the "Percent of adults with a bachelor's degree or higher" columns for 1990 and 2019 to 2023.
- *Our World in Data life expectancy*: real countries only (those with a country code; the USSR series and regional aggregates removed), years 1950 to 2023, 236 countries. A setback is a run of consecutive annual declines; loss = peak minus trough; recovery = years from trough until the pre-decline value is reached again.

**Limits and honesty notes.** The figures are descriptive, not causal. Country selections in Figures 1b and 1a highlights are my judgment. Group definitions of rural/urban are the USDA's 2023 definitions applied to older years, which the assignment permits.
