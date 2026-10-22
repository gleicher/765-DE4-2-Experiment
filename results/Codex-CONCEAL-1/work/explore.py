from pathlib import Path
import pandas as pd
c=pd.read_csv('data/full_census_dataset.csv',encoding='cp1252')
c=c[(c.State!='PR') & c['2023 Rural-urban Continuum Code'].between(1,9)].copy()
c['group']=c['2023 Rural-urban Continuum Code'].le(3).map({True:'Metro',False:'Nonmetro'})
n=c.dropna(subset=['Natural Change 2023','Net Migration 2023','Population Estimate 2023']); n=n[n['Natural Change 2023']<0].copy()
n['loss']=-1000*n['Natural Change 2023']/n['Population Estimate 2023'];n['migration']=1000*n['Net Migration 2023']/n['Population Estimate 2023']
n['status']='Migration gain, insufficient';n.loc[n['Net Migration 2023']<=0,'status']='No migration gain';n.loc[n['Net Migration 2023']>=-n['Natural Change 2023'],'status']='Migration offsets loss'
print(n.groupby(['group','status']).size());print(n[['loss','migration']].describe());print(n.sort_values('migration').tail()[['Area name','State','loss','migration']])
for g,v in c.groupby('group'):
 for y in ['2000','2019-23']:
  x=v[f"Percent of adults with a bachelor's degree or higher, {y}"].dropna();print(g,y,len(x),x.quantile([.25,.5,.75]).to_dict())
