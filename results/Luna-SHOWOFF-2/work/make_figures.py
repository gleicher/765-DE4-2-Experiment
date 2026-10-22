#!/opt/anaconda3/envs/p314/bin/python
"""Regenerate the six static figures for Design Exercise 4-2."""

from __future__ import annotations

import os
from pathlib import Path
import math

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / "work" / "mplconfig"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator
import numpy as np
import pandas as pd


DATA = ROOT / "data"
FIGURES = ROOT / "answers" / "figures"
FIGURES.mkdir(parents=True, exist_ok=True)

INK = "#203443"
MUTED = "#62727B"
GRID = "#DCE2E2"
PAPER = "#FCFBF8"
WHITE = "#FFFFFF"
ACCENT = "#D65F45"
BLUE = "#34799A"
GOLD = "#C3892F"
TEAL = "#2B7A78"
PURPLE = "#8064A2"

SEX_COLORS = {
    "Female": "#C45B57",
    "Male": "#397D9D",
    "Both": "#3B8A70",
}
GROUPS = [
    ("Metro", [1, 2, 3], "#287A78"),
    ("Micropolitan", [4, 5, 6], "#C3892F"),
    ("Rural", [7, 8, 9], "#8064A2"),
]
GROUP_COLOR = {name: color for name, _, color in GROUPS}

BA_COLS = [
    "Percent of adults with a bachelor's degree or higher, 1990",
    "Percent of adults with a bachelor's degree or higher, 2000",
    "Percent of adults with a bachelor's degree or higher, 2008-12",
    "Percent of adults with a bachelor's degree or higher, 2019-23",
]
BA_LABELS = ["1990", "2000", "2008–12", "2019–23"]
UNEMP_COLS = [f"Unemployment rate {year}" for year in range(2000, 2024)]


def setup_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 10,
            "axes.titlesize": 11,
            "axes.labelsize": 10,
            "text.color": INK,
            "axes.labelcolor": INK,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "axes.edgecolor": GRID,
            "axes.linewidth": 0.8,
            "figure.facecolor": PAPER,
            "axes.facecolor": PAPER,
            "savefig.facecolor": PAPER,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.14,
        }
    )


def clean_axis(ax: plt.Axes, *, grid_axis: str = "y") -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for edge in ("left", "bottom"):
        ax.spines[edge].set_color(GRID)
    ax.tick_params(length=0, pad=5)
    ax.grid(axis=grid_axis, color=GRID, linewidth=0.75)
    ax.set_axisbelow(True)


def add_header(
    fig: plt.Figure,
    title: str,
    subtitle: str,
    caption: str,
    source: str,
    *,
    bottom: float = 0.19,
) -> None:
    fig.suptitle(
        title,
        x=0.07,
        y=0.97,
        ha="left",
        va="top",
        fontsize=19,
        fontweight="bold",
        color=INK,
    )
    fig.text(
        0.07,
        0.91,
        subtitle,
        ha="left",
        va="top",
        fontsize=10.5,
        color=MUTED,
    )
    fig.text(
        0.07,
        0.075,
        caption,
        ha="left",
        va="bottom",
        fontsize=8.5,
        color=INK,
        wrap=True,
    )
    fig.text(
        0.07,
        0.035,
        source,
        ha="left",
        va="bottom",
        fontsize=7.5,
        color=MUTED,
    )
    fig.subplots_adjust(top=0.83, bottom=bottom, left=0.07, right=0.97)


def save(fig: plt.Figure, filename: str) -> None:
    fig.savefig(FIGURES / filename, dpi=240)
    plt.close(fig)


def load_lifespan() -> pd.DataFrame:
    df = pd.read_csv(DATA / "lifespan_dataset_1960.csv")
    df = df.drop(columns=["Unnamed: 0"], errors="ignore")
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df["Life Expectancy (years)"] = pd.to_numeric(
        df["Life Expectancy (years)"], errors="coerce"
    )
    return df


