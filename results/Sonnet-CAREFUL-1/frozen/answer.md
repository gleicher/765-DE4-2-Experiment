# Design Exercise 4-2 answers (numbered to match the Canvas questions)

## 1. Critique (not in the CLO; critique of the provided "Income inequality varies across states" chart)

What works: A dumbbell (max and min county median income per state) with a connecting line is a sensible way to show a range, and it uses a shared vertical scale so the lengths are directly comparable. Labeling each state with the max/min ratio (1.01x to 3.78x) puts the key number on the chart, and the caption explains what the dots and lines mean. Blue/orange is a colorblind-safe pairing.

What hurts it: (1) The title, "Income inequality varies across states," is generic and doesn't state the finding; it also overstates, because max/min of county medians measures spread between counties, not income inequality among households. (2) The states are not sorted by the quantity of interest, so the x-axis order (WY, AK, ND, DE, NH, ...) reads as arbitrary. Sorting by the ratio would make the ranking the story. (3) The selection rule ("top 5, bottom 5, and 6 additional") is buried in the caption and the extra 6 look arbitrary, so the viewer can't tell if the sample is representative. (4) The y axis starts at 0K and runs to 160K, so the bottom third of the plot is empty; a range of about 25K to 155K would use the space better. (5) The ratio is encoded only as text while the visual encoding is the absolute gap, which is dominated by high-income states (CA's gap looks as large as AL's but means a different ratio). A log scale or plotting the ratio directly would match the claim. (6) Details look like default Tableau output: the "Measure Names" legend title, the doubled state labels (above the dots and again on the axis), the overlapping "3.78x" label on the VA dot, and the lack of a data source or year note in the caption (only "2021" appears on the axis label). (7) The max/min of a state's counties depends heavily on how many counties it has (DE has 3 counties, VA has over 130), which is never mentioned.

Overall it is a clear, standard design, but with a stated finding in the title, sorting by ratio, a tighter axis and fewer Tableau artifacts it would be much stronger.

## 2. Story/Question 1 (Life Expectancy)

Women outlive men almost everywhere, but has that advantage been growing or shrinking since 1960, and does it depend on the country? (Answer: it widened in about two-thirds of countries, with the median gap rising from 4.1 to 5.0 years, but it narrowed in 55 mostly high-income and some African countries, with very different paths for India, the US/UK and post-Soviet states.)

## 3. Visualization 1 for Story 1

File: `figures/q1_a_gap_scatter.png`

## 4. Rationale for Visualization 1

I wanted every country on one chart so that "most countries" is visible rather than asserted. The gap (female minus male life expectancy) is computed for 1960 and 2023, and each country is one dot with 1960 on x and 2023 on y. A dashed y = x line means "no change", so the eye can immediately judge whether a dot is above (wider gap now) or below (narrower) the line without reading a change number. I colored only dots that changed by more than 0.5 years (orange widened, blue narrowed, gray unchanged), directly labeled the counts (128 and 55 of 213), and labeled a small set of informative countries (Ukraine, Russia, Pakistan, India, UK, US, Japan, Cameroon, etc.) rather than all of them. The same axis range on both axes keeps the diagonal at 45 degrees and the units identical. I removed regional and income aggregates (e.g., "World", "High income") so that dots really are countries, and used a colorblind-safe orange/blue pair. The title states the finding and the caption gives the medians and notes the war context for Ukraine so the figure stands alone.

## 5. Visualization 2 for Story 1

File: `figures/q1_b_gap_lines.png`

## 6. Rationale for Visualization 2 (Question 1 alternate)

This version shows time directly. Instead of two snapshots it plots the gap year by year for six hand-picked countries that represent different stories: India (men outlived women in 1960, now +3 years), the US and UK (peak in the 1970s, then falling), Japan (steady rise), and Russia and Ukraine (large gap that surges in the 1990s). Rather than drawing 200 gray spaghetti lines, which were unreadable because small countries are noisy, I show a gray band for the middle 80% of countries and a dashed median so the highlighted lines can be judged against a "typical" country. Lines are directly labeled at the right (no legend lookup), the zero line separates "women live longer" from "men live longer", and two short annotations explain the Soviet-era peak and India's start below zero. Color is used only for the highlighted countries.

## 7. Comparison of the two Question 1 visualizations

