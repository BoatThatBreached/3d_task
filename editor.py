#print('this is the editor')
import random

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton

import sys  # Только для доступа к аргументам командной строки


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.dots = []
        self.initUI()


    def initUI(self):

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('Points')
        self.show()


    def paintEvent(self, e):

        qp = QPainter()
        qp.begin(self)
        self.drawPoints(qp)
        qp.setPen(QPen(Qt.GlobalColor.red, 8))
        #qp.drawEllipse(100, 100, 50, 60)
        qp.end()
        
    def mouseMoveEvent(self, e):
        self.dots.append((int(e.position().x()), int(e.position().y())))
        self.paintEvent(e)
    def mouseReleaseEvent(self, e):
        self.paintEvent(e)
        

    def drawPoints(self, qp):

        qp.setPen(QPen(Qt.GlobalColor.green, 5))
        size = self.size()

        for d in self.dots:
            qp.drawEllipse(d[0], d[1], 3,3)



if __name__ == "__main__":
    # Приложению нужен один (и только один) экземпляр QApplication.
    # Передаём sys.argv, чтобы разрешить аргументы командной строки для приложения.
    # Если не будете использовать аргументы командной строки, QApplication([]) тоже работает
    app = QApplication(sys.argv)

    # Создаём виджет Qt — окно.
    ex = Example()

    app.exec()
