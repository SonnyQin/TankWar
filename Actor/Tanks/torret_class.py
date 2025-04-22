from Actor.actor_class import Actor
from Actor.Camera.followCamera_class import FollowCamera
from Component.movementComponent_class import MovementComponent
from Component.meshComponent_class import MeshComponent
import math
import glm


class Torret(Actor):
    def __init__(self, owner):
        game=owner.mGame
        super().__init__(game)
        self.mRotation*=glm.angleAxis(math.pi, glm.vec3(0,0,1))
        self.mScale=15
        self.mMeshComp=MeshComponent(self)
        self.mMeshComp.mMesh=game.mRenderer.GetMesh('Assets/Torret.gpmesh')
        self.mMovementComp=MovementComponent(self)