"""Figure 3: the urban-rural gap closed for high-school completion but widened for college degrees."""
import pandas as pd
import matplotlib.pyplot as plt
from common import setup_style, FIG, INTER, INK, INK2, MUTED, BLUE_RAMP, ORANGE
from common import census

setup_style()
d = census().dropna(subset=["rucc"])
GROUP = {1: "Large metro (1M+)", 2: "Smaller metro", 3: "Smaller metro",
         4: "Nonmetro, town 5k+", 5: "Nonmetro, town 5k+", 6: "Nonmetro, town 5k+", 7: "Nonmetro, town 5k+",
         8: "Rural (no town of 5k)", 9: "Rural (no town of 5k)"}
ORDER = ["Large metro (1M+)", "Smaller metro", "Nonmetro, town 5k+", "Rural (no town of 5k)"]
COLORS = dict(zip(ORDER, BLUE_RAMP[::-1]))  # darkest = most urban
d["grp"] = d.rucc.astype(int).map(GROUP)

PERIODS = {"1970": 1970, "1980": 1980, "1990": 1990, "2000": 2000, "2008-12": 2010, "2019-23": 2021}
rows = []
for p, x in PERIODS.items():
    if p in ("1970", "1980"):
        ba, sc = f"Four years of college or higher, {p}", f"Some college (1-3 years), {p}"
    else:
        ba, sc = f"Bachelor's degree or higher, {p}", f"Some college or associate degree, {p}"
    hs, lt = f"High school graduate (or equivalency), {p}", f"Less than high school graduate, {p}"
    sub = d.dropna(subset=[ba, sc, hs, lt])
    g = sub.groupby("grp")
    tot = g[ba].sum() + g[sc].sum() + g[hs].sum() + g[lt].sum()
    for k in ORDER:
        rows.append(dict(grp=k, period=p, x=x, ba=g[ba].sum()[k] / tot[k] * 100,
                         lths=g[lt].sum()[k] / tot[k] * 100))
t = pd.DataFrame(rows)
t.to_csv(INTER / "q3_education_by_group.csv", index=False)

fig, axes = plt.subplots(1, 2, figsize=(11.5, 6.6), sharey=True)
panels = [("lths", "Adults (25+) without a high-school diploma", axes[0]),
          ("ba", "Adults (25+) with a bachelor's degree or more", axes[1])]
for var, ttl, ax in panels:
    top = t[t.grp == ORDER[0]].set_index("x")[var]
    bot = t[t.grp == ORDER[-1]].set_index("x")[var]
    ax.fill_between(top.index, top.values, bot.values, color=ORANGE, alpha=0.10, lw=0)
    for k in ORDER:
        s = t[t.grp == k]
        ax.plot(s.x, s[var], color=COLORS[k], lw=2.2, marker="o", ms=4.5, mec="white", mew=0.8)
    # gap annotations at the two ends
    for x, ha, dx in [(1970, "right", -1.2), (2021, "left", 1.2)]:
        a, b = top[x], bot[x]
        ax.annotate("", xy=(x + dx * 0.6, a), xytext=(x + dx * 0.6, b),
                    arrowprops=dict(arrowstyle="<->", color=ORANGE, lw=1.2, shrinkA=0, shrinkB=0))
        ax.text(x + dx * 1.3, (a + b) / 2, f"gap\n{abs(a-b):.0f} pts", ha=ha, va="center",
                fontsize=9, color="#b8461a", fontweight="bold", linespacing=1.0)
    ax.set_title(ttl, loc="left", fontsize=11.5, fontweight="bold", pad=8)
    ax.set_xlim(1961, 2030)
    ax.set_xticks(list(PERIODS.values()), ["1970", "1980", "1990", "2000", "2008–\n12", "2019–\n23"])
    ax.set_ylim(0, 65)
    ax.yaxis.set_major_formatter(lambda v, _: f"{v:.0f}%")
    ax.grid(axis="x", visible=False)

# direct labels (right panel, at the 2019-23 end; left panel at 1970)
lab_y_r = {ORDER[0]: 40.5, ORDER[1]: 32.5, ORDER[2]: 23.6, ORDER[3]: 18.3}
lab_y_l = {ORDER[0]: 44.0, ORDER[1]: 48.7, ORDER[2]: 53.6, ORDER[3]: 61.5}
for k in ORDER:
    axes[1].plot([2027.3, 2030.3], [lab_y_r[k]] * 2, color=COLORS[k], lw=3, clip_on=False,
                 solid_capstyle="round")
    axes[1].text(2031.3, lab_y_r[k], k.replace(" (", "\n("), fontsize=8.8, color=INK,
                 va="center", ha="left", linespacing=1.0, clip_on=False)
axes[1].set_xlim(1961, 2027)
axes[0].set_ylabel("Share of adults 25 and older")
axes[0].text(1990.5, 52, "Rural counties had far more adults\nwithout a diploma in 1970 — by\n2019–23 they had almost caught up",
             fontsize=9, color=INK2, va="top")
axes[1].text(1971, 50, "Meanwhile the college gap tripled:\nbig metros pulled far ahead",
             fontsize=9, color=INK2, va="top")

fig.suptitle("Rural America caught up on high school, but fell further behind on college",
             x=0.01, ha="left", y=0.985, fontsize=15.5, fontweight="bold")
fig.text(0.01, 0.93,
         "Educational attainment of adults by county type, 1970 to 2019–23. The shaded band is the gap between the most urban and most rural\n"
         "counties: it shrank from 16 to 2 percentage points for lacking a diploma, but grew from 7 to 21 points for holding a college degree.",
         fontsize=10, color=INK2, ha="left", va="top")
fig.text(0.01, 0.012,
         "County types use the USDA 2023 Rural-Urban Continuum Code for every year (1 = large metro; 2–3 = smaller metro; 4–7 = nonmetro with an urban\n"
         "population of 5,000+; 8–9 = nonmetro with less). Shares are population-weighted. 1970/1980 'college' = four or more years of college. 2008–12 and\n"
         "2019–23 are 5-year survey averages, plotted at their midpoints. 50 states + DC. Data: USDA ERS county-level education data (CS765 census dataset).",
         fontsize=8.2, color=MUTED, ha="left", va="bottom")
fig.subplots_adjust(left=0.07, right=0.875, top=0.80, bottom=0.15, wspace=0.12)
fig.savefig(FIG / "q3_education_urban_rural_gaps.png")
print(t.round(1).pivot(index="grp", columns="period", values=["lths", "ba"]).to_string())
