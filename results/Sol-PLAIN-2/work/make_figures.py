from pathlib import Path
import os
os.environ.setdefault('MPLCONFIGDIR', str(Path(__file__).resolve().parent / 'matplotlib-cache'))
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'answers/figures'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'axes.labelcolor':'#364152','text.color':'#182b3a','axes.titleweight':'bold','figure.facecolor':'#fafaf7','axes.facecolor':'#fafaf7','savefig.facecolor':'#fafaf7'})
blue='#216b88'; orange='#c77439'; teal='#278c79'; red='#aa4260'; gray='#687889'
def header(fig,title,subtitle):
 fig.text(.07,.955,title,fontsize=22,weight='bold',va='top');fig.text(.07,.902,subtitle,fontsize=11,va='top')
def foot(fig,text): fig.text(.07,.035,text,fontsize=9,va='bottom',linespacing=1.5,color='#52606d')
def save(fig,name): fig.savefig(OUT/name,dpi=180);plt.close(fig)
l=pd.read_csv(ROOT/'data/lifespan_dataset_1960.csv')
names=['France','United States','Mexico','Japan','India','Russian Federation']
short={'Russian Federation':'Russia','United States':'United States'}
p=l[l['Country Name'].isin(names)].pivot(index=['Country Name','Year'],columns='Sex',values='Life Expectancy (years)')
p['Gap']=p.Female-p.Male
p.to_csv(ROOT/'work/life_selected.csv')
fig,axs=plt.subplots(2,3,figsize=(12,8),sharex=True,sharey=True)
fig.subplots_adjust(left=.08,right=.95,top=.79,bottom=.18,hspace=.44,wspace=.22)
header(fig,'Longevity gaps do not follow one path','Female minus male life expectancy at birth, 1990–2023 • six selected countries')
for ax,n in zip(axs.flat,names):
 q=p.loc[n].loc[1990:2023,'Gap'];ax.plot(q.index,q,color=blue,lw=2.5);ax.scatter([1990,2023],q.loc[[1990,2023]],color=blue,zorder=3)
 ax.set_title(short.get(n,n),loc='left',fontsize=12);ax.set_ylim(0,15);ax.set_xticks([1990,2000,2010,2023]);ax.grid(axis='y',alpha=.17)
 ax.annotate(f'{q.loc[2023]:.1f}',(2023,q.loc[2023]),xytext=(-7,8),textcoords='offset points',ha='right',fontsize=10,weight='bold')
for ax in axs[:,0]:ax.set_ylabel('Female advantage (years)')
foot(fig,'France and the United States narrowed their gaps; India widened its gap. Russia had a much larger, volatile gap.\nSelected examples, not a representative country sample. Source: supplied World Bank lifespan_dataset_1960.csv. No country aggregates.')
save(fig,'01-life-gap-trajectories.png')
fig,ax=plt.subplots(figsize=(12,7.5));fig.subplots_adjust(left=.22,right=.88,top=.78,bottom=.22)
header(fig,'France narrowed; India widened','The same six countries • female minus male life expectancy at birth, 1990 versus 2023')
for i,n in enumerate(names):
 a,b=p.loc[(n,1990),'Gap'],p.loc[(n,2023),'Gap'];ax.plot([a,b],[i,i],color=gray,lw=3);ax.scatter(a,i,color=orange,s=85,zorder=3);ax.scatter(b,i,color=blue,s=85,zorder=4)
 ax.text(12.6,i,f'{b-a:+.2f}',va='center',weight='bold',color=blue)
