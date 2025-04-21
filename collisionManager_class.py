class CollisionManager:
    def __init__(self, game):
        self.mGame=game
    
    def CheckCollision(self):
        projectils=self.mGame.mProjectiles
        enemies=self.mGame.mEnemies
        #Check enemy and cannonball
        for enemy in enemies:
            for projectile in projectils:
                if enemy.mActive and projectile.mActive:
                    enemy.mCollisionComp.CheckCollision(projectile.mCollisionComp)
        #Check Player and wall
        
        #Check Player and eney
        for enemy in enemies:
            enemy.mCollisionComp.CheckCollision(self.mGame.mPlayerTank.mCollisionComp)