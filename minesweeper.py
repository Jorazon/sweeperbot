import math
import random
from datetime import datetime
import copy
import jsonIO

#discord server id for additional emojis
serverid="503840746005200916"

#emoji translations
emojicode={
	"0":["\U00000030\U000020e3",0,0,[""]],
	"1":["\U00000031\U000020e3",0,0,[""]],
	"2":["\U00000032\U000020e3",0,1,[""]],
	"3":["\U00000033\U000020e3",0,2,[""]],
	"4":["\U00000034\U000020e3",0,3,[""]],
	"5":["\U00000035\U000020e3",0,4,[""]],
	"6":["\U00000036\U000020e3",0,5,[""]],
	"7":["\U00000037\U000020e3",0,6,[""]],
	"8":["\U00000038\U000020e3",0,7,[""]],
	"9":["\U00000039\U000020e3",0,8,[""]],
	"10":["\U0001f51f",0,9,[""]],

	"a":["\U0001f1e6",1,0,[""]],
	"b":["\U0001f1e7",1,1,[""]],
	"c":["\U0001f1e8",1,2,[""]],
	"d":["\U0001f1e9",1,3,[""]],
	"e":["\U0001f1ea",1,4,[""]],
	"f":["\U0001f1eb",1,5,[""]],
	"g":["\U0001f1ec",1,6,[""]],
	"h":["\U0001f1ed",1,7,[""]],
	"i":["\U0001f1ee",1,8,[""]],
	"j":["\U0001f1ef",1,9,[""]],

	"l":["\U0001f1f1",1,11,[""]],
	"n":["\U0001f1f3",1,13,[""]],
	"o":["\U0001f1f4",1,14,[""]],
	"q":["\U0001f1f6",1,16,[""]],
	"s":["\U0001f1f8",1,18,[""]],
	"w":["\U0001f1fc",1,22,[""]],

	"flag":["\U0001f6a9",3,0,[""]],
	"click":["\U00002196",3,0,[""]],
	"pop":["\U0001f389",3,0,[""]],
	"trash":["\U0001f5d1",3,0,[""]],
	"check":["\U00002705",3,0,[""]],
	"turtle":["\U0001F422",3,0,[""]],
	"pig":["\U0001F437",3,0,[""]]
}

#load active games
activeGames = jsonIO.read("activeGames.json")

#game board min and max side length
gridMin = 5
gridMax = 10

#emoji codes for game board
bombEmoji = ["\U00002734\U0000FE0F","\U0001F4A3","\U0001F4A5"]
numbersEmoji = ["\U00002b1c","\U00002b1b",emojicode["1"][0],emojicode["2"][0],emojicode["3"][0],emojicode["4"][0],emojicode["5"][0],emojicode["6"][0],emojicode["7"][0],emojicode["8"][0],emojicode["9"][0],emojicode["10"][0]]
lettersEmoji = [":octagonal_sign:",emojicode["a"][0],emojicode["b"][0],emojicode["c"][0],emojicode["d"][0],emojicode["e"][0],emojicode["f"][0],emojicode["g"][0],emojicode["h"][0],emojicode["i"][0],emojicode["j"][0]]

#emoji codes for row letters reactions
baseRow = [
emojicode["a"][0],emojicode["b"][0],emojicode["c"][0],emojicode["d"][0],emojicode["e"][0],emojicode["f"][0],emojicode["g"][0],
emojicode["h"][0],emojicode["i"][0],emojicode["j"][0]]

#emoji codes for column numbers reactions
baseCol = [
emojicode["1"][0],emojicode["2"][0],emojicode["3"][0],emojicode["4"][0],emojicode["5"][0],
emojicode["6"][0],emojicode["7"][0],emojicode["8"][0],emojicode["9"][0],emojicode["10"][0]]

#emoji codes for user input reactions
decisionAct = [emojicode["click"][0],emojicode["flag"][0],emojicode["check"][0],emojicode["turtle"][0],emojicode["trash"][0]]

#emoji codes for win and lose reactions
decisionLose = [emojicode["l"][0],emojicode["o"][0],emojicode["s"][0],emojicode["e"][0],emojicode["trash"][0]]
decisionWin = [emojicode["w"][0],emojicode["i"][0],emojicode["n"][0],emojicode["pop"][0],emojicode["trash"][0]]

