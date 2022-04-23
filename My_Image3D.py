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

        self.Origin = None

        self.PixelBuffer = {}

    def getPixel(self, x:int, y:int, z:int) -> Pixel3D:
        return self.PixelBuffer.get(x, {}).get(y, {}).get(z, None)

    def getArrayPixel(self) -> list[Pixel3D]:
        return [Pixel3D(Vector3D(i, j, l), v3) for i, v1 in self.PixelBuffer.items() for j,v2 in v1.items() for l,v3 in v2.items()]

    def setPixel(self, pixel:Pixel3D):
        x = pixel.x
        y = pixel.y
        z = pixel.z
        self.PixelBuffer.setdefault(x, {}).setdefault(y, {})[z] = pixel.color
    
    def putArray(self, Array:list[Pixel3D]):
        for pixel in Array:
            if isinstance(pixel, Pixel3D):
                self.setPixel(pixel)

    def __getitem__(self, x:int, y:int, z:int) -> Pixel:
        return self.getPixel(x, y, z)

    def recalculateSize(self) -> tuple:

        min_x, max_x = min(self.PixelBuffer), max(self.PixelBuffer)

        first_y = next(iter(list(self.PixelBuffer.values())[0]))
        min_y, max_y = first_y, first_y

        first_z = next(iter(list(list(self.PixelBuffer.values())[0].values())[0]))
        min_z, max_z = first_z, first_z

        for value in self.PixelBuffer.values():
            for j in value:
                min_y,max_y = min(j,min_y), max(j,max_y)

        for value in list(self.PixelBuffer.values()):
            for j in value.values():
                for l in j:
                    min_z,max_z = min(l,min_z), max(l,max_z)

        self.Width = abs(max_x - min_x)+1 if not max_x == min_x else 1
        self.Height = abs(max_y - min_y)+1 if not max_y == min_y else 1
        self.Depth = abs(max_z - min_z)+1 if not max_z == min_z else 1 

        return (max_x, min_x, max_y, min_y, max_z, min_z)

    def drawLine3D(self, vec0: Vector3D, vec1: Vector3D, color: QColor = QColor(0,0,0)):
        SDraw = super().drawLine3D(vec0, vec1, color)
        self.putArray(SDraw)
        return SDraw

    def draw3DBox(self, center: Vector3D, size: int, color: QColor = QColor(0,0,0)) -> list[Pixel]:
        self.Origin = center
        SDraw = super().draw3DBox(center, size, color)
        self.putArray(SDraw)
        return SDraw

    def Rotation3DAlf(self, alf=0, Axis: str = 'x', origin:Vector3D = None) :
        # return super().Rotation3DAlf(vec3d, alf, Axis)

        if origin is None:
            origin = self.Origin

        new_buffer = []

        for i, v1 in self.PixelBuffer.items():
            for j,v2 in v1.items():
                for l, v3 in v2.items():
                    new_buffer.append(Pixel3D(super().Rotation3DAlf(Vector3D(i, j, l), alf, Axis, origin), color = v3))

        self.PixelBuffer.clear()
        self.putArray(new_buffer)

    def copy(self, Name:str = None, Layer:int = None): #Копия
        new_cls = Image3D(self.Name if Name == None else Name, \
        self.Layer if Layer == None else Layer)

        new_cls.ScaleWidth = self.ScaleWidth
        new_cls.ScaleHeight = self.ScaleHeight
        new_cls.ScaleDepth = self.ScaleDepth

        new_cls.Width = self.Width
        new_cls.Height = self.Height
        new_cls.Depth = self.Depth

        new_cls.PixelBuffer = deepcopy(self.PixelBuffer)
        return new_cls