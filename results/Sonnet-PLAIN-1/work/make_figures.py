"""Regenerate all six figures for Design Exercise 4-2.

Run:  /opt/anaconda3/envs/p314/bin/python -I work/make_figures.py
(from the Sonnet-PLAIN-1 directory).  Writes PNGs to answers/figures/.
"""
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "answers" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": "#555555",
    "axes.labelcolor": "#222222",
    "xtick.color": "#444444",
    "ytick.color": "#444444",
    "figure.facecolor": "white",
})
INK = "#222222"
GREY = "#8a8a8a"
BLUE = "#2b6cb0"
ORANGE = "#d9730d"
RED = "#b3261e"
TEAL = "#1b7f79"


def caption(fig, text, width=150, y=0.012, size=9.5):
    fig.text(0.02, y, "\n".join(textwrap.wrap(text, width)), ha="left", va="bottom",
             fontsize=size, color="#444444", linespacing=1.35)


def title(fig, t, sub=None, size=19):
    fw, fh = fig.get_size_inches()
    width = int(fw * 72 * 0.95 / (size * 0.64))
    lines = textwrap.wrap(t, width)
    fig.text(0.02, 0.985, "\n".join(lines), ha="left", va="top", fontsize=size, fontweight="bold",
             color=INK, linespacing=1.25)
    if sub:
        dy = (len(lines) * size * 1.25 + 8) / 72 / fh
        fig.text(0.02, 0.985 - dy, sub, ha="left", va="top", fontsize=11.5, color="#444444")


# --------------------------------------------------------------------------
# Data: life expectancy (Our World in Data) -> shock episodes
# --------------------------------------------------------------------------
def load_owid():
    o = pd.read_csv(DATA / "life-expectancy-owid" / "life-expectancy-owid.csv")
    o = o.rename(columns={"Period life expectancy at birth": "LE"})
    o = o[(o.Year >= 1950) & o.Code.notna() & ~o.Code.astype(str).str.startswith("OWID")]
    return o


def shock_episodes(o, thresh=5.0, min_depth=9.0):
    """One-year drops of >= `thresh` years; keep episodes with depth >= min_depth.

    Countries with 3+ such drops (CAR, South Sudan, Somalia, Lebanon, Eritrea) are
    excluded: their estimates are erratic rather than a single identifiable event.
    Recovery = first year after the trough with LE >= the level of the year before the drop.
    """
    rows = []
    series = {}
    for e, g in o.groupby("Entity"):
        s = g.sort_values("Year").set_index("Year").LE
        d = s.diff()
        ev = d[d <= -thresh].index
        if len(ev) >= 3:
            continue
        last = -99
        for y in ev:
            if y - last <= 3:
                continue
            last = y
            pre = s.loc[y - 1]
            w = s.loc[y:y + 4]
            tr, ty = w.min(), w.idxmin()
            after = s.loc[ty:]
            rec = after[after >= pre]
            ry = rec.index[0] if len(rec) else np.nan
            rows.append(dict(entity=e, year=y, pre=pre, trough=tr, depth=pre - tr,
                             rec_year=ry, rec_years=(ry - (y - 1)) if len(rec) else np.nan))
            series[(e, y)] = s
    r = pd.DataFrame(rows)
    r = r[r.depth >= min_depth].sort_values("depth", ascending=False).reset_index(drop=True)
    return r, series


LABEL = {"Bosnia and Herzegovina": "Bosnia & Herz.", "North Korea": "North Korea",
         "Equatorial Guinea": "Equatorial Guinea", "East Timor": "East Timor"}


def recovery_color(row):
    if np.isnan(row.rec_years):
        return RED
    if row.rec_years <= 5:
        return TEAL
    if row.rec_years <= 10:
        return ORANGE
    return RED


