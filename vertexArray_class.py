import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class VertexArray:
    def __init__(self, verts, numVerts, indices, numIndices):
        self.mNumVerts = numVerts
        self.mNumIndices = numIndices
        
        # 创建顶点数组对象 (VAO)
        self.mVertexArray = glGenVertexArrays(1)
        glBindVertexArray(self.mVertexArray)

        # 创建顶点缓冲区对象 (VBO)
        self.mVertexBuffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.mVertexBuffer)
        # 为顶点缓冲区上传数据
        glBufferData(GL_ARRAY_BUFFER, numVerts * 8 * 4, np.array(verts, dtype=np.float32), GL_STATIC_DRAW)

        # 创建索引缓冲区对象 (IBO)
        self.mIndexBuffer = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.mIndexBuffer)
        # 为索引缓冲区上传数据
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, numIndices * 4, np.array(indices, dtype=np.uint32), GL_STATIC_DRAW)

        # 设置顶点属性
        # 位置：3个浮点数
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(0))

        # 法线：3个浮点数
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(3 * 4))

        # 纹理坐标：2个浮点数
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(6 * 4))
    
    def SetActive(self):
        glBindVertexArray(self.mVertexArray)
