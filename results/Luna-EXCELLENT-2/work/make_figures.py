#!/opt/anaconda3/envs/p314/bin/python
"""Regenerate the six static figures for the instructor's DE 4-2 exemplar."""
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / "work" / "mplconfig"))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import MultipleLocator, FuncFormatter

OUT = ROOT / "answers" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

# A restrained, colorblind-friendly palette used consistently throughout.
INK = "#172B3A"
MUTED = "#536575"
GRID = "#DCE3E8"
TEAL = "#187F78"
BLUE = "#3E6F91"
RUST = "#C45A45"
GOLD = "#D59C37"
PURPLE = "#8B6F9E"
PALE = "#F4F7F8"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.titleweight": "bold",
    "axes.labelsize": 10,
    "axes.labelcolor": MUTED,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "text.color": INK,
    "axes.edgecolor": GRID,
    "axes.linewidth": 0.8,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white",
})


def polish(ax, grid="y"):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(GRID)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(length=0, pad=5)
    ax.grid(axis=grid, color=GRID, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)


def heading(fig, title, subtitle, footer, top=0.88):
    fig.text(0.075, 0.965, title, fontsize=19, fontweight="bold", color=INK,
             ha="left", va="top")
    fig.text(0.075, 0.918, subtitle, fontsize=10.5, color=MUTED,
             ha="left", va="top")
    fig.text(0.075, 0.025, footer, fontsize=8.2, color=MUTED,
             ha="left", va="bottom", wrap=True)


def save(fig, filename):
    fig.savefig(OUT / filename, dpi=190, bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Load and prepare the two course-provided data files.
life = pd.read_csv(ROOT / "data" / "lifespan_dataset_1960.csv")
life["Life Expectancy (years)"] = pd.to_numeric(
    life["Life Expectancy (years)"], errors="coerce")
life["Year"] = pd.to_numeric(life["Year"], errors="coerce")

both = (life[(life["Sex"] == "Both") & life["Year"].isin([2019, 2020, 2021, 2022, 2023])]
        .pivot_table(index=["Country Name", "Country Code"],
                     columns="Year", values="Life Expectancy (years)", aggfunc="first")
        .dropna(subset=[2019, 2020, 2021, 2022, 2023]).copy())
both["change_21"] = both[2021] - both[2019]
both["change_23"] = both[2023] - both[2019]
both["rebound_23"] = both[2023] - both[2021]
top_shocks = both.nsmallest(6, "change_21")

# Figure 1: endpoint-aligned small multiples make the selected trajectories legible.
fig, axes = plt.subplots(2, 3, figsize=(12.4, 7.8), sharex=True, sharey=True)
heading(
    fig,
    "Five of the six deepest 2019–21 falls were above baseline by 2023",
    "Each line is indexed to its own 2019 life expectancy; the 2021 trough is the deepest among these six series.",
    "World Bank life expectancy, both-sex series in the course file. Selected six reporting entities with the largest 2019–21 declines; values are changes from 2019 in years. Series may include country aggregates. Recovery here describes the observed trajectory, not a causal attribution.",
)
for ax, ((name, code), row) in zip(axes.flat, top_shocks.iterrows()):
    years = np.array([2019, 2020, 2021, 2022, 2023], dtype=int)
    vals = row[years].to_numpy(dtype=float) - row[2019]
    ax.axhline(0, color=MUTED, linewidth=1, linestyle=(0, (3, 3)), zorder=1)
    ax.plot(years, vals, color=BLUE, linewidth=2.2, marker="o", markersize=5.7, zorder=3)
    ax.scatter([2021], [row[2021] - row[2019]], color=RUST, s=48, zorder=4,
               edgecolor="white", linewidth=0.8)
    ax.scatter([2023], [row[2023] - row[2019]], color=TEAL, s=48, zorder=4,
               edgecolor="white", linewidth=0.8)
    ax.set_title(name, loc="left", fontsize=11, pad=8)
    ax.text(0.99, 0.94,
            f"2021 {row['change_21']:+.1f}  ·  2023 {row['change_23']:+.1f} y",
            transform=ax.transAxes, ha="right", va="top", fontsize=8.5, color=MUTED)
    ax.set_xticks(years)
    ax.set_ylim(-7.4, 2.3)
    ax.set_xlim(2018.7, 2023.3)
    polish(ax, "y")
fig.supxlabel("Year", x=0.51, y=0.073, fontsize=10, color=MUTED)
fig.supylabel("Change from 2019 (years)", x=0.025, y=0.49, fontsize=10, color=MUTED)
fig.subplots_adjust(left=0.09, right=0.985, bottom=0.13, top=0.84, wspace=0.19, hspace=0.37)
save(fig, "01_life_expectancy_recovery_small_multiples.png")

# Figure 2: all available entities provide the context missing from the selected six.
fig, ax = plt.subplots(figsize=(11.8, 7.5))
restored = both["change_23"] >= 0
ax.axhspan(0, 4.2, color=TEAL, alpha=0.055, zorder=0)
ax.axhline(0, color=INK, linewidth=1.0, zorder=1)
ax.axvline(0, color=GRID, linewidth=1.0, zorder=1)
ax.scatter(both.loc[restored, "change_21"], both.loc[restored, "change_23"],
           s=27, color=TEAL, alpha=0.54, linewidth=0, zorder=2,
           label="2023 at/above 2019")
ax.scatter(both.loc[~restored, "change_21"], both.loc[~restored, "change_23"],
           s=31, color=RUST, alpha=0.76, linewidth=0, zorder=3,
           label="2023 below 2019")
# Ring the six deepest 2021 declines, linking this chart to the first design.
ax.scatter(top_shocks["change_21"], top_shocks["change_23"], s=85,
           facecolors="none", edgecolors=GOLD, linewidths=1.5, zorder=4,
           label="Six deepest 2019–21 declines")
labels = {
    "Bolivia": (-7, 9),
    "Lebanon": (8, -20),
    "United States": (-20, -17),
    "West Bank and Gaza": (8, -4),
    "Libya": (8, -5),
}
for name, offset in labels.items():
    matches = both[both.index.get_level_values("Country Name") == name]
    if not matches.empty:
        r = matches.iloc[0]
        ax.annotate(name, (r["change_21"], r["change_23"]), xytext=offset,
                    textcoords="offset points", fontsize=8.5, color=INK,
                    arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7),
                    bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none", alpha=0.82),
                    zorder=5)
