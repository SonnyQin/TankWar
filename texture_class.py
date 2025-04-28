from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import pygame
from PIL import Image
import numpy as np

GL_TEXTURE_MAX_ANISOTROPY_EXT = 0x84FE

class Texture:
    def __init__(self):
        self.mTextureID =0
        self.mWidth = 0
        self.mHeight = 0

    def Load(self, file_name):
        # 使用PIL加载图片
        try:
            image = Image.open(file_name)
        except Exception as e:
            print(f"Failed to load image {file_name}: {e}")
            return False
        
        # 将图片转换为RGBA格式，并获取数据
        image = image.convert("RGBA")
        image_data = np.array(image)

        # 获取图片的宽度、高度
        self.mWidth, self.mHeight = image.size

        # 生成纹理ID并绑定纹理
        self.mTextureID=glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.mTextureID)
        
        glEnable(GL_MULTISAMPLE)
        # 上传纹理数据
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.mWidth, self.mHeight, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)

        # 设置纹理参数（线性过滤）
        # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        # # 生成 Mipmap
        # glGenerateMipmap(GL_TEXTURE_2D)
        
        # 线性 Mipmap + 各向异性过滤
        # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)  # 适合近距离和远距离
        # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)  # 放大时使用线性过滤
        # 生成 Mipmap（如果没有生成）
        #glGenerateMipmap(GL_TEXTURE_2D)
        
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)  # 使用 Mipmap 的线性渐进过滤
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)  # 使用线性过滤
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAX_ANISOTROPY_EXT, 16)
        glGenerateMipmap(GL_TEXTURE_2D)

        return True

    def Unload(self):
        # 删除纹理
        glDeleteTextures(1, [self.mTextureID])

    def SetActive(self):
        # 绑定纹理
        glBindTexture(GL_TEXTURE_2D, self.mTextureID)
