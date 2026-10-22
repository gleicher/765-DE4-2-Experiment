from pathlib import Path
import os
ROOT=Path(__file__).resolve().parents[1]
os.environ['MPLCONFIGDIR']=str(ROOT/'work/mpl-cache')
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
OUT=ROOT/'answers/figures';OUT.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'axes.spines.left':False,'axes.spines.bottom':False,'axes.labelcolor':'#354354','text.color':'#172c40','xtick.color':'#556575','ytick.color':'#556575','axes.facecolor':'#faf9f5','figure.facecolor':'#faf9f5','savefig.facecolor':'#faf9f5','axes.axisbelow':True})
TEAL='#007f83';ORANGE='#c05b35';BLUE='#365b9a';GRAY='#c4cbd0'
def header(fig,num,title,sub):
 fig.text(.055,.952,f'FIELD NOTES   /   {num}',fontsize=10,color=TEAL,weight='bold')
 fig.text(.055,.9,title,fontsize=24,weight='bold')
 fig.text(.055,.855,sub,fontsize=11,color='#526372')
def footer(fig,text):fig.text(.055,.035,text,fontsize=9,color='#526372',linespacing=1.5)
def save(fig,name):
 fig.savefig(OUT/(name+'.png'),dpi=180);fig.savefig(OUT/(name+'.svg'));plt.close(fig)
def grid(ax,axis='y'):ax.grid(axis=axis,color='#dfe3e4',lw=.7)
l=pd.read_csv(ROOT/'data/lifespan_dataset_1960.csv');val='Life Expectancy (years)'
codes=['MEX','IND','BRA','USA','SWE','JPN'];names={'MEX':'Mexico','IND':'India','BRA':'Brazil','USA':'United States','SWE':'Sweden','JPN':'Japan'}
life=l[l['Country Code'].isin(codes)&l.Sex.isin(['Female','Male']) & (l.Year>=2015)].copy()
life.to_csv(ROOT/'work/life_selected.csv',index=False)
fig,axs=plt.subplots(2,3,figsize=(13,9),sharex=True,sharey=True);fig.subplots_adjust(left=.08,right=.96,bottom=.16,top=.76,hspace=.37,wspace=.17)
header(fig,'01A','Recovery did not look the same for everyone','Life expectancy at birth, 2015–2023 • Six selected countries • Women and men shown separately')
for ax,code in zip(axs.flat,codes):
 ax.axvspan(2019.5,2021.5,color='#e8e4da');ax.set_title(names[code],loc='left',weight='bold',fontsize=13)
 for sex,col in [('Female',TEAL),('Male',ORANGE)]:
  d=life[(life['Country Code']==code)&(life.Sex==sex)].sort_values('Year');ax.plot(d.Year,d[val],color=col,lw=2.4);ax.scatter(d.Year.iloc[-1],d[val].iloc[-1],s=25,color=col);ax.text(2023.12,d[val].iloc[-1],f'{d[val].iloc[-1]:.1f}',color=col,va='center',fontsize=9)
 ax.set_xlim(2015,2024);ax.set_ylim(64,89);ax.set_xticks([2015,2019,2023]);grid(ax)