ax.set_yticks(range(6),[short.get(n,n) for n in names]);ax.invert_yaxis();ax.set_xlim(0,14);ax.set_xticks([0,2,4,6,8,10,12]);ax.set_xlabel('Female advantage (years)');ax.grid(axis='x',alpha=.17);ax.text(12.6,-.65,'Change\n(years)',ha='left',fontsize=10)
ax.legend(handles=[Line2D([],[],marker='o',ls='',color=orange,label='1990'),Line2D([],[],marker='o',ls='',color=blue,label='2023')],loc='lower center',bbox_to_anchor=(.4,-.20),ncol=2,frameon=False)
foot(fig,'Endpoint change can conceal reversals: see the companion trajectories for intervening years. Russia = Russian Federation in source.\nSelected examples, not a representative country sample. Source: supplied World Bank lifespan_dataset_1960.csv.')
save(fig,'02-life-gap-endpoints.png')
c=pd.read_csv(ROOT/'data/full_census_dataset.csv',encoding='cp1252',dtype={'FIPS Code':str})
ru='2023 Rural-urban Continuum Code'
c=c[(c.State!='PR') & (pd.to_numeric(c['FIPS Code'])%1000!=0) & c[ru].between(1,9)].copy()
need=[ru,'Natural Change 2023','Net Migration 2023','Population Estimate 2022','Population Estimate 2023']
g=c.dropna(subset=need).copy();den=(g['Population Estimate 2022']+g['Population Estimate 2023'])/2
g=g[den>0].copy();den=den.loc[g.index]
g['natural']=g['Natural Change 2023']/den*1000;g['migration']=g['Net Migration 2023']/den*1000
g['type']=np.select([g.natural>=0,(g.natural<0)&(g.migration>=-g.natural),(g.natural<0)&(g.migration>0)],[0,1,2],default=3)
labels=['No natural decrease','Migration offsets natural decrease','Migration helps, but falls short','Natural decrease; no migration gain']
colors=[gray,teal,orange,red]
g.to_csv(ROOT/'work/county_growth.csv',index=False)
fig,axs=plt.subplots(1,2,figsize=(13,8),sharex=True,sharey=True);fig.subplots_adjust(left=.09,right=.96,top=.79,bottom=.28,wspace=.12)
header(fig,'Migration can offset more deaths than births','2023 county population components • each point is one county or county equivalent')
for ax,mask,title in [(axs[0],g[ru]<=3,'Metro (RUCC 1–3)'),(axs[1],g[ru]>=4,'Nonmetro (RUCC 4–9)')]:
 q=g[mask]
 for j in range(4):
  d=q[q.type==j];ax.scatter(d.natural,d.migration,s=9,alpha=.45,color=colors[j],rasterized=True)
 ax.axvline(0,c=gray,lw=.8);ax.axhline(0,c=gray,lw=.8);xx=np.linspace(-150,0,100);ax.plot(xx,-xx,c=teal,ls='--',lw=1)
 ax.set_xscale('symlog',linthresh=1);ax.set_yscale('symlog',linthresh=1);ax.set_xlim(-150,150);ax.set_ylim(-150,150);ax.set_xticks([-100,-10,-1,0,1,10,100],labels=['−100','−10','−1','0','1','10','100']);ax.set_yticks([-100,-10,-1,0,1,10,100],labels=['−100','−10','−1','0','1','10','100'])
 ax.set_title(f'{title} • n = {len(q):,}',loc='left',fontsize=13);ax.set_xlabel('Births minus deaths, per 1,000 residents');ax.grid(alpha=.12)
 nd=q[q.natural<0];pct=100*(nd.type==1).mean();ax.text(.04,.96,f'{pct:.0f}% of naturally declining counties\nhad enough migration to offset the loss',transform=ax.transAxes,va='top',fontsize=10,bbox=dict(facecolor='#fafaf7',edgecolor='none',alpha=.9))
axs[0].set_ylabel('Net migration, per 1,000 residents')
fig.legend(handles=[Patch(color=x,label=y) for x,y in zip(colors,labels)],loc='lower center',bbox_to_anchor=(.5,.145),ncol=2,frameon=False,fontsize=10)
foot(fig,f'Dashed line: net migration exactly offsets natural loss. Nonlinear axes: linear within ±1, logarithmic beyond; all {len(g):,} eligible counties shown.\nRates = component counts / mean 2022–2023 population × 1,000. Excludes PR, aggregate rows and missing inputs.\nSource: supplied USDA full_census_dataset.csv. Components exclude residual adjustments; offset does not guarantee total population growth.')
save(fig,'03-county-migration-scatter.png')
counts=pd.crosstab(g[ru].astype(int),g.type).reindex(index=range(1,10),columns=range(4),fill_value=0);counts.to_csv(ROOT/'work/growth_category_counts.csv')
fig,ax=plt.subplots(figsize=(13,8));fig.subplots_adjust(left=.19,right=.88,top=.79,bottom=.29)
header(fig,'Natural loss and migration differ across county types','Share of counties in each 2023 growth-component category • same counties as the companion scatterplot')
left=np.zeros(9);per=counts.div(counts.sum(axis=1),axis=0)*100
for j in range(4):
 vals=per[j].values;ax.barh(range(9),vals,left=left,color=colors[j],height=.72)
 for i,v in enumerate(vals):
  if v>=9:ax.text(left[i]+v/2,i,f'{v:.0f}%',ha='center',va='center',color='white',weight='bold',fontsize=10)
 left+=vals
ax.set_yticks(range(9),['Metro • code 1','Metro • code 2','Metro • code 3']+[f'Nonmetro • code {x}' for x in range(4,10)]);ax.invert_yaxis();ax.set_xlim(0,100);ax.set_xlabel('Counties (%) • each county has equal weight');ax.set_xticks([0,25,50,75,100]);ax.axhline(2.5,color=gray,lw=1)
for i,n in enumerate(counts.sum(axis=1)):ax.text(102,i,f'n = {n:,}',va='center',fontsize=10)
fig.legend(handles=[Patch(color=x,label=y) for x,y in zip(colors,labels)],loc='lower center',bbox_to_anchor=(.5,.15),ncol=2,frameon=False,fontsize=10)
foot(fig,'RUCC = supplied 2023 Rural–urban Continuum Code; 1–3 metro, 4–9 nonmetro. Code labels avoid inventing finer definitions.\nMigration offsets loss when net migration ≥ deaths − births. Natural decrease means deaths > births; zero migration is not a gain.\nExcludes PR, aggregate rows and missing inputs. Source: supplied USDA full_census_dataset.csv. Rounded labels may not sum to 100%.')
save(fig,'04-county-migration-shares.png')
# Rebound relative to a shared within-country baseline; both sexes shown separately.
rows=[];rowlabels=[]
for n in names:
 for sex in ['Female','Male']:
  rows.append([p.loc[(n,y),sex]-p.loc[(n,2019),sex] for y in [2020,2021,2022,2023]]);rowlabels.append(short.get(n,n)+' • '+sex)
