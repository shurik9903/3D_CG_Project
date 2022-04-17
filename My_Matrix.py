from turtle import distance
from My_Vectors import *
from math import cos, radians, sin, tan

import numpy as np

class Matrix_Work():
    def __init__(self) -> None:
        pass

    def Projection2D(self, vec3d:Vector3D, view:str = 'proj') -> Vector2D:
        z = 1
        distance = 140

        if view == 'orto':
            z = 1 / (distance - vec3d.z) if (distance - vec3d.z) else 0

        v = np.array([vec3d.x, vec3d.y, vec3d.z])
        m = np.array([[z, 0, 0], [0, z, 0]])
        v = m.dot(v)
        
        return Vector2D(*v)

    def Mirror2DAxis(self, vec2d:Vector2D, x:bool = False, y:bool = False) -> Vector2D:
        x = -1 if x else 1
        y = -1 if y else 1

        v = np.array([vec2d.x, vec2d.y])
        m = np.array([[x, 0],[0, y]])
        return Vector2D(*v.dot(m))

    def Mirror3DAxis(self, vec3d:Vector3D, x:bool = False, y:bool = False, z:bool = False) -> Vector3D:
        x = -1 if x else 1
        y = -1 if y else 1
        z = -1 if z else 1

        v = np.array([vec3d.x, vec3d.y, vec3d.z])
        m = np.array([[x, 0, 0],[0, y, 0], [0, 0, z]])
        return Vector3D(*v.dot(m))
    
    def Mirror2DAxisArray(self, Array:list[Vector2D], x:bool = False, y:bool = False) -> list:
        return [self.Mirror2DAxis(i, x, y) for i in Array]

    def Mirror3DAxisArray(self, Array:list[Vector3D], x:bool = False, y:bool = False, z:bool = False) -> list:
        return [self.Mirror2DAxis(i, x, y, z) for i in Array]

    def Rotation2DAlf(self, vec2d:Vector2D, alf = 0) -> Vector2D:
        alf = radians(alf)
        v = np.array([vec2d.x, vec2d.y])

        #m = np.array([[cos(alf), -sin(alf)],[sin(alf), cos(alf)]]) #Стандартный алгоритм вращения

        a = np.array([[1, -tan(alf/2)],[0, 1]])
        b = np.array([[1, 0],[sin(alf), 1]])
        c = np.array([[1, -tan(alf/2)],[0, 1]])

        v = v.dot(a)
        v = v.dot(b)
        v = v.dot(c)

        return Vector2D(*(v.astype(int)))
        
    def Rotation3DAlf(self, vec3d:Vector3D, alf = 0,  Axis:str = 'x') -> Vector3D:
        alf = radians(alf)

        v = np.array([vec3d.x, vec3d.y, vec3d.z])

        if Axis == 'x':
            m = np.array([[1, 0, 0],
                          [0, cos(alf), -sin(alf)], 
                          [0, sin(alf),  cos(alf)]])
        if Axis == 'y':
            m = np.array([[cos(alf), 0, sin(alf)],
                          [0, 1, 0], 
                          [-sin(alf), 0,  cos(alf)]])
        if Axis == 'z':
            m = np.array([[cos(alf), -sin(alf), 0],
                          [sin(alf), cos(alf), 0], 
                          [0, 0, 1]])
        
        return Vector3D(*v.dot(m))

    def Rotation2DAlfArray(self, Array:list[Vector3D], alf = 0) -> list[Vector3D]:
        return [self.Rotation2DAlf(i, alf) for i in Array]
        

    def Rotation3DAlfArray(self, Array:list[Vector3D], alf = 0,  Axis:str = 'x') -> list:
        return [self.Rotation3DAlf(i, alf, Axis) for i in Array]

    def Move2D(self, vec2d:Vector2D, Pvec2d:Vector2D, center:Vector2D = Vector2D(0,0)) -> Vector2D:
        new_x = center.x - vec2d.x
        new_y = center.y - vec2d.y

        new_x = Pvec2d.x + new_x
        new_y = Pvec2d.y + new_y

        return Vector2D(new_x,new_y)

    def Translate2D(self, vec2d:Vector2D, Pvec2d:Vector2D) -> Vector2D:
        v = np.array([vec2d.x, vec2d.y, 1]) 
        m = np.array([[1, 0, 0],[0, 1, 0],[Pvec2d.x, Pvec2d.y, 1]])
        v = v.dot(m)
        return Vector2D(*v)

    def Translate3D(self, vec3d:Vector3D, Pvec3d:Vector3D) -> Vector3D:
        v = np.array([vec3d.x, vec3d.y, vec3d.z]) 
        m = np.array([[1, 0, 0, 0],[0, 1, 0, 0], [0, 0, 1, 0],[Pvec3d.x, Pvec3d.y, Pvec3d.z, 1]])
        v = v.dot(m)
        return Vector3D(*v)

    def Translate2DArray(self, Array:list[Vector2D], Pvec2d:Vector2D) -> list:
        return [self.Translate2D(i, Pvec2d) for i in Array]

    def Translate3DArray(self, Array:list[Vector3D], Pvec3d:Vector3D) -> list:
        return [self.Translate3D(i, Pvec3d) for i in Array]
     
    def Resize2D(self, W, H, Vec2d:Vector2D) -> list:
        return [Vector2D(*[i,j]) for i in range(Vec2d.x - abs(W)+1, Vec2d.x + abs(W)) for j in range(Vec2d.y - abs(H)+1, Vec2d.y + abs(H))]

    def Scale2D(self, vec2d:Vector2D, sx:float, sy:float) -> Vector2D:
        v = np.array([vec2d.x, vec2d.y])
        m = np.array([[sx, 0],[0, sy]])
        s = v.dot(m)

        return Vector2D(*s)

    def Scale3D(self, vec3d:Vector2D, sx:float, sy:float, sz:float) -> Vector3D:
        v = np.array([vec3d.x, vec3d.y, vec3d.z])
        m = np.array([[sx, 0, 0],[0, sy, 0], [0, 0, sz]])
        s = v.dot(m)

        return Vector3D(*s)

    def Scale2DArray(self, Array:list[Vector2D], sx:float, sy:float) -> list[Vector2D]:
        return [self.Scale2D(i, sx, sy) for i in Array]

    def Scale3DArray(self, Array:list[Vector3D], sx:float, sy:float, sz:float) -> list[Vector2D]:
        return [self.Scale3D(i, sx, sy, sz) for i in Array]

    def ResScale2D(self, W, H, vec2d:Vector2D, sx:float, sy:float) -> list[Vector2D]:
        s = self.Scale2D(vec2d, sx, sy)
        return self.Resize2D(W, H, Vector2D(*s))

    def ResScale2DToPoint(self, W, H, vec2d:Vector2D, sx:float, sy:float, Pvec2d:Vector2D = Vector2D(0,0)) -> list[Vector2D]:

        v = np.array([vec2d.x, vec2d.y, 1])

        m1 = np.array([[1, 0, 0],[0, 1, 0],[-Pvec2d.x, -Pvec2d.y, 1]])
        m2 = np.array([[sx, 0, 0],[0, sy, 0], [0,0,1]])
        m3 = np.array([[1, 0, 0],[0, 1, 0],[Pvec2d.x, Pvec2d.y, 1]])

        m = m1.dot(m2.dot(m3))

        v = v.dot(m)

        # v = self.Translate2D(vec2d, Vector2D(-Pvec2d.x, -Pvec2d.y))

        # v = self.Scale2D(v, sx, sy)

        # v = self.Translate2D(v, Pvec2d)

        return self.Resize2D(W, H, Vector2D(*v))

    def ResScale2DArray(self, W, H, Array:list[Vector2D], sx:float, sy:float) -> list:
        return [self.ResScale2D(W, H, i, sx, sy) for i in Array]

    def ResScale2DToPointArray(self, W, H, Array:list[Vector2D], sx:float, sy:float, Pvec2d:Vector2D = Vector2D(0,0)) -> list[Vector2D]:

        m1 = np.array([[1, 0, 0],[0, 1, 0],[-Pvec2d.x, -Pvec2d.y, 1]])
        m2 = np.array([[sx, 0, 0],[0, sy, 0], [0,0,1]])
        m3 = np.array([[1, 0, 0],[0, 1, 0],[Pvec2d.x, Pvec2d.y, 1]])

        m = m1.dot(m2.dot(m3))

        All = []

        for i in Array:
            v = np.array([i.x, i.y, 1])
            v = v.dot(m)
            All.append(self.Resize2D(W, H, Vector2D(*v)))
            
        return All

        # return [self.ResScale2DToPoint(W, H, i, sx, sy, Pvec2d) for i in Array]

    def Shear2D(self, vec2d:Vector2D, sx:float, sy:float) -> Vector2D:
        v = np.array([vec2d.x, vec2d.y])
        m = np.array([[1, sx],[sy, 1]])
        return Vector2D(*v.dot(m))

    def Shear2DArray(self, Array:list[Vector2D], sx:float, sy:float) -> list[Vector2D]:
        return [self.Shear2D(i, sx, sy) for i in Array]