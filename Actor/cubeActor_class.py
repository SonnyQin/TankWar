from Actor.actor_class import Actor
from Component.meshComponent_class import MeshComponent
import pygame
import Math
import glm

class CubeActor(Actor):
    def __init__(self, game):
        super().__init__(game)
        self.mMeshComponent=MeshComponent(self)
        self.mMeshComponent.mMesh=game.mRenderer.GetMesh('Assets/Cube.gpmesh')
        self.mScale=100
        self.mPosition.x=200
        self.mPosition.y=10
    def ActorInput(self, keyState):
        super().ActorInput(keyState)
        if(keyState[pygame.K_q]):
            rot=glm.quat(self.mRotation)
            angle=0.01
            inc = glm.quat(glm.cos(angle / 2), 0, glm.sin(angle / 2), 0)  # 绕 y 轴旋转
            inc=rot*inc
            self.mRotation=glm.quat(inc)
            #self.mRotation=glm.normalize(self.mRotation)
            print(self.mRotation)