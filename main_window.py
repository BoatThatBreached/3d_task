from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QToolBar

from isometric import IsometricEditor
from ui_widgets.windows import AddPointWindow, AddLineWindow, AddPlaneWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Isometric 3d editor")

        self.layout = QVBoxLayout()
        # self.widgets = UIWidgets()

        # self.widgets.pointAddWindow.hide()
        # self.layout.addWidget(self.widgets.pointAddWindow)

        # self.layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
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

        self.menu = self.menuBar()
        self.geometry_menu = self.menu.addMenu("Geometry")

        self.form_geometry_menu(self.geometry_menu)

    def form_geometry_menu(self, menu):
        add_point = MenuAction("Add points", self,
                               status_tip="Add some points",
                               func=lambda s: self.open_window(s, AddLineWindow),
                               )

        add_line = MenuAction("Add line", self,
                              status_tip="Add some lines",
                              func=lambda s: self.open_window(s, AddPointWindow)
                              )

        add_plane = MenuAction("Add plane", self,
                              status_tip="Add some planes",
                              func=lambda s: self.open_window(s, AddPlaneWindow)
                              )

        menu.addActions([add_point, add_line, add_plane])

    def open_window(self, s, window):
        if len(list(filter(lambda x: type(x) == window, self.windows))) == 0:
            t = window(self)
            self.windows.append(t)
            t.show()


class MenuAction(QAction):
    def __init__(self, *args, status_tip=None, func=None):
        super().__init__(*args)
        self.setStatusTip(status_tip)
        self.triggered.connect(func)


class ToolBar(QToolBar):
    def __init__(self, name, mainWindow):
        super().__init__(name)

        button_action = QAction(QIcon("icons/Point_Icon.svg"), "Add point", self)
        button_action.setStatusTip("This is your button")
        # button_action.triggered.connect(lambda s: self.onMyToolBarButtonClick(s, mainWindow))

        self.setIconSize(QSize(20, 20))
        self.addAction(button_action)