# --------------------------------------------------------------------------
# Figure 1A: small multiples of shock episodes
# --------------------------------------------------------------------------
def fig_1a():
    o = load_owid()
    r, series = shock_episodes(o)
    n = len(r)
    ncol, nrow = 4, int(np.ceil(n / 4))
    fig, axes = plt.subplots(nrow, ncol, figsize=(15, 3.0 * nrow + 2.0), sharey=True)
    fig.subplots_adjust(left=0.05, right=0.985, top=0.86, bottom=0.13, hspace=0.62, wspace=0.08)
    for ax, (_, row) in zip(axes.flat, r.iterrows()):
        s = series[(row.entity, row.year)]
        lo, hi = row.year - 10, row.year + 30
        w = s.loc[max(lo, 1950):min(hi, 2023)]
        c = recovery_color(row)
        ax.axhline(row.pre, color=GREY, lw=1, ls=(0, (4, 3)), zorder=1)
        ax.plot(w.index, w.values, color=INK, lw=1.6, zorder=3)
        # shaded loss: years between the drop and recovery where LE is below pre-drop level
        end = row.rec_year if not np.isnan(row.rec_year) else w.index.max()
        seg = w.loc[row.year - 1:end]
        ax.fill_between(seg.index, seg.values, row.pre, where=seg.values < row.pre,
                        color=c, alpha=0.35, lw=0, zorder=2)
        ax.scatter([row.year - 1], [row.pre], s=14, color=GREY, zorder=4)
        ax.set_xlim(w.index.min(), w.index.max())
        ax.set_ylim(5, 85)
        ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(10))
        ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
        ax.tick_params(labelsize=8)
        rec = "not yet back to old level" if np.isnan(row.rec_years) else \
            f"back to old level after {int(row.rec_years)} yr"
        name = LABEL.get(row.entity, row.entity)
        ax.set_title(f"{name}, {int(row.year)}", fontsize=10.5, fontweight="bold", loc="left", color=INK, pad=14)
        ax.text(0, 1.02, f"-{row.depth:.0f} yrs; {rec}", transform=ax.transAxes, fontsize=8.3,
                color=c, va="bottom", fontweight="bold")
    for ax in axes.flat[n:]:
        ax.axis("off")
    for ax in axes[:, 0]:
        ax.set_ylabel("Life expectancy (years)", fontsize=9)
    title(fig, "Life expectancy can collapse by 10-30 years in a single year, yet most countries regained it within 5 years",
          "All 14 episodes since 1950 where life expectancy fell 9+ years in a few years (Our World in Data). Shaded area = the loss, from the drop until the pre-drop level returns.", size=15.5)
    lax = axes.flat[n]
    lax.axis("off")
    lax.legend(handles=[Patch(color=TEAL, alpha=.5, label="loss regained within 5 years"),
                        Patch(color=ORANGE, alpha=.5, label="regained in 6-10 years"),
                        Patch(color=RED, alpha=.5, label="more than 10 years / not yet"),
                        Line2D([], [], color=GREY, ls=(0, (4, 3)), label="level the year before the drop")],
               loc="center left", frameon=False, fontsize=9.5, title="Time to recover", title_fontsize=10)
    caption(fig, "Panels are ordered by size of the drop and share one vertical scale (5-85 years), so depth is comparable across panels. "
            "An episode is a year-over-year fall of 5+ years in 'period life expectancy at birth' that totals 9+ years at the trough; recovery is the first year after the trough "
            "back at the pre-drop level. Countries with three or more such drops (Central African Republic, South Sudan, Somalia, Lebanon, Eritrea) are left out because their estimates are erratic. "
            "Palestine's 2023 drop is the last year in the data, so recovery cannot be judged. Source: Our World in Data / UN WPP, HMD, Zijdeman et al., Riley (retrieved Sep 2025).",
            width=185, size=8.8)
    fig.savefig(OUT / "q1a_shocks_small_multiples.png", dpi=170)
    plt.close(fig)
    return r