ax.text(0.985, 0.965,
        f"{int(restored.sum())} of {len(both)} series ({restored.mean():.0%})\nended 2023 at/above 2019",
        transform=ax.transAxes, ha="right", va="top", fontsize=10, color=INK,
        bbox=dict(boxstyle="round,pad=0.5", fc="white", ec=GRID, lw=0.8))
ax.set_xlim(-7.25, 3.6)
ax.set_ylim(-11.8, 4.1)
ax.set_xlabel("2019 → 2021 change (years; left = larger decline)", labelpad=9)
ax.set_ylabel("2019 → 2023 change (years)", labelpad=9)
ax.legend(frameon=False, loc="lower right", bbox_to_anchor=(1, 0.02), fontsize=8.5)
polish(ax, "both")
heading(
    fig,
    "Most reporting series had regained their 2019 level by 2023",
    "The deepest 2021 losses generally rebounded; a few later declines dominate the exceptions.",
    "World Bank life expectancy, both-sex series in the course file; 265 entries with all five years present, including country and regional aggregates. A point above zero in the vertical dimension ended 2023 at/above its 2019 level. West Bank and Gaza and Libya are labeled as 2023 exceptions; the chart does not attribute their later movement to the pandemic.",
)
fig.subplots_adjust(left=0.12, right=0.965, top=0.84, bottom=0.14)
save(fig, "02_life_expectancy_recovery_overview.png")

# Figure 3: compare lifespan gains and change in the sex gap.
sex = (life[life["Year"].isin([1960, 2023])]
       .pivot_table(index=["Country Name", "Country Code"], columns=["Sex", "Year"],
                    values="Life Expectancy (years)", aggfunc="first")
       .dropna(subset=[("Both", 1960), ("Both", 2023), ("Male", 1960), ("Male", 2023),
                       ("Female", 1960), ("Female", 2023)]).copy())
