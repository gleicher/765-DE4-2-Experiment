from pathlib import Path
import os
ROOT=Path(__file__).resolve().parents[1]
os.environ['MPLCONFIGDIR']=str(ROOT/'work/.mplconfig')
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
OUT=ROOT/'answers/figures'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'axes.edgecolor':'#b9c2c9','axes.labelcolor':'#273746','text.color':'#273746','xtick.color':'#53616d','ytick.color':'#53616d','figure.facecolor':'#fafbf9','axes.facecolor':'#fafbf9','savefig.facecolor':'#fafbf9'})
BLUE='#147d92'; ORANGE='#ca6236'; GRAY='#82929c'; PURPLE='#77569a'
def canvas(title,subtitle,caption, figsize=(12,8)):
 f=plt.figure(figsize=figsize); f.text(.07,.94,title,fontsize=22,weight='bold'); f.text(.07,.89,subtitle,fontsize=12)
 f.text(.07,.035,caption,fontsize=9,va='bottom',linespacing=1.5); return f
def save(f,name):
 f.savefig(OUT/name,dpi=180); plt.close(f)
def grid(a,axis='y'): a.grid(axis=axis,color='#dce2e4',lw=.7); a.set_axisbelow(True)
l=pd.read_csv(ROOT/'data/lifespan_dataset_1960.csv')
p=l.pivot(index=['Country Name','Year'],columns='Sex',values='Life Expectancy (years)'); p['gap']=p.Female-p.Male
countries=['France','United States','Sweden','Japan']; colors=[PURPLE,ORANGE,BLUE,'#7b8233']
sub=p.loc[(countries,slice(1980,2023)),:].reset_index(); sub.to_csv(ROOT/'work/life_gap.csv',index=False)
f=canvas('The life expectancy sex gap did not narrow everywhere','Female minus male life expectancy, 1980–2023 • Four selected countries',
 'Source: supplied World Bank life expectancy data (course CSV). Gap = female − male life expectancy at birth.\nCountries selected to contrast trajectories; this is not a representative sample or a causal explanation.')
a=f.add_axes([.09,.19,.72,.62])
for name,color in zip(countries,colors):
 d=sub[sub['Country Name']==name]; a.plot(d.Year,d.gap,color=color,lw=2.5); a.scatter(d.Year.iloc[-1],d.gap.iloc[-1],color=color,s=35)
 a.text(2024,d.gap.iloc[-1],f'{name}  {d.gap.iloc[-1]:.1f}',color=color,va='center',fontsize=11)
a.set(xlim=(1980,2023),ylim=(0,9),xticks=[1980,1990,2000,2010,2020,2023],ylabel='Female advantage (years)',xlabel='Year'); grid(a)
save(f,'01_life_gap_lines.png')
f=canvas('Japan is the exception in this four-country comparison','Female advantage in life expectancy • 1980 versus 2023',
 'Source: supplied World Bank life expectancy data (course CSV). Values are female − male life expectancy at birth.\nEndpoint comparison hides intervening fluctuations. Four countries selected to contrast trajectories.')
a=f.add_axes([.20,.22,.66,.57]); y=np.arange(4)
for i,(name,col) in enumerate(zip(countries,colors)):
 start=p.loc[(name,1980),'gap']; end=p.loc[(name,2023),'gap']; a.plot([start,end],[i,i],color=GRAY,lw=3)
 a.scatter(start,i,s=100,facecolor='#fafbf9',edgecolor=GRAY,lw=2,zorder=3); a.scatter(end,i,s=100,color=col,zorder=4)
 a.text(start,i-.18,f'{start:.1f}',ha='center',fontsize=11,color='#53616d'); a.text(end,i+.23,f'{end:.1f}',ha='center',fontsize=11,color=col)
 a.text(9.2,i,f'{end-start:+.2f} years',va='center',color=col,weight='bold')