# --------------------------------------------------------------------------
# Figure 1B: depth vs years-to-recover scatter
# --------------------------------------------------------------------------
def fig_1b(r):
    fig, ax = plt.subplots(figsize=(12, 8.2))
    fig.subplots_adjust(left=0.08, right=0.97, top=0.84, bottom=0.2)
    rr = r.copy()
    ax.axhspan(0, 5, color=TEAL, alpha=0.07, lw=0)
    ax.axhspan(10, 20, color=RED, alpha=0.06, lw=0)
    offs = {
        "Rwanda": (0, -17, "center"), "Cambodia": (0, 9, "center"), "Bangladesh": (8, 4, "left"),
        "Bosnia and Herzegovina": (8, -12, "left"), "Burundi": (0, -17, "center"), "Haiti": (-9, -3, "right"),
        "China": (6, 12, "left"), "Armenia": (0, -17, "center"), "Cyprus": (-9, -3, "right"),
        "Equatorial Guinea": (8, 3, "left"), "East Timor": (8, 3, "left"), "Palestine": (8, 3, "left"),
        "North Korea": (8, 3, "left"), "Montserrat": (8, 4, "left"), "Western Sahara": (8, -12, "left"),
        "Syria": (8, 4, "left"),
    }
    # jitter identical coordinates slightly so the dots stay distinguishable
    for _, row in rr.iterrows():
        yv = 19.0 if np.isnan(row.rec_years) else row.rec_years
        marker = "X" if np.isnan(row.rec_years) else "o"
        ax.scatter(row.depth, yv, s=120, color=recovery_color(row), marker=marker,
                   edgecolor="white", lw=1.2, zorder=3)
        dx, dy, ha = offs.get(row.entity, (8, 4, "left"))
        txt = f"{LABEL.get(row.entity, row.entity)} {int(row.year)}"
        ax.annotate(txt, (row.depth, yv), xytext=(dx, dy), textcoords="offset points", ha=ha,
                    fontsize=9.5, color=INK)
    ax.set_xlim(8, 33)
    ax.set_ylim(0, 20.5)
    ax.set_yticks([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 19.0])
    ax.set_yticklabels(["0", "2", "4", "6", "8", "10", "12", "14", "16", "18", "not yet\n(data ends)"])
    ax.set_xlabel("Size of the drop: years of life expectancy lost (pre-drop level minus trough)", fontsize=11)
    ax.set_ylabel("Years from the drop until life expectancy is back at its pre-drop level", fontsize=11)
    ax.grid(axis="y", color="#e3e3e3", lw=0.8)
    ax.set_axisbelow(True)
    ax.text(32.8, 0.35, "fast rebound (5 years or less)", ha="right", color=TEAL, fontsize=10, fontweight="bold")
    ax.text(32.8, 20.0, "slow rebound", ha="right", color=RED, fontsize=10, fontweight="bold")
    title(fig, "Deeper drops do not mean slower recoveries",
          "14 collapses of 9+ years in life expectancy since 1950: how deep, and how long until the pre-drop level returned", size=19)
    fig.text(0.02, 0.88 - 0.075, "", fontsize=1)
    caption(fig, "Each dot is one country-episode. The deepest collapses (Rwanda 1994, Cambodia 1975, Bangladesh 1970, Bosnia 1992) were regained within 3-5 years, "
            "whereas smaller drops in North Korea (1995), East Timor (1975) and Equatorial Guinea (1969) took 12-17 years. "
            "Years to recover are counted from the last year before the drop until life expectancy is first back at that level. Countries with 3+ drops of this size (e.g. Central African Republic, South Sudan) are excluded as erratic estimates. "
            "Palestine's drop is in 2023, the last year of data. Source: Our World in Data (UN WPP, HMD, Zijdeman et al., Riley), retrieved Sep 2025.",
            width=140, y=0.015, size=9.2)
    fig.savefig(OUT / "q1b_depth_vs_recovery.png", dpi=170)
    plt.close(fig)


