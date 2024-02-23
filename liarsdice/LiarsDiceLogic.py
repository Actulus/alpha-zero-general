"""
Board class implementation for the game of LiarsDice.
Default board has (2 players, 5 dice each).
Board data:
    0=1, 1=2, 2=3, 3=4, 4=5, 5=6
    first dim is player, 2nd is dice:
         pieces[0][0] is player 1's first die,
         pieces[1][4] is player 2's last die,
Author: Actulus, github.com/actulus
Date: Feb 23, 2024.
"""
import random


class Board:
    """Class to represent the game board."""

    def __init__(self, dice_per_player):
        """Initialize the board with the number of dice per player."""

        self.dice_per_player = dice_per_player
        
        # Initialize players' dice counts. This is a simple representation.
        self.player_dice = [dice_per_player, dice_per_player]

    def roll_dice(self):
        """Roll the dice for each player and store the values."""

        self.player_dice_values = {
            player: [random.randint(1, 6) for _ in range(dice_count)]
            for player, dice_count in enumerate(self.player_dice)
        }

    def reset_round(self):
        """Reset the round by rolling the dice for each player."""

        self.roll_dice()

    def make_bid(self, current_bid, new_bid):
        """Determine if the new bid is valid. A bid is valid if the new bid is greater than the current bid.
        If the bid value is the same, the bid quantity must be greater.
        """

        if new_bid[0] > current_bid[0] or (
            new_bid[0] == current_bid[0] and new_bid[1] > current_bid[1]
        ):
            return True  # The bid is valid
        return False  # The bid is not valid

    def challenge_bid(self, current_bid, player_dice_values):
        """Determine if the current bid is valid.
        A bid is valid if the total count of the bid value is greater than or equal to the bid quantity.
        """

        total_count = sum(
            value.count(current_bid[1]) for value in player_dice_values.values()
        )
        if total_count >= current_bid[0]:
            return "challenger loses"
        else:
            return "bidder loses"

    def remove_dice(self, player):
        """Remove a die from the specified player's hand."""
        self.player_dice[player] -= 1

    def check_game_end(self):
        """Return True if the game is over, False otherwise."""
        active_players = sum(1 for dice_count in self.player_dice if dice_count > 0)
        return active_players <= 1

    def get_winner(self):
        """Return the index of the winning player, or None if the game is not over."""

        for player, dice_count in enumerate(self.player_dice):
            if dice_count > 0:
                return player
        return None  # In case of an unexpected condition
