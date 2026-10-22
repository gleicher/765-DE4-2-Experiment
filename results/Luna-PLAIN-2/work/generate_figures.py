"""Generate the six static figures for Design Exercise 4-2."""

from pathlib import Path
import os

os.environ.setdefault(
    "MPLCONFIGDIR",
    str(Path(__file__).resolve().parent / ".matplotlib"),
)

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter, MultipleLocator
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
FIGURES = ROOT / "answers" / "figures"
FIGURES.mkdir(parents=True, exist_ok=True)

COLORS = {
    "ink": "#20313A",
    "muted": "#52646D",
    "grid": "#E5E9E8",
    "blue": "#25627A",
    "teal": "#16877C",
    "gold": "#E4A33C",
    "coral": "#C9654D",
    "light_blue": "#D9E9EC",
    "light_gold": "#F4E5C6",
    "light_teal": "#DCEDE8",
    "light_coral": "#F3E0DA",
    "paper": "#FFFFFF",
}

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "axes.labelcolor": COLORS["ink"],
        "xtick.color": COLORS["muted"],
        "ytick.color": COLORS["muted"],
        "text.color": COLORS["ink"],
        "axes.edgecolor": COLORS["grid"],
        "axes.linewidth": 0.8,
        "figure.facecolor": COLORS["paper"],
        "axes.facecolor": COLORS["paper"],
        "savefig.facecolor": COLORS["paper"],
    }
)


def setup_figure(kicker, title, subtitle, *, width=11.5, height=7.2):
    fig, ax = plt.subplots(figsize=(width, height))
    fig.subplots_adjust(left=0.105, right=0.965, top=0.73, bottom=0.17)
    fig.text(
        0.105,
        0.95,
        kicker.upper(),
        fontsize=9,
        fontweight="bold",
        color=COLORS["teal"],
        va="top",
    )
    fig.text(
        0.105,
        0.908,
        title,
        fontsize=20,
        fontweight="bold",
        color=COLORS["ink"],
        va="top",
    )
    fig.text(
        0.105,
        0.855,
        subtitle,
        fontsize=11,
        color=COLORS["muted"],
        va="top",
    )
    return fig, ax


def footer(fig, text):
    fig.text(
        0.105,
        0.055,
        text,
        fontsize=8.3,
        color=COLORS["muted"],
        va="bottom",
        wrap=True,
    )


