from common import *
p=wb(); c=p[~p.is_agg]
print(c['Country Name'].nunique(), p[p.is_agg]['Country Name'].nunique())
c=c.assign(both=c.Both)
c['bin']=(c.both//5)*5
print(c.groupby('bin').gap.agg(['median','count',lambda s:s.quantile(.25),lambda s:s.quantile(.75)]))
for n in ['United States','Japan','Russian Federation','India','China','Korea, Rep.','Nigeria','Brazil','Poland','Germany','Iran, Islamic Rep.','Bangladesh']:
    s=c[c['Country Name']==n].set_index('Year')
    print(n, s.loc[[1960,1970,1980,1990,2000,2010,2023],'gap'].round(1).tolist(), s.loc[[1960,2023],'Both'].round(0).tolist())
