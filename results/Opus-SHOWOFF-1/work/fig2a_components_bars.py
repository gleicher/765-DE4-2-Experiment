"""Q2 primary: where population change comes from, by rural-urban continuum code (aligned diverging bars)."""
from census_components import *
setup()
c = county_components(); r = rucc_components(c)

PANELS = [("nat", "Births minus deaths", "Deaths outnumber births in every\nnonmetro group"),
          ("dom", "+ Moves within the US", "Americans leave the 1M+ metros\nfor smaller places"),
          ("intl", "+ Moves from abroad", "Immigrants add most in the\nbiggest metros"),
          ("chg", "= Total change", "Remote rural groups (7, 9)\nstill shrink")]
fig = plt.figure(figsize=(13, 8.4))
header(fig, "Big metros grow from births and immigrants; rural America grows only when Americans move in",
       "Average yearly population change per 1,000 residents, 2021–2023, for all US counties grouped by the USDA 2023 Rural-Urban Continuum Code. Blue adds people; red removes them.\n"
       "Rural counties lose people to deaths outnumbering births, and gain them back from Americans moving in. The biggest metros are the reverse.",
       x=0.03)
left, top, h = 0.245, 0.775, 0.64
w, gap = 0.163, 0.022
rows = list(range(1, 10))
ypos = {k: i + (0.55 if k >= 4 else 0) for i, k in enumerate(rows)}
yl = [ypos[k] for k in rows]
LIM = (-6, 8.5)
axes = []
for j, (key, title, sub) in enumerate(PANELS):
    ax = fig.add_axes([left + j * (w + gap), top - h, w, h])
    axes.append(ax)
    v = r[key]
    cols = [BLUE if x >= 0 else RED for x in v]
    if key == "chg":
        cols = [INK2 if x >= 0 else "#a33b3a" for x in v]
    ax.barh(yl, v, height=0.68, color=cols, edgecolor="none", zorder=3)
    ax.axvline(0, color=INK, lw=1, zorder=4)
    for y, x in zip(yl, v):
        ax.text(x + (0.25 if x >= 0 else -0.25), y, f"{x:+.1f}", va="center", ha="left" if x >= 0 else "right",
                fontsize=9.2, color=INK, zorder=5)
    ax.set_xlim(*LIM); ax.set_ylim(max(yl) + .6, -.6)
    ax.set_yticks([]); ax.spines["left"].set_visible(False)
    ax.set_xticks([-5, 0, 5]); ax.tick_params(axis="x", labelsize=8.8, length=0)
    ax.grid(axis="y", visible=False)
    ax.set_title(title, fontsize=11.5, pad=34, loc="left")
    ax.text(0, 1.012, sub, transform=ax.transAxes, fontsize=9.2, color=INK2, va="bottom", linespacing=1.3)
    if key == "chg":
        ax.patch.set_facecolor("#f4f3ef"); 
    if j == 0:
        ax.set_xlabel("per 1,000 residents per year", fontsize=8.8, color=MUTED, loc="left")

# row labels
for k in rows:
    y = ypos[k]
    yf = top - h + h * (1 - (y + .6) / (max(yl) + 1.2))
    lab = RUCC_LABEL[k]
    fig.text(left - 0.012, yf + 0.009, f"{k}  {lab}", ha="right", va="center", fontsize=9.6, color=INK)
    fig.text(left - 0.012, yf - 0.012, f"{int(r.loc[k, 'n'])} counties · {r.loc[k, 'pop'] / 1e6:.1f}M people",
             ha="right", va="center", fontsize=8.4, color=MUTED)
# metro / nonmetro brackets
def bracket(k0, k1, text):
    y0 = top - h + h * (1 - (ypos[k0] - .4 + .6) / (max(yl) + 1.2)); y1 = top - h + h * (1 - (ypos[k1] + .4 + .6) / (max(yl) + 1.2))
    fig.add_artist(plt.Line2D([0.02, 0.02], [y1, y0], color=AXIS, lw=1.6, transform=fig.transFigure))
    fig.text(0.011, (y0 + y1) / 2, text, rotation=90, ha="center", va="center", fontsize=10, fontweight="bold", color=INK2)
bracket(1, 3, "METRO")
bracket(4, 9, "NONMETRO (RURAL)")

footer(fig, "Data: USDA ERS county-level data sets (Population Estimates: natural change, domestic and international migration, 2021–2023; 2023 Rural-Urban Continuum Codes), CS765 course data.\n"
       "Rates = sum of each component over 2021–2023 ÷ July 2020 population estimate ÷ 3, computed for each group of counties as a whole (population-weighted). "
       "3,106 counties in the 50 states + DC;\nPuerto Rico (no components reported) and 17 retired Alaska/Connecticut units without a 2023 code excluded. Total change also includes the Census 'residual'.",
       x=0.03, y=0.012)
save(fig, "q2a_components_by_rucc")