# --------------------------------------------------------------------------
# Census: education by rural-urban continuum
# --------------------------------------------------------------------------
RUCC = {
    1: "1  Metro, 1M+ pop.", 2: "2  Metro, 250k-1M", 3: "3  Metro, <250k",
    4: "4  Nonmetro, urban 20k+, adjacent", 5: "5  Nonmetro, urban 20k+, not adj.",
    6: "6  Nonmetro, urban 5-20k, adjacent", 7: "7  Nonmetro, urban 5-20k, not adj.",
    8: "8  Nonmetro, rural <5k, adjacent", 9: "9  Nonmetro, rural <5k, not adj.",
}
PERIODS = ["1990", "2000", "2008-12", "2019-23"]


def load_edu():
    c = pd.read_csv(DATA / "full_census_dataset.csv", dtype={"FIPS Code": str}, encoding="latin-1")
    cols = {p: f"Percent of adults with a bachelor's degree or higher, {p}" for p in PERIODS}
    d = c[["FIPS Code", "State", "Area name", "Rural Urban Continuum Code 2023", "Census Population 2020"]
          + list(cols.values())].rename(columns={v: k for k, v in cols.items()})
    d = d.rename(columns={"Rural Urban Continuum Code 2023": "rucc"})
    d = d.dropna(subset=["rucc"] + PERIODS)
    d["rucc"] = d.rucc.astype(int)
    return d


def fig_2a():
    d = load_edu()
    med = d.groupby("rucc")[PERIODS].median()
    fig, ax = plt.subplots(figsize=(12, 8.6))
    fig.subplots_adjust(left=0.07, right=0.76, top=0.84, bottom=0.2)
    x = np.arange(4)
    cmap = plt.get_cmap("viridis_r")
    # color: metro blue family -> rural orange family (diverging in meaning, ordered by code)
    cols = {1: "#08306b", 2: "#2171b5", 3: "#6baed6", 4: "#74c476", 5: "#238b45",
            6: "#fdae6b", 7: "#e6550d", 8: "#a63603", 9: "#7f2704"}
    for k in range(1, 10):
        y = med.loc[k].values
        ax.plot(x, y, color=cols[k], lw=2.4 if k in (1, 9) else 1.8, marker="o", ms=5, zorder=3)
    # direct labels (nudged to avoid collisions)
    y_end = med[PERIODS[-1]].copy()
    lab_y = {}
    order = y_end.sort_values().index.tolist()
    last = -99
    for k in order:
        yy = max(y_end[k], last + 1.15)
        lab_y[k] = yy
        last = yy
    for k in range(1, 10):
        ax.annotate(f"{RUCC[k]}", (3, y_end[k]), xytext=(3.12, lab_y[k]), va="center", fontsize=9.3,
                    color=cols[k], fontweight="bold" if k in (1, 9) else "normal",
                    arrowprops=dict(arrowstyle="-", color=cols[k], lw=0.6, shrinkA=0, shrinkB=2))
    ax.set_xlim(-0.15, 3.0)
    ax.set_xticks(x)
    ax.set_xticklabels(["1990", "2000", "2008-12", "2019-23"], fontsize=11)
    ax.set_ylim(5, 36)
    ax.set_ylabel("Median county: % of adults with a bachelor's degree or higher", fontsize=11)
    ax.grid(axis="y", color="#e6e6e6", lw=0.8)
    ax.set_axisbelow(True)
    g90 = med.loc[1, "1990"] - med.loc[9, "1990"]
    g20 = med.loc[1, "2019-23"] - med.loc[9, "2019-23"]
    ax.annotate("", xy=(3.0, med.loc[1, "2019-23"]), xytext=(3.0, med.loc[9, "2019-23"]),
                arrowprops=dict(arrowstyle="<->", color=INK, lw=1))
    ax.text(2.97, (med.loc[1, "2019-23"] + med.loc[9, "2019-23"]) / 2 + 2.5,
            f"gap\n{g20:.0f} pts", ha="right", fontsize=9.5, color=INK, fontweight="bold")
    ax.text(0.03, med.loc[1, "1990"] + 1.8, f"gap {g90:.0f} pts", fontsize=9.5, color=INK, fontweight="bold")
    title(fig, "College education has grown everywhere, but big-metro counties pulled away from the most rural ones",
          "Median share of adults with a bachelor's degree or higher, by county type (USDA Rural-Urban Continuum Code, 2023)", size=15.5)
    caption(fig, f"Each line is the median county in one of the nine USDA Rural-Urban Continuum categories (blue = metropolitan, green/orange/brown = progressively more rural and remote). "
            f"Between 1990 and 2019-23 the median large-metro county went from {med.loc[1,'1990']:.0f}% to {med.loc[1,'2019-23']:.0f}%, while the median remote rural county went from {med.loc[9,'1990']:.0f}% to {med.loc[9,'2019-23']:.0f}%, "
            f"so the gap grew from {g90:.0f} to {g20:.0f} percentage points. Medians are over counties (not weighted by population); {len(d):,} counties with complete data. "
            "Source: USDA Economic Research Service county-level data (course file full_census_dataset.csv). Descriptive only; no causal claim.",
            width=135, y=0.015, size=9.2)
    fig.savefig(OUT / "q2a_education_lines.png", dpi=170)
    plt.close(fig)
    return med


