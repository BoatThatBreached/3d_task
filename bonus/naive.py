import numpy as np
from PyQt6.QtCore import Qt, QPointF, QLineF
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtWidgets import QWidget
import geom as g


class Editor(QWidget):
    def __init__(self):

        self.right = np.array([1., 0., 0.])
        self.up = np.array([0., 1., 0.])
        self.axis = [np.array([50., 0., 0.]), np.array([0., 50., 0.]), np.array([0., 0., 50.])]

        self.initFigures()
        self.width = 5
        super().__init__()
        self.initUI()

    def initFigures(self):
        self.points = [np.array([20, 20, 20]),
                       np.array([20, 20, 10]),
                       np.array([10, 20, 20]),
                       np.array([20, 10, 20]),
                       np.array([20, 10, 10]),
                       np.array([10, 20, 10]),
                       np.array([10, 10, 20]),
                       np.array([10, 10, 10])]
        self.lines = []

        def connect(p1, p2):
            self.lines.append((self.points[p1], self.points[p2]))

        for i in 2, 3, 7:
            connect(6, i)
        for i in 1, 3, 7:
            connect(4, i)
        for i in 1, 2, 3:
            connect(0, i)
        for i in 2, 7, 1:
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
            delta = e.position() - self.lastPos
            alpha = delta.x() / 360
            beta = delta.y() / 360

            self.up = g.turn_around_x(beta, self.up)
            self.right = g.turn_around_y(alpha, self.right)

        if self.lastButton == Qt.MouseButton.MiddleButton:
            self.center += e.position() - self.lastPos
        self.lastPos = e.position()
        self.update()

    def drawAxis(self, qp):

        cols = [Qt.GlobalColor.red, Qt.GlobalColor.yellow, Qt.GlobalColor.green]

        for a in self.axis:
            p = g.translate_point(a, self)
            qp.setPen(QPen(cols[0], 2))
            line = QLineF(self.center, self.center + p)
            qp.drawLine(line)
            cols.append(cols.pop(0))

    def drawPoints(self, qp):
        for p in self.points:
            p = g.translate_point(p, self)
            qp.setPen(QPen(Qt.GlobalColor.blue, 2))
            qp.drawEllipse(self.center + p, 3, 3)

    def drawLines(self, qp):
        for t in self.lines:
            p1 = g.translate_point(t[0], self)
            p2 = g.translate_point(t[1], self)
            qp.setPen(QPen(Qt.GlobalColor.cyan, 2))
            qp.drawLine(QLineF(self.center + p1, self.center + p2))
