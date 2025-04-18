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
        self.mScale=10
        self.mMeshComp=MeshComponent(self)
        self.mMeshComp.mMesh=game.mRenderer.GetMesh('Assets/Chassis.gpmesh')
        inc = glm.angleAxis(math.pi/2, glm.vec3(1, 0, 0))  # 使用 angleAxis 来生成增量旋转
        self.mRotation = glm.normalize(self.mRotation * inc)  # 应用增量旋转并归一化