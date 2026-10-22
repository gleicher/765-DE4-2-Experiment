from pathlib import Path
import os
ROOT=Path(__file__).resolve().parents[1]
os.environ['MPLCONFIGDIR']=str(ROOT/'work/mplconfig')
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'axes.labelcolor':'#333333','text.color':'#222222','axes.edgecolor':'#aaaaaa','savefig.facecolor':'white'})
OUT=ROOT/'answers/figures'; OUT.mkdir(exist_ok=True,parents=True)
life=pd.read_csv(ROOT/'data/lifespan_dataset_1960.csv')
c=pd.read_csv(ROOT/'data/full_census_dataset.csv',encoding='cp1252',dtype={'FIPS Code':str})
blue='#2878a4'; orange='#d78032'; gray='#b7bec4'
def page(title,sub,footer):
 f=plt.figure(figsize=(11,8)); f.text(.09,.94,title,fontsize=20,weight='bold'); f.text(.09,.895,sub,fontsize=11)
 f.text(.09,.04,footer,fontsize=9,color='#555555',linespacing=1.5); return f
def save(f,name): f.savefig(OUT/name,dpi=180);plt.close(f)
codes=['RUS','JPN','FRA','USA','SWE','IND']; names={'RUS':'Russia','JPN':'Japan','FRA':'France','USA':'United States','SWE':'Sweden','IND':'India'}
p=life[life['Country Code'].isin(codes)].pivot(index=['Country Code','Year'],columns='Sex',values='Life Expectancy (years)');p['Gap']=p.Female-p.Male
p.to_csv(ROOT/'work/selected_life.csv')
f=page('The sex gap narrowed in some countries, widened in others','Female minus male life expectancy at birth · six selected countries · 1990–2023', 'Source: course-provided World Bank life expectancy data. Gap = female − male, in years.\nSelected countries illustrate contrasting trajectories; they are not a representative global sample.')
axs=f.subplots(2,3); f.subplots_adjust(left=.09,right=.95,bottom=.18,top=.80,hspace=.45,wspace=.25)
for ax,code in zip(axs.flat,codes):
 s=p.loc[code].loc[1990:2023,'Gap'];ax.plot(s.index,s,color=blue,lw=2); ax.scatter([1990,2023],s.loc[[1990,2023]],s=23,color=blue);ax.axhline(0,color=gray,lw=.8);ax.set_ylim(0,14);ax.set_xticks([1990,2005,2023]);ax.set_title(names[code],loc='left',fontsize=12,weight='bold');ax.grid(axis='y',alpha=.18);ax.text(2022,s.loc[2023]+.55,f'{s.loc[2023]:.1f}',ha='right',fontsize=10)
for ax in axs[:,0]: ax.set_ylabel('Gap (years)')
save(f,'01_life_gap_lines.png')
f=page('India’s gap widened; France’s narrowed','Female minus male life expectancy · same six countries · 1990 versus 2023','Source: course-provided World Bank data. Points are endpoints, not the intervening trajectory.\nCountries sorted by 2023 gap. A positive gap means women have higher life expectancy at birth.')
ax=f.add_axes([.20,.20,.67,.61]);order=sorted(codes,key=lambda k:p.loc[(k,2023),'Gap'],reverse=True)
for i,k in enumerate(order):
 a,b=p.loc[(k,1990),'Gap'],p.loc[(k,2023),'Gap'];ax.plot([a,b],[i,i],color=gray,lw=4);ax.scatter(a,i,s=70,facecolors='white',edgecolors=orange,lw=2,zorder=3);ax.scatter(b,i,s=70,color=blue,zorder=4);ax.text(max(a,b)+.35,i,f'{b-a:+.1f} yr',va='center',fontsize=10)
