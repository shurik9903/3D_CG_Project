from PyQt5.QtGui import QColor
from sympy import Matrix
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



class Image_2(DrawTool, Matrix_Work):
    def __init__(self, Name:str = "", Layer:int = 0):
        self.Name = Name
        self.Layer = Layer
        self.ScaleWidth = 1
        self.ScaleHeight = 1
        self.Width = None
        self.Height = None
        self.PixelBuffer = {}

    def getPixel(self, x:int, y:int):
        return self.PixelBuffer.get(str(x)).get(str(y), None)

    def setPixel(self, pixel:Pixel):
        x = pixel.x
        y = pixel.y
        self.PixelBuffer[str(x)][str(y)] = pixel.color

    def putArray(self, Array):
        for pixel in Array:
            if isinstance(Pixel, pixel):
                self.setPixel(pixel)

    def __getitem__(self, x:int, y:int):
        return self.getPixel(x, y)

    def recalculateSize(self):
        min_x, max_x = min(self.PixelBuffer, key = self.PixelBuffer.get), max(self.PixelBuffer, key = self.PixelBuffer.get)
        min_y, max_y = min(self.PixelBuffer.values()), max(self.PixelBuffer.values())

        self.Width = abs(max_x - min_x)
        self.Height = abs(max_y - min_y)

        return (max_x, min_x, max_y, min_y)

    def drawLine(self, vec0:Vector2D, vec1:Vector2D, color:QColor = QColor(0,0,0)):
        SDraw = super().drawLine(vec0,vec1, color)
        self.putArray(SDraw)
        return SDraw

    def MirrorAxis(self, x:bool = False, y:bool = False): #Отзеркаливание
            new_buffer = [Pixel(super().Mirror2DAxis(Vector2D((i,j)), x, y), color = j.value()) for i in self.PixelBuffer for j in i]
            self.PixelBuffer.clear()
            self.putArray(new_buffer)

    def RotationAlf(self, alf = 0): #Вращение
            new_buffer = [Pixel(super().Rotation2DAlf(Vector2D((i,j)), alf), color=j.value()) for i in self.PixelBuffer for j in i]
            self.PixelBuffer.clear()
            self.putArray(new_buffer)

    def setColor(self, color:QColor): #Установка нового цвета
        for i in self.PixelBuffer: 
            for j in i:
                j:color

    def Scale(self, sx:int = 1, sy:int = 1): #Масштабирование
        if sx == 1 and sy == 1: return

        self.ScaleHeight = round(sx * self.ScaleHeight) 
        self.ScaleWidth = round(sy * self.ScaleWidth)
        
        new_buffer = [Pixel(super().Scale2D(self.ScaleWidth, self.ScaleHeight, Vector2D((i,j)), sx, sy), color=j.value()) for i in self.PixelBuffer for j in i]
        self.PixelBuffer.clear()
        self.putArray(new_buffer)

    def copy(self, Name:str = None, Layer:int = None): #Копия
        new_cls = Image_2(self.Name if Name == None else Name, \
        self.Layer if Layer == None else Layer)
        new_cls.ScaleWidth = self.ScaleWidth
        new_cls.ScaleHeight = self.ScaleHeight
        new_cls.Width = self.Width
        new_cls.Height = self.Height
        new_cls.PixelBuffer = deepcopy(self.PixelBuffer)
        return new_cls

