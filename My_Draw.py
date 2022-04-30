from tokenize import Double
from PyQt5.QtGui import QColor
from My_Vectors import *
from My_Matrix import *

import numpy as np

class Pixel(Vector2D):
    def __init__(self, vec2d:Vector2D, color = QColor(0,0,0)):
        super().__init__(vec2d.x, vec2d.y)
        self.color = color

class Pixel3D(Vector3D):
    def __init__(self, vec3d:Vector3D, color = QColor(0,0,0)):
        super().__init__(vec3d.x, vec3d.y, vec3d.z)
        self.color = color

class DrawTool():

    def convertToPixel(self, vec2d:Vector2D, color:QColor = QColor(0,0,0)):
        return Pixel(vec2d, color)


    def convertToPixel3D(self, vec3d:Vector3D, color:QColor = QColor(0,0,0)):
        return Pixel3D(vec3d, color)

    def convertToArrayPixels(self, Array:list[Vector2D], color:QColor = QColor(0,0,0)):
        FlatArray = np.array(Array).reshape(-1)
        return [self.convertToPixel(i, color) for i in FlatArray]

    def convertToArrayPixels3D(self, Array:list[Vector3D], color:QColor = QColor(0,0,0)):
        FlatArray = np.array(Array).reshape(-1)
        return [self.convertToPixel3D(i, color) for i in FlatArray]

    def drawLine(self, vec0:Vector2D, vec1:Vector2D, color:QColor = QColor(0,0,0)) -> list[Pixel]:
        #Инкрементный алгоритм растеризации
        
        line = []

        dx = abs(vec1.x - vec0.x)
        sx =  1 if vec0.x < vec1.x else -1
        dy = -abs(vec1.y - vec0.y)
        sy =  1 if vec0.y < vec1.y else -1
        error = dx + dy
        
        

        while True:
            line.append(Pixel(vec0, color))
            if vec0.x == vec1.x and vec0.y == vec1.y: break
            e2 = 2 * error

            if e2 >= dy:
                if vec0.x == vec1.x: break
                error = error + dy
                vec0.x = vec0.x + sx
            
            if e2 <= dx:
                if vec0.y == vec1.y: break
                error = error + dx
                vec0.y = vec0.y + sy

        return line

    def drawLine3D(self, vec_0:Vector3D, vec_1:Vector3D, color:QColor = QColor(0,0,0)) -> list[Pixel3D]:
        ListOfPoints = []

        vec0 = Vector3D(round(vec_0.x), round(vec_0.y), round(vec_0.z))
        vec1 = Vector3D(round(vec_1.x), round(vec_1.y), round(vec_1.z))

        ListOfPoints.append(Pixel3D(vec0,color))

        dx = abs(vec1.x - vec0.x)
        dy = abs(vec1.y - vec0.y)
        dz = abs(vec1.z - vec0.z)

        # Определение стороны движения
        if (vec1.x > vec0.x):
            xs = 1
        else:
            xs = -1
        if (vec1.y > vec0.y):
            ys = 1
        else:
            ys = -1
        if (vec1.z > vec0.z):
            zs = 1
        else:
            zs = -1
    
        # Движение по оси-x
        if (dx >= dy and dx >= dz):        
            p1 = 2 * dy - dx
            p2 = 2 * dz - dx
            while (vec0.x != vec1.x):
                vec0.x += xs
                if (p1 >= 0):
                    vec0.y += ys
                    p1 -= 2 * dx
                if (p2 >= 0):
                    vec0.z += zs
                    p2 -= 2 * dx
                p1 += 2 * dy
                p2 += 2 * dz
                ListOfPoints.append(Pixel3D(vec0,color))
    
        # Движение по оси-y
        elif (dy >= dx and dy >= dz):       
            p1 = 2 * dx - dy
            p2 = 2 * dz - dy
            while (vec0.y != vec1.y):
                vec0.y += ys
                if (p1 >= 0):
                    vec0.x += xs
                    p1 -= 2 * dy
                if (p2 >= 0):
                    vec0.z += zs
                    p2 -= 2 * dy
                p1 += 2 * dx
                p2 += 2 * dz
                ListOfPoints.append(Pixel3D(vec0,color))
    
        # Движение по оси-z
        else:        
            p1 = 2 * dy - dz
            p2 = 2 * dx - dz
            while (vec0.z != vec1.z):
                vec0.z += zs
                if (p1 >= 0):
                    vec0.y += ys
                    p1 -= 2 * dz
                if (p2 >= 0):
                    vec0.x += xs
                    p2 -= 2 * dz
                p1 += 2 * dy
                p2 += 2 * dx
                ListOfPoints.append(Pixel3D(vec0,color))

        return ListOfPoints

    def drawCircle(self, vec2D:Vector2D, R:Double, color:QColor = QColor(0,0,0)) -> list[Pixel]:

        circ = []
        
        vec = Vector2D(0,R)
        
        delta = 1 - 2 * R
        error = 0

        while (vec.y >= vec.x):

            circ.append(Pixel(Vector2D(vec2D.x + vec.x, vec2D.y + vec.y), color))
            circ.append(Pixel(Vector2D(vec2D.x + vec.x, vec2D.y - vec.y), color))
            circ.append(Pixel(Vector2D(vec2D.x - vec.x, vec2D.y + vec.y), color))
            circ.append(Pixel(Vector2D(vec2D.x - vec.x, vec2D.y - vec.y), color))
            circ.append(Pixel(Vector2D(vec2D.x + vec.y, vec2D.y + vec.x), color))
            circ.append(Pixel(Vector2D(vec2D.x + vec.y, vec2D.y - vec.x), color))
            circ.append(Pixel(Vector2D(vec2D.x - vec.y, vec2D.y + vec.x), color))
            circ.append(Pixel(Vector2D(vec2D.x - vec.y, vec2D.y - vec.x), color))

            error = 2 * (delta + vec.y) - 1
            if ((delta < 0) and (error <= 0)):
                vec.x += 1
                delta += 2 * vec.x + 1
                continue

            if ((delta > 0) and (error > 0)):
                vec.y -= 1
                delta -= 2 * vec.y + 1
                continue

            vec.x +=1
            delta += 2 * (vec.x - vec.y)
            vec.y -= 1
        
        return circ

    def draw3DBox(self, center:Vector3D, size:int, color:QColor = QColor(0,0,0)) -> list[Pixel3D]:

        Box = np.array([[center.x - size, center.y - size, center.z - size],
                        [center.x + size, center.y - size, center.z - size],
                        [center.x + size, center.y + size, center.z - size],
                        [center.x - size, center.y + size, center.z - size],
                        [center.x - size, center.y - size, center.z + size],
                        [center.x + size, center.y - size, center.z + size],
                        [center.x + size, center.y + size, center.z + size],
                        [center.x - size, center.y + size, center.z + size]])

        All = []

        for i in range(0, 4):
            All.append(self.drawLine3D(Vector3D(*Box[i]), Vector3D(*Box[(i+1)%4])))
            All.append(self.drawLine3D(Vector3D(*Box[i+4]), Vector3D(*Box[ ((i+1) % 4) + 4 ])))
            All.append(self.drawLine3D(Vector3D(*Box[i]), Vector3D(*Box[i+4])))

        return All





