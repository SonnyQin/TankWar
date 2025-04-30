from Component.component_class import Component
import Math
import glm
import Paras


#Customized
#Use for AI to sense the Player
#Sensation include aural and visual
#Fire will cause an aural sense
#If it sense the playertank, change into enemy attack state
#TODO
#Abandon Memory system and check obstacles when checking visual, just make it easy
class SenseComponent(Component):
    def __init__(self, owner, updateOrder=0):
        super().__init__(owner, updateOrder)
        self.mIsSensed=False
        
    #Must update after statemachine
    def Update(self, deltatime):
        super().Update(deltatime)
        
    #Call back function for action that may cause change in sense
    def CallVisual(self,player):
        if self.mIsSensed:
            return
        pos=player.mPosition
        EyeToTarget=pos-self.mOwner.mPosition
        if glm.length(EyeToTarget) > Paras.EnemySight:
            return
        EyeToTarget=glm.normalize(EyeToTarget)
        #TODO have an error, but I am too lazy
        TorretForward=-self.mOwner.mTorret.GetForward()
        angle=Math.AngleBetweenVectors(EyeToTarget, TorretForward)
        if angle<Paras.EnemyPOV/2 and self.See(player):
            self.mIsSensed=True
    
    def CallAural(self, player):
        if self.mIsSensed:
            return
        pos=player.mPosition
        if glm.length(pos-self.mOwner.mPosition)<Paras.EnemyHearingRad:
            self.mIsSensed=True
    
    #The target of this function is to test whether the enemy is able to shoot at the player tank
    #Therefore, no need to use sub steps test for the FOV
    #Inspired by ChatGPT
    def See(self, player):
        obstacles=self.mOwner.mGame.mObstacles
        for obstacle in obstacles:
            if obstacle.mCollisionComp.mCollider.CheckCollisionWithRay(
                self.mOwner.mPosition, glm.normalize(player.mPosition-self.mOwner.mPosition),
                glm.length(player.mPosition-self.mOwner.mPosition)):
                return False
        return True