from __future__ import print_function
import sys
sys.path.append('..')
from .LiarsDiceLogic import Board
from Game import Game
import numpy as np

"""
Game class implementation for the game of LiarsDice.

Author: Actulus, github.com/actulus
Date: Feb 23, 2024.
"""
class LiarsDiceGame(Game):
    def __init__(self, n=2):
        self.n = n  # Number of dice per player, example setting

    def getInitBoard(self):
        # Initializes board with n dice per player
        return np.array([self.n, self.n])

    def getBoardSize(self):
        # Returns the size of the board (2, for two players)
        return (2,)

    def getActionSize(self):
        # Returns the number of possible actions
        # Example: bid 1-6 on dice value, plus a challenge action
        return 7

    def getNextState(self, board, player, action):
        # For simplicity, this example just alternates the player
        # In a full implementation, you would update the board based on the action
        nextPlayer = -player
        return (board, nextPlayer)

    def getValidMoves(self, board, player):
        # Returns a fixed array of valid moves
        # In a full implementation, this would depend on the game state
        return [1] * self.getActionSize()

    def getGameEnded(self, board, player):
        # Simplified check for game end condition
        # Normally, you'd check if a challenge has been made and resolved
        return 0  # 0 for ongoing, 1 for win, -1 for lose

    def getCanonicalForm(self, board, player):
        # For Liar's Dice, the canonical form could include the player's perspective of dice
        return board * player

    def stringRepresentation(self, board):
        # Simple string representation
        return board.tostring()

    @staticmethod
    def display(board):
        print("Board state: Player 1 dice: {}, Player 2 dice: {}".format(board[0], board[1]))
