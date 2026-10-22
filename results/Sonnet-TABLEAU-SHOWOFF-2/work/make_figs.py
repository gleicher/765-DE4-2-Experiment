"""Builds the six figures. Run: /opt/anaconda3/envs/p314/bin/python -I work/make_figs.py  (from the run folder)
Matplotlib is used to imitate the look of Tableau worksheets (Tableau 10 palette, light grid,
bold sheet titles, right-hand legends). This is NOT Tableau output."""
import os, warnings
import numpy as np, pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.colors import LinearSegmentedColormap
warnings.filterwarnings('ignore')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, 'data'); OUT = os.path.join(ROOT, 'answers', 'figures'); os.makedirs(OUT, exist_ok=True)
INT = os.path.join(ROOT, 'work', 'intermediate'); os.makedirs(INT, exist_ok=True)

plt.rcParams.update({'font.family': ['Arial', 'Helvetica', 'DejaVu Sans'], 'font.size': 11,
                     'axes.edgecolor': '#b0b0b0', 'axes.labelcolor': '#333333',
                     'xtick.color': '#444444', 'ytick.color': '#444444', 'figure.dpi': 100})
# Tableau 10 classic palette
BLUE, ORANGE, RED, TEAL, GREEN, YELLOW, PURPLE, PINK, BROWN, GRAY = ['#4e79a7', '#f28e2b', '#e15759', '#76b7b2', '#59a14f', '#edc948', '#b07aa1', '#ff9da7', '#9c755f', '#bab0ac']
DARK = '#333333'

def sheet(w=13, h=8.2):
    fig = plt.figure(figsize=(w, h), facecolor='white'); return fig

def titles(fig, title, sub, caption):
    fig.text(0.04, 0.955, title, fontsize=19, fontweight='bold', color=DARK, va='top', ha='left')
    fig.text(0.04, 0.905, sub, fontsize=11.5, color='#555555', va='top', ha='left')
    fig.text(0.04, 0.025, caption, fontsize=9.5, color='#555555', va='bottom', ha='left', linespacing=1.4)

def style(ax, grid='y'):
    for s in ['top', 'right']: ax.spines[s].set_visible(False)
    ax.spines['left'].set_color('#c8c8c8'); ax.spines['bottom'].set_color('#c8c8c8')
    ax.tick_params(length=3)
    if grid: ax.grid(axis=grid, color='#e6e6e6', lw=0.8); ax.set_axisbelow(True)

# ---------------- life expectancy ----------------
l = pd.read_csv(f'{D}/lifespan_dataset_1960.csv', index_col=0)
l.columns = ['c', 'code', 'sex', 'year', 'le']
AGG = set('AFE AFW ARB CEB CSS EAP EAR EAS ECA ECS EMU EUU FCS HIC HPC IBD IBT IDA IDB IDX INX LAC LCN LDC LIC LMC LMY LTE MEA MIC MNA NAC OED OSS PRE PSS PST SAS SSA SSF SST TEA TEC TLA TMN TSA TSS UMC WLD'.split())
p = l.pivot_table(index=['c', 'code', 'year'], columns='sex', values='le').reset_index()
p['gap'] = p.Female - p.Male
p.to_csv(f'{INT}/lifespan_wide_with_gap.csv', index=False)

