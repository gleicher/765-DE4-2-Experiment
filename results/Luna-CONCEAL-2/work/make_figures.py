"""Regenerate the six static figures for the DE 4-2 instructor example."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "answers" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

NAVY = "#17324D"
BLUE = "#2878A5"
ORANGE = "#D36A35"
TEAL = "#2A8C82"
PURPLE = "#8064A2"
GOLD = "#D6A52C"
INK = "#20313F"
MUTED = "#60717E"
GRID = "#DCE3E8"
PAPER = "#FFFFFF"
SEX_COLORS = {"Female": ORANGE, "Male": BLUE, "Both": NAVY}
COUNTRY_COLORS = {"United States": BLUE, "Peru": ORANGE, "China": TEAL}

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "axes.titlesize": 12,
        "axes.labelsize": 10,
        "figure.facecolor": PAPER,
        "axes.facecolor": PAPER,
        "text.color": INK,
        "axes.labelcolor": INK,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "axes.edgecolor": GRID,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.color": GRID,
        "grid.linewidth": 0.7,
        "grid.alpha": 0.8,
        "savefig.facecolor": PAPER,
    }
)


def finish(fig, filename):
    fig.savefig(OUT / filename, dpi=220, bbox_inches="tight")
    plt.close(fig)


def add_footer(fig, text):
    fig.text(0.105, 0.018, text, fontsize=8, color=MUTED, va="bottom")


def life_world_bank():
    return pd.read_csv(DATA / "lifespan_dataset_1960.csv")


def figure_1_life_levels():
    data = life_world_bank()
    countries = ["United States", "Peru", "China"]
    years = np.arange(2015, 2024)
    fig, axes = plt.subplots(1, 3, figsize=(14.5, 6.0), sharey=True)

    for ax, country in zip(axes, countries):
        part = data[
            data["Country Name"].eq(country)
            & data["Sex"].isin(["Female", "Male"])
            & data["Year"].between(2015, 2023)
        ]
        for sex in ["Female", "Male"]:
            line = part[part["Sex"].eq(sex)].sort_values("Year")
            ax.plot(
                line["Year"],
                line["Life Expectancy (years)"],
                color=SEX_COLORS[sex],
                marker="o",
                markersize=4.3,
                linewidth=2.2,
                label=sex,
            )
        ax.axvspan(2019.7, 2021.3, color="#E7EDF1", zorder=0)
        ax.axvline(2019, color=MUTED, lw=0.9, ls=(0, (3, 3)), zorder=1)
        ax.set_title(country, loc="left", color=INK, fontweight="bold", pad=10)
        ax.set_xlim(2014.7, 2023.35)
        ax.set_xticks([2015, 2017, 2019, 2021, 2023])
        ax.set_ylim(65, 89)
        ax.grid(axis="x", visible=False)
        ax.spines["left"].set_visible(False)
        ax.tick_params(axis="y", length=0)
        ax.text(
            0.02,
            0.04,
            "2019 reference",
            transform=ax.transAxes,
            fontsize=8,
            color=MUTED,
        )

    axes[0].set_ylabel("Life expectancy at birth (years)")
    fig.suptitle(
        "The pandemic-era setback was uneven—and recovery took different paths",
        x=0.105,
        y=0.985,
        ha="left",
        fontsize=18,
        fontweight="bold",
        color=NAVY,
    )
    fig.text(
        0.105,
        0.925,
        "Female and male estimates, 2015–2023; shaded band marks 2020–2021",
        fontsize=10,
        color=MUTED,
    )
    sex_handles = [
        Line2D([0], [0], color=SEX_COLORS[sex], marker="o", lw=2.2, label=sex)
        for sex in ["Female", "Male"]
    ]
    fig.legend(
        handles=sex_handles,
        frameon=False,
        ncol=2,
        loc="upper right",
        bbox_to_anchor=(0.9, 0.934),
    )
    add_footer(
        fig,
        "Peru’s male series fell 5.3 years from 2019 to 2021; U.S. estimates remained below 2019 in 2023, "
        "while China’s changed little. Source: World Bank life-expectancy data supplied for the course.",
    )
    fig.subplots_adjust(left=0.105, right=0.98, top=0.84, bottom=0.16, wspace=0.12)
    finish(fig, "01-life-levels.png")


def figure_2_life_change():
    data = life_world_bank()
    countries = ["United States", "Peru", "China"]
    fig, ax = plt.subplots(figsize=(11.8, 6.5))
    label_y = {
        ("Peru", "Female"): 2.45,
        ("Peru", "Male"): 1.35,
        ("China", "Female"): 0.25,
        ("China", "Male"): -0.75,
        ("United States", "Female"): -1.7,
        ("United States", "Male"): -2.65,
    }
    for country in countries:
        color = COUNTRY_COLORS[country]
        for sex, linestyle in [("Female", "-"), ("Male", (0, (4, 2)))]:
            part = data[
                data["Country Name"].eq(country)
                & data["Sex"].eq(sex)
                & data["Year"].between(2015, 2023)
            ].sort_values("Year")
            baseline = part.loc[part["Year"].eq(2019), "Life Expectancy (years)"].iloc[0]
            change = part["Life Expectancy (years)"] - baseline
            ax.plot(
                part["Year"],
                change,
                color=color,
                linestyle=linestyle,
                marker="o",
                markersize=4,
                linewidth=2,
            )
            last_y = float(change.iloc[-1])
            ax.annotate(
                f"{country} · {sex.lower()}",
                (2023, last_y),
                xytext=(2023.45, label_y[(country, sex)]),
                textcoords="data",
                arrowprops={"arrowstyle": "-", "color": color, "lw": 0.8},
                fontsize=8.5,
                color=color,
                va="center",
                clip_on=False,
            )

    ax.axhline(0, color=INK, lw=1.1)
    ax.axvline(2019, color=MUTED, lw=0.9, ls=(0, (3, 3)))
    ax.axvspan(2019.7, 2021.3, color="#E7EDF1", zorder=0)
    ax.set_xlim(2014.7, 2027.0)
    ax.set_ylim(-7.4, 4.7)
    ax.set_xticks(np.arange(2015, 2024))
    ax.set_ylabel("Change from 2019 (years)")
    ax.set_xlabel("Year")
    ax.grid(axis="x", visible=False)
    fig.suptitle(
        "Relative change makes the contrast clearer",
        x=0.10,
        y=0.985,
        ha="left",
        fontsize=18,
        fontweight="bold",
        color=NAVY,
    )
    fig.text(
        0.10,
        0.925,
        "Same six series as the primary view, indexed to each country–sex group’s 2019 estimate",
        fontsize=10,
        color=MUTED,
    )
    handles = [
        Line2D([0], [0], color=COUNTRY_COLORS[name], lw=2.5, label=name)
        for name in countries
    ] + [
        Line2D([0], [0], color=INK, lw=2, label="Female (solid) / male (dashed)")
    ]
    ax.legend(handles=handles, frameon=False, ncol=4, loc="lower left", bbox_to_anchor=(0, 1.005))
    add_footer(
        fig,
        "The zero line is each series’ 2019 level. Levels are descriptive life-expectancy estimates, not a causal measure. "
        "Source: World Bank course data.",
    )
    fig.subplots_adjust(left=0.10, right=0.80, top=0.79, bottom=0.14)
    finish(fig, "02-life-relative-change.png")


def census_data():
    d = pd.read_csv(DATA / "full_census_dataset.csv", encoding="cp1252")
    d["2013 Rural-urban Continuum Code"] = pd.to_numeric(
        d["2013 Rural-urban Continuum Code"], errors="coerce"
    )
    d["2023 Rural-urban Continuum Code"] = pd.to_numeric(
        d["2023 Rural-urban Continuum Code"], errors="coerce"
    )
    d["Population Estimate 2023"] = pd.to_numeric(
        d["Population Estimate 2023"], errors="coerce"
    )
    return d


EDU_COLS = [
    "Percent of adults with a bachelor's degree or higher, 1990",
    "Percent of adults with a bachelor's degree or higher, 2000",
    "Percent of adults with a bachelor's degree or higher, 2008-12",
    "Percent of adults with a bachelor's degree or higher, 2019-23",
]
PERIOD_LABELS = ["1990", "2000", "2008–12", "2019–23"]
GROUP_COLORS = {"Metro (codes 1–3)": BLUE, "Nonmetro (codes 4–9)": ORANGE}


def education_data():
    d = census_data()
    d = d[d["2013 Rural-urban Continuum Code"].between(1, 9)].copy()
    for col in EDU_COLS:
        d[col] = pd.to_numeric(d[col], errors="coerce")
    d["Area type"] = np.where(
        d["2013 Rural-urban Continuum Code"] <= 3,
        "Metro (codes 1–3)",
        "Nonmetro (codes 4–9)",
    )
    return d


def figure_3_education_distributions():
    data = education_data()
    fig, ax = plt.subplots(figsize=(11.2, 6.6))
    positions = {"Metro (codes 1–3)": [], "Nonmetro (codes 4–9)": []}
    for i, (col, period) in enumerate(zip(EDU_COLS, PERIOD_LABELS)):
        center = i * 1.45 + 1
        for group, offset in [("Metro (codes 1–3)", -0.19), ("Nonmetro (codes 4–9)", 0.19)]:
            vals = data.loc[data["Area type"].eq(group), col].dropna().values
            pos = center + offset
            positions[group].append(pos)
            bp = ax.boxplot(
                vals,
                positions=[pos],
                widths=0.31,
                showfliers=False,
                patch_artist=True,
                whis=(10, 90),
                manage_ticks=False,
                medianprops={"color": "white", "linewidth": 2},
                whiskerprops={"color": GROUP_COLORS[group], "linewidth": 1.2},
                capprops={"color": GROUP_COLORS[group], "linewidth": 1.2},
                boxprops={"edgecolor": GROUP_COLORS[group], "linewidth": 1.1},
            )
            bp["boxes"][0].set_facecolor(GROUP_COLORS[group])
            bp["boxes"][0].set_alpha(0.83)
            median = np.nanmedian(vals)
            ax.scatter(pos, median, s=14, color="white", zorder=4)

    ax.set_xticks([i * 1.45 + 1 for i in range(4)], PERIOD_LABELS)
    ax.set_xlim(0.45, 5.95)
    ax.set_ylim(0, 65)
    ax.set_ylabel("Adults with a bachelor’s degree or higher (%)")
    ax.set_xlabel("Education estimate period")
    ax.grid(axis="x", visible=False)
    ax.grid(axis="y", alpha=0.55)
    ax.set_title(
        "Attainment rose everywhere, but metro counties pulled farther ahead",
        loc="left",
        fontsize=17,
        fontweight="bold",
        color=NAVY,
        pad=18,
    )
    ax.text(
        0,
        1.02,
        "County distributions; whiskers show the 10th–90th percentiles, boxes the interquartile range",
        transform=ax.transAxes,
        fontsize=9.5,
        color=MUTED,
    )
    med = data.groupby("Area type")[EDU_COLS].median()
    gap0 = med.loc["Metro (codes 1–3)", EDU_COLS[0]] - med.loc["Nonmetro (codes 4–9)", EDU_COLS[0]]
    gap1 = med.loc["Metro (codes 1–3)", EDU_COLS[-1]] - med.loc["Nonmetro (codes 4–9)", EDU_COLS[-1]]
    ax.annotate(
        f"Median gap: {gap0:.1f} → {gap1:.1f} points",
        xy=(4.5, 50),
        xytext=(3.0, 60),
        arrowprops={"arrowstyle": "-", "color": MUTED, "lw": 1},
        color=INK,
        fontsize=10,
        ha="center",
    )
    handles = [
        plt.Rectangle((0, 0), 1, 1, facecolor=GROUP_COLORS[group], alpha=0.83, label=group)
        for group in GROUP_COLORS
    ]
    ax.legend(handles=handles, frameon=False, loc="upper left", ncol=2, bbox_to_anchor=(0, -0.12))
    add_footer(
        fig,
        "Metro/nonmetro grouping uses the 2013 Rural–Urban Continuum Code (metro = 1–3, nonmetro = 4–9); "
        "counties with missing attainment are omitted per period. Source: USDA county data supplied for the course.",
    )
    fig.subplots_adjust(left=0.11, right=0.97, top=0.82, bottom=0.19)
    finish(fig, "03-census-education-distributions.png")


def figure_4_education_county_scatter():
    data = education_data().dropna(subset=[EDU_COLS[0], EDU_COLS[-1]])
    fig, ax = plt.subplots(figsize=(8.8, 8.0))
    for group in GROUP_COLORS:
        part = data[data["Area type"].eq(group)]
        ax.scatter(
            part[EDU_COLS[0]],
            part[EDU_COLS[-1]],
            s=16,
            alpha=0.24,
            color=GROUP_COLORS[group],
            edgecolors="none",
            rasterized=True,
            label=group,
        )

    ax.plot([0, 65], [0, 65], color=MUTED, lw=1.2, ls=(0, (5, 4)), zorder=0)
    ax.text(47, 45, "same share in both periods", color=MUTED, fontsize=8.5, rotation=42)
    med = data.groupby("Area type")[[EDU_COLS[0], EDU_COLS[-1]]].median()
    for group, row in med.iterrows():
        ax.scatter(
            row[EDU_COLS[0]],
            row[EDU_COLS[-1]],
            marker="D",
            s=95,
            color=GROUP_COLORS[group],
            edgecolor="white",
            linewidth=1.4,
            zorder=5,
        )
        ax.annotate(
            f"{group.split(' ')[0]} median",
            (row[EDU_COLS[0]], row[EDU_COLS[-1]]),
            xytext=(9, 4 if "Metro" in group else -14),
            textcoords="offset points",
            fontsize=9,
            color=GROUP_COLORS[group],
            fontweight="bold",
        )
    ax.set_xlim(0, 65)
    ax.set_ylim(0, 65)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("Bachelor’s degree or higher, 1990 (%)")
    ax.set_ylabel("Bachelor’s degree or higher, 2019–23 (%)")
    ax.grid(alpha=0.45)
    ax.set_title(
        "Almost every county moved upward; metro counties started and ended higher",
        loc="left",
        fontsize=16.5,
        fontweight="bold",
        color=NAVY,
        pad=18,
    )
    ax.text(
        0,
        1.02,
        "Each point is a county or county equivalent; color shows 2013 metro status",
        transform=ax.transAxes,
        fontsize=9.5,
        color=MUTED,
    )
    med_1990 = med[EDU_COLS[0]]
    med_2023 = med[EDU_COLS[-1]]
    add_footer(
        fig,
        f"Median metro/nonmetro shares: {med_1990['Metro (codes 1–3)']:.1f}/{med_1990['Nonmetro (codes 4–9)']:.1f}% in 1990; "
        f"{med_2023['Metro (codes 1–3)']:.1f}/{med_2023['Nonmetro (codes 4–9)']:.1f}% in 2019–23. "
        "The diagonal marks no change. Source: USDA county data supplied for the course.",
    )
    ax.legend(frameon=False, loc="lower right")
    fig.subplots_adjust(left=0.12, right=0.97, top=0.84, bottom=0.14)
    finish(fig, "04-census-education-county-change.png")


def migration_data():
    d = census_data()
    cols = [
        "Net Migration Rate 2023",
        "Natural Change Rate 2023",
        "Population Estimate 2023",
    ]
    for col in cols:
        d[col] = pd.to_numeric(d[col], errors="coerce")
    d = d[
        d["2023 Rural-urban Continuum Code"].between(1, 9)
        & d["Net Migration Rate 2023"].notna()
        & d["Natural Change Rate 2023"].notna()
    ].copy()
    code = d["2023 Rural-urban Continuum Code"]
    d["Area type"] = np.select(
        [code.le(3), code.between(4, 7), code.ge(8)],
        ["Metro (1–3)", "Smaller urban centers (4–7)", "Most rural (8–9)"],
        default="Unclassified",
    )
    return d


def figure_5_migration_components():
    data = migration_data()
    colors = {
        "Metro (1–3)": BLUE,
        "Smaller urban centers (4–7)": ORANGE,
        "Most rural (8–9)": TEAL,
    }
    xlim = (-35, 45)
    ylim = (-20, 15)
    within = data[
        data["Net Migration Rate 2023"].between(*xlim)
        & data["Natural Change Rate 2023"].between(*ylim)
    ]
    outside = len(data) - len(within)
    fig, ax = plt.subplots(figsize=(10.5, 7.2))

    for group, color in colors.items():
        part = within[within["Area type"].eq(group)]
        population = part["Population Estimate 2023"].fillna(10000).clip(lower=100)
        sizes = 8 + 33 * np.sqrt(population / population.max())
        ax.scatter(
            part["Net Migration Rate 2023"],
            part["Natural Change Rate 2023"],
            s=sizes,
            alpha=0.42,
            color=color,
            edgecolors="white",
            linewidths=0.25,
            label=group,
            rasterized=True,
        )

    ax.axvline(0, color=MUTED, lw=1.0)
    ax.axhline(0, color=MUTED, lw=1.0)
    line_x = np.linspace(*xlim, 200)
    ax.plot(line_x, -line_x, color=NAVY, lw=1.5, ls=(0, (5, 3)), alpha=0.8)
    ax.text(
        28,
        -15.3,
        "net migration offsets natural decline\n(approx. zero total change)",
        color=NAVY,
        fontsize=8.5,
        ha="center",
    )
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xlabel("Net migration rate (per 1,000 residents), 2023")
    ax.set_ylabel("Natural change rate (per 1,000 residents), 2023")
    ax.grid(alpha=0.42)
    fig.suptitle(
        "Migration often countered natural population decline",
        x=0.12,
        y=0.98,
        ha="left",
        fontsize=17,
        fontweight="bold",
        color=NAVY,
    )
    fig.text(
        0.12,
        0.93,
        "Each mark is a county; size is proportional to the square root of population",
        fontsize=9.5,
        color=MUTED,
    )
    ax.legend(frameon=False, loc="upper left", ncol=1)
    add_footer(
        fig,
        f"2023 continuum codes define area type. Dashed line marks net migration + natural change = 0; "
        f"net migration offset natural decrease in 1,152 of 2,150 such counties. "
        f"{outside} counties beyond the displayed rate bounds are omitted for legibility. "
        "Rates are descriptive components, not causal effects. Source: USDA course data.",
    )
    fig.subplots_adjust(left=0.12, right=0.97, top=0.84, bottom=0.15)
    finish(fig, "05-census-migration-components.png")


def figure_6_historical_life_expectancy():
    data = pd.read_csv(DATA / "life-expectancy-owid" / "life-expectancy-owid.csv")
    countries = ["Sweden", "France", "United Kingdom", "United States", "China"]
    colors = {
        "Sweden": TEAL,
        "France": ORANGE,
        "United Kingdom": PURPLE,
        "United States": BLUE,
        "China": NAVY,
    }
    fig, ax = plt.subplots(figsize=(12.6, 7.0))
    for country in countries:
        part = data[data["Entity"].eq(country) & data["Year"].between(1800, 2023)]
        ax.plot(
            part["Year"],
            part["Period life expectancy at birth"],
            color=colors[country],
            marker="o",
            markersize=2.4,
            linewidth=1.8,
            label=country,
        )

    ax.annotate(
        "1918",
        xy=(1918, 34.84),
        xytext=(1892, 38.3),
        arrowprops={"arrowstyle": "->", "color": ORANGE, "lw": 1},
        fontsize=9,
        color=ORANGE,
        fontweight="bold",
    )
    ax.annotate(
        "China’s 1960 low: 33.4 years",
        xy=(1960, 33.419),
        xytext=(1968, 39),
        arrowprops={"arrowstyle": "->", "color": NAVY, "lw": 1},
        fontsize=9,
        color=NAVY,
        fontweight="bold",
    )
    ax.set_xlim(1800, 2027)
    ax.set_ylim(25, 90)
    ax.set_xticks([1800, 1850, 1900, 1950, 2000, 2020])
    ax.set_ylabel("Period life expectancy at birth (years)")
    ax.set_xlabel("Year")
    ax.grid(alpha=0.45)
    ax.set_title(
        "Life expectancy rose dramatically, but the path was punctuated by reversals",
        loc="left",
        fontsize=17,
        fontweight="bold",
        color=NAVY,
        pad=18,
    )
    ax.text(
        0,
        1.02,
        "Selected countries with long-run estimates; marks show the observed years in the supplied OWID series",
        transform=ax.transAxes,
        fontsize=9.5,
        color=MUTED,
    )
    ax.legend(frameon=False, ncol=5, loc="upper left", bbox_to_anchor=(0, 1.01))
    add_footer(
        fig,
        "The series combine sources and have uneven historical coverage; connecting lines guide the eye and do not imply "
        "a new observation in every intervening year. The annotations identify observed low points, not causes. "
        "Source: Our World in Data long-run life-expectancy data supplied for the course.",
    )
    fig.subplots_adjust(left=0.10, right=0.98, top=0.82, bottom=0.15)
    finish(fig, "06-life-expectancy-long-run.png")


def main():
    figure_1_life_levels()
    figure_2_life_change()
    figure_3_education_distributions()
    figure_4_education_county_scatter()
    figure_5_migration_components()
    figure_6_historical_life_expectancy()


if __name__ == "__main__":
    main()
