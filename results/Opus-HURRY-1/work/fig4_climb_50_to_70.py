"""Story 4: how long did it take each country to go from life expectancy 50 to 70? (OWID long-run data)"""
from common import *

o = pd.read_csv(DATA / "life-expectancy-owid" / "life-expectancy-owid.csv")
o.columns = ["entity", "code", "year", "lex"]
# keep countries: rows with an ISO code (OWID_ codes are aggregates/historical, except Kosovo)
o = o[o.code.notna() & (~o.code.astype(str).str.startswith("OWID") | (o.entity == "Kosovo"))]


def crossing(d, thr):
    """First year life expectancy reaches thr, linearly interpolated between observations."""
    d = d.sort_values("year")
    above = np.where(d.lex.values >= thr)[0]
    if len(above) == 0:
        return np.nan
    i = above[0]
    if i == 0:
        return np.nan  # already above at first observation
    y0, y1 = d.year.values[i - 1], d.year.values[i]
    l0, l1 = d.lex.values[i - 1], d.lex.values[i]
    return y0 + (thr - l0) / (l1 - l0) * (y1 - y0)


rows = []
for e, d in o.groupby("entity"):
    rows.append((e, d.year.min(), crossing(d, 50), crossing(d, 70), d.sort_values("year").lex.iloc[-1]))
r = pd.DataFrame(rows, columns=["entity", "first_year", "t50", "t70", "le_2023"]).dropna(subset=["t50"])
r["reached"] = r.t70.notna()
r["years"] = np.where(r.reached, r.t70 - r.t50, 2023 - r.t50)
r.to_csv(Path(__file__).parent / "q4_climb_50_to_70.csv", index=False)
print(len(r), r.reached.sum())

fig = plt.figure(figsize=(10, 8))
ax = fig.add_axes([0.08, 0.2, 0.86, 0.64])
done, wait = r[r.reached], r[~r.reached]
ax.scatter(done.t50, done.years, s=28, color=BLUE, lw=0.8, edgecolors="white", zorder=3,
           label=f"Reached 70 ({len(done)} countries): years from 50 to 70")
ax.scatter(wait.t50, wait.years, s=34, marker="^", facecolors="none", edgecolors=ORANGE, lw=1.3, zorder=3,
           label=f"Not yet at 70 ({len(wait)} countries): years spent climbing so far")
# the 'no later than 2023' frontier for countries that have not arrived
xs = np.array([1940, 2015])
ax.plot(xs, 2023 - xs, color=ORANGE, lw=0.9, ls=(0, (4, 3)), zorder=2)
ax.text(1987, 72, "Dashed line = 2023.\nCountries still\nclimbing sit on it.", fontsize=8.5, color=INK2, ha="left", va="center")

def lab(name, dx, dy, ha="left"):
    rr = r[r.entity == name].iloc[0]
    ax.annotate(f"{name} {rr.years:.0f}", (rr.t50, rr.years), (rr.t50 + dx, rr.years + dy), fontsize=8.5,
                color=INK, ha=ha, va="center", arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7, shrinkB=3))

for name, dx, dy, ha in [("Norway", 4, 4, "left"), ("Sweden", 6, 2, "left"), ("United States", 4, 7, "left"),
                         ("Hungary", 5, 4, "left"), ("Japan", 2, -10, "left"), ("Belarus", -2, -8, "right"),
                         ("South Korea", -6, -9, "right"), ("China", 3, -9, "left"), ("India", 2, 10, "left"),
                         ("Oman", 3, -7, "left"), ("Philippines", -4, 8, "right"), ("Nigeria", 2, 8, "left"),
                         ("Kenya", -4, 7, "right"), ("Bangladesh", 6, -9, "left")]:
    lab(name, dx, dy, ha)

ax.set_xlim(1845, 2015)
ax.set_ylim(0, 100)
ax.set_xlabel("Year the country's life expectancy first reached 50")
ax.set_ylabel("Years to climb from 50 to 70")
ax.legend(loc="upper right", fontsize=9, handletextpad=0.4)
ax.text(1848, 6, "Reached 50 before 1925: the climb to 70 took 36–93 years.\nReached 50 in 1940–1975: as little as 17–25 years.",
        fontsize=8.5, color=INK2, va="bottom")

title_block(fig, "The climb from 50 to 70 years of life expectancy got faster for some latecomers —\nand has stalled for others",
            "Each mark is a country: when its life expectancy at birth first reached 50 (x), and how many years it took to reach 70 (y)", gap=0.085)
caption(fig, "Norway, the first country to reach 50 (around 1854), needed 93 years to reach 70; before 1925, no country made the climb in under 35 years.\n"
             "Mid-century climbers set the records: Japan (reached 50 in 1947) took 17 years, Oman 19. But speed was not guaranteed: many countries that\n"
             "reached 50 in the 1950s–60s are still below 70 (Kenya: 61 years and counting, about as long as Sweden needed), and only 6 of the 45 countries that\n"
             "reached 50 after 1975 have reached 70; the rest are mostly in sub-Saharan Africa, where HIV/AIDS reversed gains in the 1990s. Crossing years are\n"
             f"interpolated between observations; early series are sparse, so pre-1900 years are approximate. {len(r)} countries whose first recorded value was below 50.\n"
             "Data: Our World in Data, long-run life expectancy (Riley 2005; Zijdeman et al. 2015; HMD 2024; UN WPP 2024), via CS765 765Data repository.")
save(fig, "q4_climb_50_to_70.png")