def fig_2b(med):
    d = load_edu()
    rng = np.random.default_rng(765)
    fig, ax = plt.subplots(figsize=(13, 8.4))
    fig.subplots_adjust(left=0.07, right=0.985, top=0.84, bottom=0.22)
    off = 0.19
    for k in range(1, 10):
        for p, dx, col in (("1990", -off, "#9aa5b1"), ("2019-23", off, BLUE)):
            v = d.loc[d.rucc == k, p].values
            xs = k + dx + rng.uniform(-0.15, 0.15, len(v))
            ax.scatter(xs, v, s=4, color=col, alpha=0.28, lw=0, zorder=2, rasterized=True)
            q1, m, q3 = np.percentile(v, [25, 50, 75])
            ax.plot([k + dx] * 2, [q1, q3], color=INK, lw=3.2, zorder=4, solid_capstyle="butt")
            ax.plot([k + dx - 0.13, k + dx + 0.13], [m, m], color="white", lw=2.6, zorder=5)
            ax.plot([k + dx - 0.13, k + dx + 0.13], [m, m], color=INK, lw=1.2, zorder=6)
        ax.annotate("", xy=(k + off, med.loc[k, "2019-23"]), xytext=(k - off, med.loc[k, "1990"]),
                    arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.4), zorder=6)
    ax.axvspan(0.5, 3.5, color="#eef3f9", zorder=0)
    ax.text(2, 79, "Metropolitan counties", ha="center", fontsize=10.5, color="#2b4a6f", fontweight="bold")
    ax.text(6.5, 79, "Nonmetropolitan counties", ha="center", fontsize=10.5, color="#555555", fontweight="bold")
    ax.set_xlim(0.5, 9.5)
    ax.set_ylim(0, 84)
    ax.set_xticks(range(1, 10))
    ax.set_xticklabels(["1\nMetro\n1M+", "2\nMetro\n250k-1M", "3\nMetro\n<250k", "4\nUrban 20k+\nadjacent",
                        "5\nUrban 20k+\nnot adj.", "6\nUrban 5-20k\nadjacent", "7\nUrban 5-20k\nnot adj.",
                        "8\nRural <5k\nadjacent", "9\nRural <5k\nnot adj."], fontsize=8.8)
    ax.set_xlabel("USDA Rural-Urban Continuum Code (2023)", fontsize=10.5)
    ax.set_ylabel("% of adults with a bachelor's degree or higher", fontsize=11)
    ax.grid(axis="y", color="#e6e6e6", lw=0.8)
    ax.set_axisbelow(True)
    ax.legend(handles=[Line2D([], [], marker="o", color="none", markerfacecolor="#9aa5b1", ms=7, label="One county, 1990"),
                       Line2D([], [], marker="o", color="none", markerfacecolor=BLUE, ms=7, label="One county, 2019-23"),
                       Line2D([], [], color=INK, lw=3.2, label="Middle 50% of counties (bar) and median (tick)"),
                       Line2D([], [], color=ORANGE, lw=1.4, marker=">", ms=5, label="Shift of the median, 1990 to 2019-23")],
              loc="upper right", bbox_to_anchor=(0.995, 0.93), frameon=True, framealpha=0.95, fontsize=9, edgecolor="#cccccc")
    title(fig, "Every county type became more educated, but large-metro counties spread out far more than rural ones",
          "Distribution of county bachelor's-degree attainment, 1990 vs 2019-23, by rural-urban type", size=15)
    caption(fig, "Each dot is a county (3,100+ counties; horizontally jittered within its group). Grey = 1990, blue = 2019-23. In every category the whole distribution moves up, "
            "but the large-metro counties (code 1) also spread out, with a long upper tail of highly educated counties (up to about 65%), while remote rural counties (code 9) mostly cluster between 15% and 25%. "
            "Counties are grouped by their 2023 Rural-Urban Continuum Code. Source: USDA Economic Research Service county-level data (course file full_census_dataset.csv).",
            width=160, y=0.015, size=9.2)
    fig.savefig(OUT / "q2b_education_distributions.png", dpi=170)
    plt.close(fig)


