#!/usr/bin/env python3

import argparse
import matplotlib as mlp
mlp.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from read_data2 import read_data
from get_player_names import get_player_names
from rank import get_pl_rank, get_club_rank
from percentile import calc_percentile
from glossary import get_glossary


def get_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--template', help = 'enter the input csv file to read')
	args = parser.parse_args()
	return args

def scatter_plot(attr1, attr2, stats):
	i = 0
	names = []
	stat1 = []
	stat2 = []	
	lim = 100
	for key, val in stats.items():
		if(float(stats[key]['90s']) > 10 and (stats[key]['Pos'] == 'DF' or stats[key]['Pos'] == 'DF')):
			names.append(key)
			stat1.append((float(stats[key][attr1])/float(stats[key]['90s'])))
			stat2.append((float(stats[key][attr2])/float(stats[key]['90s'])))
			i += 1
			if(i == lim):
				break
	
	stat1_mean = np.mean(np.asarray(stat1))
	stat2_mean = np.mean(np.asarray(stat2))
	stat1_std = np.std(np.asarray(stat1))
	stat2_std = np.std(np.asarray(stat2))
	stat1_one_std = stat1_mean + stat1_std 
	stat2_one_std = stat2_mean + stat2_std
	stat1_two_std = stat1_mean + stat1_std + stat1_std
	stat2_two_std = stat2_mean + stat2_std + stat2_std
	print('stat1. mean: {} | one std: {} | two std: {}' . format(stat1_mean, stat1_one_std, stat1_two_std))
	print('stat2. mean: {} | one std: {} | two std: {}' . format(stat2_mean, stat2_one_std, stat2_two_std))
	top_names = []
	first_quad = 0
	third_quad = 0
	for name in names:
		if((float(stats[name][attr1])/float(stats[name]['90s'])) > stat1_one_std and (float(stats[name][attr2])/float(stats[name]['90s'])) > stat2_one_std):
			top_names.append(name)
			first_quad += 1
			#print(stats[name][attr1], stats[name][attr2])
			#print(name)
			#exit()
		else:
			top_names.append('')
			third_quad += 1

	print('Num players in first quadrant: {}' . format(first_quad))
	print('Num players in third quadrant: {}' . format(third_quad))

	fig, ax = plt.subplots()	
	ax.scatter(stat1, stat2, edgecolors = 'black', color = 'red')
	for i,txt in enumerate(top_names):
		ax.annotate(txt, (stat1[i], stat2[i]))
	ax.axvline(x=stat1_mean, color = 'lightcoral', linestyle = '--')
	ax.axhline(y=stat2_mean, color = 'lightcoral', linestyle = '--')
	ax.set_xlabel(attr1)
	ax.set_ylabel(attr2)
	fig.savefig('scatter')
		

def main():
	args = get_arguments()
	if(args.template == 'standard'):
		inp_file = 'stats/std_stats.csv'
		#attr = {'Min', 'G+A', 'xG+xA', 'npxG+xA'}
		attr = {'G+A'}

	elif(args.template == 'passing'):
		inp_file = 'stats/passing_stats.csv'
		attr = {'PPA', 'CrsPA', '1/3', 'TB'}	 

	elif(args.template == 'shooting'):
		inp_file = 'stats/shooting_stats.csv'
		attr = {'Gls', 'Sh', 'SoT', 'G-xG'}	 

	elif(args.template == 'defensive'):
		inp_file = 'stats/defensive_actions.csv'
		attr = {'Pressures_Def 3rd', 'Tackles_Def 3rd', 'Vs Dribbles_Past', 'Pressures_Succ', 'Tackles_TklW'}

	stats = read_data(inp_file)
	print(stats)
	
	glossary = get_glossary()

	player = 'virgil_van_dijk'
	print('Player: {}' .format(player))

	'''
	print('player: {}' . format(player))
	for key, val in stats[player].items():
		print('{} --- {}' . format(key, val))
	exit()
	'''

	get_player_names(inp_file)
	calc_percentile(player, stats, attr)
	
	#attr1 = 'Pressures_Def 3rd'
	#attr2 = 'Tackles_Def 3rd'

	#attr1 = 'Pressures_Succ'
	#attr2 = 'Tackles_TklW'

	attr1 = '1/3'
	attr2 = 'TB'

	attr1_stats = get_pl_rank(attr1,stats)
	attr2_stats = get_pl_rank(attr2,stats)
	scatter_plot(attr1, attr2, stats)

if __name__ == '__main__':
    main()
