# Design Exercise 4-2 — Canvas responses

**1. Critique of the supplied visualization**

The range plot has a clear headline, a useful caption, and a direct visual link between each state's lowest and highest county median incomes. Its endpoint labels and maximum-to-minimum ratios make the spread easy to compare for the selected states. The title overstates what the data measure, though: the chart shows the range of *county median household incomes* within each state, not inequality among households or people. A minimum–maximum range is also sensitive to one unusual county, and the selection of five high, five low, and six “interested” states leaves the comparison incomplete and partly subjective. I would rename the measure as a county-income range, show all states in a sorted dot-and-range plot, and use a percentile interval alongside the median so one county does not determine the story. If only a subset is practical, the selection rule should be stated precisely. The zero-based vertical scale is honest, but the large unused area below the lowest values makes the differences harder to read.

**2. Story/Question 1**

How did life expectancy change from 2019 to 2021 and then to 2023 across countries and regions, did recovery differ by sex, and which places had regained their 2019 level by 2023?

**3. First visualization for Question 1**

[Figure 1 — Life-expectancy losses and rebounds](figures/01-life-expectancy-loss-and-rebound.png)

**4. Rationale for Visualization 1**

The scatterplot places the 2019–21 change on the x-axis and the 2021–23 change on the y-axis, so the viewer can compare the initial loss with the subsequent gain for each place. The dashed diagonal marks the amount of rebound needed to return to the 2019 level; points above it have regained or exceeded that level. Separate panels make the sex estimates comparable without overloading one plot. I highlight several of the largest declines in the Both-sex panel, while retaining all 265 places in the background for context. By 2023, 228 places had regained their baseline in the Both-sex series; the count is 228 for female and 226 for male estimates. The figure describes the changes and does not assign them to a single cause.

**5. Second visualization for Question 1**

[Figure 2 — Life-expectancy trajectories for six places](figures/02-life-expectancy-country-trajectories.png)

**6. Rationale for Visualization 1 Alternate**

This small-multiple line chart focuses on the six places with the largest 2019–21 decline in the Both-sex series. Within each country panel, the three colored lines show female, male, and Both-sex estimates at the same three dates. A shared y-axis preserves comparisons across countries, while the paired drop-and-rebound labels summarize the overall series. The selection is deliberately narrow: the first visualization supplies the global context, and this one makes the sex-specific trajectories legible.

**7. Compare the two visualizations for Question 1**

Figure 1 is the stronger overview: it shows the range of outcomes across all places, makes the return-to-baseline threshold explicit, and separates results by sex. Its dense point cloud and overlapping estimates make individual country comparisons difficult. Figure 2 is easier to read for the places with the deepest losses and exposes differences among sex estimates and recovery paths. It loses the full distribution, however, and its selected countries should not be read as representative. Together they show both the overall recovery pattern and a few especially sharp cases.

**8. Story/Question 2**

How did county bachelor's-degree attainment change from 1990 to 2019–23 across metro, micropolitan, and rural areas, and did the median metro–rural gap narrow or widen?

**9. First visualization for Question 2**

