from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import pygame

# 手动定义常量
GL_TEXTURE_MAX_ANISOTROPY_EXT = 0x84FE

# 初始化 Pygame
pygame.init()

# 初始化 OpenGL 上下文
pygame.display.set_mode((800, 600), pygame.DOUBLEBUF | pygame.OPENGL)

# 打开 OpenGL 上下文后再获取扩展
vendor = glGetString(GL_VENDOR)
renderer = glGetString(GL_RENDERER)

# 打印显卡厂商和渲染器信息
print(f"显卡厂商: {vendor.decode('utf-8')}")
print(f"渲染器: {renderer.decode('utf-8')}")

# 获取扩展数量
num_extensions = glGetIntegerv(GL_NUM_EXTENSIONS)

# 遍历所有扩展并检查是否支持各向异性过滤扩展
support_aniso = False
for i in range(num_extensions):
    ext = glGetStringi(GL_EXTENSIONS, i).decode('utf-8')
    if "GL_EXT_texture_filter_anisotropic" in ext:
        support_aniso = True
        break

if support_aniso:
    print("支持各向异性过滤扩展。")
else:
    print("不支持各向异性过滤扩展。")

# 启用 Mipmap 线性渐进过滤
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

# 启用各向异性过滤，设置级别为 16
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAX_ANISOTROPY_EXT, 16)

# 查询最大各向异性过滤级别
# max_aniso = glGetFloatv(GL_MAX_TEXTURE_MAX_ANISOTROPY_EXT)
# print(f"支持的最大各向异性过滤级别: {max_aniso}")
