from Actor.actor_class import Actor
from Component.meshComponent_class import MeshComponent


#Inspired by ChatGPT
class DirectionalLight(Actor):
    def __init__(self, game):
        super().__init__(game)
        #For debugging
        #turn off the mesh as it will block the light
        self.mScale=10
        self.mDirection=None
        self.mDiffuseColor=None
        self.mSpecColor=None
        
        # #For debugging
        # self.mMeshComp=MeshComponent(self)
        # self.mMeshComp.mMesh=self.mGame.mRenderer.GetMesh('Assets/Sphere.gpmesh')