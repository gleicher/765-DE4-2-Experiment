from common import *
w = life_wide()
p = w.pivot(index="Country Code", columns="Year", values="Both")
nm = w.drop_duplicates("Country Code").set_index("Country Code")["Country Name"]
d = pd.DataFrame({"name": nm, "y19": p[2019], "y21": p[2021], "y23": p[2023]}).dropna()
d = d.drop(index=["CAF"])  # implausible 2019->2023 jump (+26 yrs) looks like a data artifact
d["dx"] = d.y21 - d.y19; d["dy"] = d.y23 - d.y21
fig, ax = plt.subplots(figsize=(12, 9))
fig.subplots_adjust(left=0.08, right=0.87, top=0.83, bottom=0.2)
xs = np.linspace(-7.5, 1.5, 10)
ax.plot(xs, -xs, color=INK, lw=1.3, zorder=2)
ax.fill_between(xs, -xs, 9, color="#2166ac", alpha=0.06, zorder=0)
ax.fill_between(xs, -xs, -11, color="#b2182b", alpha=0.06, zorder=0)
sc = ax.scatter(d.dx, d.dy, c=d.y19, cmap="viridis_r", s=48, edgecolor="white", lw=0.6, zorder=3, vmin=55, vmax=85)
cb = fig.colorbar(sc, ax=ax, fraction=0.03, pad=0.02); cb.set_label("Life expectancy in 2019 (years)", fontsize=10.5); cb.outline.set_visible(False)
lab = dict(BOL="Bolivia", MEX="Mexico", PER="Peru", IND="India", USA="United States", RUS="Russia",
           DEU="Germany", JPN="Japan", CHN="China", PSE="West Bank & Gaza", LBY="Libya", BRA="Brazil", SLE="Sierra Leone")
offs = dict(BOL=(0.3, 0.2), PSE=(0.3, 0.0), LBY=(0.3, -0.3), USA=(-0.3, -0.9), JPN=(0.3, -0.7), CHN=(0.4, 0.5), DEU=(-0.2,-0.8), BRA=(-0.4,-0.5), RUS=(0.3,0.9), IND=(-0.2,0.8), MEX=(-0.3,0.4), PER=(-0.2,0.5), SLE=(0.3,0.5))
for k, t in lab.items():
    if k in d.index:
        dx, dy = offs.get(k, (0.12, 0.25))
        ax.annotate(t, (d.dx[k], d.dy[k]), xytext=(d.dx[k] + dx, d.dy[k] + dy), fontsize=9, color=INK, ha="left" if dx > 0 else "right",
                    va="center", arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.5), zorder=6)
ax.axvline(0, color=MUTED, lw=0.7); ax.axhline(0, color=MUTED, lw=0.7)
ax.set_xlim(-7.3, 1.8); ax.set_ylim(-9.6, 8.6)
ax.set_xlabel("Change in life expectancy during the pandemic, 2019 to 2021 (years)", fontsize=11)
ax.set_ylabel("Change afterwards, 2021 to 2023 (years)", fontsize=11)
ax.grid(color=GRID, lw=0.6); ax.set_axisbelow(True); ax.tick_params(length=0)
ax.text(-2.4, 8.3, "Above the line: regained more than it lost,\nso above the 2019 level in 2023", fontsize=10, color="#2166ac", fontweight="bold", va="top")
ax.text(-7.1, -5.0, "Below the line: 2023 still lower than 2019", fontsize=10, color="#b2182b", fontweight="bold")
n_above = int(((d.dy + d.dx) > 0).sum()); n_below = len(d) - n_above
tot = len(d)
frame(fig, "COVID cost Latin American countries the most years of life; most countries\nhave since regained them, but 31 are still below their 2019 level",
      f"Each dot is a country (n = {tot}). Horizontal: years of life expectancy lost 2019-2021. Vertical: years regained 2021-2023.\nBlack line = full recovery (2023 level equals 2019 level).",
      caption=(f"Black line = a country that has exactly regained its 2019 life expectancy; {n_above} countries finished above it by 2023, {n_below} below. Left of zero = life expectancy fell 2019-21 (182 of {tot}).\n"
               "Colour shows 2019 life expectancy. The biggest losses (Bolivia, Paraguay, Mexico, Guyana, Peru) were in countries with mid-range life expectancy (about 65-77 years);\n"
               "the lowest-life-expectancy countries (yellow) mostly changed little. Places in conflict (West Bank and Gaza, Libya) sit far below the line for reasons unrelated to the pandemic.\n"
               "Central African Republic omitted: its reported 2019-2023 gain of 26 years is implausible and probably a data artifact. Aggregates excluded. Both sexes combined."),
      source="Data: World Bank life expectancy at birth (SP.DYN.LE00.IN), course file lifespan_dataset_1960.csv.", top=0.985)
save(fig, "q3_fig1_covid_loss_recovery.png")
print(n_above, n_below, (d.dx<0).sum(), d.sort_values('dx').head(5)[['name','dx','dy']])
