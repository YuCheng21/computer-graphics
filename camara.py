import numpy as np


class Camara:
    def __init__(self, distance, zoom, parallel=False) -> None:
        """
        camera position: x=0, y=0, z=distance
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
        result[2] = point[2]
        return result

    def listener(self, key):
        # Distance
        if key & 0xFF == ord('t'):
            self.distance += 1
        if key & 0xFF == ord('g'):
            self.distance -= 1
        # Zoom
        if key & 0xFF == ord('y'):
            self.zoom += 10

        if key & 0xFF == ord('h'):
            self.zoom -= 10
