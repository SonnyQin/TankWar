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
        
        # 每帧更新视图矩阵
        self.SetView()

    def SetView(self):
        # 获取相机位置
        cameraPos = glm.vec3(self.mPosition)
        
        # 计算相机到owner的方向向量
        direction = glm.normalize(self.mOwner.mTorret.mPosition - self.mPosition)
        
        # 偏移量，稍微让相机的目标在owner的前面
        offset = 200*self.mOwner.mTorret.GetForward()  # 偏移量，例如：y轴上偏移50单位
        
        # 使用方向计算目标位置，保持一定的距离并加上偏移量
        target = self.mOwner.mPosition + direction * 300- offset
        
        # 获取初始的上向量（默认的z轴）
        up = glm.vec3(0, 0, 1)
        
        # 计算相机的视图矩阵，确保相机朝向目标，并且up向量随旋转变化
        self.mView = glm.lookAt(cameraPos, target, up)
        
        # 更新渲染器的视图矩阵
        self.mOwner.mGame.mRenderer.mView = self.mView
