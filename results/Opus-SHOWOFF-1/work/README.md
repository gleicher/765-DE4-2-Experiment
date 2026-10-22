# DE4-2 working files

**Tools:** Python 3.14 from the `p314` conda env (`/opt/anaconda3/envs/p314/bin/python`) with pandas, NumPy, matplotlib, and seaborn (seaborn is used only for the "mako" colour ramp in Q3). No packages were installed and no manual editing was done: every figure comes straight from a script.

**Regenerate all figures** (writes PNGs to `../answers/figures/` and helper CSVs to `intermediate/`):

    sh work/make_all.sh

or run any one script, e.g. `/opt/anaconda3/envs/p314/bin/python work/fig3_milestones.py`.

| Script | Output figure |
|---|---|
| `fig1a_gap_path.py` | `q1a_gap_arc.png`: sex gap vs. life expectancy, connected scatter |
| `fig1b_gap_heatmap.py` | `q1b_gap_heatmap.png`: gap heatmap indexed by life expectancy + dumbbell |
| `fig2a_components_bars.py` | `q2a_components_by_rucc.png`: population-change components by RUCC |
| `fig2b_county_quadrants.py` | `q2b_county_quadrants.png`: county quadrant small multiples |
| `fig3_milestones.py` | `q3_fifty_to_seventy.png`: years from life expectancy 50 to 70 + Kaplan–Meier curves |
| `fig4_two_recessions.py` | `q4_two_recessions.png`: unemployment in two recessions by RUCC |

Shared code: `common.py` (paths, palette, matplotlib style, data loaders, RUCC labels), `census_components.py` (Q2 rate calculations), and `q3_milestones.py` (Q3 crossing-year calculation; running it directly prints a summary).

`explore_*.py` are the exploratory scripts used to find the stories. They aren't needed for the figures.

Notes: the county CSV is latin-1 encoded. The palette is the colour-blind-checked reference palette from the dataviz skill. The fonts are Helvetica Neue with Arial Unicode MS as a fallback for symbols; on a machine without them, matplotlib will use another font and the layout may shift slightly.
