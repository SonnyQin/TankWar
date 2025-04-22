from Actor.Tanks.tank_class import Tank
from AI.StateMachine.stateMachine_class import StateMachine
from AI.SteeringBehavior.steeringBehavior_class import SteeringBehaviors
from AI.StateMachine.States.enemyStates import *
from AI.PathFinding.pathFinder_class import PathFinder
from Component.navigationComponent_class import NavigationComponent
from gameMap_class import GameMap
import random
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
        self.mStateMachine.mGlobalState=EnemyGlobalState._Instance
        self.mStateMachine.mCurrentState=EnemyWanderState._Instance
        self.mStateMachine.mGlobalState.Enter(self)
        self.mStateMachine.mCurrentState.Enter(self)
        
        self.mSteeringBehaviors=SteeringBehaviors(self)
        self.mSteeringBehaviors.mTargetPos=None
        
        self.mNavigationCompo=NavigationComponent(self)
        
    def UpdateActor(self, deltatime):
        super().UpdateActor(deltatime)
        print(self.mPosition.xy)
        
        #Move the tank
        self.Steering(deltatime)
        
    def TurnTo(self, direction):
        currentDirection=self.GetForward().xy
        angle=Math.AngleBetweenVectors(currentDirection, direction)
        if angle<0:
            self.mMovementComp.mAngularSpeed=-0.5*math.pi
            self.mChassis.mAngularSpeed=-0.5*math.pi
        if angle>0:
            self.mMovementComp.mAngularSpeed=0.5*math.pi
            self.mChassis.mMovementComp.mAngularSpeed=0.5*math.pi
    
    #TODO may be optimized
    def Steering(self, deltatime):
        #Reset MovementComponent
        self.mMovementComp.mAngularSpeed=0
        self.mChassis.mMovementComp.mAngularSpeed=0
        self.mMovementComp.mForwardSpeed=0
        self.mChassis.mMovementComp.mForwardSpeed=0
        
        totalForce = self.mSteeringBehaviors.Calculate()
        acceleration = totalForce / Paras.EnemyMass
        expectDirection = glm.normalize(acceleration)
        
        # 获取当前角色的朝向（假设你有一个GetForward()方法返回当前的方向向量）
        currentDirection = self.GetForward().xy

        # 判断是否需要转向
        angleDifference = Math.AngleBetweenVectors(currentDirection, expectDirection)
        #print(angleDifference)

        # 如果角度差异超过阈值，则执行转向
        if not Math.NearZero(angleDifference, 0.01):
            self.TurnTo(expectDirection)
            # 如果需要转向，则直接返回，不进行位置更新
            return
            
        # 计算前进速度
        self.mMovementComp.mForwardSpeed = glm.length(acceleration)
        self.mChassis.mMovementComp.mForwardSpeed = glm.length(acceleration)
    
    def TorretWander(self):
        pass
    
    def GenerateWanderPos(self):
        rd=glm.vec2(random.random(), random.random())
        rd*=Paras.EnemyWanderRad
        return self.mPosition+rd
    
    def onCollide(self, instigator):
        if instigator.mType=='Cannonball' and instigator.mInstigator!=self:
            self.mHealth-=25
            print('Collide')
            if self.mHealth<=0:
                print('Explode')
                self.mActive=False
        if instigator.mType=='Player' or instigator.mType=='Wall':
            self.mPosition-=0.01*self.GetForward()