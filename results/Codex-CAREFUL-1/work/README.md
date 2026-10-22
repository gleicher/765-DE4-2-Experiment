# Reproducing the figures

Run from this experiment directory:

```sh
/opt/anaconda3/envs/p314/bin/python work/make_figures.py
```

The script uses the existing pandas, NumPy, and Matplotlib packages in `p314`; it installs nothing. It reads only `data/lifespan_dataset_1960.csv` and `data/full_census_dataset.csv`, writes six 180-dpi static PNGs to `answers/figures/`, and retains derived CSV tables and `audit.json` here. Matplotlib's local cache stays in `work/mpl-cache/`. Paths are relative to the script's location, so the script can also be invoked from another directory.

Manual design decisions encoded in the script: six contrasting countries for the sex-gap comparison; seven countries with similar 2023 outcomes for the endpoint scatter; fixed 2013 rural–urban county groups and a complete-series employment cohort; 2023-code grouping for migration. These are illustrative choices, not random samples. No smoothing or image editing was applied. Captions, annotation placement, and axis ranges are specified in the script. The census CSV is comma-delimited and Windows-1252 encoded.

Pillow was used to create `contact_sheet.png` for visual review. It is an intermediate overview, not a seventh submitted visualization. To recreate it after rerunning the figures:

```sh
/opt/anaconda3/envs/p314/bin/python - <<'PY'
from PIL import Image, ImageDraw
from pathlib import Path
imgs = []
for p in sorted(Path('answers/figures').glob('*.png')):
    im = Image.open(p).convert('RGB')
    im.thumbnail((700, 550))
    tile = Image.new('RGB', (720, 580), '#eeeeee')
    tile.paste(im, ((720-im.width)//2, 20))
    ImageDraw.Draw(tile).text((10, 560), p.name, fill='black')
    imgs.append(tile)
out = Image.new('RGB', (1440, 1740), 'white')
for i, im in enumerate(imgs):
    out.paste(im, ((i%2)*720, (i//2)*580))
out.save('work/contact_sheet.png')
PY
```

Validation included checking country/year/sex and county FIPS uniqueness, checking complete employment series, comparing computed endpoints to the plots, and visually reviewing all six figures. No external pages were opened. AI assistance is explicitly described in answer 20. Before submitting, review and personalize the written judgments, consistent with the supplied course policy. Upload the six figures separately using the mapping in `answers/answer.md`.
