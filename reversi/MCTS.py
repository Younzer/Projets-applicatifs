import copy
import sys
import math
from random import randint
import Reversi


class TreeNode(object):
    """A node in the MCTS tree"""

    def __init__(self, parent, board):
        self.parent = parent
        self.children = []  # a map from action to TreeNode
        self.N = 0
        self.Q = 0
        self.board = board

    def get_next_board_randomly(self):
        """All in the title"""
        legal_moves = self.board.legal_moves()
        move = legal_moves[randint(0, len(legal_moves) - 1)]
        new_board = copy.deepcopy(self.board)
        new_board.push(move)
        return new_board

    def expand(self):
        """Expand tree by creating new children"""
        board = self.get_next_board_randomly()
        new_node = TreeNode(self, board)
        self.children.append(new_node)
        return new_node

    def update(self, leaf_score):
        """Update node values from leaf evaluation"""
        # Count visit.
        self.N += 1
        # Update Q, a running average of values for all visits.
        self.Q += 1.0 * (leaf_score - self.Q) / self.N

    def update_recursive(self, leaf_score):
        """Like a call to update(), but applied recursively for all ancestors"""
        # If it is not root, this node's parent should be updated first.
        if self.parent:
            self.parent.update_recursive(-leaf_score)
        self.update(leaf_score)

    def get_score(self, c_param):
        """Calculate and return the value for this node"""
        return self.Q + c_param * math.sqrt(math.log(self.parent.N) / self.N) if self.N > 0 and self.parent.N > 0 else 0

    def is_leaf(self):
        """Check if leaf node (i.e. no nodes below this have been expanded)."""
        return self.children == []

    def is_root(self):
        return self.parent is None


class MCTS(object):
    """An implementation of Monte Carlo Tree Search."""

    def __init__(self, board, c_param=2, n_playout=8):
        """
        c_param: a number in (0, inf) that controls the trade-off 
        between exploitation and exploration in Monte Carlo Tree Search
        """
        self.board = board
        self.root = TreeNode(None, board)
        self.c_param = c_param
        self.n_playout = n_playout

    def select(self, root):
        """Return best successor node from root"""
        current = root
        while len(current.children) > 0:
            current = max(current.children, key=lambda child: child.get_score(self.c_param))
        return current

    def playout(self, node):
        """Run a single playout from the root to the leaf, getting a value at
        the leaf and propagating it back through its parents.
        State is modified in-place, so a copy must be provided.
        """
        while len(node.children) > 0:
            node = self.select(self.root)
        new_node = node.expand()
        copy_node = copy.deepcopy(new_node)
        while not copy_node.board.is_game_over():
            legal_moves = copy_node.board.legal_moves()
            move = legal_moves[randint(0, len(legal_moves) - 1)]
            copy_node.board.push(move)
        winner = copy_node.board.get_winner()
        if winner == -1:  # tie
            leaf_score = 0.0
        else:
            leaf_score = 1.0 if winner != copy_node.board._nextPlayer else -1.0
        # Update value and visit count of nodes in this traversal.
        assert self.n_playout < 9, 'Too much ressources'
        new_node.update_recursive(-leaf_score)

    def best_child(self, root, color):
        """Return the most visited child of a node"""
        best_score = sys.maxsize * -1
        best_node = None

        for node in root.children:
            score = node.N
            if score > best_score:
                best_score = score
                best_node = node
        move = best_node.board.pop()
        return move if move is not None else (color, -1, -1)

    def get_move(self, player, board):
        """Runs all playouts sequentially and returns the most visited action.
        state: the current game state
        Return: the selected action
        """
        root = TreeNode(None, self.board)
        for n in range(self.n_playout):
            self.playout(root)

        move = self.best_child(root, player)
        return move


class MCTSPlayer(object):
    """AI player based on MCTS"""

    def __init__(self, c_param=2, n_playout=8, board_size=8):
        self.board = Reversi.Board(board_size)
        self.mcts = MCTS(self.board, c_param, n_playout)
        self.player = None

    def getPlayerMove(self):
        if self.board.is_game_over():
            print("Referee told me to play but the game is over!")
            return (-1, -1)
        move = self.mcts.get_move(self.player, self.board)
        (p, x, y) = move
        print(move)
        self.board.push(move)
        assert (p == self.player)
        return (x, y)

    def playOpponentMove(self, x, y):
        #print('move ', x, y)
        #print(self.board)
        assert (self.board.is_valid_move(self.opponent, x, y))
        #print("Opponent played ", (x, y))
        self.board.push([self.opponent, x, y])

    def newGame(self, color):
        self.player = color
        self.opponent = 1 if color == 2 else 2

    def endGame(self, winner):
        if self.player == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")

    def getPlayerName(self):
        return "MCTS {}".format(self.player)