ax.set_yticks(range(6),[names[k] for k in order]);ax.invert_yaxis();ax.set_xlim(0,13);ax.set_xlabel('Female − male life expectancy (years)');ax.grid(axis='x',alpha=.2)
ax.legend(handles=[Line2D([],[],marker='o',linestyle='',markerfacecolor='white',markeredgecolor=orange,label='1990'),Line2D([],[],marker='o',linestyle='',color=blue,label='2023')],loc='lower right',frameon=False)
save(f,'02_life_gap_dumbbell.png')
w=c[c.State.eq('WI') & c['2023 Rural-urban Continuum Code'].notna()].copy();w['Group']=np.where(w['2023 Rural-urban Continuum Code']<=3,'Metro','Nonmetro'); x='Natural Change Rate 2023';y='Net Migration Rate 2023';w['Balance']=w[x]+w[y];w['Class']=np.select([w[x]>=0,(w[x]<0)&(w.Balance>=0)],['Natural change ≥ 0','Migration offsets natural loss'],default='Natural loss not offset');w[['FIPS Code','Area name','Group',x,y,'Balance','Class']].to_csv(ROOT/'work/wisconsin_balance.csv',index=False)
print(w.groupby(['Group','Class']).size().to_string())
f=page('Migration often offsets natural population loss','Wisconsin’s 72 counties · 2023 · each point is one county','Source: course-provided USDA/US Census county data. Rates per 1,000 residents; 2023 RUCC: metro 1–3, nonmetro 4–9.\nBalance shown is natural change + net migration; official population change also includes a residual.')
ax=f.add_axes([.10,.20,.79,.60]);ax.axvspan(-12,0,color='#f5f5f5');ax.axhline(0,color='#999999',lw=.8);ax.axvline(0,color='#999999',lw=.8); xx=np.array([-12,7]);ax.plot(xx,-xx,'--',color='#555555',lw=1);ax.text(-10.8,11.2,'Zero component balance',rotation=-27,rotation_mode='anchor',fontsize=9,color='#555555')
for g,col,mark in [('Metro',blue,'o'),('Nonmetro',orange,'^')]:
 z=w[w.Group==g];ax.scatter(z[x],z[y],s=48,color=col,marker=mark,alpha=.85,edgecolor='white',linewidth=.4,label=f'{g} (n={len(z)})')
for name,shift in [('Adams County',(.3,.1)),('Dane County',(.25,.3)),('Milwaukee County',(.25,-.9))]:
 r=w[w['Area name']==name].iloc[0];ax.text(r[x]+shift[0],r[y]+shift[1],name.replace(' County',''),fontsize=9)
ax.set(xlim=(-12,7),ylim=(-6,20),xlabel='Natural change: births − deaths (per 1,000)',ylabel='Net migration (per 1,000)');ax.legend(frameon=False,loc='upper right');ax.grid(alpha=.13);save(f,'03_wisconsin_scatter.png')
colors=['#9baeb8','#2878a4','#d78032'];classes=['Natural change ≥ 0','Migration offsets natural loss','Natural loss not offset']
f=page('Most Wisconsin counties lose residents naturally','County counts, classified by migration’s ability to offset that loss · 2023','Source: course-provided county data. Metro = 2023 RUCC 1–3; nonmetro = 4–9. All 72 Wisconsin counties included.\nEach county has equal weight. “Offset” means natural change + net migration ≥ 0; residual change is excluded.')
ax=f.add_axes([.18,.33,.74,.43]);left=np.zeros(2)
for cl,col in zip(classes,colors):
 n=np.array([((w.Group==g)&(w.Class==cl)).sum() for g in ['Metro','Nonmetro']]);ax.barh([0,1],n,left=left,color=col,height=.45,label=cl)
 for j in range(2):
  if n[j]:ax.text(left[j]+n[j]/2,j,str(n[j]),ha='center',va='center',color='white',weight='bold')
 left+=n
