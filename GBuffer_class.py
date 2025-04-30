import OpenGL.GL as gl
from OpenGL.GL import shaders
import numpy as np
from texture_class import Texture

#Unuse 
#Generate by ChatGPT
class GBuffer:
    def __init__(self):
        self.bufferID = 0
        self.textures = []

    def create(self, width, height):
        # 创建帧缓冲
        self.bufferID = gl.glGenFramebuffers(1)
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.bufferID)

        # 创建深度缓冲
        depthBuffer = gl.glGenRenderbuffers(1)
        gl.glBindRenderbuffer(gl.GL_RENDERBUFFER, depthBuffer)
        gl.glRenderbufferStorage(gl.GL_RENDERBUFFER, gl.GL_DEPTH_COMPONENT, width, height)
        gl.glFramebufferRenderbuffer(gl.GL_FRAMEBUFFER, gl.GL_DEPTH_ATTACHMENT, gl.GL_RENDERBUFFER, depthBuffer)

        # 创建G-buffer纹理
        num_textures = 3  # 假设有3个纹理，分别存储位置、法线、颜色
        for i in range(num_textures):
            tex = Texture()
            tex.create_for_rendering(width, height, gl.GL_RGB32F)
            self.textures.append(tex)

            gl.glFramebufferTexture(gl.GL_FRAMEBUFFER, gl.GL_COLOR_ATTACHMENT0 + i, tex.get_texture_id(), 0)

        # 设置绘制目标为多个颜色附件
        attachments = [gl.GL_COLOR_ATTACHMENT0 + i for i in range(num_textures)]
        gl.glDrawBuffers(len(attachments), np.array(attachments, dtype=np.uint32))

        # 检查帧缓冲状态
        if gl.glCheckFramebufferStatus(gl.GL_FRAMEBUFFER) != gl.GL_FRAMEBUFFER_COMPLETE:
            self.destroy()
            return False

        return True

    def destroy(self):
        gl.glDeleteFramebuffers(1, [self.bufferID])
        for tex in self.textures:
            tex.unload()

    def get_texture(self, texture_type):
        if len(self.textures) > 0:
            return self.textures[texture_type]
        return None

    def set_textures_active(self):
        for i, tex in enumerate(self.textures):
            tex.set_active(i)
