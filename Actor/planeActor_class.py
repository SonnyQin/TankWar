from Actor.actor_class import Actor
from Component.meshComponent_class import MeshComponent
import pygame
import math
import glm

class PlaneActor(Actor):
    def __init__(self, game):
        super().__init__(game)
        self.mMeshComp=MeshComponent(self)
        self.mMeshComp.mMesh=game.mRenderer.GetMesh('Assets/Ground.gpmesh')
        self.mScale=30
