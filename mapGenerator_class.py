from mazeGenerator_class import MazeGenerator
import random


class MapGenerator:
    def __init__(self):
        pass

    def generate_map(width, height, enemyNum=5):
        game_map = MazeGenerator.instance().creat_map(width, height)
        #print(game_map)

        for y in range(len(game_map)):
            for x in range(len(game_map[0])):
                if game_map[y][x]:
                    game_map[y][x] = '#'
                else:
                    game_map[y][x] = '.'
        #Add Enemies
        for i in range(enemyNum):
            px=random.randint(0, width-1)
            py=random.randint(0, height-1)
            game_map[px][py]='@'
            
        #Add Player
        while True:
            px=random.randint(0, width-1)
            py=random.randint(0, height-1)
            if game_map[px][py]=='.':
                game_map[px][py]='$'
                break

        return game_map