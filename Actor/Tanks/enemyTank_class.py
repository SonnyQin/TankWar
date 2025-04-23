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
        
        self.mSteeringBehaviors=SteeringBehaviors(self)
        self.mSteeringBehaviors.mTargetPos=None
        
        self.mNavigationComp=NavigationComponent(self)
        
        self.mStateMachine=StateMachine(self)
        self.mStateMachine.mGlobalState=EnemyGlobalState.get_instance()
        self.mStateMachine.mCurrentState=EnemyDefaultState.get_instance()
        self.mStateMachine.mGlobalState.Enter(self)
        self.mStateMachine.mCurrentState.Enter(self)
        
    def Update(self, deltatime):
        self.mStateMachine.Update()
        super().Update(deltatime)
        
    def UpdateActor(self, deltatime):
        super().UpdateActor(deltatime)
        # if self.mSteeringBehaviors.mTargetPos:
        #     print(self.mSteeringBehaviors.mTargetPos)
        
        #Move the tank
        self.Steering(deltatime)
        
        # if(glm.length(self.mPosition.xy-glm.vec2(500,500))<10):
        #     self.mSteeringBehaviors.SeekOff()
        #     self.mMovementComp.mForwardSpeed=0
        #     self.mMovementComp.mAngularSpeed=0
        
    def TurnTo(self, direction):
        currentDirection=self.GetForward().xy
        angle=Math.AngleBetweenVectors(currentDirection, direction)
        if angle<0:
            self.mMovementComp.mAngularSpeed=-0.1*math.pi
        if angle>0:
            self.mMovementComp.mAngularSpeed=0.1*math.pi
    
    #TODO may be optimized
    def Steering(self, deltatime):
        #Reset MovementComponent
        self.mMovementComp.mAngularSpeed=0
        self.mMovementComp.mForwardSpeed=0
        
        totalForce = self.mSteeringBehaviors.Calculate()
        acceleration = totalForce / Paras.EnemyMass
        
        # print(totalForce)
        
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
    
    def TorretWander(self):
        pass
    
    #TODO
    def GenerateWanderPos(self):
        # 生成一个随机的偏移量
        rd = glm.vec2(random.random(), random.random())  # 生成 [0, 1) 范围内的随机数
        rd -= glm.vec2(0.5, 0.5)  # 让偏移量范围从 [-0.5, 0.5) ，而不是 [0, 1)
        rd *= 2*Paras.EnemyWanderRad  # 放大偏移量到适当的漫游半径
        
        # 计算期望的目标位置
        expectPos = self.mPosition.xy + rd
        
        # 限制位置不超出地图边界
        expectPos.x = glm.clamp(expectPos.x, 1, len(self.mGame.mGameMap.mMap) * 1000 - 1)
        expectPos.y = glm.clamp(expectPos.y, 1, len(self.mGame.mGameMap.mMap[0]) * 1000 - 1)
        
        maploc=GameMap.GetMapLocation(expectPos.x, expectPos.y)
        
        #Regenerate if the target is a wall
        if self.mGame.mGameMap.mMap[maploc[0]][maploc[1]]=='#': 
            return self.GenerateWanderPos()
        
        return expectPos

    
    def onCollide(self, instigator):
        if instigator.mType=='Cannonball' and instigator.mInstigator!=self:
            self.mHealth-=25
            print('Collide')
            if self.mHealth<=0:
                print('Explode')
                self.mActive=False
                
        if instigator.mType=='Player' or instigator.mType=='Wall':
            OtoS=glm.normalize(instigator.mPosition-self.mPosition)
            OtoS.z=0
            self.mPosition-=2*OtoS