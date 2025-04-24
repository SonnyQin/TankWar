from Actor.actor_class import Actor
from Component.collisionComponent_class import CollisionComponent
from Component.meshComponent_class import MeshComponent
from Component.movementComponent_class import MovementComponent
import Math
import math
import glm
import Paras
from Actor.cubeActor_class import CubeActor

#TODO May destroy after several seconds
class Cannonball(Actor):
    def __init__(self, instigator):
        super().__init__(instigator.mGame)
        instigator.mGame.mProjectiles.append(self)
        self.mInstigator=instigator
        self.mPosition=glm.vec3(instigator.mTorret.mPosition)
        self.mRotation=glm.quat(instigator.mTorret.mRotation*glm.angleAxis(math.pi, glm.vec3(0,0,1)))
        self.mMovementComp=MovementComponent(self)
        #self.mCollisionComponent=CollisionComponent(self, Math.SphereCollider(self.mPosition, Paras.CannonballRadius))
        self.mMeshComp=MeshComponent(self)
        self.mMeshComp.mMesh=instigator.mGame.mRenderer.GetMesh('Assets/Cannonball.gpmesh')
        self.mSpeed=Paras.CannonballSpeed
        self.mMovementComp.mForwardSpeed=self.mSpeed
        self.mScale=4
        #self.mRotation*=glm.angleAxis(math.pi/2, glm.vec3(0,1,0))
        self.mType='Cannonball'
        
        self.mCollisionComp=CollisionComponent(self, Math.SphereCollider(self.mPosition, 4), self.onCollide)
        # self.mCube=CubeActor(instigator.mGame)
        # self.mCube.mScale=4
    
    def Update(self, deltatime):
        super().Update(deltatime)
        map=self.mGame.mGameMap.mMap
        gameWidth=len(map)*1000
        gameHeight=len(map[0])*1000
        if self.mPosition.x <0 or self.mPosition.x>gameWidth or self.mPosition.y<0 or self.mPosition.y>gameHeight:
            self.mActive=False
    
    def onCollide(self, instigator):
        if instigator!=self.mInstigator:
            self.mActive=False
            #print('collide')