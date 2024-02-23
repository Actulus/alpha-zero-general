from tensorflow import keras  # noqa: F401

from keras.models import Model
from keras.layers import Input, Dense, Flatten, Dropout
from keras.optimizers import Adam
import keras.regularizers as regularizers


class LiarsDiceNNet():
    """LiarsDiceNNet class"""

    def __init__(self, game, args):
        """Initialize the neural network with the game and arguments."""

        self.input_shape = (game.getBoardSize(),)  # Adjusted to represent full game state
        self.action_size = game.getActionSize()
        self.args = args

        self.input_layer = Input(shape=self.input_shape)
        x = Dense(128, activation='relu', kernel_regularizer=regularizers.l2(0.001))(self.input_layer)
        x = Dropout(0.3)(x)
        x = Dense(128, activation='relu', kernel_regularizer=regularizers.l2(0.001))(x)
        x = Dropout(0.3)(x)
        x = Flatten()(x)
        self.pi = Dense(self.action_size, activation='softmax', name='pi')(x)
        self.v = Dense(1, activation='tanh', name='v')(x)

        self.model = Model(inputs=self.input_layer, outputs=[self.pi, self.v])
        self.model.compile(loss=['categorical_crossentropy', 'mean_squared_error'],
                           optimizer=Adam(lr=args.lr))
