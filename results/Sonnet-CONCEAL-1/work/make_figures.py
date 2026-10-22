"""Makes all figures for DE 4-2 into ../answers/figures.
Run:  /opt/anaconda3/envs/p314/bin/python -I make_figures.py
"""
import os, textwrap
import numpy as np, pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', 'data')
OUT = os.path.join(HERE, '..', 'answers', 'figures')
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11, 'axes.spines.top': False,
                     'axes.spines.right': False})
BLUE, ORANGE, GREY, GREEN, GOLD = '#0072B2', '#D55E00', '#8c8c8c', '#009E73', '#E69F00'

def wrap(s, n):
    return '\n'.join(textwrap.fill(p, n) for p in s.split('\n'))

def finish(fig, name, title, sub, caption, cap_w=125, top=0.88, bottom=0.14):
    fig.suptitle(title, x=0.012, y=0.992, ha='left', fontsize=17, fontweight='bold')
    fig.text(0.012, 0.992 - 0.045, wrap(sub, 120), ha='left', va='top', fontsize=11.5, color='#333')
    fig.text(0.012, 0.012, wrap(caption, cap_w), ha='left', va='bottom', fontsize=9.3, color='#444')
    fig.savefig(os.path.join(OUT, name), dpi=170)
    plt.close(fig)

# ------------------------------------------------------------ load data
wb = pd.read_csv(os.path.join(DATA, 'lifespan_dataset_1960.csv'), index_col=0)
wb = wb.rename(columns={'Country Name': 'name', 'Life Expectancy (years)': 'le'})
AGG = ['income', 'dividend', '&', 'IDA', 'IBRD', 'Euro area', 'European Union', 'OECD', 'small states',
       'World', 'Arab World', 'Fragile', 'Heavily', 'Least developed', 'Not classified', 'Sub-Saharan Africa',
       'South Asia', 'Middle East', 'Africa Eastern', 'Africa Western', 'Central Europe', 'North America',
       'Latin America', 'Small states']
both = wb[wb.Sex == 'Both']
is_agg = both.name.apply(lambda n: any(k in n for k in AGG))
cty = both[~is_agg].pivot(index='name', columns='Year', values='le')
grp_le = both[is_agg].pivot(index='Year', columns='name', values='le')

census = pd.read_csv(os.path.join(DATA, 'full_census_dataset.csv'), dtype={'FIPS Code': str}, encoding='latin-1')
cn = census[~census['FIPS Code'].str.endswith('000')].copy()      # drop US + state rows
RUCC = '2023 Rural-urban Continuum Code'
def grp(c):
    if c == 1: return 'Large metro'
    if c in (2, 3): return 'Medium/small metro'
    if c in (4, 5, 6, 7): return 'Small town (nonmetro)'
    if c in (8, 9): return 'Rural (nonmetro)'
GROUPS = ['Large metro', 'Medium/small metro', 'Small town (nonmetro)', 'Rural (nonmetro)']
GCOL = dict(zip(GROUPS, [BLUE, GREEN, GOLD, ORANGE]))
cn['grp'] = cn[RUCC].map(grp)
st = pd.read_csv(os.path.join(DATA, 'aggregate_census_dataset.csv'), sep='\t', encoding='latin-1')

# ============================================================ Q1 A: catch-up scatter
d = pd.DataFrame({'le60': cty[1960], 'le23': cty[2023]}).dropna()
d['gain'] = d.le23 - d.le60
fig, ax = plt.subplots(figsize=(11, 8.6))
fig.subplots_adjust(left=0.08, right=0.97, top=0.85, bottom=0.2)
ax.scatter(d.le60, d.gain, s=28, color=GREY, alpha=.65, lw=0)
m, b = np.polyfit(d.le60, d.gain, 1)
xs = np.array([d.le60.min(), d.le60.max()])
ax.plot(xs, m * xs + b, color='#444', lw=1.2, ls='--')
ax.text(75.5, 33, 'Dashed line = overall trend:\neach extra year of starting life\nexpectancy goes with %.2f fewer\nyears gained' % abs(m),
        fontsize=9.5, color='#444', ha='right', va='top')
hl = {'Korea, Rep.': (BLUE, (6, 4)), 'China': (BLUE, (6, -3)), 'Maldives': (BLUE, (6, -3)),
      'United States': (GREY, (-30, 10)),
      'Lesotho': (ORANGE, (8, 0)), 'Eswatini': (ORANGE, (8, -4)), 'Ukraine': (ORANGE, (8, -3)),
      'Russian Federation': (ORANGE, (8, 2)), 'Central African Republic': (ORANGE, (-4, -14))}
