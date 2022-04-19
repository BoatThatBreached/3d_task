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
def turnAroundX(beta, editor):
    length = np.linalg.norm(editor.up)
    cosA = editor.up[1]/length
    cosB = np.cos(beta)
    sinA = editor.up[2]/length
    sinB = np.sin(beta)
    cosAB = cosA*cosB-sinA*sinB
    sinAB = sinA*cosB+sinB*cosA
    return np.array([0, length*cosAB, length*sinAB])
def turnAroundY(alpha, editor):
    length = np.linalg.norm(editor.right)
    cosA = editor.right[0]/length
    cosB = np.cos(alpha)
    sinA = editor.right[2]/length
    sinB = np.sin(alpha)
    cosAB = cosA*cosB-sinA*sinB
    sinAB = sinA*cosB+sinB*cosA
    return np.array([length*cosAB, 0, length*sinAB])