The scatterplot (1) covers all 213 countries, makes the "most widened, a minority narrowed" proportion easy to see, and the diagonal reference makes direction of change easy to judge; but it shows only two time points, hides the path in between (e.g., Russia's 1990s spike or the US peak), and requires understanding of a scatter of differences, which is less intuitive for a general audience. The line chart (2) is more intuitive and shows when and how the changes happened, with annotations for causes; but it can only show a handful of countries, so the selection is my choice and it cannot show how common each pattern is (the band and median help partly). The scatter is better for a "how many countries" claim and the line chart is better for "what happened in a given country," so I would use them together: the scatter to find the pattern and the lines to explain it.

## 8. Story/Question 2 (Census)

Has the gap in college education between big-city counties and small-town or rural counties grown since 1990? (Answer: yes. Every county type gained, but the median large-metro county went from 15% to 32% with a bachelor's degree, while small-town and rural counties went from about 10% to 19%, so the gap roughly tripled, from 4 to 12.5 percentage points.)

## 9. Visualization 1 for Story 2

File: `figures/q2_a_education_lines.png`

## 10. Rationale for Visualization 1

A line chart is the natural encoding for change across the four census time points (1990, 2000, 2008-12, 2019-23). I collapsed the nine USDA Rural-urban Continuum Codes into four groups (metro of 1M+, smaller metro, nonmetro urban, nonmetro small-town/rural) so that four lines can be directly labeled and told apart without a legend; each line is the county median, and a translucent band shows the middle half of counties so the viewer sees that the groups overlap heavily and the trend is not an artifact of a few outliers. The key comparison, the growing gap, is highlighted with a double-headed arrow and the numbers (4 points in 1990, 13 points now) in an annotation. The end labels also give the first and last values. The y axis starts at zero so the slopes are not exaggerated, and the title states the finding. The caption explains the grouping, sample size per group, and that counties are unweighted. The x positions use the approximate midpoint of the period (e.g., 2010 for 2008-12 and 2021 for 2019-23).

## 11. Visualization 2 for Story 2

File: `figures/q2_b_education_dumbbell.png`

## 12. Rationale for Visualization 2

The alternate puts the focus on the change itself and keeps the full nine-category detail. Each row is one USDA county type, ordered from most urban (1) to most rural (9). A gray dot marks the 1990 median, a blue dot the 2019-23 median, and an arrow between them shows the change, with the points gained printed next to it (+17 for large metros down to +8 for the more rural codes). Horizontal bars show the middle half of counties for each year (gray above, blue below), so spread as well as center is visible. Because the order is the natural urban-to-rural scale, the downward gradient in the gains is visible from the numbers and from the shortening arrows. A shared x axis lets all rows be compared, a legend explains the four symbols, and a caption notes that code 5 has only 76 counties. Gray for "then" and blue for "now" is used consistently.

## 13. Comparison of the two Question 2 visualizations

The line chart (1) is easy to read for a general audience, shows the full time sequence, and makes the growing gap obvious through diverging lines and an explicit gap annotation; its weakness is that grouping nine codes into four hides detail (for example, nonmetro urban counties near metros do better than remote ones) and the overlapping bands add some visual clutter. The dumbbell (2) shows every county type separately, makes the amount of change explicit with numbers, and shows distributions at the two endpoints; but it shows only two time points, so the shape over time is lost, and the paired bars take more effort to read. The line chart is the better poster/newspaper graphic and the dumbbell is better for an audience that wants the detail.

## 14. Story/Question 3

Which countries lost the most life expectancy in the first two years of COVID-19 (2019 to 2021), and had they recovered by 2023? (Answer: 84% of countries lost life expectancy; the largest losses, 8 of the top 10, were in Latin America, led by Bolivia at -6.4 years, and 23 of the 25 worst-hit countries were back at or above 2019 levels by 2023.)

## 15. Visualization for Question 3

File: `figures/q3_covid_losses.png`

## 16. Rationale for Visualization 3

I wanted to show before, bottom, and after for each country, so each row is a country with three marks on a shared life-expectancy axis: a hollow circle for 2019, a filled circle for the 2021 low point, and a black diamond for 2023. The connecting line between 2019 and 2021 is the loss and the diamond's position relative to the hollow circle shows whether the country recovered. To avoid a data dump I filtered to the 25 largest losses and sorted from largest to smallest, so the ranking is readable top to bottom. I colored the Latin America and Caribbean countries orange (and colored the country names to match) because the pattern of regional clustering at the top is the main finding; everything else is blue. The number of years lost is printed beside each low point, so the bars don't have to be measured. The caption gives the broader context (84% of 215 countries lost life expectancy, with a median change of -0.9 years) and names the two countries that had not recovered (Lebanon and North Macedonia). The region assignment is my own manual classification of the countries in the list.

## 17. Story/Question 4

Where did people move within the US after 2020: did the biggest counties lose residents to domestic migration while smaller counties gained? (Answer: yes. The 49 counties with 1M+ people lost about 25 residents per 1,000 on balance in 2021-23, while counties between 25k and 500k gained about 18 per 1,000, and the pattern holds in metro and nonmetro areas, so suburban counties absorbed much of the movement, not just rural places.)

## 18. Visualization for Question 4

File: `figures/q4_migration.png`

## 19. Rationale for Visualization 4

This is a compound design with two linked views. On the left, every county is a dot with its 2020 population on a log x axis (populations span four orders of magnitude, so a linear axis would pile nearly all counties at the left edge) and net domestic migration per 1,000 residents on the y axis, so counties of different sizes are comparable. Dots are semi-transparent to handle 3,097 overlapping points and are colored by USDA county type so the viewer can see that the pattern crosses the metro/nonmetro divide. A black line shows the median in each size band, and a handful of the largest counties (Los Angeles, Cook, Harris, Maricopa) are labeled for context. On the right, a bar chart summarizes the same information as the total across all residents in five size bands, with the number of counties in each band, so the viewer gets a clean headline that the large counties lose (orange) and others gain (blue). The zero line is emphasized in both. The migration measure is the sum of three years (July 2020 to June 2023), because the single-year values are noisy. International migration is excluded and noted in the caption.

## 20. How the visualizations were made

All figures were made in Python 3.14 (pandas for data prep, numpy, matplotlib for plotting) by scripts in `work/` (`fig1.py` to `fig4.py`), which read the provided CSV files directly and write PNGs. Data processing: for Census, I used the county-level file (dropping the national and state summary rows), used the percent of adults with a bachelor's degree for four periods, grouped counties by the 2023 USDA Rural-urban Continuum Code, computed medians and quartiles per group, and computed migration rates as summed 2021-23 domestic migration divided by the 2020 Census population times 1,000. For life expectancy, I used the World Bank file, removed regional and income aggregates (using the country codes in the Our World in Data file as the list of real countries), pivoted by sex to compute the female-minus-male gap, and computed 2019-2021-2023 changes for the both-sexes series. No data were added from outside sources, and no manual editing was done on the images. AI disclosure: the analysis, code, charts, and the text of this write-up (including the critique) were produced with an AI assistant (Claude, Anthropic), working from the course files;
