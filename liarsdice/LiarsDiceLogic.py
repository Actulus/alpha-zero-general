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

class BasePlayer:
    """Class to represent a base player."""
    id = 0
    hand = []
    dice_count = 0
    current_bid = (0, 0)

    def __init__(self):
        """Initialize the player."""
        self.dice_count = 5
        self.rollDices()

    def rollDices(self):
        """Roll the dice for the player and store the values."""
        self.hand = [random.randint(1, 6) for _ in range(self.dice_count)]
        return self.hand
    
    def loose_die(self):
        """Remove a die from the player's hand."""
        self.dice_count -= 1
        self.hand.pop()
        return self.hand
    
    def get_my_dices(self):
        """Return the player's hand."""
        return self.hand
       
class Bid:
    dice_count = 0 
    dice_value = 0

    def __init__(self, dice_count, dice_value):
        self.dice_count = dice_count
        self.dice_value = dice_value

    def __str__(self):
        return f"{self.dice_count} {self.dice_value}"
    
    def to_tuple(self):
        return (self.dice_count, self.dice_value)
    
    def checkIfValidBid(self, current_bid):
        if self.dice_count > current_bid.dice_count:
            return True
        elif self.dice_count == current_bid.dice_count and self.dice_value > current_bid.dice_value:
            return True
        else:
            return False
        
    def checkIfValidChallenge(self, current_bid, player_dice_values):
        total_count = sum(
            value.count(current_bid.dice_value) for value in player_dice_values.values()
        )
        if total_count >= current_bid.dice_count:
            return "challenger loses"
        else:
            return "bidder loses"

        

class Board:
    """Class to represent the game board."""
    player_number = 2
    players = []
    dice_per_player = 5
    players_dice_values = []
    current_bid = Bid(0, 0)
    current_player = BasePlayer()
    players_order = []

    def __init__(self):
        """Initialize the board with players. Roll dice for each player."""
        self.players = [BasePlayer(self), BasePlayer(self)]
        self.roll_dice()

        for player in self.players:
            player.id = self.players.index(player)
            player.hand = self.players_dice_values[player]
            player.dice_count = self.dice_per_player
            player.current_bid = Bid(0, 0)

        self.current_bid = Bid(0, 0)
        self.players_order = self.players
        random.shuffle(self.players_order)

        self.current_player = self.players_order[0]
        

    def roll_dice(self):
        """Roll the dice for each player and store the values."""

        for player in self.players:
            player.hand = [random.randint(1, 6) for _ in range(player.dice_count)]
            self.players_dice_values.append(player.hand)

        return self.players_dice_values

    def reset_round(self):
        """Reset the round by rolling the dice for each player."""

        self.roll_dice()

    def make_bid(self, current_player):
        """ Get the current_players bid, since each player has a different logic for making a bid. 
        Then check if the bid is valid, if not, ask for a new bid. If it is valid, update the current_bid and return True."""
        
        new_bid = current_player.bid()
        while not self.checkIfValidBid(new_bid):
            print("Invalid bid. Please try again.")
            new_bid = current_player.bid()
        self.current_bid = new_bid
        return True

    def check_if_valid_bid(self, new_bid):
        """Determine if the new bid is valid. 
        First determine if the values given are valid, if they are numbers and within the correct range.
        Then check if the new bid is greater than the current bid. If it is, return True, else return False.
        """

        # check if the new_bid is a tuple
        if not isinstance(new_bid, tuple):
            return False
        # check if the new_bid's dice_count is a number and within the correct range, from 0 to the sum of all dices in the game
        if not isinstance(new_bid[0], int) or new_bid[0] < 0 or new_bid[0] > sum(self.players_dice_values):
            return False
        # check if the face value is a number and within the correct range, from 1 to 6
        if not isinstance(new_bid[1], int) or new_bid[1] < 1 or new_bid[1] > 6:
            return False
        # check if the new_bid is greater than the current_bid
        if new_bid[0] > self.current_bid[0] or (new_bid[0] == self.current_bid[0] and new_bid[1] > self.current_bid[1]):
            return True
        return False
        

    def check_if_valid_challenge(self):
        """Determine if the current bid is valid.
        A bid is valid if the dice_count is greater than the current bid's dice_count, or if the dice_count is the same and the dice_value is greater.
        """

        # check if there are enough dice with the current value to challenge the bid
        total_dices_count = sum([player.dice_count for player in self.players])
        if self.current_bid.dice_count > total_dices_count:
            return False
        
        # check if there are enough dices with the current value to challenge the bid
        total_count = sum(
            value.count(self.current_bid.dice_value) for value in self.players_dice_values
        )
        if total_count >= self.current_bid.dice_count:
            return True
        return False

    def remove_dice(self, player):
        """Remove a die from the specified player's hand."""
        player.loose_die()

    def get_board_state(self):
        """Return the current board state."""

        return self.players_dice_values, self.current_bid, self.current_player

    def get_player_dice(self, player):
        """Return the dice values for the specified player."""

        print(player.get_my_dices())


    def get_current_bid(self):
        """Return the current bid."""

        return self.current_bid
    
    def get_current_player(self):
        """Return the current player."""

        return self.current_player
