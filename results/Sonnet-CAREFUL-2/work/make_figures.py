"""Generate all six figures. Run: /opt/anaconda3/envs/p314/bin/python work/make_figures.py  (from project root)"""
import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import warnings; warnings.filterwarnings('ignore')

OUT = 'answers/figures/'
plt.rcParams.update({'font.family': 'Helvetica Neue' if False else 'DejaVu Sans', 'font.size': 11,
                     'axes.spines.top': False, 'axes.spines.right': False, 'figure.dpi': 100})
INK, GREY = '#222222', '#9a9a9a'
# Okabe-Ito
BL, OR, GR, VE, SK, RD, YE = '#0072B2', '#E69F00', '#009E73', '#D55E00', '#56B4E9', '#CC79A7', '#F0E442'

def caption(fig, text, y=0.015):
    fig.text(0.06, y, text, ha='left', va='bottom', fontsize=9.5, color='#444444', wrap=True)

# ---------------------------------------------------------------- data
wb = pd.read_csv('data/lifespan_dataset_1960.csv', index_col=0)
owid = pd.read_csv('data/life-expectancy-owid/life-expectancy-owid.csv')
owid.columns = ['entity', 'code', 'year', 'le']
iso = set(owid.code.dropna()) - {c for c in owid.code.dropna() if c.startswith('OWID')}
w = wb.pivot_table(index=['Country Name', 'Country Code', 'Year'], columns='Sex', values='Life Expectancy (years)').reset_index()
w = w[w['Country Code'].isin(iso)].dropna(subset=['Female', 'Male'])
w['gap'] = w.Female - w.Male
w = w.rename(columns={'Country Name': 'country', 'Country Code': 'code', 'Year': 'year'})
w['country'] = w.country.replace({'Russian Federation': 'Russia', 'Korea, Rep.': 'South Korea', 'Iran, Islamic Rep.': 'Iran', 'Egypt, Arab Rep.': 'Egypt'})
gap = w.pivot(index='year', columns='country', values='gap')
gap.to_csv('work/gender_gap_by_country_year.csv')

# ---------------------------------------------------------------- Fig 1A
fig, ax = plt.subplots(figsize=(11, 7.6))
fig.subplots_adjust(left=0.07, right=0.86, top=0.86, bottom=0.2)
for c in gap.columns:
    ax.plot(gap.index, gap[c], color='#d8d8d8', lw=0.6, alpha=0.8, zorder=1)
hl = {'Russia': VE, 'United States': BL, 'Japan': GR, 'India': OR, 'South Africa': RD}
for c, col in hl.items():
    ax.plot(gap.index, gap[c], color=col, lw=2.6, zorder=3)
    ax.text(2023.8, gap[c].iloc[-1], c, color=col, va='center', fontsize=11, fontweight='bold')
ax.axhline(0, color=INK, lw=0.8)
ax.annotate('Russia peaks in 1994:\nwomen outlive men by 14.2 years\n(post-Soviet mortality shock)', xy=(1994, gap.loc[1994, 'Russia']), xytext=(1962, 12.6),
            fontsize=10, color=VE, arrowprops=dict(arrowstyle='-', color=VE, lw=1), va='center')
ax.annotate('India: men outlived women\nin 1960; now women lead by 3 years', xy=(1962, gap.loc[1962, 'India']), xytext=(1964, -3.9), fontsize=10, color='#b87800', va='center',
            arrowprops=dict(arrowstyle='-', color=OR, lw=1))
ax.text(1960.5, 15.4, 'Grey lines: all other countries (n = %d)' % gap.shape[1], color='#777777', fontsize=10)
ax.set_xlim(1960, 2023); ax.set_ylim(-5, 16)
ax.set_ylabel('Female minus male life expectancy at birth (years)')
ax.set_xlabel('Year'); ax.grid(axis='y', color='#eeeeee', zorder=0)
fig.suptitle("Women's life-expectancy advantage has not shrunk everywhere", x=0.07, ha='left', fontsize=18, fontweight='bold', y=0.97)
fig.text(0.07, 0.905, 'Gap between female and male life expectancy, 1960-2023', fontsize=12, color='#444444')
caption(fig, "Each line is one country. In the United States the gap fell from 7.6 years (1970) to 4.8 (2010) as men gained ground, while Russia's gap surged after\n"
             "1990 and remains above 10 years. South Africa's gap swings with the HIV/AIDS epidemic and its aftermath. Source: World Bank life expectancy by sex.\n"
             "Country-level series only (regional and income aggregates removed).")
