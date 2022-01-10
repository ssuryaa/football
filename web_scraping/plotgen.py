#!/usr/bin/env python3 

import scrape_fbref
from top_k import get_top_k
from scatter_metrics import plot_scatter

def calc_def_actions(database):
    database["Def_Actions"] = database["Tkl+Int"] + database["Blocks"] + database["Clr"]

def main():
    raw_data, database, percentiles = scrape_fbref.main()
    metrics = database.columns.values   
    database = database.rename({'90s':'nineties'}, axis=1) # renaming 90s -> nineties
    
    # get_top_k(raw_data, database, percentiles)
    calc_def_actions(database)
    # stats = ['SCA_PassLive', 'SCA_Drib']
    # stats = ['Def_Actions', 'Pressures']
    stats = ['Total_Pass_PrgDist', 'Carries_PrgDist']
    # stats = ['Pressures', 'Pressure_Success']
    plot_scatter(raw_data, database, percentiles, stats)
    

if __name__ == "__main__":
    main()