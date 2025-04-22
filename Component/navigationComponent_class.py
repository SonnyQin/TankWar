from Component.component_class import Component
from gameMap_class import GameMap
from AI.PathFinding.pathFinder_class import PathFinder
import glm


#Use for AI to go to the target position
#Remember to set Owner's steering behavior on, including seek, pursuit, etc, to  make movement
class NavigationComponent(Component):
    def __init__(self, owner, updateOrder=-1):
        super().__init__(owner, updateOrder)
        self.mPathFinder=PathFinder(owner.mGame.mGameMap)
        self.mPathProcedure=None
        self.mTargetPos=None
        self.mIsFindingPath=False
        self.mIsOnTarget=False
    
    def InitPath(self, targetPos):
        self.mIsFindingPath=True
        self.mIsOnTarget=False
        self.mTargetPos=targetPos
        self.mPathFinder.StartFindPath(GameMap.GetMapLocation(self.mOwner.mPosition.x, self.mOwner.mPosition.y),
                                GameMap.GetMapLocation(self.mTargetPos.x, self.mTargetPos.y))
        
    
    def Update(self, deltatime):
        super().Update(deltatime)
        
        #If currently is finding the path, currently one step for each frame
        if self.mIsFindingPath:
            r=self.mPathFinder.FindPathStep()
            if r:
                self.mIsFindingPath=False
                self.mPathProcedure=PathFinder.IndexToPosition(self.mTargetPos)
        
        #If currently not finding the path and the path has already found
        #Just follow the path
        if not self.mIsFindingPath and self.mPathProcedure and not self.mIsOnTarget:
            currentNode=self.mPathProcedure.GetCurrentNode()
            #If it does not have a target pos
            if not self.mOwner.mSteeringBehaviors.mTargetPos:
                self.mOwner.mSteeringBehaviors.mTargetPos=currentNode
            else:
                #Check whether already get to that position, stop first, and then go to another position
                if glm.length(self.mPosition.xy - self.mTargetPos.xy) < 10:
                    self.mMovementComp.mAngularSpeed=0
                    self.mChassis.mMovementComp.mAngularSpeed=0
                    self.mMovementComp.mForwardSpeed=0
                    self.mChassis.mMovementComp.mForwardSpeed=0
                    #Check whether finish the path
                    if self.mPathProcedure.NextNode():
                        #Reset target to the next node
                        self.mOwner.mSteeringBehaviors.mTargetPos=currentNode
                    else:
                        #Finished
                        self.mIsOnTarget=True