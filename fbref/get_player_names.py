#!/usr/bin/env python3

import csv

def get_player_names(inp_file):
    name_list = []
    with open(inp_file, 'r') as f:
        csv_obj = csv.reader(f)
        next(csv_obj)
        for row in csv_obj:     
            name_list.append((row[1].split('\\')[0].replace(' ', '_').replace('-', '_')).lower())

    op_file = 'player_names.txt'
    with open(op_file, 'w') as f:
        #csv_obj = csv.writer(f)
        for name in name_list:
            f.write('\n {}' . format(name))