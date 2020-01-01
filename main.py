#!/usr/bin/env python3

import argparse

from read_data import read_data

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--csv_file', help = 'enter the csv file to read')
    args = parser.parse_args()
    return args

def main():
    args = get_arguments()
    std_stats = read_data(args.csv_file)
    print('Number of players: {}' . format(len(std_stats.keys())))

    player_name = 'Mattéo_Guendouzi'
    print('player: {}' . format(player_name))
    for key, val in std_stats[player_name].items():
        print('{} --- {}' . format(key, val))

if __name__ == '__main__':
    main()