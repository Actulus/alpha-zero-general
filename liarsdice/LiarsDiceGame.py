from __future__ import print_function
import sys

sys.path.append("..")
from .LiarsDiceLogic import Board
from Game import Game
import numpy as np

"""
Game class implementation for the game of LiarsDice.

Author: Actulus, github.com/actulus
Date: Feb 23, 2024.
"""


class LiarsDiceGame(Game):
    """Class to represent the game of LiarsDice."""

    def __init__(self, n=5):
        """Initialize the game with the number of dice per player."""
        
        self.n = n  # Number of dice per player
        self.logic = Board(n)
        self.players = self.logic.players

    def getInitBoard(self):
        """Return initial board state."""

        return np.array([self.n, self.n])

    def getBoardSize(self):
        """Return the board size."""

        return 2 * self.n

    def getActionSize(self):
        """Returns the number of possible actions
        Example: bid 1-6 on dice value, plus a challenge action"""

        return 7

    def getNextState(self, board, player, action):
        """Apply the action to the board and return the next board state."""

        # Apply action to the game logic
        # print("action", action)
        self.logic.apply_action(
            self.logic.current_bid, action, player
        )

        # Calculate next player, there are only two players
        next_player = 1 - player # modify according to the number of players
        return (
            self.logic.get_board_state(),
            next_player,
        )  

    def getValidMoves(self, board, player):
        """Return a binary vector of valid moves for the current player."""

        return self.logic.get_valid_moves(current_bid=self.logic.current_bid)

    def getGameEnded(self, board, player):
        """Return 1 if the game is over and the current player wins, -1 if the game is over and the current player loses, 0 otherwise."""

        if self.logic.check_game_end():
            return 1 if self.logic.get_winner() == player else -1
        return 0  # Game not ended

    def getCanonicalForm(self, board, player):
        """Return the canonical form of the board. In this case, the canonical form is the board itself."""

        player_dice = self.logic.get_player_dice(player)
        
        return np.array(player_dice)

    def stringRepresentation(self, board):
        """Return a string representation of the board."""

        current_bid = self.logic.get_current_bid()
        return "Current bid: {} - Player 1 dice: {}, Player 2 dice: {}".format(current_bid, board[0], board[1])

    def getDiceSize(self):
        """Return the number of dice per player."""

        return self.n

    @staticmethod
    def display(board):
        """Print the current board state."""
        print(
            "Board state: Player 1 dice: {}, Player 2 dice: {}".format(
                board[0], board[1]
            )
        )
