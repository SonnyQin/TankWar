from Actor.actor_class import Actor
import glm
import pygame
from Component.spriteComponent_class import SpriteComponent

class HealthBar(Actor):
    def __init__(self, game):
        super().__init__(game)
        self.mSpriteComponent=SpriteComponent(self)
        self.mSpriteComponent.SetTexture(game.mRenderer.GetTexture('Assets/HealthBar.png'))
    def ActorInput(self, keyState):
        super().ActorInput(keyState)
        # if(keyState[pygame.K_1]):
        #     self.mPosition.x+=0.01
        # if(keyState[pygame.K_2]):
        #     self.mPosition.y+=0.01
        # if(keyState[pygame.K_3]):
        #     self.mPosition.z+=0.01
        # if keyState[pygame.K_q]:
        #     self.mRotation.w+=0.1
        #     print(self.mRotation)