def polish_axis(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(COLORS["grid"])
    ax.spines["bottom"].set_color(COLORS["grid"])
    ax.grid(axis="y", color=COLORS["grid"], linewidth=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(length=0, pad=7)


def save(fig, filename):
    fig.savefig(FIGURES / filename, dpi=220, bbox_inches="tight")
    plt.close(fig)


def load_life():
    df = pd.read_csv(DATA / "lifespan_dataset_1960.csv")
    df = df.drop(columns=["Unnamed: 0"], errors="ignore")
    return df


def load_census():
    # The local file is comma-delimited and uses Windows-1252 text encoding.
    df = pd.read_csv(
        DATA / "full_census_dataset.csv",
        sep=",",
        encoding="cp1252",
        dtype={"FIPS Code": str},
        low_memory=False,
    )
    return df


def numeric(df, columns):
    df[columns] = df[columns].apply(pd.to_numeric, errors="coerce")
    return df.copy()


def life_gap_data():
    life = load_life()
    paired = life[life["Sex"].isin(["Female", "Male"])].pivot_table(
        index=["Country Name", "Country Code", "Year"],
        columns="Sex",
        values="Life Expectancy (years)",
        aggfunc="first",
    )
    paired = paired.dropna(subset=["Female", "Male"]).reset_index()
    paired["Female advantage (years)"] = paired["Female"] - paired["Male"]
    return paired


def figure_1_life_gap_distribution():
    gap = life_gap_data()
    yearly = (
        gap.groupby("Year")["Female advantage (years)"]
        .agg(
            median="median",
            p10=lambda values: values.quantile(0.10),
            p25=lambda values: values.quantile(0.25),
            p75=lambda values: values.quantile(0.75),
            p90=lambda values: values.quantile(0.90),
        )
        .reset_index()
    )
    start = gap[gap["Year"] == 1960]["Female advantage (years)"]
    end = gap[gap["Year"] == 2023]["Female advantage (years)"]
    start_negative = int((start < 0).sum())
    end_negative = int((end < 0).sum())
    start_median = start.median()
    end_median = end.median()
    peak_median = yearly.loc[yearly["median"].idxmax()]

    fig, ax = setup_figure(
        "Story 1 · life expectancy · distribution over time",
        "By 2023, every reporting entity had a female advantage",
        (
            f"The median gap rose from {start_median:.1f} years in 1960 to "
            f"{end_median:.1f} in 2023, with most growth before 1980."
        ),
    )
    x = yearly["Year"].to_numpy()
    ax.fill_between(
        x,
        yearly["p10"].to_numpy(),
        yearly["p90"].to_numpy(),
        color=COLORS["light_blue"],
        alpha=0.85,
        label="10th–90th percentile",
    )
    ax.fill_between(
        x,
        yearly["p25"].to_numpy(),
        yearly["p75"].to_numpy(),
        color=COLORS["blue"],
        alpha=0.15,
        label="25th–75th percentile",
    )
    ax.plot(
        x,
        yearly["median"],
        color=COLORS["blue"],
        linewidth=3,
        label="Median entity",
        zorder=3,
    )
    ax.axhline(0, color=COLORS["muted"], linewidth=1.1, linestyle=(0, (4, 4)))
    ax.text(
        1961,
        0.25,
        "Parity",
        fontsize=9,
        color=COLORS["muted"],
        va="bottom",
    )
    ax.scatter(
        [1960, 2023],
        [start_median, end_median],
        color=COLORS["blue"],
        edgecolor="white",
        linewidth=1.4,
        s=74,
        zorder=4,
    )
    ax.annotate(
        f"{start_median:.1f}",
        (1960, start_median),
        xytext=(7, -17),
        textcoords="offset points",
        fontsize=9,
        fontweight="bold",
    )
    ax.annotate(
        f"{end_median:.1f}",
        (2023, end_median),
        xytext=(-30, -20),
        textcoords="offset points",
        fontsize=9,
        fontweight="bold",
    )
    ax.annotate(
        f"Below parity: {start_negative}/{len(start)} in 1960\n"
        f"{end_negative}/{len(end)} in 2023",
        xy=(1984, 8.8),
        fontsize=10,
        color=COLORS["ink"],
        bbox=dict(
            boxstyle="round,pad=0.55",
            facecolor="white",
            edgecolor=COLORS["grid"],
        ),
    )
    ax.set_xlim(1960, 2024)
    ax.set_ylim(-0.7, 10.0)
    ax.set_xticks([1960, 1970, 1980, 1990, 2000, 2010, 2020])
    ax.set_xlabel("Year")
    ax.set_ylabel("Female minus male life expectancy (years)")
    ax.yaxis.set_major_locator(MultipleLocator(2))
    ax.legend(
        frameon=False,
        ncol=3,
        loc="upper left",
        bbox_to_anchor=(0, 1.035),
        handlelength=1.8,
        columnspacing=1.6,
    )
    polish_axis(ax)
    footer(
        fig,
        "Source: course World Bank life expectancy file. Each value is female minus male life expectancy; "
        "the ribbon summarizes all reporting entities with both values in a year, including regional aggregates.",
    )
    save(fig, "01-life-expectancy-gap-distribution.png")


def figure_2_life_gap_country_dumbbell():
    gap = life_gap_data()
    chosen = {
        "India",
        "Nigeria",
        "Australia",
        "United States",
        "Japan",
        "China",
        "Brazil",
        "South Africa",
        "Russian Federation",
        "Ukraine",
    }
    focus = gap[
        gap["Country Name"].isin(chosen) & gap["Year"].isin([1960, 2023])
    ].pivot_table(
        index="Country Name",
        columns="Year",
        values="Female advantage (years)",
        aggfunc="first",
    )
    focus = focus.dropna(subset=[1960, 2023]).sort_values(2023, ascending=False)

    fig, ax = setup_figure(
        "Story 1 · alternate design · selected country histories",
        "The shift was uneven: some gaps widened, others narrowed",
        "Paired dots compare the same ten countries at the start and end of the series.",
    )
    y_positions = np.arange(len(focus))
    for y, (_, row) in zip(y_positions, focus.iterrows()):
        change = row[2023] - row[1960]
        connector_color = COLORS["teal"] if change >= 0 else COLORS["coral"]
        ax.plot(
            [row[1960], row[2023]],
            [y, y],
            color=connector_color,
            linewidth=2.6,
            alpha=0.88,
            zorder=2,
        )
        ax.scatter(
            row[1960],
            y,
            s=64,
            facecolor="white",
            edgecolor=COLORS["blue"],
            linewidth=2,
            zorder=3,
        )
        ax.scatter(
            row[2023],
            y,
            s=67,
            facecolor=COLORS["gold"],
            edgecolor="white",
            linewidth=1.2,
            zorder=4,
        )
        ax.annotate(
            f"{row[1960]:.1f}",
            (row[1960], y),
            xytext=(-8, 9),
            textcoords="offset points",
            ha="right",
            fontsize=8.5,
            color=COLORS["muted"],
        )
        ax.annotate(
            f"{row[2023]:.1f}",
            (row[2023], y),
            xytext=(8, -13),
            textcoords="offset points",
            ha="left",
            fontsize=8.5,
            color=COLORS["ink"],
            fontweight="bold",
        )
    ax.set_yticks(y_positions, focus.index)
    ax.invert_yaxis()
    ax.set_xlim(-2.8, 16.1)
    ax.set_xlabel("Female minus male life expectancy (years)")
    ax.set_ylabel("")
    ax.xaxis.set_major_locator(MultipleLocator(2))
    ax.grid(axis="x", color=COLORS["grid"], linewidth=0.8)
    ax.grid(axis="y", visible=False)
    fig.legend(
        handles=[
            Line2D(
                [0], [0], marker="o", color="none", markerfacecolor="white",
                markeredgecolor=COLORS["blue"], markeredgewidth=1.8,
                markersize=8, label="1960",
            ),
            Line2D(
                [0], [0], marker="o", color="none", markerfacecolor=COLORS["gold"],
                markeredgecolor="white", markersize=8, label="2023",
            ),
            Line2D([0], [0], color=COLORS["teal"], linewidth=2.5, label="Gap widened"),
            Line2D([0], [0], color=COLORS["coral"], linewidth=2.5, label="Gap narrowed"),
        ],
        frameon=False,
        ncol=4,
        loc="upper center",
        bbox_to_anchor=(0.54, 0.79),
        columnspacing=1.5,
    )
    polish_axis(ax)
    footer(
        fig,
        "Source: course World Bank life expectancy file. Countries were deliberately selected to show contrasting "
        "changes; this is an illustrative set, not a random or representative sample.",
    )
    save(fig, "02-life-expectancy-gap-country-comparison.png")


BA = "Percent of adults with a bachelor's degree or higher, 2019-23"
INCOME = "Median Household Income 2023"
RUCC = "2023 Rural-urban Continuum Code"


def census_complete_cases():
    census = load_census()
    census = numeric(census, [BA, INCOME, RUCC])
    census["Place type"] = np.where(
        census[RUCC].between(1, 3),
        "Metro (RUCC 1–3)",
        "Nonmetro (RUCC 4–9)",
    )
    return census.dropna(subset=[BA, INCOME, RUCC]).copy()


def figure_3_census_scatter():
    census = census_complete_cases()
    colors = {
        "Metro (RUCC 1–3)": COLORS["blue"],
        "Nonmetro (RUCC 4–9)": COLORS["gold"],
    }
    fig, ax = setup_figure(
        "Story 2 · census · county-level relationship",
        "Counties with more college graduates tend to have higher incomes",
        "The positive association appears in metro and nonmetro counties, with higher metro medians overall.",
    )
    stats = {}
    for place in ["Nonmetro (RUCC 4–9)", "Metro (RUCC 1–3)"]:
        part = census[census["Place type"] == place]
        r = part[BA].corr(part[INCOME])
        stats[place] = (len(part), r)
        ax.scatter(
            part[BA],
            part[INCOME],
            s=15,
            alpha=0.28,
            color=colors[place],
            edgecolor="none",
            rasterized=True,
        )
        slope, intercept = np.polyfit(part[BA].to_numpy(), part[INCOME].to_numpy(), 1)
        xs = np.linspace(part[BA].min(), part[BA].max(), 80)
        ax.plot(
            xs,
            slope * xs + intercept,
            color=colors[place],
            linewidth=2.8,
            zorder=3,
        )
    handles = []
    for place in ["Metro (RUCC 1–3)", "Nonmetro (RUCC 4–9)"]:
        n, r = stats[place]
        handles.append(
            Line2D(
                [0], [0], color=colors[place], linewidth=2.8,
                label=f"{place}  ·  n={n:,}, r={r:.2f}",
            )
        )
    ax.legend(handles=handles, frameon=False, loc="upper left")
    ax.set_xlim(-1, 80)
    ax.set_ylim(20_000, 180_000)
    ax.set_xlabel("Adults with a bachelor's degree or higher (%)")
    ax.set_ylabel("Median household income (2023 dollars)")
    ax.xaxis.set_major_locator(MultipleLocator(10))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"${value / 1000:.0f}k"))
    polish_axis(ax)
    footer(
        fig,
        f"Source: course county Census file; {len(census):,} complete county or county-equivalent records. "
        "Each dot is one county. Lines are simple within-group linear fits; correlations describe association, not cause.",
    )
    save(fig, "03-census-education-income-scatter.png")


