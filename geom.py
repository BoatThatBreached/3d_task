from PyQt6.QtCore import QPointF
import numpy as np


def dist(p1, p2):
    return ((p1.x() - p2.x()) ** 2 + (p1.y() - p2.y()) ** 2) ** 0.5


def validPoint(point, size):
    return 0 <= point.x() <= size.width() and 0 <= point.y() <= size.height()


def getProjection(a, b):
    return np.dot(a, b) / np.dot(b, b)


def withLength(x, h):
    return x / np.linalg.norm(x) * h


def translatePoint(p, editor):
    px = getProjection(p, withLength(editor.right, 1 / editor.width))
    py = getProjection(p, withLength(editor.up, 1 / editor.width))
    return QPointF(px, py)


def turnAroundX(beta, vector):
    length = np.linalg.norm(vector)
    cos_a = vector[1] / length
    cos_b = np.cos(beta)
    sin_a = vector[2] / length
    sin_b = np.sin(beta)
    cos_ab = cos_a * cos_b - sin_a * sin_b
    sin_ab = sin_a * cos_b + sin_b * cos_a
    return np.array([vector[0], length * cos_ab, length * sin_ab])


def turnAroundY(alpha, vector):
    length = np.linalg.norm(vector)
    cos_a = vector[0] / length
    cos_b = np.cos(alpha)
    sin_a = vector[2] / length
    sin_b = np.sin(alpha)
    cos_ab = cos_a * cos_b - sin_a * sin_b
    sin_ab = sin_a * cos_b + sin_b * cos_a
    return np.array([length * cos_ab, vector[1], length * sin_ab])


def clamp(val, m, M):
    return M if val > M else m if val < m else val


class Plane:
    def __init__(self, p1, p2, p3, relatively=False):
        self.anchor = p1
        # TODO: collinear check
        self.basis = (p2, p3) if relatively else (p2 - p1, p3 - p1)
        self.size = (np.linalg.norm(self.basis[0]), np.linalg.norm(self.basis[1]))

    def project_point(self, p):
        res = getProjection(p - self.anchor, self.basis[0]) * self.basis[0]
        res += getProjection(p - self.anchor, self.basis[1]) * self.basis[1]
        res += self.anchor
        return res

    def get_coords(self, p):
        return getProjection(p - self.anchor, self.basis[0]), getProjection(p - self.anchor, self.basis[1])

    def contains(self, p):
        coords = self.get_coords(p)
        return 0 <= coords[0] <= 1 and 0 <= coords[1] <= 1

    def intersect_line(self, line):
        p1 = line.anchor
        p2 = line.anchor + line.direction

        pr1 = self.project_point(p1)
        pr2 = self.project_point(p2)

        h1 = p1 - pr1
        h2 = p2 - pr2
        #TODO:вынеcти в другой метод, решить проблему с добавлением точки на xy
        if np.linalg.norm(h1)<1e-7 or np.linalg.norm(h2)<1e-7:
            return line
        r = np.linalg.norm(h1) / np.linalg.norm(h2)
        if r + 1 < 1e-7:
            return None

        b = 1 / (1 + r)
        i = p2 - line.direction * b
        if not self.contains(i):
            return None

        return i


class LineContainer:
    def __init__(self, ind1, ind2, drawMode):
        if drawMode not in ["sector", "line"]:
            raise Exception("wrong mode!")
        self.points = (ind1, ind2)
        self.drawMode = drawMode


class Line:
    def __init__(self, p1, p2):
        self.anchor = p1
        self.direction = p2 - p1
