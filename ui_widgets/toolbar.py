from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QToolBar, QPushButton

from ui_widgets.stylesheets import toolbar_stylesheet, toolbar_left_clicked_button_stylesheet, \
    toolbar_default_button_stylesheet, toolbar_right_clicked_button_stylesheet

button_stylesheets = {
    Qt.MouseButton.LeftButton: toolbar_left_clicked_button_stylesheet,
    Qt.MouseButton.RightButton: toolbar_right_clicked_button_stylesheet,
    Qt.MouseButton.NoButton: toolbar_default_button_stylesheet,
    Qt.MouseButton.MiddleButton: toolbar_default_button_stylesheet,
}


class ToolBarButton(QPushButton):
    def __init__(self, handler, action, mouse_actions, *args, **kwargs):
        super(ToolBarButton, self).__init__(*args, **kwargs)

        self.state = getattr(mouse_actions, action)
        self.setIconSize(QSize(30, 30))
        self.handler = handler
        self.action = action
        # button_action.clicked.connect(self.handler)
        self.setStyleSheet(button_stylesheets[self.state])

    def mousePressEvent(self, e):
        self.handler(self, e)

    def set_stylesheet(self, stylesheet):
        self.setStyleSheet(stylesheet)


def on_click_event(button: ToolBarButton, e):
    button.parent().update_buttons(button, e.button())


buttons = [
    ("ui_widgets/icons/Point.svg", on_click_event, "add_point"),
    ("ui_widgets/icons/Plane.svg", on_click_event, "add_plane"),
    ("ui_widgets/icons/Moving.svg", on_click_event, "moving"),
    ("ui_widgets/icons/Rotation.svg", on_click_event, "rotation"),
    ("ui_widgets/icons/Segment.svg", on_click_event, "add_line"),
]


class ToolBar(QToolBar):
    def __init__(self, mainWindow, *args):
        super(QToolBar, self).__init__(*args)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
        self.mainWindow = mainWindow
        self.setStyleSheet(toolbar_stylesheet)
        self.mouse_actions = mainWindow.editor.mouse_actions
        self.buttons = []
        for i in buttons:
            button = ToolBarButton(i[1], i[2], self.mouse_actions, QIcon(i[0]), "", self)
            self.buttons.append(button)
            self.addWidget(button)

        self.setIconSize(QSize(30, 30))

    def mousePressEvent(self, e):
        pass

    def update_buttons(self, button, click_button):
        p = list(filter(lambda x: x.state == click_button, self.buttons))

        if len(p) > 0:
            p = p[0]
            p.state = Qt.MouseButton.NoButton
            setattr(self.mouse_actions, p.action, p.state)
            p.set_stylesheet(toolbar_default_button_stylesheet)

        button.state = click_button
        setattr(self.mouse_actions, button.action, button.state)
        button.set_stylesheet(button_stylesheets[button.state])
