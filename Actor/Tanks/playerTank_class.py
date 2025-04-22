from Actor.Tanks.tank_class import Tank
from Actor.Camera.followCamera_class import FollowCamera
from Component.collisionComponent_class import CollisionComponent
from Actor.cubeActor_class import CubeActor
import Math
import math
import pygame
import glm

class PlayerTank(Tank):
    def __init__(self, game):
        super().__init__(game)
        self.mFollowCamera=FollowCamera(self, -100,75)
        self.mFollowCamera.mActive=True
        self.mCollisionComp.mOnCollide=self.onCollide
        self.mType='Player'
        # self.mCube=CubeActor(game)
        # self.mCube.mScale=65
        
    def UpdateActor(self, deltatime):
        super().UpdateActor(deltatime)
        #self.mCube.mPosition=glm.vec3(self.mPosition)
        
    def ActorInput(self, keyState):
        super().ActorInput(keyState)
        forwardSpeed=0
        angularSpeed=0
        
        if(keyState[pygame.K_w]):
            forwardSpeed+=300
        if(keyState[pygame.K_s]):
            forwardSpeed-=300
        if(keyState[pygame.K_a]):
            angularSpeed-=0.5*math.pi
        if(keyState[pygame.K_d]):
            angularSpeed+=0.5*math.pi
            
        self.mMovementComp.mForwardSpeed=forwardSpeed
        self.mMovementComp.mAngularSpeed=angularSpeed
        
        #TODO
        self.mTorret.mMovementComp.mAngularSpeed=angularSpeed
        
        self.mChassis.mMovementComp.mAngularSpeed=angularSpeed
        
        extraSpeed=0
        if(keyState[pygame.K_j]):
            extraSpeed-=math.pi
        if(keyState[pygame.K_k]):
            extraSpeed+=math.pi
        self.mTorret.mMovementComp.mAngularSpeed+=extraSpeed
        
        
        
        if(keyState[pygame.K_SPACE]):
            self.Fire()
    def onCollide(self, instigator):
        if instigator.mType=='Cannonball' and instigator.mInstigator!=self:
            self.mHealth-=25
            if self.mHealth<=0:
                print('Game Over')
                self.mActive=False
        if instigator.mType=='Enemy' or instigator.mType=='Wall':
            self.mPosition-=self.GetForward()*5