fig.savefig(OUT + 'q1_primary_gender_gap_lines.png', dpi=200); plt.close(fig)

# ---------------------------------------------------------------- Fig 1B  (dot plot, three years)
sel = ['Ukraine', 'Russia', 'Latvia', 'Kazakhstan', 'Brazil', 'France', 'Japan', 'South Korea', 'South Africa', 'China', 'United States',
       'United Kingdom', 'Sweden', 'Iran', 'India', 'Nigeria', 'Bangladesh', 'Pakistan']
yrs = [1960, 1990, 2023]
d = gap.loc[yrs, sel].T.sort_values(2023)
fig, ax = plt.subplots(figsize=(10, 8.2))
fig.subplots_adjust(left=0.17, right=0.95, top=0.85, bottom=0.2)
y = np.arange(len(d))
ax.axvline(0, color=INK, lw=0.8)
for i, (c, r) in enumerate(d.iterrows()):
    ax.plot([r.min(), r.max()], [i, i], color='#cfcfcf', lw=3, zorder=1, solid_capstyle='round')
cols = {1960: SK, 1990: '#7f7f7f', 2023: VE}
for yr in yrs:
    ax.scatter(d[yr], y, s=95, color=cols[yr], zorder=3, label=str(yr), edgecolor='white', lw=0.8)
ax.set_yticks(y); ax.set_yticklabels(d.index)
ax.set_xlabel('Female minus male life expectancy at birth (years)')
ax.grid(axis='x', color='#eeeeee', zorder=0); ax.set_axisbelow(True)
ax.set_xlim(-4.5, 14.5)
ax.legend(title='Year', loc='lower right', frameon=False, ncol=1)
ax.text(-0.15, -0.9, '< men live longer', color='#666666', fontsize=9.5, ha='right')
fig.suptitle('Women now outlive men almost everywhere, by very different margins', x=0.03, ha='left', fontsize=17, fontweight='bold', y=0.97)
fig.text(0.03, 0.905, 'Female-male life-expectancy gap in 1960, 1990 and 2023, 18 selected countries (sorted by 2023 gap)', fontsize=11.5, color='#444444')
caption(fig, "Ukraine, Russia and Latvia now have gaps of 10-13 years, far above 1960. In France, Sweden, the UK and the US the gap peaked around 1990\n"
             "and has since narrowed. Men outlived women in India, Pakistan, Bangladesh and Iran in 1960; all four have flipped. Gray bar spans the\n"
             "three years shown. Source: World Bank life expectancy by sex.", y=0.03)
fig.savefig(OUT + 'q1_alt_gender_gap_dotplot.png', dpi=200); plt.close(fig)

# ---------------------------------------------------------------- census
c = pd.read_csv('data/full_census_dataset.csv', dtype={'FIPS Code': str}, encoding='latin-1').copy()
c = c[~c['FIPS Code'].str.endswith('000')].copy()          # drop US and state rows
c['rucc'] = c['2023 Rural-urban Continuum Code']
c = c[c.rucc.notna()].copy()
c['rucc'] = c.rucc.astype(int)
def grp(r):
    return 'Large metro' if r == 1 else 'Other metro' if r in (2, 3) else 'Nonmetro, metro-adjacent' if r in (4, 6, 8) else 'Nonmetro, remote'
c['grp'] = c.rucc.map(grp)
order = ['Large metro', 'Other metro', 'Nonmetro, metro-adjacent', 'Nonmetro, remote']
gcol = {'Large metro': BL, 'Other metro': SK, 'Nonmetro, metro-adjacent': OR, 'Nonmetro, remote': VE}
years = list(range(2000, 2024))
rate = pd.DataFrame({g: [100 * d_[f'Unemployed {yv}'].sum() / d_[f'Civilian labor force {yv}'].sum() for yv in years]
                     for g, d_ in c.groupby('grp')}, index=years)[order]
rate.to_csv('work/unemployment_rate_by_group.csv')

# ---------------------------------------------------------------- Fig 2A
fig, ax = plt.subplots(figsize=(11, 7.4))
fig.subplots_adjust(left=0.08, right=0.96, top=0.86, bottom=0.2)
ax.axvspan(2007.9, 2009.9, color='#f1f1f1', zorder=0); ax.axvspan(2019.9, 2020.9, color='#f1f1f1', zorder=0)
ax.text(2008.9, 10.9, 'Great\nRecession', ha='center', va='top', fontsize=10, color='#555555')
ax.text(2020.4, 10.9, 'Pandemic', ha='center', va='top', fontsize=10, color='#555555', rotation=0)
for g in order:
    ax.plot(years, rate[g], color=gcol[g], lw=2.6, marker='o', ms=3.5)
