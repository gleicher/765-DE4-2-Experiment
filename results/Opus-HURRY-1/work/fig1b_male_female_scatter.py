"""Story 1, alternate: male vs female life expectancy, with gap shown as distance from the diagonal."""
from common import *

p = load_wb()
q = p[p.is_country].dropna(subset=["gap"])

HL = [("Russian Federation", "Russia", ORANGE),
      ("United States", "United States", BLUE),
      ("India", "India", AQUA)]

fig = plt.figure(figsize=(9, 9.6))
ax = fig.add_axes([0.1, 0.2, 0.84, 0.64])
lo, hi = 40, 88

# iso-gap guide lines
for g in [0, 5, 10, 15]:
    ax.plot([lo, hi], [lo + g, hi + g], color=INK2 if g == 0 else "#bdbcb6",
            lw=1.1 if g == 0 else 0.8, ls="-" if g == 0 else (0, (4, 3)), zorder=1)
    xl = 84.5 - g if g else 80
    ax.text(xl, xl + g + 0.4, "women live as long as men" if g == 0 else f"women +{g} yrs",
            rotation=45, rotation_mode="anchor", fontsize=8.5, color=INK2, ha="left", va="bottom",
            transform_rotates_text=True)

for yr, kw in [(1960, dict(facecolors="none", edgecolors="#b5b4ae", s=14, lw=0.7)),
               (2023, dict(color="#b5b4ae", s=14, lw=0))]:
    d = q[q.Year == yr]
    ax.scatter(d.Male, d.Female, zorder=2, **kw)

for name, lab, col in HL:
    d = q[q["Country Name"] == name].sort_values("Year")
    ax.plot(d.Male, d.Female, color=col, lw=2, zorder=4)
    dec = d[d.Year % 10 == 0]
    ax.scatter(dec.Male, dec.Female, color=col, s=16, zorder=5, lw=0)
    for yr in [1960, 2023]:
        r = d[d.Year == yr].iloc[0]
        ax.scatter([r.Male], [r.Female], color=col, s=60, zorder=6, edgecolors="white", linewidths=1.5,
                   marker="o" if yr == 2023 else "s")

def lab(xy, txy, s, **kw):
    ax.annotate(s, xy, txy, fontsize=9, color=INK, zorder=7,
                arrowprops=dict(arrowstyle="-", color=INK2, lw=0.7, shrinkA=2, shrinkB=4), **kw)

def at(name, yr):
    r = q[(q["Country Name"] == name) & (q.Year == yr)].iloc[0]
    return (r.Male, r.Female)

lab(at("India", 1960), (52, 43.5), "India 1960: men 46.3, women 44.9\n(men outlived women)", ha="left", va="center")
lab(at("India", 2023), (75, 71.6), "India 2023: +3.1 yrs", ha="left", va="center")
lab(at("Russian Federation", 1960), (57, 68.2), "Russia 1960: +8.3 yrs", ha="right", va="center")
lab(at("Russian Federation", 1994), (53, 75), "Russia 1994: men 57.6, women 71.7\n(+14.2 yrs)", ha="right", va="center")
lab(at("Russian Federation", 2023), (60, 83), "Russia 2023: +10.7 yrs", ha="right", va="center")
lab(at("United States", 1960), (69.5, 66.3), "U.S. 1960: +6.5 yrs", ha="left", va="center")
lab(at("United States", 2023), (79, 76.5), "U.S. 2023: +5.3 yrs", ha="left", va="center")
ax.text(65, 49, "How to read: colored lines trace one country's path,\n1960 (square) to 2023 (large circle); small dots\nmark each decade. Gray: every other country,\nhollow = 1960, filled = 2023.\n\nBelow the solid diagonal, men outlive women.",
        fontsize=8.5, color=INK2, va="center", ha="left", linespacing=1.45)

ax.set_xlim(lo, hi); ax.set_ylim(lo, hi)
ax.set_aspect("equal")
ax.set_xlabel("Male life expectancy at birth (years)")
ax.set_ylabel("Female life expectancy at birth (years)")

title_block(fig, "Russia's men fell behind while India's women caught up",
            "How male and female life expectancy moved together, 1960–2023. Distance above the\n"
            "solid diagonal is how many more years women can expect to live than men.")
caption(fig, "Almost every country has moved up and to the right, and in 2023 every one sits above the diagonal (women live longer).\n"
             "Most countries cluster between the 0- and 10-year guides. India started below the diagonal (men lived longer) and crossed\n"
             "it around 1982. Russia's path stalls and moves sideways around 1990–2005: women's life expectancy held near 72 while men's\n"
             "fell to 58, one of the largest sustained gaps anywhere. The U.S. gap narrowed from 6.5 to 5.3 years.\n"
             "Data: World Bank (SP.DYN.LE00) via CS765 765Data repository; 217 countries, regional and income aggregates excluded.")
save(fig, "q1b_male_vs_female_paths.png")