def lifespan_rebound_scatter(life: pd.DataFrame) -> tuple[list[str], int, int]:
    chosen_years = life[life["Year"].isin([2019, 2021, 2023])]
    wide = (
        chosen_years.pivot_table(
            index=["Country Name", "Country Code", "Sex"],
            columns="Year",
            values="Life Expectancy (years)",
            aggfunc="first",
        )
        .dropna(subset=[2019, 2021, 2023])
        .reset_index()
    )
    wide["shock"] = wide[2021] - wide[2019]
    wide["rebound"] = wide[2023] - wide[2021]
    wide["net_change"] = wide[2023] - wide[2019]

    both = wide[wide["Sex"] == "Both"].copy()
    selected = (
        both.nsmallest(6, "shock")["Country Name"].astype(str).tolist()
    )
    back_count = int((both["net_change"] >= 0).sum())
    total = len(both)

    fig, axes = plt.subplots(1, 3, figsize=(14.2, 6.0), sharex=True, sharey=True)
    fig.subplots_adjust(wspace=0.15)
    x_min = min(-9.0, math.floor(wide["shock"].min()))
    x_max = max(3.0, math.ceil(wide["shock"].max()))
    y_min = min(-3.0, math.floor(wide["rebound"].min()))
    y_max = max(9.0, math.ceil(wide["rebound"].max()))

    for ax, sex in zip(axes, ["Female", "Male", "Both"]):
        group = wide[wide["Sex"] == sex]
        ax.scatter(
            group["shock"],
            group["rebound"],
            s=21,
            color="#476579",
            alpha=0.36,
            linewidths=0,
            rasterized=True,
        )
        ax.axvline(0, color="#9BA9AD", lw=0.9, ls=":")
        ax.axhline(0, color="#9BA9AD", lw=0.9, ls=":")
        lo = max(x_min, -y_max)
        hi = min(x_max, -y_min)
        xx = np.linspace(lo, hi, 120)
        ax.plot(xx, -xx, color=INK, lw=1.1, ls=(0, (4, 3)), zorder=1)
        ax.text(
            0.04,
            0.96,
            sex,
            transform=ax.transAxes,
            ha="left",
            va="top",
            fontsize=11,
            fontweight="bold",
            color=INK,
        )
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
        ax.xaxis.set_major_locator(MaxNLocator(5))
        ax.yaxis.set_major_locator(MaxNLocator(5))
        clean_axis(ax, grid_axis="both")
        ax.set_xlabel("2019 → 2021 change (years)")
    axes[0].set_ylabel("2021 → 2023 change (years)")
    axes[0].text(
        0.67,
        0.75,
        "Back to 2019\nor higher",
        transform=axes[0].transAxes,
        fontsize=8,
        color=INK,
        rotation=-32,
        ha="center",
        va="center",
        bbox={"boxstyle": "round,pad=0.25", "fc": PAPER, "ec": "none", "alpha": 0.9},
    )

    # Mark the deepest Both-sex losses; manual offsets keep the labels legible.
    offsets = {
        "Bolivia": (22, 25),
        "Paraguay": (-55, -17),
        "Mexico": (20, 9),
        "Lebanon": (-55, -25),
    }
    for name, offset in offsets.items():
        row = both[both["Country Name"] == name]
        if row.empty:
            continue
        item = row.iloc[0]
        axes[2].scatter(
            item["shock"],
            item["rebound"],
            s=42,
            color=ACCENT,
            edgecolor=WHITE,
            linewidth=0.6,
            zorder=4,
        )
        axes[2].annotate(
            name,
            (item["shock"], item["rebound"]),
            xytext=offset,
            textcoords="offset points",
            fontsize=8,
            color=INK,
            arrowprops={"arrowstyle": "-", "color": MUTED, "lw": 0.7},
        )

    add_header(
        fig,
        f"Both-sex life expectancy returned to 2019 levels in {back_count} of {total} places by 2023",
        "Loss during 2019–21 versus change during 2021–23 · one point per country or region · panels by sex",
        "Above the dashed diagonal, the 2021–23 gain is large enough to return to the 2019 level. The 2021 troughs and later gains vary widely; the figure describes changes and does not attribute them to a single cause.",
        "Source: course-supplied World Bank life-expectancy file, 1960–2023.",
        bottom=0.21,
    )
    save(fig, "01-life-expectancy-loss-and-rebound.png")
    return selected, back_count, total


