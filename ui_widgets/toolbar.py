from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QToolBar, QPushButton

from ui_widgets.stylesheets.buttons import button_stylesheets, toolbar_default_button_stylesheet
from ui_widgets.stylesheets.toolbar import toolbar_stylesheet


class ToolBarButton(QPushButton):
    def __init__(self, handler, action, mouse_actions, size, *args, **kwargs):
        super(ToolBarButton, self).__init__(*args, **kwargs)

        self.state = getattr(mouse_actions, action)
        self.setIconSize(QSize(size, size))
        self.handler = handler
        self.action = action
        # button_action.clicked.connect(self.handler)
        self.setStyleSheet(button_stylesheets[self.state])

    def mousePressEvent(self, e):
        self.handler(self, e)

    def set_stylesheet(self, stylesheet):
        self.setStyleSheet(stylesheet)


def on_click_event(button: ToolBarButton, e):
    click_button = e.button()
    toolbar = button.parent()

    p = list(filter(lambda x: x.state == click_button, toolbar.buttons))

    if len(p) > 0:
        p = p[0]
        p.state = Qt.MouseButton.NoButton
        setattr(toolbar.mouse_actions, p.action, p.state)
        p.set_stylesheet(toolbar_default_button_stylesheet)

    button.state = click_button
    setattr(toolbar.mouse_actions, button.action, button.state)
    button.set_stylesheet(button_stylesheets[button.state])


class ToolBar(QToolBar):
    def __init__(self, mainWindow, buttons, size, state_class, *args):
        super(QToolBar, self).__init__(*args)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
        self.mainWindow = mainWindow
        self.setStyleSheet(toolbar_stylesheet)
        self.mouse_actions = state_class
        self.buttons = []
        for i in buttons:
            button = ToolBarButton(i[1], i[2], self.mouse_actions, size, QIcon(i[0]), "", self)
            self.buttons.append(button)
            self.addWidget(button)