#generate game
def genNewGame(message_id,row_id,col_id,act_id,size):
	#cells are saved as in activegames [flag,open,bomb,neighbors]
	try:
		gridSize = int(size)
		gridSize = min(gridMax, max(gridSize, gridMin))
	except:
		gridSize = gridMin#random.randint(gridMin, gridMax)
	bombcount = math.floor(gridSize*math.log(gridSize,7))
	newGameGrid = []
	for x in range(gridSize):
		newGameGrid.append([])
		for y in range(gridSize):
			newGameGrid[x].append([False,False,False,0])
	bombs = []
	while (len(bombs) < bombcount):
		newBomb = [random.randint(0,gridSize-1),random.randint(0,gridSize-1)]
		if ((newBomb in bombs) == False):
			bombs.append(newBomb)
	for b in bombs:
		newGameGrid[b[0]][b[1]][2] = True
	for y in range(gridSize):
		for x in range(gridSize):
			neighborCount = 0
			neighbors = getNeighbors(x,y,gridSize)
			for n in neighbors:
				if (newGameGrid[n[0]][n[1]][2] == True): neighborCount += 1
			newGameGrid[x][y][3] = neighborCount
			if (newGameGrid[x][y][2] == True):
				newGameGrid[x][y][3] = -1
	#refresh active games
	activeGames = jsonIO.read("activeGames.json")
	#add new hame to active games
	newGame = {
		"type":"minesweeper",
		"time":datetime.now().isoformat("-"),
		"nextSpace":[-1,-1,"none",0],
		"grid":newGameGrid,
		"gridSize":gridSize,
		"bombcount":bombcount,
		"comments":[row_id,col_id,act_id]
	}
	activeGames[message_id] = newGame
	jsonIO.rawWrite(activeGames,"activeGames.json")

	gameReacts = jsonIO.read("gameReacts.json")
	gameReacts[row_id] = message_id
	gameReacts[col_id] = message_id
	gameReacts[act_id] = message_id
	jsonIO.rawWrite(gameReacts,"gameReacts.json")

	decisionRow = []
	decisionCol = []
	for x in range(gridSize):
		decisionRow.append(baseRow[x])
		decisionCol.append(baseCol[x])
	gridMsg = str(gridToMsg(newGameGrid,gridSize,bombcount))

	return [gridMsg, decisionRow, decisionCol, decisionAct]

#handle user reactions
def onReact(emoji_name,message_id):
	package = ["hmm"]
	activeGames = jsonIO.read("activeGames.json")
	gameReacts = jsonIO.read("gameReacts.json")
	game = activeGames[message_id]
	gridSize = game["gridSize"]
	bombcount = game["bombcount"]

	for e in emojicode:
		if (emoji_name == emojicode[e][0] or emoji_name == emojicode[e][3][0]):
			game["nextSpace"][emojicode[e][1]] = emojicode[e][2]

	#delete game
	if (emoji_name == emojicode["trash"][0]):
		for i in game["comments"]:
			gameReacts.pop(i, None)
		activeGames.pop(message_id, None)
		package = ["delete",[message_id, game["comments"][0], game["comments"][1], game["comments"][2]]]
		return package

	#check win condition
	if (checkWin(game,gridSize,bombcount)):
		#uncomment to show board on win
		#for y in range(gridSize):
		#	for x in range(gridSize):
		#		game["grid"][x][y][1]=True
		package = ["react", gridToMsg(game["grid"],gridSize,bombcount), decisionWin, [game["comments"][0], game["comments"][1], game["comments"][2]]]
		return package

	#action select
	elif (emoji_name == emojicode["click"][0]):
		game["nextSpace"][2] = "open"
	elif (emoji_name == emojicode["flag"][0]):
		game["nextSpace"][2] = "flag"

	#action confirmed
	elif (emoji_name == emojicode["check"][0] and game["nextSpace"][0] != -1 and game["nextSpace"][1] != -1 and game["nextSpace"][2] != "none"):
		if (game["nextSpace"][2] == "flag"):
			if (game["grid"][game["nextSpace"][0]][game["nextSpace"][1]][0] == True):
				game["grid"][game["nextSpace"][0]][game["nextSpace"][1]][0] = False
			elif (game["grid"][game["nextSpace"][0]][game["nextSpace"][1]][1] == False):
				game["grid"][game["nextSpace"][0]][game["nextSpace"][1]][0] = True

			package = ["edit", gridToMsg(game["grid"],gridSize,bombcount)]

		elif (game["nextSpace"][2] == "open"):
			if (game["grid"][game["nextSpace"][0]][game["nextSpace"][1]][0] == False and game["grid"][game["nextSpace"][0]][game["nextSpace"][1]][2] == True):
				#uncomment to show board on lose
				for y in range(gridSize):
					for x in range(gridSize):
						game["grid"][x][y][1]=True
				package = ["react", gridToMsg(game["grid"],gridSize,bombcount), decisionLose, [game["comments"][0], game["comments"][1], game["comments"][2]]]

			elif (game["grid"][game["nextSpace"][0]][game["nextSpace"][1]][0] == False):
				game["grid"][game["nextSpace"][0]][game["nextSpace"][1]][1] = True
				gridOpen(game["grid"],game["nextSpace"][0],game["nextSpace"][1],gridSize)
				package = ["edit", gridToMsg(game["grid"],gridSize,bombcount)]

			else:
				package = ["edit", gridToMsg(game["grid"],gridSize,bombcount)]
		game["nextSpace"][0] = -1
		game["nextSpace"][1] = -1
		game["nextSpace"][2] = "none"
	elif (emoji_name == emojicode["check"][0]):
		package = ["edit", gridToMsg(game["grid"],gridSize,bombcount)]
	jsonIO.rawWrite(activeGames, "activeGames.json")
	jsonIO.rawWrite(gameReacts,"gameReacts.json")
	return package

