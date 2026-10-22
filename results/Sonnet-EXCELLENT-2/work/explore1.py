import pandas as pd, numpy as np
w=pd.read_csv('data/lifespan_dataset_1960.csv',index_col=0)
p=w.pivot_table(index=['Country Name','Country Code','Year'],columns='Sex',values='Life Expectancy (years)').reset_index()
p['gap']=p.Female-p.Male
print(p.groupby('Year').gap.describe().iloc[::7])
# aggregates: codes? 
g=p.pivot(index='Country Name',columns='Year',values='gap')
print(g.isna().sum(axis=1).value_counts().head())
g=g.dropna()
d=pd.DataFrame({'g60':g[1960],'g90':g[1990],'gmax':g.max(axis=1),'ymax':g.idxmax(axis=1),'gmin':g.min(axis=1),'g23':g[2023],'g19':g[2019]})
d['peak_minus_now']=d.gmax-d.g23
print(d.sort_values('gmax',ascending=False).head(15))
print(d.sort_values('peak_minus_now',ascending=False).head(15))
print(d.g23.describe(), d.sort_values('g23').head(8), d.sort_values('g23').tail(8))
