import glm

def transform_vector(v, q):
    qv = glm.vec3(q.x, q.y, q.z)
    retVal=glm.vec3(v)
    retVal+=2*glm.cross(qv, glm.cross(qv,v)+q.w*v)
    return retVal

def create_simple_view_proj(width, height):
    # 通过宽度和高度来创建一个正交投影矩阵
    
    matrix=[[ 2.0/width, 0.0, 0.0, 0.0 ],[ 0.0, 2.0/height, 0.0, 0.0 ], [ 0.0, 0.0, 1.0, 0.0 ],[ 0.0, 0.0, 1.0, 1.0 ],]
    matrix = glm.mat4(matrix)
    
    return matrix

def simple_ortho(window_width, window_height):
    # 创建一个正交投影矩阵
    return glm.ortho(0.0, window_width, 0.0, window_height, -1.0, 1.0)

def NearZero(num):
    if glm.abs(num)< 0.001:
        return True
    return False

def Concatenate(q,p):
    retVal=glm.quat()
    qv=glm.vec3(q.x,q.y,q.z)
    pv=glm.vec3(p.x,p.y,p.z)
    newVec=p.w*qv+q.w*pv+glm.cross(pv,qv)
    retVal.x=newVec.x
    retVal.y=newVec.y
    retVal.z=newVec.z
    retVal.w=p.w*q.w-glm.dot(pv,qv)
    #retVal=glm.normalize(retVal)
    return retVal

def CreateLookAt(eye, target, up):
    zaxis=glm.normalize(target-eye)
    xaxis=glm.normalize(glm.cross(up, zaxis))
    yaxis=glm.normalize(glm.cross(zaxis, xaxis))
    trans=glm.vec3()
    trans.x=-glm.dot(xaxis, eye)
    trans.y=-glm.dot(yaxis, eye)
    trans.z=-glm.dot(zaxis, eye)
    
    temp=[
        [xaxis.x, yaxis.x, zaxis.x,0],
        [xaxis.y, yaxis.y, zaxis.y,0],
        [xaxis.z, yaxis.z, zaxis.z, 0],
        [trans.x, trans.y, trans.z, 1],
    ]
    return glm.mat4(temp)

def CreatePerspectiveFOV(fovY, width, height, near, far):
    yScale=glm.cot(fovY/2)
    xScale=yScale*height/width
    temp=[
        [xScale,0,0,0],
        [0,yScale, 0,0],
        [0,0, far/(far-near),1],
        [0,0,-near*far/(far-near),0]
    ]
    return glm.mat4(temp)

class SphereCollider:
    def __init__(self, center, radius):
        self.center = center  # 球体的中心，使用glm.vec3表示
        self.radius = radius  # 球体的半径

    # 检查当前球体是否与另一个球体发生碰撞
    def check_collision(self, other):
        # 计算两个球体中心之间的距离
        distance = glm.length(self.center - other.center)
        
        # 如果两个球体的中心距离小于它们半径之和，则发生碰撞
        return distance < (self.radius + other.radius)