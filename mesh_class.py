import json
import os
from vertexArray_class import VertexArray
import glm

class Mesh:
    def __init__(self):
        self.mSpecPower=0
        self.mMetallic=0
        self.mTextures=[]
        self.mVertexArray=None
        self.mShader=None
        
        
    def Load(self, fileName, renderer):
            # 读取文件
        if not os.path.exists(fileName):
            print(f"File not found: Mesh {fileName}")
            return False
        
        with open(fileName, 'r') as file:
            contents = file.read()
        
        try:
            doc = json.loads(contents)
        except json.JSONDecodeError:
            print(f"Mesh {fileName} is not valid JSON")
            return False

        # 检查版本
        ver = doc.get("version", None)
        if ver != 1:
            print(f"Mesh {fileName} not version 1")
            return False

        shaderName = doc.get("shader", "")
        self.mShader=renderer.GetShader(shaderName)

        # 加载纹理
        textures = doc.get("textures", [])
        if not textures:
            print(f"Mesh {fileName} has no textures, there should be at least one")
            return False
        
        self.mSpecPower = float(doc.get("specularPower", 0.0))
        self.mMetallic = float(doc.get("metallic", 0.0))

        for tex_name in textures:
            tex = renderer.GetTexture(tex_name)
            if tex is None:
                tex = renderer.GetTexture("Assets/Default.png")
            self.mTextures.append(tex)

        # 加载顶点数据
        verts_json = doc.get("vertices", [])
        if not verts_json:
            print(f"Mesh {fileName} has no vertices")
            return False

        vertices = []
        self.radius = 0.0
        for vert in verts_json:
            if len(vert) != 8:
                print(f"Unexpected vertex format for {fileName}")
                return False

            # pos = glm.vec3(vert[0], vert[1], vert[2])
            # self.radius = max(self.radius, pos.x ** 2 + pos.y ** 2 + pos.z ** 2)

            vertices.extend(vert)
        
        # self.radius = sqrt(self.radius)

        # 加载索引数据
        ind_json = doc.get("indices", [])
        if not ind_json:
            print(f"Mesh {fileName} has no indices")
            return False

        indices = []
        for ind in ind_json:
            if len(ind) != 3:
                print(f"Invalid indices for {fileName}")
                return False
            indices.extend(ind)

        # 创建顶点数组
        self.mVertexArray = VertexArray(vertices, len(vertices) // 8, indices, len(indices))
        return True