# --------------------------------------------------------------------------
# Figure 3: gender gap scatter (World Bank)
# --------------------------------------------------------------------------
def fig_3():
    w = pd.read_csv(DATA / "lifespan_dataset_1960.csv").rename(
        columns={"Life Expectancy (years)": "LE", "Country Name": "C", "Country Code": "code"})
    o = load_owid()
    countries = set(o.Code.unique())
    w = w[w.code.isin(countries)]
    p = w.pivot_table(index=["C", "code", "Year"], columns="Sex", values="LE").reset_index()
    p["gap"] = p.Female - p.Male
    a = p[p.Year == 1960].set_index("C").gap
    b = p[p.Year == 2023].set_index("C").gap
    both = pd.concat([a.rename("g60"), b.rename("g23")], axis=1).dropna()
    both["chg"] = both.g23 - both.g60
    le23 = p[p.Year == 2023].set_index("C")[["Female", "Male"]].mean(axis=1).rename("le23")
    both = both.join(le23)
    fig, ax = plt.subplots(figsize=(11.5, 9.2))
    fig.subplots_adjust(left=0.08, right=0.93, top=0.86, bottom=0.2)
    sc = ax.scatter(both.g60, both.g23, c=both.le23, cmap="viridis", s=42, alpha=0.85,
                    edgecolor="white", lw=0.6, zorder=3, vmin=50, vmax=85)
    ax.plot([-5, 15], [-5, 15], color=GREY, lw=1.2, ls="--", zorder=1)
    ax.fill_between([-5, 15], [-5, 15], 15, color=ORANGE, alpha=0.05, zorder=0)
    ax.fill_between([-5, 15], -5, [-5, 15], color=BLUE, alpha=0.05, zorder=0)
    ax.text(-4.6, 13.3, "Women's advantage\nlarger in 2023 than in 1960", color=ORANGE, fontsize=10.5, fontweight="bold", va="top")
    ax.text(14.7, -0.8, "Women's advantage\nsmaller in 2023", color=BLUE, fontsize=10.5, fontweight="bold", ha="right")
    ax.text(10.9, 10.0, "no change", color=GREY, fontsize=9, rotation=40, ha="center")
    lab = ["Pakistan", "India", "Bangladesh", "Russian Federation", "Ukraine", "United States", "Kazakhstan",
           "Niger", "Mali", "Togo", "Cameroon", "Japan", "China", "Korea, Rep.", "Cameroon", "Nigeria", "Kuwait",
           "Chad", "Lithuania", "Belarus", "Sweden"]
    nm = {"Russian Federation": "Russia", "Korea, Rep.": "South Korea", "United States": "United States"}
    offs = {"Russian Federation": (6, -12), "Ukraine": (6, 4), "Kazakhstan": (-6, 6), "Cameroon": (6, 2),
            "Pakistan": (6, -2), "India": (6, -10), "Bangladesh": (-6, -12), "Niger": (6, 5), "Mali": (-6, -12),
            "Togo": (6, -10), "Chad": (6, 4), "Nigeria": (6, -10), "Kuwait": (-6, 6), "Japan": (6, -11),
            "China": (6, -11), "Korea, Rep.": (-6, 6), "United States": (6, -11), "Lithuania": (6, 4),
            "Belarus": (-6, -12), "Sweden": (6, 3)}
    for c in dict.fromkeys(lab):
        if c in both.index:
            r_ = both.loc[c]
            ox, oy = offs.get(c, (6, 3))
            ax.annotate(nm.get(c, c), (r_.g60, r_.g23), xytext=(ox, oy), textcoords="offset points", fontsize=8.8,
                        ha="left" if ox > 0 else "right", color=INK, zorder=5)
    ax.set_xlim(-5, 15)
    ax.set_ylim(-1, 15)
    ax.set_xlabel("Female minus male life expectancy in 1960 (years)", fontsize=11)
    ax.set_ylabel("Female minus male life expectancy in 2023 (years)", fontsize=11)
    ax.grid(color="#ececec", lw=0.8)
    ax.set_axisbelow(True)
    cb = fig.colorbar(sc, ax=ax, fraction=0.035, pad=0.015)
    cb.set_label("Average life expectancy in 2023 (years)", fontsize=10)
    n_up = int((both.chg > 0).sum())
    n_dn = int((both.chg < 0).sum())
    title(fig, "Women outlive men almost everywhere, but the size of that gap has been reshuffled since 1960",
          f"Gender gap in life expectancy at birth, 1960 vs 2023, for {len(both)} countries and territories", size=16)
    caption(fig, f"Each dot is a country; position is the female-minus-male gap in years. Dots above the dashed line have a larger female advantage in 2023 than in 1960 ({n_up} countries); "
            f"dots below it a smaller one ({n_dn}). Where the gap was negative in 1960 (Pakistan, India, Bangladesh) women have overtaken men; Ukraine and Russia have the largest gaps in 2023 (13 and 11 years), "
            "while the smallest are in Togo, Nigeria and the Gulf states (about 0.4-2 years). The U.S. gap shrank slightly (6.5 to 5.3 years). "
            "Source: World Bank life expectancy by sex (course file lifespan_dataset_1960.csv); aggregates such as regions and income groups removed.",
            width=150, y=0.015, size=9.2)
    fig.savefig(OUT / "q3_gender_gap_1960_vs_2023.png", dpi=170)
    plt.close(fig)
    return both


