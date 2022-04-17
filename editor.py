#print('this is the editor')
import random

import PyQt6.QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton

import sys  # Только для доступа к аргументам командной строки


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.dots = []
        self.initUI()
        self.lastPos = PyQt6.QtCore.QPointF(0, 0)

    def initUI(self):

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('Points')
        self.show()


    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawPoints(qp)
        qp.setPen(QPen(Qt.GlobalColor.red, 8))
        qp.end()


    def mousePressEvent(self, e):
        self.lastPos = e.position()
        self.lastButton = e.button()
    def wheelEvent(self, e):
        p = (e.position().x(), e.position().y())
        coeff = 1+e.angleDelta().y()/3600
        def sc(t):
            d = ((t[0]-p[0])*coeff, (t[1]-p[1])*coeff)
            return (p[0]+d[0], p[1]+d[1])
        self.dots = list(map(sc, self.dots))
        self.update()
        
        
        

    def mouseMoveEvent(self, e):
        if self.lastButton == Qt.MouseButton.LeftButton:
            self.dots.append((e.position().x(), e.position().y()))
        if self.lastButton == Qt.MouseButton.MiddleButton:
            offset = (e.position().x()-self.lastPos.x(), e.position().y()-self.lastPos.y())
            self.dots = list(map(lambda t: (t[0]+offset[0], t[1]+offset[1]), self.dots))
        
        self.lastPos = e.position()
        self.update()

    def drawPoints(self, qp):
        qp.setPen(QPen(Qt.GlobalColor.green, 5))
        for d in self.dots:
            qp.drawEllipse(d[0], d[1], 3, 3)



if __name__ == "__main__":
    # Приложению нужен один (и только один) экземпляр QApplication.
    # Передаём sys.argv, чтобы разрешить аргументы командной строки для приложения.
    # Если не будете использовать аргументы командной строки, QApplication([]) тоже работает
    app = QApplication(sys.argv)

    # Создаём виджет Qt — окно.
    ex = Example()

    app.exec()
