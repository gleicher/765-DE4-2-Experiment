"""Regenerate all six figures and the supporting analysis tables."""
from pathlib import Path
import os
ROOT=Path(__file__).resolve().parents[1]
os.environ['MPLCONFIGDIR']=str(ROOT/'work'/'mplconfig')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import TwoSlopeNorm
from matplotlib.ticker import PercentFormatter
OUT=ROOT/'answers'/'figures'; OUT.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Arial','DejaVu Sans'],'font.size':11,'text.color':'#333333','axes.labelcolor':'#444444','xtick.color':'#555555','ytick.color':'#555555','axes.edgecolor':'#c9c9c9','axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'white','axes.facecolor':'white','savefig.facecolor':'white'})
BLUE='#4e79a7'; ORANGE='#f28e2b'; TEAL='#76b7b2'; GRAY='#bab0ac'
def finish(fig,name,title,subtitle,caption,left=.12,bottom=.20,top=.78,right=.94):
 fig.subplots_adjust(left=left,right=right,bottom=bottom,top=top)
 fig.text(.035,.95,title,fontsize=19,ha='left',va='top')
 fig.text(.035,.895,subtitle,fontsize=11,ha='left',va='top',color='#555555')
 fig.text(.035,.035,caption,fontsize=10,ha='left',va='bottom',linespacing=1.5,color='#555555')
 fig.savefig(OUT/name,dpi=180);plt.close(fig)
def grid(ax,axis='x'):
 ax.set_axisbelow(True);ax.grid(axis=axis,color='#ededed',linewidth=.8)
life=pd.read_csv(ROOT/'data'/'lifespan_dataset_1960.csv')
assert not life.duplicated(['Country Code','Sex','Year']).any()
ns=['Mexico','Argentina','Brazil','United States','Chile','Canada']
p=life[(life['Country Name'].isin(ns))&(life.Sex=='Both')&(life.Year.between(2019,2023))].pivot(index='Country Name',columns='Year',values='Life Expectancy (years)').reindex(ns)
assert p.notna().all().all()
d=p.sub(p[2019],axis=0); p.to_csv(ROOT/'work'/'life_levels.csv'); d.to_csv(ROOT/'work'/'life_changes.csv')
fig,axs=plt.subplots(2,3,figsize=(12,7.5),sharex=True,sharey=True)
for ax,n in zip(axs.flat,ns):
 ax.plot(p.columns,p.loc[n],color=BLUE,marker='o',markersize=4,linewidth=2)
 ax.axhline(p.loc[n,2019],color='#999999',ls='--',lw=.9)
 ax.set_title(n,loc='left',fontsize=12);ax.set_ylim(68,84);ax.set_xticks([2019,2021,2023]);ax.set_yticks([70,75,80]);grid(ax,'y')
 ax.annotate(f'{p.loc[n,2023]:.1f}',(2023,p.loc[n,2023]),xytext=(-3,7),textcoords='offset points',ha='right',fontsize=10,color=BLUE)
axs[0,0].set_ylabel('Life expectancy (years)');axs[1,0].set_ylabel('Life expectancy (years)')
for ax in axs[1,:]:ax.set_xlabel('Year')
finish(fig,'q1_primary.png','Recovery by 2023 differs across six American countries','Life expectancy at birth, both sexes · 2019–2023 · Dashed line: each country’s 2019 level', 'Mexico has the deepest fall; Canada and the United States remain below their 2019 levels in 2023.\nSelected countries, not a regional average. Shared scales preserve comparisons of absolute levels.\nSource: supplied World Bank life expectancy data.',left=.09,bottom=.23,top=.79)
fig,ax=plt.subplots(figsize=(11,7.2))
a=d[[2020,2021,2022,2023]]
im=ax.imshow(a,cmap='RdBu',norm=TwoSlopeNorm(vmin=-5,vcenter=0,vmax=5),aspect='auto')
ax.set_xticks(range(4),a.columns);ax.set_yticks(range(6),a.index);ax.set_xlabel('Year');ax.tick_params(length=0)
for i in range(6):
 for j in range(4):ax.text(j,i,f'{a.iloc[i,j]:+.2f}',ha='center',va='center',color='white' if abs(a.iloc[i,j])>2.7 else '#333333')
