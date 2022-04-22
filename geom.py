from PyQt6.QtCore import QPointF
import numpy as np


def dist(p1, p2):
    return ((p1.x() - p2.x()) ** 2 + (p1.y() - p2.y()) ** 2) ** 0.5


def is_point_valid(point, size):
    return 0 <= point.x() <= size.width() and 0 <= point.y() <= size.height()


def get_vector_on_vector_projection(a, b):
    return np.dot(a, b) / np.dot(b, b)


def get_vector_with_length(x, h):
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
    result = [curr_length*cos_ab, curr_length*sin_ab]
    result.insert('xyz'.index(axis), vector['xyz'.index(axis)])
    return np.array(result)


def clamp(val, mi, ma):
    return ma if val > ma else mi if val < mi else val


def get_coordinates(point, around_x, around_y):
    return turn_around('x', around_x, turn_around('y', around_y, point))


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
    def __init__(self, ind1, ind2, draw_mode):
        if draw_mode not in ("segment", "line"):
            raise Exception("wrong mode!")
        self.p1 = ind1
        self.p2 = ind2
        self.draw_mode = draw_mode

    def get_line(self, points):
        return Line(points[self.p1], points[self.p2])

    def project_on_plane(self, points, plane, camera, origin, around_x, around_y):
        line1 = Line(camera, get_coordinates(points[self.p1], around_x, around_y)) + origin
        line2 = Line(camera, get_coordinates(points[self.p2], around_x, around_y)) + origin
        i1 = plane.intersect_line(line1)
        if type(i1) is Line:
            i1 = i1.anchor
        i2 = plane.intersect_line(line2)
        if type(i2) is Line:
            i2 = i2.anchor
        return i1, i2


class Line:
    def __init__(self, p1, p2):
        self.anchor = p1
        self.direction = p2 - p1

    def __add__(self, other):
        return Line(self.anchor+other, self.direction+other)
