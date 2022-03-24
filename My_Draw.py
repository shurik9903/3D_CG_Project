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

    def convertToPixel(self, vec2d:Vector2D, color:QColor = QColor(0,0,0)):
        return Pixel(vec2d, color)

    def convertToArrayPixels(self, Array:Vector2D, color:QColor = QColor(0,0,0)):
        FlatArray = np.array(Array).reshape(-1)
        return [self.convertToPixel(i, color) for i in FlatArray]

    def drawLine(self, vec0:Vector2D, vec1:Vector2D, color:QColor = None):
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

class Image(DrawTool, Matrix_Work):
    def __init__(self, Name:str = "", Layer:int = 0):
        self.Name = Name
        self.Layer = Layer
        self.Size = 1
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
        for i, pixel in enumerate(self.PixelBuffer):
            self.PixelBuffer[i] = Pixel(super().Mirror2DAxis(pixel, x, y), color=pixel.color)

    def RotationAlf(self, alf = 0):
        for i, pixel in enumerate(self.PixelBuffer):
            self.PixelBuffer[i] = Pixel(super().Rotation2DAlf(pixel, alf), color=pixel.color)

    def Scale(self, sx:int = 1, sy:int = 1): #Масштабирование
        new_buffer = []
        for pixel in self.PixelBuffer:
            s = super().Scale2D(pixel, sx, sy)
            new_buffer.extend(self.convertToArrayPixels(s, pixel.color))
        self.PixelBuffer = new_buffer


    def setColor(self, color:QColor): #Установка нового цвета
        for i in range(len(self.PixelBuffer)):
            self.PixelBuffer[i].color = color

    def copy(self, Name:str = None, Layer:int = None):
            new_cls = Image(self.Name if Name == None else Name, \
                self.Layer if Layer == None else Layer)
            new_cls.PixelBuffer = self.PixelBuffer.copy()
            return new_cls

        
