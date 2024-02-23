import numpy as np

class HumanPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        valid = self.game.getValidMoves(board, 1)
        for i in range(len(valid)):
            if valid[i]:
                print(int(i/self.game.n), int(i%self.game.n))
        while True:
            a = input('Enter your bid or challenge: ')
            x, y = [int(x) for x in a.split(' ')]
            a = self.game.n * x + y if x != -1 else self.game.getActionSize() - 1
            if valid[a]:
                break
            else:
                print('Invalid Move')
        return a

class RandomPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        a = np.random.randint(self.game.getActionSize())
        valid = self.game.getValidMoves(board, 1)
        while not valid[a]:
            a = np.random.randint(self.game.getActionSize())
        return a

class AIPlayer():
    def __init__(self, game, nnet):
        self.game = game
        self.nnet = nnet

    def play(self, board):
        valid = self.game.getValidMoves(board, 1)
        action_probabilities = self.nnet.predict(board)
        best_move = np.argmax(action_probabilities)
        while not valid[best_move]:
            action_probabilities[best_move] = 0
            best_move = np.argmax(action_probabilities)
        return best_move