sex["gain_both"] = sex[("Both", 2023)] - sex[("Both", 1960)]
sex["gap_1960"] = sex[("Female", 1960)] - sex[("Male", 1960)]
sex["gap_2023"] = sex[("Female", 2023)] - sex[("Male", 2023)]
sex["gap_change"] = sex["gap_2023"] - sex["gap_1960"]

fig, ax = plt.subplots(figsize=(11.8, 7.5))
wide = sex["gap_change"] > 0
ax.axhspan(-9, 0, color=BLUE, alpha=0.045, zorder=0)
ax.axhspan(0, 10, color=RUST, alpha=0.045, zorder=0)
ax.axhline(0, color=INK, linewidth=1.0, zorder=1)
ax.scatter(sex.loc[~wide, "gain_both"], sex.loc[~wide, "gap_change"], s=31,
           color=BLUE, alpha=0.55, linewidth=0, zorder=2, label="Female advantage narrowed")
ax.scatter(sex.loc[wide, "gain_both"], sex.loc[wide, "gap_change"], s=31,
           color=RUST, alpha=0.60, linewidth=0, zorder=2, label="Female advantage widened")
ann = {
    "Pakistan": (-4, 10),
    "Ukraine": (8, 7),
    "Thailand": (8, -4),
    "Cameroon": (8, -16),
    "Isle of Man": (8, -2),
}
for name, offset in ann.items():
    matches = sex[sex.index.get_level_values("Country Name") == name]
    if not matches.empty:
        r = matches.iloc[0]
        ax.annotate(name, (float(r[("gain_both", "")]), float(r[("gap_change", "")])), xytext=offset,
                    textcoords="offset points", fontsize=8.5, color=INK,
                    arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7),
                    bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none", alpha=0.84),
                    zorder=4)
ax.text(0.985, 0.965,
        f"{int(wide.sum())}/{len(sex)} series ({wide.mean():.0%}) widened\nmedian gap shift {sex.gap_change.median():+.1f} years · r = {sex[['gain_both', 'gap_change']].corr().iloc[0, 1]:.2f}",
        transform=ax.transAxes, ha="right", va="top", fontsize=9.5,
        bbox=dict(boxstyle="round,pad=0.5", fc="white", ec=GRID, lw=0.8))
ax.set_xlim(0, 47)
ax.set_ylim(-9, 10)
ax.xaxis.set_major_locator(MultipleLocator(5))
ax.yaxis.set_major_locator(MultipleLocator(2))
ax.set_xlabel("Change in both-sex life expectancy, 1960 → 2023 (years)", labelpad=9)
ax.set_ylabel("Change in female − male gap, 1960 → 2023 (years)", labelpad=9)
ax.legend(frameon=False, loc="lower right", fontsize=8.5)
polish(ax, "both")
heading(
    fig,
    "Longevity rose almost everywhere; the sex gap usually widened",
    "Across 263 reporting series, 69% had a wider female-minus-male advantage in 2023 than in 1960.",
    "World Bank life expectancy by sex in the course file; 263 entries with complete values in 1960 and 2023, including country and regional aggregates. The horizontal axis is the both-sex gain; the vertical axis is the change in female minus male life expectancy. Pearson r = 0.11: the size of the longevity gain is only weakly associated with gap change. Descriptive comparison, not a causal explanation.",
)
fig.subplots_adjust(left=0.12, right=0.965, top=0.84, bottom=0.14)
save(fig, "05_visualization3_life_sex_gap.png")

# Load full county data; it contains some Windows-1252 punctuation.
census = pd.read_csv(ROOT / "data" / "full_census_dataset.csv",
                     dtype={"FIPS Code": str}, encoding="cp1252")
county = census[census["FIPS Code"].str.fullmatch(r"\d{5}", na=False)].copy()
for col in ["Rural Urban Continuum Code 2023", "Natural Change Rate 2023",
            "Net Migration Rate 2023",
            "Percent of adults with a bachelor's degree or higher, 1990",
            "Percent of adults with a bachelor's degree or higher, 2019-23"]:
    county[col] = pd.to_numeric(county[col], errors="coerce")
county = county[county["Rural Urban Continuum Code 2023"].between(1, 9)].copy()

