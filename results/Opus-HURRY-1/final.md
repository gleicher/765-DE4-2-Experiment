The assignment is done: six figures, answers to all 20 Canvas questions, a sources file, and the scripts in work/. Before you submit, read the course AI policy note below.

**The policy issue:** the class's GenAI policy (reference/genai-policies.md) says what you turn in should be your own work, the critique should be your own opinion, and AI help must be disclosed. I didn't hide that:
- Q20 in answer.md says plainly that Claude made the figures, wrote the code and drafted all the written answers, including the critique.
- A note at the top of answer.md (not part of any answer) says the same thing.

I'd strongly suggest rewriting at least the critique (Q1) and the rationales in your own words. If you do, update Q20 so it still accurately says who did what.

**The four stories:**
- **Q1 (World Bank life expectancy):** women outlive men by about 5 years in the median country, and that hasn't changed much since 1960. The exceptions are Russia and the former Soviet bloc (gaps of 10–14 years), India (men outlived women until about 1982), and short spikes during wars.
  - Primary figure: the female-minus-male gap over time for 217 countries, with Russia, the U.S. and India in color.
  - Alternate figure: male vs. female life expectancy, tracing each of those three countries' path from 1960 to 2023.
- **Q2 (census):** for 20 years rural counties had higher unemployment than big metros. In 2020 that flipped (large metros 3.5% → 8.6%, most rural 4.2% → 6.5%), and by 2022 every type of county was back to about 3.6–3.7%.
  - Primary figure: lines for five rural–urban groups, plus a bar panel showing the big-metro minus rural difference.
  - Alternate figure: one dot per county (3,102), showing the change 2019→2020 and 2019→2022.
- **Q3 (census):** from mid-2020 to mid-2023, counties with 500k+ people lost a net 2.8M residents to the rest of the U.S. and gained 1.8M from abroad. The chart compares those two flows by county size.
- **Q4 (Our World in Data long-run life expectancy):** how many years each country took to go from life expectancy 50 to 70. Norway took 93 years and Japan 17. Many countries that reached 50 after 1975 are still below 70, and the chart shows those separately rather than dropping them.

**Things to check before submitting:**
- **Q4 numbers:** the years when each country first reached 50 and 70 are estimated between data points, and data before 1900 is sparse, so those early years are approximate. The caption says so.
- **Connecticut (Q2):** the 2023 rural–urban codes only cover Connecticut's new planning regions, which have no unemployment data. I used the 2013 codes for its 8 old counties instead.
- **Event names:** names like "post-Soviet mortality crisis" and "HIV/AIDS" in the figure notes come from general knowledge. No outside data was added.

I didn't open any web pages, so sources.txt says so and lists only the local files and the original data sources from the readmes. I didn't install anything; only pandas and matplotlib were used, through the p314 Python. To regenerate everything, run each `fig*.py` script in work/ (the README has the command). There are no manual steps, and I've checked the full regeneration runs cleanly.

Files are in /Users/mlgleich/Projects/765/765-DE4-2-Experiment/runs/Opus-HURRY-1/:
- answers/answer.md
- answers/sources.txt
- answers/figures/ (q1a_gender_gap_lines.png, q1b_male_vs_female_paths.png, q2a_unemployment_rural_urban_lines.png, q2b_unemployment_county_strips.png, q3_migration_by_county_size.png, q4_climb_50_to_70.png)
- work/README.md, work/common.py, work/fig*.py, plus the summary CSVs
