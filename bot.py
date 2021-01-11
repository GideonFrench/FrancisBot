import discord
import random
from discord.ext import commands

client = discord.Client()

# These are variables for the tictactoe function
global gameOn, board, boardString, sList1, sList2
# Whether tha game is on or off
gameOn = True
# The original empty board
board = [['-','-','-'],['-','-','-'],['-','-','-']]
# The formatted string representing the board
boardString = f"```* | 1 | 2 | 3\n1 | {board[0][0]} | {board[0][1]} | {board[0][2]}\n2 | {board[1][0]} | {board[1][1]} | {board[1][2]}\n3 | {board[2][0]} | {board[2][1]} | {board[2][2]}```"
sList1 = ['000102', '101112', '202122', '001020', '011121', '021222', '001122', '021120']
sList2 = [0, 0, 0, 0, 0, 0, 0, 0]
sList3 = [0, 1, 2, 3, 4, 5, 6, 7]

# Prints when the bot is ready
@client.event
async def on_ready():
    print('Bot is ready.')

# On message events look for the contents of sent messages
@client.event
async def on_message(message):

    global gameOn, board, boardString

    # Don't read messages from bot (myself)
    if message.author == client.user:
        return

    # If the user types "!pingas" or "!Pingas", reply it back
    if message.content.startswith('!pingas') or message.content.startswith('!Pingas'):
        await message.channel.send('Pingas!')

    # Help function, hardcoded to when user says "!help" or "!Help"
    if message.content.startswith('!help') or message.content.startswith('!Help'):
        await message.channel.send("```new tictac: start a new game\nend tictac: end the current game\ntake x y: take the spot at the x column and y row if possible\nprint board: print the tictac board\n!pingas: say pingas!```")

    # To respond to all request to make a new emoji
    if 'emoji' and 'can' in message.content.lower():
        await message.channel.send("Beep Boop. Your request has been logged. Emoji imminent.")

    #-------------------
    # ~~~TIC TAC TOE~~~
    #-------------------

    # Declare a new tictac game, and wipe the board
    if message.content.startswith('new tictac'):
        gameOn = True
        createBoard()
        await message.channel.send(f"Game started!\n{boardString}")

    # End the tictac game
    if message.content.startswith('end tictac'):
        gameOn = False
        await message.channel.send("Game ended.")

    # Make a take. In the format "take x y"
    if message.content.startswith('take'):
        # If valid game is on...
        if gameOn == True:
            # TODO: Check if the formatting is correct on the function
            x = int(message.content[5])
            y = int(message.content[7])
            if x > 3 or x < 1:
                await message.channel.send("Invalid spot!")
            elif y > 3 or y < 1:
                await message.channel.send("Invalid spot!")
            else: 
                pMove = tictac(x, y)
                if (pMove == False):
                    await message.channel.send("Invalid move!")
                else:
                    setBoardString()
                    await message.channel.send(f"Player claims {x} {y}!\n{boardString}")
                    if checkWin('X'):
                        await message.channel.send("Player wins! Game over.")
                        gameOn = False
                    if gameOn == True:
                        updatePaths()
                        aimove = tactoe()
                        if aimove[0] == -1:
                            await message.channel.send("Player wins! Game over.")
                            gameOn = False
                        else:
                            updatePaths()
                            setBoardString()
                            await message.channel.send(f"Francis claims {aimove[1]+1} {aimove[0]+1}!\n{boardString}")
                            if checkWin('O'):
                                await message.channel.send("Francis wins! Game over.")
                                gameOn = False
        # If a game isn't on, tell the user to start one
        elif gameOn == False:
            await message.channel.send("Please start a game first.")

    # Utility function to print the board
    if message.content.startswith('print board'):
        await message.channel.send(f"{boardString}")

#------------------
# ~~~FUNCTIONS~~~
#------------------

# Create a new board
def createBoard():
    # Wipes the board
    global board, sList1, sList2
    board = [['-','-','-'],['-','-','-'],['-','-','-']]
    sList1 = ['000102', '101112', '202122', '001020', '011121', '021222', '001122', '021120']
    sList2 = [0, 0, 0, 0, 0, 0, 0, 0]
    sList3 = [0, 1, 2, 3, 4, 5, 6, 7]
    # Update the string
    setBoardString()

