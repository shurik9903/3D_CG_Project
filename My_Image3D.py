from My_Draw import *

class Image3D(DrawTool, Matrix_Work):
    def __init__(self, Name:str = "", Layer:int = 0):
        self.Name = Name
        self.Layer = Layer
        self.ScaleWidth = 1
        self.ScaleHeight = 1
        self.ScaleDepth = 1
        self.Width = None
        self.Height = None
        self.Depth = None
        self.PixelBuffer = {}

    def getPixel(self, x:int, y:int, z:int) -> Pixel:
        return self.PixelBuffer.get(x, {}).get(y, {}).get(z, None)

    def getArrayPixel(self) -> list[Pixel]:
        return [Pixel(Vector2D(i, j, l), v3) for i, v1 in self.PixelBuffer.items() for j,v2 in v1.items() for l,v3 in v2.items()]

    def setPixel(self, pixel:Pixel):
        x = pixel.x
        y = pixel.y
        self.PixelBuffer.setdefault(x, {})[y] = pixel.color