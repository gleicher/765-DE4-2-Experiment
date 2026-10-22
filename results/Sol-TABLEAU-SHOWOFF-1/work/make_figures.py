from pathlib import Path
import os
ROOT=Path(__file__).resolve().parents[1]
os.environ['MPLCONFIGDIR']=str(ROOT/'work/mplconfig')
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.ticker import MultipleLocator
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.labelcolor':'#444444','text.color':'#333333','axes.edgecolor':'#cccccc','xtick.color':'#555555','ytick.color':'#555555','axes.spines.top':False,'axes.spines.right':False,'axes.spines.left':False,'axes.spines.bottom':False,'axes.titleweight':'normal','savefig.facecolor':'white'})
OUT=ROOT/'answers/figures';OUT.mkdir(parents=True,exist_ok=True)
blue='#4e79a7';orange='#f28e2b';teal='#76b7b2';red='#e15759'
life=pd.read_csv(ROOT/'data/lifespan_dataset_1960.csv')
county=pd.read_csv(ROOT/'data/full_census_dataset.csv',encoding='cp1252',dtype={'FIPS Code':str})
state=pd.read_csv(ROOT/'data/aggregate_census_dataset.csv',sep='\t',dtype={'FIPS Code':str})
state=state[~state.State.isin(['US','PR','DC'])].copy();assert len(state)==50

def frame(title,subtitle,caption,size=(11,7)):
 f=plt.figure(figsize=size);f.text(.06,.95,title,fontsize=18,ha='left');f.text(.06,.904,subtitle,fontsize=10.5,ha='left');f.text(.06,.035,caption,fontsize=9,ha='left',va='bottom',linespacing=1.5);return f

def finish(f,name):
 f.savefig(OUT/name,dpi=180);plt.close(f)

g7=['Canada','France','Germany','Italy','Japan','United Kingdom','United States']
l=life[(life['Country Name'].isin(g7)) & (life.Sex=='Both') & life.Year.between(2019,2023)].copy()
p=l.pivot(index='Country Name',columns='Year',values='Life Expectancy (years)');delta=p.sub(p[2019],axis=0);order=delta[2023].sort_values().index.tolist()
l.to_csv(ROOT/'work/g7_life.csv',index=False)
f=frame('G7 life expectancy: different paths back from 2019','Change in life expectancy at birth, both sexes • 2019 baseline = 0 years',
 'The United States had the deepest drop, but Germany ended 2023 furthest below its own 2019 level.\nSource: supplied World Bank life-expectancy data. G7 countries selected in advance; no group average.')
