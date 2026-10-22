"""Figure 4: years each country took to go from life expectancy 50 to 70, by when it reached 50."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from common import setup_style, FIG, INK, INK2, MUTED, BLUE, ORANGE
from q4_data import q4_table

setup_style()
t = q4_table()
done = t[t.status == "reached"]
nyet = t[t.status == "not yet"]

fig, ax = plt.subplots(figsize=(11, 7.6))
xs = np.array([1840, 2030])
ax.fill_between(xs, 2023 - xs, 120, color="#f2f1ee", lw=0, zorder=0)
ax.plot(xs, 2023 - xs, color=MUTED, lw=0.9, zorder=1)
ax.text(2021, 64, "Shaded: not observable yet\n(the data end in 2023, so every\n'not yet' country sits on this edge)",
        fontsize=8.3, color=MUTED, ha="right", va="top")

ax.scatter(done.y50, done.years, s=36, color=BLUE, edgecolor="white", linewidth=0.8, zorder=3)
ax.scatter(nyet.y50, nyet.years, s=34, facecolor="white", edgecolor=ORANGE, linewidth=1.5, zorder=3)
for _, r in nyet.iterrows():
    ax.annotate("", xy=(r.y50, r.years + 4.2), xytext=(r.y50, r.years + 0.9),
                arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=0.8, mutation_scale=6), zorder=2)

LAB = {  # country: (dx, dy, ha) in points
    "Norway": (8, 0, "left"), "Sweden": (8, 2, "left"), "United States": (8, 2, "left"),
    "United Kingdom": (-6, -9, "left"), "Japan": (8, 0, "left"), "South Korea": (-8, -6, "right"),
    "China": (8, -3, "left"), "India": (8, 2, "left"), "Brazil": (8, 0, "left"),
    "Hungary": (8, 0, "left"), "Bahrain": (0, -11, "center"),
    "Zimbabwe": (-8, 0, "right"), "South Africa": (-8, 0, "right"), "Nigeria": (8, 3, "left"),
    "Bangladesh": (8, -2, "left"), "Algeria": (8, -3, "left"), "Ethiopia": (-6, 9, "right"),
    "Argentina": (8, 0, "left"), "Italy": (0, -11, "center"),
}
for c, (dx, dy, ha) in LAB.items():
    r = t[t.country == c]
    if r.empty:
        print("missing", c); continue
    r = r.iloc[0]
    ax.annotate(c, (r.y50, r.years), xytext=(dx, dy), textcoords="offset points",
                fontsize=8.5, color=INK, ha=ha, va="center", zorder=5)

ax.text(1853, 86, "Pioneers took 45–95 years", fontsize=9.5, color=INK2, fontweight="bold")
ax.text(1853, 84.6, "Norway, Sweden and the US needed most of a\ncentury, inching up before modern medicine",
        fontsize=8.6, color=INK2, va="top")
ax.text(1912, 9, "Fast followers: as little as 17–30 years", fontsize=9.5, color=INK2, fontweight="bold")
ax.text(1912, 7.4, "Japan, South Korea, China and Bahrain caught up with tools the pioneers had to invent",
        fontsize=8.6, color=INK2, va="top")
ax.text(2013, 88.5, f"Still waiting: {len(nyet)} countries", fontsize=9.5, color="#b8461a",
        fontweight="bold", ha="right")
ax.text(2013, 87.0, "reached 50 but not 70 by 2023 — many in\nsouthern Africa, held back by HIV/AIDS since\nthe 1990s, have been waiting 60+ years",
        fontsize=8.6, color=INK2, va="top", ha="right")

ax.set_xlim(1845, 2025)
ax.set_ylim(0, 105)
ax.set_xlabel("Year the country first reached a life expectancy of 50")
ax.set_ylabel("Years it took to go from 50 to 70")
handles = [Line2D([], [], marker="o", ls="", color=BLUE, mec="white", ms=7, label=f"Reached 70 ({len(done)} countries)"),
           Line2D([], [], marker="o", ls="", mfc="white", mec=ORANGE, mew=1.5, ms=7,
                  label=f"Not yet at 70 in 2023 — years so far ({len(nyet)})")]
ax.legend(handles=handles, loc="upper right", frameon=False, fontsize=9.5)

fig.suptitle("Climbing from 50 to 70 years of life expectancy got faster — for most",
             x=0.01, ha="left", y=0.985, fontsize=15.5, fontweight="bold")
fig.text(0.01, 0.935,
         "Each dot is a country, placed by when its life expectancy first reached 50 and how long it then took to reach 70. Countries that\n"
         "reached 50 after 1920 typically needed 30–45 years rather than 50–60 — but a large group that reached 50 after 1950 has not made it.",
         fontsize=10, color=INK2, ha="left", va="top")
fig.text(0.01, 0.012,
         "Crossing years are interpolated between observations no more than 10 years apart; countries already above 50 in their first recorded year,\n"
         "or with too-sparse data around a crossing, are omitted. Period life expectancy at birth. Data: Our World in Data (CS765 dataset), historical estimates to 2023.",
         fontsize=8.2, color=MUTED, ha="left", va="bottom")
fig.subplots_adjust(left=0.075, right=0.985, top=0.86, bottom=0.13)
fig.savefig(FIG / "q4_life_expectancy_50_to_70.png")
print(done.sort_values("years")[["country", "y50", "years"]].head(8).round(1).to_string())