def lifespan_selected_trajectories(
    life: pd.DataFrame, selected: list[str]
) -> None:
    sample = life[
        life["Country Name"].isin(selected) & life["Year"].isin([2019, 2021, 2023])
    ].copy()
    sample["Country Name"] = pd.Categorical(
        sample["Country Name"], categories=selected, ordered=True
    )
    sample = sample.sort_values(["Country Name", "Sex", "Year"])
    years = [2019, 2021, 2023]
    y_min = math.floor(sample["Life Expectancy (years)"].min() - 2)
    y_max = math.ceil(sample["Life Expectancy (years)"].max() + 2)

    fig, axes = plt.subplots(2, 3, figsize=(14.2, 7.2), sharey=True)
    for ax, name in zip(axes.flat, selected):
        country = sample[sample["Country Name"] == name]
        for sex in ["Female", "Male", "Both"]:
            part = country[country["Sex"] == sex].sort_values("Year")
            ax.plot(
                part["Year"],
                part["Life Expectancy (years)"],
                color=SEX_COLORS[sex],
                lw=2.0,
                marker="o",
                markersize=4.2,
                label=sex,
            )
        both = country[country["Sex"] == "Both"].set_index("Year")
        shock = both.loc[2021, "Life Expectancy (years)"] - both.loc[
            2019, "Life Expectancy (years)"
        ]
        rebound = both.loc[2023, "Life Expectancy (years)"] - both.loc[
            2021, "Life Expectancy (years)"
        ]
        ax.set_title(name, loc="left", fontweight="bold", color=INK, pad=8)
        ax.text(
            0.98,
            0.96,
            f"Both: {shock:+.1f} → {rebound:+.1f} y",
            transform=ax.transAxes,
            ha="right",
            va="top",
            fontsize=8,
            color=MUTED,
        )
        ax.set_xticks(years, ["2019", "2021", "2023"])
        ax.set_ylim(y_min, y_max)
        clean_axis(ax)
    for ax in axes[:, 0]:
        ax.set_ylabel("Life expectancy (years)")
    handles = [
        Line2D([0], [0], color=SEX_COLORS[s], lw=2.2, marker="o", label=s)
        for s in ["Female", "Male", "Both"]
    ]
    fig.legend(
        handles=handles,
        loc="upper right",
        bbox_to_anchor=(0.97, 0.905),
        ncol=3,
        frameon=False,
        fontsize=9,
    )
    add_header(
        fig,
        "The deepest 2021 losses did not follow one recovery path",
        "Six places with the largest 2019–21 decline in the Both-sex series · each panel shows all three sex estimates",
        "Each line connects estimates for 2019, 2021, and 2023. The small label reports the Both-sex 2019–21 change followed by its 2021–23 change. The six places were selected using the Both-sex series, not because they represent every country.",
        "Source: course-supplied World Bank life-expectancy file, 1960–2023.",
        bottom=0.19,
    )
    save(fig, "02-life-expectancy-country-trajectories.png")


def load_census() -> pd.DataFrame:
    df = pd.read_csv(
        DATA / "full_census_dataset.csv",
        encoding="cp1252",
        dtype={"FIPS Code": str},
    )
    numeric_cols = (
        BA_COLS
        + UNEMP_COLS
        + [
            "Rural Urban Continuum Code 2023",
            "Net Migration Rate 2023",
            "Natural Change Rate 2023",
            "Population Estimate 2023",
        ]
    )
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.copy()
    rucc_col = "Rural Urban Continuum Code 2023"
    df["RUCC group"] = pd.Series(index=df.index, dtype="object")
    for name, codes, _ in GROUPS:
        df.loc[df[rucc_col].isin(codes), "RUCC group"] = name
    return df


