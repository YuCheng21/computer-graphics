from point3d import Point3d


class Camara:
    def __init__(self, distance, zoom, projection) -> None:
        super().__init__()
        self.distance = distance
        self.zoom = zoom
        self.projection = projection

    def convert(self, point: Point3d):
        if self.projection == 'parallel':
            td = self.distance
        elif self.projection == 'prospective':
            td = self.distance - point.z
        else:
            td = self.distance
        result = Point3d()
        result.x = point.x / td * self.zoom
        result.y = point.y / td * self.zoom
        result.z = point.z

        return result
