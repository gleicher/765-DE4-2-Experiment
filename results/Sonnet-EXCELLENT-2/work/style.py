import matplotlib as mpl
INK='#222222'; MUTED='#6b6b6b'; GRID='#e4e4e4'
# Okabe-Ito
BLUE='#0072B2'; ORANGE='#E69F00'; VERM='#D55E00'; GREEN='#009E73'; SKY='#56B4E9'; PINK='#CC79A7'; YEL='#B8A400'
def setup():
    mpl.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.edgecolor':'#999','axes.labelcolor':INK,
      'xtick.color':MUTED,'ytick.color':MUTED,'text.color':INK,'axes.spines.top':False,'axes.spines.right':False,
      'axes.titleweight':'bold','figure.dpi':100,'savefig.dpi':200,'figure.facecolor':'white','axes.facecolor':'white'})
import textwrap
def titles(fig,title,sub,cap,y0=0.985,sw=115,cw=150):
    sub=textwrap.fill(sub.replace('\n',' '),sw); cap='\n'.join(textwrap.fill(x,cw) for x in cap.split('\n\n'))
    fig.text(0.03,y0,title,fontsize=17,fontweight='bold',va='top',ha='left')
    fig.text(0.03,y0-0.052,sub,fontsize=11,color=MUTED,va='top',ha='left')
    fig.text(0.03,0.012,cap,fontsize=8.3,color=MUTED,va='bottom',ha='left',linespacing=1.4)