a.set(yticks=y,yticklabels=countries,xlim=(0,9),ylim=(3.6,-.6),xlabel='Female minus male life expectancy (years)'); grid(a,'x')
f.text(.20,.83,'○ 1980     ● 2023',fontsize=12); f.text(.88,.83,'Change',fontsize=11)
save(f,'02_life_gap_dumbbells.png')
c=pd.read_csv(ROOT/'data/full_census_dataset.csv',encoding='cp1252',dtype={'FIPS Code':str})
c=c[(c.State!='PR') & (pd.to_numeric(c['FIPS Code'])%1000!=0)].copy()
c['rucc']=pd.to_numeric(c['2023 Rural-urban Continuum Code']); c=c[c.rucc.between(1,9)]
e0="Percent of adults with a bachelor's degree or higher, 2000"; e1="Percent of adults with a bachelor's degree or higher, 2019-23"
ed=c.dropna(subset=[e0,e1]).copy(); summary=ed.groupby('rucc')[[e0,e1]].median(); ns=ed.groupby('rucc').size()
summary['n']=ns; summary.to_csv(ROOT/'work/education_summary.csv'); ed[['FIPS Code','State','Area name','rucc',e0,e1]].to_csv(ROOT/'work/education_counties.csv',index=False)
cap='Source: supplied USDA/Census county CSV. 50 states + DC; counties with both measurements; each county weighted equally.\n2023 rural–urban continuum codes held fixed for both periods. 2019–23 is a pooled estimate, not a single year.'
f=canvas('Bachelor’s attainment rose across all nine county groups','County median share of adults with a bachelor’s degree or higher • 2000 versus 2019–23',cap)
a=f.add_axes([.17,.19,.68,.62]); y=np.arange(9)
for i,k in enumerate(summary.index):
 v0,v1=summary.loc[k,[e0,e1]]; a.plot([v0,v1],[i,i],color='#b2bec5',lw=3); a.scatter(v0,i,color=GRAY,s=65,zorder=3); a.scatter(v1,i,color=BLUE,s=65,zorder=3)
 a.text(v1+.5,i,f'{v1:.1f}%',va='center',fontsize=10,color=BLUE)
 a.text(38,i,f'+{v1-v0:.1f} pp',va='center',fontsize=10)
