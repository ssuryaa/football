#!/usr/bin/env python3

import asyncio
import json
import matplotlib as mlp
mlp.use('Agg')
import matplotlib.pyplot as plt
import math

import aiohttp

from understat import Understat

#playername = 'Robert Lewandowski'
#playername = 'Marcus Rashford'
#playername = 'Lionel Messi'

#teamname = 'Bayern Munich'
#teamname = 'Manchester United'
#teamname = 'Barcelona'

#leaguename = 'bundesliga'
#leaguename = 'epl'
#leaguename = 'la liga'

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
		print(table[0])
		for x in table:
			#team_stats[x[0]][x[]]
			print(x[0], x[7])

def plot(xg):
	plt.hist(xg, bins=10, edgecolor='black', facecolor='red')
	plt.title(playername)
	plt.ylabel('Number of shots')
	plt.xlabel('xG')
	plt.savefig('xg')

def main():

	#playernames = ['Robert Lewandowski', 'Lionel Messi', 'Harry Kane', 'Mohamed Salah']
	#leaguenames = ['bundesliga','la liga', 'epl', 'epl']
	#teamnames = ['Bayern Munich', 'Barcelona', 'Tottenham', 'Liverpool']

	playernames = ['Mohamed Salah']
	leaguenames = ['epl']
	teamnames = ['Liverpool']
	season = 2019

	edgecolors = ['midnightblue', 'red', 'navy', 'gold']
	facecolors = ['crimson', 'mediumblue', 'ghostwhite', 'red']

	fig, ax = plt.subplots(2,2)	

	team_stats = Vividict()
	loop = asyncio.get_event_loop()
	loop.run_until_complete(league_table(team_stats))
	
	for x in range(len(playernames)):
		playerid = loop.run_until_complete(get_playerid(playernames[x], leaguenames[x], teamnames[x], season))

		print('Player: {} - id: {}'.format(playernames[x], playerid))
		player_shots = loop.run_until_complete(get_shots(playerid))		

		xg = []
		for y in range(len(player_shots)):
			xg.append(float(player_shots[y]['xG']))
		xdim = math.floor(x/2)
		ydim = x%2
		a=ax[xdim,ydim].hist(xg, bins=50, edgecolor=edgecolors[x], facecolor=facecolors[x])
		#print(a)
		ax[xdim,ydim].set_title(playernames[x])
		ax[xdim,ydim].set_xlabel('xG')
		ax[xdim,ydim].set_ylabel('Number of shots')

		#exit()

	fig.tight_layout()
	fig.savefig('plot')	

if __name__ == '__main__':
	main()
