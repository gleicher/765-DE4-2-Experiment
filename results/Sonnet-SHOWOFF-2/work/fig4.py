from common import *
o = load_owid()
c = o[(o.Code.notna() & ~o.Code.astype(str).str.startswith('OWID')) | (o.Entity == 'USSR')]
c = c[c.Year >= 1950].sort_values(['Entity', 'Year']).copy()
c = c[c.Entity != 'USSR']  # USSR overlaps its successor states; keep 235 modern countries
N = c.Entity.nunique(); print(N)
c['d'] = c.groupby('Entity').LE.diff()
cnt = c[c.d <= -1].groupby('Year').size().reindex(range(1951, 2024), fill_value=0)
base = cnt.drop([2020, 2021, 2022]).median(); print('median', base, cnt.drop([2020, 2021, 2022]).max(), cnt[[2020, 2021, 2022]].tolist())
# episodes
rows = []
for e, g in c.groupby('Entity'):
    L = g.LE.values; Y = g.Year.values; i = 1
    while i < len(g):
        if L[i] < L[i - 1]:
            j = i
            while j + 1 < len(g) and L[j + 1] < L[j]: j += 1
            peak = L[i - 1]; k = j
            while k < len(g) and L[k] < peak: k += 1
            rows.append((e, Y[i - 1], Y[j], peak - L[j], (Y[k] - Y[j]) if k < len(g) else np.nan))
            i = j + 1
        else: i += 1
