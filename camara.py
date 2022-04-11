from point3d import Point3d


class Camara:
    def __init__(self, distance, zoom) -> None:
        super().__init__()
        self.distance = distance
        self.zoom = zoom

    def projection(self, point: Point3d, projection):
        if projection == 'parallel':
            td = self.distance
        else:
            td = self.distance - point.z
        result = Point3d()
        result.x = point.x / td * self.zoom
        result.y = point.y / td * self.zoom
        result.z = point.z

        return result