def census_education_trend(census: pd.DataFrame) -> pd.DataFrame:
    # Complete cases hold the county set constant across the four survey periods.
    eligible = census.dropna(subset=BA_COLS + ["RUCC group"]).copy()
    summaries = {}
    for name, _, _ in GROUPS:
        subset = eligible[eligible["RUCC group"] == name]
        summaries[name] = {
            col: (
                subset[col].median(),
                subset[col].quantile(0.25),
                subset[col].quantile(0.75),
            )
            for col in BA_COLS
        }
    metro_gap_start = (
        summaries["Metro"][BA_COLS[0]][0] - summaries["Rural"][BA_COLS[0]][0]
    )
    metro_gap_end = (
        summaries["Metro"][BA_COLS[-1]][0] - summaries["Rural"][BA_COLS[-1]][0]
    )

    fig, ax = plt.subplots(figsize=(11.8, 6.0))
    x = np.arange(len(BA_COLS))
    for name, _, color in GROUPS:
        med = np.array([summaries[name][col][0] for col in BA_COLS])
        q1 = np.array([summaries[name][col][1] for col in BA_COLS])
        q3 = np.array([summaries[name][col][2] for col in BA_COLS])
        ax.fill_between(x, q1, q3, color=color, alpha=0.13, linewidth=0)
        ax.plot(x, med, color=color, lw=2.7, marker="o", markersize=6, label=name)
        ax.text(
            x[-1] + 0.07,
            med[-1],
            f"{med[-1]:.1f}%",
            color=color,
            fontsize=9,
            fontweight="bold",
            va="center",
        )
    ax.set_xticks(x, BA_LABELS)
    ax.set_xlim(-0.12, 3.53)
    ax.set_ylim(0, 45)
    ax.set_ylabel("Adults with a bachelor's degree or higher (%)")
    ax.set_xlabel("Survey period")
    ax.yaxis.set_major_locator(MaxNLocator(6))
    clean_axis(ax)
    ax.legend(
        loc="upper left",
        frameon=False,
        ncol=3,
        title="2023 Rural–Urban Continuum group",
        title_fontsize=9,
    )
    add_header(
        fig,
        f"The metro–rural bachelor's gap widened from {metro_gap_start:.1f} to {metro_gap_end:.1f} points",
        "Median county attainment across four periods · groups use the 2023 Rural–Urban Continuum Code",
        "Lines show the median county; translucent bands span the middle 50% of counties in each group. Counties are equally weighted, so these are not population-weighted estimates. The same complete set of counties is used at all four dates.",
        "Source: course-supplied USDA ERS county dataset; 2023 RUCC grouping: metro 1–3, micropolitan 4–6, rural 7–9.",
        bottom=0.22,
    )
    save(fig, "03-bachelors-attainment-by-rurality.png")
    return eligible


def census_education_paired(eligible: pd.DataFrame) -> None:
    fig = plt.figure(figsize=(14.2, 5.8))
    grid = fig.add_gridspec(1, 4, width_ratios=[1, 1, 1, 0.08], wspace=0.30)
    axes = [fig.add_subplot(grid[0, i]) for i in range(3)]
    colorbar_ax = fig.add_subplot(grid[0, 3])
    limit = 80
    hb = None
    for ax, (name, _, color) in zip(axes, GROUPS):
        subset = eligible[eligible["RUCC group"] == name]
        hb = ax.hexbin(
            subset[BA_COLS[0]],
            subset[BA_COLS[-1]],
            gridsize=36,
            mincnt=1,
            bins="log",
            cmap="GnBu",
            linewidths=0.15,
            edgecolors="white",
        )
        ax.plot([0, limit], [0, limit], color="#76878D", lw=1.0, ls=(0, (4, 3)))
        x_med = subset[BA_COLS[0]].median()
        y_med = subset[BA_COLS[-1]].median()
        ax.scatter(
            [x_med],
            [y_med],
            s=68,
            marker="D",
            color=color,
            edgecolor=WHITE,
            linewidth=1.0,
            zorder=5,
        )
        ax.annotate(
            f"median {x_med:.1f} → {y_med:.1f}%",
            (x_med, y_med),
            xytext=(7, 8),
            textcoords="offset points",
            fontsize=8,
            color=INK,
            bbox={"boxstyle": "round,pad=0.2", "fc": PAPER, "ec": "none", "alpha": 0.92},
        )
        ax.set_title(name, loc="left", fontweight="bold", color=INK)
        ax.set_xlim(0, limit)
        ax.set_ylim(0, limit)
        ax.set_aspect("equal", adjustable="box")
        ax.xaxis.set_major_locator(MaxNLocator(5))
        ax.yaxis.set_major_locator(MaxNLocator(5))
        clean_axis(ax, grid_axis="both")
    axes[0].set_ylabel("2019–23 adults with BA+ (%)")
    for ax in axes:
        ax.set_xlabel("1990 adults with BA+ (%)")
    cbar = fig.colorbar(hb, cax=colorbar_ax)
    cbar.set_label("Counties per hexagon (log scale)", fontsize=8)
    cbar.outline.set_visible(False)
    add_header(
        fig,
        "County attainment rose across every rurality group, but the metro lead persisted",
        "Paired county observations: 1990 on the x-axis, 2019–23 on the y-axis · current RUCC category",
        "Each hexagon summarizes county counts; darker cells contain more counties. The dashed diagonal marks no change, and the diamond marks each group's median county in both periods. Points and medians above the diagonal gained attainment. Axes share the same 0–80% scale.",
        "Source: course-supplied USDA ERS county dataset; complete cases only.",
        bottom=0.21,
    )
    save(fig, "04-bachelors-attainment-paired-counties.png")


