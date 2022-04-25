from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QToolBar, QPushButton

from isometric import IsometricEditor
from ui_widgets.toolbar import ToolBar, on_click_event
from ui_widgets.windows import AddPointWindow, AddLineWindow, AddPlaneWindow

action_buttons = [
    ("ui_widgets/icons/Point.svg", on_click_event, "add_point"),
    ("ui_widgets/icons/Plane.svg", on_click_event, "add_plane"),
    ("ui_widgets/icons/Moving.svg", on_click_event, "moving"),
    ("ui_widgets/icons/Rotation.svg", on_click_event, "rotation"),
    ("ui_widgets/icons/Segment.svg", on_click_event, "add_line"),
]

color_buttons = [
    (".", on_click_event, "add_point"),
    (".", on_click_event, "add_plane"),
    (".", on_click_event, "moving"),
    (".", on_click_event, "rotation"),
    (".", on_click_event, "add_line"),
]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Isometric 3d editor")

        self.layout = QVBoxLayout()

        self.editor = IsometricEditor("black")
        self.editor.setLayout(self.layout)

        toolbar = ToolBar(self, action_buttons, 30, self.editor.mouse_actions, "Main toolbar", self)
        self.addToolBar(toolbar)
        #toolbar = ToolBar(self, action_buttons, 15, self.editor.mouse_actions, "Palette", self)
        #self.addToolBar(toolbar)

        # Устанавливаем центральный виджет окна. Виджет будет расширяться по умолчанию,
        # заполняя всё пространство окна.
        self.setCentralWidget(self.editor)
        self.setGeometry(200, 200, 640, 480)
        self.setWindowTitle('Isometric 3D Editor')
        self.windows = list()

        self.menu = self.menuBar()
        self.geometry_menu = self.menu.addMenu("Geometry")

        self.form_geometry_menu(self.geometry_menu)

    def form_geometry_menu(self, menu):
        add_point = MenuAction("Add line", self,
                               status_tip="Add some points",
                               func=lambda s: self.open_window(s, AddLineWindow),
                               )

        add_line = MenuAction("Add point", self,
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

