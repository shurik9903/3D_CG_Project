from My_Vectors import *
from math import cos, radians, sin, tan

import numpy as np

class Matrix_Work():
    def __init__(self) -> None:
        pass

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

        v = np.around(v.dot(a))
        v = np.around(v.dot(b))
        v = np.around(v.dot(c))

        return Vector2D(*(v.astype(int)))
        
    def Rotation3DAlf(self, vec3d:Vector3D, alf = 0,  Axis:str = 'x') -> Vector3D:
        alf = radians(alf)

        v = np.array([vec3d.x, vec3d.y, vec3d.z])

        if Axis == 'x':
            m = np.array([[1, 0, 0],[0, cos(alf), -sin(alf)], [0, sin(alf),  cos(alf)]])
        elif Axis == 'y':
            m = np.array([[cos(alf), 0, sin(alf)],[0, 1, 0], [-sin(alf), 0,  cos(alf)]])
        else:
            m = np.array([[cos(alf), -sin(alf), 0],[sin(alf), cos(alf), 0], [0, 0,  1]])
        
        return Vector3D(*np.around(v.dot(m)).astype(int))

    def Rotation2DAlfArray(self, Array:list[Vector2D], alf = 0) -> list:
        return [self.Rotation2DAlf(i, alf) for i in Array]

    def Rotation3DAlfArray(self, Array:list[Vector3D], alf = 0,  Axis:str = 'x') -> list:
        return [self.Rotation3DAlf(i, alf, Axis) for i in Array]

    def Scale2D(self, W, H, vec2d:Vector2D, sx:float, sy:float) -> list:
        v = np.array([vec2d.x, vec2d.y])
        m = np.array([[sx, 0],[0, sy]])
        s = np.around(v.dot(m)).astype(int)

        return [Vector2D(*[i,j]) for i in range(s[0]-abs(W)+1, s[0]+abs(W)) for j in range(s[1]-abs(H)+1, s[1]+abs(H))]

    def Scale2DArray(self, Array:list[Vector2D], sx:float, sy:float) -> list:
        return [self.Scale2D(i, sx, sy) for i in Array]

    def Shear2D(self, vec2d:Vector2D, sx:float, sy:float):
        v = np.array([vec2d.x, vec2d.y])
        m = np.array([[1, sx],[sy, 1]])
        return Vector2D(*np.around(v.dot(m)).astype(int))

    def Shear2DArray(self, Array:list[Vector2D], sx:float, sy:float):
        return [self.Shear2D(i, sx, sy) for i in Array]