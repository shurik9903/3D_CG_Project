from xml.etree.ElementTree import PI
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QColor, QPainter, QPen

import numpy as np
import sys

from My_Draw import *
from My_Matrix import *
from My_Vectors import *

class Main_Window(QWidget, QPainter, DrawTool):
    
    def __init__(self, SizeX = 500, SizeY = 500):
        super().__init__()
        self.setupUI(SizeX, SizeY) #Инициализация окна
        self.FullImage = {-1:[]} #Буффер изображений
        self.pen = QPen(QColor(0,0,0)) #Перо с заданным цветов
        self.pen.setWidth(1) #Толщина пера
        self.Center = Vector2D(0,0) #Точка начала координат
        self.grafFlag = False #ИСпользовать ли систему координат в виде графика

    def setupUI(self, SizeX, SizeY):
        self.setWindowTitle("CG")
        self.move(300,300) #Стартовое расположение окна на экране
        self.resize(SizeX,SizeY) #Выставление размера окна
        self.setFixedSize(SizeX, SizeY) #Выставление фиксированого размера окна

    def pushImage(self, PImage:Image):
        if not self.FullImage.get(PImage.Layer) == None:
            self.FullImage.get(PImage.Layer).append(PImage)
        else:
             self.FullImage[PImage.Layer] = [PImage]

    def pushAllImage(self, PImage):
        if isinstance(PImage, list):
            for i in PImage:
                self.pushImage(i)

    def getImage(self, Name):
        for i in self.FullImage:
            for j in i.items()[1]:
                if j.Name == Name:
                    return j
        return None

    def getImage(self, Layer, Name):
        if self.FullImage.get(Layer) == None:
            return None
        else:
            return self.getImage(Name)

    def paintEvent(self, paint_event): #Событие отрисовки
        qp = QPainter()
        qp.begin(self)
        self.fullDraw(qp)
        qp.end()

    def fullDraw(self,qp):
        pen = self.pen   

        keys = list(self.FullImage.keys())
        keys.sort(reverse=True)
        All = []
        for k, v in self.FullImage.items():
             for i in v:
                 All.extend(i.PixelBuffer)

        for i in All:
            pen.setColor(i.color)
            qp.setPen(pen)

            x = self.Center.x + i.x
            y = self.Center.y + i.y if not self.grafFlag else self.Center.y - i.y

            qp.drawPoint(x,y)

    def putPixel(self, pixel:Pixel):
        self.FullImage[-1].append(pixel)

    def putArray(self, Array):
        self.FullImage[-1].extend(Array)

    def drawLine(self, vec0:Vector2D, vec1:Vector2D, color:QColor = QColor(0,0,0)):
        SDraw = super().drawLine(vec0,vec1, color)
        self.FullImage[-1].extend(SDraw)
        return SDraw

    def antialiasedPixel(self, pixel:Pixel):
        x = pixel.x
        y = pixel.y
        for rounded_x in range(x-1, x+2):
            for rounded_y in range(y-1, y+2):
                percent_x = 1 - abs(x - rounded_x)
                percent_y = 1 - abs(y - rounded_y)
                percent = percent_x * percent_y
                self.putPixel(Pixel(rounded_x, rounded_y))

def drawAxis(valueOfDivision):

    WWidth = wind.size().width()
    WHight = wind.size().height() 

    Axis = Image("Axis", 0)

    for i in range(-round(WWidth/2), round(WWidth/2), valueOfDivision):
        Axis.drawLine(Vector2D(i,round(valueOfDivision/5)), Vector2D(i,round(-valueOfDivision/5)))

    for i in range(-round(WHight/2), round(WHight/2), valueOfDivision):
        Axis.drawLine(Vector2D(round(valueOfDivision/5),i), Vector2D(round(-valueOfDivision/5),i))

    Axis.drawLine(Vector2D(-round(WWidth/2),0), Vector2D(round(WWidth/2),0))
    Axis.drawLine(Vector2D(0,-round(WHight/2)), Vector2D(0,round(WHight/2)))

    return Axis

if __name__ == '__main__':

    app = QApplication(sys.argv)
    wind = Main_Window() #Создание и инициализация окна приложения
    tools = DrawTool()

    wind.pen.setWidth(1) #Установка размера пера в пикселях

    WWidth = wind.size().width() #Ширина окна
    WHight = wind.size().height() #Высота окна

    Center = Vector2D(round(WWidth/2), round(WHight/2)) #Центр окна
    wind.Center = Center 

    wind.grafFlag = True

    wind.pushImage(drawAxis(10))

    # # for i in range(0, 100):
    # #     wind.putPixel(Pixel(i,i, QColor(255,0,0)))

    Line = Image('Line',1)
    Line.drawLine(Vector2D(-5, 10), Vector2D(5,10), QColor(255,0,0))
    #DLine = Line.drawLine(Vector2D(-5, 10), Vector2D(5,10), QColor(255,0,0))
    # #wind.putPixel(Matrix_Work().Mirror2DAxisArray(line, x = True))
    Line.MirrorAxis(False, True)
    wind.pushImage(Line)
    # MLine = Image('Mirror',1)
    # MLine.putArray(tools.convertToArray(Matrix_Work().Mirror2DAxisArray(DLine, x = True,y = True), QColor(0,255,0)))
    # #wind.putArray(wind.convertToArray(MLine, QColor(255,0,0)))

    # #RLine = Matrix_Work().Rotation2DAlfArray(line, 45)
    # #wind.putArray(wind.convertToArray(RLine, QColor(255,0,0)))

    # SMLine = Matrix_Work().Scale2DArray(DLine, 2, 2)
    # SLine = Image('Scale',2)
    # SLine.putArray(tools.convertToArray(SMLine, QColor(255,0,0)))

    # SMLine = Matrix_Work().Scale2DArray(DLine, 10, 10)
    # RMLine = Matrix_Work().Rotation2DAlfArray(tools.convertToArray(SMLine), 45)

    # RLine = Image('ScaleAndRotate',3)
    # RLine.putArray(tools.convertToArray(RMLine, QColor(255,0,0)))

    # RLine2 = Image('GreenLayer',4)
    # RLine2.putArray(tools.convertToArray(RMLine, QColor(0,255,0)))

    # MLine2 = Image('Mirror2',1)
    # MLine2.putArray(tools.convertToArray(Matrix_Work().Mirror2DAxisArray(tools.convertToArray(RMLine), x = True,y = True), QColor(0,255,0)))

    # wind.pushAllImage([Line, SLine, RLine, RLine2, MLine, MLine2])

    wind.show() #Вывод окна приложения на экран
    sys.exit(app.exec_()) #Процесс завершения работы


