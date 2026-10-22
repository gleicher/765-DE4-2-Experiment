import pandas as pd, numpy as np
D='../data/'
l=pd.read_csv(D+'lifespan_dataset_1960.csv',index_col=0)
o=pd.read_csv(D+'life-expectancy-owid/life-expectancy-owid.csv')
codes=set(o.dropna(subset=['Code']).query("~Code.str.startswith('OWID')").Code)
l=l[l['Country Code'].isin(codes)]
p=l.pivot_table(index=['Country Name','Year'],columns='Sex',values='Life Expectancy (years)').reset_index()
p['gap']=p.Female-p.Male
g=p.pivot(index='Country Name',columns='Year',values='gap')
print(len(g)); print(g[[1960,2023]].describe())
g['d']=g[2023]-g[1960]
print(g.sort_values('d').head(8)[[1960,2023,'d']]);print(g.sort_values('d').tail(8)[[1960,2023,'d']])
print(g[2023].sort_values().head(5), g[2023].sort_values().tail(5))
print(g.loc[['Russian Federation','United States','Japan','India','China','Afghanistan']][[1960,1980,1994,2000,2010,2023]])
