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

    def __str__(self) -> str:
        return super().__str__(f'x:{self.x}, y:{self.y}, color:{self.color}')

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
        self.ScaleWidth = 1
        self.ScaleHeight = 1
        self.Width = None
        self.Height = None
        self.PixelBuffer = []

    def putPixel(self, pixel:Pixel):
        self.PixelBuffer.append(pixel)

    def putArray(self, Array):
        self.PixelBuffer.extend(Array)

    def recalculateSize(self):
        start_pixel = self.PixelBuffer[0]
        min_x, max_x = start_pixel.x, start_pixel.x
        min_y, max_y = start_pixel.y, start_pixel.y

        for pixel in self.PixelBuffer[1:]:
            
            if pixel.x > max_x:
                max_x = pixel.x
            
            if pixel.x < min_x:
                min_x = pixel.x

            if pixel.y > max_y:
                max_y = pixel.y
            
            if pixel.y < min_y:
                min_y = pixel.y

        self.Width = abs(max_x - min_x)
        self.Height = abs(max_y - min_y)

        return (max_x, min_x, max_y, min_y)


    def drawLine(self, vec0:Vector2D, vec1:Vector2D, color:QColor = QColor(0,0,0)):
        SDraw = super().drawLine(vec0,vec1, color)
        self.putArray(SDraw)
        return SDraw

    def MirrorAxis(self, x:bool = False, y:bool = False): #Отзеркаливание
        for i, pixel in enumerate(self.PixelBuffer):
            self.PixelBuffer[i] = Pixel(super().Mirror2DAxis(pixel, x, y), color=pixel.color)

    def RotationAlf(self, alf = 0): #Вращение
        for i, pixel in enumerate(self.PixelBuffer):
            self.PixelBuffer[i] = Pixel(super().Rotation2DAlf(pixel, alf), color=pixel.color)

    def Scale(self, sx:int = 1, sy:int = 1): #Масштабирование
        
        if sx == 1 and sy == 1: return

        self.ScaleHeight = round(sx * self.ScaleHeight) 
        self.ScaleWidth = round(sy * self.ScaleWidth)

        new_buffer = []
        for pixel in self.PixelBuffer:
            s = super().Scale2D(self.ScaleWidth, self.ScaleHeight, pixel, sx, sy)
            new_buffer.extend(self.convertToArrayPixels(s, pixel.color))
        print("1 ", len(new_buffer))
        print("2 ",len(self.PixelBuffer))

        self.PixelBuffer = new_buffer.copy()
        
        print("3 ", len(new_buffer))
        print("4 ",len(self.PixelBuffer))

    def setColor(self, color:QColor): #Установка нового цвета
        for i in range(len(self.PixelBuffer)):
            self.PixelBuffer[i].color = color

    def copy(self, Name:str = None, Layer:int = None): #Копия
            new_cls = Image(self.Name if Name == None else Name, \
               self.Layer if Layer == None else Layer)
            new_cls.ScaleWidth = self.ScaleWidth
            new_cls.ScaleHeight = self.ScaleHeight
            new_cls.Width = self.Width
            new_cls.Height = self.Height
            new_cls.PixelBuffer = deepcopy(self.PixelBuffer)
            return new_cls