[Figure 3 — Bachelor's attainment by rurality](figures/03-bachelors-attainment-by-rurality.png)

**10. Rationale for Visualization 2**

The line chart follows the median county's bachelor's attainment across four periods, with a distinct color for each rurality group. The shaded middle-50% bands show how much county rates vary within each group, and direct endpoint labels keep the latest values readable. I use the same counties with complete data across all four periods so changes are not caused by counties entering or leaving the comparison. Counties receive equal weight; these are not population-weighted estimates. Using the 2023 rural–urban classification for all dates allows a consistent group comparison but does not represent how each county was classified in 1990.

**11. Second visualization for Question 2**

[Figure 4 — Paired county attainment distributions](figures/04-bachelors-attainment-paired-counties.png)

**12. Rationale for Visualization 2 Alternate**

The three hexbin panels compare each county's 1990 attainment with its 2019–23 attainment, using the same scale for each rurality group. Darker hexagons show where more counties fall; the diagonal marks no change, and a diamond locates each group's median in both periods. This paired view shows the county-level spread and overlap that a summary trend can hide, while the median markers keep the central metro–rural difference visible. I use the same complete-case county set as in Figure 3.

**13. Compare the two visualizations for Question 2**

Figure 3 is the clearest answer to whether the median gap widened: the change over time and the widening difference are immediately visible. Its group medians compress considerable county variation. Figure 4 shows that variation and makes clear that many counties in different rurality groups overlap, even as each group's median lies above its 1990 value. Its paired scales and hexbin legend take more effort to read, and it emphasizes the first and last periods rather than the intervening trajectory.

**14. Story/Question for Visualization 3**

How did the county unemployment-rate distribution change from 2000 to 2023 across rurality groups, and how did the 2020 spike affect the rural–metro difference?

**15. Visualization 3**

[Figure 5 — County unemployment cycle](figures/05-county-unemployment-cycle.png)

**16. Rationale for Visualization 3**

Annual median lines make the two large spikes and the subsequent decline easy to follow; bands show the middle half of county rates rather than hiding variation behind the median. The 2009 and 2020 reference lines orient the timeline, and the 2019, 2020, and 2023 values in the subtitle clarify the rural–metro change. I classify counties with the 2023 rural–urban code and give each county equal weight. This descriptive chart shows when the rate differences changed, not why they changed.

**17. Story/Question for Visualization 4**

Among county areas with both natural decrease and positive net migration in 2023, how often did migration more than offset natural decrease, and how did the balance vary across rurality and population size?

**18. Visualization 4**

[Figure 6 — Natural change and migration](figures/06-county-natural-change-and-migration.png)

**19. Rationale for Visualization 4**

The scatterplot maps natural change against net migration, colors counties by rurality group, and sizes points by population. Zero lines distinguish positive and negative rates; the dashed \(y=-x\) line marks where the two rates sum to zero. The shaded region identifies counties where positive migration more than offsets negative natural change. In the full-range panel, every complete county-area observation remains visible; the paired detail panel enlarges the dense center while the caption states the percentile bounds. This design makes the balancing relationship and its exceptions visible without treating an association as a cause.

**20. How I made the visualizations**

I used Python from the shared `p314` environment, with pandas for reading and reshaping the course CSV files, Matplotlib for the static PNG figures, and Pillow to assemble a contact sheet for layout review. The reproducible source is `work/make_figures.py`; it reads the local files in `data/` and writes all six figures to `answers/figures/`. It also reads the census file using its Windows-1252 encoding.

For Figure 1, I pivoted the life-expectancy data to compare 2019, 2021, and 2023 by country/region and sex, then computed the two interval changes and the return to the 2019 level. For Figure 2, I selected the six largest declines in the Both-sex series and plotted the three sex estimates over those dates.

For Figures 3 and 4, I grouped counties by 2023 Rural–Urban Continuum code (1–3 metro, 4–6 micropolitan, 7–9 rural), retained counties complete on all four bachelor's-attainment measures, and calculated group medians, quartiles, and paired county distributions. Figure 5 calculates annual county medians and quartiles for the three groups. Figure 6 uses the two 2023 rate fields and the 2023 population estimate to identify counties where positive net migration more than offsets negative natural change; it uses population to size the points. The source code records these transformations and figure labels.

There were no manual figure-editing steps. I made a contact sheet in `work/` to inspect the six layouts. No web pages were opened; the assignment, design guidance, and data documentation were the local copies supplied in `reference/` and `data/`.

**AI disclosure:** OpenAI Codex prepared this complete instructional example at the instructor's request. It selected and analyzed the stories, wrote the plotting code, generated the figures, and drafted the rationales, comparison, and critique. The example is not represented as student-authored work.
