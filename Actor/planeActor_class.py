from Actor.actor_class import Actor
from Component.meshComponent_class import MeshComponent

class PlaneActor(Actor):
    def __init__(self, game):
        super().__init__(game)
        self.mMeshComp=MeshComponent(self)
        self.mMeshComp.mMesh=game.mRenderer.GetMesh('Assets/Torret.gpmesh')
        self.mScale=30