for n, (col, off) in hl.items():
    r = d.loc[n]
    ax.scatter([r.le60], [r.gain], s=70, color=col, edgecolor='white', lw=.8, zorder=3)
    ax.annotate(n.replace('Russian Federation', 'Russia').replace('Korea, Rep.', 'South Korea'),
                (r.le60, r.gain), xytext=off, textcoords='offset points', fontsize=9.5, color=col, fontweight='bold')
ax.axhline(0, color='#bbb', lw=.8)
ax.set_xlabel('Life expectancy at birth in 1960 (years)')
ax.set_ylabel('Years gained by 2023')
ax.set_ylim(-3, 48)
ax.grid(alpha=.2)
finish(fig, 'q1_viz1_catchup_scatter.png',
       'Countries that started furthest behind in 1960 gained the most',
       'Each dot is a country. Life expectancy gained 1960-2023 versus where the country started.',
       'Blue = fast catch-up stories (South Korea, China, whose 1960 figure is depressed by the 1959-61 famine, and Maldives). Orange = countries that gained far less than '
       'their starting point predicts: Lesotho and Eswatini (HIV/AIDS) and Russia and Ukraine (post-Soviet mortality). Both sexes combined. '
       'Aggregates (income groups, regions) removed; %d countries/territories shown. Source: World Bank life expectancy, 1960-2023.' % len(d))

# ============================================================ Q1 B: income group lines
names = ['Low income', 'Lower middle income', 'Upper middle income', 'High income']
cols = ['#8c2d04', ORANGE, GREEN, BLUE]
fig, ax = plt.subplots(figsize=(11, 8.6))
fig.subplots_adjust(left=0.08, right=0.83, top=0.85, bottom=0.2)
hi, lo = grp_le['High income'], grp_le['Low income']
ax.fill_between(grp_le.index, lo, hi, color='#dddddd', alpha=.6, lw=0)
for n, c in zip(names, cols):
    s = grp_le[n]
    ax.plot(s.index, s, color=c, lw=2.6)
    ax.text(2023.8, s.loc[2023], n.replace(' income', '') + '\n%.1f yrs' % s.loc[2023], color=c, va='center', fontsize=10, fontweight='bold')
gap = hi - lo
for y in (1960, 1990, 2023):
    ax.plot([y, y], [lo[y], hi[y]], color='#333', lw=1.2)
    ax.text(y + (0.8 if y < 2023 else -0.8), (lo[y] + hi[y]) / 2, 'gap\n%.0f yrs' % gap[y],
            ha='left' if y < 2023 else 'right', va='center', fontsize=10, fontweight='bold', color='#333',
            bbox=dict(fc='white', ec='none', alpha=.8, pad=1.5))
ax.annotate('1959-61 China famine\n(pulls down upper-middle)', (1960, grp_le.loc[1960, 'Upper middle income']),
            xytext=(1963, 30), arrowprops=dict(arrowstyle='-', color='#555'), fontsize=9, color='#555', va='center')
ax.annotate('COVID-19', (2021, grp_le.loc[2021, 'High income']), xytext=(2007, 83.5),
            arrowprops=dict(arrowstyle='-', color='#555'), fontsize=9, color='#555')
ax.set_ylim(25, 88)
ax.set_xlim(1959, 2023)
ax.set_xlabel('Year'); ax.set_ylabel('Life expectancy at birth (years)')
ax.grid(alpha=.2)
finish(fig, 'q1_viz2_income_gap_lines.png',
       'The life expectancy gap between the richest and poorest countries is shrinking',
       'World Bank income groups, 1960-2023. Shaded band = gap between high-income and low-income groups.',
       'The gap was %.0f years in 1960, was still %.0f in 1990 (it barely moved from the mid-1970s to about 2000), and has fallen to %.0f years by 2023. '
       'Dips near 2020 reflect COVID-19. Both sexes combined; income groups are World Bank aggregates as provided in the data. '
       'Source: World Bank life expectancy, 1960-2023.' % (gap[1960], gap[1990], gap[2023]))

# ============================================================ Q2 A: lines of median % BA by group
cols_ba = {1990: "Percent of adults with a bachelor's degree or higher, 1990",
           2000: "Percent of adults with a bachelor's degree or higher, 2000",
           2010: "Percent of adults with a bachelor's degree or higher, 2008-12",
           2021: "Percent of adults with a bachelor's degree or higher, 2019-23"}
