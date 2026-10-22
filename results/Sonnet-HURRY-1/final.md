I made the six figures and wrote answers 1–20, but none of it is the student's own work yet. The course AI policy says not to turn in AI work as your own, so you'll need to rewrite it before submitting.

Everything is in `/Users/mlgleich/Projects/765/765-DE4-2-Experiment/runs/Sonnet-HURRY-1/`.

**What's there**
- `answers/answer.md` has all 20 Canvas answers, numbered in Canvas order.
- `answers/figures/` has the six PNGs, each with a title, subtitle and caption in the image. I checked each one visually and fixed label overlaps.
- `answers/sources.txt` says no web pages were opened. It lists the data-source URLs from the READMEs for citing.
- `work/` has `make_figs.py` (builds all the figures), `explore.py`, three small CSV summaries, and `README.md`.
- To regenerate, run `/opt/anaconda3/envs/p314/bin/python -I make_figs.py` from `work/`. There are no manual steps, and nothing was installed (pandas and matplotlib were already in `p314`).

**The stories**
- **Q1 (life expectancy, World Bank):** how the female-minus-male gap changed from 1960 to 2023.
  - Version A: a scatterplot of 1960 gap against 2023 gap for each country, with a no-change diagonal.
  - Version B: gap-over-time lines for six countries, against the middle-half band of all countries.
- **Q2 (census):** the bachelor's degree share by rural-urban code, 1990 to 2019-23. The metro/rural gap widened from 13 to 20 points.
  - Version A: lines for the nine rural-urban codes.
  - Version B: a county scatterplot, 1990 against 2019-23.
- **Q3 (census):** unemployment by county type, 2000–2023. The 2020 jump was +4.6 points for metro counties, against +3.0 and +2.8 for the two nonmetro groups.
- **Q4 (Our World in Data):** how often life expectancy falls year to year, and the biggest drops. 68% of countries fell in 2020 and 71% in 2021, against about 11% in a typical year.

**Before you submit**
- **Answer 20, AI disclosure:** it says the AI wrote the analysis, code and text. Edit it to say what you actually did, and keep the disclosure.
- **Answer 1, critique:** I wrote the non-CLO version, a critique of `to-critique.png`. If you were in the CLO, replace it with the name of the person who critiqued you and one sentence on how helpful it was.
- **Rationales and comparisons:** reword them into your own voice.
- **Source quirks:**
  - Regional aggregates are removed from the World Bank data. I kept only country codes that also appear in the OWID file with a real ISO code.
  - The census file is comma-separated, not tab-separated as the README says. It needs latin-1 encoding.
  - The OWID file includes some territories as well as countries.
  - The Central African Republic 2009 drop of 35 years looks like source estimation noise. The Q4 caption says so.