def figure_4_census_binned_comparison():
    census = census_complete_cases()
    education_bins = [-0.01, 15, 20, 25, 35, 100]
    education_labels = ["<15%", "15–<20%", "20–<25%", "25–<35%", "35%+"]
    census["Education band"] = pd.cut(
        census[BA],
        bins=education_bins,
        labels=education_labels,
        right=False,
        include_lowest=True,
    )
    colors = {
        "Metro (RUCC 1–3)": COLORS["blue"],
        "Nonmetro (RUCC 4–9)": COLORS["gold"],
    }
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 7.2), sharey=True)
    fig.subplots_adjust(left=0.105, right=0.965, top=0.73, bottom=0.2, wspace=0.16)
    fig.text(
        0.105, 0.95, "STORY 2 · ALTERNATE DESIGN · DISTRIBUTION SUMMARY",
        fontsize=9, fontweight="bold", color=COLORS["teal"], va="top",
    )
    fig.text(
        0.105, 0.908, "The income gradient remains within both place types",
        fontsize=20, fontweight="bold", color=COLORS["ink"], va="top",
    )
    fig.text(
        0.105, 0.855,
        "County groups with higher adult bachelor's attainment also have higher median incomes; "
        "the middle half of counties is shown.",
        fontsize=11, color=COLORS["muted"], va="top",
    )
    summary_labels = ["Metro (RUCC 1–3)", "Nonmetro (RUCC 4–9)"]
    for ax, place in zip(axes, summary_labels):
        part = census[census["Place type"] == place]
        summary = (
            part.groupby("Education band", observed=False)[INCOME]
            .agg(
                median="median",
                q25=lambda values: values.quantile(0.25),
                q75=lambda values: values.quantile(0.75),
                n="count",
            )
            .reindex(education_labels)
        )
        x = np.arange(len(education_labels))
        y = summary["median"].to_numpy(dtype=float)
        low = summary["q25"].to_numpy(dtype=float)
        high = summary["q75"].to_numpy(dtype=float)
        ax.fill_between(
            x, low, high, color=colors[place], alpha=0.16, linewidth=0,
        )
        ax.plot(x, y, color=colors[place], linewidth=2.6, zorder=2)
        ax.scatter(
            x, y, color=colors[place], edgecolor="white",
            linewidth=1.2, s=72, zorder=3,
        )
        for xi, value in zip(x, y):
            ax.annotate(
                f"${value / 1000:.0f}k",
                (xi, value),
                xytext=(0, 9),
                textcoords="offset points",
                ha="center",
                fontsize=8.5,
                fontweight="bold",
                color=COLORS["ink"],
            )
        ax.set_title(place, loc="left", fontsize=12, fontweight="bold", pad=14)
        ax.set_xticks(x, education_labels)
        ax.set_xlabel("Adults with bachelor's degree or higher")
        ax.set_ylim(30_000, 150_000)
        ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"${value / 1000:.0f}k"))
        ax.grid(axis="y", color=COLORS["grid"], linewidth=0.8)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color(COLORS["grid"])
        ax.spines["bottom"].set_color(COLORS["grid"])
        ax.tick_params(length=0, pad=7)
    axes[0].set_ylabel("Median household income (2023 dollars)")
    fig.text(
        0.105, 0.12,
        "Dots = median county income in each fixed attainment band  ·  Shading = 25th–75th percentile "
        "across counties  ·  Each panel uses the same income scale",
        fontsize=8.5, color=COLORS["muted"], va="bottom",
    )
    footer(
        fig,
        "Source: course county Census file; complete cases only. This summary bins counties by adult bachelor's "
        "attainment to make the pattern and spread easier to compare; county records are not population-weighted.",
    )
    save(fig, "04-census-education-income-binned.png")


