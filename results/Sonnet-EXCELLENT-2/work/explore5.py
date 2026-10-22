from common import *
pd.set_option('display.width',250); pd.set_option('display.max_columns',30)
d=census()
b90="Percent of adults with a bachelor's degree or higher, 1990"; b23="Percent of adults with a bachelor's degree or higher, 2019-23"
d['rucc']=d['2023 Rural-urban Continuum Code']
d['pop']=d['Census Population 2020']
g=d.groupby('rucc').agg(m90=(b90,'median'),m23=(b23,'median'),n=(b90,'size'),pop=('pop','sum'))
print(g)
d['grp']=pd.cut(d.rucc,[0,3,6,9],labels=['Metro','Nonmetro adjacent/urban','Rural'])
for k,s in d.groupby('grp'):
    print(k, s[b90].describe()[['25%','50%','75%']].tolist(), s[b23].describe()[['25%','50%','75%']].tolist(), s[b23].quantile(.9))
print(d[(d.rucc>=8)].sort_values(b23).tail(10)[['State','Area name',b90,b23,'pop']])
# top-gainers
print(d.sort_values(b23).tail(12)[['State','Area name',b90,b23,'rucc','pop']])
print(d[d.State=='CT'][['Area name',b23]])
# note CT planning regions
print(d['Area name'].str.contains('Planning').sum())
