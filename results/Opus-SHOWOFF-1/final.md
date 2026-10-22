All six figures are made, and `answers/answer.md` has text for Canvas questions 1–20 ready to paste. Every figure was rendered and checked by eye, revised for overlapping labels and colour problems, and rebuilt cleanly with `work/make_all.sh`.

**Before you submit:** question 20's AI disclosure says plainly that Claude Code chose the stories and wrote the code, the rationales and the critique. It ends with a bracketed note for you to edit. The course GenAI policy says the work, and especially the critique, should be your own, with the AI credited. So rewrite those parts in your own words and adjust the disclosure to match what you actually did.

**The four stories:**

| Q | Figure(s) in `answers/figures/` | Story and design |
|---|---|---|
| 1 (World Bank life expectancy) | `q1a_gap_arc.png`, `q1b_gap_heatmap.png` | How far women outlive men rises as countries get healthier, peaks at about 6.2 years when overall life expectancy is around 71, then narrows. Russia and other former Soviet states sit far above the pattern. **A:** gap plotted against life expectancy for all 217 countries, a median curve, and four country trails (Sweden, South Korea, India, Russia). **B:** heatmap of 43 countries whose columns are levels of life expectancy rather than years, with a summary bar chart on top and a "widest gap vs 2023" comparison on the right. |
| 2 (USDA census) | `q2a_components_by_rucc.png`, `q2b_county_quadrants.png` | 2021–23: the biggest metros grow only through births and immigrants while Americans move out. In five of six rural counties deaths outnumber births, and most of those are refilled by Americans moving in. **A:** births minus deaths, moves within the US, moves from abroad, and total change as side-by-side bar panels across all nine rural-urban codes. **B:** every county plotted in three panels by metro status, with the share in each quadrant. It also shows that the big-metro outflow comes from a few giant core counties (Los Angeles, Cook, Brooklyn). |
| 3 (Our World in Data long-run) | `q3_fifty_to_seventy.png` | Countries that reached a life expectancy of 50 later usually got to 70 faster (Norway took 93 years, Japan 17). The speed-up peaked with countries that reached 50 in 1930–49; later groups are slower, and 45 of those 64 countries haven't reached 70 yet. Scatter plus "share that has reached 70" curves that count still-waiting countries instead of dropping them. |
| 4 (census) | `q4_two_recessions.png` | Rural unemployment ran above the big metros' from 2000 to 2019. In the Great Recession every kind of county rose by a similar 4–5 points. COVID reversed the pattern: the 2020 jump fell from +5.1 points in big metros to +2.2 in the most remote counties. Line chart, rural-minus-metro bars, and a comparison of the two recessions for each county type. |

**Critique (Q1):** The main points are that the max/min county ratio isn't really inequality and goes up with how many counties a state has (rank correlation about 0.57), and that bar length shows the dollar gap while the labels and sort order show the ratio. I also flag that Wyoming's 1.01x looks like a data error: in the current 2022 data its counties span 2.4x. Alaska and North Dakota look similarly off.

**Data choices you should know about:**
- I excluded Puerto Rico because it has no population-change data. Including it would have quietly distorted the metro rates.
- I also dropped 17 retired Alaska/Connecticut county units that have no 2023 rural-urban code.
- The census CSV only reads correctly as latin-1.
- I didn't install any packages. Everything uses matplotlib, pandas and numpy, plus seaborn for one colour ramp.
- I opened no web pages, so `sources.txt` says so and lists the local references and the data sources from the readmes.

All files are in `/Users/mlgleich/Projects/765/765-DE4-2-Experiment/runs/Opus-SHOWOFF-1/`:
- `answers/answer.md`
- `answers/sources.txt`
- `answers/figures/` (the six PNGs)
- `work/README.md`: tools, script-to-figure table, how to regenerate
- `work/make_all.sh`: rebuilds every figure with no manual steps
- `work/`: one script per figure, shared helpers, the exploratory scripts, and intermediate CSVs in `work/intermediate/`