def figure_5_migration_components():
    census = load_census()
    census = numeric(census, ["Natural Change Rate 2023", "Net Migration Rate 2023", RUCC])
    census["Place type"] = np.where(
        census[RUCC].between(1, 3),
        "Metro (RUCC 1–3)",
        "Nonmetro (RUCC 4–9)",
    )
    data = census.dropna(
        subset=["Natural Change Rate 2023", "Net Migration Rate 2023", RUCC]
    ).copy()
    xcol = "Natural Change Rate 2023"
    ycol = "Net Migration Rate 2023"
    displayed = data[data[xcol].abs().le(40) & data[ycol].abs().le(40)]
    outside = len(data) - len(displayed)
    colors = {
        "Metro (RUCC 1–3)": COLORS["blue"],
        "Nonmetro (RUCC 4–9)": COLORS["gold"],
    }

    nonmetro = data[(data["Place type"] == "Nonmetro (RUCC 4–9)") & (data[xcol] < 0)]
    offsetting = int((nonmetro[ycol] > 0).sum())
    fig, ax = setup_figure(
        "Story 3 · census · population change components",
        "Most counties with natural decline still had net in-migration",
        (
            f"Among nonmetro counties with more deaths than births, "
            f"{offsetting:,} of {len(nonmetro):,} still had net in-migration in 2023."
        ),
    )
    # Above this diagonal, the two component rates sum to positive change.
    ax.fill_between(
        [-40, 40],
        [40, -40],
        [40, 40],
        color=COLORS["light_teal"],
        alpha=0.55,
        zorder=0,
    )
    ax.fill_between(
        [-40, 40],
        [-40, -40],
        [40, -40],
        color=COLORS["light_coral"],
        alpha=0.35,
        zorder=0,
    )
    for place in ["Nonmetro (RUCC 4–9)", "Metro (RUCC 1–3)"]:
        part = displayed[displayed["Place type"] == place]
        ax.scatter(
            part[xcol],
            part[ycol],
            s=19,
            alpha=0.42,
            color=colors[place],
            edgecolor="none",
            rasterized=True,
            label=f"{place}  ·  n={len(data[data['Place type'] == place]):,}",
            zorder=2,
        )
    ax.plot(
        [-40, 40],
        [40, -40],
        color=COLORS["ink"],
        linewidth=1.5,
        linestyle=(0, (5, 4)),
        zorder=3,
    )
    ax.axhline(0, color=COLORS["muted"], linewidth=0.9, alpha=0.7, zorder=1)
    ax.axvline(0, color=COLORS["muted"], linewidth=0.9, alpha=0.7, zorder=1)
    ax.text(
        -37,
        36,
        "Natural decline\nbut migration gain",
        fontsize=9,
        color=COLORS["ink"],
        va="top",
        bbox=dict(boxstyle="round,pad=0.35", facecolor="white", alpha=0.88, edgecolor="none"),
    )
    ax.text(
        37,
        -34,
        "Natural increase\nbut migration loss",
        fontsize=9,
        color=COLORS["ink"],
        ha="right",
        va="bottom",
        bbox=dict(boxstyle="round,pad=0.35", facecolor="white", alpha=0.88, edgecolor="none"),
    )
    ax.set_xlim(-40, 40)
    ax.set_ylim(-40, 40)
    ax.set_aspect("equal", adjustable="box")
    ax.xaxis.set_major_locator(MultipleLocator(20))
    ax.yaxis.set_major_locator(MultipleLocator(20))
    ax.set_xlabel("Natural change rate  ·  deaths versus births (per 1,000)")
    ax.set_ylabel("Net migration rate  ·  arrivals versus departures (per 1,000)")
    fig.legend(
        frameon=False,
        loc="upper center",
        bbox_to_anchor=(0.56, 0.79),
        ncol=2,
        columnspacing=1.5,
    )
    polish_axis(ax)
    ax.grid(axis="x", color=COLORS["grid"], linewidth=0.8)
    footer(
        fig,
        "Source: course county Census file, 2023 rate fields. Dashed line marks zero combined change: "
        f"points above it have positive combined component rates. Axes are clipped for readability; "
        f"{outside} counties with a rate outside the ±40 window are omitted from the point field.",
    )
    save(fig, "05-census-migration-natural-change.png")


