import numpy as np
from PyQt6.QtCore import Qt, QPointF, QLineF
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton
import geom as g

class Example(QWidget):
    
    def __init__(self):
        
        self.dots = []
        self.lines = []
        self.lastPos = QPointF(0, 0)
        self.lineDot = None
        self.currPoint = None
        self.currLines = []
        self.whichPoints = []
        super().__init__()
        self.initUI()


        

    def initUI(self):

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('Points')
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        #self.drawPoints(qp)
        self.drawLines(qp)
        qp.end()

    def mousePressEvent(self, e):
        self.lastPos = e.position()
        self.lastButton = e.button()
        if self.lastButton == Qt.MouseButton.RightButton:
            if self.lineDot:
                self.lines.append(QLineF(self.lineDot, e.position()))
            self.lineDot = e.position()
        elif self.lastButton == Qt.MouseButton.LeftButton:
            self.lineDot = None
            p = e.position()
            for line in self.lines:
                p1 = line.p1()
                p2 = line.p2()
                if g.dist(p, p1)<=16:
                    self.whichPoints.append(True)
                    self.currLines.append(line)
                elif g.dist(p, p2)<=16:
                    self.whichPoints.append(False)
                    self.currLines.append(line)
            for line in self.currLines:
                self.lines.remove(line)
                    
        self.update()
    def mouseReleaseEvent(self, e):
        if self.currLines:
            self.lines.extend(self.currLines)
        self.currLines = []
        self.whichPoints = []

        
    def wheelEvent(self, e):
        p = e.position()
        coeff = 1 + e.angleDelta().y() / 3600

        def expand(t):
            d = (t - p) * coeff
            return p + d

        self.dots = list(map(expand, self.dots))
        self.lines = list(map(lambda line: QLineF(
            expand(line.p1()), expand(line.p2())), self.lines))
        self.update()

    def mouseMoveEvent(self, e):
        if self.lastButton == Qt.MouseButton.LeftButton:
            if self.currLines:
                for i in range(len(self.currLines)):
                    self.currLines[i] = QLineF(e.position(), self.currLines[i].p2()) if self.whichPoints[i] else  QLineF(self.currLines[i].p1(), e.position())

        if self.lastButton == Qt.MouseButton.MiddleButton:
            offset = e.position() - self.lastPos
            self.dots = list(map(lambda t: t + offset, self.dots))
            self.lines = list(map(lambda t: QLineF(t.p1() + offset, t.p2() + offset), self.lines))

        self.lastPos = e.position()
        self.update()

    def drawPoints(self, qp):
        size = self.size()
        qp.setPen(QPen(Qt.GlobalColor.green, 5))

        for d in filter(lambda point: g.validPoint(point, size), self.dots):
            qp.drawEllipse(int(d.x()), int(d.y()), 3, 3)

    def drawLines(self, qp):
        #TODO: optimize lines
        qp.setPen(QPen(Qt.GlobalColor.red, 4))
        for d in self.lines:
            qp.drawLine(d)
        qp.setPen(QPen(Qt.GlobalColor.blue, 6))
        for d in self.lines:
            qp.drawEllipse(d.p1().x()-3, d.p1().y()-3, 6, 6)   
            qp.drawEllipse(d.p2().x()-3, d.p2().y()-3, 6, 6)
        qp.setPen(QPen(Qt.GlobalColor.red, 4))
        for d in self.currLines:
            qp.drawLine(d)
        qp.setPen(QPen(Qt.GlobalColor.blue, 6))
        for d in self.currLines:
            qp.drawEllipse(d.p1().x()-3, d.p1().y()-3, 6, 6)   
            qp.drawEllipse(d.p2().x()-3, d.p2().y()-3, 6, 6)

class Editor(QWidget):
    def __init__(self):

        self.right = np.array([1., 0., 0.])
        self.up = np.array([0., 1., 0.])
        self.axis = [np.array([50.,0.,0.]),np.array([0.,50.,0.]),np.array([0.,0.,50.])]
        
        self.initFigures()
        self.width= 5
        super().__init__()
        self.initUI()
        
    def initFigures(self):
        self.points = [np.array([20,20,20]),
                       np.array([20,20,10]),
                       np.array([10,20,20]),
                       np.array([20,10,20]),
                       np.array([20,10,10]),
                       np.array([10,20,10]),
                       np.array([10,10,20]),
                       np.array([10,10,10])]
        self.lines = []
        def connect(p1, p2):
            self.lines.append((self.points[p1], self.points[p2]))
        for i in 2,3,7:
            connect(6,i)
        for i in 1,3,7:
            connect(4,i)
        for i in 1,2,3:
            connect(0,i)
        for i in 2,7,1:
            connect(5, i)
        
        
    def initUI(self):

        self.setGeometry(640, 480, 640, 480)
        self.setWindowTitle('3D Editor')
        self.center = QPointF(320, 240)
        self.show()
    
    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        
        self.drawAxis(qp)
        self.drawLines(qp)
        self.drawPoints(qp)
        
        qp.end()
    def wheelEvent(self, e):        
        self.width += e.angleDelta().y() / 1000
        self.update()

    def mousePressEvent(self, e):
        self.lastPos = e.position()
        self.lastButton = e.button()                   
        self.update()
    def mouseMoveEvent(self, e):
        if self.lastButton == Qt.MouseButton.LeftButton:
            
            delta = e.position()-self.lastPos
            alpha = delta.x()/360
            beta = delta.y()/360
            
            self.up = g.turnAroundX(beta, self)
            self.right = g.turnAroundY(alpha, self)
            
        if self.lastButton==Qt.MouseButton.MiddleButton:
            self.center+=e.position()-self.lastPos
        self.lastPos = e.position()
        self.update()    
    def drawAxis(self, qp):
        
        cols = [Qt.GlobalColor.red,Qt.GlobalColor.yellow,Qt.GlobalColor.green]
        
        for a in self.axis:
            p = g.translatePoint(a, self)
            qp.setPen(QPen(cols[0], 2))
            line = QLineF(self.center, self.center+p)
            qp.drawLine(line)
            cols.append(cols.pop(0))
            
    def drawPoints(self, qp):
        for p in self.points:
            p = g.translatePoint(p, self)
            qp.setPen(QPen(Qt.GlobalColor.blue, 2))
            qp.drawEllipse(self.center+p, 3,3)
            
    def drawLines(self, qp):
        for t in self.lines:
            p1 = g.translatePoint(t[0], self)
            p2 = g.translatePoint(t[1], self)
            qp.setPen(QPen(Qt.GlobalColor.cyan, 2))
            qp.drawLine(QLineF(self.center+p1, self.center+p2))
            
        
if __name__ == "__main__":
    app = QApplication([])
    #ex = Example()
    ex2 = Editor()
    app.exec()
