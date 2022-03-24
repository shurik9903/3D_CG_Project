from PyQt5.QtGui import QColor
from sympy import Matrix
from My_Vectors import *
from My_Matrix import Matrix_Work

import numpy as np

class Pixel(Vector2D):
    def __init__(self, vec2d:Vector2D, color = None):
        super().__init__(vec2d.x, vec2d.y)
        self.color = QColor(0,0,0) if color == None else color

class DrawTool():
    def __init__(self) -> None:
        pass

    def convertToPixel(self, x, y, color:QColor = QColor(0,0,0)):
        return Pixel(x, y, color)

    def convertToArray(self, Array, color:QColor = QColor(0,0,0)):
        FlatArray = np.array(Array).reshape(-1,2)
        return [self.convertToPixel(i[0], i[1], color) for i in FlatArray]

    def drawLine(self, vec0:Vector2D, vec1:Vector2D, color:QColor = None):
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

class Image(DrawTool, Matrix_Work):
    def __init__(self, Name:str = "", Layer:int = 0):
        self.Name = Name
        self.Layer = Layer
        self.PixelBuffer = []

    def putPixel(self, pixel:Pixel):
        self.PixelBuffer.append(pixel)

    def putArray(self, Array):
        self.PixelBuffer.extend(Array)

    def drawLine(self, vec0:Vector2D, vec1:Vector2D, color:QColor = QColor(0,0,0)):
        SDraw = super().drawLine(vec0,vec1, color)
        self.PixelBuffer.extend(SDraw)
        return SDraw

    def MirrorAxis(self, x:bool = False, y:bool = False):
        for i in self.PixelBuffer:
            print(i.x, i.y)
            i = Pixel(super().Mirror2DAxis(i, x, y), color=i.color)
            print(i.x, i.y)

    # def convertToDict(self):
    #     return {'Name':self.Name, 'Layer':self.Layer, 'Buffer':self.PixelBuffer}
