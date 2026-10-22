from common import *
c = edu_counties(); t = edu_weighted(c)
yrs = list(t.columns)
fig, ax = plt.subplots(figsize=(12, 8.2))
fig.subplots_adjust(left=0.07, right=0.80, top=0.80, bottom=0.2)
ly = dict(zip(GRP_LABEL, spread([t.loc[k, 2021] for k in GRP_LABEL], 3.6)))
for k in GRP_LABEL:
    ax.plot(yrs, t.loc[k], color=GRP_COLOR[k], lw=3.2, marker="o", ms=7, zorder=3)
    ax.text(2021 + 1.2, ly[k], f"{GRP_SHORT[k]}\n{t.loc[k,2021]:.0f}% in 2019-23", color=GRP_COLOR[k], fontsize=10.5, fontweight="bold", va="center")
    ax.text(1970 - 0.8, t.loc[k, 1970], f"{t.loc[k,1970]:.0f}%", color=GRP_COLOR[k], fontsize=10, ha="right", va="center", fontweight="bold")
# gap brackets
for yr, dx in [(1970, 0), (2021, 0)]:
    lo, hi = t.loc["rural", yr], t.loc["metro", yr]
    xb = yr + (-4.2 if yr == 1970 else 0.9) if False else None
ax.annotate("", xy=(1970, t.loc["metro", 1970]), xytext=(1970, t.loc["rural", 1970]), arrowprops=dict(arrowstyle="<->", color=INK, lw=1.0), zorder=1)
ax.annotate("", xy=(2021, t.loc["metro", 2021]), xytext=(2021, t.loc["rural", 2021]), arrowprops=dict(arrowstyle="<->", color=INK, lw=1.0), zorder=1)
g70 = t.loc["metro", 1970] - t.loc["rural", 1970]; g21 = t.loc["metro", 2021] - t.loc["rural", 2021]
ax.text(1971.3, (t.loc["metro",1970]+t.loc["rural",1970])/2 + 2.6, f"Gap: {g70:.0f} pts", fontsize=10.5, fontweight="bold", color=INK)
ax.text(2019.7, 27.8, f"Gap: {g21:.0f} pts", fontsize=10.5, fontweight="bold", color=INK, ha="right")
# rural-today = metro-in-1980s guide
ax.hlines(t.loc["rural", 2021], 1978, 2021, color=GRP_COLOR["rural"], lw=1, ls=(0, (3, 3)), zorder=2)
ax.annotate("Rural counties in 2019-23 (19%) have just reached\nthe level metro counties had around 1984",
            xy=(1984, t.loc["rural", 2021]), xytext=(1990.5, 7.5), fontsize=10, color=GRP_COLOR["rural"],
            arrowprops=dict(arrowstyle="->", color=GRP_COLOR["rural"], lw=1), va="center")
ax.set_xlim(1964, 2021); ax.set_ylim(0, 40)
ax.set_xticks(yrs); ax.set_xticklabels(["1970", "1980", "1990", "2000", "2008-12", "2019-23"], fontsize=10.5)
ax.set_yticks(range(0, 41, 10)); ax.set_yticklabels([f"{v}%" for v in range(0, 41, 10)])
ax.grid(axis="y", color=GRID, lw=0.7); ax.set_axisbelow(True); ax.tick_params(length=0); ax.spines["left"].set_visible(False)
ax.set_ylabel("Adults with a bachelor's degree or higher", fontsize=11)
frame(fig, "Everyone is getting more college-educated, but the\nmetro-rural education gap has tripled since 1970",
      "Share of adults with a 4-year college degree or more, by county type, 1970-2023 (all U.S. counties, pooled within each type)",
      caption=("Each line pools all counties of a type: total degree holders divided by total adults, so large counties count in proportion to their adults.\n"
               "County type is the USDA 2023 Rural-Urban Continuum Code, grouped into four levels. 1970 and 1980 count adults with \"four years of college or more\";\n"
               "later years count \"bachelor's degree or higher\" (a nearly identical but not strictly identical definition). Years after 2000 are survey estimates (ACS 5-year).\n"
               "Counties without a 2023 code (e.g., Connecticut's planning regions, Puerto Rico) are excluded."),
      source="Data: USDA Economic Research Service county-level education files, via course file full_census_dataset.csv.", top=0.985)
save(fig, "q2_fig1_education_gap_lines.png")
