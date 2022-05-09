
import numpy as np
from My_Vectors import *
from DLL import *

def Cross(v1, v2) -> float:

    if isinstance(v1, Vector2D) and isinstance(v2, Vector2D):
        return np.linalg.det([[v1.x , v1.y],[v2.x, v2.y]])

    if isinstance(v1, Vector3D) and isinstance(v2, Vector3D):

        i = np.linalg.det([[v1.y, v1.z],[v2.y, v2.z]])
        j = np.linalg.det([[v1.x, v1.z],[v2.x, v2.z]])
        k = np.linalg.det([[v1.x, v1.y],[v2.x, v2.y]])

        

        return abs(np.dot([i, -j, k],[v1.x , v1.y, v1.z]))

    return None


def IsPointInTriangle( p:Vector2D, a:Vector2D, b:Vector2D, c:Vector2D):

    ab = b - a 
    bc = c - b
    ca = a - c

    ap = p - a
    bp = p - b
    cp = p - c

    cross1 = Cross(ab, ap)
    cross2 = Cross(bc, bp)
    cross3 = Cross(ca, cp)

    if cross1 > 0.0 or cross2 > 0.0 or cross3 > 0.0:
        return False
    
    return True

def Triangulation(Face: DLL):
    
    All_Face = Face.copy()

    All = []

    va = All_Face.head.next
    vb = va.prev
    vc = va.next

    while All_Face.size > 3:
        
        if va:
            va = All_Face.head.next

        vb = va.get_prev()
        vc = va.get_next()


        va_vb = vb.data - va.data
        va_vc = vc.data - va.data

        if Cross(va_vb, va_vc) < 0.0:
            va = va.next
            continue
    
        p  = vc.get_next()

        while (p == va or p == vb or p == vc) and not IsPointInTriangle(p.data, vb.data, va.data, vc.data):
            p = p.get_next()

        All.append((vb.data, va.data, vc.data))
        All_Face.pop(va)
    
        va = va.next

    return All