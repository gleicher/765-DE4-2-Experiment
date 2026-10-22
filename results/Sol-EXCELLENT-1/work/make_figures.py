"""Regenerate the six static figures from the supplied course data."""
from pathlib import Path
import os
BASE=Path(__file__).resolve().parents[1]
os.environ['MPLCONFIGDIR']=str(BASE/'work'/'mpl-cache')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.colors import TwoSlopeNorm
import numpy as np
import pandas as pd
OUT=BASE/'answers'/'figures';OUT.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.labelsize':11,'axes.titlesize':13,'axes.titleweight':'bold','figure.facecolor':'#fafaf7','axes.facecolor':'#fafaf7','axes.spines.top':False,'axes.spines.right':False,'axes.spines.left':False,'axes.spines.bottom':False,'xtick.color':'#4b5358','ytick.color':'#4b5358','text.color':'#202d35','axes.labelcolor':'#202d35','savefig.facecolor':'#fafaf7'})
BLUE='#24678d';ORANGE='#bb642a';TEAL='#247f78';RED='#b14e55';GRAY='#b3b8b8'
def heading(fig,title,sub):
 fig.text(.065,.95,title,fontsize=21,fontweight='bold',va='top')
 fig.text(.065,.895,sub,fontsize=11.5,va='top',color='#4b5358',linespacing=1.45)
def foot(fig,text): fig.text(.065,.04,text,fontsize=9,color='#4b5358',va='bottom',linespacing=1.5)
def save(fig,name):
 fig.savefig(OUT/name,dpi=180);plt.close(fig)
def clean(ax,axis='y'):
 ax.grid(axis=axis,color='#dce0dd',linewidth=.65);ax.set_axisbelow(True);ax.tick_params(length=0,pad=7)
l=pd.read_csv(BASE/'data'/'lifespan_dataset_1960.csv')
p=l.pivot(index=['Country Name','Year'],columns='Sex',values='Life Expectancy (years)')
c=pd.read_csv(BASE/'data'/'full_census_dataset.csv',encoding='cp1252',dtype={'FIPS Code':str},low_memory=False)
c['FIPS Code']=c['FIPS Code'].str.zfill(5)
c=c[(c.State!='PR') & (~c['FIPS Code'].str.endswith('000')) & c['2023 Rural-urban Continuum Code'].notna()].copy()
code='2023 Rural-urban Continuum Code';c['metro']=c[code]<=3
countries=['Sweden','Japan','Russian Federation','South Africa']
# 1. Absolute levels preserve the meaning of a changing sex gap.
fig,axs=plt.subplots(2,2,figsize=(12,8.8),sharex=True,sharey=True)
fig.subplots_adjust(left=.09,right=.96,bottom=.19,top=.77,hspace=.35,wspace=.14)
heading(fig,'A smaller sex gap can mean very different things','Four contrasting cases, 1990–2023 · life expectancy at birth, in years\nBlue: male   Orange: female   Shaded width: female minus male')
for ax,n in zip(axs.flat,countries):
 z=p.loc[n].loc[1990:2023];ax.plot(z.index,z.Male,color=BLUE,lw=2.3);ax.plot(z.index,z.Female,color=ORANGE,lw=2.3)
 ax.fill_between(z.index,z.Male,z.Female,color=ORANGE,alpha=.10)
 ax.set_title(n,loc='left');ax.set_ylim(48,90);ax.set_xlim(1990,2024);ax.set_xticks([1990,2000,2010,2023]);ax.set_yticks([50,60,70,80,90]);clean(ax)
 gap=z.Female-z.Male
 ax.text(.03,.90 if n=='South Africa' else .04,f'Sex gap: {gap.loc[1990]:.1f} → {gap.loc[2023]:.1f} years',transform=ax.transAxes,fontsize=10,bbox={'facecolor':'#fafaf7','edgecolor':'none','alpha':.85})
