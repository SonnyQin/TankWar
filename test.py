import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

# 渲染文本的函数
def render_text(text, position):
    font = pygame.font.Font(None, 36)  # 创建一个字体对象，字号为36
    
    # 渲染文本为表面
    text_surface = font.render(text, True, (255, 0, 0))  # 红色文本
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

# 初始化 pygame 和 OpenGL
def init():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    
    glClearColor(0.0, 0.0, 0.0, 1.0)  # 设置背景色为黑色
    glEnable(GL_BLEND)  # 开启混合
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # 混合模式

# 主渲染循环
def main():
    init()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # 清除颜色和深度缓存

        # 渲染文本
        render_text("Hello, PyOpenGL!", (10, 10))  # 渲染文本到屏幕上

        pygame.display.flip()  # 刷新显示
        pygame.time.wait(10)  # 控制帧率

# 启动程序
if __name__ == "__main__":
    main()