cb=fig.colorbar(im,ax=ax,pad=.035,fraction=.035);cb.set_label('Change from 2019 (years)');cb.set_ticks([-5,0,5])
finish(fig,'q1_alternate.png','Mexico’s 2021 shortfall is largest in this selection','Change in life expectancy at birth from each country’s 2019 baseline · Both sexes', 'Red: below 2019 · Blue: above 2019 · Numbers give the change in years.\nIn 2023, four selected countries exceed 2019; Canada (−0.52) and the United States (−0.40) do not.\nSource: supplied World Bank life expectancy data. Countries and row order match the companion line chart.',left=.19,bottom=.22,top=.80,right=.91)
c=pd.read_csv(ROOT/'data'/'full_census_dataset.csv',encoding='cp1252',dtype={'FIPS Code':str})
assert not c['FIPS Code'].duplicated().any()
c['FIPS Code']=c['FIPS Code'].str.zfill(5)
c=c[(~c['FIPS Code'].str.endswith('000'))&(~c.State.isin(['PR']))].copy()
code='2023 Rural-urban Continuum Code'
ecols=["Percent of adults with a bachelor's degree or higher, 2000","Percent of adults with a bachelor's degree or higher, 2019-23"]
e=c.dropna(subset=[code]+ecols).copy();assert e[code].isin(range(1,10)).all()
m=e.groupby(code)[ecols].mean();counts=e.groupby(code).size();m.columns=['2000','2019–23'];m['n']=counts;m['gain_pp']=m['2019–23']-m['2000'];m.to_csv(ROOT/'work'/'education_summary.csv')
labels=[f'Code {int(k)}  (n={counts[k]:,})' for k in m.index]
fig,ax=plt.subplots(figsize=(11,7.2));y=np.arange(9)
for i,(_,r) in enumerate(m.iterrows()):
 ax.plot([r['2000'],r['2019–23']],[i,i],color='#bcbcbc',lw=2)
 ax.text(r['2019–23']+.65,i,f'+{r.gain_pp:.1f} pp',va='center',fontsize=10,color='#666666')
ax.scatter(m['2000'],y,s=65,color=GRAY,label='2000',zorder=3);ax.scatter(m['2019–23'],y,s=65,color=BLUE,label='2019–23',zorder=3)
ax.set_yticks(y,labels);ax.invert_yaxis();ax.set_xlim(0,40);ax.set_xlabel('Mean county share of adults with a bachelor’s degree or higher (%)');grid(ax);ax.legend(frameon=False,loc='lower right')
finish(fig,'q2_primary.png','Bachelor’s attainment rises in every rural–urban code','Same counties in both periods · County means, grouped by 2023 Rural–urban Continuum Code', 'Codes 1–3 are metro; codes 4–9 are nonmetro. Labels show the increase in percentage points (pp).\nEqual weight per county, not per adult; 3,089 complete county/county-equivalent records in the 50 states + DC.\n2019–23 is a pooled period; current codes are held fixed for both periods. Source: supplied USDA census data.',left=.20,bottom=.22,top=.80)
fig,ax=plt.subplots(figsize=(11,7.2));x=np.arange(9);w=.34
b1=ax.bar(x-w/2,m['2000'],w,color=GRAY,label='2000');b2=ax.bar(x+w/2,m['2019–23'],w,color=BLUE,label='2019–23')
ax.bar_label(b1,fmt='%.1f',padding=3,fontsize=9);ax.bar_label(b2,fmt='%.1f',padding=3,fontsize=9)
ax.set_xticks(x,[str(int(k)) for k in m.index]);ax.set_ylim(0,38);ax.set_xlabel('2023 Rural–urban Continuum Code');ax.set_ylabel('Mean county bachelor’s share (%)');grid(ax,'y');ax.legend(frameon=False,loc='upper right')
finish(fig,'q2_alternate.png','Higher attainment, with a persistent metro advantage','Mean county share of adults with a bachelor’s degree or higher · 2000 and 2019–23', 'Codes 1–3 are metro; codes 4–9 are nonmetro. All nine groups rise; code 1 increases from 22.3% to 33.0%.\nEqual weight per county. Same 3,089 complete records as the companion dot chart; current codes held fixed.\n2019–23 is a pooled period. Source: supplied USDA census data, 50 states + DC; Puerto Rico excluded.',left=.10,bottom=.22,top=.80)
sel=['United States','Canada','Mexico','Brazil','Japan','France','Germany','India','China','South Africa','Nigeria','Australia']
p2=life[life['Country Name'].isin(sel)&life.Year.isin([2000,2023])&life.Sex.isin(['Male','Female'])].pivot(index='Country Name',columns=['Sex','Year'],values='Life Expectancy (years)')
g=p2.xs(2023,level=1,axis=1)-p2.xs(2000,level=1,axis=1); assert g.notna().all().all();g.to_csv(ROOT/'work'/'sex_gains.csv')
fig,ax=plt.subplots(figsize=(10.5,8));ax.plot([0,11],[0,11],ls='--',lw=1,color='#aaaaaa');
colors=np.where(g.Female>g.Male,ORANGE,BLUE);ax.scatter(g.Male,g.Female,c=colors,s=65,zorder=3)
offsets={'United States':(-5,-14),'Mexico':(5,8),'Canada':(6,-24),'Germany':(7,-7),'Japan':(7,7),'Australia':(-5,8),'France':(7,-8),'China':(-5,9),'Brazil':(7,-9),'Nigeria':(7,4),'South Africa':(-7,8),'India':(6,0)}
for n,r in g.iterrows():
 dx,dy=offsets[n];ax.annotate(n,(r.Male,r.Female),xytext=(dx,dy),textcoords='offset points',fontsize=10,ha='right' if dx<0 else 'left')
