from Actor.Tanks.tank_class import Tank
from AI.StateMachine.stateMachine_class import StateMachine
from AI.SteeringBehavior.steeringBehavior_class import SteeringBehaviors
from AI.StateMachine.States.enemyStates import *
from Component.navigationComponent_class import NavigationComponent
from Component.senseComponent_class import SenseComponent
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
        self.mSenseComp=SenseComponent(self)
        
        self.mStateMachine=StateMachine(self)
        self.mStateMachine.mGlobalState=EnemyGlobalState.get_instance()
        self.mStateMachine.mCurrentState=EnemyDefaultState.get_instance()
        self.mStateMachine.mGlobalState.Enter(self)
        self.mStateMachine.mCurrentState.Enter(self)
        
        self.mTorretWanderDirection=None
        
    def Update(self, deltatime):
        super().Update(deltatime)
        #print(self.mPosition)
        
    def UpdateActor(self, deltatime):
        super().UpdateActor(deltatime)
        # if self.mSteeringBehaviors.mTargetPos:
        #     print(self.mSteeringBehaviors.mTargetPos)
        
        self.mStateMachine.Update()
        #Move the tank
        self.Steering(deltatime)
        
        self.TorretWander()
        
        self.TorretAim()
        
        # if(glm.length(self.mPosition.xy-glm.vec2(500,500))<10):
        #     self.mSteeringBehaviors.SeekOff()
        #     self.mMovementComp.mForwardSpeed=0
        #     self.mMovementComp.mAngularSpeed=0
        
        self.CheckBoundary()
        
    def TurnTo(self, direction):
        currentDirection = -self.GetForward().xy
        # 计算叉积
        crossProduct = currentDirection.x * direction.y - currentDirection.y * direction.x
        # 计算角度差（可以根据叉积的符号来判断转向的方向）
        if Math.NearZero(crossProduct):
            self.mMovementComp.mAngularSpeed = 0
            return True
        if crossProduct < 0:  # 顺时针旋转
            self.mMovementComp.mAngularSpeed = -0.3 * math.pi
            return False
        elif crossProduct > 0:  # 逆时针旋转
            self.mMovementComp.mAngularSpeed = 0.3 * math.pi
            return False
    
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
        #currentDirection = self.GetForward().xy

        # # 判断是否需要转向
        # angleDifference = Math.AngleBetweenVectors(currentDirection, expectDirection)
        #print(angleDifference)

        # # 如果角度差异超过阈值，则执行转向
        # if not Math.NearZero(angleDifference, 0.01):
            # self.TurnTo(expectDirection)
            # # 如果需要转向，则直接返回，不进行位置更新
            # return
            
        if not self.TurnTo(expectDirection):
            return
        
        # 计算前进速度
        self.mMovementComp.mForwardSpeed = glm.length(acceleration)
    
    #Randomly rotate the Torret
    def TorretWander(self):
        if self.mStateMachine.mCurrentState==EnemyWanderState.get_instance() or self.mStateMachine.mCurrentState==EnemyAttendState.get_instance():
            if not self.mTorretWanderDirection:
                self.mTorretWanderDirection=Math.GenerateRandom2DDirection()
                
            if self.mTorret.TurnTo(self.mTorretWanderDirection):
                self.mTorretWanderDirection=Math.GenerateRandom2DDirection()
                
    def TorretAim(self):
        if self.mStateMachine.mCurrentState==EnemyAttackState.get_instance():
            direction=glm.normalize((self.mGame.mPlayerTank.mPosition-self.mPosition).xy)
            #angleDifference = Math.AngleBetweenVectors(-self.mTorret.GetForward().xy, direction)
            #if not Math.NearZero(angleDifference, 0.01):
            self.mTorret.TurnTo(direction)
            # else:
            #     self.mTorret.mMovementComp.mAngularSpeed=0
        
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
            self.mSenseComp.mIsSensed=True
            print('Enemy being hit')
            # self.mExpodeSound.play()
            if self.mHealth<=0:
                print('Explode')
                self.mStateMachine.ChangeState(EnemyDeadState.get_instance())
                self.mGame.mScore+=10
                self.mGame.mEnemyCount-=1
                
        if instigator.mType=='Player' or instigator.mType=='Obstacle':
            OtoS=glm.normalize(instigator.mPosition-self.mPosition)
            OtoS.z=0
            self.mPosition-=2*OtoS
            
    def CheckBoundary(self):
        if self.mPosition.x<0 or self.mPosition.x>self.mGame.mGameMap.GetMapWidth() or self.mPosition.y<0 or self.mPosition.y> self.mGame.mGameMap.GetMapHeight():
            self.mActive=False
    
    def Fire(self):
        if super().Fire():
            #print('Enemy fires')
            return True
        return False
        