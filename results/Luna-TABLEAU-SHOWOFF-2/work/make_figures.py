"""Generate the six static design-exercise figures from the supplied course data."""
from __future__ import annotations

from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "answers" / "figures"
WORK = ROOT / "work"
OUTPUT.mkdir(parents=True, exist_ok=True)
(WORK / "mplconfig").mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(WORK / "mplconfig"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BLUE = "#4E79A7"
ORANGE = "#E28E2C"
GREEN = "#59A14F"
RED = "#E15759"
PURPLE = "#AF7AA1"
TEAL = "#76B7B2"
DARK = "#303943"
MUTED = "#6B7280"
GRID = "#E6E9ED"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.titlesize": 16,
    "axes.labelsize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white",
})


def style_axis(ax, grid_axis="y"):
    ax.grid(axis=grid_axis, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color("#BCC2C9")
    ax.tick_params(colors="#545B64", length=0, pad=5)
    ax.xaxis.label.set_color(DARK)
    ax.yaxis.label.set_color(DARK)


def finish(fig, ax, title, subtitle, caption, name, bottom=0.23):
    fig.suptitle(title, x=0.10, y=0.965, ha="left", fontsize=17,
                 fontweight="medium", color=DARK)
    fig.text(0.10, 0.916, subtitle, ha="left", va="top", fontsize=9.5,
             color=MUTED)
    fig.text(0.10, 0.035, caption, ha="left", va="bottom", fontsize=8.2,
             color="#59616A", wrap=True)
    fig.subplots_adjust(left=0.12, right=0.97, top=0.85, bottom=bottom)
    fig.savefig(OUTPUT / name, dpi=210, bbox_inches="tight")
    plt.close(fig)


# Course data: World Bank-derived life expectancy by country, sex, and year.
life = pd.read_csv(ROOT / "data" / "lifespan_dataset_1960.csv", index_col=0)
life["Year"] = pd.to_numeric(life["Year"], errors="coerce")
selected = ["Russian Federation", "United States", "Japan", "India", "China", "South Africa"]
colors = {
    "Russian Federation": BLUE,
    "United States": ORANGE,
    "Japan": GREEN,
    "India": RED,
    "China": PURPLE,
    "South Africa": TEAL,
}
sex_wide = (life[life["Country Name"].isin(selected) & life["Sex"].isin(["Female", "Male"])]
            .pivot_table(index=["Country Name", "Year"], columns="Sex",
                         values="Life Expectancy (years)", aggfunc="mean")
            .reset_index())
sex_wide["Gap"] = sex_wide["Female"] - sex_wide["Male"]

# Figure 1: straightforward Tableau-style line chart of a calculated female-minus-male gap.
fig, ax = plt.subplots(figsize=(10.2, 6.2))
for country in selected:
    country_data = sex_wide[sex_wide["Country Name"] == country].sort_values("Year")
    ax.plot(country_data["Year"], country_data["Gap"], color=colors[country],
            linewidth=2.1 if country in ["Russian Federation", "India"] else 1.7,
            label=country)
ax.axhline(0, color="#858B92", linewidth=1, linestyle=(0, (4, 3)))
ax.set_xlim(1960, 2023)
ax.set_ylim(-2.5, 15.2)
ax.set_xticks([1960, 1970, 1980, 1990, 2000, 2010, 2020])
ax.set_xlabel("Year")
ax.set_ylabel("Female minus male life expectancy (years)")
style_axis(ax)
ax.legend(frameon=False, ncol=3, loc="upper left", columnspacing=1.4,
          handlelength=2.2)
finish(fig, ax,
       "The female advantage changes sharply by country",
       "Life expectancy gap across six selected countries, 1960–2023",
       "Positive values mean women’s estimated life expectancy is higher. The six countries were selected to compare contrasting levels and trajectories; they are not a representative sample of the world. Source: course World Bank life-expectancy data.",
       "01_life_expectancy_gap_over_time.png", bottom=0.19)

# Figure 2: sorted bar chart of the same derived gap, using the latest year available in all six series.
latest_year = int(sex_wide.groupby("Country Name")["Year"].max().min())
latest = (sex_wide[sex_wide["Year"] == latest_year]
          [["Country Name", "Female", "Male", "Gap"]]
          .dropna().sort_values("Gap", ascending=True))
fig, ax = plt.subplots(figsize=(9.8, 5.5))
bar_colors = [BLUE if name == "Russian Federation" else "#7F9DBB"
              for name in latest["Country Name"]]
bars = ax.barh(latest["Country Name"], latest["Gap"], color=bar_colors,
               height=0.62)
for bar, value in zip(bars, latest["Gap"]):
    ax.text(value + 0.18, bar.get_y() + bar.get_height()/2, f"{value:.1f} years",
            va="center", ha="left", fontsize=9, color=DARK)
ax.set_xlim(0, max(15, float(latest["Gap"].max()) + 2))
ax.set_xlabel("Female advantage in life expectancy (years)")
ax.set_ylabel("")
style_axis(ax, "x")
ax.grid(axis="y", visible=False)
finish(fig, ax,
       f"Russia has the widest sex gap in {latest_year}",
       f"Female minus male life expectancy at birth • selected countries • {latest_year}",
       "A positive bar is the number of additional years in female life expectancy. This endpoint view makes country ranking easy to compare; Figure 1 shows how each gap arrived here. Source: course World Bank life-expectancy data.",
       "02_life_expectancy_gap_2023.png", bottom=0.20)

# Course census data contains county and county-equivalent rows; status is missing for state/national totals.
census = pd.read_csv(ROOT / "data" / "full_census_dataset.csv", encoding="latin1",
                     dtype={"FIPS Code": "string"})
BA = "Percent of adults with a bachelor's degree or higher, 2019-23"
INCOME = "Median Household Income 2023"
METRO = "Metropolitan Area 2023"
NATURAL = "Natural Change Rate 2023"
MIGRATION = "Net Migration Rate 2023"
for column in [BA, INCOME, NATURAL, MIGRATION]:
    census[column] = pd.to_numeric(census[column], errors="coerce")
county = census[census[METRO].isin([0, 1])].copy()
county["Place type"] = county[METRO].map({1: "Metro", 0: "Nonmetro"})
place_colors = {"Metro": BLUE, "Nonmetro": ORANGE}

# Figure 3: county-level relationship of education to income with ordinary Tableau-like trend lines.
scatter_data = county.dropna(subset=[BA, INCOME]).copy()
fig, ax = plt.subplots(figsize=(10.2, 6.2))
correlations = {}
for place in ["Metro", "Nonmetro"]:
    part = scatter_data[scatter_data["Place type"] == place]
    x = part[BA].to_numpy(float)
    y = part[INCOME].to_numpy(float)
    rho = part[BA].corr(part[INCOME], method="spearman")
    correlations[place] = (rho, len(part))
    ax.scatter(x, y, s=14, alpha=0.30, color=place_colors[place],
               edgecolors="none", label=f"{place} counties  (ρ = {rho:.2f})")
    slope, intercept = np.polyfit(x, y, 1)
    xx = np.linspace(float(np.nanpercentile(x, 1)), float(np.nanpercentile(x, 99)), 100)
    ax.plot(xx, slope*xx + intercept, color=place_colors[place], linewidth=2.0)
ax.set_xlim(0, max(65, float(scatter_data[BA].quantile(.995)) + 3))
ax.set_ylim(0, max(160000, float(scatter_data[INCOME].quantile(.995)) + 10000))
ax.set_xlabel("Adults with a bachelor's degree or higher (2019–23, %)")
ax.set_ylabel("Median household income (2023, $)")
ax.yaxis.set_major_formatter(matplotlib.ticker.StrMethodFormatter("${x:,.0f}"))
style_axis(ax)
ax.legend(frameon=False, loc="upper left")
finish(fig, ax,
       "Higher county education goes with higher income",
       "The positive association is stronger among metro counties",
       "Each mark is a county or county equivalent with both measures available; lines are within-group least-squares trends. Spearman ρ summarizes the rank association (metro .71; nonmetro .55). County medians are compared equally, not weighted by population. The pattern is descriptive, not causal. Source: course USDA county dataset.",
       "03_census_education_income_scatter.png", bottom=0.23)

# Figure 4: summarize the same relationship by pooled attainment quartiles.
quartile_frame = scatter_data[[BA, INCOME, "Place type"]].copy()
quartile_frame["Attainment quartile"] = pd.qcut(
    quartile_frame[BA], q=4, labels=["Q1", "Q2", "Q3", "Q4"], duplicates="drop")
summary = (quartile_frame.groupby(["Place type", "Attainment quartile"], observed=True)
           .agg(BA_median=(BA, "median"), income_median=(INCOME, "median"), n=(INCOME, "size"))
           .reset_index())
fig, ax = plt.subplots(figsize=(10.2, 6.0))
for place in ["Metro", "Nonmetro"]:
    part = summary[summary["Place type"] == place].sort_values("Attainment quartile")
    ax.plot(part["BA_median"], part["income_median"], color=place_colors[place],
            linewidth=2, marker="o", markersize=7, label=place)
    for _, row in part.iterrows():
        ax.annotate(row["Attainment quartile"], (row["BA_median"], row["income_median"]),
                    xytext=(5, 4 if place == "Metro" else -12), textcoords="offset points",
                    color=place_colors[place], fontsize=8, fontweight="medium")
ax.set_xlabel("Median bachelor's attainment within pooled county quartile (%)")
ax.set_ylabel("Median household income within quartile ($)")
ax.yaxis.set_major_formatter(matplotlib.ticker.StrMethodFormatter("${x:,.0f}"))
style_axis(ax)
ax.legend(title="County type", frameon=False, loc="upper left")
finish(fig, ax,
       "The education–income pattern persists in grouped summaries",
       "Each point summarizes counties within one national attainment quartile",
       "Q1–Q4 divide counties by 2019–23 bachelor's attainment, from lowest to highest; x and y show the within-group median of each measure. Metro counties remain higher at each level, while income rises across quartiles in both groups. Grouped medians reduce overlap, but hide county-to-county variation. Source: course USDA county dataset.",
       "04_census_income_by_education_quartile.png", bottom=0.23)

# Figure 5: natural change versus net migration exposes distinct population-change components.
migration_data = county.dropna(subset=[NATURAL, MIGRATION]).copy()
neg_nat_pos_mig = ((migration_data[NATURAL] < 0) & (migration_data[MIGRATION] > 0)).sum()
all_n = len(migration_data)
fig, ax = plt.subplots(figsize=(10.2, 6.5))
for place in ["Metro", "Nonmetro"]:
    part = migration_data[migration_data["Place type"] == place]
    ax.scatter(part[NATURAL], part[MIGRATION], s=15, alpha=0.32,
               color=place_colors[place], edgecolors="none", label=place)
ax.axhline(0, color="#858B92", linewidth=1, linestyle=(0, (4, 3)))
ax.axvline(0, color="#858B92", linewidth=1, linestyle=(0, (4, 3)))
ax.set_xlim(float(migration_data[NATURAL].min()) - 2, float(migration_data[NATURAL].max()) + 2)
ax.set_ylim(float(migration_data[MIGRATION].min()) - 5, float(migration_data[MIGRATION].max()) + 5)
ax.set_xlabel("Natural change rate (2023, as supplied)")
ax.set_ylabel("Net migration rate (2023, as supplied)")
style_axis(ax)
ax.legend(title="County type", frameon=False, loc="upper right")
# Quadrant labels are descriptive and stay clear of the dense central point cloud.
ax.text(0.025, 0.965, "Migration offsets natural decline", transform=ax.transAxes,
        ha="left", va="top", fontsize=8.5, color=MUTED)
ax.text(0.025, 0.025, "Both components decline", transform=ax.transAxes,
        ha="left", va="bottom", fontsize=8.5, color=MUTED)
finish(fig, ax,
       "Migration often offsets natural population decline",
       f"{neg_nat_pos_mig:,} of {all_n:,} counties have negative natural change but positive net migration in 2023",
       "Each mark is one county or county equivalent with both rates available; metro status is encoded by color. Dashed lines mark zero, separating gains from losses in each component. Rates are shown in the source dataset's units. This is a descriptive decomposition, not an explanation of why people moved. Source: course USDA county dataset.",
       "05_census_migration_vs_natural_change.png", bottom=0.23)

# Figure 6: median county attainment over four source survey periods.
period_columns = [
    ("1990", "Percent of adults with a bachelor's degree or higher, 1990"),
    ("2000", "Percent of adults with a bachelor's degree or higher, 2000"),
    ("2008–12", "Percent of adults with a bachelor's degree or higher, 2008-12"),
    ("2019–23", "Percent of adults with a bachelor's degree or higher, 2019-23"),
]
long_parts = []
for period, column in period_columns:
    vals = pd.to_numeric(county[column], errors="coerce")
    tmp = pd.DataFrame({"Period": period, "Place type": county["Place type"], "BA share": vals})
    long_parts.append(tmp.dropna())
attainment = pd.concat(long_parts, ignore_index=True)
period_order = [p for p, _ in period_columns]
trend = (attainment.groupby(["Place type", "Period"], observed=True)["BA share"]
         .agg(median="median", n="size").reset_index())
fig, ax = plt.subplots(figsize=(9.8, 5.9))
for place in ["Metro", "Nonmetro"]:
    part = trend[trend["Place type"] == place].set_index("Period").reindex(period_order).reset_index()
    ax.plot(range(len(period_order)), part["median"], color=place_colors[place],
            linewidth=2.7, marker="o", markersize=7, label=place)
    last = part.iloc[-1]
    ax.annotate(f"{place}: {last['median']:.1f}%", (3, last["median"]),
                xytext=(9, 0), textcoords="offset points", va="center",
                color=place_colors[place], fontsize=9, fontweight="medium")
ax.set_xticks(range(len(period_order)), period_order)
ax.set_xlim(-0.12, 3.53)
ax.set_ylim(0, 38)
ax.set_xlabel("Survey period")
ax.set_ylabel("County median: adults with bachelor's degree or higher (%)")
style_axis(ax)
ax.legend(frameon=False, loc="upper left")
gap_start = float(trend[(trend["Place type"] == "Metro") & (trend["Period"] == "1990")]["median"].iloc[0] - trend[(trend["Place type"] == "Nonmetro") & (trend["Period"] == "1990")]["median"].iloc[0])
gap_end = float(trend[(trend["Place type"] == "Metro") & (trend["Period"] == "2019–23")]["median"].iloc[0] - trend[(trend["Place type"] == "Nonmetro") & (trend["Period"] == "2019–23")]["median"].iloc[0])
finish(fig, ax,
       "Both county groups gained education; their gap widened",
       f"Median bachelor's attainment rose in metro and nonmetro counties; the gap grew from {gap_start:.1f} to {gap_end:.1f} percentage points",
       "Each point is the median county share in the named ACS survey period; counties are equally weighted. Periods are categorical because the later measures summarize multi-year windows. These medians describe county distributions rather than the share of all U.S. adults. Source: course USDA county dataset.",
       "06_census_attainment_gap_over_time.png", bottom=0.22)

print(f"Wrote figures to {OUTPUT}")
print(f"Latest life-expectancy year: {latest_year}")
print("2023 sex-gap values:", latest.set_index("Country Name")["Gap"].round(2).to_dict())
print("Education/income correlations and counts:", correlations)
print("Migration compensation count:", neg_nat_pos_mig, "of", all_n)
print("Metro/nonmetro education gap:", round(gap_start, 2), "to", round(gap_end, 2), "percentage points")
