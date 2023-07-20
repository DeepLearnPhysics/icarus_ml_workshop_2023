import os
import matplotlib.pyplot as plt
from datetime import date

#Date info
day = date.today().strftime("%Y_%m_%d")

def save_plot(fname,fig=None,ftype='.png',dpi=300,folder_name=f'Plots/Plots_{day}'):
    #print(f'Plots/{folder_name}')
    os.system(f'mkdir -p {folder_name}')
    if fig == None:
      plt.savefig(f'{fname}{ftype}',bbox_inches = "tight",dpi=dpi)
    else:
      fig.savefig(f'{fname}{ftype}',bbox_inches = "tight",dpi=dpi)
    os.system("mv " + fname + f"*{ftype} {folder_name}/")

def set_style(ax,legend_size=16,legend_loc='best',axis_size=16,title_size=20,tick_size=16,
              bbox_to_anchor=None):
  ax.tick_params(axis='x', labelsize=tick_size)
  ax.tick_params(axis='y', labelsize=tick_size)
  ax.xaxis.label.set_size(axis_size)
  ax.yaxis.label.set_size(axis_size)
  ax.title.set_size(title_size)
  if ax.get_legend() is not None:
    if bbox_to_anchor is not None:
      ax.legend(bbox_to_anchor=bbox_to_anchor,fontsize=legend_size)
    else:
      ax.legend(loc=legend_loc,fontsize=legend_size)
