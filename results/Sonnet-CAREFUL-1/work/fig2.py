"""Story 2: college attainment by county type, 1990 -> 2019-23.
q2_a: lines by 4 county groups; q2_b: dumbbell by all 9 RUCC codes."""
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from common import *
style()
c = census()
P = "Percent of adults with a bachelor's degree or higher, "
periods = ["1990", "2000", "2008-12", "2019-23"]
xs = [1990, 2000, 2010, 2021]
c["rucc"] = c["2023 Rural-urban Continuum Code"]
c = c.dropna(subset=["rucc"])
grp = {1: "Large metro (1M+ people)", 2: "Smaller metro", 3: "Smaller metro",
       4: "Nonmetro, urban (20k+)", 5: "Nonmetro, urban (20k+)"}
c["grp"] = c.rucc.map(lambda r: grp.get(r, "Nonmetro, small town / rural (<20k)"))
order = ["Large metro (1M+ people)", "Smaller metro", "Nonmetro, urban (20k+)", "Nonmetro, small town / rural (<20k)"]
colors = dict(zip(order, [BLUE, GREEN, ORANGE, PURPLE]))
cols = [P + p for p in periods]
print(c.groupby("grp")[cols].median().round(1).loc[order])
print(c.groupby("grp").size())

# ---- A ----
fig, ax = plt.subplots(figsize=(10, 6.4))
for g in order:
    sub = c[c.grp == g]
    med = [sub[k].median() for k in cols]
    q1 = [sub[k].quantile(.25) for k in cols]; q3 = [sub[k].quantile(.75) for k in cols]
    ax.fill_between(xs, q1, q3, color=colors[g], alpha=.13, lw=0)
    ax.plot(xs, med, color=colors[g], lw=2.6, marker="o", ms=6)
    ax.text(2022, med[-1] + {order[2]: 0.9, order[3]: -1.2}.get(g, 0), f"{g}\n{med[-1]:.0f}%  (was {med[0]:.0f}% in 1990)", color=colors[g],
            fontsize=9.5, va="center", fontweight="bold")
ax.set_xlim(1988, 2037); ax.set_ylim(0, 45)
ax.set_xticks(xs); ax.set_xticklabels(["1990", "2000", "2008-12", "2019-23"])
ax.set_ylabel("Adults with a bachelor's degree or higher (%)")
ax.yaxis.grid(True, color="#eeeeee"); ax.set_axisbelow(True)
m0 = c[c.grp == order[0]][cols[0]].median() - c[c.grp == order[3]][cols[0]].median()
m1 = c[c.grp == order[0]][cols[-1]].median() - c[c.grp == order[3]][cols[-1]].median()
print("gap", m0, m1)
ax.annotate("", xy=(2021, c[c.grp == order[0]][cols[-1]].median()), xytext=(2021, c[c.grp == order[3]][cols[-1]].median()), arrowprops=dict(arrowstyle="<->", color="#444444"))
ax.text(2019.7, 35.5, f"Gap between large metro\nand small-town/rural:\n{m0:.0f} pts in 1990 → {m1:.0f} pts now",
        fontsize=9.5, ha="right", color="#333333")
fig.suptitle("Every kind of county gained college graduates, but large metros pulled away",
             x=0.02, ha="left", fontsize=14, fontweight="bold", y=1.0)
ax.set_title("Median share of adults with a bachelor's degree, by county type (line) and middle half of counties (band)",
             loc="left", fontsize=10, color="#444444", fontweight="normal")
fig.text(0.02, -0.015,
         "Each line is the median of the counties in that group (n = %s); bands span the 25th to 75th percentile. County types follow the USDA 2023\n"
         "Rural-urban Continuum Code. Counties are unweighted, so small rural counties count as much as big ones. Data: USDA ERS county data via course file." %
         "/".join(str(v) for v in c.groupby("grp").size().loc[order]), fontsize=9, color="#444444", va="top")
save(fig, "q2_a_education_lines.png")

# ---- B ----
labels = {1: "1  Metro, 1M+", 2: "2  Metro, 250k-1M", 3: "3  Metro, <250k",
          4: "4  Nonmetro urban 20k+, next to metro", 5: "5  Nonmetro urban 20k+, remote",
          6: "6  Nonmetro 5-20k, next to metro", 7: "7  Nonmetro 5-20k, remote",
          8: "8  Nonmetro <5k, next to metro", 9: "9  Nonmetro <5k, remote"}
fig, ax = plt.subplots(figsize=(10, 6.6))
for i, r in enumerate(range(1, 10)):
    sub = c[c.rucc == r]
    y = 9 - i
    a0, a1 = sub[cols[0]].median(), sub[cols[-1]].median()
    ax.plot([sub[cols[0]].quantile(.25), sub[cols[0]].quantile(.75)], [y + .17, y + .17], color=GREY, lw=4, alpha=.35, solid_capstyle="butt")
    ax.plot([sub[cols[-1]].quantile(.25), sub[cols[-1]].quantile(.75)], [y - .17, y - .17], color=BLUE, lw=4, alpha=.3, solid_capstyle="butt")
    ax.annotate("", xy=(a1, y), xytext=(a0, y), arrowprops=dict(arrowstyle="-|>", color="#555555", lw=1.4))
    ax.scatter([a0], [y], color=GREY, s=60, zorder=3); ax.scatter([a1], [y], color=BLUE, s=60, zorder=3)
    ax.text(a1 + 1.2, y, f"+{a1 - a0:.0f}", va="center", fontsize=9.5, color=BLUE, fontweight="bold")
ax.set_yticks(range(1, 10)); ax.set_yticklabels([labels[r] for r in range(9, 0, -1)])
ax.set_xlim(0, 45); ax.set_xlabel("Adults with a bachelor's degree or higher (%)")
ax.xaxis.grid(True, color="#eeeeee"); ax.set_axisbelow(True)
ax.scatter([], [], color=GREY, s=60, label="1990 median"); ax.scatter([], [], color=BLUE, s=60, label="2019-23 median")
ax.plot([], [], color=GREY, lw=4, alpha=.35, label="middle half of counties, 1990")
ax.plot([], [], color=BLUE, lw=4, alpha=.3, label="middle half of counties, 2019-23")
ax.legend(loc="lower right", frameon=False, fontsize=9)
fig.suptitle("Large-metro counties gained 17 points of college attainment; small rural counties gained 8-9",
             x=0.02, ha="left", fontsize=14, fontweight="bold", y=0.995)
ax.set_title("Change in median bachelor's-degree share, 1990 to 2019-23, for each of the nine USDA county types (numbers = points gained)",
             loc="left", fontsize=10, color="#444444", fontweight="normal")
fig.text(0.02, -0.015,
         "Counties are grouped by the USDA 2023 Rural-urban Continuum Code (1 = most urban, 9 = most rural). Code 5 contains only 76 counties, so its\n"
         "medians are noisier. Data: USDA ERS county-level education data, via course data file.", fontsize=9, color="#444444", va="top")
save(fig, "q2_b_education_dumbbell.png")
print({r: round(c[c.rucc==r][cols[-1]].median()-c[c.rucc==r][cols[0]].median(),1) for r in range(1,10)})