axs[0,0].set_ylabel('Life expectancy (years)');axs[1,0].set_ylabel('Life expectancy (years)')
fig.text(.09,.13,'Sweden: convergence through gains. South Africa: the gap also narrowed as both levels fell before 2005.',fontsize=11,fontweight='bold')
foot(fig,'Source: supplied World Bank lifespan_dataset_1960.csv. Selected contrasting cases, not a representative sample.\nAnnual period estimates describe mortality conditions; they are not forecasts of a newborn’s eventual lifespan. No causes are inferred.')
save(fig,'01_life_levels.png')
# 2. Re-express the same evidence as changes over two fixed intervals.
fig,axs=plt.subplots(1,2,figsize=(12,7.7),sharey=True)
fig.subplots_adjust(left=.20,right=.95,top=.75,bottom=.30,wspace=.22)
heading(fig,'Convergence through gains—or through losses?','Change in male and female life expectancy in the same four cases\nBlue: male   Orange: female   Connector: difference in their changes')
for ax,(a,b) in zip(axs,[(1990,2005),(2005,2023)]):
 ax.set_title(f'{a} → {b}',loc='left',pad=16)
 for i,n in enumerate(countries):
  delta=p.loc[(n,b)]-p.loc[(n,a)]
  ax.plot([delta.Male,delta.Female],[i,i],color='#9aa4a6',lw=3,zorder=2)
  ax.scatter(delta.Male,i,s=85,color=BLUE,zorder=3);ax.scatter(delta.Female,i,s=85,color=ORANGE,zorder=3)
  for v,dy in [(delta.Male,.23),(delta.Female,-.23)]: ax.text(v,i+dy,f'{v:+.1f}',ha='center',va='center',fontsize=10)
 ax.axvline(0,color='#617078',lw=1);ax.set_xlim(-13,17);ax.set_xticks([-10,-5,0,5,10,15]);ax.set_xlabel('Change in life expectancy (years)');clean(ax,'x')
axs[0].set_yticks(range(4),countries);axs[0].set_ylim(3.6,-.6)
fig.text(.20,.17,'If the blue dot is farther right, the female–male gap narrows.\nSouth Africa’s 1990–2005 narrowing accompanied a larger female loss, not a male gain.',fontsize=11,linespacing=1.5)
foot(fig,'Source: supplied World Bank lifespan_dataset_1960.csv. Values = endpoint minus start; no annual smoothing.\n1990 and 2023 bound the main chart; 2005 is a common checkpoint separating decline and recovery in South Africa and Russia.')
save(fig,'02_life_changes.png')
# Census outcome classification.
nat='Natural Change Rate 2023';mig='Net Migration Rate 2023'
v=c.dropna(subset=[nat,mig]).copy()
v['outcome']=np.select([v[nat]>=0,v[nat]+v[mig]>=0],[0,1],default=2)
colors=[GRAY,TEAL,RED]
labels=['Natural change ≥ 0 (any migration)','Natural loss offset by migration','Natural loss not offset']
# 3. Position relates two components; diagonal gives the threshold.
fig,axs=plt.subplots(1,2,figsize=(12,8.6),sharex=True,sharey=True)
fig.subplots_adjust(left=.09,right=.96,top=.74,bottom=.34,wspace=.13)
heading(fig,'Migration offsets natural loss more often in metro counties','2023 · natural change = births minus deaths; net migration includes domestic and international moves\nEach dot is a county; rates are per 1,000 residents. Above the diagonal, the two components sum to a gain.')
for ax,metro in zip(axs,[True,False]):
 g=v[v.metro==metro];loss=g[g[nat]<0];offset=(loss.outcome==1).sum();outside=((g[nat]<-16)|(g[nat]>12)|(g[mig]<-35)|(g[mig]>50)).sum()
 for i in [0,2,1]:
  q=g[g.outcome==i];ax.scatter(q[nat],q[mig],s=13,color=colors[i],alpha=.48,edgecolors='none',zorder=2)
 ax.plot([-16,12],[16,-12],color='#566368',lw=1.2,zorder=3)
 ax.axvline(0,color='#a5acab',lw=.8);ax.axhline(0,color='#a5acab',lw=.8)
 ax.set_title(('Metro' if metro else 'Nonmetro')+f' · {len(g):,} counties',loc='left',pad=13)
 ax.set_xlim(-16,12);ax.set_ylim(-35,50);ax.set_xlabel('Natural change per 1,000');clean(ax)
 ax.text(.04,.95,f'{offset/len(loss):.0%} of natural-loss counties offset it\n({offset:,} of {len(loss):,})',transform=ax.transAxes,va='top',fontsize=10.5,bbox={'facecolor':'#fafaf7','edgecolor':'none','alpha':.95})
 ax.text(.04,.035,f'{outside} counties outside this viewing window',transform=ax.transAxes,fontsize=9)
