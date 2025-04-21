from Actor.Tanks.tank_class import Tank
from StateMachine.


class EnemyTank(Tank):
    def __init__(self, game):
        super().__init__(game)
        game.mEnemies.append(self)
        self.mCollisionComp.mOnCollide=self.onCollide
        self.mType='Enemy'
        self.mStateMachine=
    
    def onCollide(self, instigator):
        if instigator.mType=='Cannonball' and instigator.mInstigator!=self:
            self.mHealth-=25
            print('Collide')
            if self.mHealth<=0:
                print('Explode')
                self.mActive=False
        if instigator.mType=='Player' or instigator.mType=='Wall':
            self.mPosition-=self.GetForward()*10