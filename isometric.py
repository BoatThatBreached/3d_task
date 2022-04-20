import numpy as np
from PyQt6.QtCore import Qt, QPointF, QLineF
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtWidgets import QApplication, QWidget
import geom as g


class IsometricEditor(QWidget):
    def __init__(self):
        self.lines = []
        self.initFigures()
        self.corner = QPointF(0, 480)
        self.origin = np.array([320, 240, 0])
        self.screen = g.Plane(np.array([-320, -240, 0]) + self.origin, np.array([640, 0, 0]), np.array([0, 480, 0]),
                              True)
        self.camera = np.array([0., 0., -30.])
        self.scale = 30
        self.intensity = 200
        self.chosenPoint = None
        self.lastPos = None
        self.lastButton = None
        super().__init__()

        self.init_UI()

    def init_UI(self):
        self.setGeometry(200, 200, 640, 480)
        self.setWindowTitle('Isometric 3D Editor')
        self.show()

    def initFigures(self):
        self.points = []

        def addP(x, y, z):
            self.points.append(np.array([x, y, z]))

        addP(-3, 0, -2)
        addP(3, 0, -2)
        addP(0, 5, -2)
        addP(0, -1, 2)

        self.connections = []

        def connect(p1, p2):
            self.connections.append((p1, p2))

        connect(0, 1)
        connect(0, 2)
        connect(0, 3)
        connect(1, 2)
        connect(1, 3)
        connect(2, 3)
        self.reconnect_lines()

    def reconnect_lines(self):
        self.lines = []
        for t in self.connections:
            self.lines.append((self.points[t[0]], self.points[t[1]]))

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_lines(qp)
        self.draw_points(qp)
        qp.end()

    def wheelEvent(self, e):
        self.scale += e.angleDelta().y() / 200
        self.update()

    def mousePressEvent(self, e):
        self.lastPos = e.position()
        self.lastButton = e.button()
        pos = np.array([e.position().x(), self.corner.y() - e.position().y(), 0])

        if self.lastButton == Qt.MouseButton.RightButton:
            for p in self.points:
                line = g.Line(self.camera + self.origin, p + self.origin)
                i = self.screen.intersectLine(line)
                if i is None:
                    continue
                i = (i - self.origin) * self.scale + self.origin
                i[2] = 0
                if np.linalg.norm(pos - i) < 4:
                    self.chosenPoint = p
                    break
        self.update()

    def mouseMoveEvent(self, e):
        delta = e.position() - self.lastPos
        if self.lastButton == Qt.MouseButton.LeftButton:
            alpha = -delta.y() / self.intensity
            beta = delta.x() / self.intensity
            for i in range(len(self.points)):
                self.points[i] = g.turnAroundX(alpha, g.turnAroundY(beta, self.points[i]))
            self.reconnect_lines()

        if self.lastButton == Qt.MouseButton.MiddleButton:
            pass

        self.lastPos = e.position()
        self.update()

    def draw_points(self, qp):

        for p in self.points:
            qp.setPen(QPen(Qt.GlobalColor.blue, 2))
            line = g.Line(self.camera + self.origin, p + self.origin)
            i = self.screen.intersectLine(line)
            if i is None:
                continue
            i = (i - self.origin) * self.scale + self.origin
            point = QPointF(i[0], self.corner.y() - i[1])

            # if type(self.chosenPoint)!=type(None) and np.linalg.norm(p-self.chosenPoint)<2:
            # qp.setPen(QPen(Qt.GlobalColor.red, 2))
            qp.drawEllipse(point, 3, 3)

    def draw_lines(self, qp):
        qp.setPen(QPen(Qt.GlobalColor.cyan, 2))
        for t in self.lines:
            line1 = g.Line(self.camera + self.origin, t[0] + self.origin)
            line2 = g.Line(self.camera + self.origin, t[1] + self.origin)
            i1 = self.screen.intersectLine(line1)
            if i1 is None:
                continue
            i2 = self.screen.intersectLine(line2)
            if i2 is None:
                continue
            i1 = (i1 - self.origin) * self.scale + self.origin
            i2 = (i2 - self.origin) * self.scale + self.origin
            point1 = QPointF(i1[0], self.corner.y() - i1[1])
            point2 = QPointF(i2[0], self.corner.y() - i2[1])
            qp.drawLine(QLineF(point1, point2))