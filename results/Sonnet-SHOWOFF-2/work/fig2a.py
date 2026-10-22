from common import *
d = load_census(); d['grp'] = d.rucc.map(grp_of)
yrs = list(range(2000, 2024))
rows = {}
for gname, _ in GROUPS:
    s = d[d.grp == gname]; r = []
    for y in yrs:
        m = s[[f'Unemployed {y}', f'Civilian labor force {y}']].dropna()
        r.append(100 * m.iloc[:, 0].sum() / m.iloc[:, 1].sum())
    rows[gname] = r
u = pd.DataFrame(rows, index=yrs); u.to_csv('fig2_unemployment_by_group.csv')
gap = u['Rural nonmetro (8-9)'] - u['Large metro (RUCC 1)']
print(u.round(2).loc[[2007,2009,2010,2019,2020,2021,2023]]); print(gap.round(2).loc[[2007,2009,2010,2019,2020,2021,2023]])
fig = plt.figure(figsize=(11, 9.6))
gs = fig.add_gridspec(2, 1, height_ratios=[3.1, 1.25], hspace=0.14, left=0.075, right=0.95, top=0.835, bottom=0.14)
ax = fig.add_subplot(gs[0]); ax2 = fig.add_subplot(gs[1], sharex=ax)
for y0, y1, lab in [(2007.9, 2009.9, ''), (2019.9, 2020.9, '')]:
    pass
for a in (ax, ax2):
    a.axvspan(2007.5, 2010.5, color='#f3f4f6', zorder=0); a.axvspan(2019.5, 2021.5, color='#f3f4f6', zorder=0)
for gname, _ in GROUPS:
    ax.plot(yrs, u[gname], color=GCOL[gname], lw=2.6, zorder=3)
    ax.scatter([2023], [u[gname].iloc[-1]], color=GCOL[gname], s=24, zorder=4)
for gname, _ in GROUPS:
    ax.plot([], [], color=GCOL[gname], lw=2.6, label=gname)
ax.legend(loc='upper left', frameon=False, fontsize=10.5, bbox_to_anchor=(0.0, 0.93), title='County setting', title_fontsize=10, alignment='left')
ax.text(2023.0, 3.05, 'by 2022-23 all four groups\nare back together at 3.7%', ha='right', fontsize=9.5, color=INK2)
ax.text(2009, 11.9, 'Great Recession', ha='center', fontsize=10.5, color=INK2, fontweight='bold')
ax.text(2020.5, 11.9, 'Pandemic', ha='center', fontsize=10.5, color=INK2, fontweight='bold')
ax.annotate('2010: gap nearly closes\n(rural 9.8% vs metro 9.7%)', (2010, 9.9), xytext=(2012.2, 11.1), fontsize=9.5, color=INK2,
            arrowprops=dict(arrowstyle='-', color=MUTED))
ax.annotate('2020: big metros jump to 8.6%,\nrural counties only to 6.5%', (2020, 8.6), xytext=(2013.0, 8.8), fontsize=9.5, color=INK2,
            ha='left', arrowprops=dict(arrowstyle='-', color=MUTED))
ax.set_ylim(2.5, 12.6); ax.set_ylabel('Unemployment rate (%)'); clean_grid(ax); plt.setp(ax.get_xticklabels(), visible=False)
cols = np.where(gap >= 0, GCOL['Rural nonmetro (8-9)'], GCOL['Large metro (RUCC 1)'])
ax2.bar(yrs, gap, color=cols, width=0.72, zorder=3)
ax2.axhline(0, color=INK2, lw=1)
ax2.set_ylabel('Rural minus\nlarge metro (pts)'); ax2.set_ylim(-2.9, 1.4); clean_grid(ax2)
ax2.annotate(f'{gap[2020]:+.1f}', (2020, gap[2020]), xytext=(2020, gap[2020] - 0.35), ha='center', va='top', fontsize=10, fontweight='bold', color=GCOL['Large metro (RUCC 1)'])
ax2.text(2011.0, 1.3, 'rural counties worse off', fontsize=9.5, color=GCOL['Rural nonmetro (8-9)'], va='top', fontweight='bold')
ax2.text(2011.0, -1.9, 'big metros worse off', fontsize=9.5, color=GCOL['Large metro (RUCC 1)'], va='bottom', fontweight='bold')
ax2.set_xlim(1999.4, 2023.6); ax2.set_xticks(range(2000, 2024, 4)); ax2.set_xlabel('Year')
header(fig, 'In 2020 the unemployment penalty flipped from rural America to the big cities',
       'From 2000 to 2019 rural counties had the higher unemployment rate every year (the Great Recession nearly closed the gap).\n'
       'The pandemic reversed the order in 2020 and 2021, the only two years in this record when big metros were worse off.')
caption(fig, 'US counties (Rural-Urban Continuum Codes, 2023 edition) grouped into four settings; each line is the labor-force-weighted unemployment rate '
        '(sum of unemployed people / sum of civilian labor force) of all counties in the group, 2000-2023 (USDA ERS). Bars show rural (RUCC 8-9) minus largest-metro (RUCC 1). '
        '17 counties without a 2023 code (e.g. Connecticut, whose county boundaries were replaced) are excluded. Descriptive only, not causal.', width=160)
save(fig, 'fig2a_unemployment_flip_lines.png')
