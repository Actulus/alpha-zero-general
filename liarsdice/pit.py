
import Arena
import sys
sys.path.append('..')



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

player1 = HumanPlayer(g).play
player2 = HumanPlayer(g).play

arena = Arena.Arena(player1, player2, g, display=Game.display)

print(arena.playGames(2, verbose=True))
