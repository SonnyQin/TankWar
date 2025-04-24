from Actor.actor_class import Actor
from Component.meshComponent_class import MeshComponent
import glm

class Spotlight(Actor):
    def __init__(self, game):
        super().__init__(game)
        
        self.mScale = 10.0
        
        self.mPosition = None
        self.mDirection =None
        
        self.mDiffuseColor = None
        self.mSpecColor = None
        
        self.mCutoff = glm.cos(glm.radians(12.5))
        self.mOuterCutoff = glm.cos(glm.radians(17.5))
        
        # # For debugging: mesh to represent the light (e.g., sphere for visualization)
        # self.mMeshComp = MeshComponent(self)
        # self.mMeshComp.mMesh = self.mGame.mRenderer.GetMesh('Assets/Sphere.gpmesh')