ax.legend(handles=[Line2D([], [], color=gcol[g], lw=2.6, label=g) for g in order], loc='lower left', ncol=2, frameon=False, fontsize=10.5)
ax.text(2023, 3.0, 'all groups converge\nat 3.6-3.7% in 2023', fontsize=9.5, color='#555555', ha='right', va='top')
ax.annotate('2020: large metros jump\nto %.1f%% (+%.1f pts)' % (rate.loc[2020, 'Large metro'], rate.loc[2020, 'Large metro'] - rate.loc[2019, 'Large metro']),
            xy=(2020, rate.loc[2020, 'Large metro']), xytext=(2012.6, 8.0 + 2.2), fontsize=10, color=BL, va='center', arrowprops=dict(arrowstyle='-', color=BL, lw=1))
ax.annotate('2009-10: metro-adjacent rural\ncounties peak highest (%.1f%%)' % rate['Nonmetro, metro-adjacent'].max(),
            xy=(2010, rate.loc[2010, 'Nonmetro, metro-adjacent']), xytext=(2002.2, 10.4), fontsize=10, color='#b87800', va='center', arrowprops=dict(arrowstyle='-', color=OR, lw=1))
ax.set_xlim(2000, 2023); ax.set_ylim(2, 11.2)
ax.set_xticks(range(2000, 2024, 4)); ax.set_xticks(range(2000, 2024), minor=True)
ax.set_ylabel('Unemployment rate (% of civilian labor force)'); ax.grid(axis='y', color='#eeeeee', zorder=0)
fig.suptitle('The pandemic hit big-city labor markets hardest; the Great Recession did not', x=0.08, ha='left', fontsize=15, fontweight='bold', y=0.97)
fig.text(0.08, 0.905, 'County unemployment rate by rural-urban type, 2000-2023', fontsize=12, color='#444444')
caption(fig, "Rates are pooled: total unemployed divided by total civilian labor force over all counties in each group (3,184 counties with a 2023 rural-urban code;\n"
             "17 counties in AK, CT and MT without a code omitted). Metro = USDA Rural-Urban Continuum Codes 1-3; nonmetro = 4-9, split by adjacency to a metro area.\n"
             "By 2023 all four groups have converged near 3.6-3.7%. Source: USDA ERS county data set.", y=0.025)
fig.savefig(OUT + 'q2_primary_unemployment_lines.png', dpi=200); plt.close(fig)

# ---------------------------------------------------------------- Fig 2B
lab = {1: 'Metro, 1M+ people', 2: 'Metro, 250k-1M', 3: 'Metro, <250k', 4: 'Urban 20k+, adjacent', 5: 'Urban 20k+, not adj.',
       6: 'Urban 2.5-20k, adjacent', 7: 'Urban 2.5-20k, not adj.', 8: 'Rural <2.5k, adjacent', 9: 'Rural <2.5k, not adj.'}
c['d09'] = c['Unemployment rate 2009'] - c['Unemployment rate 2007']
c['d20'] = c['Unemployment rate 2020'] - c['Unemployment rate 2019']
fig, axes = plt.subplots(1, 2, figsize=(12, 7.6), sharey=True)
fig.subplots_adjust(left=0.2, right=0.97, top=0.82, bottom=0.2, wspace=0.06)
rng = np.random.default_rng(3)
for ax, col, ttl in zip(axes, ['d09', 'd20'], ['Great Recession: 2007 to 2009', 'Pandemic: 2019 to 2020']):
    for r in range(1, 10):
        v = c.loc[c.rucc == r, col].dropna()
        yy = 9 - r + rng.uniform(-0.28, 0.28, len(v))
        ax.scatter(v, yy, s=4, alpha=0.25, color=BL if r <= 3 else VE, lw=0, zorder=1)
        q1, med, q3 = v.quantile([.25, .5, .75])
        ax.plot([q1, q3], [9 - r] * 2, color=INK, lw=4.5, solid_capstyle='butt', zorder=3)
        ax.scatter([med], [9 - r], s=60, color='white', edgecolor=INK, zorder=4, lw=1.5)
        ax.text(16.8, 9 - r, f'{med:+.1f}', va='center', ha='right', fontsize=9.5, color=INK, fontweight='bold')
    ax.axvline(0, color=INK, lw=0.8); ax.set_title(ttl, fontsize=13, loc='left', fontweight='bold')
    ax.set_xlabel('Change in county unemployment rate (percentage points)'); ax.grid(axis='x', color='#eeeeee', zorder=0)
    ax.set_xlim(-3, 17)
