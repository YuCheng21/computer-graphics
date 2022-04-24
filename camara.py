import numpy as np


class Camara:
    def __init__(self, viewpoint: tuple, zoom, parallel=False) -> None:
        """
        Viewpoint fixed at (x=0, y=0, z=distance)
        View plane fixed at (x=0, y=0, z=distance-1)
        Target fixed at (x=0, y=0, z=0)
        """
        super().__init__()
        self.x = viewpoint[0]
        self.y = viewpoint[1]
        self.z = viewpoint[2]
        self.zoom = zoom
        self.parallel = parallel

    def convert(self, point):
        if self.parallel is True:
            tz = self.z
            ty = self.y
            tx = self.x
        else:
            tz = self.z - point[2]
            ty = self.y - point[1]
            tx = self.x - point[0]
        result = np.empty(3)
        result[0] = point[0] - tx / tz * self.zoom
        result[1] = point[1] - ty / tz * self.zoom
        result[2] = point[2]  # do nothing
        return result

    def listener(self, key):
        # Distance
        if key & 0xFF == ord('h'):
            self.x += 1
        if key & 0xFF == ord('f'):
            self.x -= 1
        if key & 0xFF == ord('g'):
            self.y += 1
        if key & 0xFF == ord('t'):
            self.y -= 1
        if key & 0xFF == ord('y'):
            self.z += 1
        if key & 0xFF == ord('r'):
            self.z -= 1
        # Zoom
        if key & 0xFF == ord('x'):
            self.zoom += 10

        if key & 0xFF == ord('z'):
            self.zoom -= 10