for ax in axs[:,0]:ax.set_ylabel('Life expectancy (years)')
fig.text(.73,.8,'● Women',color=TEAL,weight='bold');fig.text(.84,.8,'● Men',color=ORANGE,weight='bold')
footer(fig,'Shared scales preserve between-country differences; shading marks 2020–2021, not a causal estimate.\nPurposive contrast set, not a global sample. Source: supplied World Bank life-expectancy file. Period estimates, not individual lifespans.')
save(fig,'01a_life_trajectories')
# alternate
fig,axs=plt.subplots(1,2,figsize=(13,9),sharex=True,sharey=True);fig.subplots_adjust(left=.17,right=.96,bottom=.17,top=.75,wspace=.15)
header(fig,'01B','The loss and the recovery, measured from 2019','Change in life expectancy (years) • The same six countries and both sexes • 2019 = zero')
summary=[]
for ax,sex,col in zip(axs,['Female','Male'],[TEAL,ORANGE]):
 ax.set_title('Women' if sex=='Female' else 'Men',loc='left',weight='bold',color=col);ax.axvline(0,color='#6a7680',lw=1)
 for i,code in enumerate(codes):
  s=life[(life['Country Code']==code)&(life.Sex==sex)].set_index('Year')[val];a=s[2021]-s[2019];b=s[2023]-s[2019];summary.append([code,sex,a,b]);ax.plot([a,b],[i,i],color=col,lw=3,alpha=.65);ax.scatter(a,i,s=70,color=col,marker='o');ax.scatter(b,i,s=80,facecolor='#faf9f5',edgecolor=col,lw=2,marker='D');ax.text(a,i-.17,f'{a:+.1f}',ha='center',va='bottom',fontsize=10,color=col);ax.text(b,i+.17,f'{b:+.1f}',ha='center',va='top',fontsize=10,color=col)
 ax.set_xlim(-6.5,2);ax.set_xlabel('Change from 2019 (years)');grid(ax,'x')
axs[0].set_yticks(range(6),[names[x] for x in codes]);axs[0].invert_yaxis()
fig.text(.17,.8,'● 2021      ◇ 2023     Line joins the two snapshots; labels show signed changes.',fontsize=11)
footer(fig,'A point left of zero is still below its 2019 level. These are snapshots; 2021 is not necessarily the country’s minimum.\nCountries were selected for contrasting patterns, not representativeness. Source: supplied World Bank life-expectancy file.')
save(fig,'01b_life_recovery');pd.DataFrame(summary,columns=['code','sex','change_2021','change_2023']).to_csv(ROOT/'work/life_changes.csv',index=False)
# Census
c=pd.read_csv(ROOT/'data/full_census_dataset.csv',encoding='cp1252');c=c[(c.State!='PR')&(c['FIPS Code']%1000!=0)].copy();r='2023 Rural-urban Continuum Code';c=c[c[r].between(1,9)].copy();c['group']=np.where(c[r]<=3,'Metro','Nonmetro')
n='Natural Change Rate 2023';m='Net Migration Rate 2023';d=c.dropna(subset=[n,m]).copy();d['sum']=d[n]+d[m];d['category']=np.select([(d[n]<0)&(d['sum']>=0),(d[n]<0)&(d['sum']<0),(d[n]>=0)&(d['sum']>=0)],['Natural decline, offset','Natural decline, not offset','Natural gain, net gain'],default='Natural gain, net loss')
d[['FIPS Code','State','Area name','group',n,m,'sum','category']].to_csv(ROOT/'work/migration_classification.csv',index=False)
fig,axs=plt.subplots(1,2,figsize=(13,9),sharex=True,sharey=True);fig.subplots_adjust(left=.09,right=.96,bottom=.19,top=.75,wspace=.12)
header(fig,'02A','More nonmetro counties lose people naturally','County components of population change, 2023 • Rates per 1,000 residents • 50 states + DC')
for ax,g,col in zip(axs,['Metro','Nonmetro'],[BLUE,TEAL]):
 s=d[d.group==g];shown=s[s[n].between(-22,16)&s[m].between(-42,55)];ax.scatter(shown[n],shown[m],s=14,color=col,alpha=.32,edgecolors='none');ax.axvline(0,color='#7a858e',lw=.8);ax.axhline(0,color='#7a858e',lw=.8);x=np.array([-22,16]);ax.plot(x,-x,color=ORANGE,lw=1.7,ls='--');ax.set_xlim(-22,16);ax.set_ylim(-42,55);grid(ax);ax.set_title(f'{g}  |  n = {len(s):,}',loc='left',weight='bold');ax.set_xlabel('Natural change: births − deaths / 1,000');ax.text(.03,.94,'Above dashed line: migration + natural change > 0',transform=ax.transAxes,fontsize=9);ax.text(.03,.04,f'{len(s)-len(shown)} extreme points outside window',transform=ax.transAxes,fontsize=9)