# ---- Fig 1a: lines of the female-minus-male gap by income group
inc = [('High income', BLUE), ('Upper middle income', ORANGE), ('Lower middle income', GREEN), ('Low income', RED)]
fig = sheet()
ax = fig.add_axes([0.07, 0.17, 0.70, 0.67]); style(ax)
w = p[p.c == 'World'].sort_values('year')
ax.plot(w.year, w.gap, color='#8c8c8c', lw=1.8, ls=(0, (4, 3)), label='World')
for n, col in inc:
    d = p[p.c == n].sort_values('year')
    ax.plot(d.year, d.gap, color=col, lw=2.4, label=n)
    ax.scatter([2023], [d.gap.iloc[-1]], color=col, s=28, zorder=5)
    off = {'High income': 6, 'Upper middle income': -6}.get(n, 0)
    ax.annotate(f'{d.gap.iloc[-1]:.1f}', (2023, d.gap.iloc[-1]), xytext=(7, off), textcoords='offset points', va='center', fontsize=10, color=col, fontweight='bold')
    i = d.gap.idxmax() if n == 'High income' else None
    if i is not None:
        ax.scatter([d.loc[i, 'year']], [d.loc[i, 'gap']], color=col, s=28, zorder=5)
        ax.annotate(f"Peak {d.loc[i,'gap']:.1f} yrs ({int(d.loc[i,'year'])})", (d.loc[i, 'year'], d.loc[i, 'gap']), xytext=(0, 10), textcoords='offset points', ha='center', fontsize=10, color=col, fontweight='bold')
lm = p[p.c == 'Lower middle income'].sort_values('year').iloc[0]
ax.annotate(f'{lm.gap:.1f}', (1960, lm.gap), xytext=(-6, 0), textcoords='offset points', ha='right', va='center', fontsize=10, color=GREEN, fontweight='bold')
ax.set_xlim(1958, 2026); ax.set_ylim(0, 9); ax.set_xticks(range(1960, 2021, 10)); ax.set_yticks(range(0, 10, 1))
ax.set_xlabel('Year'); ax.set_ylabel('Female minus male life expectancy at birth (years)')
ax.legend(title='Country income group', loc='upper left', bbox_to_anchor=(1.05, 0.75), frameon=False, title_fontsize=10.5, fontsize=10.5)
titles(fig, 'The female life-expectancy advantage is converging across income groups',
       'Gap between female and male life expectancy at birth, by World Bank income group, 1960-2023',
       'Gap = life expectancy (female) minus life expectancy (male), as reported by the World Bank for each income-group aggregate. Dashed gray line is the world.\n'
       'In high-income countries the gap rose to a peak of 7.5 years in 1994 and has since narrowed to 5.7; in lower-middle and low-income groups it has mostly widened, so the four groups now sit within 2 years of each other (3.8 to 5.7).\n'
       'Source: World Bank life expectancy data (course file lifespan_dataset_1960.csv).')
fig.savefig(f'{OUT}/q1a_gender_gap_lines.png', dpi=110); plt.close(fig)

# ---- Fig 1b: highlight table
rows = ['High income', 'Upper middle income', 'Lower middle income', 'Low income', 'North America', 'Europe & Central Asia', 'East Asia & Pacific',
        'Latin America & Caribbean', 'Sub-Saharan Africa', 'Middle East, North Africa, Afghanistan & Pakistan', 'South Asia']
lab = {'Middle East, North Africa, Afghanistan & Pakistan': 'Middle East, N. Africa,\nAfghanistan & Pakistan'}
yrs = [1960, 1970, 1980, 1990, 2000, 2010, 2020, 2023]
g = p[p.c.isin(rows) & p.year.isin(yrs)].pivot(index='c', columns='year', values='gap').loc[rows]
g_in, g_rg = g.iloc[:4], g.iloc[4:].sort_values(2023, ascending=False)
g = pd.concat([g_in.sort_values(2023, ascending=False), g_rg])
fig = sheet(13, 8.2)
ax = fig.add_axes([0.27, 0.17, 0.60, 0.67])
cmap = LinearSegmentedColormap.from_list('tb', ['#f0f5fa', '#a9c4de', '#4e79a7', '#1f4e79'])
vals = g.values
ax.imshow(vals, cmap=cmap, vmin=-1.5, vmax=9, aspect='auto')
nr = len(g)
# gap row between income groups and regions: draw white line
ax.axhline(3.5, color='white', lw=6)
for i in range(nr):
    for j in range(len(yrs)):
        v = vals[i, j]; ax.text(j, i, f'{v:.1f}', ha='center', va='center', fontsize=11, color='white' if v > 5.2 else DARK)
