import discord
from discord.utils import get
import os
import sys
import asyncio
import pathlib
import pickle
import json
from datetime import datetime

import jsonIO
import minesweeper

client = discord.Client()
emojiList = discord.Server.emojis

options = jsonIO.read("options.json")

@client.event
async def on_ready():
	print('----------------------')
	print('Logged in as: ' + client.user.name)
	print('ID: ' + client.user.id)
	print('----------------------')

#code for reading messages
@client.event
async def on_message(message):

	if message.author.bot:
		return

	prefix = options["servers"]["default"]

	if message.content.startswith(prefix + 'sweep'):
		game = await client.send_message(message.channel, "Generating game :arrows_counterclockwise:")
		row = await client.send_message(message.channel, "Row selection")
		col = await client.send_message(message.channel, "Column selection")
		act = await client.send_message(message.channel, "Action selection")
		try:
			size = message.content.split(" ")[1]
		except:
			size = "5"
		mine = minesweeper.genNewGame(game.id,row.id,col.id,act.id,size)
		await client.edit_message(game, new_content=mine[0])
		patient = await client.send_message(message.channel, "Please wait for all the reactions to arrive :turtle:")

		temparr = [[1,row],[2,col],[3,act]]
		for y in range(len(temparr)):
			for x in mine[temparr[y][0]]:
				if (type(x) is list):
					await client.add_reaction(temparr[y][1], discord.Emoji(name=x[0],id=x[1],server=x[2]))
				else:
					await client.add_reaction(temparr[y][1], x)

		await client.delete_message(patient)
		#delete starting command
		#await client.delete_message(message)

#code for reading reaction clicks
@client.event
async def on_socket_raw_receive(payload):
	if (type(payload) is str):
		jsonload = json.loads(payload)
		if (jsonload["t"]=="MESSAGE_REACTION_ADD" and jsonload["d"]["user_id"]!=client.user.id):
			activeGames = jsonIO.read("activeGames.json")
			gameReacts = jsonIO.read("gameReacts.json")
			msgID = (str(jsonload["d"]["message_id"]))
			origMsg = (str(jsonload["d"]["message_id"]))
			if (msgID in gameReacts):
				msgID = gameReacts[msgID]
			if (msgID in activeGames):
				if (activeGames[msgID]["type"]=="minesweeper"):
					await gameTypeMinesweeper(jsonload, activeGames, msgID, origMsg)

async def gameTypeMinesweeper(jsonload, activeGames, msgID, origMsg):
	action = minesweeper.onReact(jsonload["d"]["emoji"]["name"],msgID)
	chanID = client.get_channel(jsonload["d"]["channel_id"])
	msgGame = await client.get_message(chanID,msgID)
	selfMember = client.get_server(jsonload["d"]["guild_id"]).get_member(client.user.id)

	if (action[0]=="delete"):
		for x in action[1]:
			try: await client.delete_message(await client.get_message(chanID,x))
			except: None
	elif (action[0]=="edit"):
		for m in activeGames[msgID]["comments"]:
			msg = await client.get_message(chanID,m)
			await client.edit_message(msgGame, new_content=action[1])
			for react in msg.reactions:
				if (react.count>1):
					for member in await client.get_reaction_users(react,limit=40,after=None):
						if (member != selfMember):
							await client.remove_reaction(msg,react.emoji,member)

	elif (action[0]=="react"):
		await client.edit_message(msgGame, new_content=action[1])
		await client.clear_reactions(msgGame)
		for m in action[3]:
			try: await client.delete_message(await client.get_message(chanID,m))
			except: None
		for x in action[2]:
			await client.add_reaction(msgGame, x)

client.run(options["token"])