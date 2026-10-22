"""Generate the six static figures for Design Exercise 4-2."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import MultipleLocator


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "answers" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

NAVY = "#20354A"
INK = "#273746"
MUTED = "#657786"
GRID = "#DCE3E8"
PAPER = "#FCFBF8"
TEAL = "#188C83"
CORAL = "#D96D4F"
BLUE = "#547AA5"
GOLD = "#D6A23E"
PALE_TEAL = "#DDEFEA"
PALE_CORAL = "#F6E5DE"
GRAY = "#9AA8B2"

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "axes.labelcolor": INK,
        "text.color": INK,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "axes.edgecolor": GRID,
        "figure.facecolor": PAPER,
        "axes.facecolor": PAPER,
        "savefig.facecolor": PAPER,
    }
)


def frame(fig, title, subtitle, caption, source):
    fig.text(0.085, 0.94, title, fontsize=22, weight="bold", color=NAVY, va="top")
    fig.text(0.085, 0.895, subtitle, fontsize=11.5, color=MUTED, va="top")
    fig.text(0.085, 0.11, caption, fontsize=9.5, color=INK, va="top", wrap=True)
    fig.text(0.085, 0.018, source, fontsize=8.5, color=MUTED, va="bottom")


def polish_ax(ax, xgrid=True, ygrid=True):
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color(GRID)
    ax.tick_params(length=0, pad=7)
    if xgrid:
        ax.grid(axis="x", color=GRID, linewidth=0.8, alpha=0.75)
    if ygrid:
        ax.grid(axis="y", color=GRID, linewidth=0.8, alpha=0.75)
    ax.set_axisbelow(True)


def save(fig, name):
    fig.savefig(OUT / name, dpi=220, bbox_inches="tight")
    plt.close(fig)


def load_life():
    df = pd.read_csv(ROOT / "data" / "lifespan_dataset_1960.csv")
    return df.drop(columns=["Unnamed: 0"], errors="ignore")


def load_census():
    # The supplied full file uses commas and contains a few Windows-1252 name bytes.
    df = pd.read_csv(
        ROOT / "data" / "full_census_dataset.csv",
        dtype={"FIPS Code": str},
        encoding="cp1252",
        low_memory=False,
    )
    # The full file is county/county-equivalent level; Puerto Rico has no matching
    # 2023 migration-rate series in this file, so use the 50 states and DC.
    return df.loc[df["State"].ne("PR")].copy()


def fig1_life_deltas(life):
    data = life.loc[life["Sex"].eq("Both")].pivot(
        index=["Country Name", "Country Code"],
        columns="Year",
        values="Life Expectancy (years)",
    )
    candidates = [
        "Bolivia",
        "Paraguay",
        "Mexico",
        "Guyana",
        "Peru",
        "Lebanon",
        "Ecuador",
        "Cuba",
        "Colombia",
        "South Africa",
        "Oman",
        "Armenia",
        "Bulgaria",
        "Botswana",
        "Guatemala",
    ]
    data = data.loc[data.index.get_level_values("Country Name").isin(candidates)].copy()
    data["2021 change"] = data[2021] - data[2019]
    data["2023 change"] = data[2023] - data[2019]
    data = data.sort_values("2021 change")
    full = life.loc[life["Sex"].eq("Both")].pivot(
        index="Country Name", columns="Year", values="Life Expectancy (years)"
    )
    top_names = full.dropna(subset=[2019, 2021]).assign(
        drop=lambda x: x[2019] - x[2021]
    )["drop"].nlargest(15).index
    data = data.loc[data.index.get_level_values("Country Name").isin(top_names)]
    data = data.sort_values("2021 change")
    n_recovered = int((data["2023 change"] >= 0).sum())

    fig, ax = plt.subplots(figsize=(12.5, 8.2))
    fig.subplots_adjust(left=0.26, right=0.95, top=0.83, bottom=0.25)
    frame(
        fig,
        "Most of the largest 2021 setbacks had reversed by 2023",
        "Life expectancy at birth relative to each country’s 2019 level",
        f"Each row is one of the 15 countries with the largest 2019–21 declines. "
        f"By 2023, {n_recovered} of 15 had reached or passed their 2019 level; "
        "Lebanon remained below it. Changes are descriptive and do not identify causes.",
        "Source: World Bank life-expectancy series, course-provided file (1960–2023); both sexes.",
    )
    y = np.arange(len(data))
    x21 = data["2021 change"].to_numpy()
    x23 = data["2023 change"].to_numpy()
    for i, (a, b) in enumerate(zip(x21, x23)):
        ax.plot([a, b], [i, i], color="#B9C3C9", lw=2, zorder=1)
    ax.scatter(x21, y, s=55, color=CORAL, zorder=3, label="2021 vs 2019")
    ax.scatter(x23, y, s=65, color=TEAL, edgecolor=PAPER, linewidth=0.8, zorder=4, label="2023 vs 2019")
    ax.axvline(0, color=NAVY, linewidth=1.3, zorder=2)
    ax.set_yticks(y, data.index.get_level_values("Country Name"))
    ax.set_xlabel("Difference from 2019 life expectancy (years)")
    ax.set_xlim(-7.3, 2.6)
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.set_ylim(-0.8, len(data) - 0.2)
    ax.invert_yaxis()
    polish_ax(ax, xgrid=True, ygrid=False)
    ax.legend(
        loc="lower right",
        frameon=False,
        ncol=2,
        bbox_to_anchor=(1, 1.015),
        fontsize=9.5,
    )
    ax.text(
        0.02,
        0.02,
        "2019 baseline",
        transform=ax.get_xaxis_transform(),
        color=NAVY,
        fontsize=9,
        ha="left",
        va="bottom",
    )
    save(fig, "01_life_expectancy_recovery_deltas.png")
    return data


def fig2_recovery_scatter(life, selected):
    full = life.loc[life["Sex"].eq("Both")].pivot(
        index="Country Name", columns="Year", values="Life Expectancy (years)"
    )
    d = full.loc[selected.index.get_level_values("Country Name")].copy()
    d["decline"] = d[2019] - d[2021]
    d["recovered_pct"] = (d[2023] - d[2021]) / d["decline"] * 100
    d = d.sort_values("decline")

    fig, ax = plt.subplots(figsize=(12, 8))
    fig.subplots_adjust(left=0.11, right=0.96, top=0.82, bottom=0.25)
    frame(
        fig,
        "The size of the setback did not determine the rebound",
        "Among the 15 largest 2019–21 declines, recovery varied from incomplete to well beyond the loss",
        "The horizontal axis measures the 2019–21 decline; the vertical axis is the share of that loss "
        "regained by 2023. The 100% line marks return to the 2019 level. These ratios compare only "
        "the selected countries and should not be read as causal effects.",
        "Source: World Bank life-expectancy series, course-provided file (1960–2023); both sexes.",
    )
    ax.axhspan(100, 170, color=PALE_TEAL, alpha=0.55, zorder=0)
    ax.axhspan(60, 100, color=PALE_CORAL, alpha=0.35, zorder=0)
    ax.axhline(100, color=NAVY, linewidth=1.4, linestyle=(0, (4, 3)), zorder=1)
    recovered = d["recovered_pct"] >= 100
    ax.scatter(
        d.loc[recovered, "decline"],
        d.loc[recovered, "recovered_pct"],
        color=TEAL,
        s=76,
        edgecolor=PAPER,
        linewidth=0.9,
        zorder=3,
        label="At or above 2019 level by 2023",
    )
    ax.scatter(
        d.loc[~recovered, "decline"],
        d.loc[~recovered, "recovered_pct"],
        color=CORAL,
        s=76,
        edgecolor=PAPER,
        linewidth=0.9,
        zorder=3,
        label="Still below 2019 level in 2023",
    )
    annotations = {
        "Bolivia": (8, 11),
        "Lebanon": (8, -19),
        "Botswana": (8, 7),
        "Paraguay": (-55, 12),
        "South Africa": (-74, -20),
    }
    for name, offset in annotations.items():
        if name in d.index:
            ax.annotate(
                name,
                (d.loc[name, "decline"], d.loc[name, "recovered_pct"]),
                xytext=offset,
                textcoords="offset points",
                fontsize=9,
                color=INK,
                arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.8),
            )
    ax.text(7.05, 103, "2019 level regained", color=NAVY, fontsize=9, ha="right", va="bottom")
    ax.set_xlim(3.4, 6.9)
    ax.set_ylim(60, 170)
    ax.set_xlabel("Life-expectancy decline, 2019–21 (years)")
    ax.set_ylabel("2021–23 rebound as a share of the 2019–21 loss")
    ax.set_yticks([60, 80, 100, 120, 140, 160], [f"{x}%" for x in [60, 80, 100, 120, 140, 160]])
    polish_ax(ax, xgrid=True, ygrid=True)
    ax.legend(frameon=False, loc="upper left", fontsize=9)
    save(fig, "02_life_expectancy_recovery_scatter.png")


def fig3_education_transition(census):
    old = "Percent of adults with a bachelor's degree or higher, 1990"
    new = "Percent of adults with a bachelor's degree or higher, 2019-23"
    rucc = "2023 Rural-urban Continuum Code"
    d = census.dropna(subset=[old, new, rucc]).copy()
    d["setting"] = np.where(d[rucc] <= 3, "Metro (RUCC 1–3)", "Nonmetro (RUCC 4–9)")

    fig, ax = plt.subplots(figsize=(10, 10.5))
    fig.subplots_adjust(left=0.12, right=0.88, top=0.82, bottom=0.25)
    frame(
        fig,
        "Bachelor’s attainment rose in nearly every county, but the gap persisted",
        "County-level share of adults with a bachelor’s degree or higher, 1990 and 2019–23",
        f"Each dot is one county or county equivalent ({len(d):,} observations, unweighted). "
        "Points above the diagonal gained attainment; the metro and nonmetro medians show that "
        "the typical metro county remained higher at both endpoints. County medians are not population-weighted.",
        "Source: USDA county-level data, merged course file; 1990 Census and 2019–23 ACS measures.",
    )
    ax.scatter(
        d.loc[d.setting.eq("Nonmetro"), old],
        d.loc[d.setting.eq("Nonmetro"), new],
        s=17,
        alpha=0.33,
        color=GOLD,
        linewidth=0,
        label="Nonmetro (RUCC 4–9)",
        rasterized=True,
        zorder=2,
    )
    ax.scatter(
        d.loc[d.setting.eq("Metro (RUCC 1–3)"), old],
        d.loc[d.setting.eq("Metro (RUCC 1–3)"), new],
        s=17,
        alpha=0.34,
        color=BLUE,
        linewidth=0,
        label="Metro (RUCC 1–3)",
        rasterized=True,
        zorder=2,
    )
    ax.plot([0, 65], [0, 65], color=MUTED, lw=1.2, linestyle=(0, (4, 3)), zorder=1)
    for label, color in [("Metro (RUCC 1–3)", BLUE), ("Nonmetro (RUCC 4–9)", GOLD)]:
        g = d.loc[d.setting.eq(label)]
        mx, my = g[old].median(), g[new].median()
        ax.scatter([mx], [my], s=150, marker="D", color=color, edgecolor=PAPER, linewidth=1.4, zorder=5)
        ax.annotate(
            f"{'Metro' if 'Metro (' == label[:7] else 'Nonmetro'} median\n{mx:.1f}% → {my:.1f}%",
            (mx, my),
            xytext=(11, 10 if label.startswith("Metro ") else -33),
            textcoords="offset points",
            fontsize=9,
            weight="bold",
            color=NAVY,
            arrowprops=dict(arrowstyle="-", color=color, lw=0.9),
        )
    ax.set_xlim(0, 65)
    ax.set_ylim(0, 65)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("Bachelor’s degree or higher, 1990 (%)")
    ax.set_ylabel("Bachelor’s degree or higher, 2019–23 (%)")
    ax.set_xticks(np.arange(0, 66, 10))
    ax.set_yticks(np.arange(0, 66, 10))
    polish_ax(ax)
    ax.legend(frameon=False, loc="upper left", fontsize=9)
    save(fig, "03_census_education_transition.png")
    return d, old, new


def fig4_education_rurality(d, old, new):
    rucc = "2023 Rural-urban Continuum Code"
    codes = list(range(1, 10))
    groups = [d.loc[d[rucc].eq(code), new] - d.loc[d[rucc].eq(code), old] for code in codes]
    medians = [g.median() for g in groups]
    counts = [len(g) for g in groups]

    fig, ax = plt.subplots(figsize=(12.5, 7.8))
    fig.subplots_adjust(left=0.1, right=0.97, top=0.81, bottom=0.27)
    frame(
        fig,
        "The typical attainment gain was largest in the most metropolitan counties",
        "Change in bachelor’s attainment, 1990 to 2019–23; each box summarizes county percentage-point gains",
        "Boxes show the middle half of county gains, center lines show medians, and whiskers extend to "
        "the most extreme values within 1.5× the interquartile range. RUCC 1–3 are metropolitan; "
        "4–9 are nonmetropolitan, with larger codes indicating less urban and less metro-adjacent settings. "
        "The pattern is descriptive; county medians are unweighted.",
        "Source: USDA county-level data, merged course file; RUCC 2023 classification and education measures.",
    )
    colors = [BLUE if code <= 3 else GOLD for code in codes]
    box = ax.boxplot(
        groups,
        positions=codes,
        widths=0.58,
        patch_artist=True,
        showfliers=False,
        medianprops=dict(color=NAVY, linewidth=2),
        whiskerprops=dict(color=GRAY, linewidth=1.1),
        capprops=dict(color=GRAY, linewidth=1.1),
        boxprops=dict(edgecolor=GRAY, linewidth=1.0),
    )
    for patch, color in zip(box["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.53)
    ax.scatter(codes, medians, s=45, color=NAVY, zorder=4, label="Median gain")
    for x, n in zip(codes, counts):
        ax.text(x, 25.8, f"n={n}", ha="center", va="bottom", fontsize=8.2, color=MUTED)
    ax.axvline(3.5, color=GRAY, lw=1, linestyle=(0, (4, 4)))
    ax.text(2, 28.5, "METRO", color=BLUE, weight="bold", ha="center", fontsize=9)
    ax.text(6.5, 28.5, "NONMETRO", color="#9A6D14", weight="bold", ha="center", fontsize=9)
    ax.set_xlim(0.35, 9.65)
    ax.set_ylim(-3, 31)
    ax.set_xticks(codes)
    ax.set_xlabel("2023 Rural–Urban Continuum Code (RUCC)")
    ax.set_ylabel("Change in adults with bachelor’s degree or higher (percentage points)")
    polish_ax(ax, xgrid=False, ygrid=True)
    ax.legend(frameon=False, loc="upper right", fontsize=9)
    save(fig, "04_census_education_rurality.png")


def fig5_migration_balance(census):
    xcol = "Net Migration Rate 2023"
    ycol = "Natural Change Rate 2023"
    rucc = "2023 Rural-urban Continuum Code"
    population = "Population Estimate 2023"
    d = census.dropna(subset=[xcol, ycol, rucc, population]).copy()
    d["setting"] = np.where(d[rucc] <= 3, "Metro (RUCC 1–3)", "Nonmetro (RUCC 4–9)")
    xmin, xmax = -50, 50
    ymin, ymax = -25, 20
    x = d[xcol].to_numpy()
    y = d[ycol].to_numpy()
    outside = (x < xmin) | (x > xmax) | (y < ymin) | (y > ymax)
    xclip, yclip = np.clip(x, xmin, xmax), np.clip(y, ymin, ymax)
    out_n = int(outside.sum())
    offset_n = int(((d[xcol] > 0) & (d[ycol] < 0)).sum())

    fig, ax = plt.subplots(figsize=(12.5, 8.2))
    fig.subplots_adjust(left=0.12, right=0.97, top=0.82, bottom=0.25)
    frame(
        fig,
        "Migration often offsets natural population decline",
        "County and county-equivalent 2023 net migration and natural change rates",
        f"Each point is one county or county equivalent ({len(d):,} observations). "
        f"{offset_n:,} had positive net migration alongside negative natural change. "
        "The diagonal marks equal-and-opposite rates, not a full population-growth calculation; "
        f"edge triangles mark {out_n} observations outside the plotted frame.",
        "Source: USDA county-level data, merged course file; 2023 rates (per 1,000 residents).",
    )
    ax.axvspan(0, xmax, ymin=0, ymax=1, color=PALE_TEAL, alpha=0.28, zorder=0)
    ax.axhline(0, color=MUTED, linewidth=1)
    ax.axvline(0, color=MUTED, linewidth=1)
    xx = np.linspace(xmin, xmax, 100)
    ax.plot(xx, -xx, color=NAVY, lw=1.2, linestyle=(0, (4, 3)), alpha=0.85, zorder=1)
    ax.scatter(
        xclip[d.setting.eq("Nonmetro")],
        yclip[d.setting.eq("Nonmetro")],
        s=17,
        color=GOLD,
        alpha=0.42,
        linewidth=0,
        label="Nonmetro (RUCC 4–9)",
        rasterized=True,
        zorder=2,
    )
    ax.scatter(
        xclip[d.setting.eq("Metro (RUCC 1–3)")],
        yclip[d.setting.eq("Metro (RUCC 1–3)")],
        s=17,
        color=BLUE,
        alpha=0.42,
        linewidth=0,
        label="Metro (RUCC 1–3)",
        rasterized=True,
        zorder=2,
    )
    if outside.any():
        ax.scatter(
            xclip[outside],
            yclip[outside],
            marker="^",
            s=25,
            facecolor="white",
            edgecolor=NAVY,
            linewidth=0.7,
            zorder=5,
            label="Outside frame",
        )
    ax.text(24, -14.5, "Migration offsets\nnatural decline", color=TEAL, fontsize=10, weight="bold", ha="center")
    ax.text(-27, 10.5, "Natural increase,\nnet out-migration", color=MUTED, fontsize=9.5, ha="center")
    ax.text(47, -19, "Equal & opposite", color=NAVY, fontsize=8.5, rotation=-44, ha="right")
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_xlabel("Net migration rate (per 1,000 residents)")
    ax.set_ylabel("Natural change rate (per 1,000 residents)")
    ax.set_xticks(np.arange(-50, 51, 10))
    ax.set_yticks(np.arange(-20, 21, 5))
    polish_ax(ax)
    ax.legend(frameon=False, loc="upper left", fontsize=9)
    save(fig, "05_census_migration_balance.png")
    return d, offset_n, out_n


def fig6_gender_gap(life):
    long = (
        life.loc[life["Sex"].isin(["Female", "Male"])]
        .pivot_table(
            index=["Country Name", "Year"],
            columns="Sex",
            values="Life Expectancy (years)",
            aggfunc="mean",
        )
        .reset_index()
    )
    long["gap"] = long["Female"] - long["Male"]
    wide = long.pivot(index="Country Name", columns="Year", values="gap")
    years = sorted(wide.columns)
    balanced = wide.dropna(subset=years)
    series = balanced[years]
    median = series.median(axis=0)
    q25 = series.quantile(0.25, axis=0)
    q75 = series.quantile(0.75, axis=0)

    fig, ax = plt.subplots(figsize=(12.5, 7.8))
    fig.subplots_adjust(left=0.11, right=0.97, top=0.82, bottom=0.25)
    frame(
        fig,
        "The typical female advantage widened, then leveled near five years",
        "Female minus male life expectancy at birth across a balanced panel of World Bank entities",
        f"The line is the unweighted median across {len(balanced)} entities with values for both sexes "
        "in every year from 1960–2023; the band shows the 25th–75th percentiles. The median rose from "
        f"{median.loc[1960]:.1f} years in 1960 to {median.loc[1990]:.1f} in 1990, then stayed close "
        f"to {median.loc[2023]:.1f} in 2023. Entities are equally weighted, so this is not a population-weighted global estimate.",
        "Source: World Bank life-expectancy series, course-provided file (1960–2023); female and male estimates.",
    )
    ax.fill_between(years, q25.to_numpy(), q75.to_numpy(), color=PALE_TEAL, alpha=0.9, label="Middle 50% of entities")
    ax.plot(years, median.to_numpy(), color=TEAL, lw=3.1, label="Median entity")
    ax.axhline(0, color=MUTED, lw=1, linestyle=(0, (4, 3)))
    for year in [1960, 1990, 2023]:
        val = median.loc[year]
        ax.scatter([year], [val], s=62, color=CORAL if year == 2023 else NAVY, zorder=5, edgecolor=PAPER, linewidth=1)
        if year == 1960:
            offset, align = (10, 13), "left"
        elif year == 2023:
            offset, align = (-10, 13), "right"
        else:
            offset, align = (0, 13), "center"
        ax.annotate(
            f"{val:.1f} years",
            (year, val),
            xytext=offset,
            textcoords="offset points",
            ha=align,
            fontsize=9,
            weight="bold",
            color=NAVY,
        )
    ax.set_xlim(1960, 2023)
    ax.set_ylim(-1, 10)
    ax.set_xticks([1960, 1970, 1980, 1990, 2000, 2010, 2020, 2023])
    ax.set_ylabel("Female life expectancy minus male (years)")
    ax.set_xlabel("Year")
    polish_ax(ax, xgrid=False, ygrid=True)
    ax.legend(frameon=False, loc="upper left", fontsize=9)
    save(fig, "06_life_expectancy_gender_gap.png")
    return balanced, median, q25, q75


def main():
    life = load_life()
    census = load_census()
    selected = fig1_life_deltas(life)
    fig2_recovery_scatter(life, selected)
    edu, old, new = fig3_education_transition(census)
    fig4_education_rurality(edu, old, new)
    migration, offsets, outside = fig5_migration_balance(census)
    balanced, median, q25, q75 = fig6_gender_gap(life)

    print("Created figures:", *sorted(p.name for p in OUT.glob("*.png")), sep="\n  ")
    print(
        "Life-expectancy recovery rows:",
        int((selected["2023 change"] >= 0).sum()),
        "/",
        len(selected),
    )
    print(
        "Education median gain, metro/nonmetro:",
        edu.groupby(edu["2023 Rural-urban Continuum Code"].le(3))[
            new
        ].median().sub(
            edu.groupby(edu["2023 Rural-urban Continuum Code"].le(3))[old].median()
        ).round(1).to_dict(),
    )
    print("Migration complete cases / positive migration with natural decline / clipped:", len(migration), offsets, outside)
    print("Gender-gap balanced entities / medians:", len(balanced), median.loc[[1960, 1990, 2023]].round(2).to_dict())


if __name__ == "__main__":
    main()
