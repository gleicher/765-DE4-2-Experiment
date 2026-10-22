"""Generate the six static figures for the instructor review example.

Run from this folder with:
  MPLCONFIGDIR=work/.mpl-cache /opt/anaconda3/envs/p314/bin/python work/make_figures.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D


ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "answers" / "figures"
DATA = ROOT / "data"
FIGURES.mkdir(parents=True, exist_ok=True)

NAVY = "#315A78"
BLUE = "#4C78A8"
TEAL = "#4F8A8B"
ORANGE = "#D98245"
GOLD = "#C7A342"
PURPLE = "#8172A5"
GREEN = "#6B9A6B"
RED = "#B85C5C"
GREY = "#9B9B9B"
LIGHT_GREY = "#D9DDE1"
TEXT = "#252B30"
MUTED = "#626A70"

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "axes.labelcolor": TEXT,
        "text.color": TEXT,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "axes.edgecolor": LIGHT_GREY,
        "axes.linewidth": 0.8,
        "axes.titleweight": "normal",
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
    }
)


def polish_axes(ax, grid_axis="y"):
    ax.grid(axis=grid_axis, color="#E8EAEC", linewidth=0.8)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(LIGHT_GREY)


def add_header(fig, title, subtitle, caption):
    fig.text(0.075, 0.95, title, ha="left", va="top", fontsize=17, weight="medium")
    fig.text(0.075, 0.905, subtitle, ha="left", va="top", fontsize=10.5, color=MUTED)
    fig.text(0.075, 0.035, caption, ha="left", va="bottom", fontsize=8.5, color=MUTED)


def save(fig, name):
    fig.savefig(FIGURES / name, dpi=180, bbox_inches="tight")
    plt.close(fig)


def load_life():
    return pd.read_csv(DATA / "lifespan_dataset_1960.csv")


def load_census():
    # The county file contains a byte that is not valid UTF-8.
    frame = pd.read_csv(
        DATA / "full_census_dataset.csv",
        encoding="cp1252",
        dtype={"FIPS Code": str},
    )
    frame["FIPS Code"] = frame["FIPS Code"].str.zfill(5)
    return frame


def make_q1():
    life = load_life()
    region_codes = ["WLD", "NAC", "ECS", "EAS", "LCN", "MEA", "SAS", "SSF"]
    region_names = (
        life.loc[life["Country Code"].isin(region_codes), ["Country Code", "Country Name"]]
        .drop_duplicates()
        .set_index("Country Code")["Country Name"]
        .to_dict()
    )
    wide = (
        life[live_mask(life, region_codes)]
        .pivot_table(
            index=["Country Code", "Year"],
            columns="Sex",
            values="Life Expectancy (years)",
            aggfunc="mean",
        )
        .dropna(subset=["Female", "Male"])
        .reset_index()
    )
    wide["Gap"] = wide["Female"] - wide["Male"]
    palette = {
        "WLD": NAVY,
        "NAC": ORANGE,
        "ECS": TEAL,
        "EAS": PURPLE,
        "LCN": GREEN,
        "MEA": RED,
        "SAS": GOLD,
        "SSF": BLUE,
    }

    # Q1 primary: year on Columns; Female - Male as a calculated measure on Rows;
    # World Bank geographic aggregate on Color.
    fig, ax = plt.subplots(figsize=(11.5, 6.7))
    fig.subplots_adjust(left=0.1, right=0.79, top=0.81, bottom=0.14)
    add_header(
        fig,
        "Women’s life-expectancy advantage grew modestly worldwide",
        "Female minus male life expectancy, by World Bank geographic aggregate, 1960–2023",
        "A positive value means women’s estimated life expectancy is higher. World is shown in a darker, heavier line.",
    )
    for code in region_codes:
        data = wide[wide["Country Code"] == code].sort_values("Year")
        ax.plot(
            data["Year"],
            data["Gap"],
            color=palette[code],
            linewidth=2.6 if code == "WLD" else 1.6,
            alpha=1.0 if code == "WLD" else 0.9,
            label="World" if code == "WLD" else region_names[code],
        )
    ax.set_xlim(1960, 2025)
    ax.set_xticks([1960, 1970, 1980, 1990, 2000, 2010, 2020])
    ax.set_ylim(0, 9.5)
    ax.set_yticks(np.arange(0, 10, 1))
    ax.set_xlabel("Year")
    ax.set_ylabel("Female − male life expectancy (years)")
    polish_axes(ax)
    ax.legend(
        frameon=False,
        loc="center left",
        bbox_to_anchor=(1.01, 0.5),
        title="Geographic aggregate",
        fontsize=9,
    )
    world = wide[wide["Country Code"] == "WLD"].set_index("Year")["Gap"]
    ax.annotate(
        f"{world.loc[1960]:.1f}",
        (1960, world.loc[1960]),
        xytext=(5, -14),
        textcoords="offset points",
        color=NAVY,
        fontsize=9,
        weight="bold",
    )
    ax.annotate(
        f"{world.loc[2023]:.1f}",
        (2023, world.loc[2023]),
        xytext=(-26, 8),
        textcoords="offset points",
        color=NAVY,
        fontsize=9,
        weight="bold",
    )
    save(fig, "q1_life_expectancy_region_trend.png")

    # Q1 alternate: region on Rows; gap on Columns; year encoded by point color.
    endpoints = wide[wide["Year"].isin([1960, 2023])].pivot(
        index="Country Code", columns="Year", values="Gap"
    )
    endpoints = endpoints.dropna(subset=[1960, 2023]).sort_values(2023)
    short_names = {
        "WLD": "World",
        "NAC": "North America",
        "ECS": "Europe & Central Asia",
        "EAS": "East Asia & Pacific",
        "LCN": "Latin America & Caribbean",
        "MEA": "Middle East, North Africa,\nAfghanistan & Pakistan",
        "SAS": "South Asia",
        "SSF": "Sub-Saharan Africa",
    }
    codes = endpoints.index.tolist()
    labels = [short_names.get(c, region_names[c]) for c in codes]
    fig, ax = plt.subplots(figsize=(11.5, 6.8))
    fig.subplots_adjust(left=0.29, right=0.88, top=0.81, bottom=0.14)
    add_header(
        fig,
        "The female advantage changed by region",
        "A two-date comparison shows both the direction and the regional spread",
        "Each line connects the same region’s 1960 and 2023 estimates. The difference is descriptive, not a measure of cause.",
    )
    y = np.arange(len(codes))
    for yi, code in enumerate(codes):
        ax.plot(
            [endpoints.loc[code, 1960], endpoints.loc[code, 2023]],
            [yi, yi],
            color="#B6BBC0",
            linewidth=2,
            zorder=1,
        )
    ax.scatter(endpoints[1960], y, s=52, color=GOLD, edgecolor="white", linewidth=0.8, zorder=3)
    ax.scatter(endpoints[2023], y, s=52, color=NAVY, edgecolor="white", linewidth=0.8, zorder=3)
    for yi, code in enumerate(codes):
        ax.text(endpoints.loc[code, 1960] - 0.13, yi + 0.18, f"{endpoints.loc[code, 1960]:.1f}", ha="right", va="center", fontsize=8, color=MUTED)
        ax.text(endpoints.loc[code, 2023] + 0.13, yi + 0.18, f"{endpoints.loc[code, 2023]:.1f}", ha="left", va="center", fontsize=8, color=MUTED)
    ax.set_yticks(y, labels)
    ax.set_xlim(-2, 9)
    ax.set_xticks(np.arange(-2, 10, 1))
    ax.set_xlabel("Female − male life expectancy (years)")
    ax.set_ylim(-0.6, len(codes) - 0.3)
    ax.invert_yaxis()
    polish_axes(ax, grid_axis="x")
    ax.legend(
        handles=[
            Line2D([], [], marker="o", linestyle="", color=GOLD, label="1960"),
            Line2D([], [], marker="o", linestyle="", color=NAVY, label="2023"),
        ],
        frameon=False,
        title="Year",
        loc="lower right",
    )
    save(fig, "q1_life_expectancy_region_endpoints.png")


def live_mask(frame, codes):
    return frame["Country Code"].isin(codes) & frame["Sex"].isin(["Female", "Male"])


def prep_census():
    census = load_census()
    education = "Percent of adults with a bachelor's degree or higher, 2019-23"
    unemployment = "Unemployment rate 2023"
    migration = "Net Migration Rate 2023"
    natural = "Natural Change Rate 2023"
    population = "Population Estimate 2023"
    rucc = "Rural Urban Continuum Code 2023"
    census["Settlement"] = np.where(census[rucc] <= 3, "Metro (codes 1–3)", "Nonmetro (codes 4–9)")
    return census, education, unemployment, migration, natural, population, rucc


def make_q2():
    census, education, unemployment, _, _, _, _ = prep_census()
    data = census.dropna(subset=[education, unemployment]).copy()
    colors = {"Metro (codes 1–3)": NAVY, "Nonmetro (codes 4–9)": ORANGE}

    # Q2 primary: county marks; education on Columns; unemployment on Rows;
    # metro/nonmetro on Color, with separate trend lines.
    fig, ax = plt.subplots(figsize=(10.8, 7))
    fig.subplots_adjust(left=0.11, right=0.82, top=0.81, bottom=0.16)
    add_header(
        fig,
        "Higher county degree attainment tends to accompany lower unemployment",
        "Each mark is a county; 2019–23 bachelor’s attainment compared with the 2023 unemployment rate",
        "The fitted lines summarize county-level association. Metro means 2023 Rural–Urban Continuum codes 1–3; nonmetro means 4–9.",
    )
    for settlement in colors:
        subset = data[data["Settlement"] == settlement]
        ax.scatter(
            subset[education],
            subset[unemployment],
            s=15,
            alpha=0.42,
            color=colors[settlement],
            edgecolors="none",
            label=f"{settlement} (n={len(subset):,})",
        )
        slope, intercept = np.polyfit(subset[education], subset[unemployment], 1)
        xs = np.linspace(0, 75, 100)
        ax.plot(xs, slope * xs + intercept, color=colors[settlement], linewidth=2.1)
    ax.set_xlim(0, 78)
    ax.set_ylim(0, max(16, data[unemployment].quantile(0.995) + 1))
    ax.set_xlabel("Adults with a bachelor’s degree or higher (%)")
    ax.set_ylabel("Unemployment rate, 2023 (%)")
    polish_axes(ax)
    ax.legend(frameon=False, loc="upper right", fontsize=9)
    save(fig, "q2_census_education_unemployment_scatter.png")

    # Q2 alternate: education quartile on Columns; unemployment distribution on
    # Rows; metro/nonmetro split into panes (a standard box-plot workflow).
    data["Education band"] = pd.qcut(
        data[education],
        4,
        labels=["Lowest", "Lower-middle", "Upper-middle", "Highest"],
        duplicates="drop",
    )
    bands = ["Lowest", "Lower-middle", "Upper-middle", "Highest"]
    fig, axes = plt.subplots(1, 2, figsize=(12, 7), sharey=True)
    fig.subplots_adjust(left=0.09, right=0.98, top=0.81, bottom=0.18, wspace=0.08)
    add_header(
        fig,
        "Lower unemployment medians recur across education bands",
        "County unemployment distributions by bachelor’s-attainment quartile and settlement type",
        "Bands are quartiles of county attainment across the full sample. Boxes show median and interquartile range; whiskers extend to 1.5×IQR. Outlier marks are omitted.",
    )
    for ax, settlement in zip(axes, colors, strict=True):
        subset = data[data["Settlement"] == settlement]
        samples = [subset.loc[subset["Education band"] == band, unemployment].dropna() for band in bands]
        bp = ax.boxplot(
            samples,
            positions=np.arange(1, 5),
            widths=0.56,
            patch_artist=True,
            showfliers=False,
            medianprops={"color": TEXT, "linewidth": 1.6},
            whiskerprops={"color": "#8C949A", "linewidth": 1},
            capprops={"color": "#8C949A", "linewidth": 1},
        )
        for box in bp["boxes"]:
            box.set_facecolor(colors[settlement])
            box.set_alpha(0.55)
            box.set_edgecolor(colors[settlement])
        ax.set_title(f"{settlement}\nn={len(subset):,} counties", fontsize=10, pad=8)
        ax.set_xticks(range(1, 5), bands, rotation=18, ha="right")
        ax.set_ylim(0, 9)
        ax.grid(axis="y", color="#E8EAEC", linewidth=0.8)
        ax.set_axisbelow(True)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
    axes[0].set_ylabel("Unemployment rate, 2023 (%)")
    save(fig, "q2_census_education_unemployment_boxplots.png")


def make_q3():
    census, _, _, migration, natural, population, _ = prep_census()
    data = census.dropna(subset=[migration, natural]).copy()
    xlim = (-30, 50)
    ylim = (-16, 11)
    visible = data[migration].between(*xlim) & data[natural].between(*ylim)
    omitted = int((~visible).sum())
    n_positive_migration_negative_natural = int(((data[migration] > 0) & (data[natural] < 0)).sum())
    fraction = n_positive_migration_negative_natural / len(data)
    colors = {"Metro (codes 1–3)": NAVY, "Nonmetro (codes 4–9)": ORANGE}

    # Q3: one mark per county; net migration on Columns, natural change on Rows,
    # settlement type on Color. Zero reference lines expose the four quadrants.
    fig, ax = plt.subplots(figsize=(10.8, 7))
    fig.subplots_adjust(left=0.11, right=0.83, top=0.81, bottom=0.17)
    add_header(
        fig,
        "Migration offset natural decrease in about half of counties",
        f"In 2023, {n_positive_migration_negative_natural:,} of {len(data):,} counties ({fraction:.0%}) had positive net migration and negative natural change",
        f"Each dot is a county; color shows metro status. Axes focus on the central range; {omitted} counties beyond the displayed limits are omitted.",
    )
    for settlement in colors:
        subset = data[data["Settlement"] == settlement]
        subset = subset[subset[migration].between(*xlim) & subset[natural].between(*ylim)]
        ax.scatter(
            subset[migration],
            subset[natural],
            s=18,
            alpha=0.42,
            color=colors[settlement],
            edgecolors="none",
            label=f"{settlement} (n={len(subset):,} shown)",
        )
    ax.axhline(0, color="#747C82", linewidth=1.2)
    ax.axvline(0, color="#747C82", linewidth=1.2)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xlabel("Net migration rate, 2023 (per 1,000 residents)")
    ax.set_ylabel("Natural change rate, 2023 (per 1,000 residents)")
    polish_axes(ax, grid_axis="both")
    ax.legend(
        frameon=False,
        loc="upper left",
        bbox_to_anchor=(1.01, 0.98),
        fontsize=9,
        labels=["Metro (1–3)", "Nonmetro (4–9)"],
    )
    ax.text(
        0.98,
        0.035,
        "Positive migration offsets\nnegative natural change",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=8.5,
        color=MUTED,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.85, "pad": 3},
    )
    save(fig, "q3_census_population_change_components.png")


def make_q4():
    life = load_life()
    wide = (
        life[life["Sex"] == "Both"]
        .pivot_table(
            index=["Country Name", "Country Code"],
            columns="Year",
            values="Life Expectancy (years)",
            aggfunc="mean",
        )
        .dropna(subset=[2019, 2021, 2023])
    )
    wide["Change 2019–21"] = wide[2021] - wide[2019]
    wide["Change 2021–23"] = wide[2023] - wide[2021]
    selected = wide.nsmallest(12, "Change 2019–21").sort_values("Change 2019–21")
    world = wide.loc[("World", "WLD")]
    years = [2019, 2021, 2023]

    # Q4: selected entities on Rows; life expectancy on Columns; Year on Color.
    # Selection is explicit: twelve largest 2019–21 declines with all dates present.
    fig, ax = plt.subplots(figsize=(11, 7.3))
    fig.subplots_adjust(left=0.18, right=0.92, top=0.81, bottom=0.16)
    add_header(
        fig,
        "The largest 2019–21 declines were followed by uneven rebounds",
        f"World estimate: {world[2019]:.1f} years in 2019, {world[2021]:.1f} in 2021, and {world[2023]:.1f} in 2023",
        "Twelve entities with the largest 2019–21 declines, among records with values in all three years. This selected comparison describes timing; it does not establish cause.",
    )
    y_positions = np.arange(len(selected))
    for y, (_, row) in zip(y_positions, selected.iterrows(), strict=True):
        ax.plot([row[2019], row[2021], row[2023]], [y, y, y], color="#C4C8CC", linewidth=2, zorder=1)
    series_colors = {2019: GOLD, 2021: RED, 2023: NAVY}
    for year in years:
        ax.scatter(
            selected[year],
            y_positions,
            s=46,
            color=series_colors[year],
            edgecolor="white",
            linewidth=0.8,
            zorder=2,
            label=str(year),
        )
    labels = [name for name, _ in selected.index]
    ax.set_yticks(y_positions, labels)
    ax.invert_yaxis()
    ax.set_xlim(55, 90)
    ax.set_xticks(np.arange(55, 91, 5))
    ax.set_xlabel("Life expectancy at birth (years)")
    polish_axes(ax, grid_axis="x")
    ax.legend(
        frameon=False,
        title="Year",
        loc="lower right",
        ncol=3,
        bbox_to_anchor=(1, 1.02),
    )
    save(fig, "q4_life_expectancy_pandemic_dips.png")


if __name__ == "__main__":
    make_q1()
    make_q2()
    make_q3()
    make_q4()
