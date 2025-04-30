import glm


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
        x = row * 1000+500
        y = column * 1000+500
        return x, y
    
    def GetMapWidthNum(self):
        return len(self.mMap)
    
    def GetMapHeightNum(self):
        return len(self.mMap[0])
    
    def GetMapWidth(self):
        return len(self.mMap)*1000
    
    def GetMapHeight(self):
        return len(self.mMap[0])*1000
    
    def GetCenter(self):
        return glm.vec3(self.GetMapWidth()/2, self.GetMapHeight()/2, 1000)

        