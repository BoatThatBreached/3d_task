from PyQt6.QtCore import Qt, QPointF, QLineF
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtWidgets import QWidget
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
        # self.drawPoints(qp)
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
                if g.dist(p, p1) <= 16:
                    self.whichPoints.append(True)
                    self.currLines.append(line)
                elif g.dist(p, p2) <= 16:
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
                    self.currLines[i] = QLineF(e.position(), self.currLines[i].p2()) if self.whichPoints[i] else QLineF(
                        self.currLines[i].p1(), e.position())

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
        # TODO: optimize lines
        qp.setPen(QPen(Qt.GlobalColor.red, 4))
        for d in self.lines:
            qp.drawLine(d)
        qp.setPen(QPen(Qt.GlobalColor.blue, 6))
        for d in self.lines:
            qp.drawEllipse(d.p1().x() - 3, d.p1().y() - 3, 6, 6)
            qp.drawEllipse(d.p2().x() - 3, d.p2().y() - 3, 6, 6)
        qp.setPen(QPen(Qt.GlobalColor.red, 4))
        for d in self.currLines:
            qp.drawLine(d)
        qp.setPen(QPen(Qt.GlobalColor.blue, 6))
        for d in self.currLines:
            qp.drawEllipse(d.p1().x() - 3, d.p1().y() - 3, 6, 6)
            qp.drawEllipse(d.p2().x() - 3, d.p2().y() - 3, 6, 6)