rates = county.dropna(subset=["Natural Change Rate 2023", "Net Migration Rate 2023"]).copy()
rates["natural"] = rates["Natural Change Rate 2023"]
rates["migration"] = rates["Net Migration Rate 2023"]
rates["total"] = rates["natural"] + rates["migration"]
rates["rucc"] = rates["Rural Urban Continuum Code 2023"].astype(int)
rates["Place type"] = np.select(
    [rates["rucc"].between(1, 3), rates["rucc"].between(4, 7)],
    ["Metro (RUCC 1–3)", "Nonmetro towns (4–7)"], default="Rural (8–9)")

# Figure 4: population accounting components and the total-growth boundary.
fig, ax = plt.subplots(figsize=(11.8, 7.5))
xlo, xhi = -17, 16
ylo, yhi = -32, 48
xx = np.linspace(xlo, xhi, 300)
threshold = -xx
ax.fill_between(xx, threshold, yhi, color=TEAL, alpha=0.055, zorder=0,
                where=threshold < yhi)
ax.fill_between(xx, ylo, threshold, color=RUST, alpha=0.035, zorder=0,
                where=threshold > ylo)
ax.axhline(0, color=GRID, lw=1, zorder=1)
ax.axvline(0, color=GRID, lw=1, zorder=1)
colors = {"Metro (RUCC 1–3)": BLUE, "Nonmetro towns (4–7)": GOLD, "Rural (8–9)": TEAL}
markers = {"Metro (RUCC 1–3)": "o", "Nonmetro towns (4–7)": "s", "Rural (8–9)": "^"}
for label in ["Metro (RUCC 1–3)", "Nonmetro towns (4–7)", "Rural (8–9)"]:
    sub = rates[rates["Place type"] == label]
    xin = sub["natural"].clip(xlo, xhi)
    yin = sub["migration"].clip(ylo, yhi)
    inside = sub["natural"].between(xlo, xhi) & sub["migration"].between(ylo, yhi)
    ax.scatter(xin[inside], yin[inside], s=16, marker=markers[label],
               color=colors[label], alpha=0.31, linewidth=0, zorder=2, label=label)
    outside = ~inside
    # Boundary markers keep extreme rates visible without letting one county flatten the field.
    if outside.any():
        for _, r in sub.loc[outside].iterrows():
            x, y = r["natural"], r["migration"]
            if x < xlo:
                marker = "<"
            elif x > xhi:
                marker = ">"
            elif y < ylo:
                marker = "v"
            else:
                marker = "^"
            ax.scatter([np.clip(x, xlo, xhi)], [np.clip(y, ylo, yhi)], marker=marker,
                       s=39, color=colors[label], edgecolor="white", linewidth=0.45,
                       zorder=3)
# Total natural + net-migration rate = zero is the population-growth boundary.
ax.plot(xx, -xx, color=INK, linestyle=(0, (5, 3)), lw=1.35, zorder=3)
ax.text(7.7, 31.5, "Net population gain", color=TEAL, fontsize=8.5,
        rotation=-22, ha="center", va="center")
ax.text(-10.5, -25.8, "Net population loss", color=RUST, fontsize=8.5,
        rotation=-22, ha="center", va="center")
ax.text(-15.9, 44.2, "Migration offsets a natural decrease\nabove the dashed boundary",
        color=MUTED, fontsize=8.1, ha="left", va="top")
ax.set_xlim(xlo, xhi)
ax.set_ylim(ylo, yhi)
ax.xaxis.set_major_locator(MultipleLocator(5))
ax.yaxis.set_major_locator(MultipleLocator(10))
ax.set_xlabel("Natural change rate, 2023 (per 1,000 residents)", labelpad=9)
ax.set_ylabel("Net migration rate, 2023 (per 1,000 residents)", labelpad=9)
ax.legend(frameon=True, ncol=1, loc="upper right", fontsize=8.2,
          framealpha=0.92, facecolor="white", edgecolor=GRID)
polish(ax, "both")
heading(
    fig,
    "Migration offsets natural decrease less often in the most rural counties",
    "Each county is one point; the dashed line marks where the two rates sum to zero population change.",
    f"USDA county data in the course file; {len(rates):,} counties with both 2023 rates and a 2023 Rural–Urban Continuum Code. Rates use per-1,000 units. Edge triangles denote values outside the plotted ranges (natural: −17 to 16; migration: −32 to 48). Points are county-weighted, not population-weighted; rates are descriptive accounting components, not causal effects.",
)
fig.subplots_adjust(left=0.12, right=0.965, top=0.84, bottom=0.14)
save(fig, "03_q2_migration_natural_change.png")

