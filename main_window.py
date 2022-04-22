from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QToolBar, QApplication

from isometric import IsometricEditor
from ui_widgets.windows import AddPointWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Isometric 3d editor")

        self.layout = QVBoxLayout()
        #self.widgets = UIWidgets()

        #self.widgets.pointAddWindow.hide()
        #self.layout.addWidget(self.widgets.pointAddWindow)

        #self.layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.editor = IsometricEditor("black")
        self.editor.setLayout(self.layout)

        toolbar = ToolBar("My main toolbar", self)

        # Устанавливаем центральный виджет окна. Виджет будет расширяться по умолчанию,
        # заполняя всё пространство окна.
        self.setCentralWidget(self.editor)
        self.setGeometry(200, 200, 640, 480)
        self.setWindowTitle('Isometric 3D Editor')
        self.addToolBar(toolbar)
        self.windows = list()

        menu = self.menuBar()

        button_action = QAction(QIcon("bug.png"), "Add points", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.OpenAddPointWindow)
        button_action.setCheckable(True)

        file_menu = menu.addMenu("Geometry")
        file_menu.addAction(button_action)

    def OpenAddPointWindow(self, s):
        if len(list(filter(lambda x: type(x) == AddPointWindow, self.windows))) == 0:
            t = AddPointWindow(self)
            self.windows.append(t)
            t.show()


class ToolBar(QToolBar):
    def __init__(self, name, mainWindow):
        super().__init__(name)

        button_action = QAction(QIcon("icons/Point_Icon.svg"), "Add point", self)
        button_action.setStatusTip("This is your button")
        #button_action.triggered.connect(lambda s: self.onMyToolBarButtonClick(s, mainWindow))

        self.setIconSize(QSize(20, 20))
        self.addAction(button_action)