ax.set_yticks([0,1],[f'Metro (n={(w.Group=="Metro").sum()})',f'Nonmetro (n={(w.Group=="Nonmetro").sum()})']);ax.invert_yaxis();ax.set_xlabel('Number of counties');ax.set_xlim(0,50);ax.grid(axis='x',alpha=.15);ax.set_axisbelow(True);ax.legend(loc='upper left',bbox_to_anchor=(-.08,-.30),frameon=False,ncol=1);save(f,'04_wisconsin_counts.png')
# Fixed present-day geography; county aggregation excludes totals and Puerto Rico.
z=c[c['2023 Rural-urban Continuum Code'].notna() & c.State.ne('PR')].copy();z['Group']=np.where(z['2023 Rural-urban Continuum Code']<=3,'Metro','Nonmetro')
rows=[]
for yr in range(2000,2024):
 for g in ['Metro','Nonmetro']:
  t=z[z.Group.eq(g)][[f'Unemployed {yr}',f'Civilian labor force {yr}']].dropna();t=t[t[f'Civilian labor force {yr}']>0];rows.append([yr,g,100*t[f'Unemployed {yr}'].sum()/t[f'Civilian labor force {yr}'].sum(),len(t)])
u=pd.DataFrame(rows,columns=['Year','Group','Rate','Count']);u.to_csv(ROOT/'work/unemployment_summary.csv',index=False)
f=page('Metro and nonmetro unemployment move together','Labor-force-weighted county unemployment rate · United States excluding Puerto Rico · 2000–2023','Source: course-provided county data. Rate = 100 × summed unemployed / summed civilian labor force.\nFixed 2023 RUCC groups (metro 1–3; nonmetro 4–9); available matched counties each year. Not an official national series.')
ax=f.add_axes([.10,.20,.77,.60])
for g,col in [('Metro',blue),('Nonmetro',orange)]:
 t=u[u.Group==g];ax.plot(t.Year,t.Rate,color=col,lw=2.5,label=g);ax.annotate(f'{g}\n{t.Rate.iloc[-1]:.1f}%',xy=(2023,t.Rate.iloc[-1]),xytext=(2023.6,4.6 if g=='Metro' else 2.6),color=col,va='center',fontsize=10,arrowprops={'arrowstyle':'-','color':col,'lw':.8})
ax.set(xlim=(2000,2026),ylim=(0,11),ylabel='Unemployment rate (%)',xlabel='Year');ax.set_xticks([2000,2005,2010,2015,2020,2023]);ax.grid(axis='y',alpha=.2);ax.legend(frameon=False,loc='upper left');save(f,'05_unemployment_lines.png')
select=['USA','JPN','SWE','FRA','BRA','IND'];change=pd.DataFrame({names.get(k,{'BRA':'Brazil'}.get(k,k)):p.loc[k,'Both'] if k in codes else life[life['Country Code'].eq(k)&life.Sex.eq('Both')].set_index('Year')['Life Expectancy (years)'] for k in select});change=change.loc[2019:2023];change=change-change.loc[2019];change=change[change.loc[2023].sort_values(ascending=False).index];change.to_csv(ROOT/'work/recovery_change.csv')
f=page('Recovery by 2023 was uneven across six countries','Change in life expectancy at birth from each country’s own 2019 level · both sexes','Source: course-provided World Bank data. Cells show years gained/lost relative to 2019, not absolute life expectancy.\nSelected countries illustrate different recovery patterns. Timing alone does not establish the cause of a decline.')
ax=f.add_axes([.20,.22,.65,.59]);v=change.T.to_numpy();im=ax.imshow(v,cmap='RdBu',vmin=-4,vmax=4,aspect='auto');ax.set_xticks(range(5),change.index);ax.set_yticks(range(6),change.columns)
for i in range(6):
 for j in range(5):ax.text(j,i,f'{v[i,j]:+.2f}',ha='center',va='center',color='white' if abs(v[i,j])>2.3 else '#222222')
cb=f.colorbar(im,ax=ax,fraction=.046,pad=.05);cb.set_label('Change (years)');ax.set_xlabel('Year');save(f,'06_life_recovery_heatmap.png')
print(change.round(2).to_string());print(u[u.Year.isin([2000,2010,2019,2020,2023])].to_string(index=False))
