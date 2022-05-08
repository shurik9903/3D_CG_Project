from cmath import pi
from multiprocessing import Event
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QColor, QPainter, QPen
from PyQt5.QtCore import QThread, pyqtSignal

import time

from My_Image import *
from My_Image3D import *
from My_Matrix import *
from My_Vectors import *
from My_Image3D_2 import *

class Camera():

    def __init__(self, location:Vector3D, rotation:Vector3D) -> None:
        self.location = location
        self.rotation = rotation

    def AddRotation(self, rotation:Vector3D):
        self.rotation.x += rotation.x
        self.rotation.y += rotation.y
        self.rotation.z += rotation.z

    def SetRotation(self, rotation:Vector3D):
        self.rotation.x = rotation.x
        self.rotation.y = rotation.y
        self.rotation.z = rotation.z

    def AddLocation(self, location:Vector3D):
        self.location.x += location.x
        self.location.y += location.y
        self.location.z += location.z

    def SetLocation(self, location:Vector3D):
        self.location.x = location.x
        self.location.y = location.y
        self.location.z = location.z
class DrawThread(QThread):

    update = pyqtSignal(int)
    event_list = {}

    stop = False
    pause = True
    work = False

    def addEvent(self, event, event_name, value = None, queue = 1):
        while self.work:
            True

        self.pause = True
        self.event_list[event_name] = {'event':event, 'value':value, 'queue':queue}
        self.event_list = dict(sorted(self.event_list.items(), key = lambda item: item[1]['queue']))
        self.pause = False


    def run(self):
        tick = 0
        while tick < 360 and not self.stop:
        
            if self.pause:
                continue

            self.work = True

            for k,v in self.event_list.items():
                if v['value'] == None:
                    v['event']()
                else:
                    v['event'](*v['value'])

            self.work = False

            tick += 1
            print(tick)
            time.sleep(0.1)
            self.update.emit(int)


class Main_Window(QWidget, QPainter, DrawTool):
    
    def __init__(self, SizeX = 500, SizeY = 500):
        super().__init__()

        self.Camera = Camera(Vector3D(0,0,0), Vector3D(0,0,0))

        self.FOV = 45
        self.Z0 = None

        self.view = 'proj'
        
        self.setupUI(SizeX, SizeY) #Инициализация окна
        self.FullImage = {-1:[]} #Буффер изображений
        
        self.pen = QPen(QColor(0,0,0)) #Перо с заданным цветов
        self.pen.setWidth(1) #Толщина пера
        
        self.Center = Vector2D(0,0) #Точка начала координат
        self.grafFlag = False #ИСпользовать ли систему координат в виде графика
        
        self.Thread = DrawThread()
        self.Thread.addEvent(self.update, 'wind_update', queue=-1)
        self.Thread.start()
        

    def setupUI(self, SizeX, SizeY):
        self.setWindowTitle("CG")
        self.move(300,300) #Стартовое расположение окна на экране
        self.resize(SizeX,SizeY) #Выставление размера окна
        self.setFixedSize(SizeX, SizeY) #Выставление фиксированого размера окна

        self.Z0 = (self.width() / 2) / tan((self.FOV / 2) * pi / 180)

    def pushImage(self, PImage:Image):
        if not self.FullImage.get(PImage.Layer) == None:
            self.FullImage.get(PImage.Layer).append(PImage)
        else:
             self.FullImage[PImage.Layer] = [PImage]

    def pushAllImage(self, PImage):
        if isinstance(PImage, list):
            for image in PImage:
                self.pushImage(image)

    def getImage(self, Name):
        for image in self.FullImage:
            for j in image.items()[1]:
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
            for image in self.FullImage[k]:

                if isinstance(image, Image):
                    for j in image.getArrayPixel():
                        pen.setColor(j.color)
                        qp.setPen(pen)

                        x = round(self.Center.x + j.x)
                        y = round(self.Center.y + j.y) if not self.grafFlag else round(self.Center.y - j.y)

                        qp.drawPoint(x,y)

                if isinstance(image, Image3D):
                    for j in image.getArrayPixel():
                        pen.setColor(j.color)
                        qp.setPen(pen)

                        Obj = Vector3D(j.x - self.Camera.location.x, j.y - self.Camera.location.y, j.z - self.Camera.location.z)
                        Obj = Matrix_Work().Rotation3DAlf(Obj, self.Camera.rotation, self.Camera.location)
                        d2 = Matrix_Work().Projection2D(Vector3D(Obj.x, Obj.y, Obj.z), self.Z0, self.view)

                        x = round(self.Center.x + d2.x)
                        y = round(self.Center.y + d2.y) if not self.grafFlag else round(self.Center.y - d2.y)

                        qp.drawPoint(x,y)

                if isinstance(image, Image3D_2):
                    for edge in image.Edge['Edge'].keys():

                        Obj = []
                        
                        for vertex in edge:

                            Cam_Ver = Vector3D(vertex.x - self.Camera.location.x, vertex.y - self.Camera.location.y, vertex.z - self.Camera.location.z)
                            Obj.append(Matrix_Work().Rotation3DAlf(Cam_Ver, self.Camera.rotation, self.Camera.location))


                        Obj = Matrix_Work().Projection2D(Vector3D(Obj.x, Obj.y, Obj.z), self.Z0, self.view)

                        x = round(self.Center.x + d2.x)
                        y = round(self.Center.y + d2.y) if not self.grafFlag else round(self.Center.y - d2.y)

                        pen.setColor(image.Color)
                        qp.setPen(pen)
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