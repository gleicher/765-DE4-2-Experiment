"""Generate the six static figures for Design Exercise 4-2."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.ticker import MultipleLocator, PercentFormatter


HERE = Path(__file__).resolve().parents[1]
DATA = HERE / "data"
OUT = HERE / "answers" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

INK = "#172B3A"
MUTED = "#526577"
GRID = "#DCE4EA"
PAPER = "#FFFFFF"
TEAL = "#167D8D"
BLUE = "#4677A8"
ORANGE = "#D06C3B"
GOLD = "#D6A63B"
PURPLE = "#8064A2"
GREEN = "#44866C"
PALE = "#F3F6F8"
GREY = "#9AA9B5"

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "axes.labelcolor": INK,
        "text.color": INK,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "axes.edgecolor": GRID,
        "axes.linewidth": 0.8,
        "savefig.facecolor": PAPER,
        "figure.facecolor": PAPER,
    }
)


def frame(fig, number, title, subtitle, source, note):
    fig.text(0.075, 0.94, f"DESIGN EXERCISE 4-2  /  VISUALIZATION {number}", color=TEAL,
             fontsize=10, fontweight="bold", va="top")
    fig.text(0.075, 0.895, title, color=INK, fontsize=23, fontweight="bold", va="top")
    fig.text(0.075, 0.845, subtitle, color=MUTED, fontsize=12, va="top")
    fig.text(0.075, 0.078, note, color=MUTED, fontsize=9.5, va="bottom", wrap=True)
    fig.text(0.075, 0.045, source, color=MUTED, fontsize=8.5, va="bottom")


def clean_axis(ax):
    ax.set_facecolor(PAPER)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(GRID)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(length=0, pad=7)


def save(fig, name):
    fig.savefig(OUT / name, dpi=220, bbox_inches="tight")
    plt.close(fig)


def fig1_covid_trajectories():
    owid = pd.read_csv(DATA / "life-expectancy-owid" / "life-expectancy-owid.csv")
    entities = ["World", "Africa", "Americas", "Asia", "Europe", "Oceania"]
    colors = {
        "World": INK,
        "Africa": ORANGE,
        "Americas": PURPLE,
        "Asia": TEAL,
        "Europe": BLUE,
        "Oceania": GREEN,
    }
    df = owid[owid["Entity"].isin(entities) & owid["Year"].between(2015, 2023)].copy()
    pivot = df.pivot(index="Year", columns="Entity", values="Period life expectancy at birth")

    fig, ax = plt.subplots(figsize=(12, 7.4))
    fig.subplots_adjust(left=0.09, right=0.83, top=0.79, bottom=0.19)
    frame(
        fig,
        "1A",
        "The 2021 life-expectancy dip was deepest in the Americas",
        "Most regions reached a low around 2021; by 2023, all six series had moved above their 2019 level.",
        "Data: Our World in Data, long-run period life expectancy (downloaded September 2025).",
        "The shaded band marks 2019–2021. Life expectancy is a period estimate, not a forecast of an individual’s lifespan. "
        "The six entities are the world total and continental aggregates.",
    )
    clean_axis(ax)
    ax.axvspan(2019, 2021, color=ORANGE, alpha=0.08, zorder=0)
    ax.axvline(2019, color=ORANGE, linewidth=1, linestyle=(0, (3, 3)), alpha=0.75)
    ax.axvline(2021, color=ORANGE, linewidth=1, linestyle=(0, (3, 3)), alpha=0.75)
    for entity in entities:
        y = pivot[entity]
        width = 3.2 if entity == "World" else 2.2
        style = (0, (5, 3)) if entity == "World" else "solid"
        ax.plot(y.index, y.values, color=colors[entity], linewidth=width, linestyle=style,
                marker="o", markersize=4.4 if entity == "World" else 3.5, zorder=3)
    ax.set_xlim(2015, 2024.65)
    ax.set_ylim(49, 87)
    ax.set_xticks([2015, 2017, 2019, 2021, 2023])
    ax.set_ylabel("Period life expectancy at birth (years)", labelpad=10)
    ax.set_xlabel("Year", labelpad=8)
    ax.yaxis.set_major_locator(MultipleLocator(5))
    offsets = {
        "Oceania": (8, 10),
        "Europe": (8, -8),
        "Americas": (8, 0),
        "Asia": (8, -1),
        "World": (8, -10),
        "Africa": (8, 0),
    }
    for entity in entities:
        v = pivot.loc[2023, entity]
        dx, dy = offsets[entity]
        ax.annotate(
            f"{entity}  {v:.1f}",
            (2023, v),
            xytext=(dx, dy),
            textcoords="offset points",
            color=colors[entity],
            fontsize=10,
            fontweight="bold" if entity == "World" else "medium",
            va="center",
            annotation_clip=False,
        )
    ax.text(2020, 85.7, "COVID-19 period", color=ORANGE, fontsize=9, ha="center")
    save(fig, "01-life-expectancy-pandemic-line.png")


def fig2_covid_interval_changes():
    owid = pd.read_csv(DATA / "life-expectancy-owid" / "life-expectancy-owid.csv")
    entities = ["World", "Africa", "Americas", "Asia", "Europe", "Oceania"]
    df = owid[owid["Entity"].isin(entities) & owid["Year"].isin([2019, 2021, 2023])]
    pivot = df.pivot(index="Entity", columns="Year", values="Period life expectancy at birth")
    changes = pd.DataFrame(
        {
            "2019 to 2021": pivot[2021] - pivot[2019],
            "2021 to 2023": pivot[2023] - pivot[2021],
        }
    )
    order = changes["2019 to 2021"].sort_values().index.tolist()
    y = np.arange(len(order))

    fig, ax = plt.subplots(figsize=(12, 7.4))
    fig.subplots_adjust(left=0.20, right=0.94, top=0.79, bottom=0.20)
    frame(
        fig,
        "1B",
        "The largest fall was followed by the strongest rebound",
        "Change in life expectancy (years) across the pandemic low, measured over two adjacent two-year periods.",
        "Data: Our World in Data, long-run period life expectancy (downloaded September 2025).",
        "Bars show endpoint differences, not annual rates. The world and continental aggregates are not independent populations.",
    )
    clean_axis(ax)
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.grid(axis="y", visible=False)
    ax.axvline(0, color=MUTED, linewidth=1)
    for i, entity in enumerate(order):
        fall = changes.loc[entity, "2019 to 2021"]
        rebound = changes.loc[entity, "2021 to 2023"]
        ax.barh(i + 0.16, fall, height=0.25, color=PURPLE, alpha=0.92)
        ax.barh(i - 0.16, rebound, height=0.25, color=TEAL, alpha=0.95)
        ax.text(fall - 0.08, i + 0.16, f"{fall:.1f}", ha="right", va="center",
                color=INK, fontsize=9, fontweight="bold")
        ax.text(rebound + 0.08, i - 0.16, f"+{rebound:.1f}", ha="left", va="center",
                color=INK, fontsize=9, fontweight="bold")
    ax.set_yticks(y, order)
    ax.set_xlim(-3.7, 4.25)
    ax.set_xlabel("Difference between endpoint years (years)", labelpad=9)
    ax.set_ylabel("")
    ax.xaxis.set_major_locator(MultipleLocator(1))
    fig.legend(
        handles=[
            Line2D([0], [0], color=PURPLE, lw=8, label="2019 → 2021"),
            Line2D([0], [0], color=TEAL, lw=8, label="2021 → 2023"),
        ],
        frameon=False,
        loc="upper right",
        ncol=2,
        bbox_to_anchor=(0.94, 0.805),
    )
    save(fig, "02-life-expectancy-pandemic-intervals.png")


def census_counties():
    c = pd.read_csv(DATA / "full_census_dataset.csv", encoding="cp1252", low_memory=False)
    numeric = ["Natural Change Rate 2023", "Net Migration Rate 2023", "2023 Rural-urban Continuum Code"]
    for col in numeric:
        c[col] = pd.to_numeric(c[col], errors="coerce")
    c = c[
        c["Area name"].str.contains("County", case=False, na=False)
        & c["2023 Rural-urban Continuum Code"].between(1, 9)
    ].dropna(subset=["Natural Change Rate 2023", "Net Migration Rate 2023"]).copy()
    c["Place type"] = np.where(c["2023 Rural-urban Continuum Code"] <= 3, "Metro", "Nonmetro")
    c["Natural Change Rate 2023"] = c["Natural Change Rate 2023"].astype(float)
    c["Net Migration Rate 2023"] = c["Net Migration Rate 2023"].astype(float)
    c["Combined balance"] = c["Natural Change Rate 2023"] + c["Net Migration Rate 2023"]
    c["Pattern"] = np.select(
        [
            (c["Natural Change Rate 2023"] < 0) & (c["Net Migration Rate 2023"] <= 0),
            (c["Natural Change Rate 2023"] < 0)
            & (c["Net Migration Rate 2023"] > 0)
            & (c["Combined balance"] <= 0),
            (c["Natural Change Rate 2023"] < 0)
            & (c["Net Migration Rate 2023"] > 0)
            & (c["Combined balance"] > 0),
            (c["Natural Change Rate 2023"] >= 0) & (c["Net Migration Rate 2023"] < 0),
        ],
        [
            "Natural decrease + out-migration",
            "Migration partly offsets natural decrease",
            "Migration more than offsets natural decrease",
            "Natural increase + out-migration",
        ],
        default="Both rates positive",
    )
    return c


def fig3_migration_scatter():
    c = census_counties()
    colors = {
        "Migration more than offsets natural decrease": TEAL,
        "Migration partly offsets natural decrease": ORANGE,
        "Natural decrease + out-migration": "#82909B",
        "Natural increase + out-migration": PURPLE,
        "Both rates positive": BLUE,
    }
    fig, axs = plt.subplots(1, 2, figsize=(13, 7.6), sharex=True, sharey=True)
    fig.subplots_adjust(left=0.09, right=0.97, top=0.78, bottom=0.31, wspace=0.15)
    metro_neg = c[(c["Place type"] == "Metro") & (c["Natural Change Rate 2023"] < 0)]
    nonmetro_neg = c[(c["Place type"] == "Nonmetro") & (c["Natural Change Rate 2023"] < 0)]
    metro_positive = (metro_neg["Combined balance"] > 0).mean() * 100
    nonmetro_positive = (nonmetro_neg["Combined balance"] > 0).mean() * 100
    frame(
        fig,
        "2A",
        "Migration often reversed natural decrease in metro counties",
        f"Among counties with a negative natural-change rate, combined natural-change + net-migration rates were positive in "
        f"{metro_positive:.0f}% of metro counties and {nonmetro_positive:.0f}% of nonmetro counties.",
        "Data: USDA county-level dataset supplied for CS 765; rates shown as reported for 2023.",
        "Each point is a county or county equivalent. Metro = 2023 Rural-urban Continuum Codes 1–3; nonmetro = 4–9. "
        "The diagonal marks a zero combined balance; 5 extreme observations fall beyond the displayed axes.",
    )
    for ax, place in zip(axs, ["Metro", "Nonmetro"]):
        clean_axis(ax)
        ax.grid(axis="x", color=GRID, linewidth=0.8)
        ax.set_xlim(-25, 20)
        ax.set_ylim(-60, 80)
        ax.axvline(0, color=MUTED, linewidth=1)
        ax.axhline(0, color=MUTED, linewidth=1)
        xs = np.linspace(-25, 20, 250)
        ax.plot(xs, -xs, color=INK, linestyle=(0, (4, 3)), linewidth=1.5, alpha=0.8, zorder=2)
        part = c[c["Place type"] == place].copy()
        # Plot low-salience counties first and focus the two natural-decrease/in-migration outcomes.
        part["priority"] = part["Pattern"].map(
            {
                "Natural decrease + out-migration": 0,
                "Natural increase + out-migration": 0,
                "Both rates positive": 0,
                "Migration partly offsets natural decrease": 1,
                "Migration more than offsets natural decrease": 2,
            }
        )
        for pattern, z in [
            ("Natural decrease + out-migration", 1),
            ("Natural increase + out-migration", 1),
            ("Both rates positive", 1),
            ("Migration partly offsets natural decrease", 3),
            ("Migration more than offsets natural decrease", 4),
        ]:
            sub = part[part["Pattern"] == pattern]
            ax.scatter(
                sub["Natural Change Rate 2023"],
                sub["Net Migration Rate 2023"],
                s=15 if z < 3 else 19,
                color=colors[pattern],
                alpha=0.42 if z < 3 else 0.78,
                edgecolors="none",
                zorder=z,
                label=pattern,
            )
        ax.text(0.03, 1.03, f"{place}  ·  n = {len(part):,}", transform=ax.transAxes,
                color=INK, fontsize=13, fontweight="bold", va="bottom")
        ax.set_xlabel("Natural-change rate (2023)", labelpad=8)
    axs[0].set_ylabel("Net-migration rate (2023)", labelpad=10)
    axs[0].text(-23, 67, "Migration exceeds\nnatural loss", color=TEAL, fontsize=9, va="top")
    axs[0].text(-23, -49, "Combined rate\nremains negative", color=MUTED, fontsize=9, va="bottom")
    axs[1].text(19, 21, "combined balance = 0", color=INK, fontsize=8.5, rotation=-48,
                ha="right", va="center")
    fig.legend(
        handles=[
            Line2D([0], [0], marker="o", lw=0, markersize=7, color=colors[k], label=k)
            for k in [
                "Migration more than offsets natural decrease",
                "Migration partly offsets natural decrease",
                "Natural decrease + out-migration",
                "Natural increase + out-migration",
                "Both rates positive",
            ]
        ],
        frameon=False,
        loc="lower center",
        bbox_to_anchor=(0.53, 0.12),
        ncol=3,
        fontsize=9,
        columnspacing=1.3,
        handletextpad=0.45,
    )
    save(fig, "03-county-natural-change-migration-scatter.png")


def fig4_migration_patterns():
    c = census_counties()
    patterns = [
        "Natural decrease + out-migration",
        "Migration partly offsets natural decrease",
        "Migration more than offsets natural decrease",
        "Natural increase + out-migration",
        "Both rates positive",
    ]
    colors = [GREY, ORANGE, TEAL, PURPLE, BLUE]
    counts = c.groupby("Place type").size()
    shares = (
        pd.crosstab(c["Place type"], c["Pattern"], normalize="index")
        .reindex(index=["Metro", "Nonmetro"], columns=patterns, fill_value=0)
    )
    fig, ax = plt.subplots(figsize=(12, 7.4))
    fig.subplots_adjust(left=0.19, right=0.96, top=0.79, bottom=0.31)
    frame(
        fig,
        "2B",
        "Natural decrease is common outside metros; migration often changes the balance",
        "Among counties with natural decrease, combined rates turned positive in 69% of metro vs 49% of nonmetro counties.",
        "Data: USDA county-level dataset supplied for CS 765; rates shown as reported for 2023.",
        "Each county contributes equally to its bar. “More than offsets” means natural-change rate + net-migration rate > 0. "
        "Metro/nonmetro groups use 2023 Rural-urban Continuum Codes (1–3 / 4–9).",
    )
    clean_axis(ax)
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    left = np.zeros(2)
    for pattern, color in zip(patterns, colors):
        vals = shares[pattern].values
        ax.barh([1, 0], vals, left=left, height=0.5, color=color, edgecolor=PAPER, linewidth=1)
        for j, val in enumerate(vals):
            if val >= 0.085:
                label = f"{val:.0%}"
                ax.text(left[j] + val / 2, [1, 0][j], label, ha="center", va="center",
                        color=PAPER if color in [TEAL, PURPLE, BLUE, GREY] else INK,
                        fontsize=10, fontweight="bold")
        left += vals
    ax.set_yticks([1, 0], [f"Metro   (n={counts['Metro']:,})", f"Nonmetro   (n={counts['Nonmetro']:,})"])
    ax.set_xlim(0, 1)
    ax.xaxis.set_major_formatter(PercentFormatter(1))
    ax.set_xlabel("Share of county equivalents", labelpad=8)
    fig.legend(
        handles=[plt.Rectangle((0, 0), 1, 1, color=color, label=pattern) for pattern, color in zip(patterns, colors)],
        frameon=False,
        loc="lower center",
        bbox_to_anchor=(0.57, 0.11),
        ncol=2,
        fontsize=9.5,
        columnspacing=1.6,
        handletextpad=0.55,
    )
    save(fig, "04-county-migration-patterns-stacked.png")


def fig5_education_trend():
    c = pd.read_csv(DATA / "full_census_dataset.csv", encoding="cp1252", low_memory=False)
    c["2023 Rural-urban Continuum Code"] = pd.to_numeric(c["2023 Rural-urban Continuum Code"], errors="coerce")
    c = c[
        c["Area name"].str.contains("County", case=False, na=False)
        & c["2023 Rural-urban Continuum Code"].between(1, 9)
    ].copy()
    c["Place type"] = np.where(c["2023 Rural-urban Continuum Code"] <= 3, "Metro", "Nonmetro")
    periods = ["1990", "2000", "2008-12", "2019-23"]
    values = {}
    for period in periods:
        col = f"Percent of adults with a bachelor's degree or higher, {period}"
        c[col] = pd.to_numeric(c[col], errors="coerce")
        values[period] = c.groupby("Place type")[col].agg(
            median="median",
            q25=lambda x: x.quantile(0.25),
            q75=lambda x: x.quantile(0.75),
        )
    x = np.arange(len(periods))
    fig, ax = plt.subplots(figsize=(12, 7.4))
    fig.subplots_adjust(left=0.11, right=0.94, top=0.79, bottom=0.21)
    gap_start = values["1990"].loc["Metro", "median"] - values["1990"].loc["Nonmetro", "median"]
    gap_end = values["2019-23"].loc["Metro", "median"] - values["2019-23"].loc["Nonmetro", "median"]
    frame(
        fig,
        "3",
        "College attainment rose everywhere, while the county gap widened",
        f"Median county share of adults with a bachelor’s degree or higher: metro–nonmetro gap grew "
        f"from {gap_start:.1f} to {gap_end:.1f} percentage points.",
        "Data: USDA county-level dataset supplied for CS 765; education estimates for 1990, 2000, 2008–12, and 2019–23.",
        "Lines show unweighted county medians; bands show the middle half of counties (25th–75th percentiles). "
        "Metro/nonmetro status is assigned from 2023 Rural-urban Continuum Codes and applied to all four periods.",
    )
    clean_axis(ax)
    ax.grid(axis="x", visible=False)
    for place, color in [("Metro", BLUE), ("Nonmetro", ORANGE)]:
        med = [values[p].loc[place, "median"] for p in periods]
        lo = [values[p].loc[place, "q25"] for p in periods]
        hi = [values[p].loc[place, "q75"] for p in periods]
        ax.fill_between(x, lo, hi, color=color, alpha=0.13, linewidth=0)
        ax.plot(x, med, color=color, linewidth=3, marker="o", markersize=8, label=place, zorder=4)
        for xi, yi in zip(x, med):
            ax.text(xi, yi + (1.25 if place == "Metro" else -2.3), f"{yi:.1f}%",
                    ha="center", va="center", color=color, fontsize=9, fontweight="bold")
    ax.annotate(
        f"Gap: {gap_end:.1f} pp",
        xy=(x[-1], values["2019-23"].loc["Metro", "median"] - 3.9),
        xytext=(x[-1] + 0.28, 23.5),
        arrowprops={"arrowstyle": "-", "color": MUTED, "linewidth": 1},
        color=INK,
        fontsize=10,
        fontweight="bold",
        ha="left",
    )
    ax.set_xticks(x, periods)
    ax.set_xlim(-0.28, 3.78)
    ax.set_ylim(4, 38)
    ax.set_ylabel("Adults with bachelor’s degree or higher (%)", labelpad=9)
    ax.set_xlabel("Education estimate period", labelpad=8)
    ax.yaxis.set_major_formatter(PercentFormatter(100))
    ax.legend(frameon=False, loc="upper left", ncol=2)
    save(fig, "05-county-education-gap.png")


def fig6_gender_gap():
    wb = pd.read_csv(DATA / "lifespan_dataset_1960.csv")
    countries = ["Russian Federation", "Japan", "China", "United States"]
    df = wb[
        wb["Country Name"].isin(countries)
        & wb["Sex"].isin(["Male", "Female"])
        & wb["Year"].isin([1960, 2023])
    ]
    df["Year/Sex"] = df["Year"].astype(str) + " " + df["Sex"]
    pivot = df.pivot(index="Country Name", columns="Year/Sex", values="Life Expectancy (years)")
    pivot["gap_1960"] = pivot["1960 Female"] - pivot["1960 Male"]
    pivot["gap_2023"] = pivot["2023 Female"] - pivot["2023 Male"]
    pivot = pivot.sort_values("gap_2023", ascending=True)
    fig, ax = plt.subplots(figsize=(12, 7.4))
    fig.subplots_adjust(left=0.22, right=0.94, top=0.79, bottom=0.21)
    frame(
        fig,
        "4",
        "The female life-expectancy lead changed in opposite directions",
        "Female minus male period life expectancy, 1960 and 2023, in four selected countries.",
        "Data: World Bank life-expectancy dataset supplied for CS 765; values for 1960 and 2023.",
        "A positive gap means female life expectancy is higher. The country selection illustrates distinct trajectories; it is not a global ranking.",
    )
    clean_axis(ax)
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.grid(axis="y", visible=False)
    y = np.arange(len(pivot))
    for yi, (country, row) in enumerate(pivot.iterrows()):
        a, b = row["gap_1960"], row["gap_2023"]
        ax.plot([a, b], [yi, yi], color=GRID, linewidth=4, solid_capstyle="round", zorder=2)
        ax.scatter(a, yi, s=110, color="#CAD4DC", edgecolor=PAPER, linewidth=1, zorder=3)
        ax.scatter(b, yi, s=130, color=TEAL if b >= a else ORANGE, edgecolor=PAPER, linewidth=1, zorder=4)
        ax.text(a, yi + 0.22, f"{a:.1f}", ha="center", va="bottom", color=MUTED, fontsize=10)
        ax.text(b, yi - 0.20, f"{b:.1f}", ha="center", va="top",
                color=TEAL if b >= a else ORANGE, fontsize=10, fontweight="bold")
    ax.set_yticks(y, pivot.index)
    ax.set_xlim(0, 13)
    ax.set_ylim(-0.6, len(y) - 0.25)
    ax.set_xlabel("Female minus male life expectancy (years)", labelpad=8)
    ax.xaxis.set_major_locator(MultipleLocator(2))
    ax.legend(
        handles=[
            Line2D([0], [0], marker="o", lw=0, markersize=9, color="#CAD4DC", label="1960"),
            Line2D([0], [0], marker="o", lw=0, markersize=9, color=TEAL, label="2023 gap wider"),
            Line2D([0], [0], marker="o", lw=0, markersize=9, color=ORANGE, label="2023 gap narrower"),
        ],
        frameon=False,
        loc="upper center",
        ncol=3,
        bbox_to_anchor=(0.76, 1.0),
    )
    save(fig, "06-gender-life-expectancy-gap.png")


def main():
    fig1_covid_trajectories()
    fig2_covid_interval_changes()
    fig3_migration_scatter()
    fig4_migration_patterns()
    fig5_education_trend()
    fig6_gender_gap()
    print(f"Saved 6 figures to {OUT}")


if __name__ == "__main__":
    main()
