from Actor.actor_class import Actor
from Component.meshComponent_class import MeshComponent
from Component.collisionComponent_class import CollisionComponent
import pygame
import Math
import glm

#Use for wall
class Block(Actor):
    def __init__(self, game):
        super().__init__(game)
        self.mMeshComponent=MeshComponent(self)
        self.mMeshComponent.mMesh=game.mRenderer.GetMesh('Assets/Block.gpmesh')
        self.mCollisionComp=CollisionComponent(self, Math.BoxCollider(self.mPosition, glm.vec3(500,500,500)), self.onCollide)
        self.mScale=500
        self.mGame.mObstacles.append(self)
        self.mType='Obstacle'
    def ActorInput(self, keyState):
        super().ActorInput(keyState)
    
    def onCollide(self, instigator):
        # if instigator.mType=='Cannonball':
        #     print('I am being hit')
        pass
