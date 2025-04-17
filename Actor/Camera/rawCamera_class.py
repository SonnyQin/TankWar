from Actor.Camera.cameraActor_class import CameraActor
from Component.movementComponent_class import MovementComponent
import math
import pygame

class RawCamera(CameraActor):
    def __init__(self, game):
        super().__init__(game)
        self.mc=MovementComponent(self)
    
    def UpdateActor(self, deltatime):
        super().UpdateActor(deltatime)
    
    def ActorInput(self, keyState):
        super().ActorInput(keyState)
        forwardSpeed=0
        angularSpeed=0
        
        if(keyState[pygame.K_w]):
            forwardSpeed+=100
        if(keyState[pygame.K_s]):
            forwardSpeed-=100
        if(keyState[pygame.K_a]):
            angularSpeed-=math.pi
        if(keyState[pygame.K_d]):
            angularSpeed+=math.pi
            
        self.mc.mForwardSpeed=forwardSpeed
        self.mc.mAngularSpeed=angularSpeed
    