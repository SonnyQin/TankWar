import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

#Inspired by Game Programming in C++: Creating 3D Games

class VertexArray:
    def __init__(self, verts, numVerts, indices, numIndices):
        self.mNumVerts = numVerts
        self.mNumIndices = numIndices
        
        self.mVertexArray = glGenVertexArrays(1)
        glBindVertexArray(self.mVertexArray)

        self.mVertexBuffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.mVertexBuffer)
        glBufferData(GL_ARRAY_BUFFER, numVerts * 8 * 4, np.array(verts, dtype=np.float32), GL_STATIC_DRAW)

        self.mIndexBuffer = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.mIndexBuffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, numIndices * 4, np.array(indices, dtype=np.uint32), GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(3 * 4))

        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(6 * 4))
    
    def SetActive(self):
        glBindVertexArray(self.mVertexArray)