a.set(yticks=y,yticklabels=[f'Code {int(k)}  (n={ns[k]})' for k in summary.index],xlim=(0,44),ylim=(8.6,-.7),xlabel='Adults with a bachelor’s degree or higher (%)',xticks=[0,10,20,30,40]); grid(a,'x'); f.text(.17,.83,'● 2000',color=GRAY); f.text(.30,.83,'● 2019–23',color=BLUE); f.text(.80,.83,'Change',fontsize=10)
save(f,'03_education_medians.png')
f=canvas('Higher attainment, with wide differences among counties','Bachelor’s degree or higher • Distributions shift right in every 2023 rural–urban code',cap,figsize=(12,9))
for j,k in enumerate(range(1,10)):
 a=f.add_axes([.08+(j%3)*.305,.64-(j//3)*.235,.265,.19]); d=ed[ed.rucc==k]
 for field,color in [(e0,GRAY),(e1,BLUE)]:
  vals=np.sort(d[field].to_numpy()); a.step(vals,np.arange(1,len(vals)+1)/len(vals),where='post',color=color,lw=2)
 a.set(xlim=(0,80),ylim=(0,1),xticks=[0,20,40,60,80],yticks=[0,.5,1]); a.yaxis.set_major_formatter(PercentFormatter(1)); a.set_title(f'Code {k} · {len(d)} counties',fontsize=11,loc='left'); grid(a)
 if j//3==2: a.set_xlabel('Bachelor’s attainment (%)',fontsize=10)
 if j%3==0: a.set_ylabel('Counties at or below',fontsize=9)
f.text(.08,.855,'2000',color=GRAY,weight='bold'); f.text(.16,.855,'2019–23',color=BLUE,weight='bold'); f.text(.34,.855,'A curve farther right indicates higher attainment.',fontsize=10)
save(f,'04_education_distributions.png')
# Changes relative to a shared 2019 baseline.
chosen=['Japan','Sweden','France','United States','Brazil','India','South Africa','China']
changes=[]
for name in chosen:
 changes.append([name,p.loc[(name,2021),'Both']-p.loc[(name,2019),'Both'],p.loc[(name,2023),'Both']-p.loc[(name,2019),'Both']])
g=pd.DataFrame(changes,columns=['Country','2019–2021 change','2019–2023 change']); g.to_csv(ROOT/'work/life_recovery.csv',index=False)
f=canvas('Early setbacks and 2023 recovery differ across countries','Life expectancy at birth, both sexes • Eight selected countries • Changes from 2019',
 'Source: supplied World Bank life expectancy data (course CSV). Both axes measure change from the same 2019 baseline.\nAbove zero on the vertical axis: 2023 exceeds 2019. Selected countries illustrate contrasts, not global prevalence.\nThese are descriptive endpoint comparisons; they do not isolate the effects of the pandemic or explain recovery.')
a=f.add_axes([.12,.20,.68,.60]); grid(a)
a.axhline(0,color=GRAY,lw=1.5); a.axvline(0,color=GRAY,lw=1.5)
for name,x,y in g.itertuples(index=False):
 col=BLUE if y>=0 else ORANGE; a.scatter(x,y,s=95,color=col,zorder=4)
 offsets={'France':(-62,12),'Sweden':(-65,20),'Japan':(12,-12),'United States':(-16,-23),'China':(12,12),'Brazil':(-25,16),'India':(10,-3),'South Africa':(-15,15)}
 a.annotate(name,(x,y),xytext=offsets[name],textcoords='offset points',fontsize=11,color=col)
a.set(xlim=(-4.8,1.0),ylim=(-.8,1.6),xlabel='2019 → 2021 change (years)',ylabel='2019 → 2023 change (years)',xticks=[-4,-3,-2,-1,0,1],yticks=[-.5,0,.5,1,1.5])
f.text(.83,.68,'2023 above\n2019',color=BLUE,fontsize=13,weight='bold'); f.text(.83,.42,'2023 below\n2019',color=ORANGE,fontsize=13,weight='bold')
save(f,'05_life_recovery_scatter.png')
# Four outcome combinations in natural change and net migration.
d=c.dropna(subset=['Natural Change 2023','Net Migration 2023']).copy()
d['quadrant']=np.select([(d['Natural Change 2023']>=0)&(d['Net Migration 2023']>=0),(d['Natural Change 2023']<0)&(d['Net Migration 2023']>=0),(d['Natural Change 2023']>=0)&(d['Net Migration 2023']<0)],['Both nonnegative','Natural decrease, migration nonnegative','Natural nonnegative, migration loss'],default='Both negative')
q=pd.crosstab(d.rucc,d.quadrant).reindex(columns=['Both nonnegative','Natural decrease, migration nonnegative','Natural nonnegative, migration loss','Both negative'],fill_value=0)
q.to_csv(ROOT/'work/population_components.csv'); shares=q.div(q.sum(axis=1),axis=0)*100
f=canvas('Migration gains often accompany natural population losses','2023 county population components • Share of counties within each rural–urban code',
 'Source: supplied USDA/Census county CSV. 50 states + DC; valid 2023 code and both components; counties equally weighted.\nNatural change = births − deaths. Net migration combines domestic and international migration. Zero is grouped with gains.\nA migration gain need not fully offset natural loss; these categories describe signs, not total population growth.')
a=f.add_axes([.18,.25,.75,.50]); left=np.zeros(9); palette=[BLUE,'#dcaa53','#97b8b8',PURPLE]
for col,color in zip(shares.columns,palette):
 vals=shares[col].to_numpy(); a.barh(np.arange(9),vals,left=left,color=color,height=.67)
 for i,v in enumerate(vals):
  if v>=9: a.text(left[i]+v/2,i,f'{v:.0f}%',ha='center',va='center',fontsize=10,color='white' if color in [BLUE,PURPLE] else '#273746')
 left+=vals
a.set(yticks=np.arange(9),yticklabels=[f'Code {int(k)} (n={q.loc[k].sum()})' for k in q.index],xlim=(0,100),ylim=(8.6,-.6),xlabel='Share of counties (%)',xticks=[0,25,50,75,100]); grid(a,'x')
for i,(lab,color) in enumerate(zip(['Natural + / migration +','Natural − / migration +','Natural + / migration −','Natural − / migration −'],palette)):
 f.text(.10+(i%2)*.43,.825-(i//2)*.038,'■ '+lab,color=color,fontsize=11)
save(f,'06_population_components.png')
print(summary.round(2).to_string()); print(g.round(2).to_string(index=False)); print(shares.round(1).to_string()); print('Counties:',len(c),'education:',len(ed),'components:',len(d))