# --------------------------------------------------------------------------
# Figure 4: tile-grid map of domestic migration
# --------------------------------------------------------------------------
GRID = {
    "AK": (0, 0), "ME": (0, 10),
    "VT": (1, 9), "NH": (1, 10),
    "WA": (2, 0), "ID": (2, 1), "MT": (2, 2), "ND": (2, 3), "MN": (2, 4), "IL": (2, 5), "WI": (2, 6),
    "MI": (2, 7), "NY": (2, 8), "RI": (2, 9), "MA": (2, 10),
    "OR": (3, 0), "NV": (3, 1), "WY": (3, 2), "SD": (3, 3), "IA": (3, 4), "IN": (3, 5), "OH": (3, 6),
    "PA": (3, 7), "NJ": (3, 8), "CT": (3, 9),
    "CA": (4, 0), "UT": (4, 1), "CO": (4, 2), "NE": (4, 3), "MO": (4, 4), "KY": (4, 5), "WV": (4, 6),
    "VA": (4, 7), "MD": (4, 8), "DE": (4, 9),
    "AZ": (5, 1), "NM": (5, 2), "KS": (5, 3), "AR": (5, 4), "TN": (5, 5), "NC": (5, 6), "SC": (5, 7), "DC": (5, 8),
    "OK": (6, 3), "LA": (6, 4), "MS": (6, 5), "AL": (6, 6), "GA": (6, 7),
    "HI": (7, 0), "TX": (7, 3), "FL": (7, 8),
}


