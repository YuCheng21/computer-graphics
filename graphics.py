import cv2
from math import radians, sin, cos, ceil

import numpy as np


def re_position(point, img_shape):
    """
    make origin point to the middle
    """
    result = np.empty(3)
    result[0] = img_shape[0] * 0.5 + point[0]
    result[1] = img_shape[1] * 0.5 + point[1]
    result[2] = point[2]  # do nothing
    return result


class Graphics:
    def __init__(self, face: np.ndarray = None, vertex: np.ndarray = None) -> None:
        super().__init__()
        self.face = face - 1  # file-format start at 1.
        self.vertex = vertex
        self.init_x = 0
        self.init_y = 0
        self.init_z = 0
        self.init_x_degree = 0
        self.init_y_degree = 0
        self.init_z_degree = 0

    def modeling(self):
        # splitting
        buffer = []
        for row in self.face:
            size = ceil(row.reshape(-1).shape[0] ** 0.5)
            reshape2size = np.pad(row.astype(float), (0, size * size - row.size),
                   mode='constant', constant_values=np.nan).reshape(size, size)
            for i in range(reshape2size.shape[0] - 1):
                for j in range(reshape2size.shape[1] - 1):
                    buffer.append(reshape2size[i:i + 1 + 1, j:j + 1 + 1].reshape(-1))
        self.face = buffer

    def split(self):
        length = int(self.face.shape[1]**0.5)
        buffer_face = self.face.reshape(-1, length, length)  # 4x4
        buffer_vertex = self.vertex
        # start loop
        for i in range(2):  # 1: row, 2: col
            new_first_vertex = np.empty((0, 3))
            new_first_face = np.empty((0, (length + 3), buffer_face.shape[1]), dtype=int)
            for index in range(buffer_face.shape[0]):  # 32
                row_face = np.empty((0, (length + 3)), dtype=int)
                for row in range(buffer_face.shape[1]):
                    # calculate new point
                    ret = self.bezier(*buffer_vertex[buffer_face[index][row]])
                    # process face (delete and insert)
                    row_face = np.append(row_face, [np.arange(len(new_first_vertex), len(new_first_vertex) + (length + 3), dtype=int)], 0)
                    # process vertex (delete and insert)
                    new_first_vertex = np.append(new_first_vertex, ret, 0)
                row_face = row_face.transpose()
                new_first_face = np.append(new_first_face, [row_face], 0)
            buffer_face = new_first_face
            buffer_vertex = new_first_vertex
        self.face = buffer_face
        self.vertex = buffer_vertex

    def to_triangle(self):
        buffer = []
        for row in self.face:
            for i in range(len(row)-3+1):
                buffer.append([row[0], row[1+i], row[2+i]])
        self.face = buffer

    def bezier(self, p1: np.ndarray, p2: np.ndarray, p3: np.ndarray, p4: np.ndarray):
        p12 = (p1 + p2) * 0.5
        p23 = (p2 + p3) * 0.5
        p34 = (p3 + p4) * 0.5
        p1223 = (p12 + p23) * 0.5
        p2334 = (p23 + p34) * 0.5
        p12232334 = (p1223 + p2334) * 0.5
        return [p1, p12, p1223, p12232334, p2334, p34, p4]

    def translate(self, x: float = 0, y: float = 0, z: float = 0):
        """
        Coordinate translation
        """
        self.init_x += x
        self.init_y += y
        self.init_z += z
        for item in self.vertex:
            item[0] += x
            item[1] += y
            item[2] += z

    def rotate(self, degree: int, axis: int):
        """
        rotate axis x:0, y:1, z:2
        """
        self.init_x_degree = (self.init_x_degree + degree) % 360 if axis == 0 else self.init_x_degree
        self.init_y_degree = (self.init_y_degree + degree) % 360 if axis == 1 else self.init_y_degree
        self.init_z_degree = (self.init_z_degree + degree) % 360 if axis == 2 else self.init_z_degree
        for item in self.vertex:
            rad = radians(degree)
            x = item[0]
            y = item[1]
            z = item[2]
            if axis == 0:
                item[1] = cos(rad) * y - sin(rad) * z
                item[2] = sin(rad) * y + cos(rad) * z
            elif axis == 1:
                item[0] = cos(rad) * x - sin(rad) * z
                item[2] = sin(rad) * x + cos(rad) * z
            elif axis == 2:
                item[0] = cos(rad) * x - sin(rad) * y
                item[1] = sin(rad) * x + cos(rad) * y
            else:
                raise

    def draw_frame(self, img, camara):
        for row in self.face:
            buffer = []
            for col in row:
                if np.isnan(col):
                    continue
                index = col
                result = camara.convert(self.vertex[int(index)])
                buffer.append(re_position(result, img.shape))
            for key, value in enumerate(buffer):
                next_key = key + 1
                next_key = 0 if next_key >= len(buffer) else next_key
                start_point = (int(buffer[key][0]), int(buffer[key][1]))
                end_point = (int(buffer[next_key][0]), int(buffer[next_key][1]))
                cv2.line(img, start_point, end_point, (150, 240, 150), 1)

    def listener(self, key):
        # Rotate
        if key & 0xFF == ord('i'):
            self.rotate(5, axis=0)
        if key & 0xFF == ord('j'):
            self.rotate(5, axis=1)
        if key & 0xFF == ord('o'):
            self.rotate(5, axis=2)

        if key & 0xFF == ord('k'):
            self.rotate(-5, axis=0)
        if key & 0xFF == ord('l'):
            self.rotate(-5, axis=1)
        if key & 0xFF == ord('u'):
            self.rotate(-5, axis=2)
        # Translate
        if key & 0xFF == ord('d'):
            self.translate(1, 0, 0)
        if key & 0xFF == ord('s'):
            self.translate(0, 1, 0)
        if key & 0xFF == ord('e'):
            self.translate(0, 0, 1)

        if key & 0xFF == ord('a'):
            self.translate(-1, 0, 0)
        if key & 0xFF == ord('w'):
            self.translate(0, -1, 0)
        if key & 0xFF == ord('q'):
            self.translate(0, 0, -1)
