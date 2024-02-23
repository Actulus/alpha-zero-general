import argparse
import os
import shutil
import time
import random
import numpy as np
import math
import sys
sys.path.append('../..')
from utils import *
from NeuralNet import NeuralNet

import argparse

from .LiarsDiceNNet import LiarsDiceNNet as ldnnet

args = dotdict({
    'lr': 0.001,
    'dropout': 0.3,
    'epochs': 10,
    'batch_size': 64,
    'cuda': False,
    'hidden1': 512,
    'hidden2': 256,
})

class NNetWrapper(NeuralNet):
    def __init__(self, game):
        self.nnet = ldnnet(game, args)
        self.dice_size = game.getDiceSize()
        self.action_size = game.getActionSize()

    def train(self, examples):
        """
        examples: list of examples, each example is of form (board, pi, v)
        """
        input_dice, target_pis, target_vs = list(zip(*examples))
        input_dice = np.asarray(input_dice)
        target_pis = np.asarray(target_pis)
        target_vs = np.asarray(target_vs)
        self.nnet.model.fit(x = input_dice, y = [target_pis, target_vs], batch_size = args.batch_size, epochs = args.epochs)

    def predict(self, dice):
        """
        dice: np array with dice
        """
        # timing
        start = time.time()

        # preparing input
        dice = dice[np.newaxis, :]

        # run
        pi, v = self.nnet.model.predict(dice, verbose=False)

        #print('PREDICTION TIME TAKEN : {0:03f}'.format(time.time()-start))
        return pi[0], v[0]

    def save_checkpoint(self, folder='checkpoint', filename='checkpoint.pth.tar'):
        # change extension
        filename = filename.split(".")[0] + ".h5"
        filepath = os.path.join(folder, filename)
        if not os.path.exists(folder):
            print("Checkpoint Directory does not exist! Making directory {}".format(folder))
            os.mkdir(folder)
        else:
            print("Checkpoint Directory exists! ")
        self.nnet.model.save_weights(filepath)
        #shutil.copyfile(filename, 'best.pth.tar')
        print("Model saved to file: ", filepath)