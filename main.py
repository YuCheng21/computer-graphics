import cv2
import numpy as np
from camara import Camara
from point3d import Point3d
from triangle import Triangle

import teapot
import square


obj = square
obj_vertex = []
for i in obj.vertex:
    obj_vertex.append(Point3d(x=i[0], y=i[1], z=i[2]))
obj_face = obj.face

camara = Camara(20, 3000)

triangle = Triangle()
triangle.rect2tri(obj_face, obj_vertex)
triangle.rotate_x(5)
triangle.rotate_y(5)
# triangle.rotate_z(30)
# triangle.translate(0, 0.3, 0)


img_size = (500, 500)
img = np.zeros((img_size[0], img_size[1], 3), np.uint8)

triangle.draw_frame(img, camara)


cv2.imshow('img', img)
cv2.waitKey(0)


