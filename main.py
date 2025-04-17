from game_class import Game

game=Game()
game.Initialize()
while game.mIsRunning:
    game.Loop()