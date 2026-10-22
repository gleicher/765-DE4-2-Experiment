import pandas as pd, numpy as np
o=pd.read_csv('data/life-expectancy-owid/life-expectancy-owid.csv'); o.columns=['ent','code','year','lex']
o=o[o.code.notna() & ~o.code.str.startswith('OWID',na=False)]
rows=[]
for e,g in o.groupby('ent'):
    g=g.sort_values('year')
    def cross(th):
        a=g[g.lex>=th]
        if len(a)==0: return np.nan
        y=a.year.iloc[0]
        if g.year.iloc[0]>=y and g.lex.iloc[0]>=th: return np.nan  # already above at first obs
        return y
    rows.append(dict(ent=e,first=g.year.min(),n=len(g),pre1950=(g.year<1950).sum(),c40=cross(40),c50=cross(50),c60=cross(60),c70=cross(70),le23=g[g.year==2023].lex.max()))
d=pd.DataFrame(rows)
d['t50_70']=d.c70-d.c50; d['t40_60']=d.c60-d.c40
print(d.pre1950.gt(0).sum(), 'with pre-1950')
print(d.dropna(subset=['t50_70']).sort_values('c50')[['ent','c40','c50','c60','c70','t50_70']].to_string())
print(d[d.c70.isna()].ent.tolist())
