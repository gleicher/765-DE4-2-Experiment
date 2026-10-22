"""Q2 primary: unemployment rate 2000-2023 by USDA 2015 county economic type."""
import matplotlib.pyplot as plt
import pandas as pd

from common import *

style()
c = load_census()
c = c[c["Economic typology 2015"].notna()].copy()
c["type"] = c["Economic typology 2015"].astype(int).map(ECON_TYPES)
YEARS = list(range(2000, 2024))

# labor-force-weighted rate per type: total unemployed / total labor force
rate = pd.DataFrame({
    t: [100 * g[f"Unemployed {y}"].sum() / g[f"Civilian labor force {y}"].sum() for y in YEARS]
    for t, g in c.groupby("type")}, index=YEARS)
rate["All counties"] = [100 * c[f"Unemployed {y}"].sum() / c[f"Civilian labor force {y}"].sum() for y in YEARS]
rate.to_csv(Path(__file__).parent / "out_fig2_unemployment_by_type.csv", float_format="%.2f")
ncounty = c["type"].value_counts()

STYLE = {  # type -> color, emphasized?
    "Manufacturing": (BLUE, True),
    "Recreation": (ORANGE, True),
    "Mining": (AQUA, True),
    "Farming": (YELLOW, True),
    "Nonspecialized": (GRAY, False),
    "Federal/state government": ("#c2c1bb", False),
}

fig = plt.figure(figsize=(11, 7.2))
ax = fig.add_axes([0.07, 0.21, 0.68, 0.63])

for (a, b, lab) in [(2007.9, 2010.1, "Great Recession\nand aftermath"),
                    (2014.9, 2016.1, "Oil-price\ncollapse"),
                    (2019.6, 2020.4, "COVID-19")]:
    ax.axvspan(a, b, color="#f3f2ee", zorder=0)
    ax.text((a + b) / 2, 0.25, lab, ha="center", va="bottom", fontsize=8.3, color=INK2)

ax.plot(rate.index, rate["All counties"], color=INK, lw=1.0, ls=(0, (1, 1.5)), zorder=2)

for t in ["Nonspecialized", "Federal/state government", "Farming", "Mining", "Recreation", "Manufacturing"]:
    col, emph = STYLE[t]
    ax.plot(rate.index, rate[t], color=col, lw=2.2 if emph else 1.2, zorder=3 if emph else 2,
            solid_capstyle="round")

# peak markers that carry the story
def mark(t, yr, text, dx, dy, ha="left"):
    v = rate.loc[yr, t]
    ax.scatter([yr], [v], s=30, color=STYLE[t][0], zorder=5, edgecolor="white", lw=1)
    ax.annotate(text.format(v=v), xy=(yr, v), xytext=(yr + dx, v + dy), fontsize=8.8, color=INK,
                ha=ha, va="center", arrowprops=dict(arrowstyle="-", color=INK2, lw=0.6))

def mark2(t, yr, text, tx, ty, ha="left"):
    v = rate.loc[yr, t]
    ax.scatter([yr], [v], s=30, color=STYLE[t][0], zorder=5, edgecolor="white", lw=1)
    ax.annotate(text.format(v=v), xy=(yr, v), xytext=(tx, ty), fontsize=8.8, color=INK,
                ha=ha, va="center", arrowprops=dict(arrowstyle="-", color=INK2, lw=0.6, shrinkB=3))

mark2("Manufacturing", 2009, "Manufacturing: {v:.1f}% in 2009,\nhighest of any type that year", 2007.6, 11.6, ha="right")
mark2("Recreation", 2010, "Recreation: {v:.1f}% in 2010, and slowest\nto recover afterward", 2011.2, 11.6)
mark2("Mining", 2016, "Mining: the only type whose\nrate rose in 2016 ({v:.1f}%)", 2013.6, 2.3)
mark2("Recreation", 2020, "Recreation: {v:.1f}% in 2020,\n2.4x its 2019 rate", 2019.0, 10.4, ha="right")
mark2("Farming", 2020, "Farming: {v:.1f}%,\nsmallest jump", 2020.9, 2.3)

# legend to the right (ordered by story), with line swatches in each series' color
order = ["Manufacturing", "Recreation", "Mining", "Farming", "Nonspecialized",
         "Federal/state government", "All counties"]
ax.text(2024.0, 10.6, "County type (number of counties)", fontsize=9, color=INK, va="center",
        fontweight="bold")
for i, t in enumerate(order):
    y = 9.9 - i * 0.62
    if t in STYLE:
        col, emph = STYLE[t]
        ax.plot([2024.0, 2025.0], [y, y], color=col, lw=2.2 if emph else 1.2, clip_on=False)
        lab = f"{t} ({ncounty[t]:,})"
    else:
        emph = False
        ax.plot([2024.0, 2025.0], [y, y], color=INK, lw=1.0, ls=(0, (1, 1.5)), clip_on=False)
        lab = "All counties combined"
    ax.text(2025.3, y, lab, fontsize=9.2 if emph else 8.8, va="center", color=INK if emph else INK2)

ax.set_xlim(2000, 2023.2)
ax.set_ylim(0, 12.6)
ax.set_xticks(range(2000, 2024, 4))
ax.set_ylabel("Unemployment rate (% of civilian labor force)")
ax.yaxis.set_major_formatter(lambda v, p: f"{v:.0f}%")
ax.grid(axis="y")
ax.set_axisbelow(True)
ax.spines["left"].set_visible(False)
ax.tick_params(axis="y", length=0)

title_block(fig, "Each downturn hit a different kind of county economy",
            "Manufacturing counties spiked first in the Great Recession, mining counties suffered alone in the "
            "2016 oil bust, and recreation\ncounties were hit hardest by COVID-19. Farming counties had the "
            "smallest rise in both national downturns.")
caption(fig,
        "Lines show the unemployment rate for all U.S. counties of each USDA 2015 economic type, computed as "
        "total unemployed / total civilian labor force across the counties of that type (so large counties "
        "count more). The dotted black line is all counties combined. Economic type describes the county's "
        "dominant industry in 2010-12 and is held fixed for all years. Puerto Rico and the 20 counties with no "
        "2015 type (mostly Alaska and Connecticut, whose county units changed) are excluded. Shaded spans mark the downturns discussed.\n"
        "Data: USDA Economic Research Service county-level data sets, 2000-2023 (CS765 full_census_dataset.csv).",
        chars=165)
fig.savefig(FIG / "q2a_unemployment_lines.png")
print(rate.round(1).loc[[2007, 2009, 2010, 2014, 2016, 2019, 2020, 2023]])
