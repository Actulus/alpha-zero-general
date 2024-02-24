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
        self.player_dice_values = {0: [], 1: []}
        self.current_bid = (0, 0)

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

        # print("current_bid", current_bid)
        # print("new_bid", new_bid)

        if new_bid[0] > current_bid[0] or (
            new_bid[0] == current_bid[0] and new_bid[1] > current_bid[1]
        ):
            return True  # The bid is valid
        return False  # The bid is not valid

    def challenge_bid(self, current_bid):
        """Determine if the current bid is valid.
        A bid is valid if the total count of the bid value is greater than or equal to the bid quantity.
        """

        total_count = sum(
            value.count(current_bid[1]) for value in self.player_dice_values.values()
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

    def get_board_state(self):
        """Return the current board state."""

        return self.player_dice_values

    def get_valid_moves(self, current_bid):
        """Return a list of valid moves for the current player."""

        valid_moves = [0] * 7
        for i in range(1, 7):
            # print(current_bid)
            if self.make_bid(current_bid, (current_bid[0] + 1, i)):
                valid_moves[i] = 1
        valid_moves[0] = self.challenge_bid(current_bid)
        return valid_moves

    def decode_action_to_bid(self, action):
        """Decode the action to a bid."""

        if action == 0:
            return -1
        return (action, (action - 1) % 6 + 1)

    def apply_action(self, current_bid, action, player):
        """Apply the specified action to the current game state."""

        if action == -1:
            # Challenge
            result = self.challenge_bid(self.current_bid)
            if result == "challenger loses":
                self.remove_dice(player)
            else:
                self.remove_dice(3 - player)
        else:
            bid = self.decode_action_to_bid(action)
            is_valid = self.make_bid(self.current_bid, bid)
            if is_valid:
                self.current_bid = action
            else:
                raise ValueError("Invalid bid")

    def get_player_dice(self, player):
        """Return the dice values for the specified player."""

        return self.player_dice_values[player]

    def get_current_bid(self):
        """Return the current bid."""

        return self.current_bid
