from Tanks.tank_class import Tank
from Actor.Camera.followCamera_class import FollowCamera
#from Component.movementComponent_class import MovementComponent
from Component.meshComponent_class import MeshComponent
import glm

class PlayerTank(Tank):
    def __init__(self, game):
        super().__init__(game)
        #self.mMovementComp=MovementComponent(self)
        self.mFollowCamera=FollowCamera(self.mGame, self, glm.vec3(0,0,100))
        self.mTorretMeshComp=MeshComponent(self)
        self.mChassisMeshComp=MeshComponent(self)
    