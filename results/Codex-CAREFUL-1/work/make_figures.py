"""Reproduce six DE4-2 figures using only the supplied course data."""
from pathlib import Path
import os
ROOT=Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR', str(ROOT/'work'/'mpl-cache'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm, LinearSegmentedColormap
from matplotlib.lines import Line2D
from matplotlib.ticker import PercentFormatter
import pandas as pd
import numpy as np
OUT=ROOT/'answers'/'figures'; OUT.mkdir(parents=True,exist_ok=True)
WORK=ROOT/'work'
BLUE='#32658A'; ORANGE='#B96532'; TEAL='#32796D'; DARK='#25313B'; GRAY='#7B8790'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'text.color':DARK,'axes.labelcolor':DARK,'xtick.color':DARK,'ytick.color':DARK,'axes.edgecolor':'#CDD2D5','axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'white','axes.facecolor':'white','savefig.facecolor':'white'})
def heading(f,title,sub):
 f.text(.07,.95,title,fontsize=21,fontweight='bold',va='top')
 f.text(.07,.897,sub,fontsize=11.5,va='top',color='#52606B',linespacing=1.5)
def footer(f,txt):
 f.text(.07,.035,txt,fontsize=9,color='#52606B',va='bottom',linespacing=1.5)
def finish(f,name):
 f.savefig(OUT/name,dpi=180); plt.close(f)
def grid(ax,axis='y'):
 ax.set_axisbelow(True); ax.grid(axis=axis,color='#E7EAED',lw=.8)
life=pd.read_csv(ROOT/'data'/'lifespan_dataset_1960.csv')
assert not life.duplicated(['Country Code','Sex','Year']).any()
p=life.pivot(index=['Country Name','Year'],columns='Sex',values='Life Expectancy (years)')
# Six illustrative countries, not a representative sample or a ranking of all countries.
countries=['France','Sweden','Hungary','United States','Poland','Japan']
rows=[]
for country in countries:
 for year in range(1990,2024):
  r=p.loc[(country,year)]
  rows.append({'country':country,'year':year,'male':r.Male,'female':r.Female,'gap':r.Female-r.Male})
gaps=pd.DataFrame(rows); gaps.to_csv(WORK/'life_gap_data.csv',index=False)
f,axs=plt.subplots(2,3,figsize=(12,8.5),sharex=True,sharey=True)
f.subplots_adjust(left=.08,right=.96,top=.78,bottom=.19,wspace=.17,hspace=.35)
heading(f,'The lifespan gap narrowed — but not everywhere',
        'Female and male life expectancy at birth, 1990–2023 · six illustrative countries')
f.legend(handles=[Line2D([0],[0],color=BLUE,lw=2.5,label='Female'),Line2D([0],[0],color=ORANGE,lw=2.5,label='Male')],loc='upper right',bbox_to_anchor=(.96,.86),frameon=False,ncol=2)
for ax,country in zip(axs.flat,countries):
 d=gaps[gaps.country.eq(country)]
 ax.fill_between(d.year,d.male,d.female,color=BLUE,alpha=.09)
 ax.plot(d.year,d.female,color=BLUE,lw=2.3); ax.plot(d.year,d.male,color=ORANGE,lw=2.3)
 ax.set_title(country,loc='left',fontsize=12,fontweight='bold',pad=10)
 ax.set_xlim(1990,2023); ax.set_ylim(63,90); ax.set_xticks([1990,2005,2023]); ax.set_yticks([65,70,75,80,85,90]); grid(ax)
 a,b=d.iloc[0],d.iloc[-1]
 ax.text(.02,.025,f'Gap: {a.gap:.1f} → {b.gap:.1f} years',transform=ax.transAxes,fontsize=10)
f.text(.028,.49,'Life expectancy at birth (years)',rotation=90,va='center',fontsize=11)
f.text(.52,.125,'Year',ha='center')
footer(f,'Source: course-supplied World Bank lifespan data. Shading shows the female–male gap; panels use identical axes.\nCountry selection illustrates contrasting trajectories. These are descriptive estimates, not individual lifespans or causes.')
finish(f,'01_life_gap_trajectories.png')
# Alternate: endpoint gaps only, sorted by the amount of narrowing.
end=gaps[gaps.year.isin([1990,2023])].pivot(index='country',columns='year',values='gap')
end['change']=end[2023]-end[1990]; end=end.sort_values('change')
end.to_csv(WORK/'gap_endpoints.csv')
f,ax=plt.subplots(figsize=(11,7.5)); f.subplots_adjust(left=.21,right=.84,top=.77,bottom=.23)
heading(f,'France and Sweden saw the largest narrowing',
 'Female minus male life expectancy, 1990 and 2023 · same six countries as the trajectory view')
