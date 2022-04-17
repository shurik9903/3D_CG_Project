from multiprocessing import Event
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QColor, QPainter, QPen
from PyQt5.QtCore import QThread, pyqtSignal

import time

from My_Image import *
from My_Image3D import *
from My_Matrix import *
from My_Vectors import *


class DrawThread(QThread):

    update = pyqtSignal(int)
    event_list = {}

    stop = False

    def addEvent(self, event, event_name, value = None):
        self.event_list[event_name] = {'event':event, 'value':value}

    def run(self):
        tick = 0
        while tick <= 360 and not self.stop:

            for k,v in self.event_list.items():
                if v['value'] == None:
                    v['event']()
                else:
                    v['event'](*v['value'])
            
            tick += 1
            print(tick)
            time.sleep(0.1)
            self.update.emit(int)


class Main_Window(QWidget, QPainter, DrawTool):
    
    def __init__(self, SizeX = 500, SizeY = 500):
        super().__init__()
        
        self.setupUI(SizeX, SizeY) #Инициализация окна
        self.FullImage = {-1:[]} #Буффер изображений
        
        self.pen = QPen(QColor(0,0,0)) #Перо с заданным цветов
        self.pen.setWidth(1) #Толщина пера
        
        self.Center = Vector2D(0,0) #Точка начала координат
        self.grafFlag = False #ИСпользовать ли систему координат в виде графика
        
        self.Thread = DrawThread()
        self.Thread.addEvent(self.update, 'wind_update')
        self.Thread.start()
        
        self.view = 'proj'


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

        for k in sorted(self.FullImage.keys()):
            for i in self.FullImage[k]:

                if isinstance(i, Image):
                    for j in i.getArrayPixel():
                        pen.setColor(j.color)
                        qp.setPen(pen)

                        x = round(self.Center.x + j.x)
                        y = round(self.Center.y + j.y) if not self.grafFlag else round(self.Center.y - j.y)

                        qp.drawPoint(x,y)

                if isinstance(i, Image3D):
                    for j in i.getArrayPixel():
                        pen.setColor(j.color)
                        qp.setPen(pen)

                        d2 = Matrix_Work().Projection2D(Vector3D(j.x, j.y, j.z), self.view)

                        x = round(self.Center.x + d2.x)
                        y = round(self.Center.y + d2.y) if not self.grafFlag else round(self.Center.y - d2.y)

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


    # def closeEvent(self, event):
    #     self.Thread.stop = True
    
    #     self.Thread.exec_()