med = pd.DataFrame({y: cn.groupby('grp')[c].median() for y, c in cols_ba.items()}).loc[GROUPS]
fig, ax = plt.subplots(figsize=(11, 8.6))
fig.subplots_adjust(left=0.08, right=0.72, top=0.85, bottom=0.2)
for g in GROUPS:
    ax.plot(med.columns, med.loc[g], color=GCOL[g], lw=3, marker='o', ms=7)
    dy = {'Small town (nonmetro)': 1.3, 'Rural (nonmetro)': -1.3}.get(g, 0)
    ax.text(2021.6, med.loc[g, 2021] + dy, '%s  %.0f%%' % (g, med.loc[g, 2021]), color=GCOL[g], va='center', fontsize=10, fontweight='bold')
    ax.text(1989.4, med.loc[g, 1990], '%.0f%%' % med.loc[g, 1990], color=GCOL[g], va='center', ha='right', fontsize=10)
ax.set_xticks([1990, 2000, 2010, 2021])
ax.set_xticklabels(['1990', '2000', '2008-12', '2019-23'])
ax.set_xlim(1986, 2021)
ax.set_ylim(0, 36)
ax.set_ylabel("Median county: % of adults with a bachelor's degree or higher")
ax.grid(axis='y', alpha=.2)
gap90 = med.loc['Large metro', 1990] - med.loc['Rural (nonmetro)', 1990]
gap21 = med.loc['Large metro', 2021] - med.loc['Rural (nonmetro)', 2021]
ax.text(1991, 33, 'Large metro minus rural gap:\n%.0f points in 1990 -> %.0f points in 2019-23' % (gap90, gap21), ha='left', va='center', fontsize=11, color='#333', fontweight='bold')
finish(fig, 'q2_viz1_education_lines.png',
       'College degrees spread everywhere, but big-city counties pulled away',
       "Share of adults with a bachelor's degree or higher, median county in each urban-rural group.",
       "Groups use the 2023 USDA Rural-Urban Continuum Codes (1 = large metro; 2-3 = other metro; 4-7 = nonmetro with an urban area of 5,000+; 8-9 = rural). "
       "Each line is the median of county percentages (n = %d counties; counties not weighted by population). Time points are 1990, 2000, "
       "2008-12 and 2019-23, plotted at roughly their midpoints. Source: USDA ERS county census data." % cn[cols_ba[2021]].notna().sum())

# ============================================================ Q2 B: county scatter
fig, ax = plt.subplots(figsize=(11, 8.6))
fig.subplots_adjust(left=0.08, right=0.97, top=0.85, bottom=0.2)
pop = cn['Census Population 2020']
dd = cn[[cols_ba[1990], cols_ba[2021], 'grp']].assign(pop=pop).dropna()
dd = dd.sort_values('pop', ascending=False)
for g in GROUPS[::-1]:
    s = dd[dd.grp == g]
    ax.scatter(s[cols_ba[1990]], s[cols_ba[2021]], s=8 + 90 * np.sqrt(s['pop'] / dd['pop'].max()), color=GCOL[g],
               alpha=.35, lw=0, label=g)
for g in GROUPS:
    s = dd[dd.grp == g]
    ax.scatter(s[cols_ba[1990]].median(), s[cols_ba[2021]].median(), s=170, marker='D', color=GCOL[g],
               edgecolor='black', lw=1.4, zorder=5)
ax.plot([0, 80], [0, 80], color='#444', ls='--', lw=1)
ax.text(52, 49, 'no change', rotation=33, color='#444', fontsize=9.5)
ax.set_xlim(0, 62); ax.set_ylim(0, 82)
ax.set_xlabel("% of adults with a bachelor's degree or higher, 1990")
ax.set_ylabel("% with a bachelor's degree or higher, 2019-23")
ax.grid(alpha=.2)
leg = [Line2D([], [], marker='o', ls='', color=GCOL[g], ms=9, alpha=.7, label=g) for g in GROUPS]
leg.append(Line2D([], [], marker='D', ls='', mfc='white', mec='black', ms=9, label='group median'))
ax.legend(handles=leg, loc='upper left', frameon=False, title='County type', title_fontsize=10)
finish(fig, 'q2_viz2_education_scatter.png',
       'Nearly every county gained, and counties that started higher gained more',
       "Each circle is a county: 1990 versus 2019-23 share of adults with a bachelor's degree. Circle area = 2020 population.",
       "Diamonds mark the median county of each group, which sit well above the dashed no-change line (rural and small-town counties moved up less than "
       "large metros). Groups use 2023 USDA Rural-Urban Continuum Codes. %d counties with both years of data; only %d of them fall below the no-change line. "
       "Source: USDA ERS county census data." % (len(dd), (dd[cols_ba[2021]] < dd[cols_ba[1990]]).sum()))