def census_unemployment(census: pd.DataFrame) -> None:
    annual = {}
    for year, col in zip(range(2000, 2024), UNEMP_COLS):
        annual[year] = col

    fig, ax = plt.subplots(figsize=(12.2, 6.1))
    years = np.array(list(annual.keys()))
    medians = {}
    for name, _, color in GROUPS:
        med = []
        q1 = []
        q3 = []
        for year in years:
            vals = census.loc[census["RUCC group"] == name, annual[year]].dropna()
            med.append(vals.median())
            q1.append(vals.quantile(0.25))
            q3.append(vals.quantile(0.75))
        med = np.array(med)
        q1 = np.array(q1)
        q3 = np.array(q3)
        medians[name] = med
        ax.fill_between(years, q1, q3, color=color, alpha=0.10, linewidth=0)
        ax.plot(years, med, color=color, lw=2.5, label=name)
        ax.scatter(years[[0, 9, 20, 23]], med[[0, 9, 20, 23]], color=color, s=20, zorder=3)

    ax.axvline(2020, color=ACCENT, lw=1.1, ls=(0, (3, 3)), alpha=0.8)
    ax.text(2020.25, 0.97, "2020", transform=ax.get_xaxis_transform(), color=ACCENT, fontsize=8, va="top")
    ax.axvline(2009, color="#9AA8AC", lw=0.9, ls=":", alpha=0.75)
    ax.text(2009.25, 0.97, "2009", transform=ax.get_xaxis_transform(), color=MUTED, fontsize=8, va="top")
    ax.set_xlim(2000, 2025.5)
    ax.set_ylim(0, 16)
    ax.set_xticks([2000, 2005, 2010, 2015, 2020, 2023])
    ax.set_ylabel("Median county unemployment rate (%)")
    ax.set_xlabel("Year")
    clean_axis(ax)
    ax.legend(
        loc="upper left",
        frameon=False,
        ncol=3,
        title="2023 Rural–Urban Continuum group",
        title_fontsize=9,
    )
    metro_2019 = medians["Metro"][19]
    rural_2019 = medians["Rural"][19]
    metro_2020 = medians["Metro"][20]
    rural_2020 = medians["Rural"][20]
    metro_2023 = medians["Metro"][23]
    rural_2023 = medians["Rural"][23]
    add_header(
        fig,
        "A sharper metro spike in 2020 gave way to near-equal rural and metro rates",
        f"Median county rate: metro {metro_2019:.1f}% vs rural {rural_2019:.1f}% in 2019; {metro_2020:.1f}% vs {rural_2020:.1f}% in 2020; {metro_2023:.1f}% vs {rural_2023:.1f}% in 2023",
        "Lines show annual county medians; bands show the middle 50% of counties. The 2009 and 2020 markers orient the two visible spikes. County types are classified using the 2023 RUCC code; each county has equal weight, and the association does not explain why a rate changed.",
        "Source: course-supplied USDA ERS county dataset; unemployment rates, 2000–2023.",
        bottom=0.20,
    )
    save(fig, "05-county-unemployment-cycle.png")