a=np.array(rows);pd.DataFrame(a,index=rowlabels,columns=[2020,2021,2022,2023]).to_csv(ROOT/'work/recovery_changes.csv')
fig,ax=plt.subplots(figsize=(11,9));fig.subplots_adjust(left=.31,right=.88,top=.81,bottom=.19)
header(fig,'Recovery depends on country and sex','Life expectancy change from each country–sex’s 2019 level • years gained or lost')
im=ax.imshow(a,cmap='RdBu',vmin=-6,vmax=6,aspect='auto');ax.set_yticks(range(12),rowlabels);ax.set_xticks(range(4),[2020,2021,2022,2023]);ax.xaxis.tick_top();ax.tick_params(length=0)
for i in range(12):
 for j in range(4):ax.text(j,i,f'{a[i,j]:+.1f}',ha='center',va='center',color='white' if abs(a[i,j])>3 else '#182b3a',fontsize=11,weight='bold')
for y in np.arange(1.5,12,2):ax.axhline(y,color='#fafaf7',lw=4)
cb=fig.colorbar(im,ax=ax,fraction=.045,pad=.045);cb.set_label('Change from 2019 (years)');cb.set_ticks([-6,-3,0,3,6])
foot(fig,'In 2023, both sexes remained below 2019 in Japan and the United States; India and Mexico were above their own baselines.\nCells show differences, not absolute lifespan. No causal attribution to the pandemic or other events.\nSame selected six countries; not a representative sample. Source: supplied World Bank lifespan_dataset_1960.csv.')
save(fig,'05-life-recovery-heatmap.png')
cols=["Percent of adults with a bachelor's degree or higher, 1990","Percent of adults with a bachelor's degree or higher, 2019-23"]
e=c.dropna(subset=cols).copy();e.to_csv(ROOT/'work/education_complete.csv',index=False)
fig,axs=plt.subplots(1,2,figsize=(12,8),sharex=True,sharey=True);fig.subplots_adjust(left=.09,right=.96,top=.79,bottom=.25,wspace=.12)
header(fig,'College attainment shifted upward, unevenly','Distribution across counties of adults with a bachelor’s degree or higher • paired complete records')
for ax,mask,title in [(axs[0],e[ru]<=3,'Metro (RUCC 1–3)'),(axs[1],e[ru]>=4,'Nonmetro (RUCC 4–9)')]:
 q=e[mask]
 for col,color,label in zip(cols,[orange,blue],['1990','2019–23']):
  x=np.sort(q[col]);y=np.arange(1,len(x)+1)/len(x)*100;ax.step(x,y,where='post',color=color,lw=2.4,label=label)
 ax.axhline(50,c=gray,ls=':',lw=1);ax.set_title(f'{title} • n = {len(q):,}',loc='left',fontsize=13);ax.set_xlim(0,85);ax.set_ylim(0,100);ax.set_xlabel('Adults with bachelor’s degree or higher (%)');ax.grid(alpha=.15)
 med=q[cols].median();ax.text(.05,.95,f'Median county: {med.iloc[0]:.1f}% → {med.iloc[1]:.1f}%',transform=ax.transAxes,va='top',fontsize=11,weight='bold',bbox=dict(facecolor='#fafaf7',edgecolor='none',alpha=.9));ax.legend(loc='lower right',frameon=False)
axs[0].set_ylabel('Counties at or below this attainment level (%)')
foot(fig,f'Each step curve accumulates counties, not people: a rightward shift means higher county attainment. Dotted line marks the median.\nSame {len(e):,} counties in both periods; metro status held at 2023 RUCC. 2019–23 is a pooled estimate, not a single-year measure.\nExcludes PR, aggregate rows and missing paired values. Source: supplied USDA full_census_dataset.csv; educational shares are provided fields.')
save(fig,'06-education-distributions.png')
summary={'growth_count':len(g),'education_count':len(e),'excluded_growth':len(c)-len(g),'excluded_education':len(c)-len(e),'growth_max_abs':float(g[['natural','migration']].abs().max().max()),'education_medians':{lab:e[mask][cols].median().tolist() for mask,lab in [(e[ru]<=3,'metro'),(e[ru]>=4,'nonmetro')]},'offset_percent':{lab:float(100*(g[mask & (g.natural<0)].type==1).mean()) for mask,lab in [(g[ru]<=3,'metro'),(g[ru]>=4,'nonmetro')]}}
import json
(ROOT/'work/summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
