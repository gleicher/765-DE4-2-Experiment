# Reproduce this submission draft

Tools: Python 3.14 from the existing `p314` environment, pandas, NumPy, Matplotlib, Pillow. No packages were installed. No network sources were used. All generated material is preserved here or in `../answers/`.

From this run's root directory:

```sh
/opt/anaconda3/envs/p314/bin/python work/make_figures.py > work/calculated_metrics.txt
/opt/anaconda3/envs/p314/bin/python work/validate.py > work/validation.txt
```

`make_figures.py` reads the original CSVs in `data/`, computes the derived tables in this directory, and writes the six PNG and matching SVG pages to `answers/figures/`. It sets a local Matplotlib cache in `work/.mplconfig/`, so nothing is written to the user's global configuration. The script does not download fonts. All exported images are 2850 × 1805 pixels; the SVGs are vector alternatives. Text bounds are checked before export. The titles, captions, labels, page layouts, selections, and annotations are encoded in the script; no post-export manual image editing is necessary.

`explore.py` preserves the preliminary exploration. Its exploratory education totals use variable-specific availability; the final chart instead uses a balanced complete-case panel. Use `education_shares.csv` and `calculated_metrics.txt` for final values, not exploratory prints.

Derived files:

- `life_selected.csv`: annual records for the six countries in story 1.
- `life_endpoint_metrics.csv`: sex gaps and both-sex gains.
- `growth_rates.csv`: county component rates, totals, and complete-record counts by code.
- `education_shares.csv`: complete-panel shares of four education categories.
- `recovery_metrics.csv`: baseline, trough deficit/year, first threshold recovery, and elapsed years.
- `calculated_metrics.txt`: readable final table output.
- `contact_sheet.png`: visual inspection preview (the final PNGs are authoritative).
- `validation.txt`: data and artifact checks.

Methods: County summary rows are excluded using FIPS modulo 1000, and Puerto Rico is excluded. Rates use mean 2022–2023 population and summed components. Education shares use summed counts and fixed 2023 classifications. Recovery means the first year at or above 1990 life expectancy after the minimum in 1990–2023; it is not causal inference or a measure of a counterfactual trend. See answer 20 for full processing and AI disclosure.

Manual steps before submission: inspect the images at normal viewing size; make the final story/design decisions; rewrite the critique and rationales to express the student's own understanding under `reference/genai-policies.md`; keep an accurate AI disclosure. Paste responses 1–20 in Canvas order and upload the corresponding PNG at questions 3, 5, 9, 11, 15, and 18. If the student participated in the CLO, replace answer 1 with the actual reviewer name and assessment of their feedback.
