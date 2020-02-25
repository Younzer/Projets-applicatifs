import Reversi
from MCTS import *
import time
from io import StringIO
import sys

def run_local_game(vs = 'random', board_size = 8):

    b = Reversi.Board(board_size)

    players = []
    if vs == "random":
        player1 = myPlayer()
    if vs == "MCTS":
        player1 = MCTSPlayer()
    player1.newGame(b._BLACK)
    players.append(player1)
    player2 = MCTSPlayer()
    player2.newGame(b._WHITE)
    players.append(player2)

    totalTime = [0, 0] # total real time for each player
    nextplayer = 0
    nextplayercolor = b._BLACK
    nbmoves = 1

    outputs = ["",""]
    sysstdout= sys.stdout
    stringio = StringIO()
    print(b)
    while not b.is_game_over():
        nbmoves += 1
        otherplayer = (nextplayer + 1) % 2
        othercolor = b._BLACK if nextplayercolor == b._WHITE else b._WHITE
        
        currentTime = time.time()
        sys.stdout = stringio
        move = players[nextplayer].getPlayerMove()
        sys.stdout = sysstdout
        playeroutput = "\r" + stringio.getvalue()
        stringio.truncate(0)
        print(("[Player "+str(nextplayer) + "] ").join(playeroutput.splitlines(True)))
        outputs[nextplayer] += playeroutput
        totalTime[nextplayer] += time.time() - currentTime
        print("Player ", nextplayercolor, players[nextplayer].getPlayerName(), "plays" + str(move))
        (x,y) = move 
        if not b.is_valid_move(nextplayercolor,x,y):
            print(otherplayer, nextplayer, nextplayercolor)
            print("Problem: illegal move")
            break
        b.push([nextplayercolor, x, y])
        players[otherplayer].playOpponentMove(x,y)

        nextplayer = otherplayer
        nextplayercolor = othercolor

        print(b)

    print("The game is over")
    print(b)
    (nbwhites, nbblacks) = b.get_nb_pieces()
    winner = b.get_winner()
    print("Time:", totalTime)
    print("Winner: ", end="")
    if nbwhites > nbblacks:
        print("WHITE")
    elif nbblacks > nbwhites:
        print("BLACK")
    else:
        print("DEUCE")

    player2.endGame(winner)

    return winner, nbwhites, nbblacks, totalTime

if __name__ == '__main__':
    run_local_game()


