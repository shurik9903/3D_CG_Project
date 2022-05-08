from My_Draw import *
from DLL import *
class Image3D_2():
    def __init__(self, Name:str = "", Layer:int = 0, Color:QColor = QColor(0,0,0)):
        self.Name = Name
        self.Layer = Layer
        
        self.Vertex = {'id':{},'vertex':{}}
        self.Edge = {'id':{},'Edge':{}}
        self.Face = {'id':{},'Face':{}}

        self.Color = Color

        self.Origin = None

    def AddVertex(self, vert:Vector3D):
        
        if isinstance(vert, list):
            for v in vert:
                self.AddVertex(v)
            return vert

        if vert in self.Vertex['vertex']:
            return vert

        i = 1
        while (True):
            if i not in self.Vertex['id']:
                self.Vertex['id'][i] = vert
                self.Vertex['vertex'][vert] = i
                break
            i += 1

        return vert

    def AddEdge(self, vert1:Vector3D, vert2:Vector2D):

        self.AddVertex([vert1, vert2])
        
        edge = (vert1,vert2)

        if edge in self.Edge['Edge']:
            return [vert1, vert2]

        i = 1
        while (True):
            if i not in self.Edge['id']:
                self.Edge['id'][i] = edge
                self.Edge['Edge'][edge] = i
                break
            i += 1

        return [vert1, vert2]

    def SetFace(self, Face:DLL):

        if Face in self.Face['Face']:
            return Face

        i = 1
        while (True):
            if i not in self.Face['id']:
                self.Face['id'][i] = Face
                self.Face['Face'][Face] = i
                break
            i += 1

        return Face

    def Create3DBox(self, center: Vector3D, size: int, ):
        self.Origin = center
        

        BoxVertex = [Vector3D(center.x - size, center.y - size, center.z - size),
                    Vector3D(center.x + size, center.y - size, center.z - size),
                    Vector3D(center.x + size, center.y + size, center.z - size),
                    Vector3D(center.x - size, center.y + size, center.z - size),
                    Vector3D(center.x - size, center.y - size, center.z + size),
                    Vector3D(center.x + size, center.y - size, center.z + size),
                    Vector3D(center.x + size, center.y + size, center.z + size),
                    Vector3D(center.x - size, center.y + size, center.z + size)]

        for i in range(0, 4):
            self.AddEdge(BoxVertex[i], BoxVertex[(i+1)%4])
            self.AddEdge(BoxVertex[i+4], BoxVertex[((i+1) % 4) + 4])
            self.AddEdge(BoxVertex[i], BoxVertex[i+4])

        # for i in range(2):
        #     for j in range(2):
        #         for k in range(2):
        #             print



        self.SetFace( DLL((BoxVertex[0], BoxVertex[1],BoxVertex[2], BoxVertex[3])) )
        self.SetFace( DLL((BoxVertex[4], BoxVertex[5],BoxVertex[6], BoxVertex[7])) )

        self.SetFace( DLL((BoxVertex[0], BoxVertex[1],BoxVertex[4], BoxVertex[5])) )
        self.SetFace( DLL((BoxVertex[2], BoxVertex[3],BoxVertex[6], BoxVertex[7])) )
    
        self.SetFace( DLL((BoxVertex[0], BoxVertex[3],BoxVertex[4], BoxVertex[7])) )
        self.SetFace( DLL((BoxVertex[1], BoxVertex[2],BoxVertex[5], BoxVertex[6])) )

    def RewritVertex(self, id, vertex):
        pass

    def Rotation(self, rotation:Vector3D, origin:Vector3D = None):
        if origin is None:
            origin = self.Origin

        for i in self.Vertex['vertex'].keys():
            i.x, i.y, i.z = Matrix_Work().Rotation3DAlf(i, rotation, origin).get()

    # def Triangle(self):
    #     All = []

    #     for i in self.Face['Face'].keys():
    #         # All.append([])
    #         # print(i)
            


    # def Fill(self, ):
    #     pass

    # def Draw(self) -> list[Pixel3D]:
        
    #     All = []
    #     for edge in self.Edge['Edge'].keys():
    #         All.extend(DrawTool().drawLine3D(*edge,self.Color))
            
    #     self.Triangle()
    #     return All

    def __str__(self) -> str:
        return str(f'Vertex:\n{self.Vertex}\n Edge:\n{self.Edge}\n Face:\n{self.Face}\n')