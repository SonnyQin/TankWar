import math
import glm

class FollowCamera:
    def __init__(self, owner, length, height):
        self.mOwner = owner
        self.mLength=length
        self.mHeight=height
        
        self.mOwner.mGame.mCameras.append(self)
        
        self.mPosition = owner.mTorret.mPosition - owner.mTorret.GetForward()*self.mLength+glm.vec3(0,0,self.mHeight)

    def Update(self):
        self.mPosition = self.mOwner.mTorret.mPosition - self.mOwner.mTorret.GetForward()*self.mLength+glm.vec3(0,0,self.mHeight)
        
        self.SetView()

    def SetView(self):
        cameraPos = glm.vec3(self.mPosition)
        direction = glm.normalize(self.mOwner.mTorret.mPosition - self.mPosition)
        
        offset = 200*self.mOwner.mTorret.GetForward()
        
        target = self.mOwner.mPosition + direction * 300- offset
        
        up = glm.vec3(0, 0, 1)
        
        self.mView = glm.lookAt(cameraPos, target, up)
        
        self.mOwner.mGame.mRenderer.mView = self.mView
