"""Q4: how many years of life-expectancy progress did the COVID-era trough erase, and was it regained?"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from common import *

style()
o = load_owid()
o = o[o["Code"].notna()]
w = o.pivot(index="Entity", columns="Year", values="le")
w = w[list(range(1950, 2024))].dropna()
countries = [e for e in w.index if not str(o[o.Entity == e]["Code"].iloc[0]).startswith("OWID")]

def setback(e):
    s = w.loc[e]
    trough_year = int(s[[2020, 2021, 2022]].idxmin())
    trough = s[trough_year]
    before = s.loc[:2019]
    last_as_low = before[before <= trough]
    back_to = int(last_as_low.index.max()) if len(last_as_low) else np.nan
    return dict(entity=e, le2019=s[2019], trough_year=trough_year, trough=trough,
                drop=s[2019] - trough, back_to=back_to, le2023=s[2023],
                vs2019=s[2023] - s[2019])

d = pd.DataFrame([setback(e) for e in countries]).set_index("entity")
d.to_csv(Path(__file__).parent / "out_fig4_setbacks_all.csv", float_format="%.2f")
# Central African Republic shows a 12-year one-year collapse in 2022 in this series (conflict/data
# artifact, not COVID); exclude it so it doesn't dominate.
d = d.drop(index="Central African Republic")
top = d.sort_values("drop", ascending=False).head(20)
ref = pd.DataFrame([setback(e) for e in ["World", "United States"]]).set_index("entity")
show = pd.concat([top.sort_values("back_to"), ref])
print(show.round(2))

n_drop = (d["drop"] >= 1).sum()
n_rec = ((d["drop"] >= 1) & (d["vs2019"] >= 0)).sum()

fig = plt.figure(figsize=(12, 8.2))
ax = fig.add_axes([0.17, 0.2, 0.52, 0.63])
bx = fig.add_axes([0.73, 0.2, 0.22, 0.63], sharey=ax)

ypos = {e: i + (0.8 if e in ref.index else 0) for i, e in enumerate(show.index)}
for e, r in show.iterrows():
    y = ypos[e]
    isref = e in ref.index
    col = INK2 if isref else RED
    ax.plot([r["back_to"], 2019], [y, y], color=col, lw=5 if not isref else 3.5, alpha=0.85,
            solid_capstyle="butt", zorder=2)
    ax.scatter([r["back_to"]], [y], s=34, color=col, zorder=3, edgecolor="white", lw=1)
    ax.text(r["back_to"] - 0.8, y, f"{int(r['back_to'])}", ha="right", va="center", fontsize=8.6,
            color=INK2)
    ax.text(2020.2, y, f"{int(2019 - r['back_to'])} yrs", ha="left", va="center", fontsize=8.8,
            color=INK, fontweight="bold" if not isref else "normal")
    # right panel: change vs 2019 at trough and in 2023
    bx.plot([-r["drop"], r["vs2019"]], [y, y], color=LIGHTGRAY, lw=2, zorder=1)
    bx.scatter([-r["drop"]], [y], s=34, color=RED if not isref else INK2, zorder=3,
               edgecolor="white", lw=1)
    bx.scatter([r["vs2019"]], [y], s=34, color=BLUE if not isref else INK2, zorder=3,
               marker="D", edgecolor="white", lw=1)

ax.set_yticks(list(ypos.values()))
ax.set_yticklabels(list(ypos.keys()), fontsize=9.5)
for lab in ax.get_yticklabels():
    if lab.get_text() in ref.index:
        lab.set_color(INK2); lab.set_style("italic")
ax.tick_params(axis="y", length=0)
ax.set_ylim(max(ypos.values()) + 0.7, -1.0)
ax.set_xlim(1975, 2024)
ax.set_xticks(range(1975, 2021, 5))
ax.axvline(2019, color=INK2, lw=0.8)
ax.grid(axis="x"); ax.set_axisbelow(True)
ax.spines["left"].set_visible(False)
ax.set_xlabel("Year when life expectancy was last as low as at the pandemic trough")
ax.text(1975, -2.05, "Progress erased", fontsize=11.5, fontweight="bold", color=INK, va="bottom")
ax.text(1975, -1.4, "red bar runs from the year whose level the trough matched, to 2019",
        fontsize=8.8, color=INK2, va="bottom")
ax.text(2019.4, -0.75, "2019", fontsize=8.5, color=INK2, ha="left", va="bottom")

bx.axvline(0, color=INK2, lw=0.8)
bx.set_xlim(-7, 2.5)
bx.set_xticks([-6, -4, -2, 0, 2])
bx.xaxis.set_major_formatter(lambda v, p: f"{v:+.0f}" if v else "0")
bx.grid(axis="x"); bx.set_axisbelow(True)
bx.spines["left"].set_visible(False)
bx.tick_params(axis="y", length=0, labelleft=False)
bx.set_xlabel("Life expectancy vs. 2019 (years)")
bx.text(-7, -2.05, "Drop and recovery", fontsize=11.5, fontweight="bold", color=INK, va="bottom")
bx.text(-7, -1.4, "change in life expectancy relative to 2019", fontsize=8.8, color=INK2, va="bottom")
bx.scatter([-6.6], [-0.55], s=30, color=RED); bx.text(-6.3, -0.55, "trough (2020-22)", fontsize=8.4,
                                                     va="center", color=INK2)
bx.scatter([-1.6], [-0.55], s=30, color=BLUE, marker="D"); bx.text(-1.3, -0.55, "2023", fontsize=8.4,
                                                                  va="center", color=INK2)

title_block(fig, "COVID-19 erased decades of gains in life expectancy, but most were won back by 2023",
            f"The 20 countries and territories with the largest pandemic-era drops. At the trough, life expectancy fell "
            f"back to its level of {int(top.back_to.min())}-{int(top.back_to.max())}\n(a median of {int((2019 - top.back_to).median())} years of progress erased). Of the {n_drop} places that lost a year or more, "
            f"{n_rec} were back at or above their 2019 level by 2023.")
caption(fig,
        "Trough = lowest life expectancy at birth in 2020, 2021 or 2022. \"Years erased\" = 2019 minus the last "
        "year before 2019 in which life expectancy was at or below the trough value (countries that improved "
        "slowly before 2019 lose more calendar years for the same drop, e.g. Cuba). Shows the 20 largest drops, "
        "sorted by years erased; World and United States shown for reference. Central African Republic "
        "excluded: its series drops 12.7 years in 2022, far beyond any other country, and is not clearly a pandemic effect.\n"
        "Data: Our World in Data life expectancy (UN World Population Prospects 2024 for 1950 onward) "
        "(CS765 life-expectancy-owid.csv).",
        chars=170)
fig.savefig(FIG / "q4_covid_setback.png")
