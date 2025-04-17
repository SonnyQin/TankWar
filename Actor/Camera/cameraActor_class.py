from Actor.actor_class import Actor
from pyglm.glm import *
import pyglm.glm as glm
import Math
import pygame

class CameraActor(Actor):
    def __init__(self, game):
        super().__init__(game)
    def UpdateActor(self, deltatime):
        super().UpdateActor(deltatime)
        cameraPos=vec3(self.mPosition) 
        target=self.mPosition+ self.GetForward()*100
        up=vec3(0,0,1)
        self.mView=glm.lookAt(cameraPos, target, up)
        self.mGame.mRenderer.mView=self.mView
    def ActorInput(self, keyState):
        super().ActorInput(keyState)
        