ax.scatter([],[],color=ORANGE,label='Larger female gain');ax.scatter([],[],color=BLUE,label='Larger male gain');ax.legend(frameon=False,loc='upper left');ax.set_xlim(0,11);ax.set_ylim(0,11);ax.set_aspect('equal');ax.set_xlabel('Male life expectancy gain, 2000 to 2023 (years)');ax.set_ylabel('Female life expectancy gain, 2000 to 2023 (years)');grid(ax,'both')
finish(fig,'q3.png','Longevity gains favor different sexes in different countries','Twelve selected countries · Change in life expectancy at birth between 2000 and 2023', 'Above the dashed equality line: female gain is larger (the female–male gap widens); below: male gain is larger.\nFive countries are above the line and seven below. This concerns gains, not which sex lives longer.\nPurposive country selection across several world regions; no claim of global representativeness.\nSource: supplied World Bank life expectancy data.',left=.11,bottom=.23,top=.80,right=.93)
z=c.dropna(subset=[code,'Natural Change 2023','Net Migration 2023']).copy();z=z[z[code].isin(range(1,10))];z=z[z['Natural Change 2023']<0].copy()
z['Group']=np.where(z[code]<=3,'Metro (codes 1–3)','Nonmetro (codes 4–9)')
z['Status']=np.where(z['Net Migration 2023']>=-z['Natural Change 2023'],'Offsets natural loss',np.where(z['Net Migration 2023']>0,'Positive but insufficient','Zero or negative migration'))
order=['Offsets natural loss','Positive but insufficient','Zero or negative migration'];tab=pd.crosstab(z.Group,z.Status).reindex(columns=order);pct=tab.div(tab.sum(axis=1),axis=0)*100;tab.to_csv(ROOT/'work'/'migration_counts.csv');pct.to_csv(ROOT/'work'/'migration_percent.csv')
fig,ax=plt.subplots(figsize=(11,6.5));left=np.zeros(2)
for status,color in zip(order,[BLUE,TEAL,GRAY]):
 vals=pct[status].to_numpy();ax.barh(np.arange(2),vals,left=left,height=.47,color=color,label=status)
 for i,v in enumerate(vals):ax.text(left[i]+v/2,i,f'{v:.1f}%',ha='center',va='center',color='white' if color==BLUE else '#333333',fontsize=12)
 left+=vals
ax.set_yticks(range(2),[f'{s}\nn = {tab.loc[s].sum():,}' for s in tab.index]);ax.invert_yaxis();ax.set_xlim(0,100);ax.set_xticks(range(0,101,20));ax.xaxis.set_major_formatter(PercentFormatter());ax.set_xlabel('Share of counties with more deaths than births');ax.legend(frameon=False,loc='upper left',bbox_to_anchor=(-.19,-.26),ncol=3,fontsize=10);grid(ax)
finish(fig,'q4.png','Migration offsets natural loss more often in metro counties','2023 · Only counties with negative natural change (births minus deaths) · 50 states + DC', 'Net migration ≥ −natural change is classified as offsetting the loss: 67.4% of metro vs 48.8% of nonmetro counties.\nDomestic and international net migration combined; each county gets equal weight. 2,155 complete records.\nThis accounting comparison excludes residual population adjustments and does not establish causes.\n2023 rural–urban codes; Puerto Rico and records missing either count/code excluded. Source: supplied USDA census data.',left=.25,bottom=.32,top=.78)
assert len(e)==3089;assert len(z)==2155
print('Six figures saved. Education records:',len(e),'Migration natural-loss records:',len(z))
