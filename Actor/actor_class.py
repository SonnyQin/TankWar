from pyglm.glm import *
import pyglm.glm as glm
import Math

class Actor:
    def __init__(self, game):
        self.mGame=game
        
        self.mWorldTransform=mat4()
        self.mPosition=vec3(0,0,0)
        self.mRotation=quat(1,0,0,0)
        self.mScale=1
        
        self.mComponents=[]
        self.mActive=True
        self.mGame.AddActor(self)
    
    def ProcessInput(self, keyState):
        self.ActorInput(keyState)
        for cp in self.mComponents:
            cp.ProcessInput(keyState)
    
    def ActorInput(self, keyState):
        pass
        
    def Update(self, deltatime:int):
        if self.mActive:
            self.ComputeWorldTransform()
            self.UpdateActor(deltatime)
            self.UpdateComponent(deltatime)
            self.ComputeWorldTransform()
    def UpdateActor(self, deltatime):
        pass
    def UpdateComponent(self, deltatime):
        for component in self.mComponents:
            component.Update(deltatime)
    def AddComponent(self, c):
        self.mComponents.append(c)
        self.mComponents.sort(key=lambda c: c.mUpdateOrder)
    def RemoveComponent(self, c):
        self.mComponents.remove(c)
        self.mComponents.sort(key=lambda c: c.mUpdateOrder)
        
    #Generate by ChatGPT
    def ComputeWorldTransform(self):
        # 1. 使用 glm 的缩放矩阵
        scale_matrix = glm.scale(glm.mat4(1.0), glm.vec3(self.mScale, self.mScale, self.mScale))  # 确保缩放是通过 glm.scale 来进行的

        # 2. 使用 glm 的旋转矩阵（通过四元数）
        rotation_matrix = glm.mat4_cast(glm.quat(self.mRotation) )

        # 3. 使用 glm 的平移矩阵
        translation_matrix = glm.translate(glm.mat4(1.0), self.mPosition)

        # 4. 将它们结合起来：缩放 * 旋转 * 平移
        self.mWorldTransform = translation_matrix * rotation_matrix * scale_matrix
        return self.mWorldTransform
    
    def GetForward(self):
        return Math.transform_vector(vec3(1,0,0), glm.quat(self.mRotation))
    
    #Generate by ChatGPT
    def GetRight(self):
        # 从当前旋转获取右向量
        rot = glm.quat(self.mRotation)  # 获取当前物体的旋转（四元数表示）
        right = rot * glm.vec3(0, 1, 0)  # 乘以单位向量 (1, 0, 0) 获取右方向
        return glm.normalize(right)  # 返回归一化后的右向量

        