# Updates boardString
def setBoardString():
    # Updates the formatting of the boardString with new information
    global boardString
    boardString = f"```* | 1 | 2 | 3\n1 | {board[0][0]} | {board[0][1]} | {board[0][2]}\n2 | {board[1][0]} | {board[1][1]} | {board[1][2]}\n3 | {board[2][0]} | {board[2][1]} | {board[2][2]}```"

# Take spot (y, x), reversed for ease of use. Returns True if take is successful.
def tictac(x, y):
    global board
    # Invalid move, already occupied
    if (board[y-1][x-1] == 'X') or (board[y-1][x-1] == 'O'):
        return False
    # If not occupied, move there
    board[y-1][x-1] = 'X'
    return True

# AI move function
def tactoe():
    global board
    # Go to the middle if not occupied
    if board[1][1] == '-':
        board[1][1] = 'O'
        return [1, 1]
    # Else, pick a random unoccupied spot
    if len(sList3) == 0:
        while True:
            x = random.randint(0,2)
            z = random.randint(0,2)
            if board[x][z] == '-':
                board[x][z] = 'O'
                return [x, z]
                break
    lind = sList2.index(max(sList2))
    if sList2[lind] == -1:
        while True:
            x = random.randint(0,2)
            z = random.randint(0,2)
            if board[x][z] == '-':
                board[x][z] = 'O'
                return [x, z]
                break
    y = sList1[lind]
    if (board[int(y[0])][int(y[1])] == 'O' or board[int(y[0])][int(y[1])] == 'X'):
        if (board[int(y[2])][int(y[3])] == 'O' or board[int(y[2])][int(y[3])] == 'X'):
            if (board[int(y[4])][int(y[5])] == 'O' or board[int(y[4])][int(y[5])] == 'X'):
                return [-1, -1]
            else:
                board[int(y[4])][int(y[5])] = 'O'
                return [int(y[4]), int(y[5])]
        else:
            board[int(y[2])][int(y[3])] = 'O'
            return [int(y[2]), int(y[3])]
    else:
        board[int(y[0])][int(y[1])] = 'O'
        return [int(y[0]), int(y[1])]

# Check if path is still open. x is the player, "X" or "O", and y is the path, a string of 6 numbers xyxyxy for the coordinates
def checkPath(x, y):
    if ((board[int(y[0])][int(y[1])] == x or board[int(y[0])][int(y[1])] == "-") and (board[int(y[2])][int(y[3])] == x or board[int(y[2])][int(y[3])] == "-") and (board[int(y[4])][int(y[5])] == x or board[int(y[4])][int(y[5])] == "-")):
        counter = 0
        if (board[int(y[0])][int(y[1])] == x):
            counter += 1
            print(f"Yes! {int(y[0])} and {int(y[1])}")
        if (board[int(y[2])][int(y[3])] == x):
            counter += 1
            print(f"Yes! {int(y[2])} and {int(y[3])}")
        if (board[int(y[4])][int(y[5])] == x):
            counter += 1
            print(f"Yes! {int(y[4])} and {int(y[5])}")
        return counter
    else:
        return -1

def updatePaths():
    global sList1, sList2, sList3
    for x in sList3:
        y = checkPath("O", sList1[x])
        sList2[x] = y
        if (y == -1):
            sList3.remove(x)
    print (sList1)
    print(sList2)
    print(sList3)
    print("----------------")



# Check the win for the player x. "X" for user and "O" for bot
def checkWin(x):
    # All possible win combinations, return true if player has won
    if ((board[0][0] == x and board[0][1] == x and board[0][2] == x) or
    (board[1][0] == x and board[1][1] == x and board[1][2] == x) or
    (board[2][0] == x and board[2][1] == x and board[2][2] == x) or
    (board[0][0] == x and board[1][0] == x and board[2][0] == x) or
    (board[0][1] == x and board[1][1] == x and board[2][1] == x) or
    (board[0][2] == x and board[1][2] == x and board[2][2] == x) or
    (board[0][0] == x and board[1][1] == x and board[2][2] == x) or
    (board[0][2] == x and board[1][1] == x and board[2][0] == x)):
        return True
    else:
        return False

client.run('token')