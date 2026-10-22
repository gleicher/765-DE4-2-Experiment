import pandas as pd, numpy as np
w=pd.read_csv('data/lifespan_dataset_1960.csv',index_col=0)
p=w.pivot_table(index=['Country Name','Country Code','Year'],columns='Sex',values='Life Expectancy (years)').reset_index()
p['gap']=p.Female-p.Male
print(sorted(p['Country Name'].unique()))
