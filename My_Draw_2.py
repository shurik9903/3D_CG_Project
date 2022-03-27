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

    def getPixel(self, x:int, y:int) -> Pixel:
        
        return self.PixelBuffer.get(x, {}).get(y, None)

    def getArrayPixel(self) -> list[Pixel]:
        return [Pixel(Vector2D(*(i,j)), v) for i, value in self.PixelBuffer.items() for j,v in value.items()]

    def setPixel(self, pixel:Pixel):
        x = pixel.x
        y = pixel.y
        self.PixelBuffer.setdefault(x, {})[y] = pixel.color

    def putArray(self, Array:list[Pixel]):
        for pixel in Array:
            if isinstance(pixel, Pixel):
                self.setPixel(pixel)

    def __getitem__(self, x:int, y:int) -> Pixel:
        return self.getPixel(x, y)

    def recalculateSize(self) -> tuple:
        min_x, max_x = min(self.PixelBuffer), max(self.PixelBuffer)
        first = next(iter(list(self.PixelBuffer.values())[0]))
        min_y, max_y = first, first

        for value in self.PixelBuffer.values():
            for j in value:
                min_y,max_y = min(j,min_y), max(j,max_y)

        self.Width = abs(max_x - min_x) if not max_x == min_x else 1
        self.Height = abs(max_y - min_y) if not max_y == min_y else 1

        return (max_x, min_x, max_y, min_y)

    def drawLine(self, vec0:Vector2D, vec1:Vector2D, color:QColor = QColor(0,0,0)) -> list:
        SDraw = super().drawLine(vec0,vec1, color)
        self.putArray(SDraw)
        return SDraw

    def MirrorAxis(self, x:bool = False, y:bool = False): #Отзеркаливание
            new_buffer = []
            for i, value in self.PixelBuffer.items():
                 for j,v in value.items():
                     new_buffer.append(Pixel(super().Mirror2DAxis(Vector2D(*(i,j)), x, y), color = v))

            self.PixelBuffer.clear()
            self.putArray(new_buffer)

    def RotationAlf(self, alf = 0): #Вращение
            new_buffer = []
            for i, value in self.PixelBuffer.items():
                for j,v in value.items():
                    new_buffer.append(Pixel(super().Rotation2DAlf(Vector2D(*(i,j)), alf), color = v))

            self.PixelBuffer.clear()
            self.putArray(new_buffer)

    def setColor(self, color:QColor): #Установка нового цвета
        for i, value in self.PixelBuffer.items(): 
            for j in value:
                self.PixelBuffer[i][j] = color

    def Scale(self, sx:float, sy:float): #Масштабирование

        if sx == 1 and sy == 1: return

        self.ScaleHeight = round(sx * self.ScaleHeight) 
        self.ScaleWidth = round(sy * self.ScaleWidth)

        new_buffer = []

        for i, value in self.PixelBuffer.items():
             for j,v in value.items():
                 s = super().Scale2D(self.ScaleWidth, self.ScaleHeight, Vector2D(*(i,j)), sx, sy)
                 new_buffer.extend([Pixel(vec, color = v) for vec in s])
        
        self.PixelBuffer.clear()
        self.putArray(new_buffer)

    def Shear(self, sx:int, sy:int): #Смещение
        new_buffer = []
        for i, value in self.PixelBuffer.items():
            for j,v in value.items():
                new_buffer.append(Pixel(super().Shear2D(Vector2D(*(i,j)), sx, sy), color = v))

        self.PixelBuffer.clear()
        self.putArray(new_buffer)

    # def Scale_2(self, sx:int = 1, sy:int = 1):

    #     self.recalculateSize()
    #     new_W, new_H = self.Width * sx, self.Height * sy
    #     scrW, scrH = self.Width, self.Height

    #     retimg = {}
    #     for i in range(new_H-1):
    #         for j in range(new_W-1):
    #             scrx=round(i*(scrH/new_H))
    #             scry=round(j*(scrW/new_W))
    #             retimg.setdefault(j, {})[i] = QColor(0,0,0) if self.getPixel(scrx, scry) == None else self.getPixel(scrx, scry)
    #     self.PixelBuffer.clear()
    #     self.PixelBuffer = retimg




    def copy(self, Name:str = None, Layer:int = None): #Копия
        new_cls = Image_2(self.Name if Name == None else Name, \
        self.Layer if Layer == None else Layer)
        new_cls.ScaleWidth = self.ScaleWidth
        new_cls.ScaleHeight = self.ScaleHeight
        new_cls.Width = self.Width
        new_cls.Height = self.Height
        new_cls.PixelBuffer = deepcopy(self.PixelBuffer)
        return new_cls

