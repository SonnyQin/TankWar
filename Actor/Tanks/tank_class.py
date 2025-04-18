from Actor.actor_class import Actor
from Component.movementComponent_class import MovementComponent
from Actor.Tanks.torret_class import Torret
from Actor.Tanks.chassis_class import Chassis
import Paras
import glm


class Tank(Actor):
    def __init__(self, game):
        super().__init__(game)
        self.mPosition=glm.vec3(0,0,15)
        self.mTorret=Torret(self)
        self.mChassis=Chassis(self)
        self.mTorret.mPosition=glm.vec3(self.mPosition.x, self.mPosition.y, self.mPosition.z+Paras.TorretOffset)
        self.mChassis.mPosition=glm.vec3(self.mPosition)
        self.mMovementComp=MovementComponent(self)
    def Update(self, deltatime):
        super().Update(deltatime)
    def UpdateActor(self, deltatime):
        super().UpdateActor(deltatime)
        self.mTorret.mPosition=glm.vec3(self.mPosition.x, self.mPosition.y, self.mPosition.z+Paras.TorretOffset)
        self.mChassis.mPosition=glm.vec3(self.mPosition)