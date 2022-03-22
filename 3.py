from cmath import cos, sin
from math import ceil, degrees, floor, radians
from xml.etree.ElementTree import PI
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QColor, QPainter, QPen, QImage

import numpy as np
import sys

class Vector2D():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Pixel(Vector2D):
    def __init__(self, x, y, color = None):
        super().__init__(x, y)
        self.color = QColor(0,0,0) if color == None else color

class Main_Window(QWidget, QPainter):
    
    def __init__(self, SizeX = 500, SizeY = 500):
        super().__init__()
        self.setupUI(SizeX, SizeY) #Инициализация окна
        self.PixelCoordinate = [] #Буффер пикселей
        self.pen = QPen(QColor(0,0,0)) #Перо с заданным цветов
        self.pen.setWidth(1) #Толщина пера
        self.Center = Vector2D(0,0) #Точка начала координат
        self.grafFlag = False #ИСпользовать ли систему координат в виде графика

    def setupUI(self, SizeX, SizeY):
        self.setWindowTitle("Matrix")
        self.move(300,300) #Стартовое расположение окна на экране
        self.resize(SizeX,SizeY) #Выставление размера окна
        self.setFixedSize(SizeX, SizeY) #Выставление фиксированого размера окна

        self.Image = QImage

    def paintEvent(self, paint_event): #Событие отрисовки
        qp = QPainter()
        qp.begin(self)
        self.drawPixel(qp)
        qp.end()

    def drawPixel(self,qp):
        pen = self.pen   
        
        for i in self.PixelCoordinate:
            pen.setColor(i.color)
            qp.setPen(pen)

            x = self.Center.x + i.x
            y = self.Center.y + i.y if not self.grafFlag else self.Center.y - i.y

            qp.drawPoint(x,y)

    def putPixel(self, pixel:Pixel):
        self.PixelCoordinate.append(pixel)

    def putArray(self, Array):
        self.PixelCoordinate.extend(Array)

    def convertToPixel(self, x, y, color:QColor):
        return Pixel(x, y, color)

    def convertToArray(self, Array, color:QColor):
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
            line.append(Pixel(vec0.x, vec0.y, color))
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

        self.PixelCoordinate.extend(line)
        return line

    def antialiasedPixel(self, pixel:Pixel):
        x = pixel.x
        y = pixel.y
        for rounded_x in range(x-1, x+2):
            for rounded_y in range(y-1, y+2):
                percent_x = 1 - abs(x - rounded_x)
                percent_y = 1 - abs(y - rounded_y)
                percent = percent_x * percent_y
                self.putPixel(Pixel(rounded_x, rounded_y))

class Matrix_Work():
    def __init__(self) -> None:
        pass

    def Mirror2DAxis(self, vec2d:Vector2D, x:bool = False, y:bool = False):
        x = -1 if x else 1
        y = -1 if y else 1

        v = np.array([vec2d.x, vec2d.y])
        m = np.array([[x, 0],[0, y]])
        return v.dot(m)

    def Mirror3DAxis(self, vec3d, x:bool = False, y:bool = False, z:bool = False):
        x = -1 if x else 1
        y = -1 if y else 1
        z = -1 if z else 1

        v = np.array([vec3d.x, vec3d.y, vec3d.z])
        m = np.array([[x, 0, 0],[0, y, 0], [0, 0, z]])
        return v.dot(m)
    
    def Mirror2DAxisArray(self, Array, x:bool = False, y:bool = False):
        return [self.Mirror2DAxis(i, x, y) for i in Array]

    def Mirror3DAxisArray(self, Array, x:bool = False, y:bool = False, z:bool = False):
        return [self.Mirror2DAxis(i, x, y, z) for i in Array]



    def Rotation2DAlf(self, vec2d:Vector2D, alf = 0):
        alf = radians(alf)
        v = np.array([vec2d.x, vec2d.y])
        m = np.array([[cos(alf), -sin(alf)],[sin(alf), cos(alf)]])
        return (v.dot(m)).astype(int)
    
    def Rotation3DAlf(self, vec3d, alf = 0,  Axis:str = 'x'):
        alf = radians(alf)

        v = np.array([vec3d.x, vec3d.y, vec3d.z])

        if Axis == 'x':
            m = np.array([[1, 0, 0],[0, cos(alf), -sin(alf)], [0, sin(alf),  cos(alf)]])
        elif Axis == 'y':
            m = np.array([[cos(alf), 0, sin(alf)],[0, 1, 0], [-sin(alf), 0,  cos(alf)]])
        else:
            m = np.array([[cos(alf), -sin(alf), 0],[sin(alf), cos(alf), 0], [0, 0,  1]])
        
        return (v.dot(m)).astype(int)

    def Rotation2DAlfArray(self, Array, alf = 0):
        return [self.Rotation2DAlf(i, alf) for i in Array]

    def Rotation3DAlfArray(self, Array, alf = 0,  Axis:str = 'x'):
        return [self.Rotation3DAlf(i, alf, Axis) for i in Array]



    def Scale2D(self, vec2d:Vector2D, sx:int = 1, sy:int = 1):
        v = np.array([vec2d.x, vec2d.y])
        m = np.array([[sx, 0],[0, sy]])
        s = (v.dot(m)).astype(int)
        
        x = np.linspace(s[0]-sx+1, s[0]+sx-1, 2*sx-1,endpoint=True, dtype=int)
        y = np.linspace(s[1]-sy+1, s[1]+sy-1, 2*sy-1,endpoint=True, dtype=int)

        return [[i,j] for i in x for j in y]

    def Scale2DArray(self, Array, sx:int = 1, sy:int = 1):
        return [self.Scale2D(i, sx, sy) for i in Array]


    

