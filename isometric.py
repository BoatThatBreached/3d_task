import numpy as np
from PyQt6.QtCore import Qt, QPointF, QLineF, QRectF
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtWidgets import QWidget
import geom as g


class IsometricEditor(QWidget):
    def __init__(self, theme="black"):
        self.theme = theme
        self.lines = []
        self.connections = []
        self.points = []
        self.init_figures()
        self.corner = QPointF(0, 480)
        self.origin = np.array([320, 240, 0])
        self.screen = g.Plane(np.array([-320, -240, 0]) + self.origin, np.array([640, 0, 0]), np.array([0, 480, 0]),
                              True)
        self.camera = np.array([0., 0., 30.])
        self.scale = 30
        self.intensity = 200
        self.chosenPoint = None
        self.lastPos = None
        self.lastButton = None

        self.axis = [np.array([10, 0, 0]), np.array([0, 10, 0]), np.array([0, 0, 10])]

        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setGeometry(200, 200, 640, 480)
        self.setWindowTitle('Isometric 3D Editor')
        self.show()

    def init_figures(self):
        self.points = []

        def add_p(x, y, z):
            self.points.append(np.array([x, y, z]))

        add_p(-3., 0., -2.)
        add_p(3., 0., -2.)
        add_p(0., 5., -2.)
        add_p(0., -1., 2.)

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
        self.draw_background(qp)
        self.draw_axis(qp)
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
                i = self.screen.intersect_line(line)
                if i is None:
                    continue
                i = (i - self.origin) * self.scale + self.origin
                i[2] = 0
                if np.linalg.norm(pos - i) < 4:
                    self.chosenPoint = p
                    break
        self.update()

    def mouseReleaseEvent(self, e):
        self.lastButton = Qt.MouseButton.NoButton

    def mouseMoveEvent(self, e):
        delta = e.position() - self.lastPos
        if self.lastButton == Qt.MouseButton.LeftButton:
            alpha = -delta.y() / self.intensity
            beta = delta.x() / self.intensity
            for i in range(len(self.points)):
                self.points[i] = g.turnAroundX(alpha, g.turnAroundY(beta, self.points[i]))
            for i in range(len(self.axis)):
                self.axis[i] = g.turnAroundX(alpha, g.turnAroundY(beta, self.axis[i]))

        if self.lastButton == Qt.MouseButton.MiddleButton:
            pass

        self.lastPos = e.position()
        self.reconnect_lines()
        self.update()

    def draw_background(self, qp):
        if self.theme == "black":
            qp.fillRect(0,0,self.size().width().real, self.size().height().real, Qt.GlobalColor.black)

    def draw_axis(self, qp):
        colors = [Qt.GlobalColor.red, Qt.GlobalColor.blue, Qt.GlobalColor.green]
        for i in range(len(self.axis)):
            qp.setPen(QPen(colors[i], 2))
            line1 = g.Line(self.axis[i] + self.origin, self.origin)
            line2 = g.Line(self.origin, self.origin)
            i1 = self.screen.intersect_line(line1)
            if type(i1) is g.Line:
                i1 = i1.anchor
            if i1 is None:
                continue
            i2 = self.screen.intersect_line(line2)
            if type(i2) is g.Line:
                i2 = i2.anchor
            if i2 is None:
                continue
            i1 = (i1 - self.origin) * self.scale + self.origin
            i2 = (i2 - self.origin) * self.scale + self.origin
            point1 = QPointF(i1[0], self.corner.y() - i1[1])
            point2 = QPointF(i2[0], self.corner.y() - i2[1])
            qp.drawLine(QLineF(point1, point2))
            qp.drawEllipse(point1, 3,3)

    def draw_points(self, qp):
        for p in self.points:
            qp.setPen(QPen(Qt.GlobalColor.blue, 2))
            line = g.Line(self.camera + self.origin, p + self.origin)
            i = self.screen.intersect_line(line)
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
            i1 = self.screen.intersect_line(line1)
            if i1 is None:
                continue
            i2 = self.screen.intersect_line(line2)
            if i2 is None:
                continue
            i1 = (i1 - self.origin) * self.scale + self.origin
            i2 = (i2 - self.origin) * self.scale + self.origin
            point1 = QPointF(i1[0], self.corner.y() - i1[1])
            point2 = QPointF(i2[0], self.corner.y() - i2[1])
            qp.drawLine(QLineF(point1, point2))
