# work/ — scripts for the DE4-2 figures

Tools: Python 3.14 (`/opt/anaconda3/envs/p314/bin/python`) with pandas, numpy and matplotlib.
No other packages were installed, and no R code was used. Font: Arial (ships with macOS).

| Script | Output (in `answers/figures/`) | Data |
|---|---|---|
| `fig1a_gap_lines.py` | `q1a_gap_lines.png` | World Bank life expectancy by sex |
| `fig1b_gap_trajectories.py` | `q1b_gap_trajectories.png` | World Bank life expectancy by sex |
| `fig2a_unemployment_lines.py` | `q2a_unemployment_lines.png` | USDA county census file |
| `fig2b_unemployment_shocks.py` | `q2b_unemployment_shocks.png` | USDA county census file |
| `fig3_population_components.py` | `q3_population_components.png` | USDA county census file |
| `fig4_covid_setback.py` | `q4_covid_setback.png` | Our World in Data life expectancy |

`common.py` holds the shared data loaders (it handles the census file's Latin-1 encoding and
comma thousands separators and drops Puerto Rico), the label lookups (USDA economic types, RUCC
codes, World Bank aggregate codes) and the plot style.

## Regenerate

```
cd work
for f in fig*.py; do /opt/anaconda3/envs/p314/bin/python "$f"; done
```

Each script reads from `../data/` and writes its PNG (200 dpi) into `../answers/figures/`. Some
also write an intermediate table here (`out_*.csv`) with the numbers used in the figure and
the text.

Manual steps: none. All titles, annotations, captions and legends are drawn by the scripts. A
few label positions are hand-tuned in the code, so if you change the data or figure size,
check the labels for overlaps.
