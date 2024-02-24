import sys
sys.path.append('..')
import Arena


from liarsdice.LiarsDiceGame import LiarsDiceGame as Game

from liarsdice.LiarsDicePlayers import HumanPlayer

"""
use this script to play any two agents against each other, or play manually with
any agent.
"""

mini_othello = False  # Play in 6x6 instead of the normal 8x8.
human_vs_cpu = False
human_vs_human = True


g = Game(5)
hp = HumanPlayer(g).play

n1p = hp
player2 = hp

arena = Arena.Arena(n1p, player2, g, display=Game.display)
print("hi")
print(arena.playGames(2, verbose=True))
