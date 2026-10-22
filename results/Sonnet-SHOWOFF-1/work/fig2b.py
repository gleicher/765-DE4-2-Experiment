from common import *
c = edu_counties()
rng = np.random.default_rng(7)
fig, ax = plt.subplots(figsize=(12, 8.2))
fig.subplots_adjust(left=0.07, right=0.97, top=0.80, bottom=0.30)
off = {1970: -0.2, 2021: 0.2}
for i, k in enumerate(GRP_LABEL):
    for y in (1970, 2021):
        d = c[c.grp == k][f"pct{y}"].dropna()
        x = i + off[y] + rng.uniform(-0.13, 0.13, len(d))
        col = GRP_COLOR[k]
        ax.scatter(x, d, s=7, color=col, alpha=0.16 if y == 1970 else 0.38, lw=0, zorder=2)
        q1, md, q3 = d.quantile([.25, .5, .75])
        ax.plot([i + off[y]]*2, [q1, q3], color=INK if y == 2021 else MUTED, lw=5, solid_capstyle="butt", alpha=0.85, zorder=4)
        ax.plot([i + off[y] - 0.15, i + off[y] + 0.15], [md, md], color="white", lw=2.2, zorder=5)
        ax.text(i + off[y], 74 if y == 2021 else 74, "", )
        ax.text(i + off[y] + 0.17, md, f"{md:.0f}%", fontsize=10, fontweight="bold", color=INK if y == 2021 else MUTED, va="center", zorder=6)
        ax.text(i + off[y], -3.2, str(y if y == 1970 else "2019-23"), ha="center", fontsize=9.5, color=MUTED)
    n = c[c.grp == k]["pct2021"].notna().sum()
    ax.text(i, -8.0, GRP_SHORT[k] + f"\n{n} counties", ha="center", va="top", fontsize=10, fontweight="bold", color=GRP_COLOR[k], linespacing=1.3)
# call out highest rural county
r = c[c.grp == "rural"].dropna(subset=["pct2021"]).sort_values("pct2021").iloc[-1]
ax.annotate(f"{r['Area name']}, {r['State']}: {r['pct2021']:.0f}%\\n(the most-educated rural county, above most metros)".replace("\\n", "\n"),
            xy=(3.2, r["pct2021"]), xytext=(1.85, 66), fontsize=9.5, color=GRP_COLOR["rural"],
            arrowprops=dict(arrowstyle="-", color=GRP_COLOR["rural"], lw=0.9), va="center", zorder=6)
lowm = c[c.grp == "metro"].dropna(subset=["pct2021"]).sort_values("pct2021").iloc[0]
ax.annotate(f"Lowest metro: {lowm['Area name']}, {lowm['State']}: {lowm['pct2021']:.0f}%", xy=(0.2, lowm["pct2021"]), xytext=(0.35, 3),
            fontsize=9.5, color=GRP_COLOR["metro"], arrowprops=dict(arrowstyle="-", color=GRP_COLOR["metro"], lw=0.9), va="center", zorder=6)
ax.set_xlim(-0.55, 3.55); ax.set_ylim(0, 80)
ax.set_xticks([]); ax.set_yticks(range(0, 81, 20)); ax.set_yticklabels([f"{v}%" for v in range(0, 81, 20)])
ax.grid(axis="y", color=GRID, lw=0.7); ax.set_axisbelow(True); ax.tick_params(length=0); ax.spines["bottom"].set_visible(False); ax.spines["left"].set_visible(False)
ax.set_ylabel("Adults in the county with a bachelor's degree or higher", fontsize=11)
frame(fig, "Behind the averages: the typical rural county trails the typical metro county\nby 8 points, and the two groups overlap heavily",
      "Each dot is one U.S. county. Left (faint) dots: 1970. Right (darker) dots: 2019-23. Bar = middle 50% of counties; white tick and number = median county.",
      caption=("Every county type shifted up, but metro counties are the most spread out, from 10% to 77%, while the most-rural counties are the most tightly bunched. Medians differ by 8 points here vs. 18 points\nin the pooled chart because big, highly educated metros hold most of the adults.\n"
               "Unweighted: every county counts once regardless of population, so this view shows the typical county rather than the typical resident (compare with the line chart of pooled shares).\n"
               "County type = USDA 2023 Rural-Urban Continuum Code. 1970 counts 'four years of college or more'; 2019-23 counts 'bachelor's degree or higher'. Counties without a code excluded."),
      source="Data: USDA Economic Research Service county-level education files, via course file full_census_dataset.csv.", top=0.985)
save(fig, "q2_fig2_education_county_distributions.png")
