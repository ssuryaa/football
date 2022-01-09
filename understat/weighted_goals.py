#!/usr/bin/env python3

import asyncio
import json
import aiohttp
from understat import Understat

import matplotlib as mlp
mlp.use('Agg')
import matplotlib.pyplot as plt
import math
import numpy as np
from scipy.special import softmax

#playername = 'Robert Lewandowski'
#playername = 'Marcus Rashford'
#playername = 'Lionel Messi'

#teamname = 'Bayern Munich'
#teamname = 'Manchester United'
#teamname = 'Barcelona'

#leaguename = 'bundesliga'
#leaguename = 'epl'
#leaguename = 'la liga'

PRINT_TABLE = 0

class Vividict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value

async def get_playerid(playername, leaguename, teamname, season):
	async with aiohttp.ClientSession() as session:
		understat = Understat(session)
		player = await understat.get_league_players(leaguename, season, player_name=playername, team_title=teamname)
		return player[0]['id']


async def get_shots(playerid):
	async with aiohttp.ClientSession() as session:
		understat = Understat(session)
		player_shots = await understat.get_player_shots(playerid)
		return player_shots		

async def league_table(team_stats):
	async with aiohttp.ClientSession() as session:
		understat = Understat(session)
		table = await understat.get_league_table("EPL", "2019")
		table_header = table[0]
		table = table[1:] # removing header from the table
		for x in table:
			for y in range(1, len(x)):			
				team_stats[x[0]][table_header[y]] = x[y]
		
		return team_stats

def main():

	#playernames = ['Robert Lewandowski', 'Lionel Messi', 'Harry Kane', 'Mohamed Salah']
	#leaguenames = ['bundesliga','la liga', 'epl', 'epl']
	#teamnames = ['Bayern Munich', 'Barcelona', 'Tottenham', 'Liverpool']

	playernames = ['Mohamed Salah', 'Harry Kane']
	leaguenames = ['epl', 'epl']
	teamnames = ['Liverpool', 'Tottenham']
	season = 2019

	edgecolors = ['midnightblue', 'red', 'navy', 'gold']
	facecolors = ['crimson', 'mediumblue', 'ghostwhite', 'red']

	fig, ax = plt.subplots(2,2)	

	team_stats = Vividict()
	loop = asyncio.get_event_loop()
	team_stats = loop.run_until_complete(league_table(team_stats))
	
	if(PRINT_TABLE):
		for k, v in team_stats.items():
			print(k, v)
	
	ga = []
	for k, v in team_stats.items():
		ga.append(v['GA'])	
	print('GA: \n{}'.format(ga))
	ga_sum = sum(ga)
	weighted_ga = []
	for g in ga:
		weighted_ga.append(round(g/ga_sum, 4))
	print('Weighted GA: \n{}'.format(weighted_ga))
	
	exit()


	for x in range(len(playernames)):

		playerid = loop.run_until_complete(get_playerid(playernames[x], leaguenames[x], teamnames[x], season))
		print('Player: {} - id: {}'.format(playernames[x], playerid))
		player_shots = loop.run_until_complete(get_shots(playerid))		
		for shot in player_shots:
			if(shot['season'] == '2019' and shot['result'] == 'Goal'):
				if(shot['h_a'] == 'h'):
					print(shot['a_team'])
				else:
					print(shot['h_team'])
				
			
		
	
		exit()
		

if __name__ == '__main__':
	main()


# SHOT DICT KEYS
#['id', 'minute', 'result', 'X', 'Y', 'xG', 'player', 'h_a', 'player_id', 'situation', 'season', 'shotType', 
#'match_id', 'h_team', 'a_team', 'h_goals', 'a_goals', 'date', 'player_assisted', 'lastAction'])
