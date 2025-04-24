from Actor.actor_class import Actor
from Component.collisionComponent_class import CollisionComponent
from Component.movementComponent_class import MovementComponent
from Component.meshComponent_class import MeshComponent
import math
import Math


class RepairPacket(Actor):
    def __init__(self, game):
        super().__init__(game)
        self.mCollisionComp=CollisionComponent(self, Math.SphereCollider(self.mPosition, 50), self.OnCollide)
        self.mMovemmentComp=MovementComponent(self)
        self.mMovemmentComp.mAngularSpeed=0.1*math.pi
        self.mMeshComp=MeshComponent(self)
        self.mMeshComp.mMesh=game.mRenderer.GetMesh('Assets/RepairPacket.gpmesh')
        
    def UpdateActor(self, deltatime):
        super().UpdateActor(deltatime)

    def OnCollide(self, instigator):
        if instigator.mType=='Player':
            instigator.mHealth=100