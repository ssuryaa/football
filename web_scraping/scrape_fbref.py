#!/usr/bin/env python3

import numpy as np
import pandas as pd
pd.set_option('display.max_rows', None)
import os

class Vividict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value

def cleanup_data(table):
    # ******** removing "Player" rows ********
    for index, row in table.iterrows():
        if(row['Player'] == "Player"):
            table = table.drop(index=index)
    # print("Shape after removing 'Players': {}".format(table.shape))
    names = table['Player'].to_list()
    count = {}
    
    # ******** removing duplicates ********
    for x in range(len(names)):
        if(names[x] in count.keys()):
            count[names[x]] += 1
        else:
            count[names[x]] = 1
    duplicate_players = []
    for k,v in count.items():
        if(v > 1):
            duplicate_players.append(k)
    # print("Number of duplicate players = {}".format(len(duplicate_players)))
    for dupe in duplicate_players:
        dupe_index = table.index[table['Player'] == dupe].tolist()
        # for x in range(len(dupe_index)):
        if(table["90s"][dupe_index[0]] > table["90s"][dupe_index[1]]):
            table = table.drop(index=dupe_index[1])
        else:
            table = table.drop(index=dupe_index[0])   
    
    # ******** removing column "Matches" ********
    table = table.drop("Matches", 1)
    print("Shape after removing duplicates: {}".format(table.shape))
    
    return table

def get_passing_table():
    passing_table = pd.read_html("https://fbref.com/en/comps/Big5/passing/players/Big-5-European-Leagues-Stats#stats_passing")[0]
    print("\nScraped Passing. Shape: {}".format(passing_table.shape))
    new_col_header = []
    for col in passing_table.columns:
        if "Unnamed" in col[0]:
            new_col_header.append(col[1])
        else:
            new_col_header.append(col[0]+'_Pass_'+col[1])
    passing_table.columns = new_col_header

    return passing_table

def get_pass_type_table():
    pass_type_table = pd.read_html("https://fbref.com/en/comps/Big5/passing_types/players/Big-5-European-Leagues-Stats#stats_passing_types")[0]
    print("\nScraped Pass Types. Shape: {}".format(pass_type_table.shape))
    new_col_header = []
    for col in pass_type_table.columns:
        if "Unnamed" in col[0]:
            new_col_header.append(col[1])
        elif "Types" in col[0]:
            new_col_header.append(col[1] + '_Pass')
        elif "Corner" in col[0]:
            new_col_header.append('Corner_kicks' + '_' +col[1])
        elif "Height" in col[0]:
            new_col_header.append(col[0] + '_' +col[1])
        elif "Body" in col[0]:
            new_col_header.append('Body_Parts' + '_' +col[1])
        elif "Outcomes" in col[0]:
            new_col_header.append(col[0] + '_' +col[1])
    pass_type_table.columns = new_col_header
    
    return pass_type_table

def get_gsca_table():
    gsca_table = pd.read_html("https://fbref.com/en/comps/Big5/gca/players/Big-5-European-Leagues-Stats#stats_gca")[0]
    print("\nScraped GSCA. Shape: {}".format(gsca_table.shape))
    new_col_header = []
    for col in gsca_table.columns:
        if "Unnamed" in col[0]:
            new_col_header.append(col[1])
        elif col[0] == "SCA":
            new_col_header.append(col[1])
        elif col[0] == "SCA Types":
            new_col_header.append("SCA_"+col[1])
        elif col[0] == "GCA":
            new_col_header.append(col[1])
        elif col[0] == "GCA Types":
            new_col_header.append("GCA_"+col[1])
    gsca_table.columns = new_col_header

    return gsca_table

def get_def_actions_table():
    def_actions_table = pd.read_html("https://fbref.com/en/comps/Big5/defense/players/Big-5-European-Leagues-Stats#stats_defense")[0]
    print("\nScraped Defensive Actions. Shape: {}".format(def_actions_table.shape))
    new_col_header = []
    for col in def_actions_table.columns:
        if "Unnamed" in col[0]:
            new_col_header.append(col[1])
        elif col[0] == "Tackles":
            if col[1] == "Tkl":
                new_col_header.append("Tackles")
            elif col[1] == "TklW":
                new_col_header.append("Tackles_Won")
            else:
                new_col_header.append(col[0] + "_" + col[1])
        elif "Dribbles" in col[0]:
            new_col_header.append("Vs_Dribbles_" + col[1])
        elif col[0] == "Pressures":
            if col[1] == "Press":
                new_col_header.append("Pressures")
            elif col[1] == "Succ":
                new_col_header.append("Pressure_Success")
            elif col[1] == "%":
                new_col_header.append("Pressure_Success%")
            else:
                new_col_header.append(col[0] + "_" + col[1])
        elif col[0] == "Blocks":
            if col[1] == "Blocks":
                new_col_header.append("Blocks")
            else:
                new_col_header.append(col[0] + "_" + col[1])
    def_actions_table.columns = new_col_header

    return def_actions_table

