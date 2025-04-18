from Actor.Tanks.tank_class import Tank
from Actor.Camera.followCamera_class import FollowCamera
import math
import pygame
import glm

class PlayerTank(Tank):
    def __init__(self, game):
        super().__init__(game)
        self.mFollowCamera=FollowCamera(self, glm.vec3(100,0,300))
        self.mFollowCamera.mActive=True
        
    def UpdateActor(self, deltatime):
        super().UpdateActor(deltatime)
        
    def ActorInput(self, keyState):
        super().ActorInput(keyState)
        forwardSpeed=0
        angularSpeed=0
        
        if(keyState[pygame.K_w]):
            forwardSpeed+=100
        if(keyState[pygame.K_s]):
            forwardSpeed-=100
        if(keyState[pygame.K_a]):
            angularSpeed-=math.pi
        if(keyState[pygame.K_d]):
            angularSpeed+=math.pi
            
        self.mMovementComp.mForwardSpeed=forwardSpeed
        self.mMovementComp.mAngularSpeed=angularSpeed
        
        self.mTorret.mMovementComp.mForwardSpeed=forwardSpeed
        self.mTorret.mMovementComp.mAngularSpeed=angularSpeed
        
        self.mChassis.mMovementComp.mForwardSpeed=forwardSpeed
        self.mChassis.mMovementComp.mAngularSpeed=angularSpeed
        
        extraSpeed=0
        if(keyState[pygame.K_j]):
            extraSpeed-=math.pi
        if(keyState[pygame.K_k]):
            extraSpeed+=math.pi
        self.mTorret.mMovementComp.mAngularSpeed+=extraSpeed
        
        
        
        if(keyState[pygame.K_SPACE]):
            self.Fire()