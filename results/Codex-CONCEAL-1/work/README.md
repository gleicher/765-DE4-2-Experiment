# Regenerating the figures

Run from this run's root directory:

```sh
/opt/anaconda3/envs/p314/bin/python work/make_figures.py
```

Uses the existing p314 installation of pandas, NumPy, and Matplotlib; nothing was installed. The script configures a local Matplotlib cache in `work/mplconfig/`, reads the two supplied files under `data/`, and writes six 1980 × 1350 PNGs to `answers/figures/`. It also writes the derived CSVs used to audit the plotted values into `work/`. No manual figure editing is required. Country selection, label positions, layout, and colors are specified in the script.

`explore.py` records an initial county check and can be rerun with the same interpreter. `contact_sheet.png` is a preview assembled with Pillow, not a seventh submission figure. Regenerate it with:

```sh
/opt/anaconda3/envs/p314/bin/python work/check_outputs.py
```

Processing: the county file is comma-separated and CP1252 encoded. Puerto Rico is excluded, and valid 2023 RUCC codes define metro (1–3) and nonmetro (4–9). Natural decrease means deaths exceed births; migration is domestic plus international net migration as already provided. Ratio ≥ 1 qualifies as offsetting natural decrease, independently of residual population adjustments. Education comparisons use complete cases across both periods, with fixed 2023 group membership. Counties are equally weighted; the figures do not estimate population-weighted attainment or growth. Life expectancy is estimated life expectancy at birth, not observed age at death.

The numbered response draft follows all 20 Canvas prompts. Q1 uses the supplied critique image because no CLO participation details were provided. Q20 discloses Codex's assistance; review the substantive choices and prose before submission.
