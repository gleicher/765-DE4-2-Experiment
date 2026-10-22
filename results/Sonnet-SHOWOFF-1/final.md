The answers, six figures, work files and sources note are all written. I checked every figure by eye except the final regenerated versions of figures 1 and 6 (the post-fix reruns), and I didn't re-read answer.md after writing it.

**Files**
- Answers: `answers/answer.md`, with Canvas Q1–Q20 numbered to match.
- Sources: `answers/sources.txt`. I opened no web pages, so it says everything came from the local `reference/` and `data/` files.
- Work: all scripts are in `work/` (`common.py`, `fig1a.py`, `fig1b.py`, `fig2a.py`, `fig2b.py`, `fig3.py`, `fig4.py`) with `work/README.md`.
- Tools: pandas and matplotlib in p314, nothing installed. There are no manual steps.

**Figures** in `answers/figures/`:
- Q1 (life expectancy, why women outlive men by different margins):
  - `q1_fig1_gap_small_multiples.png`: the female–male life-expectancy gap in four panels. They are post-Soviet states, wealthy countries, South Asia, and Gulf states plus West Africa. All other countries sit in gray behind for context.
  - `q1_fig2_gap_dumbbell.png`: a dumbbell chart of the 1960 versus 2023 gap for 25 countries, using the same four groups and colors.
- Q2 (census, education by county type):
  - `q2_fig1_education_gap_lines.png`: pooled bachelor's-or-higher share by county type, 1970–2019-23. The metro–rural gap grows from 6 to 18 points, and rural counties today match metro counties around 1984.
  - `q2_fig2_education_county_distributions.png`: every county as a dot, 1970 versus 2019-23, with medians. The median gap is only 8 points, because big metros drive the pooled 18.
- Q3 (`q3_fig1_covid_loss_recovery.png`): a scatter of life expectancy lost 2019–21 against regained 2021–23. A full-recovery diagonal splits 185 countries above their 2019 level from 31 below, and color shows 2019 life expectancy.
- Q4 (`q4_fig1_unemployment_tile_map.png`): a tile-grid map of state unemployment sparklines, 2000–2023. Tiles are tinted by whether the Great Recession (42 states) or 2020 (9 states) was worse.

**Things to check before pasting**
- **Q1 critique:** I wrote the non-CLO critique of the supplied dumbbell chart. If you were in the CLO, replace it with the name of whoever critiqued you and one sentence on how helpful it was.
- **Q20 AI disclosure:** it says Claude Code generated the stories, code, figures and draft wording. Edit it to match what you actually did and put the text in your own words, since the course's AI policy expects that.
- **Possible unflagged data issues:** I dropped Central African Republic from the COVID chart (reported +26 years 2019–2023, probably a data artifact) and said so in the caption. Fixing the Q2 distribution chart's headline cost an iteration: I first wrote an 18-point gap and corrected it to the 8-point median.
- **Claims that leave the data:** the Q3 title calls the biggest losers "Latin American countries" and the Q4 title names "Sun Belt", "Rust Belt" and "tourism-heavy" states. Both rest on general knowledge of the country and state names, not on columns in the data.
- **Q4 understates COVID:** annual averages smooth the 2020 spike, and the caption says so. Puerto Rico is omitted because it has no 2020 value.
- **Education definition shift:** the 1970 and 1980 education columns are "four years of college or more" while later years are "bachelor's degree or higher". The caption flags this.
