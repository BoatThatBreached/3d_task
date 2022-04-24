from PyQt6.QtCore import QPointF
from PyQt6.QtCore import Qt
import numpy as np


def dist(p1, p2):
    return ((p1.x() - p2.x()) ** 2 + (p1.y() - p2.y()) ** 2) ** 0.5


def is_point_valid(point, size):
    return 0 <= point.x() <= size.width() and 0 <= point.y() <= size.height()


def is_plane_valid(*points):
    points = list(points)
    for i in range(3):
        pts = points[:]
        pts.pop(i)
        if length(pts[0] - pts[1]) < 1e-7:
            return False
    return True


def get_vector_on_vector_projection(a, b):
    return np.dot(a, b) / np.dot(b, b)


def get_vector_with_length(x, h):
    if length(x) < 1e-7:
        return x
    return x / length(x) * h


def translate_point(p, editor):
    px = get_vector_on_vector_projection(p, get_vector_with_length(editor.right, 1 / editor.width))
    py = get_vector_on_vector_projection(p, get_vector_with_length(editor.up, 1 / editor.width))
    return QPointF(px, py)


def turn_around(axis, angle, vector):
    if axis not in list('xyz'):
        raise Exception("Wrong axis: {0}".format(axis))
    curr_length = length(vector)
    if curr_length < 1e-7:
        return vector
    indices = list(range(3))
    indices.pop('xyz'.index(axis))
    cos_a = vector[indices[0]] / curr_length
    cos_b = np.cos(angle)
    sin_a = vector[indices[1]] / curr_length
    sin_b = np.sin(angle)
    cos_ab = cos_a * cos_b - sin_a * sin_b
    sin_ab = sin_a * cos_b + sin_b * cos_a
    result = [curr_length * cos_ab, curr_length * sin_ab]
    result.insert('xyz'.index(axis), vector['xyz'.index(axis)])
    return np.array(result)


def turn_queue(axis, angles, vector):
    if len(axis) != len(angles):
        raise Exception("Wrong number of axis ({0}) and angles ({1})".format(len(axis), len(angles)))
    result = np.copy(vector)
    for i in range(len(axis)):
        result = turn_around(axis[i], angles[i], result)
    return result


def clamp(val, mi, ma):
    return ma if val > ma else mi if val < mi else val


def get_coordinates(point, around_x, around_y):
    return turn_queue('xy', (around_x, around_y), point)


def length(vector):
    return np.linalg.norm(vector)


class Plane:
    def __init__(self, p1, p2, p3, relatively=False):
        self.anchor = p1
        # TODO: collinear check
        self.basis = (p2, p3) if relatively else (p2 - p1, p3 - p1)
        self.size = (length(self.basis[0]), length(self.basis[1]))

    def project_point(self, p):
        res = get_vector_on_vector_projection(p - self.anchor, self.basis[0]) * self.basis[0]
        res += get_vector_on_vector_projection(p - self.anchor, self.basis[1]) * self.basis[1]
        res += self.anchor
        return res

    def get_coordinates_on_plane(self, p):
        return get_vector_on_vector_projection(p - self.anchor, self.basis[0]), \
               get_vector_on_vector_projection(p - self.anchor, self.basis[1])

    def contains(self, p):
        coordinates = self.get_coordinates_on_plane(p)
        return 0 <= coordinates[0] <= 1 and 0 <= coordinates[1] <= 1

    def intersect_line(self, line):
        p1 = line.anchor
        p2 = line.anchor + line.direction

        pr1 = self.project_point(p1)
        pr2 = self.project_point(p2)

        h1 = p1 - pr1
        h2 = p2 - pr2
        # TODO:вынеcти в другой метод, решить проблему с добавлением точки на xy
        if length(h1) < 1e-7 or length(h2) < 1e-7:
            return line
        r = length(h1) / length(h2)
        if r + 1 < 1e-7:
            return None

        b = 1 / (1 + r)
        i = p2 - line.direction * b
        if not self.contains(i):
            return None

        return i


class LineContainer:
    def __init__(self, p1, p2, draw_mode, color=Qt.GlobalColor.cyan):
        if draw_mode not in ("segment", "line"):
            raise Exception("Wrong draw mode: {0}".format(draw_mode))
        self.p1 = p1
        self.p2 = p2
        self.draw_mode = draw_mode
        self.color = color

    def get_line(self):
        return Line(self.p1, self.p2)

    def project_on_plane(self, plane, camera, origin, around_x, around_y):
        line1 = Line(camera, get_coordinates(self.p1, around_x, around_y)) + origin
        line2 = Line(camera, get_coordinates(self.p2, around_x, around_y)) + origin
        i1 = plane.intersect_line(line1)
        if type(i1) is Line:
            i1 = i1.anchor
        i2 = plane.intersect_line(line2)
        if type(i2) is Line:
            i2 = i2.anchor
        return i1, i2


class PlaneContainer:
    def __init__(self, anchor, p1, p2, draw_mode, density=10):
        self.anchor = anchor
        self.p1 = p1
        self.p2 = p2
        if draw_mode not in ("triangle", "para", "plane"):
            raise Exception("Wrong draw mode: {0}".format(draw_mode))
        self.draw_mode = draw_mode
        self.points = set()
        self.line_containers = set()
        self.density = density
        self.reset_grid()

    def reset_grid(self):
        self.line_containers.clear()
        basis_x = self.p1 - self.anchor
        basis_y = self.p2 - self.anchor
        if self.draw_mode == "triangle":
            for i in range(1, self.density):
                p1 = self.anchor + basis_y * i / (self.density - 1)
                p2 = self.anchor + basis_y * i / (self.density - 1) + basis_x * (self.density - 1 - i) / (
                        self.density - 1)
                self.line_containers.add(LineContainer(p1, p2, "segment", Qt.GlobalColor.yellow))
            for i in range(1, self.density):
                p1 = self.anchor + basis_x * i / (self.density - 1)
                p2 = self.anchor + basis_x * i / (self.density - 1) + basis_y * (self.density - 1 - i) / (
                        self.density - 1)
                self.line_containers.add(LineContainer(p1, p2, "segment", Qt.GlobalColor.yellow))
            self.line_containers.add(
                LineContainer(self.anchor, self.anchor + basis_x, "segment", Qt.GlobalColor.magenta))
            self.line_containers.add(
                LineContainer(self.anchor, self.anchor + basis_y, "segment", Qt.GlobalColor.magenta))
            self.line_containers.add(
                LineContainer(self.anchor + basis_x, self.anchor + basis_y, "segment", Qt.GlobalColor.magenta))
        if self.draw_mode == "para":
            for i in range(self.density):
                p1 = self.anchor + basis_y * i / (self.density - 1)
                p2 = self.anchor + basis_y * i / (self.density - 1) + basis_x
                self.line_containers.add(LineContainer(p1, p2, "segment"))

    def normal(self):
        return np.cross(self.p1 - self.anchor, self.p2 - self.anchor)


class Line:
    def __init__(self, p1, p2):
        self.anchor = p1
        self.direction = p2 - p1

    def __add__(self, other):
        return Line(self.anchor + other, self.direction + other)
