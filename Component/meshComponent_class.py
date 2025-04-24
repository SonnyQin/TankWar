from Component.component_class import Component
from mesh_class import Mesh
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class MeshComponent(Component):
    def __init__(self, owner, updateOrder=0):
        super().__init__(owner,updateOrder)
        self.mMesh=None
        self.mTextureIndex=0
        self.mOwner.mGame.mRenderer.mMeshComponents.append(self)
    
    def Draw(self):
        if self.mMesh:
            t=self.mMesh.mTextures[self.mTextureIndex]
            t.SetActive()
            va=self.mMesh.mVertexArray
            va.SetActive()
            shader=self.mMesh.mShader
            shader.SetActive()
            shader.SetMatrixUniform("uWorldTransform", self.mOwner.mWorldTransform)
            shader.SetFloatUniform("uSpecPower", self.mMesh.mSpecPower)
            shader.SetFloatUniform('uMetallic', self.mMesh.mMetallic)
            
            # self.mMesh.mShader.SetMatrixUniform("uViewProj", self.mOwner.mGame.mRenderer.mProjection*self.mOwner.mGame.mRenderer.mView)
            #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)  # 切换到线框模式
            glDrawElements(GL_TRIANGLES, va.mNumIndices, GL_UNSIGNED_INT, ctypes.c_void_p(0))