axs[0].set_ylabel('Net migration / 1,000 residents')
footer(fig,'Each dot is one county or county equivalent; equal visual weight does not imply equal population. The dashed line is migration = −natural change.\nNatural decline is x < 0; only points above the diagonal have that decline offset. Residual adjustments are excluded from this component sum.\nMetro = 2023 RUCC 1–3; nonmetro = 4–9. Source: supplied USDA county file. Full observations are included in the alternate summary.')
save(fig,'02a_migration_balance')
# categorical alternate
cats=['Natural decline, not offset','Natural decline, offset','Natural gain, net gain','Natural gain, net loss'];cols=[ORANGE,TEAL,BLUE,'#8f7ca5'];fig,ax=plt.subplots(figsize=(13,9));fig.subplots_adjust(left=.18,right=.95,bottom=.28,top=.69)
header(fig,'02B','Migration offsets decline less often outside metros','Share of counties by natural change and migration balance, 2023 • Every county counts once')
fig.text(.18,.77,'Among counties with natural decline: 68% offset in metros; 49% in nonmetros.',fontsize=12,color=TEAL,weight='bold')
metrics={}
for y,g in enumerate(['Metro','Nonmetro']):
 s=d[d.group==g];left=0;metrics[g]={}
 for cat,col in zip(cats,cols):
  count=(s.category==cat).sum();p=count/len(s)*100;metrics[g][cat]=int(count);ax.barh(y,p,left=left,color=col,height=.4)
  if p>5:ax.text(left+p/2,y,f'{p:.1f}%\n'+(f'(n={count:,})' if p<15 else f'{count:,} counties'),ha='center',va='center',color='white',fontsize=9 if p<15 else 11,weight='bold')
  left+=p
 ax.text(101,y,f'n={len(s):,}',va='center',fontsize=10)