axes[0].set_yticks(range(9)); axes[0].set_yticklabels([lab[r] for r in range(9, 0, -1)])
axes[0].axhline(5.5, color=GREY, lw=0.8, ls='--'); axes[1].axhline(5.5, color=GREY, lw=0.8, ls='--')
axes[0].text(-2.8, 5.65, 'Metro', fontsize=9.5, color='#666666'); axes[0].text(-2.8, 5.35, 'Nonmetro', fontsize=9.5, color='#666666', va='top')
fig.suptitle('Remote rural counties rose least in both downturns; in 2020 the rise scaled with city size', x=0.03, ha='left', fontsize=15, fontweight='bold', y=0.97)
fig.text(0.03, 0.905, 'Change in unemployment rate for each U.S. county, by USDA rural-urban continuum type', fontsize=12, color='#444444')
caption(fig, "Each dot is a county (blue = metro, vermilion = nonmetro). White circle = median county; black bar = middle half (interquartile range); number = median change.\n"
             "In 2020 the median rise falls steadily from big metros (+3.4) to the most rural counties (+1.5),\n"
             "while in 2009 most groups rose by a similar +4 to +5 and the most remote only +2.6. Source: USDA ERS county data set.", y=0.025)
fig.savefig(OUT + 'q2_alt_unemployment_change_strip.png', dpi=200); plt.close(fig)

# ---------------------------------------------------------------- Fig 3 (education)
b90 = "Percent of adults with a bachelor's degree or higher, 1990"; b20 = b90.replace('1990', '2019-23')
e = c.dropna(subset=[b90, b20, 'Census Population 2020']).copy()
fig, ax = plt.subplots(figsize=(10, 8.6))
fig.subplots_adjust(left=0.09, right=0.96, top=0.86, bottom=0.2)
ax.plot([0, 80], [0, 80], color=GREY, lw=1, ls='--', zorder=1)
ax.text(52, 49, 'no change (dashed line)', color='#777777', rotation=38, fontsize=9.5, ha='center')
for g in order[::-1]:
    s = e[e.grp == g]
    ax.scatter(s[b90], s[b20], s=6 + s['Census Population 2020'] / 25000, alpha=0.32, color=gcol[g], lw=0, zorder=2)
for g in order:
    s = e[e.grp == g]; mx, my = s[b90].median(), s[b20].median()
    ax.scatter([mx], [my], s=170, color=gcol[g], edgecolor=INK, lw=1.8, zorder=5)
    off = {'Large metro': (-12, 6), 'Other metro': (4, 2), 'Nonmetro, metro-adjacent': (14, -19), 'Nonmetro, remote': (22, -13)}[g]
    ax.annotate(f'{g}\n{mx:.0f}% to {my:.0f}% (+{my - mx:.0f})', xy=(mx, my), xytext=(mx + off[0] / 2.5, my + off[1] * 0.5),
                fontsize=10, fontweight='bold', color={'Other metro': '#1f7fb5', 'Nonmetro, metro-adjacent': '#b87800'}.get(g, gcol[g]), zorder=6, va='center',
                arrowprops=dict(arrowstyle='-', color=INK, lw=0.8), bbox=dict(fc='white', ec='none', alpha=0.8, pad=1.5))
ax.set_xlim(0, 60); ax.set_ylim(0, 80)
ax.set_xlabel("Adults with a bachelor's degree or higher, 1990 (% of county adults)")
ax.set_ylabel("Adults with a bachelor's degree or higher, 2019-23 (%)")
ax.grid(color='#eeeeee', zorder=0); ax.set_axisbelow(True)
fig.suptitle("Every county gained college graduates, but metros pulled away", x=0.09, ha='left', fontsize=16, fontweight='bold', y=0.97)
fig.text(0.09, 0.905, "Bachelor's-degree attainment, 1990 vs. 2019-23, all U.S. counties", fontsize=12, color='#444444')
caption(fig, "Each bubble is a county (area scaled to 2020 population); large dots mark the median county in each group. Counties above the dashed\n"
             "line gained. The median large-metro county gained 16 points, the median remote nonmetro county only 9, so the gap between them grew\n"
             "from about 3 to 11 points. Source: USDA ERS county data set; 3,184 counties with rural-urban codes.", y=0.03)
