import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from texture_class import Texture
from mesh_class import Mesh
from shader_class import Shader
from vertexArray_class import VertexArray
import Math
import glm
import sys
import Paras

import numpy as np

class Renderer:
    def __init__(self, game, screen_width, screen_height):
        self.mGame=game
        self.mScreenWidth = screen_width
        self.mScreenHeight = screen_height
        self.mTextures={}
        self.mMeshes={}
        self.mShaders={}
        #calculate by the camera
        self.mView=None
        self.mProjection=glm.perspectiveFov(glm.radians(70), screen_width, screen_height, 25, 100000)
        #self.mPP=glm.perspectiveFov(glm.radians(70), screen_width, screen_height, 0.1, 100)

        self.mMeshComponents=[]
        self.mSpriteComponents=[]

        self.mSpriteVerts=None
        self.mSpriteShader=None
        
        self.mSimpleShader=None
        
        self.mHorizontalProj=None

    def Initialize(self):
        # Initialize pygame
        pygame.init()

        # Set up the OpenGL context attributes
        pygame.display.set_mode((self.mScreenWidth, self.mScreenHeight), pygame.DOUBLEBUF | pygame.OPENGL)
        
        pygame.display.gl_set_attribute(pygame.GL_SWAP_CONTROL, 1)  # 启用 V-Sync

        # Set OpenGL viewport size
        glViewport(0, 0, self.mScreenWidth, self.mScreenHeight)

        # Initialize shaders (assuming we have a function `load_shaders` for this)
        if not self.LoadShaders():
            print("Failed to load shaders.")
            return False
        
        self.CreateSpriteVerts()
        
        glEnable(GL_BLEND)  # 开启混合
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # 混合模式
        
        # debug_window = pygame.display.set_mode((800, 600))
        # pygame.display.set_caption("Pathfinding Debug")
        
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH | GLUT_MULTISAMPLE)
        
        return True

    def LoadShaders(self):
        self.mSpriteShader=Shader()
        self.mSpriteShader.Load('Shaders/Sprite.vert', 'Shaders/Sprite.frag')
        self.mSpriteShader.SetActive()
        self.mHorizontalProj=Math.create_simple_view_proj(Paras.WINDOWWIDTH, Paras.WINDOWHEIGHT)
        self.mSpriteShader.SetMatrixUniform('uViewProj', self.mHorizontalProj)

        # self.mSimpleShader=Shader()
        # self.mSimpleShader.Load('Shaders/BasicShader.vert', 'Shaders/BasicShader.frag')
        # self.mSimpleShader.SetActive()
        
        # self.mFancyShader=Shader()
        # self.mFancyShader.Load('Shaders/MetallicBlinnPhongShader.vert', 'Shaders/MetallicBlinnPhongShader.frag')
        # self.mFancyShader.SetActive()
        
        return True
    
    def GetTexture(self, file_name):
        # 获取缓存中的纹理，如果没有则加载
        if file_name in self.mTextures:
            return self.mTextures[file_name]
        
        tex = Texture()
        if tex.Load(file_name):
            self.mTextures[file_name] = tex
            return tex
        else:
            return None

    def GetMesh(self, file_name):
        # 获取缓存中的网格，如果没有则加载
        if file_name in self.mMeshes:
            return self.mMeshes[file_name]
        
        m = Mesh()
        if m.Load(file_name, self):
            self.mMeshes[file_name] = m
            return m
        else:
            return None
    
    def GetShader(self, shader_name):
        if shader_name in self.mShaders:
            return self.mShaders[shader_name]
        
        s= Shader()
        if s.Load('Shaders/'+shader_name+'.vert', 'Shaders/'+shader_name+'.frag'):
            self.mShaders[shader_name]=s
            return s
        else:
            return None
    
    def AddSprite(self, sprite):
        self.mSpriteComponents.append(sprite)
        self.mSpriteComponents.sort(key=lambda sp: sp.mDrawOrder)

    def RemoveSprite(self, sprite):
        try:
            self.mSpriteComponents.remove(sprite)
        except:
            pass
        self.mSpriteComponents.sort(key=lambda sprite: sprite.mDrawOrder)
    
    def CreateSpriteVerts(self):
        vertices=[
		-0.5, 0.5, 0., 0., 0., 0.0, 0., 0.,
		0.5, 0.5, 0., 0., 0., 0.0, 1., 0.,
		0.5,-0.5, 0., 0., 0., 0.0, 1., 1.,
		-0.5,-0.5, 0., 0., 0., 0.0, 0., 1.
        ]

        indices = [0, 1, 2, 
                   2, 3, 0]
        self.mSpriteVerts = VertexArray(vertices, 4, indices, 6);

    def Draw(self):
        #glDisable(GL_CULL_FACE)  # 禁用背面剔除
        # Render the scene (clear the screen and render)
        glClearColor(0.5,0,0,1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        #Draw Meshes
        glEnable(GL_DEPTH_TEST)
        glDisable(GL_BLEND)
        
        self.mGame.mPlayerTank.mTorret.ComputeWorldTransform()
        self.mGame.mPlayerTank.mChassis.ComputeWorldTransform()
        
        for camera in self.mGame.mCameras:
            camera.Update()
        
        mainCamera=self.mGame.mCameras[0]

        
        for mc in self.mMeshComponents:
            if mc.mOwner.mActive:
                mc.mMesh.mShader.SetActive()
                mc.mMesh.mShader.SetMatrixUniform("uViewProj", self.mProjection*self.mView)
                mc.mMesh.mShader.SetVectorUniform('uCameraPos', mainCamera.mPosition)
                mc.mMesh.mShader.SetVectorUniform('uAmbientLight', self.mGame.mAmbientLight)
                dirLight=self.mGame.mDirectionalLight
                mc.mMesh.mShader.SetVectorUniform('uDirLight.mDirection', dirLight.mDirection)
                mc.mMesh.mShader.SetVectorUniform('uDirLight.mDiffuseColor', dirLight.mDiffuseColor)
                mc.mMesh.mShader.SetVectorUniform('uDirLight.mSpecColor', dirLight.mSpecColor)
                mc.Draw()
            #print(glGetError())
        
        # #Draw Sprites
        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendEquationSeparate(GL_FUNC_ADD, GL_FUNC_ADD)
        glBlendFuncSeparate(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_ONE, GL_ZERO)
        
        self.mSpriteShader.SetActive()
        # self.mSpriteShader.SetMatrixUniform('uViewProj', self.mHorizontalProj)
        #print(glGetError())
        self.mSpriteVerts.SetActive()
        #print(glGetError())
        

        
        for sc in self.mSpriteComponents:
            if sc.mOwner.mActive:
                sc.Draw(self.mSpriteShader)
            #print(glGetError())
        
        glUseProgram(0)
        
        #Draw score
        render_text('Score: ' +str(self.mGame.mScore), (75, 500))  # 渲染文本到屏幕上
        #Draw health
        render_text('Health: '+str(self.mGame.mPlayerTank.mHealth), (475,500))
        
        if not self.mGame.mPlayerTank.mActive:
            render_text('Game Over', (290,350))
        
        pygame.display.flip()
    
    # def Draw(self):
    #     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # 清除颜色和深度缓存

    #     # 渲染文本
    #     render_text("Hello, PyOpenGL!", (10, 10))  # 渲染文本到屏幕上

    #     pygame.display.flip()  # 刷新显示
    #     pygame.time.wait(10)  # 控制帧率



# 渲染文本的函数
def render_text(text, position):
    font = pygame.font.Font('Assets/Corna/Corna/Corna-2.otf', 36)  # 创建一个字体对象，字号为36
    
    # 渲染文本为表面
    text_surface = font.render(text, True, (0, 204, 255))  # 红色文本
    text_data = pygame.image.tostring(text_surface, "RGBA", True)

    # 创建 OpenGL 纹理
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, text_surface.get_width(), text_surface.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # 设置 2D 正交投影，适用于文本渲染
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, 800, 600, 0, -1, 1)  # 假设窗口大小是 800x600

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # 启用 2D 纹理
    glEnable(GL_TEXTURE_2D)

    # 渲染时翻转 y 坐标，确保文本上下正常
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex2f(position[0], 600 - position[1])  # 翻转y坐标
    glTexCoord2f(1, 0)
    glVertex2f(position[0] + text_surface.get_width(), 600 - position[1])  # 翻转y坐标
    glTexCoord2f(1, 1)
    glVertex2f(position[0] + text_surface.get_width(), 600 - (position[1] + text_surface.get_height()))  # 翻转y坐标
    glTexCoord2f(0, 1)
    glVertex2f(position[0], 600 - (position[1] + text_surface.get_height()))  # 翻转y坐标
    glEnd()

    glDisable(GL_TEXTURE_2D)

    # 恢复投影和模型视图矩阵
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()

    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()