axs[0].set_ylabel('Net migration per 1,000')
handles=[plt.Line2D([],[],marker='o',ls='',color=x,markersize=7) for x in colors]
fig.legend(handles,labels,loc='lower left',bbox_to_anchor=(.085,.16),ncol=1,frameon=False,fontsize=10)
foot(fig,'Source: supplied county Census/USDA file. 3,106 counties/county equivalents in 50 states + DC with 2023 RUCC and both rates.\nMetro = RUCC 1–3; nonmetro = 4–9. Puerto Rico and 17 records without RUCC excluded. Each county counts equally.\nViewing window emphasizes the dense pattern; all counties contribute to counts. Component sums omit the population-estimate residual.')
save(fig,'03_county_components.png')
# 4. Ordered classification shows prevalence rather than rate magnitude.
fig,ax=plt.subplots(figsize=(12,8.5));fig.subplots_adjust(left=.26,right=.78,top=.74,bottom=.31)
heading(fig,'Natural loss is common; migration changes the outcome','2023 county outcomes by Rural–urban Continuum Code (RUCC)\nBars include every eligible county; right-hand labels give the share of natural-loss counties whose loss is offset.')
summary=[]
for k in range(1,10):
 g=v[v[code]==k];counts=g.outcome.value_counts().reindex([0,1,2],fill_value=0);shares=counts/len(g)*100;left=0
 for i in range(3):
  ax.barh(k,shares[i],left=left,color=colors[i],height=.63)
  if shares[i]>=9:ax.text(left+shares[i]/2,k,f'{shares[i]:.0f}%',ha='center',va='center',color='white' if i>0 else '#202d35',fontsize=10)
  left+=shares[i]
 loss=(g[nat]<0).sum();off=counts[1]
 ax.text(103,k,f'{off/loss:.0%}  ({off}/{loss})',va='center',fontsize=10)
 summary.append({'RUCC':k,'n':len(g),'natural_nonnegative':int(counts[0]),'loss_offset':int(counts[1]),'loss_unoffset':int(counts[2])})
ax.set_yticks(range(1,10),[f'{k} · '+('Metro' if k<=3 else 'Nonmetro')+f'  (n={int((v[code]==k).sum())})' for k in range(1,10)])
ax.invert_yaxis();ax.set_xlim(0,100);ax.set_xticks([0,25,50,75,100],[f'{x}%' for x in [0,25,50,75,100]]);ax.set_xlabel('Share of counties within each code');ax.tick_params(length=0);ax.axhline(3.5,color='#869394',lw=1)
ax.text(103,.2,'Offset / natural loss',fontsize=10,fontweight='bold')
fig.legend(handles,labels,loc='lower left',bbox_to_anchor=(.065,.145),frameon=False,fontsize=10)
foot(fig,'Source: supplied county Census/USDA file. 3,106 counties in 50 states + DC; Puerto Rico and 17 missing-RUCC records excluded.\nNatural loss = rate < 0. Offset = natural change rate + net migration rate ≥ 0 (including exactly zero).\nCodes are ordered categories, not equal steps in rurality. Metro 1–3; nonmetro 4–9. Counties are equally weighted, not residents.')
save(fig,'04_county_outcomes.png');pd.DataFrame(summary).to_csv(BASE/'work'/'county_outcomes.csv',index=False)
# 5. Heatmaps make recovery relative to a common pre-2020 baseline explicit.
ns=['Mexico','South Africa','India','Brazil','United States','Russian Federation','Germany','France','Sweden','Japan']
ns=sorted(ns,key=lambda n:p.loc[(n,2021),'Both']-p.loc[(n,2019),'Both'])
fig,axs=plt.subplots(1,2,figsize=(12,9.2),sharey=True);fig.subplots_adjust(left=.20,right=.87,top=.76,bottom=.23,wspace=.14)
heading(fig,'A deep 2021 loss did not always leave a 2023 deficit','Life expectancy relative to each country’s own 2019 value, in years\nTen selected countries · red = below baseline; blue = above baseline; cell labels give signed changes')
for ax,sex in zip(axs,['Male','Female']):
 arr=np.array([[p.loc[(n,y),sex]-p.loc[(n,2019),sex] for y in range(2020,2024)] for n in ns])
 im=ax.imshow(arr,cmap='RdBu',norm=TwoSlopeNorm(vmin=-6,vcenter=0,vmax=6),aspect='auto')
 for i in range(len(ns)):
  for j in range(4):ax.text(j,i,f'{arr[i,j]:+.1f}',ha='center',va='center',fontsize=11,color='white' if abs(arr[i,j])>3 else '#202d35')
 ax.set_title(sex,loc='left',pad=14);ax.set_xticks(range(4),range(2020,2024));ax.set_yticks(range(len(ns)),ns);ax.tick_params(length=0)
 ax.set_xticks(np.arange(-.5,4,1),minor=True);ax.set_yticks(np.arange(-.5,10,1),minor=True);ax.grid(which='minor',color='#fafaf7',lw=3);ax.tick_params(which='minor',length=0)
