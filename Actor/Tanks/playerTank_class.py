from Actor.Tanks.tank_class import Tank
from Actor.Camera.followCamera_class import FollowCamera
from Component.collisionComponent_class import CollisionComponent
from Actor.cubeActor_class import CubeActor
import Math
import Paras
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
        
        #For sound
        self.mPreviousMoving=False
        self.mIsMoving=False
        
        self.mRecoverTime=0
        
    def UpdateActor(self, deltatime):
        super().UpdateActor(deltatime)
        self.CheckBoundary()
        
        self.Recover(deltatime)
        
        # speed=abs(self.mMovementComp.mForwardSpeed)
        # if speed>0:
        #     self.mPreviousMoving=self.mIsMoving
        #     self.mIsMoving=True
        # else:
        #     self.mPreviousMoving=self.mIsMoving
        #     self.mIsMoving=False
            
        # if (not self.mPreviousMoving and self.mIsMoving):
        #     self.mMoveSound.play(loops=-1)
        
        # if (self.mPreviousMoving and not self.mIsMoving):
        #     self.mMoveSound.stop()
        
        
    def ActorInput(self, keyState):
        super().ActorInput(keyState)
        forwardSpeed=0
        angularSpeed=0
        
        if(keyState[pygame.K_w]):
            forwardSpeed+=150
        if(keyState[pygame.K_s]):
            forwardSpeed-=150
        if(keyState[pygame.K_a]):
            angularSpeed-=0.3*math.pi
        if(keyState[pygame.K_d]):
            angularSpeed+=0.3*math.pi
            
        self.mMovementComp.mForwardSpeed=forwardSpeed
        self.mMovementComp.mAngularSpeed=angularSpeed
        
        #TODO
        self.mTorret.mMovementComp.mAngularSpeed=angularSpeed
        
        extraSpeed=0
        if(keyState[pygame.K_j]):
            extraSpeed-=0.5*math.pi
        if(keyState[pygame.K_k]):
            extraSpeed+=0.5*math.pi
        self.mTorret.mMovementComp.mAngularSpeed+=extraSpeed
        
        if(keyState[pygame.K_SPACE]):
            self.Fire()
            
        # if(keyState[pygame.K_o]):
        #     self.mPosition+=glm.vec3(0,0,1)
        # if(keyState[pygame.K_l]):
        #     self.mPosition+=glm.vec3(0,0,-1)
        
    def Recover(self, deltaTime):
        self.mRecoverTime+=deltaTime
        if self.mRecoverTime>Paras.RecoverTime:
            self.mRecoverTime=Paras.RecoverTime
        if self.mRecoverTime<Paras.RecoverTime:
            return False
        self.mRecoverTime=0
        if self.mHealth<100:
            self.mHealth+=1
            
    def onCollide(self, instigator):
        if instigator.mType=='Cannonball' and instigator.mInstigator!=self:
            self.mHealth-=7
            #print('I am being hit')
            self.mExpodeSound.play()
            if self.mHealth<=0:
                print('Game Over')
                self.mActive=False
        if instigator.mType=='Enemy' or instigator.mType=='Obstacle':
            OtoS=glm.normalize(instigator.mPosition-self.mPosition)
            OtoS.z=0
            self.mPosition-=4*OtoS
    
    def CheckBoundary(self):
        if self.mPosition.x < 0:
            self.mPosition.x=0
        if self.mPosition.x> self.mGame.mGameMap.GetMapWidth():
            self.mPosition.x=self.mGame.mGameMap.GetMapWidth()
        if self.mPosition.y < 0:
            self.mPosition.y=0
        if self.mPosition.y> self.mGame.mGameMap.GetMapHeight():
            self.mPosition.y=self.mGame.mGameMap.GetMapHeight()
            
    def Fire(self):
        if super().Fire():
            self.mFireSound.play()
            #Call enemy sense
            for enemy in self.mGame.mEnemies:
                enemy.mSenseComp.CallAural(self)
            return True
        return False