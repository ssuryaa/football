#!/usr/bin/env python3 

import numpy as np
import pandas as pd 
import os 
import math
import matplotlib as mpl
import matplotlib.pyplot as plt 
plt.rcParams["font.family"] = "Latin Modern Roman"
# plt.rcParams["font.weight"] = "bold"
# plt.rcParams["axes.labelweight"] = "bold"
plt.rcParams["font.size"] = 12
plt.rcParams["figure.figsize"] = (10,6)
plt.rcParams['figure.dpi'] = 140
from matplotlib.pyplot import figure 
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
# figure(figsize=(400, 300), dpi=200)

from scrape_fbref import scrape_data, convert_to_numeric, convert_to_p90

def get_data():
    if os.path.isfile("database" and "raw_data"):
        print("Database exists")
        raw_data = pd.read_pickle("raw_data")
        database = pd.read_pickle("database")
    else:
        print("\n ***** Creating database ***** ")
        database = scrape_data()
        raw_data = convert_to_numeric(database)
        raw_data.to_pickle("raw_data")
        database = convert_to_numeric(database) 
        database = convert_to_p90(database)
        database.to_pickle("database")
    return raw_data, database

def get_percentiles(database):
    print("Calculating percentiles")
    string_cols = ["Rk", "Player", "Nation", "Pos", "Squad", "Comp", "Age"]
    metrics = database.columns.values
    percent = []
    for m in metrics:
        if m not in string_cols:
            percent.append(database[m].rank(pct=True))
        else:
            percent.append(database[m])
    percentiles = pd.DataFrame(percent)
    percentiles = percentiles.transpose()
    return percentiles

def get_top_k(raw_data, database, percentiles):
    top = database['Age'].str.split('-')
    age_yr = []
    for x in range(len(top)):
        if isinstance(top[x], list):
            age_yr.append(top[x][0])
        else:
            age_yr.append(0)
    print(database.shape)
    database['Age'] = age_yr
    database = database[database.Age != 0]
    print(database.shape)
    database['Age'] = pd.to_numeric(database['Age'])

    # print(raw_data.sort_values(by=['SCA_Drib'], ascending=False)['SCA_Drib'][:5])
    stats = ['Total_Pass_PrgDist', 'Carries_PrgDist']
    print("\nMean 90s: {:2.2f} \t Median 90s: {:2.2f}\n".format(database['nineties'].mean(), database['nineties'].median()))
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
    plot = ax.scatter(df2[stats[0]], df2[stats[1]], s=100, c=df2['nineties'], cmap='cool')
    ax.set_xlim([0,350])
    cbaxes = inset_axes(ax, width="30%", height="3%", loc=1) 
    cbar = fig.colorbar(plot, cax=cbaxes, orientation="horizontal")
    cbar.set_label('90s played')
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
    ax.set_title('Ball progression by U23 midfielders and forwards (min. 8 nineties)')
    ax.set_xlabel('Progressive pass distance (in Yards)')
    ax.set_ylabel('Progressive carry distance (in Yards)')
    plt.savefig('test', bbox_inches="tight")

def main():
    raw_data, database = get_data()
    percentiles = get_percentiles(database)
    metrics = database.columns.values
    percentiles = percentiles.set_index("Player")
    database = database.set_index("Player")
    raw_data = raw_data.set_index("Player")
   
    database = database.rename({'90s':'nineties'}, axis=1) # renaming 90s -> nineties
    get_top_k(raw_data, database, percentiles)

if __name__ == "__main__":
    # import matplotlib.font_manager
    # flist = mpl.font_manager.get_fontconfig_fonts()
    # names = [mpl.font_manager.FontProperties(fname=fname).get_name() for fname in flist]
    # print(names)
    # exit()
    main()