# Figure 5: the same county accounting, recast as outcome shares by RUCC.
rates["status"] = np.select(
    [
        (rates["natural"] < 0) & (rates["total"] < 0),
        (rates["natural"] >= 0) & (rates["total"] < 0),
        (rates["natural"] < 0) & (rates["total"] >= 0),
    ],
    ["Decline: natural loss not offset", "Decline: migration erases natural gain",
     "Growth: migration offsets natural loss"],
    default="Growth: natural gain retained")
status_order = [
    "Decline: natural loss not offset",
    "Decline: migration erases natural gain",
    "Growth: migration offsets natural loss",
    "Growth: natural gain retained",
]
status_colors = ["#B65043", "#D98D77", "#66A99B", "#247566"]
summary = (rates.groupby(["rucc", "status"]).size().unstack(fill_value=0)
           .reindex(columns=status_order, fill_value=0))
summary = summary.div(summary.sum(axis=1), axis=0) * 100
ns = rates.groupby("rucc").size()

fig, ax = plt.subplots(figsize=(12, 7.6))
left = np.zeros(len(summary), dtype=float)
for status, color in zip(status_order, status_colors):
    vals = summary[status].to_numpy()
    ax.barh(np.arange(len(summary)), vals, left=left, height=0.66, color=color,
            edgecolor="white", linewidth=0.9, label=status, zorder=3)
    for y, start, value in zip(np.arange(len(summary)), left, vals):
        if value >= 9:
            text_color = "white" if color in ["#B65043", "#247566"] else INK
            ax.text(start + value / 2, y, f"{value:.0f}%", ha="center", va="center",
                    fontsize=8.1, fontweight="bold", color=text_color, zorder=4)
    left += vals
ax.set_yticks(np.arange(len(summary)))
ax.set_yticklabels([f"RUCC {c}" for c in summary.index])
ax.invert_yaxis()
ax.set_xlim(0, 111)
ax.set_xticks([0, 20, 40, 60, 80, 100])
ax.set_xlabel("Share of counties in each RUCC category", labelpad=9)
ax.set_ylabel("2023 Rural–Urban Continuum Code (1 = metro; 9 = most rural)", labelpad=9)
ax.grid(axis="x", color=GRID, linewidth=0.8, zorder=0)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.spines["bottom"].set_color(GRID)
ax.tick_params(length=0, pad=5)
for y, n in enumerate(ns.reindex(summary.index)):
    ax.text(103.2, y, f"n={n}", ha="left", va="center", fontsize=8.2, color=MUTED)
ax.legend(frameon=False, ncol=2, loc="upper center", bbox_to_anchor=(0.51, -0.13),
          fontsize=8.4, columnspacing=1.4, handlelength=1.6)
# Conditional migration-offset percentages among counties with natural decrease.
def offset_share(code):
    group = rates[rates["rucc"] == code]
    natural_decrease = group[group["natural"] < 0]
    return (natural_decrease["total"] >= 0).mean()
ax.text(0.985, 1.075,
        f"Among naturally declining counties, migration restored growth in\n"
        f"{offset_share(1):.0%} of RUCC 1 vs {offset_share(9):.0%} of RUCC 9",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=9.1,
        bbox=dict(boxstyle="round,pad=0.45", fc="white", ec=GRID, lw=0.8))
heading(
    fig,
    "A growing county can still depend on migration to replace natural decrease",
    "The mix shifts from metro growth toward sustained decline at the rural end of the continuum.",
    "USDA county data in the course file; county shares use both 2023 rates and valid RUCC codes (same complete-case set as the scatterplot). The four categories classify the signs of natural change and total rate (natural + net migration). Every county counts equally; n at right is the number of counties in the code. RUCC is a current classification applied to 2023 rates.",
)
fig.subplots_adjust(left=0.16, right=0.92, top=0.78, bottom=0.23)
save(fig, "04_q2_population_change_by_rucc.png")