# ============================================================ Q3: unemployment tile grid
LAYOUT = {'AK': (0, 0), 'ME': (0, 10), 'VT': (1, 9), 'NH': (1, 10),
          'WA': (2, 0), 'ID': (2, 1), 'MT': (2, 2), 'ND': (2, 3), 'MN': (2, 4), 'IL': (2, 5), 'WI': (2, 6), 'MI': (2, 7), 'NY': (2, 8), 'RI': (2, 9), 'MA': (2, 10),
          'OR': (3, 0), 'NV': (3, 1), 'WY': (3, 2), 'SD': (3, 3), 'IA': (3, 4), 'IN': (3, 5), 'OH': (3, 6), 'PA': (3, 7), 'NJ': (3, 8), 'CT': (3, 9),
          'CA': (4, 0), 'UT': (4, 1), 'CO': (4, 2), 'NE': (4, 3), 'MO': (4, 4), 'KY': (4, 5), 'WV': (4, 6), 'VA': (4, 7), 'MD': (4, 8), 'DE': (4, 9),
          'AZ': (5, 1), 'NM': (5, 2), 'KS': (5, 3), 'AR': (5, 4), 'TN': (5, 5), 'NC': (5, 6), 'SC': (5, 7), 'DC': (5, 8),
          'OK': (6, 2), 'LA': (6, 3), 'MS': (6, 4), 'AL': (6, 5), 'GA': (6, 6),
          'HI': (7, 0), 'TX': (7, 3), 'FL': (7, 7)}
yrs = list(range(2000, 2024))
ur = st.set_index('State')[['Unemployment rate %d' % y for y in yrs]]
ur.columns = yrs
assert set(LAYOUT) <= set(ur.index) and len(LAYOUT) == 51, set(ur.index) - set(LAYOUT)
fig = plt.figure(figsize=(14, 10.4))
W, H = 0.9 / 11, 0.7 / 8
x0, ytop = 0.045, 0.835
rows = []
for s, (r, c) in LAYOUT.items():
    v = ur.loc[s]
    rec = v.loc[2008:2012].max(); rec_y = v.loc[2008:2012].idxmax(); cov = v.loc[2020]
    worse = cov > rec
    rows.append((s, rec, rec_y, cov, worse))
    ax = fig.add_axes([x0 + c * W + 0.003, ytop - (r + 1) * H + 0.004, W - 0.006, H - 0.008])
    col = ORANGE if worse else BLUE
    ax.set_facecolor('#fdf3ec' if worse else '#eef4fa')
    ax.plot(yrs, v.values, color=col, lw=1.3)
    ax.scatter([rec_y], [rec], s=22, marker='s', color=BLUE, zorder=3)
    ax.scatter([2020], [cov], s=22, marker='o', color=ORANGE, zorder=3)
    ax.set_ylim(0, 16); ax.set_xlim(1999, 2024)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values(): sp.set_visible(False)
    ax.text(0.04, 0.96, s, transform=ax.transAxes, fontsize=9.5, fontweight='bold', va='top', color='#222')
nw = sum(r[4] for r in rows)
# legend / key in the empty top middle area
kx = fig.add_axes([x0 + 2 * W, ytop - 2 * H + 0.01, 7 * W - 0.01, 2 * H - 0.02]); kx.axis('off')
ex = ur.loc['NV']
kx.set_xlim(0, 10); kx.set_ylim(0, 2)
ia = fig.add_axes([x0 + 2 * W + 0.01, ytop - 2 * H + 0.015, 2 * W, 2 * H - 0.03])
ia.plot(yrs, ex.values, color=ORANGE, lw=1.6); ia.set_ylim(0, 16); ia.set_xlim(1999, 2024)
ia.scatter([ex.loc[2008:2012].idxmax()], [ex.loc[2008:2012].max()], marker='s', s=30, color=BLUE, zorder=3)
ia.scatter([2020], [ex.loc[2020]], s=30, color=ORANGE, zorder=3)
ia.set_yticks([0, 8, 16]); ia.set_xticks([2000, 2010, 2020]); ia.tick_params(labelsize=7.5)
ia.set_title('How to read a tile (Nevada)', fontsize=8.5, loc='left')
kx.text(4.0, 1.65, wrap('Line = annual average unemployment rate, 2000-2023. Every tile uses the same 0-16% scale.', 44), fontsize=9.3, va='top')
kx.text(4.0, 0.95, '■ Great Recession peak (2008-12 high)', fontsize=9.3, color=BLUE, va='top')
kx.text(4.0, 0.62, '● 2020 (pandemic year)', fontsize=9.3, color=ORANGE, va='top')
kx.text(4.0, 0.2, wrap('Orange tile = 2020 rate beat the Great Recession peak. Blue tile = it did not.', 44), fontsize=9.3, va='top')
finish(fig, 'q3_unemployment_tilemap.png',
       'The pandemic was a bigger jobs shock than 2008 in only %d states' % nw,
       'Unemployment rate in each state, 2000-2023, with the Great Recession peak compared to the pandemic year 2020.',
       'Tiles are placed roughly where each state sits on the map. Rates are annual averages, which smooth the very sharp but brief spike in spring 2020, '
       'so 2020 looks milder here than it felt. States where 2020 topped the 2008-12 peak: ' + ', '.join(r[0] for r in rows if r[4]) +
       '. Source: USDA ERS state-level census data (BLS unemployment rates).', cap_w=150)
