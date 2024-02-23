import numpy as np

class HumanPlayer():
    """Class to represent a human player."""

    def __init__(self, game):
        """Initialize the human player with the game."""
        self.game = game

    def play(self, board):
        """Prompt the human player to make a move and return the action."""
        
        valid_moves = self.game.getValidMoves(board, 1)
        print("Enter your bid as 'quantity face_value' (e.g., '2 5') or enter '-1' to challenge the last bid.")
        while True:
            input_str = input()
            if input_str == '-1':
                action = self.game.getActionSize() - 1  # Assume last action is a challenge
            else:
                try:
                    quantity, face_value = map(int, input_str.split())
                    action = self.game.encodeAction(quantity, face_value)
                except ValueError:
                    print('Invalid input format. Please follow the format "quantity face_value" or "-1" for challenge.')
                    continue
            if 0 <= action < len(valid_moves) and valid_moves[action]:
                break
            else:
                print('Invalid move. Please try again.')
        return action


class RandomPlayer():
    """Class to represent a random player."""

    def __init__(self, game):
        """Initialize the random player with the game."""
        
        self.game = game

    def play(self, board):
        """Choose a random valid move and return the action."""

        valid_moves = self.game.getValidMoves(board, 1)
        valid_actions = [i for i, valid in enumerate(valid_moves) if valid]
        return np.random.choice(valid_actions)


class AIPlayer():
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
