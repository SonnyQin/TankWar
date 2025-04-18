from Actor.Camera.cameraActor_class import CameraActor
import math
import glm

class FollowCamera(CameraActor):
    def __init__(self,owner, offset):
        super().__init__(owner.mGame)
        self.mOwner=owner
        self.mOffset=offset
        self.mPosition=owner.mPosition+offset
        self.mRotation*=glm.angleAxis(0.5*math.pi, glm.vec3(0,1,0))
    
    def UpdateActor(self, deltatime):
        super().UpdateActor(deltatime)
        self.mPosition=self.mOwner.mPosition+self.mOffset