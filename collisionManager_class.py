class CollisionManager:
    def __init__(self, game):
        self.mGame=game
    
    def CheckCollision(self):
        projectils=self.mGame.mProjectiles
        enemies=self.mGame.mEnemies
        obstacles=self.mGame.mObstacles
        #Check enemy and cannonball
        for enemy in enemies:
            for projectile in projectils:
                if enemy.mActive and projectile.mActive:
                    enemy.mCollisionComp.CheckCollision(projectile.mCollisionComp)
        
        #Check Player and cannonball
        for projectile in projectils:
            if self.mGame.mPlayerTank.mActive and projectile.mActive:
                self.mGame.mPlayerTank.mCollisionComp.CheckCollision(projectile.mCollisionComp)
                    
        #Check cannonball and wall
        for obstacle in obstacles:
            for projectile in projectils:
                if projectile.mActive:
                    obstacle.mCollisionComp.CheckCollision(projectile.mCollisionComp)
                    
        #Check Player and wall
        for obstacle in obstacles:
            if self.mGame.mPlayerTank:
                obstacle.mCollisionComp.CheckCollision(self.mGame.mPlayerTank.mCollisionComp)
        
        #Check Player and enemy
        for enemy in enemies:
            if self.mGame.mPlayerTank:
                enemy.mCollisionComp.CheckCollision(self.mGame.mPlayerTank.mCollisionComp)