cax=fig.add_axes([.90,.23,.018,.53]);cb=fig.colorbar(im,cax=cax,ticks=[-6,-3,0,3,6]);cb.set_label('Change from 2019 (years)');cb.outline.set_visible(False)
fig.text(.20,.145,'Mexico and India exceeded their baselines by 2023; Germany and the US remained below for both sexes.',fontsize=11,fontweight='bold')
foot(fig,'Source: supplied World Bank lifespan_dataset_1960.csv. Rows ordered by 2019–2021 loss in the “Both” estimate.\nCountry selection spans differing loss/recovery patterns; it is not a global ranking. Annual changes are descriptive, not pandemic-attributed.\nThe baseline is sex-specific; no cross-country averaging or population weights. Rounded to one decimal; full precision determines color.')
save(fig,'05_life_recovery.png')
# 6. Quantile ranges reveal why attainment improvement need not close a divide.
fig,axs=plt.subplots(1,2,figsize=(12,8),sharey=True);fig.subplots_adjust(left=.17,right=.95,top=.75,bottom=.29,wspace=.18)
heading(fig,'Two education thresholds, two different divides','County adult education shares, 2000 versus 2019–23 · blue = 2000; orange = 2019–23\nDot = median county; thick segment = middle 50% of counties. The same complete-case counties appear at both dates.')
stats=[]
metrics=[('Without a high school diploma','Percent of adults who are not high school graduates, '),("Bachelor’s degree or higher","Percent of adults with a bachelor's degree or higher, ")]
for ax,(title,prefix) in zip(axs,metrics):
 ax.set_title(title,loc='left',pad=16)
 for y,metro in enumerate([True,False]):
  g=c[c.metro==metro].dropna(subset=[prefix+'2000',prefix+'2019-23'])
  for delta,date,color in [(-.13,'2000',BLUE),(.13,'2019-23',ORANGE)]:
   q=g[prefix+date].quantile([.25,.5,.75]);ax.plot([q.loc[.25],q.loc[.75]],[y+delta]*2,lw=7,color=color,solid_capstyle='round',alpha=.65)
   ax.scatter(q.loc[.5],y+delta,s=100,color=color,edgecolor='#fafaf7',lw=1.4,zorder=3)
   ax.text(q.loc[.5],y+delta+(-.12 if delta<0 else .16),f'{q.loc[.5]:.1f}%',ha='center',fontsize=10,color=color)
   stats.append({'metric':title,'metro':metro,'period':date,'n':len(g),'q25':q.loc[.25],'median':q.loc[.5],'q75':q.loc[.75]})
 ax.set_xlim(0,45);ax.set_xticks([0,10,20,30,40],[f'{i}%' for i in [0,10,20,30,40]]);ax.set_xlabel('Share of adults in a county');clean(ax,'x')
axs[0].set_yticks([0,1],['Metro\n(n=1,149)','Nonmetro\n(n=1,940)']);axs[0].set_ylim(1.6,-.6)
fig.text(.17,.17,'Metro–nonmetro median difference:\nWithout a diploma: 3.6 → 1.9 percentage points     |     Bachelor’s or higher: 4.7 → 7.7 points',fontsize=11,fontweight='bold',linespacing=1.6)
foot(fig,'Source: supplied county Census/USDA file. Adult percentages are supplied education variables. 3,089 paired counties.\n50 states + DC; Puerto Rico, 17 missing-RUCC records, and 17 further counties missing either education period excluded.\nMetro = 2023 RUCC 1–3; nonmetro = 4–9, held fixed for both dates. Equal county weighting; this is not the national adult share.\n2000 Census and 2019–23 multi-year estimates differ in collection period; no uncertainty intervals are provided in this file.')
save(fig,'06_education_thresholds.png');pd.DataFrame(stats).to_csv(BASE/'work'/'education_summary.csv',index=False)
print('Saved six figures to',OUT)
