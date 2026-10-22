# Regenerating this instructor example

Run from this run directory:

```sh
/opt/anaconda3/envs/p314/bin/python work/make_figures.py
```

The script uses already installed pandas, NumPy, and Matplotlib. It sets a local Matplotlib cache in `work/mplcache`, reads only the supplied data, and writes six 2160×1440 PNGs into `answers/figures/`. It also writes the four processed CSVs and `summary.json` here. No installation or toolchain changes are needed.

The census input is comma-separated CP1252 (the README's tab-separator note does not match this supplied copy). County rows are filtered by valid 2023 rural–urban codes and exclusion of Puerto Rico. Education rows require both shares; migration rows require both component rates. Country choices, grouping, and transformations are explicit in the script and described in answer 20.

`preview.png` is a contact sheet used to inspect spacing, labeling, and readability. It was made with Pillow by shrinking each generated figure to fit a 720×480 cell on a 2-column, 3-row canvas. This optional preview has no role in generating the final figures. No manual image editing is required. The answers were authored in Markdown by Codex for instructor review and may be edited independently of the plotting script.
