from Actor.actor_class import Actor
from Component.meshComponent_class import MeshComponent
import pygame
import Math
import glm

#Inspired by ChatGPT
#Unused

class SkyBox(Actor):
    def __init__(self, game):
        super().__init__(game)
        self.mMeshComponent=MeshComponent(self)
        self.mMeshComponent.mMesh=game.mRenderer.GetMesh('Assets/SkyBox.gpmesh')
        self.mScale=5000
    def ActorInput(self, keyState):
        super().ActorInput(keyState)
