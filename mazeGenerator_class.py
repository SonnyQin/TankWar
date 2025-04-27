import random
import glm  # 使用 glm 库来表示 Vector2

class MazeGenerator:
    def __init__(self):
        self.mapArr = []
        self.mStartPos = None
        self.mEndPos = None

    def creat_map(self, r: int, c: int):
        self.mapArr = []
        notAccessed = []
        accessed = []

        # 创建一个(r * 2 + 1) * (c * 2 + 1) 的地图
        for i in range(r * 2 + 1):
            arr = []
            for n in range(c * 2 + 1):
                if ((n ^ (n - 1)) == 1 and (i ^ (i - 1)) == 1):
                    arr.append(0)  # 0 表示路
                    notAccessed.append(0)
                else:
                    arr.append(1)  # 1 表示墙
            self.mapArr.append(arr)

        # 迷宫生成的核心算法部分
        count = r * c
        cur = random.randint(0, count - 1)
        offs = [-c, c, -1, 1]  # 四周顶点在notAccessed的偏移量
        offr = [-1, 1, 0, 0]  # 四周顶点在arr的纵向偏移量
        offc = [0, 0, -1, 1]  # 四周顶点在arr的横向偏移量
        
        accessed.append(cur)
        notAccessed[cur] = 1

        while len(accessed) < count:
            tr = cur // c
            tc = cur % c
            num = 0
            off = -1

            # 遍历上下左右顶点
            while num < 4:
                around = random.randint(0, 3)
                nr = tr + offr[around]
                nc = tc + offc[around]
                if 0 <= nr < r and 0 <= nc < c and notAccessed[cur + offs[around]] == 0:
                    off = around
                    break
                num += 1

            # 四周顶点均被访问，则从已访问的顶点中随机抽取一个为cur
            if off < 0:
                cur = accessed[random.randint(0, len(accessed) - 1)]
            else:
                tr = 2 * tr + 1
                tc = 2 * tc + 1
                self.mapArr[tr + offr[off]][tc + offc[off]] = 0
                cur = cur + offs[off]
                notAccessed[cur] = 1
                accessed.append(cur)

        # 去除外围的墙壁，保留内核迷宫
        self.mapArr = [row[1:-1] for row in self.mapArr[1:-1]]  # 去掉最外层的墙

        return self.mapArr

    def get_map_arr(self):
        return self.mapArr

    @staticmethod
    def instance():
        if not hasattr(MazeGenerator, "_instance"):
            MazeGenerator._instance = MazeGenerator()
        return MazeGenerator._instance