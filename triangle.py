import cv2
from point3d import Point3d
from math import sin, cos


class Triangle:
    def __init__(self, tri = None, vertex = None) -> None:
        super().__init__()
        self.tri = tri
        self.vertex = vertex

    def rect2tri(self, rect_face, vertex: Point3d):
        """
        1. split rectangle
        2. rectangle -> triangle
        """
        self.vertex = vertex

        rect = []
        for item in rect_face:
            while len(item) > 0:
                rect.append(item[0:4])
                item = item[4:]

        tri = []
        for i in rect:
            tri.append([i[0], i[1], i[2]])
            tri.append([i[0], i[2], i[3]])
        self.tri = tri

    def translate(self, x: float = 0, y: float = 0 , z: float = 0):
        """
        Coordinate translation
        """
        for item in self.vertex:
            item.x += x
            item.y += y
            item.z += z

    def rotate_x(self, degree: int):
        """
        rotate axis x
        """
        for item in self.vertex:
            rad = degree * 3.1416 / 180.0
            y = item.y
            z = item.z
            item.y = cos(rad) * y - sin(rad) * z
            item.z = sin(rad) * y + cos(rad) * z

    def rotate_y(self, degree: int):
        """
        rotate axis y
        """
        for item in self.vertex:
            rad = degree * 3.1416 / 180.0
            x = item.x
            z = item.z
            item.x = cos(rad) * x - sin(rad) * z
            item.z = sin(rad) * x + cos(rad) * z

    def rotate_z(self, degree: int):
        """
        rotate axis z
        """
        for item in self.vertex:
            rad = degree * 3.1416 / 180.0
            x = item.x
            y = item.y
            item.x = cos(rad)*x - sin(rad)*y
            item.y = sin(rad)*x + cos(rad)*y

    def re_position(self, point: Point3d, img_shape):
        """
        make origin point to the middle
        """
        result = Point3d()
        result.x = img_shape[0]/2 + point.x
        result.y = img_shape[1]/2 + point.y
        result.z = point.z
        return result

    def draw_frame(self, img, camara):
        for row in self.tri:
            buffer = []
            # 3d to 2d (projection)
            for col in row:
                index = col - 1
                buffer.append(camara.convert(self.vertex[index]))
                buffer[len(buffer) - 1] = self.re_position(buffer[len(buffer)-1], img.shape)
            # draw frame (triangle)
            for key, value in enumerate(buffer):
                next_key = key + 1
                next_key = 0 if next_key >= len(buffer) else next_key
                start_point = (int(buffer[key].x), int(buffer[key].y))
                end_point = (int(buffer[next_key].x), int(buffer[next_key].y))
                cv2.line(img, start_point, end_point, (255, 0, 0), 2)

