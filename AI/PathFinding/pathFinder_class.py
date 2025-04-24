from gameMap_class import GameMap
import glm
import heapq

# TODO
# Consider all paths to adjacent nodes have the same length
# May be optimized through checking whether attainable between two nodes, if true, deleting the nodes between them
class PathFinder:
    def __init__(self, map):
        self.start = None
        self.goal = None
        self.map = map  # 地图信息
        self.open_list = []  # 优先队列
        self.came_from = {}  # 记录路径
        self.g_score = {}  # G 值
        self.f_score = {}  # F 值
        self.mUnableToAttend=False

    def Heuristic(self, node, goal):
        # 计算启发值（例如曼哈顿距离）
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

    def GetNeighbors(self, node):
        # 获取当前节点的邻居
        x, y = node
        neighbors = []
        # 包括上下左右以及斜对角方向
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(self.map) and 0 <= ny < len(self.map[0]) and (self.map[nx][ny] == 0 or self.map[nx][ny] == '.' or self.map[nx][ny] == '@' or self.map[nx][ny] == '$') and self.map[nx][ny]!='#':
                neighbors.append((nx, ny))
        return neighbors

    def ReconstructPath(self, came_from, current):
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path

    def FindPathStep(self):
        if not self.open_list:
            print('Unable to Attend')
            self.mUnAbleToAttend=True
            return False  # 没有更多的节点可探索

        # 弹出 F 值最小的节点
        _, current = heapq.heappop(self.open_list)

        # 如果到达目标，返回路径
        if current == self.goal:
            return self.ReconstructPath(self.came_from, current)

        # 继续探索邻居
        for neighbor in self.GetNeighbors(current):
            tentative_g_score = self.g_score[current] + 1  # 假设每个边的权重为 1
            if neighbor not in self.g_score or tentative_g_score < self.g_score[neighbor]:
                self.came_from[neighbor] = current
                self.g_score[neighbor] = tentative_g_score
                self.f_score[neighbor] = self.g_score[neighbor] + self.Heuristic(neighbor, self.goal)
                heapq.heappush(self.open_list, (self.f_score[neighbor], neighbor))

        return None  # 没有找到路径，继续执行

    def StartFindPath(self, start, goal):
        # 初始化
        self.start = start
        self.goal = goal
        self.open_list = []
        self.mUnAbleToAttend=False
        heap=[]
        heapq.heapify(heap)
        heapq.heappush(self.open_list, (0, start))  # (f_score, node)
        self.came_from = {start: None}
        self.g_score = {start: 0}
        self.f_score = {start: self.Heuristic(start, goal)}

    def Reset(self):
        # 重置 PathFinder 状态
        self.start = None
        self.goal = None
        self.open_list = []
        self.came_from = {}
        self.g_score = {}
        self.f_score = {}
        self.mUnAbleToAttend=False

    # Transform from index form to position form
    @staticmethod
    def IndexToPosition(path, endPos):
        result = []
        #result.append(glm.vec2(startPos.x, startPos.y))
        for node in path:
            x, y = GameMap.GetWorldLocation(node[0], node[1])
            result.append((x, y))
        result.append(glm.vec2(endPos.x, endPos.y))
        return result
    
    
class PathProcedure:
    def __init__(self, path):
        #The node currently expected to attend
        #Because first need to go the start pos
        self.mCurrentNodeIndex=0
        self.mPath=path
    
    def GetCurrentNode(self):
        return self.mPath[self.mCurrentNodeIndex]
    
    def NextNode(self):
        self.mCurrentNodeIndex+=1
        if self.mCurrentNodeIndex==len(self.mPath):
            return False
        return True
    


if __name__=='__main__':
    game_map = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 0, 0, 1, 0, 0, 0],
        [0, 1, 1, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 0, 0],
        [0, 1, 0, 0, 0, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
        
    pathfinder = PathFinder(game_map)
    start = (0, 0)  # 起点
    goal = (8, 8)   # 终点

    # 初始化路径搜索
    pathfinder.StartFindPath(start, goal)

    result=False
    while not result:
        # 你可以在游戏的每一帧调用 FindPathStep 来迭代计算
        result = pathfinder.FindPathStep(goal)

        if result is not None:
            print("找到路径:", result)
        else:
            print("路径仍在计算中...")
