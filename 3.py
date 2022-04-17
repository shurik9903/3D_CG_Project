from PyQt5.QtWidgets import QApplication

import sys

from My_Window import *

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
    wind.view = 'orto'

    wind.show() #Вывод окна приложения на экран

    wind.pen.setWidth(1) #Установка размера пера в пикселях

    WWidth = wind.size().width() #Ширина окна
    WHight = wind.size().height() #Высота окна

    Center = Vector2D(round(WWidth/2), round(WHight/2)) #Центр окна
    wind.Center = Center 

    wind.grafFlag = True

    wind.pushImage(drawAxis(10))

    Box = Image3D('Box', 1)
    wind.pushImage(Box)
    
    Box.draw3DBox(Vector3D(0,0,0), 100)

    wind.Thread.addEvent(Box.Rotation3DAlf, 'Rotation', (1,'x'))
    # wind.Thread.addEvent(Box.Rotation3DAlf, 'Rotation2', (1,'y'))
    # wind.Thread.addEvent(Box.Rotation3DAlf, 'Rotation3', (1,'z'))

    # Box.Rotation3DAlf(45, 'y')
    # Box.Rotation3DAlf(45, 'z')
    # Box.Rotation3DAlf(1, 'z')
    # Box.Rotation3DAlf(1, 'z')
    # Box.Rotation3DAlf(1, 'z')
    # Box.Rotation3DAlf(1, 'z')
    # Box.Rotation3DAlf(1, 'z')
    # Box.Rotation3DAlf(1, 'z')
    # Box.Rotation3DAlf(1, 'z')
    # Box.Rotation3DAlf(1, 'z')
    # Box.Rotation3DAlf(1, 'z')
    # Box.Rotation3DAlf(1, 'z')
    # Box.Rotation3DAlf(1, 'z')
    
    # Box.Rotation3DAlf(1, 'x')
    # Box.Rotation3DAlf(1, 'x')
    # Box.Rotation3DAlf(1, 'x')
    # Box.Rotation3DAlf(1, 'x')
    # Box.Rotation3DAlf(1, 'x')
    # Box.Rotation3DAlf(1, 'x')
    # Box.Rotation3DAlf(1, 'x')
    # Box.Rotation3DAlf(1, 'x')
    # Box.Rotation3DAlf(1, 'x')
    # Box.Rotation3DAlf(1, 'x')
    # Box.Rotation3DAlf(1, 'x')
    # Box.Rotation3DAlf(1, 'x')

    # Box.Rotation3DAlf(1, 'y')
    # Box.Rotation3DAlf(1, 'y')
    # Box.Rotation3DAlf(1, 'y')
    # Box.Rotation3DAlf(1, 'y')
    # Box.Rotation3DAlf(1, 'y')
    # Box.Rotation3DAlf(1, 'y')
    # Box.Rotation3DAlf(1, 'y')
    # Box.Rotation3DAlf(1, 'y')
    # Box.Rotation3DAlf(1, 'y')
    # Box.Rotation3DAlf(1, 'y')
    # Box.Rotation3DAlf(1, 'y')
    # Box.Rotation3DAlf(1, 'y')
    # Box.Rotation3DAlf(1, 'y')

    # Box.Rotation3DAlf(45, 'y')
    # Box.Rotation3DAlf(45, 'z')

    # Box.drawLine3D(Vector3D(-100,-100,-100), Vector3D(100,100,100))
    
    

     

    # wind.update()
    sys.exit(app.exec_()) #Процесс завершения работы


    # Line = Image('Line',1)
    # Line.drawLine(Vector2D(-5, 10), Vector2D(5,10), QColor(255,0,0))
    # wind.pushImage(Line)

    # My_Circle = Image('Circle', 10)
    # My_Circle.drawCircle(Vector2D(0, 0), 50)
    # wind.pushImage(My_Circle)

    # MLine = Line.copy('Mirror',1)
    # MLine.MirrorAxis(False, True)
    # wind.pushImage(MLine)

    # RLine = Line.copy('Rotation',1)
    # RLine.RotationAlf(45)
    # wind.pushImage(RLine)

    # SLine = Line.copy('Scale',-1)
    # SLine.setColor(QColor(0,0,255))
    # SLine.ScaleToPoint(10, 10)

    # # SLine.Translate(Vector2D(0,100))
    # # SLine.Translate(Vector2D(0,0))

    # # SLine.ScaleToPoint(10, 10, Vector2D(-15, 10))
    # # SLine.ScaleToPoint(10, 10, Vector2D(0, 0))
    # wind.pushImage(SLine)

    # MLine = SLine.copy('Move',1)
    # MLine.setColor(QColor(255,100,255))
    # MLine.Move(Vector2D(100, 100))
    # wind.pushImage(MLine)

    # MLine2 = MLine.copy('Move',1)
    # MLine2.setColor(QColor(255,100,255))
    # MLine2.Move(Vector2D(-100, 100))
    # wind.pushImage(MLine2)

    # MLine3 = MLine.copy('Move',1)
    # MLine3.setColor(QColor(255,100,255))
    # MLine3.Move(Vector2D(-100, -100))
    # wind.pushImage(MLine3)

    # MLine4 = MLine.copy('Move',1)
    # MLine4.setColor(QColor(255,100,255))
    # MLine4.Move(Vector2D(100, -100))
    # wind.pushImage(MLine4)


    # MLine5 = MLine.copy('Move',1)
    # MLine5.setColor(QColor(255,100,255))
    # MLine5.Move(Vector2D(0, 0))
    # wind.pushImage(MLine5)

    # SLine3 = Line.copy('Scale3',3)
    # SLine3.setColor(QColor(0,255,255))
    # SLine3.Scale(-10, -10)
    # SLine3.Shear(2,0)
    # wind.pushImage(SLine3)

    # SLine2 = SLine.copy(Layer=3)
    # SLine2.Scale(2,2)
    # SLine2.setColor(QColor(0,255,0))
    # wind.pushImage(SLine2)

    # SRCLine = Line.copy("SRC", 4)
    # SRCLine.Scale(20, 20)
    # SRCLine.RotationAlf(45)
    # SRCLine.setColor(QColor(255,0,255))
    # wind.pushImage(SRCLine)

    # SRCLine2 = SRCLine.copy("SRC2", 4)
    # SRCLine2.MirrorAxis(True,True)
    # SRCLine2.setColor(QColor(255,50,20))
    # wind.pushImage(SRCLine2)

    # SSLine = SRCLine2.copy("SS", 5)
    # # SSLine = Image("SS", 5)
    # # SSLine.drawLine(Vector2D(-5, 10), Vector2D(5,10), QColor(255,0,0))
    # SSLine.setColor(QColor(0,0,0))
    # #SSLine.Scale(20, 20)
    # #SSLine.Scale(1, -1)
    # wind.pushImage(SSLine)


    # # wind.pushAllImage([Line, MLine, RLine, SLine, SLine2, SRCLine, SRCLine2, SSLine]) 

    # wind.show() #Вывод окна приложения на экран
    # # wind.update()
    # sys.exit(app.exec_()) #Процесс завершения работы