ax.set_xticks(range(len(yrs))); ax.set_xticklabels([str(y) for y in yrs]); ax.xaxis.tick_top()
ax.set_yticks(range(nr)); ax.set_yticklabels([lab.get(n, n) for n in g.index], fontsize=10.5)
for s in ax.spines.values(): s.set_visible(False)
ax.tick_params(length=0)
ax.set_xticks(np.arange(-.5, len(yrs), 1), minor=True); ax.set_yticks(np.arange(-.5, nr, 1), minor=True)
ax.grid(which='minor', color='white', lw=2); ax.tick_params(which='minor', length=0)
fig.text(0.05, 0.835, 'Income group / region', fontsize=10.5, color='#555555', ha='left')
cax = fig.add_axes([0.90, 0.40, 0.018, 0.25])
sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(-1.5, 9)); cb = fig.colorbar(sm, cax=cax); cb.outline.set_visible(False)
cb.ax.tick_params(length=0, labelsize=9.5); cax.set_title('Gap (years)', fontsize=10, loc='left')
titles(fig, 'Almost everywhere women outlive men, and the size of the gap is evening out',
       'Female minus male life expectancy at birth (years), World Bank income groups (top) and regions (bottom), selected years',
       'Each cell = female minus male life expectancy in that year; darker = larger gap. Rows sorted by the 2023 value within each block. South Asia began with men living longer (negative gap in 1960).\n'
       'Lower middle income, South Asia and Middle East & N. Africa rows have darkened the most since 1960; the North America row is lighter now than in 1980.\n'
       'Source: World Bank life expectancy data (course file lifespan_dataset_1960.csv).')
fig.savefig(f'{OUT}/q1b_gender_gap_highlight_table.png', dpi=110); plt.close(fig)

# ---- Fig 4: COVID drop
b = p[~p.code.isin(AGG)].pivot(index='c', columns='year', values='Both')
b = b[[2019, 2021, 2023]].dropna(); b['drop'] = b[2021] - b[2019]; b['rec'] = b[2023] >= b[2019]
b.to_csv(f'{INT}/covid_drop_all_countries.csv')
top = b.sort_values('drop').head(15).iloc[::-1]
fig = sheet(13, 8.2)
ax = fig.add_axes([0.20, 0.17, 0.58, 0.67]); style(ax, 'x')
cols = [BLUE if r else ORANGE for r in top.rec]
ax.barh(range(len(top)), top['drop'], color=cols, height=0.7)
ax.set_yticks(range(len(top))); ax.set_yticklabels(top.index, fontsize=10.5)
for i, (n, r) in enumerate(top.iterrows()):
    ax.text(r['drop'] - 0.08, i, f"{r['drop']:.1f}", va='center', ha='right', fontsize=10, color=DARK)
    ax.text(0.12, i, f"{r[2019]:.1f} → {r[2021]:.1f} → {r[2023]:.1f}", va='center', ha='left', fontsize=9.5, color='#666666')
med = b['drop'].median()
ax.axvline(med, color=RED, lw=1.3, ls='--'); ax.text(med + 0.08, -0.85, f'Median of all {len(b)} countries: {med:.1f}', color=RED, fontsize=9.5, ha='left'); ax.set_ylim(-1.1, len(top) + 0.3)
ax.set_xlim(-7.3, 3.3); ax.set_xticks(range(-7, 1)); ax.set_xlabel('Change in life expectancy at birth, 2019 to 2021 (years)')
ax.spines['left'].set_visible(False); ax.tick_params(axis='y', length=0)
ax.text(0.12, len(top) - 0.05 + 0.0, '2019 → 2021 → 2023 (years)', fontsize=9.5, color='#666666', ha='left', va='bottom')
fig.legend(handles=[Patch(color=BLUE, label='Recovered by 2023'), Patch(color=ORANGE, label='Still below 2019 level')],
           title='Life expectancy vs 2019', loc='upper left', bbox_to_anchor=(0.80, 0.70), frameon=False, fontsize=10.5, title_fontsize=10.5)
