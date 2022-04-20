from PyQt6.QtCore import Qt, QPointF, QLineF
import numpy as np

def dist(p1, p2):
    return ((p1.x()-p2.x())**2+(p1.y()-p2.y())**2)**0.5

def validPoint(point, size):
    return 0<=point.x()<=size.width() and 0<=point.y()<=size.height()
def getProjection(a,b):
    return np.dot(a,b)/np.dot(b,b)
def withLength(x, h):
    return x/np.linalg.norm(x)*h
def translatePoint(p, editor):
    px = getProjection(p, withLength(editor.right, 1/editor.width))
    py = getProjection(p, withLength(editor.up, 1/editor.width))
    return QPointF(px, py)
def turnAroundX(beta, OY):
    length = np.linalg.norm(OY)
    cosA = OY[1]/length
    cosB = np.cos(beta)
    sinA = OY[2]/length
    sinB = np.sin(beta)
    cosAB = cosA*cosB-sinA*sinB
    sinAB = sinA*cosB+sinB*cosA
    return np.array([OY[0], length*cosAB, length*sinAB])
def turnAroundY(alpha, OX):
    length = np.linalg.norm(OX)
    cosA = OX[0]/length
    cosB = np.cos(alpha)
    sinA = OX[2]/length
    sinB = np.sin(alpha)
    cosAB = cosA*cosB-sinA*sinB
    sinAB = sinA*cosB+sinB*cosA
    return np.array([length*cosAB, OX[1], length*sinAB])
def clamp(val, m, M):
    return M if val > M else m if val < m else val



    
    
class Plane():
    def __init__(self, p1, p2, p3, relatively=False):
        self.anchor= p1
        #TODO: collinear check
        self.basis = (p2, p3) if relatively else (p2-p1,p3-p1)
        self.size = (np.linalg.norm(self.basis[0]), np.linalg.norm(self.basis[1]))
    def projectPoint(self, p):
        res= getProjection(p-self.anchor, self.basis[0])*self.basis[0]
        res+=getProjection(p-self.anchor, self.basis[1])*self.basis[1]
        res+=self.anchor
        return res
    def getCoords(self, p):
        return (getProjection(p-self.anchor, self.basis[0]), getProjection(p-self.anchor, self.basis[1]))
    def contains(self, p):
        coords = self.getCoords(p)
        return 0<=coords[0]<=1 and 0<=coords[1]<=1
    def intersectLine(self, line):
        p1 = line.anchor
        p2 = line.anchor+line.direction
        pr1 = self.projectPoint(p1)
        pr2 = self.projectPoint(p2)
        h1 = p1-pr1
        h2 = p2-pr2
        diag = p1-p2
        S = np.linalg.norm(diag)
        R = np.linalg.norm(h1)/np.linalg.norm(h2)
        if R+1<1e-7:
            return None
        b = 1/(1+R)
        I = p2 + diag * b
        if not self.contains(I):
            return None
        return I
class LineContainer():
    def __init__(self, ind1, ind2, drawMode):
        if drawMode not in ["sector", "line"]:
            raise Exception("wrong mode!")
        self.points = (ind1, ind2)
        self.drawMode = drawMode
        
class Line():
    def __init__(self, p1, p2):
        self.anchor = p1
        self.direction = p2-p1
        
