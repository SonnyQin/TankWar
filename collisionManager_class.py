class CollisionManager:
    def __init__(self, game):
        self.mGame=game
    
    def CheckCollision(self):
        projectils=self.mGame.mProjectiles
        enemies=self.mGame.mEnemies
        #Check enemy and cannonball
        for enemy in enemies:
            for projectile in projectils:
                enemy.mCollisionComp.CheckCollision(projectile.mCollisionComp)