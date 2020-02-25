from MCTS import *
from localGame import run_local_game
import matplotlib.pyplot as plt
import numpy as np

NUM_PARTY = 10
_BLACK = 1 # Black
_WHITE = 2 # White


def random_vs_uct():
   
    victory_rdm = []
    victory_uct = []
    for n in range(NUM_PARTY):
        winner, nb_white, nb_black, time = run_local_game()
        if winner == _BLACK:
            victory_rdm.append([True, nb_black, time[0]])
            victory_uct.append([False, nb_white, time[1]])
        elif winner == _WHITE:
            victory_rdm.append([False, nb_black, time[0]])
            victory_uct.append([True, nb_white, time[1]])
        else:
            print('Deuce')
    plt.figure(1)
    plt.bar([0,1], [np.sum([victory_rdm[i][0] for i in range(len(victory_rdm))]),
                    np.sum([victory_uct[i][0] for i in range(len(victory_uct))])],
                    color='r')
    plt.xticks([0, 1], ('Random moves', 'MCTS'))
    plt.title('Number of games won')
    plt.show()

    plt.figure(2)
    plt.plot([victory_rdm[i][1] for i in range(len(victory_rdm))], label='Black (random) pieces')
    plt.plot([victory_uct[i][1] for i in range(len(victory_uct))], label='White (MCTS) pieces')
    plt.title('Number of pieces per party for each method')
    plt.show()

    plt.figure(3)
    plt.plot([victory_rdm[i][2] for i in range(len(victory_rdm))], label='Time to play random method')
    plt.plot([victory_uct[i][2] for i in range(len(victory_uct))], label='Time to play UCT Search method')
    plt.title('Move time per method per party')
    plt.show()

def utc_vs_uct():
   
    victory_uct1 = []
    victory_uct2 = []
    for n in range(NUM_PARTY):
        winner, nb_white, nb_black, time = run_local_game(vs = "MCTS")
        if winner == _BLACK:
            victory_uct1.append([True, nb_black, time[0]])
            victory_uct2.append([False, nb_white, time[1]])
        elif winner == _WHITE:
            victory_uct1.append([False, nb_black, time[0]])
            victory_uct2.append([True, nb_white, time[1]])
        else:
            print('Deuce')
    plt.figure(1)
    plt.bar([0,1], [np.sum([victory_uct1[i][0] for i in range(len(victory_uct1))]),
                    np.sum([victory_uct2[i][0] for i in range(len(victory_uct2))])],
                    color='r')
    plt.xticks([0, 1], ('Black', 'White'))
    plt.title('Number of games won (MCTS vs MCTS)')
    plt.show()

    plt.figure(2)
    plt.plot([victory_uct1[i][1] for i in range(len(victory_uct1))], label='Black pieces')
    plt.plot([victory_uct2[i][1] for i in range(len(victory_uct2))], label='White pieces')
    plt.title('Number of pieces per party')
    plt.show()

    plt.figure(3)
    plt.plot([victory_uct1[i][2] for i in range(len(victory_uct1))], label='Time to play Black')
    plt.plot([victory_uct2[i][2] for i in range(len(victory_uct2))], label='Time to play White')
    plt.title('Move time per party')
    plt.show()


if __name__ == '__main__':
    random_vs_uct()
    #utc_vs_uct()