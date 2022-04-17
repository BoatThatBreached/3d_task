#print('this is the editor')
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
        super().__init__()
        self.initUI()

        self.dots = []
        self.lastPos = self.getPoint(0, 0)

        self.lines = []
        self.lineDot = None

    def initUI(self):

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('Points')
        self.show()


    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawPoints(qp)
        self.drawLines(qp)
        qp.setPen(QPen(Qt.GlobalColor.red, 8))
        qp.end()


    def mousePressEvent(self, e):
        self.lastPos = e.position()
        self.lastButton = e.button()
        if self.lastButton == Qt.MouseButton.RightButton:
            if not self.lineDot:
                self.lineDot = e.position()
            else:
                self.lines.append(self.getLine(self.lineDot, e.position()))
                self.lineDot = None
        self.update()

    def wheelEvent(self, e):
        p = e.position()
        coeff = 1+e.angleDelta().y()/3600
        def expand(t):
            d = (t - p) * coeff
            return p + d
        self.dots = list(map(expand, self.dots))
        self.lines = list(map(lambda line: self.getLine(
            expand(line.p1()), expand(line.p2())), self.lines))
        self.update()
        

    def mouseMoveEvent(self, e):
        if self.lastButton == Qt.MouseButton.LeftButton:
            self.dots.append(e.position())
        if self.lastButton == Qt.MouseButton.MiddleButton:
            offset = e.position() - self.lastPos
            self.dots = list(map(lambda t: t + offset, self.dots))
            self.lines = list(map(lambda t: self.getLine(t.p1() + offset, t.p2() + offset), self.lines))
        
        self.lastPos = e.position()
        self.update()

    def drawPoints(self, qp):
        qp.setPen(QPen(Qt.GlobalColor.green, 5))
        for d in self.dots:
            qp.drawEllipse(d.x(), d.y(), 3, 3)


    def drawLines(self, qp):
        qp.setPen(QPen(Qt.GlobalColor.red, 5))
        for d in self.lines:
            qp.drawLine(d)



if __name__ == "__main__":
    # Приложению нужен один (и только один) экземпляр QApplication.
    # Передаём sys.argv, чтобы разрешить аргументы командной строки для приложения.
    # Если не будете использовать аргументы командной строки, QApplication([]) тоже работает
    app = QApplication(sys.argv)

    # Создаём виджет Qt — окно.
    ex = Example()

    app.exec()
