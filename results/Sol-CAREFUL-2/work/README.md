# Regenerating the example

Run from this run directory:

```sh
/opt/anaconda3/envs/p314/bin/python work/make_figures.py
```

The script uses the existing pandas, NumPy, and Matplotlib packages in `p314`; no installation or virtual environment is needed. It resolves input and output paths relative to itself, reads the supplied data, and writes six 1980 × 1440 PNGs to `answers/figures/`. It also writes derived CSVs here: selected life estimates and sex gaps, Wisconsin county component balances and classifications, weighted unemployment summaries (including observation counts), and recovery changes. A writable Matplotlib cache is kept under `work/mplconfig/`.

Python/Pillow was used to build `review_contact_sheet.png` from the six rendered PNGs for inspection. This review image is not an assignment upload. There are no manual chart-editing steps: labels, layout, country selections, and captions are in `make_figures.py`. The supplied critique image was inspected visually; the written critique and rationales are in `answers/answer.md`.

The census file actually uses comma separators and CP1252 encoding despite the readme's tab-separated warning. County filtering uses a nonmissing 2023 RUCC, excluding aggregate rows. Puerto Rico is excluded from the national unemployment series. The script uses fixed 2023 metro/nonmetro groups and matched nonmissing observations for each unemployment year; it does not harmonize changing county boundaries. Population balances use supplied rates and exclude residual change.

No external pages were opened. This is an AI-generated instructor review example, as disclosed in response 20.
