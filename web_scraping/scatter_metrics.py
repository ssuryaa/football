import numpy as np
import pandas as pd 
import os 
import math
import matplotlib as mpl
import matplotlib.pyplot as plt 
plt.rcParams["font.family"] = "Latin Modern Roman"
# plt.rcParams["font.family"] = "Noto Mono"
# plt.rcParams["font.weight"] = "bold"
# plt.rcParams["axes.labelweight"] = "bold"
plt.rcParams["font.size"] = 12
plt.rcParams["figure.figsize"] = (10,6)
plt.rcParams['figure.dpi'] = 140
from matplotlib.pyplot import figure 
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
# figure(figsize=(400, 300), dpi=200)

def plot_scatter(raw_data, database, percentiles, stats):
    top = database['Age'].str.split('-')
    age_yr = []
    for x in range(len(top)):
        if isinstance(top[x], list):
            age_yr.append(top[x][0])
        else:
            age_yr.append(0)
    # print(database.shape)
    database['Age'] = age_yr
    database = database[database.Age != 0]
    # print(database.shape)
    database['Age'] = pd.to_numeric(database['Age'])

    # print(raw_data.sort_values(by=['SCA_Drib'], ascending=False)['SCA_Drib'][:5])
    # stats = ['Total_Pass_PrgDist', 'Carries_PrgDist']
    # print("\nMean 90s: {:2.2f} \t Median 90s: {:2.2f}\n".format(database['nineties'].mean(), database['nineties'].median()))
    # print(database.query('nineties > 8').sort_values(by=[s], ascending=False)[s][:10])
    d = {}
    for s in stats:
        df1 = database.query('nineties > 8').sort_values(by=[s], ascending=False)
        # print(df1.query('`Pos` == "MF" | `Pos` == "FW,MF" | `Pos` == "FW"')[s][:10])
        df2 = df1.query('`Pos` == "MF" | `Pos` == "FW,MF" | `Pos` == "FW"')[df1.Age < 23]
        # df3 = df2[df2.Age < 25]
        # print(df2[s][:20])
        d[s] = df2[s]
        #df2.plot(x=stats[0], y=stats[1])
        # exit()
    
    names = df2.index.values
    n = []
    for x in names:
        n.append(x.split())
    na = []
    for x in n:
        na.append(x[-1])

    fig, ax = plt.subplots()
    stat1_mean = df2[stats[0]].mean()
    stat2_mean = df2[stats[1]].mean()
    print(stat1_mean, stat2_mean)
    plot = ax.scatter(df2[stats[0]], df2[stats[1]], s=100, c=df2['nineties'], cmap='cool')
    
    # ax.set_xlim([0,350]) # prog pass/carry distance axis limits
    ax.set_xlim([ax.get_xlim()[0],ax.get_xlim()[1]+((ax.get_xlim()[0]+ax.get_xlim()[1])*0.15)])
    ax.set_ylim([ax.get_ylim()[0],ax.get_ylim()[1]])
    cbaxes = inset_axes(ax, width="30%", height="3%", loc=2) 
    cbar = fig.colorbar(plot, cax=cbaxes, orientation="horizontal")
    cbar.set_label('90s played')
    ax.hlines(y=stat2_mean, xmin=ax.get_xlim()[0], xmax=ax.get_xlim()[1], linestyle='dashed', colors='silver', linewidth=2)
    ax.vlines(x=stat1_mean, ymin=ax.get_ylim()[0], ymax=ax.get_ylim()[1], linestyle='dashed', colors='silver', linewidth=2)
    ax.text(ax.get_xlim()[0], stat2_mean, "Average", color="gray", rotation="horizontal")
    ax.text(stat1_mean, ax.get_ylim()[0]+0.5, "Average", color="gray", rotation="vertical")
    ann = []
    # font = {'font.family':'cursive'}
    for i, txt in enumerate(names):
        ann.append(ax.annotate(txt, (df2[stats[0]][i], df2[stats[1]][i]), clip_on=True))
    fig.tight_layout()
    mask = np.zeros(fig.canvas.get_width_height(), bool)

    fig.canvas.draw()

    for a in ann:
        bbox = a.get_window_extent()
        x0 = int(bbox.x0)
        x1 = int(math.ceil(bbox.x1))
        y0 = int(bbox.y0)
        y1 = int(math.ceil(bbox.y1))

        s = np.s_[x0:x1+1, y0:y1+1]
        if np.any(mask[s]):
            a.set_visible(False)
        else:
            mask[s] = True
    # ax.set_title('Ball progression by U23 midfielders and forwards (min. 8 nineties)')
    ax.set_title('u23 Midfielders and Forwards (min. 8 nineties)')
    # ax.set_xlabel('Progressive pass distance (in Yards)')
    # ax.set_ylabel('Progressive carry distance (in Yards)')
    ax.set_xlabel(' '.join(stats[0].split("_")))
    ax.set_ylabel(' '.join(stats[1].split("_")))
    # fname = 'plots/u23_sca'
    fname = 'plots/' + stats[0] + '_vs_' + stats[1]
    print("Storing plot to: {}".format(fname))
    plt.savefig(fname, bbox_inches="tight")