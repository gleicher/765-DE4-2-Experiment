"""Make all six figures for DE 4-2.

Run from anywhere:
    /opt/anaconda3/envs/p314/bin/python work/make_figures.py
Writes PNGs to answers/figures/ and a few intermediate CSVs to work/intermediate/.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "answers" / "figures"
INTER = ROOT / "work" / "intermediate"
OUT.mkdir(parents=True, exist_ok=True)
INTER.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": "#555555",
    "axes.labelcolor": "#222222",
    "xtick.color": "#444444",
    "ytick.color": "#444444",
    "axes.titlesize": 11,
    "axes.titleweight": "bold",
    "figure.dpi": 100,
    "savefig.dpi": 200,
})

INK = "#222222"
MUTED = "#6b6b6b"
GRID = "#e6e6e6"


def caption(fig, text, y=0.012, size=8.6):
    fig.text(0.012, y, text, ha="left", va="bottom", fontsize=size, color="#333333")


def title(fig, main, sub=None, y=0.975):
    fig.text(0.012, y, main, ha="left", va="top", fontsize=15, fontweight="bold", color=INK)
    if sub:
        fig.text(0.012, y - 0.045, sub, ha="left", va="top", fontsize=10.5, color="#444444")


# ---------------------------------------------------------------- life expectancy (World Bank)
WB_AGGREGATES = set("""AFE AFW ARB CEB CSS EAP EAR EAS ECA ECS EMU EUU FCS HIC HPC IBD IBT IDA IDB
IDX INX LAC LCN LDC LIC LMC LMY LTE MEA MIC MNA NAC OED OSS PRE PSS PST SAS SSA SSF SST TEA
TEC TLA TMN TSA TSS UMC WLD""".split())

EX_USSR = ["Russian Federation", "Ukraine", "Belarus", "Moldova", "Lithuania", "Latvia", "Estonia",
           "Georgia", "Armenia", "Azerbaijan", "Kazakhstan", "Kyrgyz Republic", "Tajikistan",
           "Turkmenistan", "Uzbekistan"]


EURO_USSR = ["Russian Federation", "Ukraine", "Belarus", "Lithuania", "Latvia", "Estonia"]
SOUTH_USSR = [c for c in EX_USSR if c not in EURO_USSR]


def load_wb():
    d = pd.read_csv(DATA / "lifespan_dataset_1960.csv", index_col=0)
    d = d[~d["Country Code"].isin(WB_AGGREGATES)]
    w = d.pivot_table(index=["Country Name", "Year"], columns="Sex",
                      values="Life Expectancy (years)").reset_index()
    w["gap"] = w["Female"] - w["Male"]
    return w


def fig1a(w):
    others = w[~w["Country Name"].isin(EX_USSR)].dropna(subset=["gap"])
    band = others.groupby("Year")["gap"].quantile([0.1, 0.5, 0.9]).unstack()
    band.to_csv(INTER / "fig1a_rest_of_world_band.csv")

    fig = plt.figure(figsize=(11, 7.4))
    ax = fig.add_axes([0.07, 0.15, 0.80, 0.69])
    ax.fill_between(band.index, band[0.1], band[0.9], color="#d9d9d9", lw=0,
                    label="Middle 80% of all other countries")
    ax.plot(band.index, band[0.5], color="#8a8a8a", lw=2, label="Median of all other countries")

    red_light = "#e8a39a"
    red = "#c0392b"
    for c in EURO_USSR:
        if c == "Russian Federation":
            continue
        s = w[w["Country Name"] == c].set_index("Year")["gap"]
        ax.plot(s.index, s.values, color=red_light, lw=1.1, alpha=0.95)
    south = w[w["Country Name"].isin(SOUTH_USSR)].groupby("Year")["gap"].median()
    south_col = "#8e6c8a"
    ax.plot(south.index, south.values, color=south_col, lw=1.8, ls=(0, (5, 2)))
    ru = w[w["Country Name"] == "Russian Federation"].set_index("Year")["gap"]
    ax.plot(ru.index, ru.values, color=red, lw=2.6)
    ua = w[w["Country Name"] == "Ukraine"].set_index("Year")["gap"]

    # direct labels
    ax.text(2023.6, ru.loc[2023], "Russia", color=red, fontweight="bold", va="center", fontsize=10)
    ax.text(2023.6, ua.loc[2023], "Ukraine", color="#b5584c", va="center", fontsize=9.5)
    ax.text(2023.6, south.loc[2023] - 0.25, "Caucasus, Central\nAsia & Moldova\n(median)",
            color=south_col, va="center", fontsize=8.5)
    ax.text(2023.6, band.loc[2023, 0.5], "Rest of world\n(median)", color="#6b6b6b",
            va="center", fontsize=8.5)

    # annotations of events (background knowledge, not data)
    def note(x, y, txt, xt, yt, ha="left"):
        ax.annotate(txt, xy=(x, y), xytext=(xt, yt), fontsize=8.8, color="#333333", ha=ha,
                    arrowprops=dict(arrowstyle="-", color="#777777", lw=0.8))
    note(1987, ru.loc[1987], "1985-87: Soviet anti-alcohol\ncampaign; gap shrinks", 1979, 0.5,
         ha="center")
    note(1994, ru.loc[1994], "1994: 14.2 years.\nRussian men live to 57.6,\nwomen to 71.7", 1997.5,
         15.6)
    note(2023, ua.loc[2023], "2023: Ukraine's gap\njumps to 13.3 years\n(war since 2022)", 2012.5,
         15.6)
    ax.axvline(1991, color="#999999", lw=0.8, ls=(0, (3, 3)))
    ax.text(1991.3, 1.0, "1991: USSR dissolves", fontsize=8.5, color="#555555")

    ax.set_xlim(1960, 2023)
    ax.set_ylim(0, 16.5)
    ax.set_ylabel("Women's life expectancy minus men's (years)")
    ax.set_xlabel("Year")
    ax.grid(axis="y", color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    ax.legend(loc="upper left", bbox_to_anchor=(0.0, 1.0), frameon=False, fontsize=9,
              handles=[Line2D([], [], color=red, lw=2.6, label="Russia"),
                       Line2D([], [], color=red_light, lw=1.2,
                              label="Ukraine, Belarus, Lithuania, Latvia, Estonia"),
                       Line2D([], [], color=south_col, lw=1.8, ls=(0, (5, 2)),
                              label="Other 9 former Soviet republics (median)"),
                       Line2D([], [], color="#8a8a8a", lw=2, label="Median, all other countries"),
                       mpatches.Patch(color="#d9d9d9", label="Middle 80% of all other countries")])

    title(fig, "In Russia and its European neighbors, women outlive men by twice the usual margin",
          "Gap between female and male life expectancy at birth, 1960-2023. "
          "The Russian gap swings with the country's political shocks.")
    caption(fig, "Data: World Bank life expectancy at birth by sex (CS765 version). Regional and "
            "income-group aggregates removed; 'rest of world' = ~200 countries outside the former "
            "USSR.\nThe gray band is the 10th-90th percentile of their gap in each year. Event labels "
            "come from general background knowledge, not from the data set.")
    fig.savefig(OUT / "q1a_gender_gap_lines.png")
    plt.close(fig)


def fig1b(w):
    panels = [("Russian Federation", "Russia"), ("Ukraine", "Ukraine"), ("Belarus", "Belarus"),
              ("Latvia", "Latvia"),
              ("Poland", "Poland (Soviet bloc, not USSR)"), ("United States", "United States"),
              ("Japan", "Japan"), ("France", "France")]
    fem, mal = "#d35400", "#2c5d8a"
    fig, axes = plt.subplots(2, 4, figsize=(12, 7.6), sharex=True, sharey=True)
    fig.subplots_adjust(left=0.06, right=0.985, top=0.79, bottom=0.14, wspace=0.10, hspace=0.45)
    for ax, (name, lab) in zip(axes.flat, panels):
        s = w[w["Country Name"] == name].set_index("Year").sort_index()
        ax.fill_between(s.index, s["Male"], s["Female"], color="#f2d7c9", lw=0)
        ax.plot(s.index, s["Female"], color=fem, lw=1.8)
        ax.plot(s.index, s["Male"], color=mal, lw=1.8)
        ax.set_title(lab, loc="left", fontsize=10.5,
                     color="#c0392b" if name in EX_USSR else INK)
        for yr in (1994, 2019):
            g = s.loc[yr, "gap"]
            mid = (s.loc[yr, "Male"] + s.loc[yr, "Female"]) / 2
            ax.plot([yr, yr], [s.loc[yr, "Male"], s.loc[yr, "Female"]], color="#555555", lw=0.8)
            dx, ha = (0.8, "left") if yr == 1994 else (-0.8, "right")
            if yr == 1994:
                mid = s.loc[yr, "Female"] - 0.35 * g
            ax.text(yr + dx, mid, f"{g:.1f}", fontsize=8.5, va="center", ha=ha,
                    color="#333333", bbox=dict(fc="#f2d7c9", ec="none", pad=0.5))
        ax.grid(axis="y", color=GRID, lw=0.7)
        ax.set_axisbelow(True)
        ax.set_xlim(1960, 2023)
        ax.set_ylim(50, 90)
        ax.set_xticks([1970, 1990, 2010])
    for ax in axes[:, 0]:
        ax.set_ylabel("Life expectancy at birth (years)")
    a0 = axes[0, 0]
    a0.text(1962, 80.5, "Women", color=fem, fontweight="bold", fontsize=9.5)
    a0.text(1962, 58.5, "Men", color=mal, fontweight="bold", fontsize=9.5)
    for row, (txt, col) in enumerate([("FORMER SOVIET REPUBLICS", "#c0392b"),
                                      ("COMPARISON COUNTRIES", MUTED)]):
        top = axes[row, 0].get_position().y1
        fig.text(0.06, top + 0.045, txt, fontsize=9, color=col, fontweight="bold")

    title(fig, "In the former USSR, the gender gap grows when men's lives get shorter",
          "Life expectancy of women (orange) and men (blue); shaded area is the gap. "
          "Numbers mark the gap in 1994 and 2019.")
    caption(fig, "Data: World Bank life expectancy at birth by sex, 1960-2023 (CS765 version). "
            "Same vertical scale in every panel. In Russia, Ukraine, Belarus and Latvia the female\n"
            "line is fairly flat while the male line falls in the 1990s, so the shaded gap balloons; "
            "in the comparison countries both lines rise together.")
    fig.savefig(OUT / "q1b_gender_gap_small_multiples.png")
    plt.close(fig)


# ---------------------------------------------------------------- census
RUCC_LABELS = {
    1: "Metro, 1 million+",
    2: "Metro, 250k-1 million",
    3: "Metro, under 250k",
    4: "Nonmetro, 20k+ urban, next to metro",
    5: "Nonmetro, 20k+ urban, remote",
    6: "Nonmetro, 5k-20k urban, next to metro",
    7: "Nonmetro, 5k-20k urban, remote",
    8: "Nonmetro, <5k urban, next to metro",
    9: "Nonmetro, <5k urban, remote",
}
YEARS = [2021, 2022, 2023]


def load_counties():
    d = pd.read_csv(DATA / "full_census_dataset.csv", encoding="latin1", low_memory=False)
    c = d[(d["FIPS Code"] % 1000 != 0) & (d["State"] != "PR")].copy()
    c = c[c["2023 Rural-urban Continuum Code"].notna() & c["Population Estimate 2023"].notna()]
    c["rucc"] = c["2023 Rural-urban Continuum Code"].astype(int)
    c["pop"] = c[[f"Population Estimate {y}" for y in YEARS]].mean(axis=1)
    for comp, col in [("natural", "Natural Change"), ("domestic", "Domestic migration"),
                      ("intl", "International Migration")]:
        c[comp] = c[[f"{col} {y}" for y in YEARS]].sum(axis=1) / 3  # people per year
        c[comp + "_rate"] = c[comp] / c["pop"] * 1000
    return c


def fig2a(c):
    g = c.groupby("rucc")
    t = pd.DataFrame({
        "natural": g["natural"].sum() / g["pop"].sum() * 1000,
        "domestic": g["domestic"].sum() / g["pop"].sum() * 1000,
        "intl": g["intl"].sum() / g["pop"].sum() * 1000,
        "n": g.size(),
        "popshare": g["pop"].sum() / c["pop"].sum() * 100,
    })
    t["net"] = t[["natural", "domestic", "intl"]].sum(axis=1)
    t.to_csv(INTER / "fig2a_components_by_rucc.csv")

    cols = {"natural": "#7b6aa8", "domestic": "#e08a2c", "intl": "#2a9d8f"}
    names = {"natural": "Natural change (births minus deaths)",
             "domestic": "Domestic migration (moves within the US)",
             "intl": "International migration"}
    fig = plt.figure(figsize=(11.5, 7.2))
    ax = fig.add_axes([0.27, 0.17, 0.52, 0.60])
    import matplotlib.transforms as mtrans
    tr = mtrans.blended_transform_factory(ax.transAxes, ax.transData)
    ypos = {k: i + (0.6 if k >= 4 else 0) for i, k in enumerate(range(1, 10))}
    h = 0.62
    for k, row in t.iterrows():
        y = ypos[k]
        pos, neg = 0.0, 0.0
        for comp in ["natural", "domestic", "intl"]:
            v = row[comp]
            if v >= 0:
                ax.barh(y, v, left=pos, height=h, color=cols[comp], edgecolor="white", lw=1.2)
                pos += v
            else:
                ax.barh(y, v, left=neg, height=h, color=cols[comp], edgecolor="white", lw=1.2)
                neg += v
        ax.plot(row["net"], y, marker="D", color="black", ms=6.5, mec="white", mew=1.2, zorder=5)
        ax.text(1.10, y, f"{row['net']:+.1f}", va="center", ha="right", fontsize=9.5,
                fontweight="bold", transform=tr)
        ax.text(1.24, y, f"{int(row['n'])}", va="center", ha="right", fontsize=9, color=MUTED,
                transform=tr)
        ax.text(1.38, y, f"{row['popshare']:.1f}%", va="center", ha="right", fontsize=9,
                color=MUTED, transform=tr)
    ax.text(1.10, -0.95, "Net", fontsize=9, fontweight="bold", ha="right", transform=tr)
    ax.text(1.24, -0.95, "Counties", fontsize=9, color=MUTED, ha="right", transform=tr)
    ax.text(1.38, -0.95, "Share of\nUS pop.", fontsize=9, color=MUTED, ha="right", transform=tr)
    ax.set_yticks([ypos[k] for k in range(1, 10)])
    ax.set_yticklabels([RUCC_LABELS[k] for k in range(1, 10)])
    ax.set_ylim(9.2, -1.5)
    ax.set_xlim(-6.5, 8.5)
    ax.axvline(0, color="#333333", lw=1)
    ax.grid(axis="x", color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.set_xlabel("Average yearly change per 1,000 residents, 2021-2023\n"
                  "<- shrinking                                        growing ->")
    ax.text(-0.47, -0.75, "METRO", fontsize=8.5, color=MUTED, fontweight="bold", transform=tr)
    ax.text(-0.47, 3.12, "NONMETRO", fontsize=8.5, color=MUTED, fontweight="bold", transform=tr)
    ax.plot([-0.47, 1.38], [2.8, 2.8], color="#bbbbbb", lw=0.8, transform=tr, clip_on=False)
    handles = [mpatches.Patch(color=cols[k], label=names[k]) for k in cols]
    handles.append(Line2D([], [], marker="D", color="black", ls="none", ms=6,
                          label="Net change (sum of the three)"))
    fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.012, 0.865), ncol=4,
               frameon=False, fontsize=9, handlelength=1.4, columnspacing=1.3)

    # callouts
    r1 = t.loc[1]
    ax.annotate("Big metros lose movers to the\nrest of the US every year; births\n"
                "and immigrants make up for it",
                xy=(r1["domestic"] * 0.5, ypos[1] + 0.3), xytext=(-6.3, 2.0), fontsize=8.4,
                va="center",
                color="#333333", arrowprops=dict(arrowstyle="-", color="#777777", lw=0.8))
    r8 = t.loc[8]
    ax.text(1.6, ypos[5], "Rural counties: more deaths than births,\nso movers from elsewhere "
            "in the US are\nwhat keeps most of them growing", fontsize=8.4, va="center",
            color="#333333")

    title(fig, "Big metros grow from births and immigrants; everywhere else grows from movers",
          "Where population change came from in 2021-2023, by the USDA's 2023 rural-urban "
          "continuum code")
    caption(fig, "Data: USDA ERS county-level population estimates (CS765 joined census file), "
            "3,106 US counties/county-equivalents (Puerto Rico excluded). Each bar is all counties of "
            "that type pooled together:\ncomponent totals for 2021-2023 divided by the group's "
            "average population, per year. 'Urban' = population of the county's urban areas. The "
            "Census 'residual' term is omitted (it is small).", size=8.3)
    fig.savefig(OUT / "q2a_components_by_rucc.png")
    plt.close(fig)


def fig2b(c):
    c = c.copy()
    c["metro"] = c["rucc"] <= 3
    xlim, ylim = 20, 45
    fig, axes = plt.subplots(1, 2, figsize=(12, 7.0), sharex=True, sharey=True)
    fig.subplots_adjust(left=0.07, right=0.985, top=0.79, bottom=0.2, wspace=0.07)
    colors = {True: "#3b6ea5", False: "#b8732c"}
    # county label: (FIPS, text, x offset, y offset)
    labels_big = [(6037, "Los Angeles", -6, -6), (17031, "Cook (Chicago)", 6, -8),
                  (48201, "Harris (Houston)", 5, -5), (4013, "Maricopa (Phoenix)", 6, 6),
                  (36047, "Brooklyn", 6, -3)]
    rows = []
    for ax, metro in zip(axes, [True, False]):
        s = c[c["metro"] == metro]
        x = s["natural_rate"].clip(-xlim, xlim)
        y = s["domestic_rate"].clip(-ylim, ylim)
        size = np.sqrt(s["pop"]) / 18
        ax.scatter(x, y, s=size, color=colors[metro], alpha=0.45, lw=0.3, edgecolor="white")
        ax.axhline(0, color="#333333", lw=0.9)
        ax.axvline(0, color="#333333", lw=0.9)
        ax.set_xlim(-xlim, xlim)
        ax.set_ylim(-ylim, ylim)
        ax.grid(color=GRID, lw=0.7)
        ax.set_axisbelow(True)
        n = len(s)
        P = s["pop"].sum()
        quads = {
            "tr": ((s.natural_rate > 0) & (s.domestic_rate > 0)),
            "tl": ((s.natural_rate <= 0) & (s.domestic_rate > 0)),
            "br": ((s.natural_rate > 0) & (s.domestic_rate <= 0)),
            "bl": ((s.natural_rate <= 0) & (s.domestic_rate <= 0)),
        }
        pos = {"tr": (xlim - 0.6, ylim - 1.5, "right", "top"),
               "tl": (-xlim + 0.6, ylim - 1.5, "left", "top"),
               "br": (xlim - 0.6, -ylim + 1.5, "right", "bottom"),
               "bl": (-xlim + 0.6, -ylim + 1.5, "left", "bottom")}
        desc = {"tr": "more births & gaining movers", "tl": "more deaths, but gaining movers",
                "br": "more births, but losing movers", "bl": "more deaths & losing movers"}
        for q, m in quads.items():
            px, py, ha, va = pos[q]
            pc = m.sum() / n * 100
            pp = s.loc[m, "pop"].sum() / P * 100
            ax.text(px, py, f"{pc:.0f}% of counties\n{pp:.0f}% of people\n{desc[q]}", ha=ha, va=va,
                    fontsize=8.8, color=INK,
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#cccccc", alpha=0.9))
            rows.append(dict(metro=metro, quad=q, pct_counties=pc, pct_pop=pp))
        ax.set_title(("Metro counties" if metro else "Nonmetro (rural and small-town) counties")
                     + f"  (n = {n:,})", loc="left", color=colors[metro])
        ax.set_xlabel("Natural change: births minus deaths, per 1,000 residents per year")
        if metro:
            for fips, nm, dx, dy in labels_big:
                r = s[s["FIPS Code"] == fips]
                xx = min(r["natural_rate"].iloc[0], xlim)
                yy = min(r["domestic_rate"].iloc[0], ylim)
                ax.annotate(nm, xy=(xx, yy), xytext=(xx + dx, yy + dy), fontsize=8,
                            color="#222222", ha="left" if dx > 0 else "right", va="center",
                            arrowprops=dict(arrowstyle="-", color="#666666", lw=0.6))
    axes[0].set_ylabel("Domestic migration: net movers from elsewhere in the US,\n"
                       "per 1,000 residents per year")
    pd.DataFrame(rows).to_csv(INTER / "fig2b_quadrant_shares.csv", index=False)
    # size legend
    for p, lab in [(10_000, "10k"), (100_000, "100k"), (1_000_000, "1M")]:
        axes[1].scatter([], [], s=np.sqrt(p) / 18, color="#999999", alpha=0.6, label=lab)
    axes[1].legend(title="County population", loc="center right", frameon=True, fontsize=8,
                   title_fontsize=8, labelspacing=1.1, borderpad=0.9, framealpha=0.9,
                   edgecolor="#cccccc", bbox_to_anchor=(1.0, 0.62))

    title(fig, "84% of rural counties have more deaths than births; movers decide if they grow",
          "Each dot is a county (2021-2023 average). Nearly half of metro residents live in "
          "counties with more births but net domestic out-migration (lower right).")
    caption(fig, "Data: USDA ERS county-level population estimates (CS765 joined census file), "
            "2021-2023, 3,106 US counties (Puerto Rico excluded). Metro = 2023 rural-urban "
            "continuum codes 1-3.\nDot area is proportional to population. Counties beyond the "
            "axis limits (about 1%) are pinned to the edge of the plot. International migration is not shown "
            "here (it is small outside big metros).", size=8.3)
    fig.savefig(OUT / "q2b_county_scatter.png")
    plt.close(fig)


# ---------------------------------------------------------------- life expectancy (OWID)
def first_crossing(g, t, max_gap=5):
    """Year life expectancy first reaches t, only if the observation before it is <= max_gap
    years earlier (so the crossing year is actually pinned down by the data)."""
    v = g["le"].values
    yrs = g["year"].values
    idx = np.where(v >= t)[0]
    if len(idx) == 0:
        return np.nan, "never"
    i = idx[0]
    if i == 0:
        return np.nan, "already above at first record"
    if yrs[i] - yrs[i - 1] > max_gap:
        return np.nan, "data too sparse"
    return yrs[i], "ok"


def fig3():
    d = pd.read_csv(DATA / "life-expectancy-owid" / "life-expectancy-owid.csv")
    d.columns = ["ent", "code", "year", "le"]
    d = d[d["code"].notna() & ~d["code"].astype(str).str.startswith("OWID")]
    rows = []
    for e, g in d.groupby("ent"):
        g = g.sort_values("year")
        a, fa = first_crossing(g, 50)
        b, fb = first_crossing(g, 70)
        rows.append(dict(country=e, reach50=a, flag50=fa, reach70=b, flag70=fb,
                         le2023=g["le"].iloc[-1], last=g["year"].iloc[-1]))
    r = pd.DataFrame(rows)
    r.to_csv(INTER / "fig3_crossing_years.csv", index=False)
    ok = r[r["flag50"] == "ok"].copy()
    done = ok[ok["flag70"] == "ok"].copy()
    done["years"] = done["reach70"] - done["reach50"]
    notyet = ok[ok["flag70"] == "never"].copy()
    notyet["years"] = 2023 - notyet["reach50"]

    fig = plt.figure(figsize=(11.5, 7.6))
    ax = fig.add_axes([0.075, 0.15, 0.89, 0.71])
    xs = np.array([1940, 2023])
    ax.plot(xs, 2023 - xs, color="#bbbbbb", lw=1, ls=(0, (4, 3)), zorder=1,
            label="Years elapsed between reaching 50 and 2023")
    ax.scatter(done["reach50"], done["years"], s=34, color="#1f6f8b", alpha=0.85,
               edgecolor="white", lw=0.6, zorder=3, label="Reached 70: years from 50 to 70")
    ax.scatter(notyet["reach50"], notyet["years"], s=40, marker="^", facecolor="white",
               edgecolor="#c0392b", lw=1.2, zorder=3,
               label="Not at 70 yet in 2023: years so far (still counting)")

    lab = {"Norway": (6, 0), "Sweden": (6, -2), "United States": (6, 2), "United Kingdom": (-4, -6),
           "Argentina": (6, 2), "Italy": (-5, -6), "Japan": (-4, -6), "Russia": (6, 1),
           "South Korea": (-6, 6), "China": (5, 3), "India": (5, 3), "Oman": (4, -5),
           "Bangladesh": (5, -4), "Algeria": (4, -5), "Brazil": (5, 3), 
           "Maldives": (-3, -6), "Nigeria": (5, 2), "Chad": (4, 2),
           "Zimbabwe": (5, 0), "South Africa": (5, 1), "Lesotho": (5, 1), "Ethiopia": (4, 2),
           "Philippines": (0, 0)}
    allpts = pd.concat([done, notyet])
    for nm, (dx, dy) in lab.items():
        rr = allpts[allpts["country"] == nm]
        if not len(rr):
            continue
        x, y = rr["reach50"].iloc[0], rr["years"].iloc[0]
        ha = "left" if dx >= 0 else "right"
        ax.annotate(nm, xy=(x, y), xytext=(x + dx * 0.8, y + dy * 0.8), fontsize=8.3,
                    color="#333333", ha=ha, va="center",
                    arrowprops=dict(arrowstyle="-", color="#999999", lw=0.5,
                                    shrinkA=0, shrinkB=3))

    ax.annotate("Pioneers took 50-90 years:\nNorway first hit 50 in 1854\nand 70 in 1947",
                xy=(1856, 92), xytext=(1868, 84), fontsize=9, color="#333333",
                arrowprops=dict(arrowstyle="-", color="#777777", lw=0.8))
    ax.text(1952, 6, "Late starters such as Japan, Oman and the\nMaldives did it in under 25 years",
            fontsize=9, color="#1f6f8b")
    ax.text(1971, 82, "58 countries that reached 50 (most of them\nin sub-Saharan Africa) "
            "were still below 70\nin 2023. Their marks sit on the dashed line\nand will move up "
            "until they get there.", fontsize=9, color="#c0392b", va="top")

    ax.set_xlim(1845, 2015)
    ax.set_ylim(0, 100)
    ax.set_xlabel("Year the country's life expectancy first reached 50")
    ax.set_ylabel("Years it took to go from 50 to 70")
    ax.grid(color=GRID, lw=0.7)
    ax.set_axisbelow(True)
    ax.legend(loc="upper right", frameon=False, fontsize=9)

    title(fig, "Getting from 50 to 70: latecomers did it faster, but not all of them",
          f"Each mark is a country. {len(done)} have made the climb; {len(notyet)} crossed 50 "
          "but were still below 70 in 2023.")
    caption(fig, "Data: Our World in Data, period life expectancy at birth (Riley; Zijdeman "
            "et al.; HMD; UN WPP), CS765 version. Regions and aggregates removed.\n"
            "A country is included only if the data pins down when it crossed 50 (an observation "
            "less than 5 years before the crossing). This drops countries that were\n"
            "already above 50 when their record starts (often 1950) and ones with sparse "
            "historical data. 'First reached' ignores later dips (e.g., Zimbabwe and South\n"
            "Africa fell back below 50 during the HIV/AIDS epidemic).", size=8.2)
    fig.savefig(OUT / "q3_fifty_to_seventy.png")
    plt.close(fig)


# ---------------------------------------------------------------- unemployment (state level)
def fig4():
    a = pd.read_csv(DATA / "aggregate_census_dataset.csv", sep="\t", encoding="latin1")
    a = a[a["State"] != "PR"]  # no 2020 value for PR
    yrs = list(range(2000, 2024))
    u = a.set_index("State")[[f"Unemployment rate {y}" for y in yrs]]
    u.columns = yrs
    names = a.set_index("State")["Area name"]
    gr = u[[2009, 2010, 2011]].max(axis=1) - u[2007]
    cv = u[2020] - u[2019]
    diff = cv - gr
    states = u.drop(index="US")
    order = diff.drop(index="US").sort_values(ascending=False).index.tolist()
    rows = ["US"] + order
    pd.DataFrame({"great_recession_rise": gr, "covid_rise": cv, "covid_minus_gr": diff}).loc[rows]\
        .to_csv(INTER / "fig4_recession_rises.csv")

    fig = plt.figure(figsize=(11.5, 13))
    axh = fig.add_axes([0.15, 0.12, 0.53, 0.74])
    axd = fig.add_axes([0.72, 0.12, 0.25, 0.74], sharey=axh)
    M = u.loc[rows].values
    yy = np.arange(len(rows)) + np.array([0] + [0.6] * len(order))
    cmap = plt.get_cmap("YlOrRd")
    from matplotlib.colors import BoundaryNorm
    bounds = [0, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14]
    norm = BoundaryNorm(bounds, cmap.N)
    for i, rw in enumerate(rows):
        for j, y in enumerate(yrs):
            axh.add_patch(mpatches.Rectangle((y - 0.5, yy[i] - 0.5), 1, 1,
                                             color=cmap(norm(M[i, j])), ec="white", lw=0.6))
    axh.set_xlim(1999.5, 2023.5)
    axh.set_ylim(yy[-1] + 0.6, -0.6)
    axh.set_yticks(yy)
    axh.set_yticklabels([("United States" if s == "US" else names[s]) for s in rows], fontsize=8.6)
    axh.get_yticklabels()[0].set_fontweight("bold")
    axh.set_xticks([2000, 2005, 2010, 2015, 2020])
    axh.tick_params(axis="x", labeltop=False, labelbottom=True, length=2)
    axh.tick_params(axis="y", length=0)
    for sp in axh.spines.values():
        sp.set_visible(False)
    for x0, x1, lab in [(2007.5, 2013.5, "Great Recession and slow recovery"),
                        (2019.5, 2021.5, "Pandemic")]:
        axh.plot([x0, x1], [-1.0, -1.0], color="#555555", lw=1, clip_on=False)
        axh.text((x0 + x1) / 2, -1.3, lab, ha="center", va="bottom", fontsize=8.6, color="#333333",
                 clip_on=False)
    # colorbar
    cax = fig.add_axes([0.15, 0.072, 0.30, 0.010])
    sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    cb = fig.colorbar(sm, cax=cax, orientation="horizontal", ticks=bounds)
    cb.set_label("Unemployment rate (%), annual average", fontsize=8.8)
    cb.ax.tick_params(labelsize=8)
    cb.outline.set_visible(False)

    # dumbbell panel
    gcol, ccol = "#555555", "#c0392b"
    for i, rw in enumerate(rows):
        axd.plot([gr[rw], cv[rw]], [yy[i], yy[i]], color="#cccccc", lw=1.4, zorder=1)
        axd.scatter(gr[rw], yy[i], s=30, color=gcol, zorder=3)
        axd.scatter(cv[rw], yy[i], s=30, color=ccol, zorder=3)
    axd.set_xlim(0, 10)
    axd.grid(axis="x", color=GRID, lw=0.7)
    axd.set_axisbelow(True)
    axd.tick_params(axis="y", left=False, labelleft=False)
    axd.tick_params(axis="x", labeltop=True, labelbottom=True)
    axd.spines["left"].set_visible(False)
    axd.set_xlabel("Rise in unemployment (percentage points)", fontsize=8.8)
    axd.legend(handles=[Line2D([], [], marker="o", ls="none", color=gcol,
                               label="Great Recession: 2009-11 peak\nminus 2007"),
                        Line2D([], [], marker="o", ls="none", color=ccol,
                               label="Pandemic: 2020 minus 2019")],
               loc="lower left", bbox_to_anchor=(0.0, 1.035), fontsize=8.3, frameon=False)
    axd.text(9.8, yy[1] + 0.2, "hit harder by\nthe pandemic", ha="right", va="top", fontsize=8.5,
             color=ccol, fontweight="bold")
    axd.text(9.8, yy[-14], "hit harder by the\nGreat Recession", ha="right", va="center",
             fontsize=8.5, color=gcol, fontweight="bold")

    title(fig, "Two recessions, two different maps of who got hurt", y=0.985)
    fig.text(0.012, 0.958,
             "Unemployment rate by state, 2000-2023. States are sorted by how much bigger their "
             "2020 jump was than their Great Recession rise.\nHawaii, Massachusetts and New York "
             "were hit far harder by the pandemic; Arizona, Idaho, Alabama, Utah and Georgia far "
             "harder in 2009-11.\nThe Great Recession spike lasted years; the pandemic spike was mostly "
             "gone by 2022.", ha="left", va="top", fontsize=10, color="#444444")
    caption(fig, "Data: USDA ERS / BLS LAUS state unemployment rates (CS765 aggregate census "
            "file). 50 states + DC; Puerto Rico omitted\n(no 2020 value). Annual averages, so the "
            "April 2020 peak is smoothed out.", y=0.005, size=8.3)
    fig.text(0.50, 0.045, "", fontsize=1)
    fig.savefig(OUT / "q4_unemployment_two_recessions.png")
    plt.close(fig)


if __name__ == "__main__":
    w = load_wb()
    fig1a(w)
    fig1b(w)
    c = load_counties()
    fig2a(c)
    fig2b(c)
    fig3()
    fig4()
    print("done")
