#!/usr/bin/env python3

from collections import Counter

def rank_players(stats_dir, attr):
	temp_dict = {}
	nineties_played = {}
	for key, value in stats_dir.items():
		#print(stats_dir[key][attr], attr, key)
		temp_dict[key] = float(stats_dir[key][attr])
		nineties_played[key] = float(stats_dir[key]['90s'])

	a = ({k: v for k, v in sorted(temp_dict.items(), key=lambda item: item[1])})

	return a, nineties_played

def get_pl_rank(attr, stats):
    
	a, nineties_played = rank_players(stats, attr)
	top_n = 10
	nineties_threshold = 10 # the player should have played at least these many 90s 

	kp_ninety = {}
	for key, val in a.items():
		if(nineties_played[key] >= nineties_threshold):
			try:
				kp_ninety[key] = round(a[key]/nineties_played[key], 2)
			except ZeroDivisionError:
				kp_ninety[key] = 0

		k = Counter(kp_ninety)
		high = k.most_common(top_n)

	#'''
	print('------------------')
	print('{} p90 (more than {} 90s played):' . format(attr, nineties_threshold))
	for x in high:
		print(x)
	#'''

def get_club_rank(stats):
    pass
