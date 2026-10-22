"""Story 1, primary: female-minus-male life expectancy gap over time, all countries, with highlights."""
from common import *

p = load_wb()
q = p[p.is_country].dropna(subset=["gap"])
stats = q.groupby("Year").gap.quantile([0.25, 0.5, 0.75]).unstack()

HL = [("Russian Federation", "Russia", ORANGE, 10.7),
      ("United States", "United States", BLUE, 6.1),
      ("India", "India", AQUA, 1.5)]

fig = plt.figure(figsize=(10, 7.2))
ax = fig.add_axes([0.08, 0.2, 0.74, 0.66])

for _, d in q.groupby("Country Name"):
    ax.plot(d.Year, d.gap, color="#d8d7d2", lw=0.45, alpha=0.5, zorder=1)
ax.fill_between(stats.index, stats[0.25], stats[0.75], color="#a9a8a2", alpha=0.45, lw=0, zorder=2)
ax.plot(stats.index, stats[0.5], color=INK, lw=2.2, zorder=4)
ax.axhline(0, color=INK2, lw=1, zorder=3)
ax.text(2022.5, -0.35, "below 0 = men outlive women", ha="right", fontsize=8.5, color=INK2, va="top")

for name, lab, col, ly in HL:
    d = q[q["Country Name"] == name]
    ax.plot(d.Year, d.gap, color=col, lw=2.2, zorder=5)
    ax.text(2024.6, ly, lab, color=INK, fontsize=10, va="center", fontweight="bold")
    ax.plot([2023.2, 2024.3], [d.gap.iloc[-1], ly], color=col, lw=2.2, clip_on=False)
ly = 4.6
ax.plot([2023.2, 2024.3], [stats[0.5].iloc[-1], ly], color=INK, lw=2.2, clip_on=False)
ax.text(2024.6, ly, "Median country", fontsize=10, va="center", fontweight="bold")
ax.text(2024.6, ly - 0.55, "(gray band: middle\n50% of countries)", fontsize=8.5, color=INK2, va="top")

# annotations for the stories inside the exceptions
def note(x, y, tx, ty, s):
    ax.annotate(s, (x, y), (tx, ty), fontsize=8.5, color=INK2,
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8), va="center")

r = q[q["Country Name"] == "Russian Federation"].set_index("Year").gap
note(1994, r[1994], 1997, 17.5, "Russia 1994: women outlive men by 14 years\nafter the post-Soviet male mortality crisis")
i = q[q["Country Name"] == "India"].set_index("Year").gap
note(1982, i[1982], 1986, -2.6, "India: men outlived women until ~1982")
note(1974, 26.6, 1977, 25.8, "War spikes: Cyprus 1974")
note(1993, 22.6, 1998, 22.6, "Bosnia 1993")
note(2023, 13.3, 2009, 15.5, "Ukraine 2023")

ax.set_xlim(1960, 2023)
ax.set_ylim(-5, 28)
ax.set_ylabel("Female minus male life expectancy at birth (years)")
ax.set_yticks(range(-5, 30, 5))

title_block(fig, "Women outlive men by about 5 years, a gap that has barely changed since 1960 —\nbut the exceptions tell stories of crisis and war",
            "Female minus male life expectancy at birth, 217 countries, 1960–2023 (each thin gray line is one country)", gap=0.075)
caption(fig, "The median country's gap rose only from 4.1 to 5.0 years, and countries have become more alike: in 1960 five countries "
             "(India, Pakistan, Bangladesh, Iran, North Macedonia)\nhad men outliving women; by 2023 none did. "
             "The big exceptions are the former Soviet bloc, where male life expectancy stagnated (Russia's gap peaked at 14 years), and wars,\n"
             "which kill mostly men and produce short spikes. The U.S. gap peaked near 8 years around 1970 and has since narrowed.\n"
             "Data: World Bank (SP.DYN.LE00), via CS765 765Data repository. Regional/income aggregates excluded.")
save(fig, "q1a_gender_gap_lines.png")