for i,(country,r) in enumerate(end.iterrows()):
 ax.plot([r[1990],r[2023]],[i,i],color='#B5BDC3',lw=4,zorder=1)
 ax.scatter(r[1990],i,s=90,facecolors='white',edgecolors=GRAY,lw=2,zorder=3)
 ax.scatter(r[2023],i,s=90,color=BLUE,zorder=4)
 ax.text(9.9,i,f'{r.change:+.1f}',ha='right',va='center',fontsize=11)
 ax.text(r[2023]-.12,i+.24,f'{r[2023]:.1f}',color=BLUE,ha='right',fontsize=10)
 ax.text(r[1990]+.12,i-.23,f'{r[1990]:.1f}',color=GRAY,ha='left',fontsize=10)
ax.set_yticks(range(len(end)),end.index); ax.set_ylim(len(end)-.35,-.8); ax.set_xlim(0,10)
ax.set_xticks(range(0,10,2)); ax.set_xlabel('Female–male gap (years)'); grid(ax,'x')
ax.spines['left'].set_visible(False); ax.tick_params(axis='y',length=0,pad=12)
ax.text(9.9,-.66,'Change\n(years)',ha='right',fontsize=10)
f.legend(handles=[Line2D([0],[0],marker='o',color='none',markeredgecolor=GRAY,markerfacecolor='white',markersize=8,label='1990'),Line2D([0],[0],marker='o',color='none',markerfacecolor=BLUE,markersize=8,label='2023')],loc='upper right',bbox_to_anchor=(.87,.86),frameon=False,ncol=2)
footer(f,'Source: course-supplied World Bank lifespan data. Negative change means a smaller female advantage.\nCountries are ordered by change, not by the 2023 gap. Endpoints omit intervening fluctuations; numbers are rounded to 0.1 year.')
finish(f,'02_life_gap_endpoints.png')
# Census CSV is comma-delimited despite the readme's tab-delimited warning, and uses cp1252.
c=pd.read_csv(ROOT/'data'/'full_census_dataset.csv',encoding='cp1252',dtype={'FIPS Code':str})
assert not c['FIPS Code'].duplicated().any()
empcols=[f'Employed {y}' for y in range(2007,2024)]
base=c[c.State.ne('PR') & c['2013 Rural-urban Continuum Code'].between(1,9)].copy()
e=base.dropna(subset=empcols).copy()
e['group']=np.select([e['2013 Rural-urban Continuum Code'].eq(1),e['2013 Rural-urban Continuum Code'].between(2,3)],['Metro: code 1','Metro: codes 2–3'],default='Nonmetro: codes 4–9')
groups=['Metro: code 1','Metro: codes 2–3','Nonmetro: codes 4–9']; colors=[BLUE,TEAL,ORANGE]
sums=e.groupby('group')[empcols].sum().reindex(groups); sums.columns=list(range(2007,2024)); idx=sums.div(sums[2007],axis=0)*100
sums.to_csv(WORK/'employed_group_totals.csv'); idx.to_csv(WORK/'employment_index.csv')
ns=e.groupby('group').size().reindex(groups)
f,ax=plt.subplots(figsize=(11.5,7.7)); f.subplots_adjust(left=.1,right=.76,top=.78,bottom=.23)
heading(f,'Nonmetro employment still trailed 2007 in 2023',
 'Employed residents, indexed to 2007 = 100 · fixed groups of counties, using 2013 rural–urban codes')
for g,col in zip(groups,colors):
 ax.plot(idx.columns,idx.loc[g],color=col,lw=2.8)
 v=idx.loc[g,2023]; ax.scatter(2023,v,color=col,s=38,zorder=4)
 ax.text(2023.45,v,f'{g}\n{v:.1f}  ({v-100:+.1f}%)',color=col,va='center',fontsize=11,linespacing=1.4)
