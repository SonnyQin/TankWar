from Actor.Camera.cameraActor_class import CameraActor
import glm
import math
import pygame

#Generate by ChatPGT for debugging

class FreeCamera(CameraActor):
    def __init__(self, game):
        super().__init__(game)
        self.speed = 1  # 摄像机移动速度
        self.rotation_speed = 0.01*math.pi  # 摄像机旋转速度

    def ActorInput(self, keyState):
        super().ActorInput(keyState)

        # 摄像机的前后左右平移
        if keyState[pygame.K_w]:  # W键向前
            self.mPosition += glm.vec3(self.speed,0,0)
        if keyState[pygame.K_s]:  # S键向后
            self.mPosition -= glm.vec3(self.speed,0,0)
        if keyState[pygame.K_a]:  # A键向左
            self.mPosition -= glm.vec3(0,self.speed,0)
        if keyState[pygame.K_d]:  # D键向右
            self.mPosition += glm.vec3(0,self.speed,0)
        if keyState[pygame.K_o]:  # O键向上
            self.mPosition += glm.vec3(0,0,self.speed)
        if keyState[pygame.K_k]:  # K键向下
            self.mPosition -= glm.vec3(0,0,self.speed)

        # 摄像机旋转
        if keyState[pygame.K_LEFT]:  # 左箭头
            self.mRotation = glm.rotate(self.mRotation, self.rotation_speed, glm.vec3(0.0, 0.0, 1.0))
        if keyState[pygame.K_RIGHT]:  # 右箭头
            self.mRotation = glm.rotate(self.mRotation, -self.rotation_speed, glm.vec3(0.0, 0.0, 1.0))
        if keyState[pygame.K_UP]:  # 上箭头
            self.mRotation = glm.rotate(self.mRotation, -self.rotation_speed, glm.vec3(0.0, 1.0, 0.0))
        if keyState[pygame.K_DOWN]:  # 下箭头
            self.mRotation = glm.rotate(self.mRotation, self.rotation_speed, glm.vec3(0.0, 1.0, 0.0))
