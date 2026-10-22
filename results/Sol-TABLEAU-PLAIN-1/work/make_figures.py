from pathlib import Path
import os
ROOT=Path(__file__).resolve().parents[1]
os.environ['MPLCONFIGDIR']=str(ROOT/'work/mpl-cache')
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.labelcolor':'#555555','text.color':'#333333','axes.edgecolor':'#cccccc','axes.spines.top':False,'axes.spines.right':False,'axes.spines.left':False,'axes.spines.bottom':False,'xtick.color':'#666666','ytick.color':'#666666','axes.titleweight':'normal'})
OUT=ROOT/'answers/figures'
L=pd.read_csv(ROOT/'data/lifespan_dataset_1960.csv')
C=pd.read_csv(ROOT/'data/full_census_dataset.csv',encoding='cp1252',dtype={'FIPS Code':str})
C=C[(C.State!='PR') & C['2023 Rural-urban Continuum Code'].notna()].copy()
C['Place']=np.where(C['2023 Rural-urban Continuum Code']<=3,'Metro','Nonmetro')
blue='#4e79a7'; orange='#f28e2b'; teal='#76b7b2'; gray='#bab0ac'
def page(title,subtitle,caption,size=(11.5,7.6)):
 fig=plt.figure(figsize=size,facecolor='white')
 fig.text(.075,.95,title,fontsize=20,va='top')
 fig.text(.075,.89,subtitle,fontsize=11,va='top',color='#666666')
 fig.text(.075,.055,caption,fontsize=9,va='bottom',color='#666666',linespacing=1.5)
 return fig
def save(fig,name):
 fig.savefig(OUT/name,dpi=180,facecolor='white');plt.close(fig)
def grid(ax):ax.grid(axis='y',color='#eeeeee');ax.set_axisbelow(True)
countries=['Sweden','United States','France','Korea, Rep.','Japan','Poland']
P=L[L['Country Name'].isin(countries)].pivot(index=['Country Name','Year'],columns='Sex',values='Life Expectancy (years)')
P['Gap']=P.Female-P.Male
P.reset_index().to_csv(ROOT/'work/life_sex_comparison.csv',index=False)
cap='Source: supplied World Bank life expectancy data. Gap = female minus male life expectancy at birth.\nSix selected countries illustrate different trajectories; this is not a global sample or a causal comparison.'
fig=page('The female–male gap narrowed, except in Japan','Selected countries, 1990–2023 • Difference in life expectancy at birth (years)',cap)
axes=fig.subplots(2,3);fig.subplots_adjust(left=.075,right=.96,bottom=.21,top=.79,hspace=.48,wspace=.24)
for ax,name in zip(axes.flat,countries):
 d=P.loc[name].loc[1990:2023];ax.plot(d.index,d.Gap,color=blue,lw=2);ax.scatter([1990,2023],d.Gap.loc[[1990,2023]],color=blue,s=22)
 ax.set(title=name,xlim=(1988,2028),ylim=(0,10),xticks=[1990,2000,2010,2023],yticks=[0,2,4,6,8,10]);grid(ax)
 ax.text(2024,d.Gap.loc[2023],f'{d.Gap.loc[2023]:.1f}',va='center',fontsize=10)
 ax.text(1990,d.Gap.loc[1990]+.35,f'{d.Gap.loc[1990]:.1f}',fontsize=10)
save(fig,'01_life_gap_lines.png')
years=[1990,2000,2010,2023]
H=P.Gap.unstack('Year').loc[countries,years]
H.to_csv(ROOT/'work/life_gap_table.csv')
fig=page('Japan’s gap stayed near six years','Same six countries • Female minus male life expectancy at birth (years)',cap)
ax=fig.add_axes([.23,.24,.61,.55]);im=ax.imshow(H,aspect='auto',cmap='Blues',vmin=0,vmax=10)
ax.set_xticks(range(4),years);ax.set_yticks(range(6),countries);ax.tick_params(length=0);ax.xaxis.tick_top()
for i in range(6):
 for j in range(4):ax.text(j,i,f'{H.iloc[i,j]:.1f}',ha='center',va='center',color='white' if H.iloc[i,j]>6 else '#333333',fontsize=13)
cb=fig.colorbar(im,ax=ax,fraction=.035,pad=.045);cb.set_label('Gap (years)');cb.set_ticks([0,2,4,6,8,10])
save(fig,'02_life_gap_highlight_table.png')
periods=['1990','2000','2008-12','2019-23']
levels=['Less than high school','High school only','Some college / associate','Bachelor’s or higher']
rows=[]
for place,g in C.groupby('Place'):
 for period in periods:
  fields=[f'Less than high school graduate, {period}',f'High school graduate (or equivalency), {period}',f'Some college or associate degree, {period}',f"Bachelor's degree or higher, {period}"]
  valid=g.dropna(subset=fields);s=valid[fields].sum();total=s.sum()
  for lev,v in zip(levels,s):rows.append([place,period,lev,v,total,100*v/total,len(valid)])
E=pd.DataFrame(rows,columns=['Place','Period','Education','Count','Total','Share','Counties']);E.to_csv(ROOT/'work/education_shares.csv',index=False)
print(E[E.Education=='Bachelor’s or higher'].to_string(index=False));print('Census rows',len(C))
cap2='Source: supplied USDA/course county data, 50 states + DC; Puerto Rico excluded. Adults age 25+.\nShares = summed education-category counts / sum of all four categories; complete records per period only.\nMetro = 2023 rural–urban codes 1–3; nonmetro = 4–9, held fixed across periods. ACS periods are estimates.'
fig=page('College attainment rose more in metro counties','Bachelor’s degree or higher • Share of adults age 25+ (%)',cap2)
ax=fig.add_axes([.09,.28,.80,.49]);x=np.arange(4)
for k,(place,color) in enumerate([('Metro',blue),('Nonmetro',orange)]):
 vals=E[(E.Place==place)&(E.Education=='Bachelor’s or higher')].set_index('Period').loc[periods].Share
 bars=ax.bar(x+(k-.5)*.34,vals,.32,color=color,label=place);ax.bar_label(bars,fmt='%.1f',padding=4,fontsize=10)
