import pandas as pd
c=pd.read_csv('data/full_census_dataset.csv',encoding='cp1252',low_memory=False)
c=c[(c['FIPS Code']%1000!=0)&c.State.ne('PR')].copy()
k='2023 Rural-urban Continuum Code'
cols=['Natural Change 2023','Domestic migration 2023','International Migration 2023','Population Estimate 2022','Population Estimate 2023']
v=c.dropna(subset=[k]+cols);g=v.groupby(k)[cols].sum();den=(g['Population Estimate 2022']+g['Population Estimate 2023'])/2
print('counts',len(c),len(v));print((g[cols[:3]].div(den,axis=0)*1000).round(2).to_string())
c['group']=pd.cut(c[k],[0,3,7,9],labels=['Metro','Larger nonmetro','Smallest nonmetro'])
for group,d in c.groupby('group',observed=True):
 print(group,len(d))
 for t in ['1990','2019-23']:
  b=d[f"Bachelor's degree or higher, {t}"];n=d[[f'Less than high school graduate, {t}',f'High school graduate (or equivalency), {t}',f'Some college or associate degree, {t}',f"Bachelor's degree or higher, {t}"]].sum(axis=1,min_count=4)
  print(t,100*b.sum()/n.sum())
l=pd.read_csv('data/lifespan_dataset_1960.csv');
for code in ['ZAF','RWA','RUS','USA']:
 d=l[(l['Country Code']==code)&l.Sex.eq('Both')].set_index('Year')['Life Expectancy (years)']; sub=d.loc[1990:2023]; y=sub.idxmin(); base=d.loc[1990]; rec=sub.loc[y:];rec=rec[rec>=base];print(code,base,y,sub.min(),rec.index.min(),sub.loc[2023])
