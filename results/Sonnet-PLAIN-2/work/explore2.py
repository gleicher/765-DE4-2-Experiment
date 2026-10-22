import pandas as pd, numpy as np
c=pd.read_csv('data/full_census_dataset.csv',dtype={'FIPS Code':str},encoding='latin-1')
c['rucc']=c['Rural Urban Continuum Code 2023']
c['metro']=np.where(c.rucc<=3,'Metro','Nonmetro')
for g,d in c.dropna(subset=['rucc']).groupby('rucc'):
    print(g, len(d), [round(d[f"Percent of adults with a bachelor's degree or higher, {y}"].median(),1) for y in ['1990','2000','2008-12','2019-23']], [round(d[f'Unemployed {y}'].sum()/d[f'Civilian labor force {y}'].sum()*100,2) for y in [2007,2009,2010,2019,2020,2021,2023]])
print(c[['Area name','State']].head(3), c.State.unique()[:60])
