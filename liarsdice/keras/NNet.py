import os
import time
import numpy as np
import sys

sys.path.append("../..")
from utils import dotdict
from NeuralNet import NeuralNet
from tensorflow import keras  # noqa: F401
from keras.callbacks import ModelCheckpoint, LearningRateScheduler
from .LiarsDiceNNet import LiarsDiceNNet as ldnnet


args = dotdict(
    {
        "lr": 0.001,
        "dropout": 0.3,
        "epochs": 10,
        "batch_size": 64,
        "cuda": False,
        "hidden1": 512,
        "hidden2": 256,
        "num_channels": 1,
    }
)


class NNetWrapper(NeuralNet):
    """Class to represent the neural network wrapper."""

    def __init__(self, game):
        """Initialize the neural network with the game."""

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

        # learning rate schedule
        def sheduler(epoch, lr):
            if epoch < 5:
                return lr
            else:
                return lr * np.exp(-0.1)

        # model checkpoint
        checkpoint = ModelCheckpoint(
            "best_model.h5",
            monitor="val_loss",
            verbose=1,
            save_best_only=True,
            mode="min",
        )

        lr_scheduler = LearningRateScheduler(sheduler, verbose=1)

        self.nnet.model.fit(
            x=input_dice,
            y=[target_pis, target_vs],
            batch_size=args.batch_size,
            epochs=args.epochs,
            callbacks=[lr_scheduler, checkpoint],
            validation_split=0.1,
        )

    def predict(self, dice):
        """
        dice: np array with dice
        """

        # timing
        start = time.time()  # noqa: F841

        # preparing input
        dice = dice[np.newaxis, :]

        # run
        pi, v = self.nnet.model.predict(dice, verbose=False)

        # print('PREDICTION TIME TAKEN : {0:03f}'.format(time.time()-start))
        return pi[0], v[0]

    def save_checkpoint(self, folder="checkpoint", filename="checkpoint.pth.tar"):
        """Save the current model to file."""

        # change extension
        filename = filename.split(".")[0] + ".h5"
        filepath = os.path.join(folder, filename)
        if not os.path.exists(folder):
            print(
                "Checkpoint Directory does not exist! Making directory {}".format(
                    folder
                )
            )
            os.mkdir(folder)
        else:
            print("Checkpoint Directory exists! ")
        self.nnet.model.save_weights(filepath)
        # shutil.copyfile(filename, 'best.pth.tar')
        print("Model saved to file: ", filepath)

    def load_checkpoint(self, folder, filename):
        """Load the model from file."""

        filename = filename.split(".")[0] + ".h5"
        filepath = os.path.join(folder, filename)
        if os.path.exists(filepath):
            self.nnet.model.load_weights(filepath)
            print("Model loaded from file: ", filepath)
        else:
            print("No checkpoint found at: ", filepath)