def census_growth_balance(census: pd.DataFrame) -> None:
    xcol = "Natural Change Rate 2023"
    ycol = "Net Migration Rate 2023"
    required = [xcol, ycol, "RUCC group", "Population Estimate 2023"]
    d = census.dropna(subset=required).copy()
    d["net_change_rate"] = d[xcol] + d[ycol]
    erased = d[(d[xcol] < 0) & (d["net_change_rate"] > 0)]
    erased_count = len(erased)
    migration_offsets = d[(d[xcol] < 0) & (d[ycol] > 0)]
    offset_pct = 100 * erased_count / len(migration_offsets)

    min_pop = max(1.0, float(d["Population Estimate 2023"].min()))
    log_pop = np.log10(d["Population Estimate 2023"].clip(lower=min_pop))
    log_min, log_max = log_pop.min(), log_pop.max()
    if log_max == log_min:
        d["marker_area"] = 35.0
    else:
        d["marker_area"] = 8 + 115 * (log_pop - log_min) / (log_max - log_min)

    fig, (overview, detail) = plt.subplots(
        1,
        2,
        figsize=(14.2, 7.0),
        gridspec_kw={"width_ratios": [1.15, 1]},
    )

    def draw_panel(ax: plt.Axes, limits: tuple[float, float, float, float]) -> None:
        xmin, xmax, ymin, ymax = limits
        # Natural decrease is left of zero; above y=-x migration more than offsets it.
        left_hi = min(0, xmax)
        if xmin < left_hi:
            xx = np.linspace(xmin, left_hi, 120)
            yy = -xx
            ax.fill_between(
                xx,
                yy,
                ymax,
                where=yy < ymax,
                color="#D9E9DF",
                alpha=0.68,
                zorder=0,
                interpolate=True,
            )
        for name, _, color in GROUPS:
            sub = d[d["RUCC group"] == name]
            ax.scatter(
                sub[xcol],
                sub[ycol],
                s=sub["marker_area"],
                color=color,
                alpha=0.45,
                linewidths=0,
                rasterized=True,
                label=name,
                zorder=2,
            )
        ax.axhline(0, color="#829399", lw=0.9)
        ax.axvline(0, color="#829399", lw=0.9)
        line_lo = max(xmin, -ymax)
        line_hi = min(xmax, -ymin)
        if line_lo < line_hi:
            xx = np.linspace(line_lo, line_hi, 100)
            ax.plot(xx, -xx, color=INK, lw=1.25, ls=(0, (4, 3)), zorder=3)
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)
        ax.xaxis.set_major_locator(MaxNLocator(5))
        ax.yaxis.set_major_locator(MaxNLocator(5))
        clean_axis(ax, grid_axis="both")

    xmin = float(d[xcol].min())
    xmax = float(d[xcol].max())
    ymin = float(d[ycol].min())
    ymax = float(d[ycol].max())
    draw_panel(
        overview,
        (xmin - 3, xmax + 4, ymin - 4, ymax + 3),
    )
    overview.set_title("Every county area", loc="left", fontweight="bold")
    overview.set_xlabel("Natural change rate (reported units)")
    overview.set_ylabel("Net migration rate (reported units)")
    overview.text(
        0.03,
        0.96,
        f"{erased_count:,} of {len(migration_offsets):,}\n({offset_pct:.0f}%) above break-even",
        transform=overview.transAxes,
        ha="left",
        va="top",
        fontsize=9,
        fontweight="bold",
        color=INK,
        bbox={"boxstyle": "round,pad=0.3", "fc": PAPER, "ec": GRID, "alpha": 0.95},
    )
    dekalb = d[(d["Area name"] == "DeKalb County") & (d["State"] == "MO")]
    if not dekalb.empty:
        item = dekalb.iloc[0]
        overview.annotate(
            "DeKalb Co., MO",
            (item[xcol], item[ycol]),
            xytext=(12, 10),
            textcoords="offset points",
            fontsize=7.5,
            arrowprops={"arrowstyle": "-", "color": MUTED, "lw": 0.7},
        )
    loving = d[(d["Area name"] == "Loving County") & (d["State"] == "TX")]
    if not loving.empty:
        item = loving.iloc[0]
        overview.annotate(
            "Loving Co., TX",
            (item[xcol], item[ycol]),
            xytext=(8, 10),
            textcoords="offset points",
            fontsize=7.5,
            arrowprops={"arrowstyle": "-", "color": MUTED, "lw": 0.7},
        )

    # Axis-wise 2nd–98th percentile zoom; full data remain visible in overview.
    xlo, xhi = d[xcol].quantile([0.02, 0.98]).tolist()
    ylo, yhi = d[ycol].quantile([0.02, 0.98]).tolist()
    xpad = (xhi - xlo) * 0.06
    ypad = (yhi - ylo) * 0.07
    draw_panel(detail, (xlo - xpad, xhi + xpad, ylo - ypad, yhi + ypad))
    detail.set_title("Detail around the dense center", loc="left", fontweight="bold")
    detail.set_xlabel("Natural change rate (reported units)")
    detail.set_ylabel("Net migration rate (reported units)")

    sumter = d[(d["Area name"] == "Sumter County") & (d["State"] == "FL")]
    if not sumter.empty:
        item = sumter.iloc[0]
        detail.scatter(
            [item[xcol]],
            [item[ycol]],
            s=82,
            color=ACCENT,
            edgecolor=WHITE,
            linewidth=1.0,
            zorder=5,
        )
        detail.annotate(
            "Sumter Co., FL",
            (item[xcol], item[ycol]),
            xytext=(7, -15),
            textcoords="offset points",
            fontsize=8,
            arrowprops={"arrowstyle": "-", "color": MUTED, "lw": 0.7},
        )
    group_handles = [
        Line2D(
            [0],
            [0],
            marker="o",
            color="none",
            markerfacecolor=color,
            markeredgecolor="none",
            markersize=7,
            label=name,
        )
        for name, _, color in GROUPS
    ]
    size_values = [10_000, 100_000, 1_000_000]
    size_handles = []
    for value in size_values:
        value_log = np.log10(value)
        area = 8 + 115 * (value_log - log_min) / (log_max - log_min)
        area = max(8, min(123, area))
        size_handles.append(
            Line2D(
                [0],
                [0],
                marker="o",
                color="none",
                markerfacecolor="#73858A",
                markeredgecolor="none",
                markersize=math.sqrt(area),
                label=("1M" if value == 1_000_000 else f"{value / 1000:g}k"),
            )
        )
    handles = group_handles + size_handles
    labels = [h.get_label() for h in handles]
    fig.legend(
        handles,
        labels,
        loc="lower center",
        bbox_to_anchor=(0.52, 0.145),
        ncol=6,
        frameon=False,
        title="2023 county type  ·  marker area = population",
        title_fontsize=8.5,
        fontsize=8,
    )
    add_header(
        fig,
        f"Migration offset natural decrease in {offset_pct:.0f}% of county areas where both forces were present",
        f"{erased_count:,} of {len(migration_offsets):,} areas with natural decrease and positive migration · 2023 rate units as provided in the dataset",
        "The x-axis is natural change (births minus deaths); the y-axis is net migration. Above the dashed y = −x line, the two rates sum to a positive change. The left panel includes every complete observation; the right enlarges the central 2nd–98th percentile on each axis. Point size represents 2023 population.",
        "Source: course-supplied USDA ERS county dataset; 3,106 county areas with both rates and population available.",
        bottom=0.26,
    )
    save(fig, "06-county-natural-change-and-migration.png")


def main() -> None:
    setup_style()
    life = load_lifespan()
    selected, _, _ = lifespan_rebound_scatter(life)
    lifespan_selected_trajectories(life, selected)

    census = load_census()
    eligible = census_education_trend(census)
    census_education_paired(eligible)
    census_unemployment(census)
    census_growth_balance(census)
    print(f"Wrote figures to {FIGURES}")


if __name__ == "__main__":
    main()
