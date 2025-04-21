import random


class MapGenerator:
    def __init__(self):
        pass

    # 随机生成地图
    def generate_map(width, height, enemyNum=5, obstacle_probability=0.3):
        # 初始化一个空地图
        game_map = [[' ' for _ in range(width)] for _ in range(height)]
        
        for y in range(height):
            for x in range(width):
                # 随机决定是否放置障碍物
                if random.random() < obstacle_probability:
                    game_map[y][x] = '#'
                else:
                    game_map[y][x] = '.'
        #Add Enemies
        for i in range(enemyNum):
            px=random.randint(0, width-1)
            py=random.randint(0, height-1)
            game_map[px][py]='@'

        return game_map

    # 打印地图
    def print_map(game_map):
        for row in game_map:
            print(' '.join(row))

        