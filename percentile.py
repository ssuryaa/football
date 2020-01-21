#!/usr/bin/env python3

from rank import rank_players

def calc_percentile(player, stats):
    attr = {'PPA', 'CrsPA', '1/3', 'TB'}
    print('---------------------------')
    print('Stat \t Rank \t Percentile')
    print('---------------------------')
    for attribute in attr:
        ranked, nineties_played = rank_players(stats, attribute)
        num_total_players = len(ranked.keys())
        
        nineties_threshold = 10 # the player should have played at least these many 90s 

        stat_per_ninety = {}
        for key, val in ranked.items():
            if(nineties_played[key] >= nineties_threshold):
                try:
                    stat_per_ninety[key] = round(ranked[key]/nineties_played[key], 2)
                except ZeroDivisionError:
                    stat_per_ninety[key] = 0   

        num_qualified_players = len(stat_per_ninety.keys())
        #print('Number of players qualified: {}' . format(num_qualified_players))
        stat_rank = num_qualified_players - list(stat_per_ninety.keys()).index(player)
        stat_percentile = round(100 - (stat_rank/num_qualified_players)*100)
        print('{} \t {} \t {}' . format(attribute, stat_rank, stat_percentile))