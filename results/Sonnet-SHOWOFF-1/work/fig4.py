from common import *
from matplotlib.patches import FancyBboxPatch, Rectangle
a = census_states(); us = a[a.State == "US"].iloc[0]
a = a[~a.State.isin(["US", "PR"])]
yrs = list(range(2000, 2024))
u = a.set_index("State")[[f"Unemployment rate {y}" for y in yrs]]; u.columns = yrs
usu = pd.Series([us[f"Unemployment rate {y}"] for y in yrs], index=yrs)
gr = u.loc[:, 2008:2012].max(axis=1); gry = u.loc[:, 2008:2012].idxmax(axis=1); cv = u[2020]
LAYOUT = {0: {"AK": 0, "ME": 10}, 1: {"WI": 5, "VT": 9, "NH": 10},
          2: dict(WA=0, ID=1, MT=2, ND=3, MN=4, IL=5, MI=6, NY=8, MA=9),
          3: dict(OR=0, NV=1, WY=2, SD=3, IA=4, IN=5, OH=6, PA=7, NJ=8, CT=9, RI=10),
          4: dict(CA=0, UT=1, CO=2, NE=3, MO=4, KY=5, WV=6, VA=7, MD=8, DE=9),
          5: dict(AZ=1, NM=2, KS=3, AR=4, TN=5, NC=6, SC=7, DC=8),
          6: dict(OK=3, LA=4, MS=5, AL=6, GA=7), 7: dict(HI=0, TX=3, FL=8)}
BLUE, ORG = "#2166ac", "#e08214"
fig = plt.figure(figsize=(14, 10.4))
W, H = 0.0805, 0.0795; X0, Y0 = 0.035, 0.745
YMAX = 14.5

def tile(ax, s, big=False):
    worse = cv[s] > gr[s]
    ax.add_patch(Rectangle((2000, 0), 23.5, YMAX, color=(ORG if worse else BLUE), alpha=0.11 if not big else 0.0, lw=0, zorder=0))
    ax.plot(yrs, u.loc[s], color=INK, lw=1.2 if not big else 2.0, zorder=3)
    ax.plot(yrs, usu, color=MUTED, lw=0.7, ls=(0, (2, 2)), zorder=2)
    ax.scatter([gry[s]], [gr[s]], s=22 if not big else 70, color=BLUE, zorder=5)
    ax.scatter([2020], [cv[s]], s=22 if not big else 70, color=ORG, zorder=5)
    ax.set_xlim(1999.5, 2023.5); ax.set_ylim(0, YMAX); ax.axis("off")

for r, row in LAYOUT.items():
    for s, col in row.items():
        ax = fig.add_axes([X0 + col * (W + 0.0035), Y0 - r * (H + 0.0015) - 0.0 , W, H - 0.017])
        tile(ax, s)
        fig.text(X0 + col * (W + 0.0035) + 0.0015, Y0 - r * (H + 0.0015) + H - 0.0165, s, fontsize=9.5, fontweight="bold", color=INK, va="bottom")
        fig.text(X0 + col * (W + 0.0035) + W - 0.0015, Y0 - r * (H + 0.0015) + H - 0.0165, f"{gr[s]:.0f} | {cv[s]:.0f}", fontsize=7.8, color=MUTED, va="bottom", ha="right")

# key (Nevada) in empty top-left area
k = fig.add_axes([0.125, 0.675, 0.29, 0.1]); tile(k, "NV", big=True)
k.add_patch(Rectangle((2000, 0), 23.5, YMAX, color=BLUE, alpha=0.11, lw=0))
k.annotate("Great Recession peak\n(worst year 2008-12)\n13.8% in 2010", xy=(2010, 13.8), xytext=(2000.5, 12.3), fontsize=8.3, color=BLUE, va="top", arrowprops=dict(arrowstyle="-", color=BLUE, lw=.8))
k.annotate("COVID year 2020\n13.5%", xy=(2020, 13.5), xytext=(2013.3, 13.6), fontsize=8.3, color=ORG, va="top", arrowprops=dict(arrowstyle="-", color=ORG, lw=.8))
fig.text(0.125, 0.782, "HOW TO READ A TILE (example: Nevada)", fontsize=9, fontweight="bold", color=MUTED)
fig.text(0.56, 0.705, "Each tile = one state, 2000-2023, same 0-14.5% scale.\nNumbers at top right of a tile: Great Recession peak % | 2020 %.\nDotted line = U.S. rate.", fontsize=8.2, color=MUTED)
# tint legend
for i, (c_, t_) in enumerate([(BLUE, "Great Recession was worse (42 states)"), (ORG, "2020 was worse (9 states)")]):
    fig.patches.append(Rectangle((0.46, 0.765 - i * 0.026), 0.014, 0.018, color=c_, alpha=0.25, transform=fig.transFigure))
    fig.text(0.48, 0.765 - i * 0.026 + 0.003, t_, fontsize=9.5, va="bottom", color=INK)
fig.text(0.46, 0.79, "Tile shading", fontsize=9, fontweight="bold", color=MUTED)

frame(fig, "Two recessions, two geographies: the Great Recession pummeled the Sun Belt and Rust Belt,\nwhile the 2020 pandemic spike beat it only in tourism-, energy- and Northeast-heavy states",
      "Annual average unemployment rate by state, 2000-2023. Blue dot = worst year of the Great Recession (2008-12); orange dot = 2020.",
      caption=("In 42 of 51 states (incl. DC), annual unemployment was higher at the Great Recession's worst than in 2020. Exceptions: Hawaii (2.5% to 11.7%), Massachusetts, New York,\n"
               "Louisiana, Pennsylvania, Alaska, New Mexico, New Hampshire and North Dakota. The 2020 jump was brief (most states were back near pre-2020 lows by 2023), whereas the\n"
               "recession peak came in 2009-10 and recovery was slow. Annual averages smooth over the short, sharp 2020 spike, so this view likely understates COVID's severity.\n"
               "Tile layout is a schematic grid (not to scale). Puerto Rico omitted (no 2020 value)."),
      source="Data: USDA ERS / BLS Local Area Unemployment Statistics via course file aggregate_census_dataset.csv.", top=0.985)
save(fig, "q4_fig1_unemployment_tile_map.png")