nrec = int(top.rec.sum())
titles(fig, 'The pandemic cut life expectancy by up to 6 years, but nearly all hard-hit countries recovered',
       'The 15 countries with the largest fall in life expectancy at birth (both sexes) between 2019 and 2021, World Bank data',
       f'Bars show the change from 2019 to 2021 (years); the gray text gives 2019, 2021 and 2023 values. {nrec} of these 15 countries were back at or above their 2019 level by 2023.\n'
       'Countries only (World Bank regional and income aggregates removed). Descriptive only: the data do not say what caused each change.\n'
       'Source: World Bank life expectancy data (course file lifespan_dataset_1960.csv).')
fig.savefig(f'{OUT}/q4_covid_life_expectancy_drop.png', dpi=110); plt.close(fig)
print(top[[2019, 2021, 2023, 'drop', 'rec']].round(1)); print('median', med, 'n', len(b), 'share fell', (b['drop'] < 0).mean(), 'n rec all', b.rec.mean())

# ---------------- census ----------------
c = pd.read_csv(f'{D}/full_census_dataset.csv', dtype={'FIPS Code': str}, encoding='latin-1')
R = 'Rural Urban Continuum Code 2023'
c = c[c[R].notna()].copy(); c['rucc'] = c[R].astype(int)
c['grp'] = pd.cut(c.rucc, [0, 1, 3, 9], labels=['Large metro (code 1)', 'Smaller metro (codes 2-3)', 'Nonmetro (codes 4-9)'])
def urate(df, by):
    out = {}
    for y in range(2000, 2024):
        gg = df.groupby(by).apply(lambda d: d[f'Unemployed {y}'].sum() / d[f'Civilian labor force {y}'].sum() * 100)
        out[y] = gg
    return pd.DataFrame(out).T
ug = urate(c, 'grp'); uc = urate(c, 'rucc')
ug.to_csv(f'{INT}/unemp_by_group.csv'); uc.to_csv(f'{INT}/unemp_by_rucc.csv')
allu = {y: c[f'Unemployed {y}'].sum() / c[f'Civilian labor force {y}'].sum() * 100 for y in range(2000, 2024)}

# ---- Fig 2a
fig = sheet(); ax = fig.add_axes([0.07, 0.17, 0.70, 0.67]); style(ax)
gcol = {'Large metro (code 1)': RED, 'Smaller metro (codes 2-3)': ORANGE, 'Nonmetro (codes 4-9)': BLUE}
for k, col in gcol.items():
    ax.plot(ug.index, ug[k], color=col, lw=2.4, label=k)
ax.axvline(2020, color='#999999', lw=1, ls=':')
ax.annotate(f"2020: large metro {ug.loc[2020,'Large metro (code 1)']:.1f}%\nnonmetro {ug.loc[2020,'Nonmetro (codes 4-9)']:.1f}%", (2020, ug.loc[2020, 'Large metro (code 1)']), xytext=(-12, 6), textcoords='offset points', ha='right', fontsize=10, color=RED, fontweight='bold')
ax.annotate(f"2010: nonmetro {ug.loc[2010,'Nonmetro (codes 4-9)']:.1f}%\nlarge metro {ug.loc[2010,'Large metro (code 1)']:.1f}%", (2010, ug.loc[2010, 'Nonmetro (codes 4-9)']), xytext=(0, 8), textcoords='offset points', ha='center', fontsize=10, color=BLUE, fontweight='bold')
ax.text(2000.4, 7.6, '2000-2019: nonmetro counties\nhad the higher rate every year', ha='left', fontsize=9.5, color='#555555')
ax.set_xlim(2000, 2023.5); ax.set_ylim(0, 11); ax.set_xticks([2000, 2005, 2010, 2015, 2020, 2023]); ax.set_yticks(range(0, 12, 2))
ax.yaxis.set_major_formatter(lambda v, _: f'{v:.0f}%')
ax.set_xlabel('Year'); ax.set_ylabel('Unemployment rate (unemployed / civilian labor force)')
ax.legend(title='Rural-urban continuum', loc='upper left', bbox_to_anchor=(1.03, 0.7), frameon=False, fontsize=10.5, title_fontsize=10.5)
titles(fig, 'In 2020 the pandemic hit big-city unemployment hardest, reversing the usual rural penalty',
       'County unemployment rate by 2023 USDA rural-urban group, 2000-2023 (pooled across counties)',
       'Rates are pooled: total unemployed divided by total civilian labor force for all counties in the group, so large counties count in proportion to their size.\n'
       'Counties without a 2023 rural-urban code (17 Alaska/Connecticut/Montana areas) are excluded. Descriptive only: the data do not show why the pattern changed.\n'
       'Source: USDA ERS county data (course file full_census_dataset.csv).')
