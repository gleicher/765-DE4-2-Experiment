"""Q2 alternate: county-level change in unemployment during three downturns, by economic type."""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from common import *

style()
c = load_census()
c = c[c["Economic typology 2015"].notna()].copy()
c["type"] = c["Economic typology 2015"].astype(int).map(ECON_TYPES)

ROWS = ["Manufacturing", "Recreation", "Mining", "Farming", "Nonspecialized", "Federal/state government"]
COLORS = {"Manufacturing": BLUE, "Recreation": ORANGE, "Mining": AQUA, "Farming": YELLOW,
          "Nonspecialized": GRAY, "Federal/state government": GRAY}
SHOCKS = [(2007, 2010, "Great Recession", "2007 to 2010"),
          (2014, 2016, "Oil-price collapse", "2014 to 2016"),
          (2019, 2020, "COVID-19", "2019 to 2020")]

rng = np.random.default_rng(765)
fig = plt.figure(figsize=(12, 7.0))
left, width, gap = 0.17, 0.255, 0.02
summary = []
for k, (a, b, name, span) in enumerate(SHOCKS):
    ax = fig.add_axes([left + k * (width + gap), 0.21, width, 0.57])
    d = c[f"Unemployment rate {b}"] - c[f"Unemployment rate {a}"]
    meds = {}
    for i, t in enumerate(ROWS):
        v = d[c["type"] == t].dropna().values
        y = i + rng.uniform(-0.28, 0.28, len(v))
        col = COLORS[t]
        ax.scatter(v, y, s=5, color=col, alpha=0.28 if col != GRAY else 0.22, edgecolor="none",
                   zorder=2, rasterized=True)
        q1, med, q3 = np.percentile(v, [25, 50, 75])
        meds[t] = med
        ax.plot([q1, q3], [i, i], color=INK, lw=2.2, zorder=3, solid_capstyle="butt")
        ax.plot([med, med], [i - 0.2, i + 0.2], color=INK, lw=2.2, zorder=4)
        summary.append(dict(shock=name, type=t, n=len(v), q1=q1, median=med, q3=q3))
    top = max(meds, key=meds.get)
    for i, t in enumerate(ROWS):
        bold = t == top
        ax.text(meds[t], i - 0.27, f"{meds[t]:+.1f}", ha="center", va="bottom", fontsize=8.8,
                color=INK if bold else INK2, fontweight="bold" if bold else "normal", zorder=6,
                bbox=dict(boxstyle="square,pad=0.08", fc="white", ec="none", alpha=0.85))
    ax.axvline(0, color=INK2, lw=0.8, zorder=1)
    ax.set_xlim(-6, 16)
    ax.set_ylim(len(ROWS) - 0.45, -0.75)
    ax.set_xticks([-5, 0, 5, 10, 15])
    ax.xaxis.set_major_formatter(lambda v, p: f"{v:+.0f}" if v else "0")
    ax.grid(axis="x")
    ax.set_axisbelow(True)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.set_yticks(range(len(ROWS)))
    if k == 0:
        ax.set_yticklabels(ROWS, fontsize=10)
        for lab, t in zip(ax.get_yticklabels(), ROWS):
            lab.set_color(INK if COLORS[t] != GRAY else INK2)
    else:
        ax.set_yticklabels([])
    ax.text(-6, -1.15, name, fontsize=11.5, fontweight="bold", color=INK, va="bottom")
    ax.text(-6, -0.82, f"change in unemployment rate, {span}", fontsize=8.8, color=INK2, va="bottom")
    if k == 1:
        ax.set_xlabel("Change in county unemployment rate (percentage points)")

pd.DataFrame(summary).to_csv(Path(__file__).parent / "out_fig2b_shock_summary.csv", index=False,
                             float_format="%.2f")

# small key for the box marks
kax = fig.add_axes([0.78, 0.04, 0.2, 0.09]); kax.axis("off")
kax.set_xlim(0, 10); kax.set_ylim(-1, 1)
xs = rng.normal(1.6, 0.6, 40)
kax.scatter(xs, rng.uniform(-0.35, 0.35, 40), s=5, color=GRAY, alpha=0.45, edgecolor="none")
kax.plot([1.2, 2.0], [0, 0], color=INK, lw=2.2); kax.plot([1.6, 1.6], [-0.3, 0.3], color=INK, lw=2.2)
kax.text(1.6, 0.42, "+2.0", ha="center", va="bottom", fontsize=8, color=INK2)
kax.text(3.6, 0, "dot = one county\nblack bar = middle 50% of counties\ntick and number = median",
         fontsize=8, color=INK2, va="center", ha="left")

title_block(fig, "Which counties' unemployment jumped most in each downturn?",
            "Recreation and manufacturing counties led the Great Recession, mining counties were the only ones "
            "hit by the 2016 oil bust, and recreation\ncounties led again in 2020. In both national downturns the typical "
            "farming county saw the smallest increase.")
caption(fig,
        "Each dot is one U.S. county, placed by how much its unemployment rate changed (percentage points) "
        "between the two years shown; dots are jittered vertically within each row. Rows are USDA 2015 "
        "county economic types; the bold median is the largest increase in that panel. Puerto Rico and counties "
        "with no 2015 type are excluded.\n"
        "Data: USDA Economic Research Service county-level data sets (CS765 full_census_dataset.csv).",
        chars=125)
fig.savefig(FIG / "q2b_unemployment_shocks.png")
print(pd.DataFrame(summary).round(1))
