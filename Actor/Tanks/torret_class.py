from Actor.actor_class import Actor
from Actor.Camera.followCamera_class import FollowCamera
from Component.movementComponent_class import MovementComponent
from Component.meshComponent_class import MeshComponent
import Math
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
        
    def TurnTo(self, direction):
        currentDirection = self.GetForward().xy
        # 计算叉积
        crossProduct = currentDirection.x * direction.y - currentDirection.y * direction.x
        # 计算角度差（可以根据叉积的符号来判断转向的方向）
        if Math.NearZero(crossProduct):
            self.mMovementComp.mAngularSpeed = 0
            return True
        if crossProduct < 0:  # 顺时针旋转
            self.mMovementComp.mAngularSpeed = -0.3 * math.pi
            return False
        elif crossProduct > 0:  # 逆时针旋转
            self.mMovementComp.mAngularSpeed = 0.3 * math.pi
            return False