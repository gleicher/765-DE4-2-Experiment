# work/ — how the DE 4-2 figures were made

## Tools
- Python 3.14 from the `p314` conda environment (`/opt/anaconda3/envs/p314/bin/python`)
- pandas / numpy for data processing, matplotlib for every figure (Arial font, 200 dpi PNG)
- No packages were installed and no other tools were used. Everything is scripted; nothing
  was edited by hand afterwards.

## Regenerate everything
```sh
./make_all.sh          # or: sh work/make_all.sh from the run folder
```
This writes the six PNGs to `../answers/figures/` and intermediate CSVs to `intermediate/`.
You can also run any one `fig*.py` script on its own. There are no manual steps.

## Files
| File | Purpose |
|---|---|
| `common.py` | paths, shared style/colors, data loaders (drops WB/OWID aggregates; census county rows only, no PR) |
| `q1_data.py` | Q1 table: 2019 LE, pandemic low (2020–22), "setback year", recovery by 2023 |
| `fig1a_setback_small_multiples.py` | Q1 visualization 1 (16 small multiples) |
| `fig1b_setback_scatter.py` | Q1 visualization 2 (all-country scatter) |
| `q2_data.py` | Q2 components of population change by 2023 RUCC, 2021–2023 |
| `fig2a_components_bars.py` | Q2 visualization 1 (diverging stacked bars, 3-year cumulative) |
| `fig2b_components_heatmap.py` | Q2 visualization 2 (annual heatmap) |
| `fig3_education_gaps.py` | Q3 (education gaps by county type, 1970–2019/23) |
| `q4_data.py` | Q4 table: interpolated years each country reached LE 50 and 70 |
| `fig4_50_to_70.py` | Q4 (scatter with censored "not yet" countries) |
| `intermediate/*.csv` | the computed tables behind each figure |

## Data-processing notes
- `full_census_dataset.csv` is actually comma-separated and Latin-1 encoded (the readme says tab).
- World Bank aggregates (e.g. "Euro area", "IDA only") were removed by keeping only codes that
  OWID also uses for real countries (OWID's own aggregates have `OWID_` codes).
- Central African Republic is dropped from Q1 because its World Bank series is implausible
  (31.5 → 50.6 → 40.3 → 18.8 → 57.4 for 2019–2023).
- Census rates are population-weighted group totals, not averages of county rates.
- Q3 uses 2023 RUCC codes for all years (allowed: "approximately correct" years).