def checkWin(game,gridSize,bombcount):
	flagbomb=0
	opennotbomb=0

	for y in range(gridSize):
		for x in range(gridSize):
			if (game["grid"][x][y][0] == True):
				if (game["grid"][x][y][2] == True): flagbomb+=1
				else: flagbomb-=1
			elif (game["grid"][x][y][1] == True):
				if (game["grid"][x][y][2] == False): opennotbomb+=1
				else: opennotbomb-=1

	return (flagbomb == bombcount or opennotbomb == gridSize*gridSize-bombcount)

#convert grid data to message
def gridToMsg(grid,gridSize,bombcount):
	msg = ""
	for y in range(gridSize+1):
		for x in range(gridSize+1):
			if (y==0): msg += numbersEmoji[1+x]
			elif (y!=0):
				if (x==0): msg += lettersEmoji[y]
				else:
					if (grid[x-1][y-1][0] == True): msg += "\U0001F6A9"
					elif (grid[x-1][y-1][1] == True):
						if (grid[x-1][y-1][2] == True): msg += bombEmoji[2]
						elif (grid[x-1][y-1][3] == 0): msg += numbersEmoji[1]
						else: msg += numbersEmoji[1+grid[x-1][y-1][3]]
					else: msg += numbersEmoji[0]
			if (x==gridSize): msg += "\n"
		if (y==gridSize): msg += "There are "+str(bombcount)+" bombs."
	return str(msg)

#opening selected grid cell
def gridOpen(grid,x,y,gridSize):
	neighbors = getNeighbors(x,y,gridSize)
	for n in neighbors:
		if (grid[x][y][3] == 0 and grid[n[0]][n[1]][1] == False):
			grid[n[0]][n[1]][1] = True
			gridOpen(grid,n[0],n[1],gridSize)
		elif (grid[n[0]][n[1]][3] == 0 and grid[n[0]][n[1]][1] == False):
			grid[n[0]][n[1]][1] = True
			gridOpen(grid,n[0],n[1],gridSize)

#get neighboring cells
def getNeighbors(x,y,gridSize):
	nei=[]
	if (x==0 and y==0):
		nei=[[x+1,y],[x,y+1],[x+1,y+1]]
	elif (x==gridSize-1 and y==0):
		nei=[[x-1,y],[x,y+1],[x-1,y+1]]
	elif (x==0 and y==gridSize-1):
		nei=[[x+1,y],[x,y-1],[x+1,y-1]]
	elif (x==gridSize-1 and y==gridSize-1):
		nei=[[x-1,y],[x,y-1],[x-1,y-1]]
	elif (x==0):
		nei=[[x,y-1],[x,y+1],[x+1,y-1],[x+1,y],[x+1,y+1]]
	elif (x==gridSize-1):
		nei=[[x,y-1],[x,y+1],[x-1,y-1],[x-1,y],[x-1,y+1]]
	elif (y==0):
		nei=[[x-1,y],[x+1,y],[x-1,y+1],[x,y+1],[x+1,y+1]]
	elif (y==gridSize-1):
		nei=[[x-1,y],[x+1,y],[x-1,y-1],[x,y-1],[x+1,y-1]]
	else:
		nei=[[x-1,y-1],[x,y-1],[x+1,y-1],[x-1,y],[x+1,y],[x-1,y+1],[x,y+1],[x+1,y+1]]
	return nei