"""Story 3: COVID-era life-expectancy losses (2019 -> 2021) and recovery by 2023."""
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from common import *
style()
l = wb()
b = l[l.Sex == "Both"].pivot(index="country", columns="Year", values="le")
d = pd.DataFrame({"y19": b[2019], "y21": b[2021], "y23": b[2023]}).dropna()
d["drop"] = d.y21 - d.y19
top = d.sort_values("drop").head(25).iloc[::-1]   # biggest loss at the top
latam = {"Bolivia", "Paraguay", "Mexico", "Guyana", "Peru", "Ecuador", "Cuba", "Colombia",
         "Guatemala", "Nicaragua", "Argentina", "St. Lucia"}
print(top.round(1)); print("share lost:", (d["drop"] < 0).mean(), "median", d["drop"].median())
n_rec = ((top.y23 >= top.y19 - 0.05)).sum(); print("recovered", n_rec, "of", len(top))

fig, ax = plt.subplots(figsize=(9.5, 8.6))
for i, (k, r) in enumerate(top.iterrows()):
    c = ORANGE if k in latam else BLUE
    ax.plot([r.y21, r.y19], [i, i], color=c, lw=1.5, alpha=.45, zorder=1)
    ax.scatter(r.y19, i, s=55, facecolor="white", edgecolor=c, lw=1.8, zorder=3)
    ax.scatter(r.y21, i, s=60, color=c, zorder=3)
    ax.scatter(r.y23, i, s=60, marker="D", color="#222222", zorder=4, linewidth=0)
    ax.text(r.y21 - .7, i, f"{r['drop']:.1f}", ha="right", va="center", fontsize=8.5, color=c)
ax.set_yticks(range(len(top))); ax.set_yticklabels([k.replace("Russian Federation", "Russia").replace("Iran, Islamic Rep.", "Iran").replace("Slovak Republic", "Slovakia") for k in top.index])
for t, k in zip(ax.get_yticklabels(), top.index):
    t.set_color(ORANGE if k in latam else BLUE)
ax.set_xlim(52, 87); ax.set_ylim(-0.8, len(top) - 0.2)
ax.set_xlabel("Life expectancy at birth, both sexes (years)")
ax.xaxis.grid(True, color="#eeeeee"); ax.set_axisbelow(True)
h = [plt.Line2D([], [], marker="o", ls="", mfc="white", mec="#555555", mew=1.8, ms=8, label="2019 (before)"),
     plt.Line2D([], [], marker="o", ls="", color="#555555", ms=8, label="2021 (low point)"),
     plt.Line2D([], [], marker="D", ls="", color="#222222", ms=7, label="2023 (latest)"),
     plt.Line2D([], [], color=ORANGE, lw=6, alpha=.6, label="Latin America & Caribbean"),
     plt.Line2D([], [], color=BLUE, lw=6, alpha=.6, label="Other")]
ax.legend(handles=h, loc="lower left", frameon=False, fontsize=9.5)
fig.suptitle("COVID-era life-expectancy losses hit Latin America hardest, and nearly all recovered by 2023",
             x=0.02, ha="left", fontsize=13.5, fontweight="bold", y=0.995)
ax.set_title("The 25 countries with the largest drop in life expectancy from 2019 to 2021 (labels = years lost)",
             loc="left", fontsize=10, color="#444444", fontweight="normal")
fig.text(0.02, 0.005,
         f"Across {len(d)} countries, {100*(d['drop']<0).mean():.0f}% lost life expectancy from 2019 to 2021 (median change {d['drop'].median():.1f} years). 8 of the 10 biggest losers are in\n"
         f"Latin America & the Caribbean. Of the 25 shown, {n_rec} were back to their 2019 level by 2023 (within 0.05 years); Lebanon and North Macedonia were not.\n"
         "Ranked by 2019-21 change. Data: World Bank life expectancy at birth, both sexes.",
         fontsize=9, color="#444444", va="top")
save(fig, "q3_covid_losses.png")
