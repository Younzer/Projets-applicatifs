import copy
import sys
import numpy as np
import math
from random import randint
import Reversi

class TreeNode(object):
    """A node in the MCTS tree"""
    def __init__(self, parent, board):
        self._parent = parent
        self._children = []  # a map from action to TreeNode
        self._N = 0
        self._Q = 0
        self._board = board

    def get_next_board_randomly(self):
        """All in the title"""
        legal_moves = self._board.legal_moves()
        move =  legal_moves[randint(0,len(legal_moves)-1)]
        new_board = copy.deepcopy(self._board)  
        new_board.push(move)
        return new_board

    def expand(self):
        """Expand tree by creating new children"""
        board = self.get_next_board_randomly()
        new_node = TreeNode(self,board)
        self._children.append(new_node)
        return new_node

    def select(self, root, exploration_rate):
        """Return best successor of node"""
        aux = root
        while len(aux._children)>0:
            best_node = None
            best_score = sys.maxsize*-1
            for node in aux._children:
                score = node.get_score(exploration_rate)
                if score>best_score:
                    best_score = score
                    best_node = node
            rand = np.random.rand(1)[0]
            if rand>0.8:
                aux = aux.expand()
            else:
                aux = best_node
    
        return aux

    def update(self, leaf_score):
        """Update node values from leaf evaluation"""
        # Count visit.
        self._N += 1
        # Update Q, a running average of values for all visits.
        self._Q += 1.0*(leaf_score - self._Q) / self._N

    def update_recursive(self, leaf_score):
        """Like a call to update(), but applied recursively for all ancestors"""
        # If it is not root, this node's parent should be updated first.
        if self._parent:
            self._parent.update_recursive(-leaf_score)
        self.update(leaf_score)

    def get_score(self, c_param):
        """Calculate and return the value for this node"""
        return self._Q + c_param*math.sqrt(math.log(self._parent._N)/self._N) if self._N != 0 else self._Q

    def is_leaf(self):
        """Check if leaf node (i.e. no nodes below this have been expanded)."""
        return self._children == []

    def is_root(self):
        return self._parent is None


class MCTS(object):
    """An implementation of Monte Carlo Tree Search."""

    def __init__(self, board, c_param=0.3, n_playout=80):
        """
        c_param: a number in (0, inf) that controls the trade-off 
        between exploitation and exploration in Monte Carlo Tree Search
        """
        #self._board = board
        self._root = TreeNode(None, board)
        self._c_param = c_param
        self._n_playout = n_playout

    def _playout(self, state):
        """Run a single playout from the root to the leaf, getting a value at
        the leaf and propagating it back through its parents.
        State is modified in-place, so a copy must be provided.
        """
        node = self._root
        while(1):
            if node.is_leaf():
                break
            node = node.select(self._root, self._c_param)

        if not node._board.is_game_over():
            node.expand()
        while not node._board.is_game_over():
            node._board = node.get_next_board_randomly()
        winner = state.get_winner()

        if winner == -1:  # tie
            leaf_score = 0.0
        else:
            leaf_score = 1.0 if winner != state._nextPlayer else -1.0

        # Update value and visit count of nodes in this traversal.
        node.update_recursive(-leaf_score)

    def get_move(self, state):
        """Runs all playouts sequentially and returns the most visited action.
        state: the current game state
        Return: the selected action
        """
        for n in range(self._n_playout):
            state_copy = copy.deepcopy(state)
            self._playout(state_copy)

        move = best_child(root,color)
        return move


class MCTSPlayer(object):
    """AI player based on MCTS"""
    def __init__(self, c_param=0.3, n_playout=80, board_size=10):
        self._board = Reversi.Board(board_size)
        self._mcts = MCTS(self._board, c_param, n_playout)
        self._player = None
    
    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return (-1,-1)
        move = self._mcts.get_move(self._board)
        print('move : ',move)
        (p,x,y) = move
        print(move)
        self._board.push(move)
        assert(p==self._player)
        return (x,y) 

    def playOpponentMove(self, x,y):
        print('move ',x,y)
        print(self._board)
        assert(self._board.is_valid_move(self._opponent, x, y))
        print("Opponent played ", (x,y))
        self._board.push([self._opponent, x, y])

    def newGame(self, color):
        self._player = color
        self._opponent = 1 if color == 2 else 2

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")

    def __str__(self):
        return "MCTS {}".format(self.player)    