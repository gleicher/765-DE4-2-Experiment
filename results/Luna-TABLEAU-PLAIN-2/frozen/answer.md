# Design Exercise 4-2 — example responses

## 1. Critique of the provided visualization

The paired dots and gray stems make the county-income range easy to compare across states, and the ratio labels add a useful relative comparison to the absolute dollar values. The title and caption explain the measure, and the selected states keep the figure focused. The main limitation is that a state’s maximum-to-minimum ratio is sensitive to its most extreme county and does not describe the experience of a typical county or resident. The caption says that only 16 states are shown, but the selection rule for the six “interesting” states is not explicit, so the comparison should not be read as representative of all states. The ratio labels and small, light caption are also difficult to read at this image size.

## 2. Story/Question 1

How did the female life-expectancy advantage over men change from 1960 to 2023 in six countries with different trajectories, and how did it shift between 2019 and 2021?

## 3. First visualization for Question 1

[Visualization 1 — annual gender-gap lines](figures/1-life-gap-line.png)

## 4. Rationale for Visualization 1

I calculated the difference between female and male life expectancy and put that difference on the vertical axis, so the chart directly answers whether and by how much women live longer in each country. The zero reference line makes the change from a male to a female advantage visible; India crosses it during the series. Country color supports comparison across the full annual trajectories, while the vertical 2020 marker makes the period around the pandemic easier to locate without attributing the changes to a cause. I selected six countries with visibly different paths, including the persistent large gap in Russia and the shift in India.

## 5. Second visualization for Question 1

[Visualization 2 — milestone small multiples](figures/2-life-gap-small-multiples.png)

## 6. Rationale for Visualization 1 Alternate

This version gives each country its own pane and holds the vertical scale constant. The four colored points show the gap in 1960, 2019, 2021, and 2023, with a connecting line to show the order of the observations. This makes the direction and size of each country’s long-term change easier to inspect without tracing six lines through one plot. The milestone years are equally spaced to align the panes, so horizontal distance should not be interpreted as elapsed time.

## 7. Comparison of the two visualizations for Question 1

The annual line chart gives the fuller history: it shows when trajectories changed, whether a shift lasted, and how countries compared in any year. Its six lines and legend require more visual tracking. The small multiples reduce that tracking and make country-specific differences, including India’s crossing of zero, easier to see. They discard most years, though, and their equal spacing for milestone years hides the very different time intervals. The first chart is stronger for following the whole trajectory; the alternate is stronger for comparing selected checkpoints.

## 8. Story/Question 2

How did county bachelor’s attainment change across the available education periods, and how does the 2019–23 distribution differ between metro and nonmetro counties?

## 9. First visualization for Question 2

[Visualization 3 — county education trend](figures/3-county-education-trend.png)

## 10. Rationale for Visualization 3

The line chart compares the median county share of adults with a bachelor’s degree or higher over four available periods. I grouped counties by the 2023 Rural-urban Continuum Code: codes 1–3 are metro and codes 4–9 are nonmetro. The median gives each county equal weight and reduces the influence of counties with unusually high or low values. Both groups rose, while the median gap grew from about 2.9 percentage points in 1990 to 7.6 points in 2019–23. The caption notes that the education periods have different lengths and that the current county classification is applied throughout.

## 11. Second visualization for Question 2

[Visualization 4 — county education box plots](figures/4-county-education-boxplot.png)

## 12. Rationale for Visualization 4

The box plots show the distribution of county attainment in the latest period separately for each of the nine rural–urban codes. The median, middle half of counties, whiskers, and outliers reveal both the overall metro/nonmetro difference and the substantial variation within each code. Blue and orange distinguish the broad metro and nonmetro groups. The chart makes clear that the distributions overlap, so the group difference is not a claim that every metro county exceeds every nonmetro county.

## 13. Compare the two visualizations for Question 2

The trend chart is better for answering how county medians changed across the available education periods. It compresses the nine codes into two groups, so it does not show within-group variation or differences among codes. The box plots show that variation and overlap directly and preserve the nine code categories, but they show only 2019–23 and cannot answer how attainment changed over time. Together they show the broad widening median gap and the distributional nuance behind it.

## 14. Story/Question 3

How did life expectancy at birth change over the twentieth century and into 2023 in four countries with long-running historical series, and where do the data show setbacks in that long-term rise?

## 15. Visualization for Question 3

[Visualization 5 — historical life expectancy](figures/5-owid-long-run-life-expectancy.png)

## 16. Rationale for Visualization 3

The line chart uses year and life expectancy to show long-term direction and interruptions for the United Kingdom, Sweden, the United States, and Japan. I began at 1900 to put the four series on a shared time window and used distinct colors with a compact legend. The common scale makes broad changes and differences in levels visible, including the sharp wartime drop in Japan and the more recent dips around 2020. The supplied Our World in Data file combines estimates from multiple sources and has uneven historical coverage; lines connect observed years, and the chart describes patterns without assigning causes.

## 17. Story/Question 4

In 2023, when state-level areas had more deaths than births, did net migration tend to offset that natural decline?

## 18. Visualization for Question 4

[Visualization 6 — natural change and migration](figures/6-state-migration-natural-change.png)

## 19. Rationale for Visualization 4

The scatterplot puts natural change rate on the horizontal axis and net migration rate on the vertical axis, both per 1,000 residents. The zero reference lines divide areas by whether each component adds to or subtracts from population change; color identifies the four sign combinations. Among the 50 states and Washington, D.C., 18 had negative natural change and 17 of those had positive net migration. Oregon was the only one with both rates negative. Equal-size marks keep the state-level areas visually comparable, and selected labels identify a few points without covering the dense center of the plot. These components describe population change; they do not show why people moved or establish causation.

## 20. How I made these visualizations

I used Python 3.14 from the `p314` environment, with pandas 3.0.6 for data preparation and Matplotlib 3.11.2 for static PNG figures. I did not use Tableau; I kept the charts close to basic worksheet designs using rows/columns, color, small multiples, reference lines, medians, box plots, and straightforward calculated fields. I used the local World Bank life-expectancy file to calculate female-minus-male gaps; the county census file to group county education percentages by the 2023 rural–urban code and calculate medians; the state aggregate file for the population-component scatterplot; and the local Our World in Data file for the historical life-expectancy chart. No external data were added.

OpenAI Codex (GPT-6) contributed to data exploration, story and design choices, Python chart code, the critique, and these written rationales. I inspected the resulting figures and adjusted their layout. The assignment, rubric, critique image, and data documentation came from the supplied local `reference/` and `data/` folders. No web pages were opened.
