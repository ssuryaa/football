#!/usr/bin/env python3

from collections import Counter

def get_pl_rank(stats):
    attr = 'long_Cmp%' # through ball
    temp_dict = {}
    nineties_played = {}
    for key, value in stats.items():
        print(stats[key][attr])
        print('float: {}' . format(float(stats[key][attr])))
        #temp_dict[key] = float(stats[key][attr])
        #nineties_played[key] = float(stats[key]['90s'])
    
    exit()
    a = ({k: v for k, v in sorted(temp_dict.items(), key=lambda item: item[1])})

    top_n = 10
    nineties_threshold = 10 # the player should have played at least 5 90s 

    kp_ninety = {}
    for key, val in a.items():
        if(nineties_played[key] >= nineties_threshold):
            try:
                kp_ninety[key] = round(a[key]/nineties_played[key], 2)
            except ZeroDivisionError:
                kp_ninety[key] = 0

    k = Counter(kp_ninety)
    high = k.most_common(top_n)

    print('{} p90 (more than {} 90s played):' . format(attr, nineties_threshold))
    for x in high:
        print(x)


def get_club_rank(stats):
    pass