def drawAxis(Window, valueOfDivision):

    WWidth = wind.size().width()
    WHight = wind.size().height() 

    for i in range(-int(WWidth/2), int(WWidth/2), valueOfDivision):
        wind.drawLine(Vector2D(i,int(valueOfDivision/5)), Vector2D(i,int(-valueOfDivision/5)))

    for i in range(-int(WHight/2), int(WHight/2), valueOfDivision):
        wind.drawLine(Vector2D(int(valueOfDivision/5),i), Vector2D(int(-valueOfDivision/5),i))

    wind.drawLine(Vector2D(-int(WWidth/2),0), Vector2D(int(WWidth/2),0))
    wind.drawLine(Vector2D(0,-int(WHight/2)), Vector2D(0,int(WHight/2)))

app = QApplication(sys.argv)
wind = Main_Window() #Создание и инициализация окна приложения
wind.pen.setWidth(1) #Установка размера пера в пикселях

WWidth = wind.size().width() #Ширина окна
WHight = wind.size().height() #Высота окна

Center = Vector2D(int(int(WWidth/2)), int(WHight/2)) #Центр окна
wind.Center = Center 

wind.grafFlag = True

drawAxis(wind, 10)
# for i in range(0, 100):
#     wind.putPixel(Pixel(i,i, QColor(255,0,0)))

line = wind.drawLine(Vector2D(-5, 10), Vector2D(5,10), QColor(255,0,0))
#wind.putPixel(Matrix_Work().Mirror2DAxisArray(line, x = True))

#MLine = Matrix_Work().Mirror2DAxisArray(line, x = True,y = True)
#wind.putArray(wind.convertToArray(MLine, QColor(255,0,0)))

#RLine = Matrix_Work().Rotation2DAlfArray(line, 45)
#wind.putArray(wind.convertToArray(RLine, QColor(255,0,0)))

SLine = Matrix_Work().Scale2DArray(line, 2, 2)
wind.putArray(wind.convertToArray(SLine, QColor(255,0,0)))

SLine = Matrix_Work().Scale2DArray(line, 10, 10)
RLine = Matrix_Work().Rotation2DAlfArray(wind.convertToArray(SLine, QColor(255,0,0)), 45)
wind.putArray(wind.convertToArray(RLine, QColor(255,0,0)))

# m = np.array([[1,2],[2,1]])
# m = np.array([1])
# print(m.shape)
# m2 = np.pad(m, ((1,1),(2,2)), mode="symmetric")
# print(m2)

x = np.linspace(-1, 1, 3,endpoint=True)
y = np.linspace(-1, 1, 3,endpoint=True)

xx,yy = np.meshgrid(x,y)
res = np.stack((xx, yy), axis=2)


wind.show() #Вывод окна приложения на экран
sys.exit(app.exec_()) #Процесс завершения работы
