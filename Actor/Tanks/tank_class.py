from Actor.actor_class import Actor

class Tank(Actor):
    def __init__(self, game):
        super().__init__(game)
    def Update(self, deltatime):
        return super().Update(deltatime)
    def UpdateActor(self, deltatime):
        return super().UpdateActor(deltatime)