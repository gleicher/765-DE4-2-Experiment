import pandas as pd
c=pd.read_csv('data/full_census_dataset.csv',encoding='cp1252',dtype={'FIPS Code':str},low_memory=False)
c['FIPS Code']=c['FIPS Code'].str.zfill(5)
c=c[(c.State!='PR') & (~c['FIPS Code'].str.endswith('000')) & c['2023 Rural-urban Continuum Code'].notna()].copy()
cols=['Natural Change Rate 2023','Net Migration Rate 2023']
v=c.dropna(subset=cols).copy(); v['loss']=v[cols[0]]<0;v['offset']=v[cols].sum(axis=1)>=0
print('county counts',len(c),len(v));print(v.groupby(v['2023 Rural-urban Continuum Code']<=3).agg(n=('loss','size'),loss=('loss','sum')))
for metro,g in v.groupby(v['2023 Rural-urban Continuum Code']<=3):
 z=g[g.loss];print(metro,len(z),z.offset.sum(),len(z[z.offset])/len(z))
print(v[cols].describe(percentiles=[.01,.99]))
for m,g in c.groupby(c['2023 Rural-urban Continuum Code']<=3):
 for metric in ['not high school graduates',"with a bachelor's degree or higher"]:
  a=f'Percent of adults who are {metric}, 2000' if metric.startswith('not') else f'Percent of adults {metric}, 2000'
  b=a.replace('2000','2019-23');z=g.dropna(subset=[a,b]);print(m,metric,len(z),z[a].quantile([.25,.5,.75]).round(1).tolist(),z[b].quantile([.25,.5,.75]).round(1).tolist())
