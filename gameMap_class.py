class GameMap:
    def __init__(self, map):
        self.mMap=map
        
    def GetMapLocation(x, y):
        row=x//1000
        if x%1000!=0:
            row+=1
        column=y//1000
        if y%1000!=0:
            column+=1
        return int(row-1), int(column-1)
    
    def GetWorldLocation(row, column):
        # 计算世界坐标，假设每个格子的大小是1000单位
        x = row * 1000+500
        y = column * 1000+500
        return x, y

        