ax.set(xticks=x,xticklabels=periods,ylim=(0,45),ylabel='Share of adults (%)');grid(ax);ax.legend(frameon=False,loc='upper left');save(fig,'03_college_grouped_bars.png')
fig=page('Metro counties shifted further toward college degrees','Education composition, 1990 and 2019–23 • Share of adults age 25+ (%)',cap2)
ax=fig.add_axes([.22,.30,.72,.45]);labels=['Metro · 1990','Metro · 2019–23','Nonmetro · 1990','Nonmetro · 2019–23'];pairs=[('Metro','1990'),('Metro','2019-23'),('Nonmetro','1990'),('Nonmetro','2019-23')];left=np.zeros(4)
for lev,color in zip(levels,['#bab0ac','#e1d7c4',teal,blue]):
 vals=[E[(E.Place==p)&(E.Period==t)&(E.Education==lev)].Share.iloc[0] for p,t in pairs];ax.barh(np.arange(4),vals,left=left,color=color,height=.60,label=lev)
 for i,v in enumerate(vals):ax.text(left[i]+v/2,i,f'{v:.1f}',ha='center',va='center',fontsize=10,color='white' if lev=='Bachelor’s or higher' else '#333333')
 left+=vals
ax.set(yticks=np.arange(4),yticklabels=labels,xlim=(0,100),xticks=[0,25,50,75,100],xlabel='Share of adults (%)');ax.invert_yaxis();ax.legend(frameon=False,ncol=2,bbox_to_anchor=(.5,-.22),loc='upper center',fontsize=10)
save(fig,'04_education_stacked_bars.png')
sel=['United States','Japan','Sweden','Poland','Korea, Rep.','France']
D=L[(L['Country Name'].isin(sel))&(L.Sex=='Both')&(L.Year.between(2019,2023))].copy();D['Change']=D['Life Expectancy (years)']-D.groupby('Country Name')['Life Expectancy (years)'].transform('first');D.to_csv(ROOT/'work/life_2019_changes.csv',index=False)
fig=page('By 2023, recovery past 2019 was uneven','Life expectancy at birth, both sexes • Change from each country’s 2019 value (years)', 'Source: supplied World Bank data. Selected countries; values relative to each country’s own 2019 baseline.\nThese estimates describe changes during 2019–2023 and do not isolate the causes of those changes.')
axes=fig.subplots(2,3);fig.subplots_adjust(left=.075,right=.96,bottom=.21,top=.79,hspace=.48,wspace=.25)
for ax,name in zip(axes.flat,sel):
 d=D[D['Country Name']==name];ax.axhline(0,color='#888888',lw=1);ax.plot(d.Year,d.Change,color=blue,marker='o',lw=2,ms=4);ax.set(title=name,xticks=[2019,2021,2023],xlim=(2018.7,2023.6),ylim=(-3,1.2),yticks=[-3,-2,-1,0,1]);grid(ax);v=d[d.Year==2023].Change.iloc[0];ax.text(2023.12,v,f'{v:+.1f}',va='center',fontsize=10)
save(fig,'05_life_recovery.png')
N=C.dropna(subset=['Natural Change 2023','Net Migration 2023']).copy();N=N[N['Natural Change 2023']<0].copy();N['Outcome']=np.where(N['Net Migration 2023']>-N['Natural Change 2023'],'Migration exceeds natural loss','Migration does not exceed natural loss');N.to_csv(ROOT/'work/natural_loss_counties.csv',index=False)
T=pd.crosstab(N.Place,N.Outcome);print(T.to_string());T.to_csv(ROOT/'work/natural_loss_summary.csv')
fig=page('Migration offset natural decline in many counties','Counties with more deaths than births in 2023 • Metro versus nonmetro', 'Source: supplied USDA/course county data, 50 states + DC; Puerto Rico excluded. County counts, not people.\n“Offsets” means net migration > deaths minus births, using 2023 component counts. Residual population\nadjustments are excluded; this does not claim that every offset county had positive reported population change.')
ax=fig.add_axes([.18,.35,.74,.38]);left=np.zeros(2);places=['Metro','Nonmetro']
for outcome,color in [('Migration exceeds natural loss',blue),('Migration does not exceed natural loss',gray)]:
 vals=T.loc[places,outcome]/T.loc[places].sum(axis=1)*100;ax.barh([0,1],vals,left=left,height=.53,color=color,label=outcome)
 for i,v in enumerate(vals):ax.text(left[i]+v/2,i,f'{v:.1f}%\n{T.loc[places[i],outcome]:,} counties',ha='center',va='center',color='white' if color==blue else '#333333',fontsize=12)
 left+=vals.to_numpy()
ax.set(yticks=[0,1],yticklabels=[f'{p}\n(n = {T.loc[p].sum():,})' for p in places],xlim=(0,100),xticks=[0,25,50,75,100],xlabel='Share of counties with natural decrease (%)');ax.invert_yaxis();ax.legend(frameon=False,bbox_to_anchor=(.5,-.25),loc='upper center',fontsize=10)
save(fig,'06_migration_offsets.png')
