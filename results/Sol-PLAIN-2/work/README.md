# Regenerating this instructor example

Tools: the existing p314 Python 3.14 environment, pandas, NumPy, Matplotlib and Pillow (contact-sheet inspection only). No installations or toolchain changes were made.

From this run directory:

```sh
/opt/anaconda3/envs/p314/bin/python work/make_figures.py
```

The script reads the supplied files in `data/`, generates six PNGs in `answers/figures/`, and writes selected/derived CSVs and `summary.json` here. It directs Matplotlib’s cache to `work/matplotlib-cache/`. All chart labels, captions and annotations are scripted. There are no manual figure edits. The written response is `answers/answer.md`; revise prose manually if changing the analysis.

The CSVs preserve data used to verify the graphics: `life_selected.csv`, `county_growth.csv`, `growth_category_counts.csv`, `recovery_changes.csv`, and `education_complete.csv`. `contact-sheet.png` is a visual inspection intermediate made from the final render; the separate PNGs are the authoritative deliverables.

County input uses Windows-1252 decoding. See question 20 in the response and script for precise filtering, denominator and missing-data rules. All sources were local; `answers/sources.txt` records that no web pages were opened.