fig.savefig(f'{OUT}/q2a_unemployment_lines.png', dpi=110); plt.close(fig)

# ---- Fig 2b: bar of change 2019 -> 2020 by code
ch = (uc.loc[2020] - uc.loc[2019]); n = {1: 'Metro, 1M+ pop.', 2: 'Metro, 250K-1M', 3: 'Metro, <250K', 4: 'Urban 20K+, adjacent', 5: 'Urban 20K+, not adjacent',
                                          6: 'Urban 5-20K, adjacent', 7: 'Urban 5-20K, not adjacent', 8: 'Rural <5K, adjacent', 9: 'Rural <5K, not adjacent'}
fig = sheet(); ax = fig.add_axes([0.25, 0.17, 0.55, 0.67]); style(ax, 'x')
ys = np.arange(9)[::-1]
cl = [RED if k <= 3 else BLUE for k in ch.index]
ax.barh(ys, ch.values, color=cl, height=0.7)
for y, v, k in zip(ys, ch.values, ch.index):
    ax.text(v + 0.05, y, f'+{v:.1f}', va='center', fontsize=10.5, color=DARK, fontweight='bold')
    ax.text(0.08, y, f'{uc.loc[2019,k]:.1f}% → {uc.loc[2020,k]:.1f}%', va='center', fontsize=9.5, color='white')
ax.set_yticks(ys); ax.set_yticklabels([f'{k}  {n[k]}' for k in ch.index], fontsize=10.5)
avg = allu[2020] - allu[2019]
ax.axvline(avg, color=DARK, lw=1.2, ls='--'); ax.text(avg - 0.05, 8.62, f'All counties: +{avg:.1f}', fontsize=9.5, ha='right', color=DARK)
ax.set_xlim(0, 6); ax.set_ylim(-0.6, 9.0); ax.set_xlabel('Rise in unemployment rate, 2019 to 2020 (percentage points)')
ax.spines['left'].set_visible(False); ax.tick_params(axis='y', length=0)
ax.set_ylabel('Rural-urban continuum code (2023)', labelpad=8)
fig.legend(handles=[Patch(color=RED, label='Metro (codes 1-3)'), Patch(color=BLUE, label='Nonmetro (codes 4-9)')], title='County type', loc='upper left', bbox_to_anchor=(0.82, 0.70), frameon=False, fontsize=10.5, title_fontsize=10.5)
titles(fig, 'Unemployment jumped most in the biggest metro counties in 2020, and least in remote rural ones',
       'Change in pooled county unemployment rate from 2019 to 2020, by rural-urban continuum code',
       'White text inside each bar gives the 2019 and 2020 unemployment rates. Codes follow the USDA 2023 rural-urban continuum (1 = largest metro areas, 9 = most remote rural counties).\n'
       'Dashed line marks the pooled change across all counties. Counties without a 2023 code are excluded.\n'
       'Source: USDA ERS county data (course file full_census_dataset.csv).')