def get_possession_table():
    possession_table = pd.read_html("https://fbref.com/en/comps/Big5/possession/players/Big-5-European-Leagues-Stats#stats_possession")[0]
    print("\nScraped Possession. Shape: {}".format(possession_table.shape))
    new_col_header = []
    for col in possession_table.columns:
        if "Unnamed" in col[0]:
            new_col_header.append(col[1])
        elif "Touches" in col[0]:
            if col[1] == "Touches":
                new_col_header.append(col[1])
            else:
                new_col_header.append(col[0] + '_' +col[1])    
        elif(col[0] == "Dribbles"):
            new_col_header.append(col[0] + '_' +col[1])
        elif(col[0] == "Carries"):
            if col[1] == "Carries":
                new_col_header.append(col[1])
            else:
                new_col_header.append(col[0] + '_' +col[1])    
        elif(col[0] == "Receiving"):
            new_col_header.append(col[0] + '_' +col[1])
    possession_table.columns = new_col_header
    return possession_table

def get_shooting_table():
    shooting_table = pd.read_html("https://fbref.com/en/comps/Big5/shooting/players/Big-5-European-Leagues-Stats#stats_shooting")[0]
    print("\nScraped Shooting. Shape: {}".format(shooting_table.shape))
    new_col_header = []
    for col in shooting_table.columns:
        new_col_header.append(col[1])
    shooting_table.columns = new_col_header
    return shooting_table

def combine_tables(combined_table, to_combine_table):
    new_metrics = []
    to_combine_metrics = to_combine_table.columns.values
    combined_metrics = combined_table.columns.values
    for x in range(len(to_combine_metrics)):
        if(to_combine_metrics[x] not in combined_metrics):
            new_metrics.append(to_combine_metrics[x])
    
    for x in new_metrics:
        combined_table[x] = to_combine_table[x]
        combined_table[x] = to_combine_table[x].values
    return combined_table

def scrape_data():
    passing_table = get_passing_table()
    passing_table = cleanup_data(passing_table)
    combined_table = passing_table
    print("Combined shape after Passing: {}".format(combined_table.shape))

    pass_type_table = get_pass_type_table()
    pass_type_table = cleanup_data(pass_type_table)
    combine_tables(combined_table, pass_type_table)
    print("Combined shape after pass type: {}".format(combined_table.shape))

    gsca_table = get_gsca_table()
    gsca_table = cleanup_data(gsca_table)
    combine_tables(combined_table, gsca_table)
    print("Combined shape after pass type: {}".format(combined_table.shape))

    def_actions_table = get_def_actions_table()
    def_actions_table = cleanup_data(def_actions_table)     
    combine_tables(combined_table, def_actions_table)
    print("Combined shape after def actions: {}".format(combined_table.shape))

    possession_table = get_possession_table()
    possession_table = cleanup_data(possession_table)
    combine_tables(combined_table, possession_table)
    print("Combined shape after Posession: {}".format(combined_table.shape))

    shooting_table = get_shooting_table()
    shooting_table = cleanup_data(shooting_table)
    combine_tables(combined_table, shooting_table)
    print("Combined shape after Shooting: {}".format(combined_table.shape))

    return combined_table

def convert_to_numeric(database):
    string_cols = ["Rk", "Player", "Nation", "Pos", "Squad", "Comp", "Age"]
    # database['Age'] = database['Age'].split()
    for col in database.columns.values:
        if col not in string_cols:
            database[col] = pd.to_numeric(database[col]) 

    return database

def divide_by_90(x, num_90s):
    return x/num_90s

def convert_to_p90(database):
    string_cols = ["Rk", "Player", "Nation", "Pos", "Squad", "Comp", "Age"]
    # for col in database.columns.values:
    # for col, row in database.items():
    for col in database.columns.values:
        if(col not in string_cols and "%"  not in col and "90s" not in col):
            # database[col] = database[col].apply(divide_by_90, args=(database["90s"],))
            database[col] = database[col].div(database["90s"])
    return database 

def main():
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
    # print(database.iloc[0])
    # print(percentiles.loc[percentiles.index[percentiles["Player"] == 'Thomas Partey']])
    # print(database.iloc[1834])
    percentiles = percentiles.set_index("Player")
    database = database.set_index("Player")
    raw_data = raw_data.set_index("Player")
    # print(metrics)
    # print(raw_data.loc["Mohamed Salah"]["Gls"])
    # print(database.loc["Mohamed Salah"]["Gls"])
    # print(percentiles.loc["Mohamed Salah"]["Gls"])

    top = raw_data.sort_values(by=['Gls'], ascending=False).head(5)
    print(top['Gls'])


if __name__ == "__main__":
    main()
    # TODO
    # standard stats 
    # misc stats 
    # goalkeeping stats 
    # advanced goalkeeping stats