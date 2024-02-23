'''
Board class implementation for the game of LiarsDice.
Default board size is 1 row 5 columns (2 players, 5 dice each).
Board data:
    0=1, 1=2, 2=3, 3=4, 4=5, 5=6
    first dim is player, 2nd is dice:
         pieces[0][0] is player 1's first die,
         pieces[1][4] is player 2's last die,
Author: Actulus, github.com/actulus
Date: Feb 23, 2024.
'''
import math

class Board:
    def __init__(self, dice_per_player):
        self.dice_per_player = dice_per_player
        # Initialize players' dice counts. This is a simple representation.
        # A more complex implementation might track the specific values of each die.
        self.player_dice = [dice_per_player, dice_per_player]

    def roll_dice(self):
        # Simulate rolling the dice for each player at the beginning or when required
        # This function would randomly determine the dice values for each player
        
        # For simplicity, we'll just return a random value for each die
        values = math.random.randint(1, 7, self.dice_per_player)
        return values
    
    def make_bid(self, player, bid):
        # Process a player's bid
        # Bids would need to be validated against the current game state and previous bids
        
        bid_value, bid_count = bid
        return bid_value, bid_count



    def challenge_bid(self, challenger):
        # Process a challenge to the last bid
        # This would involve comparing the bid to the actual state of the dice
        # and determining the outcome of the challenge
        
        pass

    def remove_dice(self, player):
        # Remove a die from the player's count if they lose a challenge or bid
        self.player_dice[player] -= 1

    def is_game_over(self):
        # Check if the game is over (if any player has no dice left)
        return any(dice == 0 for dice in self.player_dice)

    def get_winner(self):
        # Determine the winner (the player with dice remaining)
        # In case of a draw (which shouldn't happen in Liars Dice), additional logic may be required
        
        if self.player_dice[0] > self.player_dice[1]:
            return 1
        elif self.player_dice[0] < self.player_dice[1]:
            return -1
        else:
            return 0
