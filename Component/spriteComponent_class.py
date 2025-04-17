from OpenGL.GL import *
from Component.component_class import Component
import glm

class SpriteComponent (Component):
    def __init__(self, owner, draw_order=0):
        super().__init__(owner)
        self.mTexture = None
        self.mDrawOrder = draw_order
        self.mTexWidth = 0
        self.mTexHeight = 0
        owner.mGame.mRenderer.AddSprite(self)

    def Draw(self, shader):
        if self.mTexture:
            # Scale the quad by the width/height of texture
            scale_mat = glm.scale(glm.mat4(1.0), glm.vec3(self.mTexWidth, self.mTexHeight, 1.0))

            # Calculate the world transform
            world = scale_mat * self.mOwner.mWorldTransform

            # Set world transform
            shader.SetMatrixUniform("uWorldTransform", world)

            # Set current texture
            self.mTexture.SetActive()
            
            # r=world*self.mOwner.mGame.mRenderer.mHorizontalProj
            # print(r)

            # Draw quad (assuming index buffer has 6 indices for a quad)
            glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

    def SetTexture(self, texture):
        self.mTexture = texture
        # Set width/height
        self.mTexWidth = texture.mWidth
        self.mTexHeight = texture.mHeight
