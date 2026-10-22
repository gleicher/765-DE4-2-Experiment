"""Story 2, primary: unemployment rate by rural-urban group, 2000-2023, plus the big-metro minus rural difference."""
from common import *

c = load_counties()
years = list(range(2000, 2024))
g = c.groupby("rgroup", observed=True)
rate = pd.DataFrame({y: 100 * g[f"Unemployed {y}"].sum() / g[f"Civilian labor force {y}"].sum() for y in years})
rate.to_csv(Path(__file__).parent / "q2_unemployment_by_group.csv")
groups = list(rate.index)
cols = dict(zip(groups, SEQ[::-1]))  # large metro darkest, most rural lightest
ncount = g.size()

fig = plt.figure(figsize=(10, 8))
ax = fig.add_axes([0.08, 0.40, 0.66, 0.47])
ax2 = fig.add_axes([0.08, 0.17, 0.66, 0.16], sharex=ax)

for a in (ax, ax2):
    for x0, x1, lab in [(2007.9, 2010.1, "Great Recession"), (2019.9, 2021.1, "COVID-19")]:
        a.axvspan(x0, x1, color="#f1f0ec", lw=0, zorder=0)
for x, lab in [(2009, "Great Recession"), (2020.5, "COVID-19\npandemic")]:
    ax.text(x, 10.9, lab, ha="center", va="top", fontsize=8.5, color=INK2)

# draw rural first so the large-metro line sits on top
for grp in groups[::-1]:
    ax.plot(years, rate.loc[grp], color=cols[grp], lw=2.2 if grp in (groups[0], groups[-1]) else 1.6, zorder=3)
label_y = {groups[0]: 9.0, groups[1]: 8.1, groups[2]: 7.2, groups[3]: 6.3, groups[4]: 5.4}
for grp in groups:
    ax.plot([2020.15, 2021.4], [rate.loc[grp, 2020], label_y[grp]], color=cols[grp], lw=0.8)
    ax.text(2021.5, label_y[grp], f"{grp}\n{ncount[grp]} counties", va="center", fontsize=8.8, linespacing=1.1, color=INK,
            fontweight="bold" if grp in (groups[0], groups[-1]) else "normal")
ax.set_ylim(2.5, 11)
ax.set_ylabel("Unemployment rate (%)")
ax.text(2000.2, 3.0, "Before 2020, the most rural counties (light) always had\nhigher unemployment than the largest metros (dark).",
        fontsize=8.5, color=INK2, va="bottom")
ax.tick_params(labelbottom=False)

diff = rate.loc[groups[0]] - rate.loc[groups[-1]]
ax2.axhline(0, color=INK2, lw=1)
ax2.bar(years, diff, width=0.7, color=[cols[groups[0]] if v > 0 else cols[groups[-1]] for v in diff], zorder=3)
ax2.set_ylim(-1.3, 2.4)
ax2.set_yticks([-1, 0, 1, 2])
ax2.set_ylabel("Gap (points)")
ax2.text(2021.5, 1.6, "Large metros worse\n(+2.0 points in 2020)", fontsize=8.5, color=INK, va="center")
ax2.text(2022, 0.25, "≈ 0", fontsize=8.5, color=INK2, ha="center")
ax2.text(2021.5, -0.8, "Rural worse", fontsize=8.5, color=INK, va="center")
ax2.set_title("Large-metro rate minus most-rural rate", loc="left", fontsize=9.5, color=INK, pad=4)
ax2.set_xlim(1999.5, 2023.5)
ax2.set_xticks(range(2000, 2024, 2))

title_block(fig, "The pandemic flipped America's rural–urban unemployment gap — for two years",
            "Unemployment rate by type of county, 2000–2023 (all unemployed ÷ all labor force in each group of counties)",
            gap=0.05)
caption(fig, "For two decades — even in the Great Recession, when all groups rose to about 10% — the most rural counties had higher\n"
             "unemployment than the large metros (bottom panel below zero). In 2020 the order reversed exactly: the more urban the county, the larger the spike\n"
             "(large metros 3.5% → 8.6%, most rural 4.2% → 6.5%). Large metros were still worse in 2021; by 2022 all five groups were at 3.6–3.7%.\n"
             "Groups use the USDA 2023 Rural-Urban Continuum Codes: 1 | 2–3 | 4–5 | 6–7 | 8–9. 50 states + DC (Connecticut: its 8 former counties, 2013 codes).\n"
             "Data: USDA ERS county-level data sets (unemployment from BLS LAUS), via CS765 765Data repository.")
save(fig, "q2a_unemployment_rural_urban_lines.png")
