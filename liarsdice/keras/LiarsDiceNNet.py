import sys
sys.path.append('..')
from tensorflow.keras.models import *
from tensorflow.keras.layers import *
from tensorflow.keras.optimizers import *

class LiarsDiceNNet():
    def __init__(self, game, args):
        self.dice_size = game.getDiceSize()  # Assuming getDiceSize is a method that returns the size of the dice array
        self.action_size = game.getActionSize()
        self.args = args

        # Neural Net
        self.input_dice = Input(shape=(self.dice_size,))  # Input layer for dice state

        x = Reshape((self.dice_size, 1))(self.input_dice)  # Reshape for dense layer input
        x = Dense(args.hidden1, activation='relu')(x)
        x = Dropout(args.dropout)(x)
        x = Dense(args.hidden2, activation='relu')(x)
        x = Dropout(args.dropout)(x)
        x = Flatten()(x)
        self.pi = Dense(self.action_size, activation='softmax', name='pi')(x)  # Output layer for action probabilities
        self.v = Dense(1, activation='tanh', name='v')(x)  # Output layer for state value estimation

        self.model = Model(inputs=self.input_dice, outputs=[self.pi, self.v])
        self.model.compile(loss=['categorical_crossentropy','mean_squared_error'], optimizer=Adam(args.lr))
