import cv2
from math import radians, sin, cos, ceil

import numpy as np


def re_position(point, img_shape):
    """
    make origin point to the middle
    """
    result = np.empty(3)
    result[0] = img_shape[0] / 2 + point[0]
    result[1] = img_shape[1] / 2 + point[1]
    result[2] = point[2]  # do nothing
    return result


class Graphics:
    def __init__(self, face: np.ndarray = None, vertex: np.ndarray = None) -> None:
        super().__init__()
        self.face = face
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
            size = ceil(row.shape[0] ** 0.5)
            reshape2size = np.pad(row.astype(float), (0, size * size - row.size),
                   mode='constant', constant_values=np.nan).reshape(size, size)
            for i in range(reshape2size.shape[0] - 1):
                for j in range(reshape2size.shape[1] - 1):
                    buffer.append(reshape2size[i:i + 1 + 1, j:j + 1 + 1].reshape(-1))
        self.face = buffer
        # to triangle
        buffer = []
        for row in self.face:
            for i in range(len(row)-3+1):
                buffer.append([row[0], row[1+i], row[2+i]])
        self.face = buffer

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
                index = col - 1
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
