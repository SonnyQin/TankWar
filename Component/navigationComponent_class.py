from Component.component_class import Component
from gameMap_class import GameMap
from AI.PathFinding.pathFinder_class import PathFinder, PathProcedure
import glm


#Use for AI to go to the target position
#Remember to set Owner's steering behavior on, including seek, pursuit, etc, to  make movement
class NavigationComponent(Component):
    def __init__(self, owner, updateOrder=-1):
        super().__init__(owner, updateOrder)
        self.mPathFinder=PathFinder(owner.mGame.mGameMap.mMap)
        self.mPathProcedure=None
        self.mTargetPos=None
        self.mIsFindingPath=False
        self.mIsOnTarget=False
    
    def InitPath(self, targetPos):
        self.mPathProcedure=None
        self.mTargetPos=targetPos
        self.mIsFindingPath=True
        self.mIsOnTarget=False
        startLoc=GameMap.GetMapLocation(self.mOwner.mPosition.x, self.mOwner.mPosition.y)
        goalLoc=GameMap.GetMapLocation(self.mTargetPos.x, self.mTargetPos.y)
        self.mPathFinder.StartFindPath(startLoc,goalLoc)
        print(self.mOwner.mGame.mGameMap.mMap)
        print('Start calculate path', startLoc, goalLoc)
        
    
    def Update(self, deltatime):
        super().Update(deltatime)
        
        #If currently is finding the path, currently one step for each frame
        if self.mIsFindingPath:
            print('Calculating path')
            r=self.mPathFinder.FindPathStep()
            if r:
                print('Path calculated')
                self.mIsFindingPath=False
                self.mPathProcedure=PathProcedure(PathFinder.IndexToPosition(r,self.mTargetPos))
                #print(self.mOwner.mPosition.x, self.mOwner.mPosition.y)
                print(self.mPathProcedure.mPath)
            #Unable to get to the position
            if r==False:
                self.mPathProcedure=None
                self.mTargetPos=None
                self.mIsFindingPath=False
                self.mIsOnTarget=False
                return
        
        #If currently not finding the path and the path has already found
        #Just follow the path
        if not self.mIsFindingPath and self.mPathProcedure and not self.mIsOnTarget:
            currentNode=self.mPathProcedure.GetCurrentNode()
            #If it does not have a target pos
            if not self.mOwner.mSteeringBehaviors.mTargetPos:
                self.mOwner.mSteeringBehaviors.mTargetPos=currentNode
            else:
                #print(glm.length(self.mOwner.mPosition.xy - currentNode))
                #Check whether already get to that position, stop first, and then go to another position
                if glm.length(self.mOwner.mPosition.xy - currentNode) < 10:
                    self.mOwner.mMovementComp.mAngularSpeed=0
                    self.mOwner.mMovementComp.mForwardSpeed=0
                    print('Attend a Node')
                    #Check whether finish the path
                    if self.mPathProcedure.NextNode():
                        #Reset target to the next node
                        self.mOwner.mSteeringBehaviors.mTargetPos=self.mPathProcedure.GetCurrentNode()
                        print(' ')
                    else:
                        #Finished
                        self.mIsOnTarget=True
                        self.mOwner.mSteeringBehaviors.mTargetPos=None
                        print('On Target')