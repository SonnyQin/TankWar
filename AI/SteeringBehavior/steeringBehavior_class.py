import glm
import math
import random
import Paras

class BehaviorTypes:
    none = 0x0000
    seek = 0x0002
    pursuit = 0x0004
    wander = 0x0008

class SteeringBehaviors:
    def __init__(self, owner):
        self.mOwner = owner
        self.mSteeringForce = glm.vec2(0, 0)
        self.mTarget = None
        self.mTargetPos = None
        self.mFlag = BehaviorTypes.none
        self.mMaxForce = Paras.EnemyMaxForce
        theta = random.uniform(0, 2 * math.pi)
        self.m_vWanderTarget = glm.vec2(Paras.EnemyWanderRad * math.cos(theta), 
                                        Paras.EnemyWanderRad * math.sin(theta))

    #TODO
    def Seek(self, target_pos):
        # 转换 mOwner.mPosition 为 vec2 (只取 x 和 y)
        owner_pos_2d = glm.vec2(self.mOwner.mPosition.x, self.mOwner.mPosition.y)
        desired_velocity = glm.normalize(target_pos - owner_pos_2d) * Paras.EnemyMaxSpeed
        return desired_velocity - self.mOwner.GetForward().xy*self.mOwner.mMovementComp.mForwardSpeed

    def Pursuit(self, evader):
        # 转换 mOwner.mPosition 和 evader.mPosition 为 vec2
        owner_pos_2d = glm.vec2(self.mOwner.mPosition.x, self.mOwner.mPosition.y)
        evader_pos_2d = glm.vec2(evader.mPosition.x, evader.mPosition.y)

        to_evader = evader_pos_2d - owner_pos_2d
        self.mOwner.mHeading = glm.normalize(evader_pos_2d - owner_pos_2d)
        relative_heading = glm.dot(self.mOwner.mHeading, glm.vec2(0, 1))

        if glm.dot(to_evader, self.mOwner.mHeading) > 0 and relative_heading < -0.95:
            return self.Seek(evader_pos_2d)

        look_ahead_time = 0
        if evader.mMovementComp.mVelocity.length() != 0:
            look_ahead_time = to_evader.length() / evader.mMovementComp.mVelocity.length()

        self.mTargetPos = evader_pos_2d + evader.mMovementComp.mVelocity * look_ahead_time
        return self.Seek(self.mTargetPos)

    def Wander(self):
        jitter_this_time_slice = Paras.WanderJitterPerSec * self.mOwner.mTimeElapsed
        self.m_vWanderTarget.x += random.uniform(-1, 1) * jitter_this_time_slice
        self.m_vWanderTarget.y += random.uniform(-1, 1) * jitter_this_time_slice
        self.m_vWanderTarget = glm.normalize(self.m_vWanderTarget)
        self.m_vWanderTarget *= Paras.EnemyWanderRad

        target = self.m_vWanderTarget + glm.vec2(Paras.WanderDist, 0)
        target_in_world_space = target + glm.vec2(self.mOwner.mPosition.x, self.mOwner.mPosition.y)
        return target_in_world_space - glm.vec2(self.mOwner.mPosition.x, self.mOwner.mPosition.y)

    def on(self, bt):
        return (self.mFlag & bt) == bt

    def SeekOn(self):
        self.mFlag |= BehaviorTypes.seek

    def PursuitOn(self):
        self.mFlag |= BehaviorTypes.pursuit

    def WanderOn(self):
        self.mFlag |= BehaviorTypes.wander

    def SeekOff(self):
        if self.on(BehaviorTypes.seek):
            self.mFlag ^= BehaviorTypes.seek

    def PursuitOff(self):
        if self.on(BehaviorTypes.pursuit):
            self.mFlag ^= BehaviorTypes.pursuit

    def WanderOff(self):
        if self.on(BehaviorTypes.wander):
            self.mFlag ^= BehaviorTypes.wander
            
    #TODO
    def AccumulateForce(self, RT, force_to_add):
        magnitude_so_far = glm.length(RT)
        magnitude_remaining = self.mMaxForce - magnitude_so_far
        if magnitude_remaining <= 0.0:
            return False

        magnitude_to_add = glm.length(force_to_add)

        if magnitude_to_add < magnitude_remaining:
            RT += force_to_add
        else:
            RT += glm.normalize(force_to_add) * magnitude_remaining

        return True

    def SumForces(self):
        force = glm.vec2(0, 0)

        if self.on(BehaviorTypes.seek):
            force += self.Seek(self.mTargetPos)
            if not self.AccumulateForce(self.mSteeringForce, force):
                return self.mSteeringForce

        if self.on(BehaviorTypes.pursuit) and self.mTarget:
            force += self.Pursuit(self.mTarget)
            if not self.AccumulateForce(self.mSteeringForce, force):
                return self.mSteeringForce

        if self.on(BehaviorTypes.wander):
            force += self.Wander()
            if not self.AccumulateForce(self.mSteeringForce, force):
                return self.mSteeringForce

        return self.mSteeringForce

    def Calculate(self):
        self.mSteeringForce = self.SumForces()
        self.mSteeringForce = glm.clamp(self.mSteeringForce, -Paras.EnemyMaxForce, Paras.EnemyMaxForce)
        return self.mSteeringForce
