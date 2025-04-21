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
        self.type='Cannonball'
        
        self.mCollisionComp=CollisionComponent(self, Math.SphereCollider(self.mPosition, 4))
        # self.mCube=CubeActor(instigator.mGame)
        # self.mCube.mScale=4
    
    def Update(self, deltatime):
        super().Update(deltatime)
        #self.mCube.mPosition=glm.vec3(self.mPosition)