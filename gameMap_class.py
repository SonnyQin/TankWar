class GameMap:
    def __init__(self, map):
        self.mMap=map
        
    def GetMapLocation(x, y):
        row=x/1000
        if x%1000!=0:
            row+=1
        column=y/1000
        if y%1000!=0:
            column+=1
        return x,y