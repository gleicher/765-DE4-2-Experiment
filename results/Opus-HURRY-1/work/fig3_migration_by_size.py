"""Story 3: net domestic vs international migration (mid-2020 to mid-2023) by county population size."""
from common import *

c = load_counties()
c["pop"] = c["Population Estimate 2020"]
c = c[c["pop"] > 0].copy()
yrs = [2021, 2022, 2023]  # each "year" runs July 1 of the prior year to June 30
c["dom"] = c[[f"Domestic migration {y}" for y in yrs]].sum(axis=1)
c["intl"] = c[[f"International Migration {y}" for y in yrs]].sum(axis=1)

bins = [0, 1e4, 2.5e4, 5e4, 1e5, 2.5e5, 5e5, 1e6, 2e6, 1.1e7]
labels = ["Under 10k", "10k–25k", "25k–50k", "50k–100k", "100k–250k", "250k–500k", "500k–1M", "1M–2M", "2M+"]
c["size"] = pd.cut(c["pop"], bins, labels=labels)
g = c.groupby("size", observed=True)
t = pd.DataFrame({"counties": g.size(), "pop": g["pop"].sum(), "dom": g.dom.sum(), "intl": g.intl.sum()})
t["dom_rate"] = 100 * t.dom / t["pop"]
t["intl_rate"] = 100 * t.intl / t["pop"]
t.to_csv(Path(__file__).parent / "q3_migration_by_size.csv")

fig = plt.figure(figsize=(10, 7.6))
ax = fig.add_axes([0.17, 0.2, 0.53, 0.6])
y = np.arange(len(t))[::-1]
h = 0.36
ax.barh(y + h / 2 + 0.02, t.dom / 1e6, height=h, color=ORANGE, zorder=3, label="Domestic (moved from/to another U.S. county)")
ax.barh(y - h / 2 - 0.02, t.intl / 1e6, height=h, color=BLUE, zorder=3, label="International (moved from/to abroad)")
ax.axvline(0, color=INK2, lw=1, zorder=4)
ax.set_yticks(y)
ax.set_yticklabels([f"{l}" for l in t.index], fontsize=10, color=INK)
ax.set_ylabel("County population in 2020", fontsize=10)
ax.grid(axis="y", visible=False)
ax.set_xlim(-1.85, 1.45)
ax.set_xlabel("Net migrants, July 2020 – June 2023 (millions of people)")
ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:+.1f}" if v else "0"))

for yi, (_, r) in zip(y, t.iterrows()):
    for val, off in [(r.dom, h / 2 + 0.02), (r.intl, -h / 2 - 0.02)]:
        txt = f"{val/1e3:+,.0f}k"
        ax.text(val / 1e6 + (0.03 if val >= 0 else -0.03), yi + off, txt, va="center",
                ha="left" if val >= 0 else "right", fontsize=8.3, color=INK)

# right-hand table: counties and per-100-resident rates
tx = 1.02
ax.text(tx, 1.02, "Counties", transform=ax.transAxes, fontsize=8.5, color=INK2, ha="left", va="bottom", fontweight="bold")
ax.text(tx + 0.13, 1.02, "Domestic\nper 100", transform=ax.transAxes, fontsize=8.5, color=INK2, ha="left", va="bottom", fontweight="bold")
ax.text(tx + 0.29, 1.02, "Intl.\nper 100", transform=ax.transAxes, fontsize=8.5, color=INK2, ha="left", va="bottom", fontweight="bold")
for yi, (_, r) in zip(y, t.iterrows()):
    yy = ax.transLimits.transform((0, yi))[1]
    ax.text(tx, yy, f"{int(r.counties):,}", transform=ax.transAxes, fontsize=9, color=INK2, va="center")
    ax.text(tx + 0.13, yy, f"{r.dom_rate:+.1f}", transform=ax.transAxes, fontsize=9, color=INK, va="center")
    ax.text(tx + 0.29, yy, f"{r.intl_rate:+.1f}", transform=ax.transAxes, fontsize=9, color=INK, va="center")

ax.legend(loc="lower left", bbox_to_anchor=(0.0, 1.0), ncol=1, fontsize=9, handlelength=1.2, borderaxespad=0.4)
ax.annotate("Counties of 500k+ lost a net\n2.8 million residents to the\nrest of the U.S. ...", (-1.0, 1.25), (-1.8, 3.9),
            fontsize=8.5, color=INK2, va="center", arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))
ax.annotate("... and gained\n1.8 million\nfrom abroad", (0.63, 1.2), (0.85, 2.5),
            fontsize=8.5, color=INK2, va="center", arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))

title_block(fig, "After 2020, Americans left the biggest counties; immigrants refilled them only partly",
            "Net migration into U.S. counties from mid-2020 to mid-2023, grouped by county population", gap=0.045)
caption(fig, "Domestic movers flowed out of the 142 counties with 500,000+ people (−2.8 million net) and into mid-sized counties of 50,000–500,000\n"
             "(+2.3 million). International migration ran the other way: the bigger the county, the more immigrants it gained per resident\n"
             "(about 1.2–1.4 per 100 residents in counties of 1M+, vs. 0.2–0.3 per 100 in counties under 50k). Rates are per 100 residents of the 2020 population.\n"
             "Migration years run July 1–June 30 (e.g. '2021' = July 2020–June 2021). Population = 2020 estimate. 50 states + DC.\n"
             "Data: USDA ERS county-level data sets (Census Bureau population estimates), via CS765 765Data repository.")
save(fig, "q3_migration_by_county_size.png")
