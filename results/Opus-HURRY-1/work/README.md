# work/ — how the DE4-2 figures were made

**Tools:** Python 3.14 (`/opt/anaconda3/envs/p314/bin/python`) with pandas and matplotlib.
No other packages and no manual steps: each script writes one PNG (200 dpi) straight
to `answers/figures/`. Text, labels, and captions are all drawn in code.

| Script | Output | Data |
|---|---|---|
| `fig1a_gap_lines.py` | `q1a_gender_gap_lines.png` | World Bank life expectancy by sex |
| `fig1b_male_female_scatter.py` | `q1b_male_vs_female_paths.png` | World Bank life expectancy by sex |
| `fig2a_unemployment_lines.py` | `q2a_unemployment_rural_urban_lines.png` (+ `q2_unemployment_by_group.csv`) | USDA county data |
| `fig2b_unemployment_strips.py` | `q2b_unemployment_county_strips.png` (+ `q2b_strip_summary.csv`) | USDA county data |
| `fig3_migration_by_size.py` | `q3_migration_by_county_size.png` (+ `q3_migration_by_size.csv`) | USDA county data |
| `fig4_climb_50_to_70.py` | `q4_climb_50_to_70.png` (+ `q4_climb_50_to_70.csv`) | OWID long-run life expectancy |

`common.py` holds the paths, palette, matplotlib style, title/caption helpers, and data loaders
(the World Bank aggregate-code list, the county cleaning and rural-urban grouping).

## Regenerate

```sh
cd work
for f in fig*.py; do /opt/anaconda3/envs/p314/bin/python -W ignore "$f"; done
```

Notes:
- The county CSV is Latin-1 encoded. The loader drops state/US summary rows (FIPS ending in 000)
  and Puerto Rico. Connecticut's former counties fall back to their 2013 rural-urban code.
- The jitter in fig2b uses a fixed random seed (7), so it is reproducible.
- The categorical colors (#2a78d6, #eb6834, #1baf7a) were checked with the dataviz skill's
  `validate_palette.js` (all checks pass, adjacent and all-pairs). This is a one-time check,
  not part of regeneration.
