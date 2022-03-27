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
    
    def Mirror2DAxisArray(self, Array, x:bool = False, y:bool = False) -> list:
        return [self.Mirror2DAxis(i, x, y) for i in Array]

    def Mirror3DAxisArray(self, Array, x:bool = False, y:bool = False, z:bool = False) -> list:
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

    def Rotation2DAlfArray(self, Array, alf = 0) -> list:
        return [self.Rotation2DAlf(i, alf) for i in Array]

    def Rotation3DAlfArray(self, Array, alf = 0,  Axis:str = 'x') -> list:
        return [self.Rotation3DAlf(i, alf, Axis) for i in Array]

    def Scale2D(self, W, H, vec2d:Vector2D, sx:int = 1, sy:int = 1, ) -> list:
        v = np.array([vec2d.x, vec2d.y])
        m = np.array([[sx, 0],[0, sy]])
        s = np.around(v.dot(m)).astype(int)

        return [Vector2D(*[i,j]) for i in range(s[0]-abs(W)+1, s[0]+abs(W)) for j in range(s[1]-abs(H)+1, s[1]+abs(H))]


    def Down_Scale2D(self, sx:int, sy:int, Width:int, Height:int, ImageBuffer):

        ImageFinal = {}

        thumbwidth = sx
        thumbheight = sy

        xscale = thumbwidth / Width
        yscale = thumbheight / Height

        threshold = 0.5 / (xscale * yscale)
        yend = 0.0

        for f in range(0, thumbheight):

            ystart = yend
            yend = (f + 1) / yscale

            if (yend >= Height): yend = Height - 0.000001
            xend = 0.0

            for g in range(0, thumbwidth):

                xstart = xend
                xend = (g + 1) / xscale
                if (xend >= Width): xend = Width - 0.000001
                sum = 0.0

                for y in range(int(ystart), int(yend)):

                    yportion = 1.0
                    if (y == int(ystart)): yportion -= ystart - y
                    if (y == int(yend)): yportion -= y+1 - yend

                    for x in range(int(xstart, int(xend))):

                        xportion = 1.0
                        if (x == int(xstart)): xportion -= xstart - x
                        if (x == int(xend)): xportion -= x+1 - xend
                        sum += ImageBuffer[y][x] * yportion * xportion
                    
                ImageFinal.setdefault(x, {})[y] =  1 if (sum > threshold) else 0
            
        

    def Scale2DArray(self, Array, sx:int = 1, sy:int = 1) -> list:
        return [self.Scale2D(i, sx, sy) for i in Array]
