"""Create six static, worksheet-style figures for Design Exercise 4-2.

Run from this directory with:
    MPLCONFIGDIR=/private/tmp/p314-mpl-cache \
      /opt/anaconda3/envs/p314/bin/python work/make_figures.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
FIGURES = ROOT / "answers" / "figures"
DERIVED = ROOT / "work" / "derived"
FIGURES.mkdir(parents=True, exist_ok=True)
DERIVED.mkdir(parents=True, exist_ok=True)

BLUE = "#4E79A7"
ORANGE = "#F28E2B"
TEAL = "#59A14F"
RED = "#E15759"
PURPLE = "#B07AA1"
GRAY = "#797979"
LIGHT_GRAY = "#D9D9D9"
PALETTE = {
    "United States": BLUE,
    "Japan": ORANGE,
    "India": TEAL,
    "South Africa": RED,
    "Russian Federation": PURPLE,
    "Sweden": GRAY,
}
YEARS = [1960, 2019, 2021, 2023]
YEAR_COLORS = {
    1960: "#9C9C9C",
    2019: BLUE,
    2021: ORANGE,
    2023: "#222222",
}

plt.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.size": 9,
        "axes.titlesize": 10,
        "axes.labelsize": 9,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.edgecolor": "#B8B8B8",
        "axes.linewidth": 0.8,
        "grid.color": "#E8E8E8",
        "grid.linewidth": 0.7,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
    }
)


def title_and_subtitle(fig, title, subtitle):
    fig.suptitle(
        title,
        x=0.075,
        y=0.975,
        ha="left",
        va="top",
        fontsize=15,
        fontweight="normal",
        color="#262626",
    )
    fig.text(0.076, 0.925, subtitle, ha="left", va="top", fontsize=9, color="#555555")


def footer(fig, text):
    fig.text(
        0.076,
        0.025,
        text,
        ha="left",
        va="bottom",
        fontsize=7.7,
        color="#555555",
        wrap=True,
    )


def style_axis(ax, grid_axis="y"):
    ax.grid(True, axis=grid_axis, zorder=0)
    ax.tick_params(length=0, colors="#555555")
    ax.spines["left"].set_color("#B8B8B8")
    ax.spines["bottom"].set_color("#B8B8B8")


def save(fig, filename):
    fig.savefig(FIGURES / filename, dpi=170, bbox_inches="tight")
    plt.close(fig)


def read_life():
    return pd.read_csv(DATA / "lifespan_dataset_1960.csv")


def read_county_census():
    # The supplied county file is comma separated and contains Windows-1252 text.
    return pd.read_csv(DATA / "full_census_dataset.csv", encoding="cp1252")


def read_state_census():
    # The supplied state aggregate file is tab separated.
    return pd.read_csv(
        DATA / "aggregate_census_dataset.csv", sep="\t", encoding="cp1252"
    )


def make_life_gap_line():
    life = read_life()
    countries = list(PALETTE)
    selected = life[
        life["Country Name"].isin(countries)
        & life["Sex"].isin(["Female", "Male"])
    ]
    wide = selected.pivot_table(
        index=["Country Name", "Year"],
        columns="Sex",
        values="Life Expectancy (years)",
        aggfunc="first",
    ).reset_index()
    wide["Female advantage (years)"] = wide["Female"] - wide["Male"]
    wide = wide.dropna(subset=["Female advantage (years)"])
    wide.to_csv(DERIVED / "life_expectancy_gender_gap.csv", index=False)

    fig, ax = plt.subplots(figsize=(10.2, 6.1))
    fig.subplots_adjust(left=0.10, right=0.98, top=0.82, bottom=0.25)
    title_and_subtitle(
        fig,
        "The female longevity advantage took different paths across countries",
        "Female minus male life expectancy at birth, 1960–2023",
    )
    for country in countries:
        series = wide[wide["Country Name"] == country].sort_values("Year")
        ax.plot(
            series["Year"],
            series["Female advantage (years)"],
            color=PALETTE[country],
            linewidth=1.8,
            label=country,
            zorder=3,
        )
    ax.axhline(0, color="#333333", linewidth=1, zorder=2)
    ax.axvline(2020, color="#AFAFAF", linewidth=0.9, linestyle=(0, (3, 3)), zorder=1)
    ax.text(2020.8, 13.35, "2020", fontsize=8, color="#777777", va="top")
    ax.set_xlim(1960, 2024)
    ax.set_ylim(-2, 14)
    ax.set_xlabel("Year")
    ax.set_ylabel("Female advantage (years)")
    ax.set_xticks([1960, 1970, 1980, 1990, 2000, 2010, 2020])
    ax.set_yticks(np.arange(-2, 15, 2))
    style_axis(ax)
    ax.legend(
        ncol=3,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.15),
        frameon=False,
        fontsize=8,
        handlelength=2.4,
        columnspacing=1.8,
    )
    footer(
        fig,
        "Source: supplied World Bank life-expectancy data. Gap is calculated as female minus male life expectancy; "
        "a value below zero means male life expectancy is higher. Six countries selected to show different trajectories.",
    )
    save(fig, "1-life-gap-line.png")
    return wide


def make_life_gap_small_multiples(wide):
    countries = list(PALETTE)
    fig, axes = plt.subplots(3, 2, figsize=(10.2, 7.2), sharex=True, sharey=True)
    fig.subplots_adjust(left=0.085, right=0.98, top=0.84, bottom=0.17, hspace=0.48, wspace=0.20)
    title_and_subtitle(
        fig,
        "The size and direction of the gender gap differ by country",
        "Selected years make the long-term change and the 2019–21 disruption easier to compare",
    )
    for ax, country in zip(axes.flat, countries):
        series = wide[
            (wide["Country Name"] == country) & wide["Year"].isin(YEARS)
        ].sort_values("Year")
        x = np.arange(len(series))
        y = series["Female advantage (years)"].to_numpy()
        ax.plot(x, y, color="#888888", linewidth=1.15, zorder=1)
        for position, year in enumerate(series["Year"]):
            ax.scatter(
                position,
                series.iloc[position]["Female advantage (years)"],
                s=33,
                color=YEAR_COLORS[year],
                edgecolor="white",
                linewidth=0.5,
                zorder=2,
            )
        ax.axhline(0, color="#333333", linewidth=0.8, zorder=0)
        ax.set_title(country, loc="left", fontsize=9.5, color="#333333", pad=5)
        ax.set_xticks(np.arange(len(series)), [str(y) for y in series["Year"]])
        ax.set_ylim(-2, 14)
        ax.set_yticks([0, 5, 10])
        style_axis(ax)
    for ax in axes[-1, :]:
        ax.set_xlabel("Year")
    for ax in axes[:, 0]:
        ax.set_ylabel("Female minus male (years)")
    legend_handles = [
        Line2D(
            [0],
            [0],
            marker="o",
            linestyle="none",
            color=YEAR_COLORS[y],
            markeredgecolor="white",
            markersize=6,
            label=str(y),
        )
        for y in YEARS
    ]
    fig.legend(
        handles=legend_handles,
        ncol=4,
        loc="lower center",
        bbox_to_anchor=(0.52, 0.085),
        frameon=False,
        fontsize=8,
        title="Year",
        title_fontsize=8,
    )
    footer(
        fig,
        "Source: supplied World Bank life-expectancy data. Values below zero indicate a male advantage. "
        "Countries share a vertical scale; connected points are milestone years shown at equal spacing.",
    )
    save(fig, "2-life-gap-small-multiples.png")


def county_education_data():
    census = read_county_census()
    rucc = "2023 Rural-urban Continuum Code"
    cols = [
        "Percent of adults with a bachelor's degree or higher, 1990",
        "Percent of adults with a bachelor's degree or higher, 2000",
        "Percent of adults with a bachelor's degree or higher, 2008-12",
        "Percent of adults with a bachelor's degree or higher, 2019-23",
    ]
    years = ["1990", "2000", "2008–12", "2019–23"]
    census = census[[rucc, *cols]].copy()
    census["Settlement group"] = pd.Series(index=census.index, dtype="object")
    census.loc[census[rucc].between(1, 3), "Settlement group"] = "Metro"
    census.loc[census[rucc].between(4, 9), "Settlement group"] = "Nonmetro"
    subset = census.dropna(subset=["Settlement group"])
    records = []
    for field, year in zip(cols, years):
        for group, values in subset.groupby("Settlement group")[field]:
            records.append(
                {
                    "Year": year,
                    "Settlement group": group,
                    "Median county percent": values.median(),
                    "Counties": values.notna().sum(),
                }
            )
    medians = pd.DataFrame(records)
    medians.to_csv(DERIVED / "county_bachelors_medians.csv", index=False)
    latest = census[[rucc, cols[-1]]].dropna()
    latest.to_csv(DERIVED / "county_bachelors_latest.csv", index=False)
    return census, medians, cols, years, rucc


def make_education_trend(medians, years):
    fig, ax = plt.subplots(figsize=(9.7, 5.8))
    fig.subplots_adjust(left=0.10, right=0.96, top=0.82, bottom=0.20)
    title_and_subtitle(
        fig,
        "Bachelor’s attainment rose in both county groups as the gap widened",
        "Median county share of adults with a bachelor’s degree or higher",
    )
    colors = {"Metro": BLUE, "Nonmetro": ORANGE}
    for group in ["Metro", "Nonmetro"]:
        values = medians[medians["Settlement group"] == group]
        ax.plot(
            years,
            values["Median county percent"],
            marker="o",
            markersize=5.5,
            linewidth=2,
            color=colors[group],
            label=group,
            zorder=3,
        )
        last = values.iloc[-1]
        ax.annotate(
            f"{group}  {last['Median county percent']:.1f}%",
            (years[-1], last["Median county percent"]),
            xytext=(8, 0),
            textcoords="offset points",
            ha="left",
            va="center",
            fontsize=8.5,
            color=colors[group],
        )
    ax.set_ylim(0, 40)
    ax.set_xlabel("Education data period")
    ax.set_ylabel("Median county attainment (%)")
    ax.set_xticks(range(len(years)), years)
    style_axis(ax)
    ax.legend(loc="upper left", frameon=False, fontsize=8.5)
    footer(
        fig,
        "Source: supplied USDA county census file. Each county contributes one value to its group median; "
        "metro/nonmetro uses the 2023 Rural-urban Continuum Code (1–3 / 4–9). Education periods vary in length.",
    )
    save(fig, "3-county-education-trend.png")


def make_education_boxplot(census, cols, rucc):
    field = cols[-1]
    usable = census.dropna(subset=[rucc, field])
    codes = list(range(1, 10))
    boxdata = [
        usable.loc[usable[rucc] == code, field].to_numpy() for code in codes
    ]
    fig, ax = plt.subplots(figsize=(10.0, 6.0))
    fig.subplots_adjust(left=0.10, right=0.98, top=0.82, bottom=0.20)
    title_and_subtitle(
        fig,
        "Metro counties have higher attainment, but distributions overlap",
        "County-level bachelor’s attainment, 2019–23; blue = metro (1–3), orange = nonmetro (4–9)",
    )
    bp = ax.boxplot(
        boxdata,
        positions=codes,
        widths=0.56,
        patch_artist=True,
        showfliers=True,
        medianprops={"color": "#222222", "linewidth": 1.5},
        whiskerprops={"color": "#888888", "linewidth": 1.0},
        capprops={"color": "#888888", "linewidth": 1.0},
        flierprops={
            "marker": ".",
            "markersize": 2.1,
            "markerfacecolor": "#777777",
            "markeredgecolor": "#777777",
            "alpha": 0.36,
        },
    )
    for patch, code in zip(bp["boxes"], codes):
        patch.set_facecolor(BLUE if code <= 3 else ORANGE)
        patch.set_alpha(0.72)
        patch.set_edgecolor("#666666")
        patch.set_linewidth(0.8)
    ax.set_xlim(0.4, 9.6)
    ax.set_ylim(0, 80)
    ax.set_xticks(codes)
    ax.set_xlabel("2023 Rural-urban Continuum Code")
    ax.set_ylabel("Adults with bachelor’s degree or higher (%)")
    style_axis(ax)
    # The subtitle explains the fill colors, leaving the data area uncluttered.
    footer(
        fig,
        "Source: supplied USDA county census file. Each box summarizes counties (median and interquartile range; "
        "whiskers extend to 1.5×IQR); points beyond are outliers. Counties are equally weighted.",
    )
    save(fig, "4-county-education-boxplot.png")


def make_owid_history():
    owid = pd.read_csv(DATA / "life-expectancy-owid" / "life-expectancy-owid.csv")
    countries = ["United Kingdom", "Sweden", "United States", "Japan"]
    value = "Period life expectancy at birth"
    selected = owid[owid["Entity"].isin(countries) & (owid["Year"] >= 1900)].copy()
    selected.to_csv(DERIVED / "owid_life_expectancy_selected.csv", index=False)

    colors = {
        "United Kingdom": BLUE,
        "Sweden": ORANGE,
        "United States": TEAL,
        "Japan": RED,
    }
    fig, ax = plt.subplots(figsize=(10.0, 6.0))
    fig.subplots_adjust(left=0.10, right=0.98, top=0.82, bottom=0.25)
    title_and_subtitle(
        fig,
        "Long-run gains in life expectancy include sharp setbacks",
        "Period life expectancy at birth in four countries, observed estimates from 1900 onward",
    )
    for country in countries:
        series = selected[selected["Entity"] == country].sort_values("Year")
        ax.plot(
            series["Year"],
            series[value],
            color=colors[country],
            linewidth=1.7,
            label=country,
            zorder=3,
        )
    ax.axvline(2020, color="#AFAFAF", linewidth=0.9, linestyle=(0, (3, 3)), zorder=1)
    ax.text(2020.7, 37, "2020", fontsize=8, color="#777777", va="bottom")
    ax.set_xlim(1900, 2024)
    ax.set_ylim(25, 90)
    ax.set_xlabel("Year")
    ax.set_ylabel("Life expectancy at birth (years)")
    ax.set_xticks([1900, 1920, 1940, 1960, 1980, 2000, 2020])
    ax.set_yticks(np.arange(30, 91, 10))
    style_axis(ax)
    ax.legend(
        ncol=4,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.15),
        frameon=False,
        fontsize=8,
    )
    footer(
        fig,
        "Source: supplied Our World in Data historical life-expectancy file. The series combines estimates from "
        "multiple sources; lines connect observed years and do not imply causation.",
    )
    save(fig, "5-owid-long-run-life-expectancy.png")


def migration_category(row):
    natural = row["Natural Change Rate 2023"]
    migration = row["Net Migration Rate 2023"]
    if natural < 0 and migration > 0:
        return "Migration offsets natural decline"
    if natural < 0 and migration < 0:
        return "Both rates negative"
    if natural > 0 and migration < 0:
        return "Natural increase, net out-migration"
    return "Both rates positive"


def make_state_migration_scatter():
    state = read_state_census()
    state = (
        state[(state["State"] != "US") & (state["State"] != "PR")]
        .dropna(subset=["Natural Change Rate 2023", "Net Migration Rate 2023"])
        .copy()
    )
    state["Rate pattern"] = state.apply(migration_category, axis=1)
    state.to_csv(DERIVED / "state_population_change_2023.csv", index=False)

    palette = {
        "Migration offsets natural decline": ORANGE,
        "Both rates negative": RED,
        "Natural increase, net out-migration": PURPLE,
        "Both rates positive": BLUE,
    }
    fig, ax = plt.subplots(figsize=(9.8, 6.3))
    fig.subplots_adjust(left=0.11, right=0.98, top=0.82, bottom=0.30)
    offset_n = int((state["Rate pattern"] == "Migration offsets natural decline").sum())
    natural_decline_n = int((state["Natural Change Rate 2023"] < 0).sum())
    title_and_subtitle(
        fig,
        f"Migration offset natural decline in {offset_n} of {natural_decline_n} state-level areas",
        "2023 natural change and net migration rates for the 50 states and Washington, D.C.",
    )
    for pattern, color in palette.items():
        subset = state[state["Rate pattern"] == pattern]
        ax.scatter(
            subset["Natural Change Rate 2023"],
            subset["Net Migration Rate 2023"],
            s=42,
            color=color,
            edgecolor="white",
            linewidth=0.55,
            label=pattern,
            zorder=3,
        )
    ax.axhline(0, color="#555555", linewidth=0.9, linestyle=(0, (4, 3)), zorder=2)
    ax.axvline(0, color="#555555", linewidth=0.9, linestyle=(0, (4, 3)), zorder=2)

    # Label a few representative points to ground the statewide pattern without
    # crowding the dense center of the scatterplot.
    label_rows = state[state["State"].isin(["ME", "VT", "WV", "SC", "OR", "DC"])]
    for _, row in label_rows.iterrows():
        x = row["Natural Change Rate 2023"]
        y = row["Net Migration Rate 2023"]
        offset = {
            "ME": (7, -4),
            "VT": (7, 0),
            "WV": (7, 4),
            "SC": (7, 3),
            "OR": (7, -10),
            "DC": (7, 5),
        }[row["State"]]
        ax.annotate(
            row["State"],
            (x, y),
            xytext=offset,
            textcoords="offset points",
            ha="left",
            va="center",
            fontsize=7.5,
            color="#333333",
            zorder=4,
        )
    ax.set_xlim(-6.3, 8.6)
    ax.set_ylim(-8.6, 18.8)
    ax.set_xlabel("Natural change rate per 1,000 residents")
    ax.set_ylabel("Net migration rate per 1,000 residents")
    ax.set_xticks(np.arange(-6, 9, 2))
    ax.set_yticks(np.arange(-8, 19, 4))
    style_axis(ax, grid_axis="both")
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.16),
        frameon=False,
        fontsize=7.8,
        ncol=2,
        columnspacing=1.2,
        handletextpad=0.5,
    )
    footer(
        fig,
        "Source: supplied USDA state aggregate census file. 17 of 18 areas with negative natural change had "
        "positive net migration; Oregon had both rates below zero. Equal-size marks; rates are descriptive, not causal.",
    )
    save(fig, "6-state-migration-natural-change.png")


def main():
    gap = make_life_gap_line()
    make_life_gap_small_multiples(gap)
    census, medians, cols, years, rucc = county_education_data()
    make_education_trend(medians, years)
    make_education_boxplot(census, cols, rucc)
    make_owid_history()
    make_state_migration_scatter()
    print(f"Saved six figures to {FIGURES}")
    print(f"Saved derived tables to {DERIVED}")


if __name__ == "__main__":
    main()