fig.savefig(OUT + 'q3_education_scatter.png', dpi=200); plt.close(fig)
print(e.groupby('grp')[[b90, b20]].median().round(1))

# ---------------------------------------------------------------- Fig 4 (COVID life expectancy)
p = owid[owid.code.isin(iso)].pivot(index='entity', columns='year', values='le')
p = p.drop(index=['Central African Republic'], errors='ignore')   # implausible 2019 value (31.5), excluded
v = pd.DataFrame({'drop': p[2021] - p[2019], 'rebound': p[2023] - p[2021]}).dropna()
v['net'] = v['drop'] + v['rebound']
fig, ax = plt.subplots(figsize=(10.5, 8.2))
fig.subplots_adjust(left=0.09, right=0.96, top=0.86, bottom=0.2)
xs = np.array([-7, 4.2])
ax.plot(xs, -xs, color=INK, lw=1.2, ls='--', zorder=1)
ax.fill_between(xs, -xs, 10, color='#e8f3ec', zorder=0); ax.fill_between(xs, -xs, -10, color='#fbeadf', zorder=0)
ax.text(0.2, 6.5, 'Above line: 2023 life expectancy\nback above its 2019 level', fontsize=10, color='#1b7a4b', va='top')
ax.text(-6.8, -3.0, 'Below line: still short of 2019 in 2023', fontsize=10, color='#b4501a')
ax.text(2.0, -1.0, 'full recovery:\nrebound = loss', fontsize=9.5, color=INK, rotation=-20, ha='center', va='bottom')
ax.scatter(v['drop'], v.rebound, s=26, color=np.where(v.net >= 0, GR, VE), alpha=0.7, edgecolor='white', lw=0.4, zorder=3)
lbl = {'Bolivia': (0.15, 0.2), 'Mexico': (-0.9, -0.55), 'Peru': (0.15, 0.1), 'Paraguay': (0.15, 0.1), 'Lebanon': (-0.9, -0.55),
       'United States': (0.1, -0.55), 'India': (-0.65, 0.2), 'Russia': (-0.5, -0.65), 'South Africa': (-0.2, -0.6), 'Palestine': (0.15, -0.1),
       'Japan': (0.1, 0.45), 'China': (0.1, -0.5), 'Libya': (0.15, -0.1), 'Eswatini': (0.1, 0.2), 'Namibia': (0.1, 0.2), 'Germany': (-0.35, -0.6)}
for k, (dx, dy) in lbl.items():
    if k in v.index:
        ax.text(v.loc[k, 'drop'] + dx, v.loc[k, 'rebound'] + dy, k, fontsize=9.5, color=INK)
ax.set_xlim(-7, 3); ax.set_ylim(-9.5, 8)
ax.axhline(0, color='#bbbbbb', lw=0.7, zorder=2); ax.axvline(0, color='#bbbbbb', lw=0.7, zorder=2)
ax.set_xlabel('Change in life expectancy 2019 to 2021 (years): the pandemic loss')
ax.set_ylabel('Change 2021 to 2023 (years): the rebound')
ax.legend(handles=[Line2D([], [], marker='o', ls='', color=GR, label='2023 at or above 2019'), Line2D([], [], marker='o', ls='', color=VE, label='2023 below 2019')],
          loc='lower left', frameon=False)
fig.suptitle('Most countries lost life expectancy to COVID-19, then won it back by 2023', x=0.09, ha='left', fontsize=16, fontweight='bold', y=0.97)
fig.text(0.09, 0.905, 'Period life expectancy at birth: loss 2019-2021 vs. rebound 2021-2023, %d countries and territories' % len(v), fontsize=11.5, color='#444444')
caption(fig, "Each dot is a country or territory. Latin American countries (Bolivia, Mexico, Peru, Paraguay) fell the furthest and rebounded the most; India and\n"
             "Russia sit in the middle; Japan, China and Germany barely moved. %d of %d are back above 2019. Palestine (2023) is an outlier far below the line.\n"
             "Source: Our World in Data long-run life expectancy (UN WPP 2024). Central African Republic excluded: its 2019 value looks erroneous." % ((v.net >= 0).sum(), len(v)), y=0.025)
fig.savefig(OUT + 'q4_covid_life_expectancy.png', dpi=200); plt.close(fig)
print(len(v), (v.net >= 0).sum(), v.loc[['Palestine', 'Libya', 'Bolivia']].round(1))
print(rate.loc[[2007, 2009, 2010, 2019, 2020, 2023]].round(2)); print(len(c))
print(c.groupby('grp')[['d09','d20']].median().round(2))
