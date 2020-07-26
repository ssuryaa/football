#!/usr/bin/env python3

import csv
import argparse

class Vividict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value

def read_data(inp_file):
	stats = Vividict()

	with open(inp_file, 'r') as f:
		csv_obj = csv.reader(f)
		first_row = next(csv_obj) # next reads just the next row of the csv file pointed 
		second_row = next(csv_obj) # next reads just the next row of the csv file pointed 

		keys = []
		for x in range(len(first_row)):
			if(first_row[x] == ''):
				keys.append(second_row[x])
			else:
				keys.append(first_row[x] + '_' + second_row[x])


		#print('list of stats: {}\n' . format(keys))
		for row in csv_obj:
			name = row[1].split('\\')[0].replace(' ', '_')
			name = name.lower() # converting to all lower case
			name = name.replace('-', '_') # few players with middle names had - instead of _. this line takes care of it
			nationality = row[2].split(' ')[1] # name has a backslash and repeats once. this line deletes the unnecessary stuff
			stats[name][keys[2]] = nationality # like name, nationality also has unnecessary stuff. this line takes care of it
			for x in range(3, len(row)):
				stats[name][keys[x]] = row[x]           
	    
	return stats

# this is the dict format needed
# std_stats['lucas_torerira']['Pos'] 
# std_stats['lucas_torerira']['Starts'] 

            
        