gs=f.add_gridspec(2,4,left=.07,right=.96,bottom=.20,top=.82,hspace=.58,wspace=.3)
for i,c in enumerate(order):
 ax=f.add_subplot(gs[i//4,i%4]);ax.axhline(0,color='#aaaaaa',lw=1);ax.plot(delta.columns,delta.loc[c],color=blue,marker='o',ms=4,lw=2)
 ax.set_title(c,loc='left',fontsize=11,pad=10);ax.set_ylim(-2.8,.65);ax.set_xticks([2019,2021,2023]);ax.set_yticks([-2,-1,0]);ax.grid(axis='y',color='#eeeeee');ax.text(2023,delta.loc[c,2023]+.13,f'{delta.loc[c,2023]:+.2f}',ha='center',fontsize=9)
 if i%4==0:ax.set_ylabel('Years from 2019')
ax=f.add_subplot(gs[1,3]);ax.axis('off');ax.text(0,.7,'Each pane has the same scale.\n\nEndpoint labels show the\n2023 change in years.',fontsize=10,va='top',linespacing=1.8)
finish(f,'01_g7_paths.png')
f=frame('Only Italy and France were above their 2019 level','G7 • change in life expectancy at birth from 2019 to 2023 • both sexes',
 'The endpoint comparison shows recovery status; it does not show the depth or timing of the intervening drop.\nSource: supplied World Bank life-expectancy data. Values rounded to 0.01 years; G7 countries selected in advance.')
ax=f.add_axes([.19,.22,.71,.60]);v=delta.loc[order,2023];ax.barh(range(7),v,color=[orange if x<0 else blue for x in v],height=.55);ax.set_yticks(range(7),order);ax.invert_yaxis();ax.axvline(0,color='#777777',lw=1);ax.set_xlim(-.9,.35);ax.set_xlabel('2023 minus 2019 life expectancy (years)');ax.grid(axis='x',color='#eeeeee');ax.set_axisbelow(True)
for i,x in enumerate(v):ax.text(x+(.02 if x>=0 else -.02),i,f'{x:+.2f}',ha='left' if x>=0 else 'right',va='center')
finish(f,'02_g7_endpoint.png')

c=county[(county.State!='PR') & county['2023 Rural-urban Continuum Code'].between(1,9)].dropna(subset=['Natural Change Rate 2023','Net Migration Rate 2023']).copy()
x=c['Natural Change Rate 2023'];y=c['Net Migration Rate 2023'];c['County group']=np.where(c['2023 Rural-urban Continuum Code']<=3,'Metro','Nonmetro')
c['Pattern']=np.select([x>=0,(x<0)&(y>=-x),(x<0)&(y>0)],['No natural decrease','Migration offsets decrease','Migration partially offsets'],default='No migration offset')
patterns=['No natural decrease','Migration offsets decrease','Migration partially offsets','No migration offset'];colors=[blue,teal,orange,red]
count=pd.crosstab(c['County group'],c.Pattern).reindex(index=['Metro','Nonmetro'],columns=patterns,fill_value=0);pct=count.div(count.sum(axis=1),axis=0)*100
print('County counts:',count.to_string());print('County percentages:',pct.round(2).to_string());c[['FIPS Code','State','Area name','County group','Pattern','Natural Change Rate 2023','Net Migration Rate 2023']].to_csv(ROOT/'work/county_patterns.csv',index=False);count.to_csv(ROOT/'work/county_pattern_counts.csv')
f=frame('Migration offsets natural decline in many counties','2023 county patterns • every county counts equally • metro vs. nonmetro',
 'Natural decrease means deaths exceed births. Full offset means net migration ≥ the size of that decrease.\nSource: supplied USDA county data. U.S. counties/equivalents, excluding Puerto Rico; complete records only.\nMetro = 2023 rural–urban codes 1–3; nonmetro = 4–9. Rates rounded in the source; equality counts as offset.')
ax=f.add_axes([.15,.38,.79,.40]);left=np.zeros(2)
for pat,col in zip(patterns,colors):
 vals=pct[pat].values;ax.barh([0,1],vals,left=left,height=.55,color=col,label=pat)
 for j,val in enumerate(vals):ax.text(left[j]+val/2,j,f'{val:.1f}%',ha='center',va='center',fontsize=10,color='#222222')
 left+=vals
ax.set_yticks([0,1],[f'Metro\nn = {count.loc["Metro"].sum():,}',f'Nonmetro\nn = {count.loc["Nonmetro"].sum():,}']);ax.invert_yaxis();ax.set_xlim(0,100);ax.set_xlabel('Share of counties (%)');ax.set_xticks([0,25,50,75,100]);ax.legend(loc='upper center',bbox_to_anchor=(.5,-.25),ncol=2,frameon=False,fontsize=9)
finish(f,'03_county_shares.png')
f=frame('County rates reveal how migration offsets natural decline','2023 • natural change = births − deaths • net migration = domestic + international',
 'Above the diagonal, migration exceeds natural decrease (when x < 0); below it, the two components sum negative.\nSource: supplied USDA county data; same complete-record county subset and classifications as the percentage bars.\nFixed plotting window emphasizes the main cluster; counts outside the window are shown in each pane. Rates per 1,000.',size=(11,7.5))
for j,group in enumerate(['Metro','Nonmetro']):
 ax=f.add_axes([.09+j*.46,.25,.39,.55]);sub=c[c['County group']==group]
 for pat,col in zip(patterns,colors):
  s=sub[sub.Pattern==pat];ax.scatter(s['Natural Change Rate 2023'],s['Net Migration Rate 2023'],s=12,color=col,alpha=.48,edgecolors='none',label=pat)
 ax.set_xlim(-20,20);ax.set_ylim(-40,80);ax.set_xticks([-20,-10,0,10,20]);ax.set_yticks([-40,-20,0,20,40,60,80]);ax.axvline(0,color='#aaaaaa',lw=.7);ax.axhline(0,color='#aaaaaa',lw=.7)
 z=np.linspace(-100,0,400);ax.plot(z,-z,color='#555555',lw=1,ls='--');outside=(~sub['Natural Change Rate 2023'].between(-20,20) | ~sub['Net Migration Rate 2023'].between(-40,80)).sum();ax.set_title(f'{group} (n = {len(sub):,}; {outside} outside window)',loc='left',fontsize=10);ax.set_xlabel('Natural change per 1,000');ax.set_ylabel('Net migration per 1,000' if j==0 else '');ax.grid(color='#eeeeee',lw=.5);ax.set_axisbelow(True)
f.legend(*ax.get_legend_handles_labels(),loc='upper center',bbox_to_anchor=(.52,.88),ncol=2,frameon=False,fontsize=9)
finish(f,'04_county_rates.png')

sub=life[life['Country Code'].isin(['KOR','JPN']) & life.Sex.isin(['Female','Male'])].copy();sub.to_csv(ROOT/'work/japan_korea_sex.csv',index=False)
f=frame('South Korea nearly closed Japan’s life-expectancy lead','Life expectancy at birth by sex • 1960–2023 • Japan and South Korea',
 'In 1960, Japan led by 13.8 years for women and 13.9 for men; in 2023 the leads were 0.7 and 0.5 years.\nSource: supplied World Bank data (South Korea appears as “Korea, Rep.”). Descriptive comparison; no causal claim.\nThe sharp late-1960s step is retained from the supplied estimates; its cause is not established here.')
for i,sex in enumerate(['Female','Male']):
 ax=f.add_axes([.09+i*.46,.23,.39,.56]);ax.set_title(sex,loc='left',fontsize=12)
 for code,col,name in [('JPN',blue,'Japan'),('KOR',orange,'South Korea')]:
  s=sub[(sub['Country Code']==code)&(sub.Sex==sex)].sort_values('Year');ax.plot(s.Year,s['Life Expectancy (years)'],color=col,lw=2,label=name)
  ax.scatter(s.Year.iloc[-1],s['Life Expectancy (years)'].iloc[-1],color=col,s=22)
 ax.set_ylim(45,90);ax.set_xlim(1960,2025);ax.set_xticks([1960,1980,2000,2023]);ax.set_yticks([50,60,70,80,90]);ax.grid(axis='y',color='#eeeeee');ax.set_xlabel('Year');ax.set_ylabel('Life expectancy (years)' if i==0 else '')
f.legend(*ax.get_legend_handles_labels(),loc='upper center',bbox_to_anchor=(.52,.875),ncol=2,frameon=False)
finish(f,'05_japan_korea.png')

Y=list(range(2007,2024));m=state.set_index('State')[[f'Unemployment rate {y}' for y in Y]];m.columns=Y;m=m.sort_values(2020,ascending=False);m.to_csv(ROOT/'work/state_unemployment.csv')
f=frame('The 2020 unemployment spike was uneven across states','Annual unemployment rate (%) • 50 states • sorted by 2020 rate, highest first',
 'Hawaii and Nevada led in 2020; many states had higher annual rates during the 2009–2011 downturn.\nSource: supplied USDA state aggregates; excludes D.C., Puerto Rico, and the U.S. total.\nAnnual averages hide within-year peaks. Color scale is fixed across all states and years.',size=(11,12))
ax=f.add_axes([.10,.14,.74,.73]);im=ax.imshow(m.values,aspect='auto',cmap='Blues',vmin=0,vmax=15);ax.set_yticks(range(50),m.index,fontsize=8);ax.set_xticks(range(len(Y)),Y,rotation=45,ha='right',fontsize=9);ax.tick_params(length=0);ax.set_xlabel('Year');ax.set_ylabel('State');ax.set_xticks(np.arange(-.5,17,1),minor=True);ax.set_yticks(np.arange(-.5,50,1),minor=True);ax.grid(which='minor',color='white',lw=.4);ax.tick_params(which='minor',length=0)
for i in range(50):
 for j in [3,13]:
  val=m.iloc[i,j];ax.text(j,i,f'{val:.1f}',fontsize=6.7,ha='center',va='center',color='white' if val>=8 else '#333333')
cb=f.colorbar(im,cax=f.add_axes([.88,.59,.025,.25]));cb.set_label('Unemployment (%)');cb.set_ticks([0,5,10,15]);f.text(.875,.53,'Labels in\n2010 and 2020\nshow exact rates.',fontsize=9,va='top',linespacing=1.5)
finish(f,'06_state_unemployment.png')
print('Generated six figures.')
