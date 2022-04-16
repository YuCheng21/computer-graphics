import numpy as np


class Camara:
    def __init__(self, distance, zoom, parallel=False) -> None:
        """
        Viewpoint fixed at (x=0, y=0, z=distance)
        View plane fixed at (x=0, y=0, z=distance-1)
        Target fixed at (x=0, y=0, z=0)
        """
        super().__init__()
        self.distance = distance
        self.zoom = zoom
        self.parallel = parallel

    def convert(self, point):
        if self.parallel is True:
            td = self.distance
        else:
            td = self.distance - point[2]
        result = np.empty(3)
        result[0] = point[0] / td * self.zoom
        result[1] = point[1] / td * self.zoom
        result[2] = point[2]  # do nothing
        return result

    def listener(self, key):
        # Distance
        if key & 0xFF == ord('h'):
            self.distance += 1
        if key & 0xFF == ord('y'):
            self.distance -= 1
        # Zoom
        if key & 0xFF == ord('g'):
            self.zoom += 10

        if key & 0xFF == ord('t'):
            self.zoom -= 10
