# LiarsDice implementation for Alpha Zero General

An implementation of a simple game provided to check extendability of the framework.

To train a model for LiarsDice, change the imports in ```main.py``` to:
```python
from Coach import Coach
from liarsdice.TicTacToeGame import TicTacToeGame
from liarsdice.keras.NNet import NNetWrapper as nn
from utils import *
```

Make similar changes to ```pit.py```.

To start training a model for TicTacToe:
```bash
python main.py
```
To start a tournament of 100 episodes with the model-based player against a random player:
```bash
python pit.py
```
You can play againt the model by switching to HumanPlayer in ```pit.py```

### Experiments
I trained a Keras model for ... (TODO: train model)
 ```pretrained_models/liarsdice/keras/```. You can play a game against it using ```pit.py```. 

### Contributors and Credits
* [Actulus](https://github.com/actulus)

The implementation is based on the game of Othello (https://github.com/suragnair/alpha-zero-general/tree/master/othello).


