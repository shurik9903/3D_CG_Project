class Vector2D():
    def __init__(self, *xy):
        self.x = xy[0]
        self.y = xy[1]

    def __iter__(self):
         return iter(self.get())

    def get(self):
        return (self.x, self.y)

    def __str__(self) -> str:
        return f'{self.x}, {self.y}'
class Vector3D():
    def __init__(self, *xyz):
        self.x = xyz[0]
        self.y = xyz[1]
        self.z = xyz[2]

    def __iter__(self):
         return iter(self.get())

    def get(self):
        return (self.x, self.y, self.z)

    def __str__(self) -> str:
        return f'{self.x}, {self.y}, {self.z}'
