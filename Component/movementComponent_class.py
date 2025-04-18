from Component.component_class import Component
import glm
import Math
import Paras


class MovementComponent(Component):
    def __init__(self, owner, updateOrder=0):
        super().__init__(owner, updateOrder=0)
        self.mForwardSpeed = 0
        self.mAngularSpeed = 0
    
    def ProcessInput(self, keyState):
        super().ProcessInput(keyState)
    
    def Update(self, deltatime):
        super().Update(deltatime)
        
        #print(self.mOwner.mRotation)
        #print(self.mOwner.mPosition)
        
        if not Math.NearZero(self.mAngularSpeed):
            rot = glm.quat(self.mOwner.mRotation)  # 当前旋转
            angle = self.mAngularSpeed * deltatime  # 旋转增量
            
            inc = glm.angleAxis(-angle, glm.vec3(0, 0, 1))  # 使用 angleAxis 来生成增量旋转
            self.mOwner.mRotation = rot * inc

        if not Math.NearZero(self.mForwardSpeed):
            pos = glm.vec3(self.mOwner.mPosition)
            forward = self.mOwner.GetForward()  # 获取前方向量
            pos += forward * self.mForwardSpeed * deltatime  # 更新位置
            self.mOwner.mPosition=glm.vec3(pos)