ep = pd.DataFrame(rows, columns=['e', 'start', 'trough', 'loss', 'rec'])
big = ep[ep.loss >= 5].copy(); print(len(big), big.groupby(big.trough // 10 * 10).size().to_dict())
big.to_csv('fig4_episodes_5yr.csv', index=False)
fig = plt.figure(figsize=(12, 10))
gs = fig.add_gridspec(2, 1, height_ratios=[1, 1.15], hspace=0.30, left=0.08, right=0.96, top=0.835, bottom=0.20)
ax = fig.add_subplot(gs[0]); ax2 = fig.add_subplot(gs[1], sharex=ax)
cols = ['#b5481b' if y in (2020, 2021) else '#9aa3ad' for y in cnt.index]
ax.bar(cnt.index, cnt.values, color=cols, width=0.78, zorder=3)
ax.axhline(base, color=INK2, lw=1, ls='--', zorder=4)
ax.text(1951, base + 1.6, f'typical year (median, excluding 2020-22): {base:.0f} countries', fontsize=9.5, color=INK2)
for y in (2020, 2021):
    ax.text(y, cnt[y] + 1.5, f'{cnt[y]}', ha='center', fontsize=11, fontweight='bold', color='#b5481b')
ax.text(2018.6, 78, 'COVID-19\n2020-21', ha='right', fontsize=10.5, color='#b5481b', fontweight='bold', va='top')
ax.annotate('Soviet collapse,\nRwanda, Bosnia', (1993, cnt[1993]), xytext=(1984, 40), fontsize=9.5, color=INK2, ha='center', arrowprops=dict(arrowstyle='-', color=MUTED))
ax.annotate('HIV/AIDS, Cold-War\nfamines and wars', (1975, cnt[1975]), xytext=(1963, 30), fontsize=9.5, color=INK2, ha='center', arrowprops=dict(arrowstyle='-', color=MUTED))
ax.set_ylim(0, 80); ax.set_ylabel(f'Countries whose life expectancy\nfell by 1+ year (of {N})'); clean_grid(ax)
plt.setp(ax.get_xticklabels(), visible=False)
ax.set_title('A. How many countries had a setback each year?', loc='left', fontsize=12.5, color=INK)
# panel B
rc = big.rec.fillna(40)
cmap = {1: '#2b6f94', 2: '#7fb3d5'}
def colr(r):
    if np.isnan(r): return '#7a1f0b'
    return '#d9a441' if r <= 3 else ('#c1622a' if r <= 10 else '#7a1f0b')
ax2.scatter(big.trough, big.loss, s=np.where(big.trough >= 2020, 40, 40), c=[colr(r) for r in big.rec], alpha=0.85, lw=0.6, edgecolor='white', zorder=3)
ax2.set_yscale('log'); ax2.set_ylim(4.6, 50); ax2.set_yticks([5, 10, 20, 40]); ax2.set_yticklabels(['5', '10', '20', '40']); ax2.minorticks_off()
ax2.set_ylabel('Years of life expectancy lost\n(peak to trough, log scale)'); clean_grid(ax2)
def ann2(t, xy, xyt, ha='right'):
    ax2.annotate(t, xy, xytext=xyt, fontsize=9, color=INK2, ha=ha, va='center', arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7, shrinkA=1, shrinkB=3))
ann2('Rwanda 1994 (genocide)', (1994, 39.5), (1986, 40))
ann2('Central African Rep. 2009', (2009, 35.2), (2002, 38.5))
ann2('Lebanon 1976', (1976, 30.0), (1969, 33))
ann2('Cambodia 1975-77', (1977, 28.0), (1982, 29.5), ha='left')
ann2('Bangladesh 1971', (1971, 22.2), (1964, 24))
ann2('Somalia 1992, Bosnia 1993', (1992, 21.9), (1988.5, 25.5), ha='right')
ann2('China 1960 (famine)', (1960, 15.4), (1953, 18.5), ha='left')
ann2('Eswatini, Zimbabwe\n(HIV/AIDS)', (2004, 18.0), (1999.5, 25.5), ha='left')
ann2('', (2001, 16.5), (1999.5, 25.5), ha='left')
ann2('South Sudan 2017', (2017, 22.9), (2013.5, 31))
n6 = len(big[big.trough.between(2020, 2021)]); print('covid-era large', n6, big[big.trough.between(2020, 2021)].loss.max())
ax2.text(2023.6, 5.0, f'COVID-19 era: only {n6} of {len(big)} large\nsetbacks bottomed out in 2020-21,\nnone deeper than {big[big.trough.between(2020, 2021)].loss.max():.0f} years', fontsize=9.5, ha='right', va='bottom', color='#b5481b', fontweight='bold')
from matplotlib.lines import Line2D
fig.legend([Line2D([], [], marker='o', ls='', color=c_, markersize=8) for c_ in ['#d9a441', '#c1622a', '#7a1f0b']],
           ['regained pre-setback level within 3 years', '4-10 years', '11+ years, or not yet by 2023'], title='Time to recover', title_fontsize=9.5, fontsize=9.5,
           loc='lower center', ncol=3, frameon=False, bbox_to_anchor=(0.53, 0.095))
ax2.set_xlim(1949.5, 2024); ax2.set_xlabel('Year')
ax2.set_title('B. How big were the large setbacks (5+ years lost), and how long did recovery take?', loc='left', fontsize=12.5, color=INK)
header(fig, 'COVID-19 was the first time in the 1950-2023 record that setbacks went global',
       f'In a typical year only about {base:.0f} of {N} countries saw life expectancy fall by a year or more. In 2020 and 2021, {cnt[2020]} and {cnt[2021]} did.\n'
       'But the deepest losses on record are local catastrophes (wars, genocide, famine, HIV/AIDS): COVID-19 was broad, not usually deep.')
caption(fig, f'Our World in Data / UN World Population Prospects 2024 (period life expectancy at birth, 1950-2023, {N} countries and territories; the USSR series and regional aggregates are excluded). '
        'A "setback" in B is an uninterrupted run of annual declines whose total loss is at least 5 years; recovery = years from the trough until life expectancy is back at the pre-decline level. '
        'Several countries appear more than once. Central African Republic estimates (2009, 2019, 2022) are extreme and should be read with caution.', width=170)
save(fig, 'fig4_global_setbacks.png')
