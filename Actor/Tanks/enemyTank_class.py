from Actor.Tanks.tank_class import Tank
from AI.StateMachine.stateMachine_class import StateMachine
from AI.SteeringBehavior.steeringBehavior_class import SteeringBehaviors
from AI.StateMachine.States.enemyStates import *
import glm
import math
import Math
import Paras


class EnemyTank(Tank):
    def __init__(self, game):
        super().__init__(game)
        game.mEnemies.append(self)
        self.mCollisionComp.mOnCollide=self.onCollide
        self.mType='Enemy'
        self.mStateMachine=StateMachine(self)
        self.mSteeringBehaviors=SteeringBehaviors(self)
        self.mSteeringBehaviors.mTargetPos=glm.vec2(0,0)
        self.mSteeringBehaviors.SeekOn()
        
    def UpdateActor(self, deltatime):
        super().UpdateActor(deltatime)
    
        totalForce = self.mSteeringBehaviors.Calculate()
        acceleration = totalForce / Paras.EnemyMass
        expectDirection = glm.normalize(acceleration)
        
        # 获取当前角色的朝向（假设你有一个GetForward()方法返回当前的方向向量）
        currentDirection = self.GetForward().xy

        # 判断是否需要转向
        angleDifference = Math.AngleBetweenVectors(currentDirection, expectDirection)

        # 如果角度差异超过阈值，则执行转向
        if not Math.NearZero(angleDifference, 0.01):
            self.TurnTo(expectDirection)
            # 如果需要转向，则直接返回，不进行位置更新
            return
        else:
            # 如果朝向已经对准目标，更新角色的旋转
            self.mRotation = glm.angleAxis(angleDifference, glm.vec3(0, 0, 1))
            
        # 计算前进速度
        self.mMovementComp.mForwardSpeed = glm.length(acceleration) * deltatime
        
    def TurnTo(self, direction):
        currentDirection=self.GetForward().xy
        angle=Math.AngleBetweenVectors(currentDirection, direction)
        if angle<0:
            self.mMovementComp.mAngularSpeed=0.5*math.pi
        if angle>0:
            self.mMovementComp.mAngularSpeed=-0.5*math.pi
    
    def onCollide(self, instigator):
        if instigator.mType=='Cannonball' and instigator.mInstigator!=self:
            self.mHealth-=25
            print('Collide')
            if self.mHealth<=0:
                print('Explode')
                self.mActive=False
        if instigator.mType=='Player' or instigator.mType=='Wall':
            self.mPosition-=self.GetForward()*10