def figure_6_unemployment_rural_metro():
    census = load_census()
    years = list(range(2000, 2024))
    unemployment_columns = [f"Unemployment rate {year}" for year in years]
    census = numeric(census, [RUCC, *unemployment_columns])
    census["Place type"] = np.where(
        census[RUCC].between(1, 3),
        "Metro (RUCC 1–3)",
        "Nonmetro (RUCC 4–9)",
    )
    long = census.melt(
        id_vars=["Place type"],
        value_vars=unemployment_columns,
        var_name="Measure",
        value_name="Unemployment rate",
    )
    long["Year"] = long["Measure"].str.extract(r"(\d{4})").astype(int)
    stats = (
        long.dropna(subset=["Unemployment rate"])
        .groupby(["Place type", "Year"])["Unemployment rate"]
        .agg(
            median="median",
            q25=lambda values: values.quantile(0.25),
            q75=lambda values: values.quantile(0.75),
        )
        .reset_index()
    )
    colors = {
        "Metro (RUCC 1–3)": COLORS["blue"],
        "Nonmetro (RUCC 4–9)": COLORS["gold"],
    }
    fig, ax = setup_figure(
        "Story 4 · census · county unemployment over time",
        "The metro median overtook the rural median in the 2020 spike",
        "Median county rates were usually higher outside metro areas; in 2020, the metro median rose above them.",
    )
    for place in ["Nonmetro (RUCC 4–9)", "Metro (RUCC 1–3)"]:
        part = stats[stats["Place type"] == place].sort_values("Year")
        ax.fill_between(
            part["Year"],
            part["q25"],
            part["q75"],
            color=colors[place],
            alpha=0.12,
            linewidth=0,
        )
        ax.plot(
            part["Year"],
            part["median"],
            color=colors[place],
            linewidth=2.8,
            marker="o",
            markersize=4.3,
            label=place,
        )
    ax.axvspan(2019.6, 2020.4, color=COLORS["light_coral"], alpha=0.75, zorder=0)
    med = stats.pivot(index="Year", columns="Place type", values="median")
    metro = "Metro (RUCC 1–3)"
    nonmetro = "Nonmetro (RUCC 4–9)"
    ax.annotate(
        "2020\nMetro 6.8%  ·  Nonmetro 6.3%",
        xy=(2020, med.loc[2020, metro]),
        xytext=(2021.3, 10.8),
        arrowprops=dict(arrowstyle="->", color=COLORS["muted"], linewidth=1),
        fontsize=9.5,
        color=COLORS["ink"],
        bbox=dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor=COLORS["grid"]),
    )
    ax.annotate(
        "2023: 3.4% vs 3.5%",
        xy=(2023, med.loc[2023, nonmetro]),
        xytext=(2019.5, 2.3),
        arrowprops=dict(arrowstyle="->", color=COLORS["muted"], linewidth=1),
        fontsize=9,
        color=COLORS["ink"],
        bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor=COLORS["grid"]),
    )
    ax.set_xlim(2000, 2023.8)
    ax.set_ylim(0, 13)
    ax.set_xticks([2000, 2005, 2010, 2015, 2020])
    ax.set_xlabel("Year")
    ax.set_ylabel("County unemployment rate (%)")
    ax.yaxis.set_major_locator(MultipleLocator(2))
    ax.legend(frameon=False, loc="upper right", ncol=2)
    polish_axis(ax)
    footer(
        fig,
        "Source: course county Census file. Lines are the median county unemployment rate by the 2023 rural–urban "
        "classification; shading spans the 25th–75th percentile across counties. County rates are not population-weighted.",
    )
    save(fig, "06-census-unemployment-gap.png")


def main():
    figure_1_life_gap_distribution()
    figure_2_life_gap_country_dumbbell()
    figure_3_census_scatter()
    figure_4_census_binned_comparison()
    figure_5_migration_components()
    figure_6_unemployment_rural_metro()
    print(f"Wrote six figures to {FIGURES}")


if __name__ == "__main__":
    main()
