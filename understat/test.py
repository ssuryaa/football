#!/usr/bin/env python3

import asyncio
import json

import aiohttp

from understat import Understat

'''
async def get_players():
	async with aiohttp.ClientSession() as session:
		understat = Understat(session)
		player = await understat.get_league_players("epl", 2018, player_name="Marcus Rashford", team_title="Manchester United")
		#print(json.dumps(player))

loop = asyncio.get_event_loop()
loop.run_until_complete(get_players())
'''

async def get_shots():
	async with aiohttp.ClientSession() as session:
		understat = Understat(session)
		player_shots = await understat.get_player_shots(556)
		print(json.dumps(player_shots))

loop = asyncio.get_event_loop()
loop.run_until_complete(get_shots())