def fig_4():
    a = pd.read_csv(DATA / "aggregate_census_dataset.csv", sep="\t", encoding="latin-1")
    cols = ["Domestic Migration Rate 2021", "Domestic Migration Rate 2022", "Domestic Migration Rate 2023"]
    m = a.set_index("State")[cols]
    fig = plt.figure(figsize=(14, 10.3))
    ax = fig.add_axes([0.03, 0.12, 0.94, 0.70])
    ax.set_xlim(-0.1, 11.1)
    ax.set_ylim(8.1, -0.15)
    ax.axis("off")
    vmax = 28
    for st, (r_, c_) in GRID.items():
        v = m.loc[st].values
        x0, y0 = c_ + 0.04, r_ + 0.04
        w_, h_ = 0.92, 0.92
        tot = np.nanmean(v)
        bg = "#e8f4f2" if tot > 3 else ("#fbeadd" if tot < -3 else "#f5f5f5")
        ax.add_patch(plt.Rectangle((x0, y0), w_, h_, facecolor=bg, edgecolor="#d0d0d0", lw=0.6))
        base = y0 + 0.62
        sc_ = 0.38 / vmax
        for i, val in enumerate(v):
            bx = x0 + 0.10 + i * 0.27
            hgt = val * sc_
            ax.add_patch(plt.Rectangle((bx, base - max(hgt, 0)), 0.2, abs(hgt),
                                       facecolor=TEAL if val >= 0 else ORANGE, edgecolor="none"))
        ax.plot([x0 + 0.06, x0 + w_ - 0.06], [base, base], color="#666666", lw=0.6)
        ax.text(x0 + 0.06, y0 + 0.14, st, fontsize=11, fontweight="bold", color=INK, va="center")
        ax.text(x0 + w_ - 0.06, y0 + 0.14, (f"{tot:+.0f}" if round(tot) else "0"), fontsize=8.8, color=TEAL if tot > 0 else ORANGE,
                va="center", ha="right", fontweight="bold")
    # key tile
    kx, ky = 0.2, 0.2
    ax.text(4.3, 0.12, "How to read a tile", fontsize=10.5, fontweight="bold", va="center")
    ax.text(4.3, 0.42, "Three bars = 2021, 2022, 2023 (left to right).\nBar up (teal) = more people moved in from other states than left;\nbar down (orange) = more left than arrived. Number = 3-year average.",
            fontsize=9, va="top", color="#333333", linespacing=1.4)
    ax.text(4.3, 1.35, "Net domestic migration per 1,000 residents per year", fontsize=9, va="top", color="#333333")
    title(fig, "The pandemic-era boom in the Mountain West faded by 2023, while the Southeast kept growing and NY, CA and IL kept losing people",
          "Net domestic migration (moves between U.S. states) per 1,000 residents, by state, 2021-2023", size=15.5)
    # highlight notes
    ax.text(0.0, 8.05, "", fontsize=1)
    caption(fig, "Each tile is a state placed roughly where it sits on the map (Puerto Rico omitted; no domestic-migration estimates). "
            "Idaho (+28 per 1,000 in 2021) and Montana, Utah, Nevada, Arizona and Maine started the period with big gains that shrank each year; "
            "South Carolina, North Carolina, Tennessee and Delaware stayed strongly positive in all three years, and New York has been about -11 to -15 every year. "
            "Rates are the USDA/Census Bureau estimates for July-June years ending in 2021, 2022, 2023, scaled identically in every tile. "
            "Source: USDA Economic Research Service state-level data (course file aggregate_census_dataset.csv).",
            width=165, y=0.02, size=9.2)
    fig.savefig(OUT / "q4_migration_tile_map.png", dpi=170)
    plt.close(fig)
    return m


if __name__ == "__main__":
    r = fig_1a()
    print(r.round(1).to_string())
    fig_1b(r)
    med = fig_2a()
    print(med.round(1))
    fig_2b(med)
    both = fig_3()
    print(both.chg.describe())
    fig_4()