ax.set_xlim(0,110);ax.set_xticks([0,25,50,75,100],['0%','25%','50%','75%','100%']);ax.set_yticks([0,1],['Metro','Nonmetro']);ax.invert_yaxis();ax.set_xlabel('Share of counties');grid(ax,'x')
for i,(cat,col) in enumerate(zip(cats,cols)):fig.text(.18+(i%2)*.40,.20-(i//2)*.045,'■ '+cat,color=col,weight='bold',fontsize=11)
footer(fig,'“Offset” means net migration + natural change ≥ 0 where natural change < 0; zero natural change is grouped with natural gain.\nThe sum excludes residual adjustments and is not an exact classification of official total population growth. Classification uses supplied rates before display rounding.\nMetro = 2023 RUCC 1–3; nonmetro = 4–9. Source: supplied USDA county file; 50 states + DC; missing RUCC/rates excluded.')
save(fig,'02b_migration_shares')
# unemployment group trajectories aligned episodes
fig,axs=plt.subplots(1,2,figsize=(13,9),sharey=True);fig.subplots_adjust(left=.09,right=.95,bottom=.21,top=.75,wspace=.15)
header(fig,'03','Two labor-market shocks, two different aftermaths','Pooled unemployment rate relative to each episode’s starting year • Percentage-point change')
rows=[]
for ax,start in zip(axs,[2007,2019]):
 ax.set_title(f'{start}–{start+4}',loc='left',weight='bold');ax.axhline(0,color='#7a858e',lw=1)
 for g,col in [('Metro',BLUE),('Nonmetro',TEAL)]:
  s=c[c.group==g];need=[f'{p} {y}' for y in range(start,start+5) for p in ['Unemployed','Civilian labor force']];s=s.dropna(subset=need);rates=[100*s[f'Unemployed {y}'].sum()/s[f'Civilian labor force {y}'].sum() for y in range(start,start+5)];delta=np.array(rates)-rates[0];ax.plot(range(5),delta,color=col,lw=3,marker='o');ax.text(4.08,delta[-1],f'{delta[-1]:+.1f}',color=col,va='center',weight='bold');rows.extend([[start,g,start+i,rates[i],delta[i],len(s)] for i in range(5)]);ax.text(.04,.93 if g=='Metro' else .85,f'{g}: starts at {rates[0]:.1f}% (n={len(s):,})',color=col,transform=ax.transAxes)
 ax.set_xticks(range(5),[str(start+i) for i in range(5)]);ax.set_xlim(-.15,4.5);ax.set_ylim(-1.5,6);grid(ax);ax.set_xlabel('Calendar year (matched four-year follow-up)')
axs[0].set_ylabel('Change in pooled unemployment rate (pp)');fig.text(.7,.8,'● Metro',color=BLUE,weight='bold');fig.text(.82,.8,'● Nonmetro',color=TEAL,weight='bold')
footer(fig,'Rates = 100 × summed unemployed / summed civilian labor force, not an average of county percentages. Fixed complete counties within each panel.\n2007 and 2019 are descriptive baselines; differencing does not equalize historical conditions or establish causes. Classification fixed at 2023 RUCC.\nSource: supplied USDA county file; 50 states + DC; metro 1–3, nonmetro 4–9. No seasonal or age adjustment is applied.')
save(fig,'03_unemployment_aftermaths');pd.DataFrame(rows,columns=['baseline','group','year','rate','delta','n']).to_csv(ROOT/'work/unemployment_summary.csv',index=False)
# Education changes
low='Percent of adults who are not high school graduates, ';high="Percent of adults with a bachelor's degree or higher, "
e=c.dropna(subset=[low+'2000',low+'2019-23',high+'2000',high+'2019-23']).copy();e['less_hs_decline']=e[low+'2000']-e[low+'2019-23'];e['ba_gain']=e[high+'2019-23']-e[high+'2000'];fig,ax=plt.subplots(figsize=(13,9));fig.subplots_adjust(left=.10,right=.92,bottom=.20,top=.75)
header(fig,'04','Two kinds of educational progress diverge','County education change, 2000 → 2019–2023 • Percentage points • Adults aged 25 and older')
for g,col in [('Nonmetro',TEAL),('Metro',BLUE)]:
 s=e[e.group==g];ax.scatter(s.less_hs_decline,s.ba_gain,s=17,color=col,alpha=.27,edgecolors='none');mx=s.less_hs_decline.median();my=s.ba_gain.median();ax.scatter(mx,my,s=180,color=col,marker='D',edgecolor='white',lw=1.5,zorder=4);ax.annotate(f'{g} median\n({mx:.1f}, {my:.1f})',xy=(mx,my),xytext=(mx+7,my+(9 if g=='Metro' else -7)),arrowprops={'arrowstyle':'-','color':col},color=col,weight='bold',fontsize=11)
ax.axhline(0,color='#89939a',lw=1);ax.axvline(0,color='#89939a',lw=1);ax.plot([-10,36],[-10,36],ls='--',color='#7b858e',lw=1);ax.set_xlim(-10,36);ax.set_ylim(-10,40);grid(ax);ax.set_xlabel('Decline in share without a high-school diploma (pp) →');ax.set_ylabel('Gain in share with a bachelor’s degree or higher (pp) →');ax.text(-8,35,'Above diagonal: bachelor’s gain is larger',fontsize=10,color='#526372');fig.text(.58,.8,'● Metro',color=BLUE,weight='bold');fig.text(.70,.8,'● Nonmetro',color=TEAL,weight='bold');fig.text(.83,.8,'◆ Medians',weight='bold')
footer(fig,f'Each dot is one county (n={len(e):,}); diamonds locate separate medians of the two changes, not an actual “median county.” All points shown.\nThese are changes in place-level shares, not transitions of the same people. 2019–2023 is a pooled estimate, not a single-year census.\nSource: supplied USDA county file; 50 states + DC; complete paired percentages; metro = 2023 RUCC 1–3, nonmetro = 4–9.')
save(fig,'04_education_two_changes');e[['FIPS Code','State','Area name','group','less_hs_decline','ba_gain']].to_csv(ROOT/'work/education_changes.csv',index=False)
import json
(ROOT/'work/summary.json').write_text(json.dumps({'migration':metrics,'migration_n':len(d),'education_n':len(e),'education_medians':e.groupby('group')[['less_hs_decline','ba_gain']].median().round(3).to_dict()},indent=2))
print((ROOT/'work/summary.json').read_text());print(pd.DataFrame(rows).to_string(index=False))