fig.savefig(f'{OUT}/q2b_unemployment_change_bars.png', dpi=110); plt.close(fig)
print(ug.loc[[2000, 2010, 2019, 2020, 2021, 2023]].round(2)); print(ch.round(2)); print(allu[2019], allu[2020])

# ---- Fig 3: education dumbbell
eo = {}
for y in ['1990', '2000', '2008-12', '2019-23']:
    nn = c[f"Bachelor's degree or higher, {y}"]; pp = c[f"Percent of adults with a bachelor's degree or higher, {y}"]
    dd = (nn / (pp / 100)).where(pp > 0)
    t = pd.DataFrame({'n': nn, 'd': dd, 'k': c.rucc}).dropna().groupby('k').sum()
    eo[y] = t.n / t.d * 100
eo = pd.DataFrame(eo); eo.to_csv(f'{INT}/bachelors_pct_by_rucc.csv')
fig = sheet(); ax = fig.add_axes([0.25, 0.17, 0.55, 0.67]); style(ax, 'x')
for y, k in zip(ys, eo.index):
    a, z = eo.loc[k, '1990'], eo.loc[k, '2019-23']
    col = RED if k <= 3 else BLUE
    ax.plot([a, z], [y, y], color='#bdbdbd', lw=3, zorder=1)
    ax.scatter([a], [y], s=70, facecolor='white', edgecolor=col, lw=2, zorder=3)
    ax.scatter([z], [y], s=70, color=col, zorder=3)
    ax.text(a - 0.8, y, f'{a:.0f}%', ha='right', va='center', fontsize=10, color='#555555')
    ax.text(z + 0.8, y, f'{z:.0f}%  (+{z-a:.0f} pts)', ha='left', va='center', fontsize=10, color=col, fontweight='bold')
ax.set_yticks(ys); ax.set_yticklabels([f'{k}  {n[k]}' for k in eo.index], fontsize=10.5)
ax.set_xlim(4, 52); ax.set_ylim(-0.6, 8.6); ax.set_xticks(range(5, 51, 5)); ax.xaxis.set_major_formatter(lambda v, _: f'{v:.0f}%')
ax.spines['left'].set_visible(False); ax.tick_params(axis='y', length=0)
ax.set_xlabel("Adults 25+ with a bachelor's degree or higher"); ax.set_ylabel('Rural-urban continuum code (2023)', labelpad=8)
fig.legend(handles=[Line2D([], [], marker='o', ls='', mfc='white', mec='#555555', mew=2, ms=8, label='1990'), Line2D([], [], marker='o', ls='', color='#555555', ms=8, label='2019-23'),
                    Patch(color=RED, label='Metro (codes 1-3)'), Patch(color=BLUE, label='Nonmetro (codes 4-9)')], loc='upper left', bbox_to_anchor=(0.82, 0.70), frameon=False, fontsize=10.5)
gap90, gap20 = eo.loc[1, '1990'] - eo.loc[9, '1990'], eo.loc[1, '2019-23'] - eo.loc[9, '2019-23']
titles(fig, 'Every kind of county gained degrees, but the metro-rural education gap grew wider',
       "Share of adults with a bachelor's degree or higher, 1990 vs 2019-23, by rural-urban continuum code",
       f"The gap between the largest metro counties and the most remote rural counties grew from {gap90:.0f} to {gap20:.0f} percentage points, even though rural counties roughly doubled their share ({eo.loc[9,'1990']:.0f}% to {eo.loc[9,'2019-23']:.0f}%).\n"
       "Shares are pooled (degree holders / adults 25+ across all counties in a code; adults 25+ recovered as count / percent). Counties without a 2023 code are excluded.\n"
       'Source: USDA ERS county data (course file full_census_dataset.csv).')
fig.savefig(f'{OUT}/q3_education_dumbbell.png', dpi=110); plt.close(fig)
print(eo.round(1), gap90, gap20)
