# -*- coding: utf-8 -*-

import Reversi
from random import randint, choice

def RandomMove(b):
    return choice(list(b.legal_moves()))

def deroulementRandom(b):
    print("----------")
    print(b)
    if b.is_game_over():
        return
    move = RandomMove(b) 
    b.push(move)
    deroulementRandom(b)
    b.pop()

board = Reversi.Board(10)
deroulementRandom(board)

def heuristique(b, blanc):
    return b.heuristique()

def negaMax(b, blanc=True, horizon=10):

    if horizon == 0:
        return heuristique(b, blanc)

    if b.is_game_over():
        (nbwhite, nbblack) = b.get_nb_pieces()
        if nbwhite == nbblack:
            return 0
        elif nbwhite > nbblack:
            return 1000 if blanc else -1000
        else:
            return -1000 if blanc else 1000

    meilleur = None
    meilleurCoup = None
    for m in b.legal_moves():
        b.push(m)
        (nm, _) = -negaMax(b, not blanc, horizon - 1)
        if meilleur is None or nm > meilleur:
            meilleur = nm
            meilleurCoup = m
        b.pop()

    return (meilleur, meilleurCoup)

# Neg Alpha Beta avec version d'echec
def negAlphaBeta(b, alpha, beta, blanc=True, horizon=10):

    if horizon == 0:
        return heuristique(b, blanc)

    if b.is_game_over():
        (nbwhite, nbblack) = b.get_nb_pieces()
        if nbwhite == nbblack:
            return 0
        elif nbwhite > nbblack:
            return 1000 if blanc else -1000
        else:
            return -1000 if blanc else 1000

    meilleur = None
    meilleurCoup = None
    for m in b.legal_moves():
        b.push(m)
        (nm, _) = -negAlphaBeta(b, -beta, -alpha,
                            not blanc, horizon - 1)
        if meilleur is None or nm > meilleur:
            meilleur = nm
            meilleurCoup = m
            if meilleur > alpha:
                alpha = meilleur
                if alpha > beta: # Coupure
                    b.pop()
                    return (meilleur, meilleurCoup)
        b.pop()

    return (meilleur, meilleurCoup)