# Figure 6: county medians and IQRs at two education endpoints, stratified by current RUCC.
base_col = "Percent of adults with a bachelor's degree or higher, 1990"
end_col = "Percent of adults with a bachelor's degree or higher, 2019-23"
edu = county.dropna(subset=[base_col, end_col]).copy()
edu["rucc"] = edu["Rural Urban Continuum Code 2023"].astype(int)

def med_q(s, q):
    return s.quantile(q)
agg = edu.groupby("rucc").agg(
    n=(base_col, "size"),
    med90=(base_col, "median"), q25_90=(base_col, lambda s: med_q(s, .25)), q75_90=(base_col, lambda s: med_q(s, .75)),
    medend=(end_col, "median"), q25_end=(end_col, lambda s: med_q(s, .25)), q75_end=(end_col, lambda s: med_q(s, .75)),
)

fig, ax = plt.subplots(figsize=(11.8, 7.5))
x = np.arange(1, 10)
# IQRs are deliberately thinner/lighter than the connected median summaries.
for i, r in agg.iterrows():
    ax.vlines(i - 0.065, r.q25_90, r.q75_90, color=BLUE, alpha=0.28, lw=5, zorder=2)
    ax.vlines(i + 0.065, r.q25_end, r.q75_end, color=RUST, alpha=0.25, lw=5, zorder=2)
ax.plot(x - .065, agg["med90"], color=BLUE, marker="o", markersize=5.5,
        linewidth=2, zorder=4, label="1990 county median")
ax.plot(x + .065, agg["medend"], color=RUST, marker="o", markersize=5.5,
        linewidth=2.2, zorder=4, label="2019–23 county median")
ax.set_xticks(x)
ax.set_xticklabels([str(i) for i in x])
ax.set_xlim(.55, 9.55)
ax.set_ylim(0, 71)
ax.yaxis.set_major_locator(MultipleLocator(10))
ax.set_xlabel("2023 Rural–Urban Continuum Code (1 = metro; 9 = most rural)", labelpad=9)
ax.set_ylabel("Adults with a bachelor's degree or higher (%)", labelpad=9)
ax.legend(frameon=False, loc="upper right", fontsize=8.8)
ax.text(0.02, 0.965, "Thick vertical marks = county 25th–75th percentile range",
        transform=ax.transAxes, ha="left", va="top", fontsize=8.5, color=MUTED)
polish(ax, "y")
heading(
    fig,
    "College attainment rose at every RUCC level, while the metro–rural gap widened",
    f"Gap between RUCC 1 and RUCC 9 county medians: {agg.loc[1, 'med90'] - agg.loc[9, 'med90']:.1f} pp in 1990 → {agg.loc[1, 'medend'] - agg.loc[9, 'medend']:.1f} pp in 2019–23.",
    "USDA county data in the course file. Each point is the unweighted county median and each vertical range is the county interquartile range. 1990 and 2019–23 degree shares are compared within the 2023 RUCC groups; this does not reconstruct historical rural/urban classifications. Latest endpoint is a 2019–23 estimate, not a single-year 2023 count.",
)
fig.subplots_adjust(left=0.12, right=0.965, top=0.84, bottom=0.14)
save(fig, "06_visualization4_census_bachelors_attainment.png")

print(f"Wrote 6 figures to {OUT}")
print(f"Q1 all-series: {len(both)}; at/above 2019 by 2023: {(both['change_23'] >= 0).sum()} ({(both['change_23'] >= 0).mean():.1%})")
print(f"Q3 complete sex series: {len(sex)}; gap widened: {(sex['gap_change'] > 0).sum()} ({(sex['gap_change'] > 0).mean():.1%}); correlation r={sex[['gain_both','gap_change']].corr().iloc[0,1]:.3f}")
print(f"Q2 county rates: {len(rates)}; RUCC 1 offset among nat decrease: {offset_share(1):.1%}; RUCC 9: {offset_share(9):.1%}")
print(f"Q4 county endpoints: {len(edu)}; RUCC1 median gap {(agg.loc[1,'medend']-agg.loc[9,'medend']):.1f} pp vs {(agg.loc[1,'med90']-agg.loc[9,'med90']):.1f} pp")
