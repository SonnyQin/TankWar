from Component.component_class import Component

class CollisionComponent(Component):
    def __init__(self, owner, collider, onCollide=None):
        super().__init__(owner)
        self.mCollider=collider
        self.mOnCollide=onCollide

    def Update(self, deltaTime):
        self.mCollider.mCenter.x=self.mOwner.mPosition.x
        self.mCollider.mCenter.y=self.mOwner.mPosition.y
    
    def CheckCollision(self, collisionComp):
        if self.mCollider.CheckCollision(collisionComp.mCollider):
            if self.mOnCollide:
                self.mOnCollide(collisionComp.mOwner)
                collisionComp.mOnCollide(self)