print('Q3 worse-in-2020:', [r[0] for r in rows if r[4]])

# ============================================================ Q4: domestic migration after 2020
mig_cols = ['Domestic migration %d' % y for y in (2021, 2022, 2023)]
m = cn[[RUCC, 'grp', 'Census Population 2020'] + mig_cols].dropna()
byc = m.groupby(RUCC).agg(pop=('Census Population 2020', 'sum'), **{c: (c, 'sum') for c in mig_cols})
byc['cum'] = byc[mig_cols].sum(axis=1)
byc['rate'] = byc.cum / byc['pop'] * 1000
for c in mig_cols: byc[c + '_r'] = byc[c] / byc['pop'] * 1000
codes = list(byc.index.astype(int))
colr = [GCOL[grp(c)] for c in codes]
labels = {1: 'Metro, 1M+ people', 2: 'Metro, 250k-1M', 3: 'Metro, <250k', 4: 'Urban 20k+, adjacent to metro',
          5: 'Urban 20k+, not adjacent', 6: 'Urban 5k-20k, adjacent', 7: 'Urban 5k-20k, not adjacent',
          8: 'Rural, adjacent to metro', 9: 'Rural, not adjacent'}
fig, (a1, a2) = plt.subplots(1, 2, figsize=(14, 8.2), sharey=True, gridspec_kw={'width_ratios': [1.15, 1], 'wspace': 0.06})
fig.subplots_adjust(left=0.27, right=0.97, top=0.82, bottom=0.2)
ypos = np.arange(len(codes))
a1.barh(ypos, byc.rate, color=colr, height=.65)
for yv, (c, r) in enumerate(zip(codes, byc.rate)):
    a1.text(r + (0.5 if r >= 0 else -0.5), yv, '%+.1f' % r, va='center', ha='left' if r >= 0 else 'right', fontsize=9.5, fontweight='bold')
a1.set_yticks(ypos); a1.set_yticklabels(['%d  %s' % (c, labels[c]) for c in codes])
a1.invert_yaxis(); a1.axvline(0, color='#333', lw=1)
a1.set_xlabel('Net domestic migration, 2021-2023,\nper 1,000 residents (2020 population)')
a1.set_xlim(-14, 26)
a1.grid(axis='x', alpha=.2)
a2.barh(ypos, byc.cum / 1000, color=colr, height=.65)
for yv, v in enumerate(byc.cum / 1000):
    a2.text(v + (12 if v >= 0 else -12), yv, '%+.0fk' % v, va='center', ha='left' if v >= 0 else 'right', fontsize=9.5, fontweight='bold')
a2.axvline(0, color='#333', lw=1)
a2.set_xlabel('Net people moved in (+) or out (-), 2021-2023\n(thousands)')
a2.set_xlim(-2300, 1400)
a2.grid(axis='x', alpha=.2)
a2.spines['left'].set_visible(False); a2.tick_params(axis='y', length=0)
a1.text(-13.5, -0.85, 'Counties by Rural-Urban Continuum Code (2023)', fontsize=9, color='#555', style='italic', va='bottom', clip_on=False)
finish(fig, 'q4_domestic_migration.png',
       'After 2020, large metros lost residents to everywhere else',
       'Net domestic migration (moves within the US) by county type, July 2020 through June 2023.',
       'Only the largest metro counties (1M+ people) show a real net loss, about %.1f million people in three years; every other county type gains or roughly '
       'breaks even (type 5 is about flat); smaller metros, towns and rural areas next to a metro grow fastest per resident. Domestic migration excludes immigration. Left panel '
       'scales by population; right panel shows absolute counts. Counties with missing values dropped (n = %d). Source: USDA ERS county census data.'
       % (-byc.loc[1, 'cum'] / 1e6, len(m)), cap_w=140)
print(byc[['rate', 'cum']].round(1))
