import pandas as pd, numpy as np
l=pd.read_csv('data/lifespan_dataset_1960.csv').rename(columns={'Life Expectancy (years)':'le','Country Name':'name','Country Code':'code'})
w=l.pivot_table(index=['name','code','Year'],columns='Sex',values='le').reset_index()
w['gap']=w.Female-w.Male
print(w[w.name.isin(['World','United States','Russian Federation','China','Japan','India','Brazil','Nigeria','Germany'])&w.Year.isin([1960,1970,1980,1990,1995,2000,2010,2019,2021,2023])].pivot(index='name',columns='Year',values='gap').round(1))
