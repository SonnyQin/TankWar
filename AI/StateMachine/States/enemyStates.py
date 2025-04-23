from AI.StateMachine.States.state_class import State
import glm
import Math

class EnemyGlobalState(State):
    def __init__(self):
        super().__init__()
    def Enter(self, owner):
        super().Enter(owner)
    def Execute(self, owner):
        super().Execute(owner)
        #Sense whether the PlayerTank is in attack range
    def Exit(self, owner):
        super().Exit(owner)

    @staticmethod
    def get_instance():
        if EnemyGlobalState._Instance is None:
            EnemyGlobalState._Instance = EnemyGlobalState()
        return EnemyGlobalState._Instance
    _Instance = None

#default
class EnemyDefaultState(State):
    def __init__(self):
        super().__init__()
    def Enter(self, owner):
        super().Enter(owner)
    def Execute(self, owner):
        super().Execute(owner)
        owner.mStateMachine.ChangeState(EnemyAttendState.get_instance())
    def Exit(self, owner):
        super().Exit(owner)

    @staticmethod
    def get_instance():
        if EnemyDefaultState._Instance is None:
            EnemyDefaultState._Instance = EnemyDefaultState()
        return EnemyDefaultState._Instance
    _Instance = None


class EnemyWanderState(State):
    def __init__(self):
        super().__init__()
    def Enter(self, owner):
        super().Enter(owner)
        # TODO must use pathfinder to get to the place
        owner.mSteeringBehaviors.SeekOn()
        wanderPos=owner.GenerateWanderPos()
        owner.mNavigationComp.InitPath(wanderPos)
    def Execute(self, owner):
        super().Execute(owner)
        
        #If already attend the wanderpos, generate a new one
        if owner.mNavigationComp.mIsOnTarget or owner.mNavigationComp.mPathFinder.mUnableToAttend:
            print('Generate new WanderPos')
            wanderPos=owner.GenerateWanderPos()
            print(wanderPos)
            owner.mNavigationComp.mPathFinder.Reset()
            owner.mNavigationComp.InitPath(wanderPos)
            
    def Exit(self, owner):
        super().Exit(owner)
        owner.mSteeringBehaviors.SeekOff()

    @staticmethod
    def get_instance():
        if EnemyWanderState._Instance is None:
            EnemyWanderState._Instance = EnemyWanderState()
        return EnemyWanderState._Instance
    _Instance = None

#When Other Enemy is died, goto that player position for ease
class EnemyAttendState(State):
    def __init__(self):
            super().__init__()
    def Enter(self, owner):
        super().Enter(owner)
        owner.mSteeringBehaviors.SeekOn()
        owner.mNavigationComp.InitPath(glm.vec2(owner.mGame.mPlayerTank.mPosition.xy))
    def Execute(self, owner):
        super().Execute(owner)
    def Exit(self, owner):
        super().Exit(owner)
        owner.mSteeringBehaviors.SeekOff()
    @staticmethod
    def get_instance():
        if EnemyAttendState._Instance is None:
            EnemyAttendState._Instance = EnemyAttendState()
        return EnemyAttendState._Instance
    _Instance = None
    
class EnemyAttackState(State):
    def __init__(self):
            super().__init__()
    def Enter(self, owner):
        super().Enter(owner)
        #owner.mSteeringBehaviors.WanderOn()
        owner.mSteeringBehaviors.SeekOn()
        #owner.mSteeringBehaviors.PursuitOn()
    def Execute(self, owner):
        super().Execute(owner)
    def Exit(self, owner):
        super().Exit(owner)
        #owner.mSteeringBehaviors.WanderOff()
        owner.mSteeringBehaviors.SeekOff()
        #owner.mSteeringBehaviors.PursuitOff()

    @staticmethod
    def get_instance():
        if EnemyAttackState._Instance is None:
            EnemyAttackState._Instance = EnemyAttackState()
        return EnemyAttackState._Instance
    _Instance = None
    
class EnemyDeadState(State):
    def __init__(self):
            super().__init__()
    def Enter(self, owner):
        super().Enter(owner)
        self.mActive=False
        enemies=owner.mGame.mEnemies
        for enemy in enemies:
            enemy.mStateMachine.ChangeState(EnemyAttendState.get_instance())
    def Execute(self, owner):
        super().Execute(owner)
    def Exit(self, owner):
        super().Exit(owner)
        #owner.mSteeringBehaviors.WanderOff()
        owner.mSteeringBehaviors.SeekOff()
        #owner.mSteeringBehaviors.PursuitOff()

    @staticmethod
    def get_instance():
        if EnemyDeadState._Instance is None:
            EnemyDeadState._Instance = EnemyDeadState()
        return EnemyDeadState._Instance
    _Instance = None