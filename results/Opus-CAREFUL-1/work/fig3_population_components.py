"""Q3: components of population change (2021-2023) by 2023 Rural-Urban Continuum Code."""
import matplotlib.pyplot as plt
import matplotlib.transforms as mtrans
import numpy as np
import pandas as pd

from common import *

style()
c = load_census()
k = "Rural Urban Continuum Code 2023"
c = c[c[k].notna()].copy()
c[k] = c[k].astype(int)
YRS = [2021, 2022, 2023]

rows = []
for code, g in c.groupby(k):
    pop = sum(g[f"Population Estimate {y}"].sum() for y in YRS)  # person-years
    nat = sum(g[f"Natural Change {y}"].sum() for y in YRS)
    dom = sum(g[f"Domestic migration {y}"].sum() for y in YRS)
    intl = sum(g[f"International Migration {y}"].sum() for y in YRS)
    # share of counties where deaths outnumbered births over 2021-23
    nat_cty = sum(g[f"Natural Change {y}"] for y in YRS)
    rows.append(dict(code=code, n=len(g), pop23=g["Population Estimate 2023"].sum(),
                     natural=1000 * nat / pop, domestic=1000 * dom / pop,
                     international=1000 * intl / pop,
                     pct_more_deaths=100 * (nat_cty < 0).mean()))
d = pd.DataFrame(rows).set_index("code")
d["net"] = d[["natural", "domestic", "international"]].sum(axis=1)
d.to_csv(Path(__file__).parent / "out_fig3_components.csv", float_format="%.3f")
print(d.round(2))

COMP = [("natural", "Natural change (births minus deaths)", BLUE),
        ("international", "International migration", AQUA),
        ("domestic", "Domestic migration (moves within the U.S.)", ORANGE)]

fig = plt.figure(figsize=(12, 7.4))
ax = fig.add_axes([0.30, 0.2, 0.47, 0.58])
bt = mtrans.blended_transform_factory(ax.transAxes, ax.transData)
ypos = {code: i + (0.6 if code >= 4 else 0) for i, code in enumerate(d.index)}  # gap between metro/nonmetro
H = 0.62
for code, r in d.iterrows():
    y = ypos[code]
    pos, neg = 0.0, 0.0
    for key, lab, col in COMP:
        v = r[key]
        if v >= 0:
            ax.barh(y, v, left=pos, height=H, color=col, edgecolor="white", linewidth=1.2, zorder=2)
            pos += v
        else:
            ax.barh(y, v, left=neg, height=H, color=col, edgecolor="white", linewidth=1.2, zorder=2)
            neg += v
    ax.scatter([r["net"]], [y], s=46, color=INK, zorder=4, edgecolor="white", linewidth=1.2)
    ax.text(pos + 0.18, y, f"net {r['net']:+.1f}", ha="left", va="center", fontsize=8.6,
            color=INK, fontweight="bold", zorder=5)
    # left labels
    ax.text(-6.6, y, RUCC_LABELS[code], ha="right", va="center", fontsize=9.3, color=INK)
    # right-hand context columns
    ax.text(1.12, y, f"{r['pop23'] / 1e6:,.1f}M", ha="right", va="center", fontsize=9,
            color=INK2, transform=bt)
    ax.text(1.25, y, f"{int(r['n']):,}", ha="right", va="center", fontsize=9, color=INK2, transform=bt)
    ax.text(1.43, y, f"{r['pct_more_deaths']:.0f}%", ha="right", va="center", fontsize=9,
            color=INK, transform=bt)

top = -0.85
ax.text(1.12, top, "People\n(2023)", ha="right", va="bottom", fontsize=8.5, color=INK2, transform=bt)
ax.text(1.25, top, "Counties", ha="right", va="bottom", fontsize=8.5, color=INK2, transform=bt)
ax.text(1.43, top, "% of counties with\nmore deaths\nthan births", ha="right", va="bottom",
        fontsize=8.5, color=INK2, transform=bt)
ax.text(-6.6, ypos[1] - 0.75, "METRO COUNTIES", ha="right", va="bottom", fontsize=8.5,
        color=INK2, fontweight="bold")
ax.text(-6.6, ypos[4] - 0.75, "NONMETRO (RURAL) COUNTIES", ha="right", va="bottom", fontsize=8.5,
        color=INK2, fontweight="bold")

ax.axvline(0, color=INK2, lw=0.9, zorder=3)
ax.set_xlim(-6, 9.5)
ax.set_ylim(max(ypos.values()) + 0.6, -0.9)
ax.set_yticks([])
ax.set_xticks(range(-6, 10, 2))
ax.xaxis.set_major_formatter(lambda v, p: f"{v:+.0f}" if v else "0")
ax.set_xlabel("Average yearly population change per 1,000 residents, 2021-2023")
ax.grid(axis="x")
ax.set_axisbelow(True)
for sp in ["left"]:
    ax.spines[sp].set_visible(False)
ax.text(-0.15, max(ypos.values()) + 0.58, "< shrinking", ha="right", va="bottom", fontsize=8.3, color=INK2)
ax.text(0.15, max(ypos.values()) + 0.58, "growing >", ha="left", va="bottom", fontsize=8.3, color=INK2)

# annotation of the key contrast
ax.text(-5.9, (ypos[2] + ypos[3]) / 2 + 0.05,
        "Big metros lose residents to the\nrest of the U.S.; births and\nimmigrants make up for it",
        fontsize=8.8, color=INK, va="center", ha="left")
for code in (7, 9):
    ax.text(-6.5, ypos[code] + 0.36, "remote: shrinking", ha="right", va="center", fontsize=8,
            color=RED, style="italic")

# legend
lax = fig.add_axes([0.03, 0.85, 0.94, 0.035]); lax.axis("off")
x = 0.0
for key, lab, col in COMP:
    lax.add_patch(plt.Rectangle((x, 0.25), 0.018, 0.5, color=col, transform=lax.transAxes))
    lax.text(x + 0.025, 0.5, lab, transform=lax.transAxes, va="center", fontsize=9, color=INK)
    x += 0.025 + 0.0068 * len(lab) + 0.03
lax.scatter([x + 0.008], [0.5], s=46, color=INK, transform=lax.transAxes)
lax.text(x + 0.025, 0.5, "Net change (sum)", transform=lax.transAxes, va="center", fontsize=9, color=INK)

title_block(fig, "In small metros and rural America, deaths outnumber births: growth depends on movers",
            "Where population growth came from in 2021-2023. Rural counties next to a metro area gain movers from "
            "elsewhere in the U.S. and grow;\nremote rural counties (not next to a metro) attract few or none, and "
            "stall or shrink, even though their natural decrease is similar.")
caption(fig,
        "Bars stack the three components of population change for all counties in each USDA 2023 "
        "Rural-Urban Continuum category, as a yearly rate per 1,000 residents (components summed over July "
        "2020-June 2023, divided by summed population estimates). Positive parts stack right of zero, negative "
        "parts left; the black dot is their sum. The Census Bureau's small \"residual\" term is omitted. "
        "Rightmost column: share of counties in the category whose 2021-23 deaths exceeded births. "
        "Puerto Rico excluded.\n"
        "Data: USDA Economic Research Service county-level population estimates (CS765 full_census_dataset.csv).",
        chars=170)
fig.savefig(FIG / "q3_population_components.png")
