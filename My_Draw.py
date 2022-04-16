from statistics import mean
from tokenize import Double
from PyQt5.QtGui import QColor
from My_Vectors import *
from My_Matrix import Matrix_Work

from copy import deepcopy

import numpy as np

class Pixel(Vector2D):
    def __init__(self, vec2d:Vector2D, color = None):
        super().__init__(vec2d.x, vec2d.y)
        self.color = QColor(0,0,0) if color == None else color

class DrawTool():
    def __init__(self) -> None:
        pass

    def convertToPixel(self, vec2d:Vector2D, color:QColor = QColor(0,0,0)):
        return Pixel(vec2d, color)

    def convertToArrayPixels(self, Array:list[Vector2D], color:QColor = QColor(0,0,0)):
        FlatArray = np.array(Array).reshape(-1)
        return [self.convertToPixel(i, color) for i in FlatArray]

    def drawLine(self, vec0:Vector2D, vec1:Vector2D, color:QColor = None) -> list[Pixel]:
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

    def draw3DBox(self, center:Vector2D, size:int, color:QColor = QColor(0,0,0)) -> list[Pixel]:

        Box = np.array([[center.x - size, center.y - size, 0],
                        [center.x + size, center.y - size, 0],
                        [center.x + size, center.y + size, 0],
                        [center.x - size, center.y + size, 0]])


        proj = [[1, 0, 0],
                [0, 1, 0]]

        Box = [Vector2D(*i) for i in Box]

        return self.convertToArrayPixels(Box, color)





