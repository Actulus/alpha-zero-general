import numpy as np

class BasePlayer:
    """Base class to represent a player."""
    id: int
    hand: list
    current_bid: tuple
    dice_count: int

    def __init__(self, game):
        """Initialize the player with the game."""
        self.game = game       

    def play(self, board):
        """Choose a move and return the action."""
        action = self.choose_action()
        current_bid = board.current_bid
        while True:
            if action == 'b':
                self.bid(board, current_bid)
            elif action == 'c':
                if current_bid == (0, 0):
                    print("You can't challenge if there is no bid. Please try again!")
                    return
                else:
                    self.challenge(board, current_bid)
            else:
                print("Invalid action. Please try again.")
                continue
        return


    def choose_action(self):
        """Choose an action and return the action."""
        print("Choose an action: 'b' for bid, 'c' for challenge.")
        while True:
            action = input()
            if action == 'b' or action == 'c':
                return action
            else:
                print('Invalid action. Please try again.')
                continue

    def bid(self):
        """Choose a bid and return the action. Different for each player type."""
        pass

    def challenge(self, board):
        """Choose whether to challenge the current bid and return the action."""
        print("You've challenged the last bid: ", board.current_bid)
        board.check_if_valid_challenge()
        
    
    def loose_die(self):
        """Remove a die from the player's hand."""
        self.hand.pop()
        return
    
    def get_my_dices(self):
        """Return the player's hand."""
        return self.hand
        

class HumanPlayer(BasePlayer):
    """Class to represent a human player derived from the BasePlayer."""

    def __init__(self, game):
        """Initialize the human player with the game."""
        super().__init__(game)

    def play(self, board):
        """Choose a move and return the action."""
        action = self.choose_action(board)
        current_bid = board.current_bid
        while True:
            if action == 'b':
                bid = self.bid(board, current_bid)
                board.makeBid(bid)
            elif action == 'c':
                if current_bid == (0, 0):
                    print("You can't challenge if there is no bid. Please try again!")
                    return
                else:
                    self.challenge(board, current_bid)
            elif action == 'q':
                print("You've quit the game.")
                exit()
            else:
                print("Invalid action. Please try again.")
                continue
        return

    def choose_action(self, board):
        """Choose an action and return the action."""
        print("Choose an action: 'b' for bid, 'c' for challenge, 'q' to quit.")
        while True:
            action = input()
            if action == 'b' or action == 'c' or action == 'q':
                return action
            else:
                print('Invalid action. Please try again.')
                continue

    def bid(self):
        """Choose a bid and return the action. Bid validation is done in the Board class."""

        print("Make your bid as 'quantity face_value' (e.g., '2 5').")
        
        while True:
            try:
                bid = input()
                bid = bid.split()
                bid = (int(bid[0]), int(bid[1]))
                self.current_bid = bid
                return bid
                              
            except ValueError:
                print('Invalid input format. Please follow the format "quantity face_value".')
                continue
                
    def printDices(self):
        """Print the player's hand."""
        print("You have ", self.dice_count, " dices left.")
        print("Your hand: ", self.hand)
        return


class RandomPlayer(BasePlayer):
    """Class to represent a random bid generator NPC player."""
    
    def __init__(self, game):
        """Initialize the random player with the game."""
        super().__init__(game)

    def play(self, board):
        """Choose a bid and return the action."""
        a = np.random.randint(self.game.getActionSize())
        valids = self.game.getValidMoves(board, 1)
        while valids[a]!=1:
            a = np.random.randint(self.game.getActionSize())
        return a

class AIPlayer(BasePlayer):
    """Class to represent an AI player."""

    def __init__(self, game, nnet):
        """Initialize the AI player with the game and neural network."""

        self.game = game
        self.nnet = nnet

    def play(self, board):
        """Choose the best move according to the neural network and return the action."""
        
        valid_moves = self.game.getValidMoves(board, 1)
        action_probabilities = self.nnet.predict(board)
        valid_probs = np.zeros(action_probabilities.shape)
        valid_probs[valid_moves] = action_probabilities[valid_moves]  # Mask valid moves
        if np.sum(valid_probs) > 0:  # Check if there are any valid moves recommended by the nnet
            return np.argmax(valid_probs)
        else:  # Fallback strategy
            print("Fallback to random move.")
            return np.random.choice(np.flatnonzero(valid_moves))
