from Actor.actor_class import Actor
from Component.collisionComponent_class import CollisionComponent
import Math
import math
import Paras

class Cannonball(Actor):
    def __init__(self, instigator):
        super().__init__(instigator.mGame)
        instigator.mGame.mProjectiles.append(self)
        self.mCollisionComponent=CollisionComponent(self, Math.SphereCollider(self.mPosition, Paras.CannonballRadius))
        self.type='Cannonball'
    
    def Update(self, deltatime):
        super().Update(deltatime)