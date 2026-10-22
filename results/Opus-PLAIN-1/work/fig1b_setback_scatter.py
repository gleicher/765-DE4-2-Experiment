"""Figure 1b: every country's pandemic loss (years of life expectancy) vs. years of progress erased."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from common import setup_style, FIG, INK, INK2, MUTED, ORANGE, BLUE
from q1_data import q1_table

setup_style()
t, _ = q1_table()
t = t[t.country != "Central African Republic"].copy()
t.loc[t.loss <= 0, "yrs_erased"] = 0
t["recovered"] = t.rec >= 0
rng = np.random.default_rng(3)
t["yj"] = t.yrs_erased + rng.uniform(-0.35, 0.35, len(t))

n = len(t)
n_loss1 = (t.loss >= 1).sum()
n_10 = (t.yrs_erased >= 10).sum()
n_rec = t.recovered.sum()
n_rec_hit = (t.recovered & (t.yrs_erased >= 10)).sum()

fig, ax = plt.subplots(figsize=(10, 7.6))
for rec, col, z in [(True, BLUE, 3), (False, ORANGE, 4)]:
    d = t[t.recovered == rec]
    ax.scatter(d.loss, d.yj, s=34, color=col, alpha=0.85, edgecolor="white", linewidth=0.8, zorder=z)

LABELS = {  # country: (dx, dy, ha) offsets in points
    "Jamaica": (8, 0, "left"), "Cuba": (8, 0, "left"), "St. Lucia": (8, 0, "left"),
    "St. Vincent and the Grenadines": (-8, 0, "right"), "Fiji": (-8, 0, "right"),
    "Bahamas, The": (-8, 0, "right"), "Andorra": (-8, 6, "right"), "Mexico": (6, -10, "left"),
    "Paraguay": (8, 0, "left"), "Philippines": (8, 0, "left"), "United States": (0, -13, "center"),
    "Bolivia": (0, 11, "center"), "Ecuador": (8, -2, "left"), "Lebanon": (-4, 10, "center"),
    "Peru": (8, 0, "left"), "India": (8, 0, "left"), "Russian Federation": (-8, 0, "right"),
    "South Africa": (8, 0, "left"), "Botswana": (8, 0, "left"), "Japan": (-8, 6, "right"),
}
SHORT = {"Russian Federation": "Russia", "St. Vincent and the Grenadines": "St. Vincent & Grenadines",
         "Bahamas, The": "Bahamas"}
for c, (dx, dy, ha) in LABELS.items():
    r = t[t.country == c]
    if r.empty:
        print("missing", c); continue
    r = r.iloc[0]
    ax.scatter([r.loss], [r.yj], s=34, facecolor="none", edgecolor=INK, linewidth=0.9, zorder=6)
    ax.annotate(SHORT.get(c, c), (r.loss, r.yj), xytext=(dx, dy), textcoords="offset points",
                fontsize=8.5, color=INK, ha=ha, va="center", zorder=7)

ax.set_xlabel("Life expectancy lost: 2019 level minus pandemic low (2020–22), in years")
ax.set_ylabel("Years of progress erased\n(2019 minus the last year life expectancy was that low)")
ax.set_xlim(-1.2, 7.2)
ax.set_ylim(-2, 42)
ax.axvline(0, color=MUTED, lw=0.8)
ax.text(-0.1, 41, "no pandemic\ndrop ←", ha="right", va="top", fontsize=8, color=MUTED)

# guide lines: same drop, different setback
ax.annotate("The setback depends on how fast a\ncountry had been improving: Jamaica's\n2.4-year drop erased 39 years of slow\nprogress; Botswana's larger 3.9-year\ndrop erased only 4 years of rapid gains.",
            xy=(4.75, 35.3), fontsize=8.5, color=INK2, ha="left", va="top")

handles = [Line2D([], [], marker="o", ls="", color=BLUE, markersize=7, label=f"Back at or above 2019 level by 2023 ({n_rec})"),
           Line2D([], [], marker="o", ls="", color=ORANGE, markersize=7, label=f"Still below 2019 level in 2023 ({n - n_rec})")]
ax.legend(handles=handles, loc="upper right", frameon=False, fontsize=9.5, bbox_to_anchor=(1.0, 1.0))

fig.suptitle("How far back did COVID-19 push each country's life expectancy — and did it recover?",
             x=0.01, ha="left", y=0.985, fontsize=15, fontweight="bold")
fig.text(0.01, 0.935,
         f"Each dot is one of {n} countries. {n_loss1} lost at least a year of life expectancy during 2020–22, and for {n_10} the low point\n"
         f"matched a level last seen 10 or more years earlier. Yet {n_rec} of {n} were back at or above their 2019 level by 2023.",
         fontsize=10, color=INK2, ha="left", va="top")
fig.text(0.01, 0.012,
         "Dots are jittered vertically by up to ±0.35 to reduce overlap. Central African Republic omitted (implausible series: 31.5 → 50.6 → 18.8 years).\n"
         "Data: World Bank life expectancy at birth, both sexes, 1960–2023 (CS765 dataset); regional aggregates removed.",
         fontsize=8.3, color=MUTED, ha="left", va="bottom")
fig.subplots_adjust(left=0.1, right=0.98, top=0.86, bottom=0.13)
fig.savefig(FIG / "q1b_pandemic_setback_scatter.png")
print(n, n_loss1, n_10, n_rec, n_rec_hit)
print(t[t.country.isin(["Botswana", "Jamaica", "Japan"])][["country", "loss", "yrs_erased", "rec"]])
