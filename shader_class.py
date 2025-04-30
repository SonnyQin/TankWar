from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import glm

#Inspired by Game Programming in C++: Creating 3D Games

class Shader:
    def __init__(self):
        self.shader_program = None
        self.vertex_shader = None
        self.fragment_shader = None

    def Load(self, vert_name, frag_name):
        # 读取着色器代码
        with open(vert_name, 'r') as f:
            vertex_shader_code = f.read()
        
        with open(frag_name, 'r') as f:
            fragment_shader_code = f.read()

        # 编译着色器
        self.vertex_shader = self.CompileShader(vertex_shader_code, GL_VERTEX_SHADER)
        self.fragment_shader = self.CompileShader(fragment_shader_code, GL_FRAGMENT_SHADER)

        # 创建着色器程序并链接
        self.shader_program = glCreateProgram()
        glAttachShader(self.shader_program, self.vertex_shader)
        glAttachShader(self.shader_program, self.fragment_shader)
        glLinkProgram(self.shader_program)

        # 检查链接状态
        if not self.IsValidProgram():
            return False
        return True

    def UnLoad(self):
        if self.shader_program:
            glDeleteProgram(self.shader_program)
        if self.vertex_shader:
            glDeleteShader(self.vertex_shader)
        if self.fragment_shader:
            glDeleteShader(self.fragment_shader)
            
    def CompileShader(self, shader_code, shader_type):
        # 创建着色器对象
        shader = glCreateShader(shader_type)
        glShaderSource(shader, shader_code)
        glCompileShader(shader)

        # 检查是否编译成功
        if not self.IsCompiled(shader):
            return None
        return shader

    def IsCompiled(self, shader):
        # 查询编译状态
        compile_status = glGetShaderiv(shader, GL_COMPILE_STATUS)
        if compile_status != GL_TRUE:
            # 获取错误信息
            error_message = glGetShaderInfoLog(shader)
            print(f"Shader Compile Failed:\n{error_message}")
            return False
        return True

    def IsValidProgram(self):
        # 查询链接状态
        link_status = glGetProgramiv(self.shader_program, GL_LINK_STATUS)
        if link_status != GL_TRUE:
            # 获取链接错误信息
            error_message = glGetProgramInfoLog(self.shader_program)
            print(f"Program Link Failed:\n{error_message}")
            return False
        return True

    def SetActive(self):
        glUseProgram(self.shader_program)


    def SetMatrixUniform(self, name, matrix):
        location = glGetUniformLocation(self.shader_program, name)
        glUniformMatrix4fv(location, 1, GL_TRUE, glm.value_ptr(matrix))

    def SetVectorUniform(self, name, vector):
        location = glGetUniformLocation(self.shader_program, name)
        glUniform3fv(location, 1, glm.value_ptr(vector))

    def SetFloatUniform(self, name, value):
        location = glGetUniformLocation(self.shader_program, name)
        glUniform1f(location, value)