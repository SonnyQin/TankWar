from Actor.actor_class import Actor
from Actor.Camera.followCamera_class import FollowCamera
from Component.movementComponent_class import MovementComponent
from Component.meshComponent_class import MeshComponent
import math
import glm


class Chassis(Actor):
    def __init__(self, owner):
        game=owner.mGame
        super().__init__(game)
        self.mScale=1.6
        self.mMeshComp=MeshComponent(self)
        self.mMeshComp.mMesh=game.mRenderer.GetMesh('Assets/FancyChassisxxxx.gpmesh')