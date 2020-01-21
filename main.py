#!/usr/bin/env python3

import argparse

from read_data import read_data
from get_player_names import get_player_names
from rank import get_pl_rank, get_club_rank
from percentile import calc_percentile
from glossary import get_glossary

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--csv_file', help = 'enter the csv file to read')
    args = parser.parse_args()
    return args

def main():
    args = get_arguments()
    std_stats = read_data(args.csv_file)
    #print('Number of players: {}' . format(len(std_stats.keys())))
    
    glossary = get_glossary()

    player = 'kevin_de_bruyne'
    
    '''
    print('player: {}' . format(player))
    for key, val in std_stats[player].items():
        print('{} --- {}' . format(key, val))
    '''

    get_player_names(args.csv_file)
    #get_pl_rank(std_stats)
    calc_percentile(player, std_stats)
    

if __name__ == '__main__':
    main()