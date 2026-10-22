# Regenerating the example

Run from this run directory:

```sh
/opt/anaconda3/envs/p314/bin/python work/make_figures.py
```

The script uses existing pandas, NumPy, and Matplotlib in p314. It reads supplied files in `data/`, writes six static PNGs to `answers/figures/`, and retains derived CSV tables and its Matplotlib cache in `work/`. It requires no installations, network access, external data, or manual graphic editing. `answer.md` was drafted separately in Markdown; the critique was based on visual inspection of the supplied `reference/images/to-critique.png`.

County data are comma-delimited with cp1252 encoding, despite the general readme calling the county file tab-separated. County selection excludes Puerto Rico and invalid/missing RUCC values. Education has a complete-pair filter; migration has a complete-rate filter. Both use fixed 2023 RUCC group membership. Life figures select named countries explicitly and do not include aggregate regions.
