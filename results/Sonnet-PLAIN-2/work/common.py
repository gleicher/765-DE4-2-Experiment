import re, pandas as pd, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.family':'DejaVu Sans','axes.spines.top':False,'axes.spines.right':False,
                     'axes.titleweight':'bold','figure.dpi':100,'savefig.dpi':200})
AGG = re.compile(r'income|IDA|IBRD|dividend|&|World|OECD|area$|Union|states$|countries|situations|Not classified|Middle East|Arab World|Heavily|Fragile|Least developed|Sub-Saharan|South Asia|Small states|Euro area|Africa')
# keep real country names with 'Africa' in them
KEEP = {'South Africa','Central African Republic'}
def is_country(n):
    return n in KEEP or not AGG.search(n)
def load_le():
    l=pd.read_csv('data/lifespan_dataset_1960.csv').rename(columns={'Life Expectancy (years)':'le','Country Name':'name','Country Code':'code'})
    w=l.pivot_table(index=['name','code','Year'],columns='Sex',values='le').reset_index()
    w['gap']=w.Female-w.Male
    w['country']=w.name.map(is_country)
    return w
def load_census():
    c=pd.read_csv('data/full_census_dataset.csv',dtype={'FIPS Code':str},encoding='latin-1').copy()
    return c
