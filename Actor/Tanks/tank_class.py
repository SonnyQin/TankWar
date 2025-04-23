from Actor.actor_class import Actor
from Component.movementComponent_class import MovementComponent
from Actor.Tanks.torret_class import Torret
from Actor.Tanks.chassis_class import Chassis
from Projectile.cannonball_class import Cannonball
from Component.collisionComponent_class import CollisionComponent
import Math
import Paras
import glm

#Chassis and Torret's position is always Updated to Actor's position
#TODO
#Chassis rotation should be Actor's rotation

class Tank(Actor):
    def __init__(self, game):
        super().__init__(game)
        self.mPosition=glm.vec3(0,0,15)
        self.mTorret=Torret(self)
        self.mChassis=Chassis(self)
        game.RemoveActor(self.mTorret)
        game.RemoveActor(self.mChassis)
        self.mTorret.mPosition=glm.vec3(self.mPosition.x, self.mPosition.y, self.mPosition.z+Paras.TorretOffset)
        self.mChassis.mPosition=glm.vec3(self.mPosition)
        self.mCollisionComp=CollisionComponent(self, Math.SphereCollider(self.mPosition, 50))
        self.mMovementComp=MovementComponent(self)
        self.mCoolDownTime=Paras.CoolDownTime
        
        self.mHealth=100
        
    def Update(self, deltatime):
        super().Update(deltatime)
    def UpdateActor(self, deltatime):
        super().UpdateActor(deltatime)
        
        self.mTorret.Update(deltatime)
        self.mChassis.Update(deltatime)

        self.mCoolDownTime+=deltatime
        if self.mCoolDownTime>Paras.CoolDownTime:
            self.mCoolDownTime=Paras.CoolDownTime
        
        #Set two parts of the Tank to Tank's pos
        self.mTorret.mPosition=glm.vec3(self.mPosition.x, self.mPosition.y, self.mPosition.z+Paras.TorretOffset)
        self.mChassis.mPosition=glm.vec3(self.mPosition)
        self.mChassis.mRotation=glm.quat(self.mRotation)
        
        #Call enemy sense
        for enemy in self.mGame.mEnemies:
            enemy.mSenseComp.CallVisual(self)
        
    def Fire(self):
        if self.mCoolDownTime<Paras.CoolDownTime:
            return
        self.mCoolDownTime=0
        Cannonball(self)
        #Call enemy sense
        for enemy in self.mGame.mEnemies:
            enemy.mSenseComp.CallAural(self)