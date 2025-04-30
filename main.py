from game_class import Game
import time

game=Game()
game.Initialize()

while game.mIsRunning:
    game.Loop()