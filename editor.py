# print('this is the editor')
import random

import PyQt6.QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton

import sys  # Только для доступа к аргументам командной строки


class Example(QWidget):

    @staticmethod
    def getLine(x, y):
        return PyQt6.QtCore.QLineF(x, y)

    @staticmethod
    def getPoint(x, y):
        return PyQt6.QtCore.QPointF(x, y)

    def __init__(self):
        
        self.dots = []
        self.lines = []
        self.lastPos = self.getPoint(0, 0)
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
                self.lines.append(self.getLine(self.lineDot, e.position()))
            self.lineDot = e.position()
##            if not self.lineDot:
##                self.lineDot = e.position()
##            else:
##                self.lines.append(self.getLine(self.lineDot, e.position()))
##                self.lineDot = None
        elif self.lastButton == Qt.MouseButton.LeftButton:
            self.lineDot = None
            def dist(p1, p2):
                return ((p1.x()-p2.x())**2+(p1.y()-p2.y())**2)**0.5
            p = e.position()
            for line in self.lines:
                p1 = line.p1()
                p2 = line.p2()
                if dist(p, p1)<=16:
                    #self.lines.remove(line)
                    self.whichPoints.append(True)
                    self.currLines.append(line)
                elif dist(p, p2)<=16:
                    #self.lines.remove(line)
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
        self.lines = list(map(lambda line: self.getLine(
            expand(line.p1()), expand(line.p2())), self.lines))
        self.update()

    def mouseMoveEvent(self, e):
        if self.lastButton == Qt.MouseButton.LeftButton:
            if self.currLines:
                for i in range(len(self.currLines)):
                    self.currLines[i] = self.getLine(e.position(), self.currLines[i].p2()) if self.whichPoints[i] else  self.getLine(self.currLines[i].p1(), e.position())

            #self.dots.append(e.position())
        if self.lastButton == Qt.MouseButton.MiddleButton:
            offset = e.position() - self.lastPos
            self.dots = list(map(lambda t: t + offset, self.dots))
            self.lines = list(map(lambda t: self.getLine(t.p1() + offset, t.p2() + offset), self.lines))

        self.lastPos = e.position()
        self.update()

    def drawPoints(self, qp):
        size = self.size()
        qp.setPen(QPen(Qt.GlobalColor.green, 5))

        for d in filter(lambda point: not (point.x() < 0 or point.x() > size.width() \
                                      or point.y() < 0 or point.y() > size.height()), self.dots):
            qp.drawEllipse(d.x(), d.y(), 3, 3)

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

if __name__ == "__main__":
    # Приложению нужен один (и только один) экземпляр QApplication.
    # Передаём sys.argv, чтобы разрешить аргументы командной строки для приложения.
    # Если не будете использовать аргументы командной строки, QApplication([]) тоже работает
    app = QApplication(sys.argv)

    # Создаём виджет Qt — окно.
    ex = Example()

    app.exec()