ax.axhline(100,color=GRAY,ls='--',lw=1.1); ax.text(2007.2,100.8,'2007 baseline',fontsize=9,color=GRAY)
ax.set_xlim(2007,2023); ax.set_ylim(88,119); ax.set_xticks([2007,2010,2013,2016,2019,2023]); ax.set_yticks([90,95,100,105,110,115]); grid(ax)
ax.set_ylabel('Employed-resident index (2007 = 100)'); ax.set_xlabel('Year')
footer(f,f'Source: course-supplied USDA county data. {len(e):,} counties/equivalents in 50 states + DC; Puerto Rico excluded.\nSum employed residents within each fixed group, then divide by that group’s 2007 total. Seven incomplete county series excluded.\n2013 codes are held fixed; this is employment by residence, not a job-location count, employment rate, or causal effect.')
finish(f,'03_employment_lines.png')
# Alternate: annual percentage departure from baseline, fixed symmetric color scale.
vals=idx-100
f,ax=plt.subplots(figsize=(12,7.6)); f.subplots_adjust(left=.2,right=.94,top=.70,bottom=.36)
heading(f,'Nonmetro counties never regained the 2007 total',
 'Annual change in employed residents relative to 2007 · blue = above baseline; orange = below')
im=ax.imshow(vals.values,cmap=LinearSegmentedColormap.from_list('employment',[ORANGE,'#F7F7F7',BLUE]),norm=TwoSlopeNorm(vmin=-16,vcenter=0,vmax=16),aspect='auto')
ax.set_xticks(range(17),list(range(2007,2024)),rotation=45,ha='right',fontsize=9)
ax.set_yticks(range(3),[f'{g}\n(n = {ns[g]:,})' for g in groups],fontsize=11)
ax.tick_params(length=0,pad=9); ax.spines[['left','bottom']].set_visible(False)
for row in range(3):
 for col in range(17):
  v=vals.iloc[row,col]; ax.text(col,row,('0' if round(v)==0 else f'{v:+.0f}'),ha='center',va='center',fontsize=9,color='white' if abs(v)>10 else DARK)
ax.set_xticks(np.arange(-.5,17,1),minor=True); ax.set_yticks(np.arange(-.5,3,1),minor=True)
ax.grid(which='minor',color='white',linewidth=2); ax.tick_params(which='minor',bottom=False,left=False)
cax=f.add_axes([.35,.235,.42,.027]); cb=f.colorbar(im,cax=cax,orientation='horizontal',ticks=[-16,-8,0,8,16]); cb.ax.xaxis.set_major_formatter(PercentFormatter(xmax=100,decimals=0)); cb.set_label('Change from each group’s 2007 employed-resident total',fontsize=10)
footer(f,f'Source: course-supplied USDA county data. Same {len(e):,}-county complete-series cohort as the line view; 50 states + DC.\n2013 rural–urban codes held fixed. Group totals are summed before indexing; cells are rounded to whole percent.\nCounts in labels are counties, not residents. Puerto Rico and seven incomplete series excluded; colors share a symmetric scale.')
finish(f,'04_employment_heatmap.png')
# Third story: denominator is natural-decline counties, not all counties.
n=c[c.State.ne('PR') & c['2023 Rural-urban Continuum Code'].between(1,9)].dropna(subset=['Natural Change Rate 2023','Net Migration Rate 2023']).copy()
t=[]
for code in range(1,10):
 d=n[n['2023 Rural-urban Continuum Code'].eq(code)]; loss=d[d['Natural Change Rate 2023']<0]
 win=(loss['Net Migration Rate 2023']+loss['Natural Change Rate 2023']>0).sum()
 t.append({'code':code,'all_counties':len(d),'natural_decline_counties':len(loss),'offset_counties':win,'offset_percent':100*win/len(loss)})
t=pd.DataFrame(t); t.to_csv(WORK/'migration_offsets.csv',index=False)
f,ax=plt.subplots(figsize=(11.5,8.4)); f.subplots_adjust(left=.20,right=.83,top=.75,bottom=.23)
heading(f,'Migration offset natural loss less often outside metros',
 'Among counties with more deaths than births in 2023, what share gained enough migrants to offset the loss?')
y=np.arange(9)
ax.barh(y,t.offset_percent,color=TEAL,height=.62,label='Migration exceeded natural loss')
ax.barh(y,100-t.offset_percent,left=t.offset_percent,color='#DCE2E5',height=.62,label='Did not exceed natural loss')
for i,r in t.iterrows():
 ax.text(r.offset_percent/2,i,f'{r.offset_percent:.0f}%',ha='center',va='center',fontweight='bold',color='white',fontsize=11)
 ax.text(103,i,f'{int(r.offset_counties):,} / {int(r.natural_decline_counties):,}',va='center',fontsize=10)
