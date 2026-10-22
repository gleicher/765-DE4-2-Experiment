I made the six figures and wrote answers for all 20 Canvas questions. I did not use Tableau, because it isn't installed here. The figures are matplotlib charts styled to look like default Tableau worksheets. That styling means the Tableau 10 palette, an Arial-style font, light gridlines, legends at the right and reference lines. The disclosure answer (Q20) says this plainly and says the work was done by Claude (Sonnet 5.5, in Claude Code) as an instructor-requested example.

I viewed every figure at least once. The first versions had label overlaps and a clipped title, which I fixed. After the last edits I re-viewed only the Q3 and Q4 images.

**Figures (in answers/figures/):**

| Story | File | Design |
|---|---|---|
| Q1 Life expectancy: is the female advantage shrinking or growing? | `q1a_gap_lines.png` | Lines of the female-minus-male gap, 1960–2023, for 8 countries, with a zero line and end labels. |
| | `q1b_gap_dumbbell.png` | Dumbbell chart (two dots joined by a line) of the 1960 vs 2023 gap for 18 countries, sorted by 2023 gap. |
| Q2 Census: do more-educated counties have lower unemployment, in every rural-urban group? | `q2a_scatter.png` | Scatter of 2023 unemployment vs. share of adults with a bachelor's degree, colored by rural-urban group, sized by population, with trend lines. |
| | `q2b_bars.png` | Grouped bars of median unemployment by education quartile and rural-urban group. |
| Q3 Census: did 2009 and 2020 hit metro and rural counties differently? | `q3_unemployment_time.png` | Unemployment lines 2000–2023, weighted by labor force, with markers at 2009 and 2020. |
| Q4 Census: which states gained or lost residents to other states, 2021–2023? | `q4_migration_states.png` | Sorted diverging bars of net domestic migration per 1,000 residents, colored by sign. |

The rural-urban groups are metro (codes 1–3), nonmetro adjacent to a metro area (4, 6, 8) and nonmetro not adjacent (5, 7, 9).

**Findings the answers rely on:**
- **Q1:** Russia and Ukraine have the largest gaps (about 10.7 and 13.3 years in 2023). The gap is about 0.6 years in Nigeria and about 3 years in India, which started at −1.4 in 1960.
- **Q2:** The correlation between education and unemployment is about −0.29 within each group.
- **Q3:** In 2020 the metro rate hit 8.2% against about 7% elsewhere. In 2009–10 the adjacent nonmetro counties peaked highest, at 10.3%.
- **Q4:** Idaho gained the most (16.8 per 1,000) and New York lost the most (−13.6).

**Things to know:**
- Bangladesh's 1971 spike in Q1A is in the source data. The caption says so, and I did not remove it.
- Q2A leaves out the few counties with unemployment above 12%, and the caption says so.
- Q1 of the Canvas list (the critique) is answered by critiquing `reference/images/to-critique.png`, since there is no CLO partner.

**Files:**
- Answers: `/Users/mlgleich/Projects/765/765-DE4-2-Experiment/runs/Sonnet-TABLEAU-PLAIN-2/answers/answer.md`
- Figures: `/Users/mlgleich/Projects/765/765-DE4-2-Experiment/runs/Sonnet-TABLEAU-PLAIN-2/answers/figures/`
- Sources: `answers/sources.txt` says no web pages were opened.
- Script: `work/make_figures.py` regenerates all six figures with no manual steps. `work/README.md` has the command and the data-processing notes.

I used only the existing p314 Python and installed nothing.
