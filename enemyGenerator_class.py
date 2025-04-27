from Actor.Tanks.enemyTank_class import EnemyTank
from gameMap_class import GameMap
import random
import glm


class EnemyGenerator:
    def __init__(self, game):
        self.mGame=game
        
    def GenerateNewEnemy(self):
        if self.mGame.mEnemyCount<5:
            gameMap=self.mGame.mGameMap.mMap
            width=len(gameMap)
            height=len(gameMap[0])
            #Generate new enemy
            while True:
                px=random.randint(0, width-1)
                py=random.randint(0, height-1)
                if gameMap[px][py]!='#':
                    etank=EnemyTank(self.mGame)
                    x,y=GameMap.GetWorldLocation(px, py)
                    etank.mPosition=glm.vec3(x,y, 15)
                    print("Generate a new enemy")
                    break