ax.set_xlim(0,100); ax.set_ylim(8.6,-1.05); ax.set_yticks(y,[f'Metro · code {i}' if i<4 else f'Nonmetro · code {i}' for i in range(1,10)])
ax.axhline(2.5,color='#BDC5CA',lw=1); ax.set_xticks([0,25,50,75,100]); ax.xaxis.set_major_formatter(PercentFormatter(xmax=100)); ax.set_xlabel('Share of natural-decline counties'); ax.tick_params(axis='y',length=0,pad=10); ax.spines['left'].set_visible(False)
ax.text(103,-.77,'Offset /\nnatural decline',fontsize=9,va='center')
f.legend(*ax.get_legend_handles_labels(),loc='upper left',bbox_to_anchor=(.20,.845),frameon=False,ncol=2,fontsize=10)
footer(f,f'Source: course-supplied USDA county data. 2023 rural–urban continuum codes; 50 states + DC, Puerto Rico excluded.\n{len(n):,} counties/equivalents with valid codes and both rates. Denominator: counties with natural change rate < 0.\nOffset: net migration rate + natural change rate > 0 (rates per 1,000 residents). Uses supplied rounded rates; residual change excluded.\nEach county counts equally. This measures demographic components, not an explanation of why people moved.')
finish(f,'05_migration_offsets.png')
# Fourth story: selected similar contemporary outcomes, unlike starting values.
selected=['Sweden','Japan','Korea, Rep.','France','Portugal','Chile','Costa Rica']
s=[]
for country in selected:
 a=p.loc[(country,1960),'Both']; b=p.loc[(country,2023),'Both']
 s.append({'country':country,'1960':a,'2023':b,'gain':b-a})
s=pd.DataFrame(s); s.to_csv(WORK/'lifespan_catchup.csv',index=False)
f,ax=plt.subplots(figsize=(10.8,8.5)); f.subplots_adjust(left=.12,right=.92,top=.77,bottom=.23)
heading(f,'Similar lifespans today, very different starting points',
 'Life expectancy at birth, both sexes · seven illustrative countries in 1960 and 2023')
ax.set_xlim(50,77); ax.set_ylim(76,88); ax.set_xticks([50,55,60,65,70,75]); ax.set_yticks([76,78,80,82,84,86,88]); grid(ax,'both')
# All annotations give the gain explicitly: unlike axes, it cannot be read from distance to a diagonal.
offsets={'Sweden':(-12,18),'Japan':(0,20),'Korea, Rep.':(12,12),'France':(12,-4),'Portugal':(12,-2),'Chile':(12,-6),'Costa Rica':(12,-24)}
for _,r in s.iterrows():
 ax.scatter(r['1960'],r['2023'],s=75,color=BLUE,zorder=3)
 label='South Korea' if r.country=='Korea, Rep.' else r.country
 ax.annotate(f'{label}\n+{r.gain:.1f} years',xy=(r['1960'],r['2023']),xytext=offsets[r.country],textcoords='offset points',fontsize=10,ha='right' if r.country=='Sweden' else 'left',va='bottom',color=DARK)
ax.set_xlabel('Life expectancy in 1960 (years)',labelpad=10); ax.set_ylabel('Life expectancy in 2023 (years)',labelpad=10)
ax.text(.03,.04,'1960 spread: 19.2 years\n2023 spread: 3.2 years',transform=ax.transAxes,fontsize=11,bbox=dict(facecolor='white',edgecolor='#DCE2E5',pad=9))
footer(f,'Source: course-supplied World Bank lifespan data, “Both” sex category. Labels show change from 1960 to 2023.\nCountries chosen to illustrate convergence toward 81–84 years; this is not a global sample or evidence that all countries converged.\nAxes have different ranges to make the remaining 2023 differences legible. No causal inference is intended.')
finish(f,'06_lifespan_catchup.png')
# Machine-readable audit trail for the write-up.
audit={'employment_counties':int(len(e)),'employment_excluded_incomplete':int(len(base)-len(e)),'employment_group_sizes':{k:int(v) for k,v in ns.items()},'employment_2023_index':{k:float(v) for k,v in idx[2023].items()},'natural_decline_counties':int(t.natural_decline_counties.sum()),'offset_counties':int(t.offset_counties.sum()),'lifespan_spread_1960':float(s['1960'].max()-s['1960'].min()),'lifespan_spread_2023':float(s['2023'].max()-s['2023'].min())}
import json
(WORK/'audit.json').write_text(json.dumps(audit,indent=2)+'\n')
print(json.dumps(audit,indent=2))
