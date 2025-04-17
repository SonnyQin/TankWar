from Camera.cameraActor_class import CameraActor

class FollowCamera(CameraActor):
    def __init__(self, game, owner, offset):
        super().__init__(game)
        self.mOwner=owner
        self.mOffset=offset
        self.mPosition=owner.mPosition+offset
        #TODO
        #May adjust rotation
    
    def UpdateActor(self, deltatime):
        super().UpdateActor(deltatime)
        self.mPosition=self.mOwner.mPosition+self.mOffset