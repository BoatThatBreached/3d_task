import numpy as np
from PyQt6.QtCore import Qt, QPointF, QLineF
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtWidgets import QWidget
import geom as g


class MouseClickActions:
    def __init__(self, add_line=Qt.MouseButton.NoButton,
                 add_point=Qt.MouseButton.NoButton,
                 add_plane=Qt.MouseButton.NoButton,
                 rotation=Qt.MouseButton.NoButton,
                 moving=Qt.MouseButton.NoButton,):
        self.add_line = add_line
        self.add_point = add_point
        self.add_plane = add_plane
        self.rotation = rotation
        self.moving = moving


class IsometricEditor(QWidget):
    def __init__(self, theme):
        if theme not in ("white", "black"):
            raise Exception("Wrong theme: {0}".format(theme))
        self.theme = theme
        self.mouse_actions = MouseClickActions(add_line=Qt.MouseButton.RightButton,
 #                                              add_plane=Qt.MouseButton.LeftButton,
                                               rotation=Qt.MouseButton.LeftButton,
 #                                              moving=Qt.MouseButton.MiddleButton,
                                               )
        self.points = []
        self.line_containers = set()
        self.plane_containers = set()
        self.init_figures()
        self.corner = QPointF(0, 480)
        self.origin = np.array([320, 240, 0])
        self.around_x = 0
        self.around_y = 0
        self.current_point = self.origin
        self.screen = g.Plane(np.array([-320, -240, -1000]) + self.origin,
                              np.array([640, 0, 0]),
                              np.array([0, 480, 0]),
                              True)
        self.camera = np.array([0., 0., -80.])
        self.scale = 30
        self.intensity = 200
        self.lastPos = None
        self.lastButton = None
        self.line_point = None
        self.plane_points = []
        self.axis = [np.array([10, 0, 0]), np.array([0, 10, 0]), np.array([0, 0, 10])]

        super().__init__()

        self.init_ui()

    def geometry_safe_args(self):
        return self.screen, self.camera, self.origin, self.around_x, self.around_y

    def angles(self):
        return self.around_x, self.around_y

    def init_ui(self):
        self.setGeometry(200, 200, 640, 480)
        self.setWindowTitle('Isometric 3D Editor')
        self.show()

    def connect_two_points(self, p1, p2, draw_mode):
        self.line_containers.add(g.LineContainer(p1, p2, draw_mode))

    def add_point(self, x, y, z):
        self.points.append(np.array([x, y, z]))

    def form_plane(self, p1, p2, p3, draw_mode, density=10):
        plane_container = g.PlaneContainer(p1, p2, p3, draw_mode, density)
        self.plane_containers.add(plane_container)

    def form_plane_by_indices(self, p1, p2, p3, draw_mode):
        plane_container = g.PlaneContainer(self.points[p1], self.points[p2], self.points[p3], draw_mode)
        self.plane_containers.add(plane_container)

    def init_square(self, radius, center=np.array([0, 0, 0])):
        for i in range(8):
            b = bin(i)[2:].zfill(3)
            x, y, z = map(lambda n: radius if n == '1' else -radius, b)
            x += center[0]
            y += center[1]
            z += center[2]
            self.add_point(x, y, z)

    def init_figures(self):
        self.points = []
        self.init_square(2)

    def wheelEvent(self, e):
        self.scale += e.angleDelta().y() / 200
        self.update()

    def mousePressEvent(self, e):
        self.lastPos = e.position()
        self.lastButton = e.button()
        pos = np.array([e.position().x(), self.corner.y() - e.position().y(), 0])

        if self.lastButton == self.mouse_actions.add_line:
            for p in self.points:
                translated = g.get_coordinates(p, self.around_x, self.around_y)
                line = g.Line(self.camera + self.origin, translated + self.origin)
                i = self.screen.intersect_line(line)
                if i is None:
                    continue
                if type(i) == g.Line:
                    i = i.anchor
                i = (i - self.origin) * self.scale + self.origin
                i[2] = 0
                if g.length(pos - i) < 4:
                    if self.line_point is not None:
                        self.connect_two_points(self.line_point, p, "line")
                    self.line_point = p
                    break
            else:
                self.line_point = None
        if self.lastButton == self.mouse_actions.add_plane:
            for p in self.points:
                translated = g.get_coordinates(p, self.around_x, self.around_y)
                line = g.Line(self.camera + self.origin, translated + self.origin)
                i = self.screen.intersect_line(line)
                if i is None:
                    continue
                if type(i) == g.Line:
                    i = i.anchor
                i = (i - self.origin) * self.scale + self.origin
                i[2] = 0
                if g.length(pos - i) < 4:
                    if len(self.plane_points) == 0 \
                            or len(self.plane_points) == 1 and g.length(self.plane_points[0] - p) > 1e-7 \
                            or len(self.plane_points) == 2 and g.is_plane_valid(p, *self.plane_points):
                        self.plane_points.append(p)
                    break
            if len(self.plane_points) >= 3:
                self.form_plane(self.plane_points.pop(0), self.plane_points.pop(0), self.plane_points.pop(0),
                                "triangle", 10)

        self.update()

    def mouseReleaseEvent(self, e):
        self.lastButton = Qt.MouseButton.NoButton

    def mouseMoveEvent(self, e):
        delta = e.position() - self.lastPos
        if self.lastButton == self.mouse_actions.rotation:
            self.around_x += -delta.y() / self.intensity
            self.around_y += delta.x() / self.intensity

        if self.lastButton == self.mouse_actions.moving:
            self.origin[0] += delta.x()
            self.origin[1] -= delta.y()

        self.lastPos = e.position()
        self.update()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_background(qp)
        self.draw_axis(qp)
        self.draw_planes(qp)
        self.draw_lines(qp)
        self.draw_points(qp)
        qp.end()

    def draw_background(self, qp):
        if self.theme == "black":
            qp.fillRect(0, 0, self.size().width().real, self.size().height().real, Qt.GlobalColor.black)

    def draw_axis(self, qp):
        colors = [Qt.GlobalColor.red, Qt.GlobalColor.blue, Qt.GlobalColor.green]
        for i in range(len(self.axis)):
            qp.setPen(QPen(colors[i], 2))
            p = g.get_coordinates(self.axis[i], self.around_x, self.around_y)
            line1 = g.Line(p + self.origin, self.origin)
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
            qp.drawEllipse(point1, 3, 3)

    def draw_planes(self, qp):
        for container in self.plane_containers:
            for line_container in container.line_containers:
                i1, i2 = line_container.project_on_plane(*self.geometry_safe_args())
                if i1 is None or i2 is None:
                    continue

                if line_container.draw_mode == "line":
                    if g.length(i1[:2] - i2[:2]) < 1e-1:
                        continue
                    direction = g.get_vector_with_length(i1 - i2, 1)
                    i1 -= direction * 1000
                    i2 += direction * 1000
                i1 = (i1 - self.origin) * self.scale + self.origin
                i2 = (i2 - self.origin) * self.scale + self.origin
                point1 = QPointF(i1[0], self.corner.y() - i1[1])
                point2 = QPointF(i2[0], self.corner.y() - i2[1])
                qp.setPen(QPen(line_container.color, 2))
                qp.drawLine(QLineF(point1, point2))

    def draw_points(self, qp):
        for p in self.points:
            translated = g.get_coordinates(p, self.around_x, self.around_y)
            qp.setPen(QPen(Qt.GlobalColor.blue, 2))
            line = g.Line(self.camera + self.origin, translated + self.origin)
            i = self.screen.intersect_line(line)
            if i is None:
                continue
            if type(i) == g.Line:
                i = i.anchor
            i = (i - self.origin) * self.scale + self.origin
            point = QPointF(i[0], self.corner.y() - i[1])
            if id(self.line_point) == id(p):
                qp.setPen(QPen(Qt.GlobalColor.red, 2))
            if id(p) in map(id, self.plane_points):
                qp.setPen(QPen(Qt.GlobalColor.magenta, 2))
            qp.drawEllipse(point, 3, 3)

    def draw_lines(self, qp):

        for container in self.line_containers:
            i1, i2 = container.project_on_plane(*self.geometry_safe_args())
            if i1 is None or i2 is None:
                continue
            qp.setPen(QPen(container.color, 2 if container.draw_mode == "segment" else 1))
            if container.draw_mode == "line":
                if g.length(i1[:2] - i2[:2]) < 1e-1:
                    continue
                direction = g.get_vector_with_length(i1 - i2, 1)
                i1 -= direction * 1000
                i2 += direction * 1000
            i1 = (i1 - self.origin) * self.scale + self.origin
            i2 = (i2 - self.origin) * self.scale + self.origin
            point1 = QPointF(i1[0], self.corner.y() - i1[1])
            point2 = QPointF(i2[0], self.corner.y() - i2[1])
            qp.drawLine(QLineF(point1, point2))
