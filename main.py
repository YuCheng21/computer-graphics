import cv2
import numpy as np
from camara import Camara
from graphics import Graphics

import model.teapot as teapot
import model.square as square
import model.triangle as triangle


def print_info():
    cv2.putText(img, f"x_degree: {graphics.init_x_degree};", (200, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
    cv2.putText(img, f"y_degree: {graphics.init_y_degree};", (200, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
    cv2.putText(img, f"z_degree: {graphics.init_z_degree};", (200, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
    cv2.putText(img, f"x: {graphics.init_x};", (325, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    cv2.putText(img, f"y: {graphics.init_y};", (325, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    cv2.putText(img, f"z: {graphics.init_z};", (325, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    cv2.putText(img, f"camara_distance: {camara.distance};", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)
    cv2.putText(img, f"camara_zoom: {camara.zoom};", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)


if __name__ == '__main__':
    obj = teapot
    obj_vertex = np.array(obj.vertex, dtype=float)
    obj_face = np.array(obj.face, dtype=int)

    graphics = Graphics(obj_face, obj_vertex)
    # graphics.split()
    graphics.modeling()
    # graphics.to_triangle()
    # Initial
    graphics.rotate(0, axis=0)
    graphics.rotate(0, axis=1)
    graphics.rotate(0, axis=2)
    graphics.translate(0, 0, 0)
    camara = Camara(30, 2000, parallel=False)

    img_size = (500, 500)
    while True:
        img = np.zeros((img_size[0], img_size[1], 3), np.uint8)
        graphics.draw_frame(img, camara)

        print_info()

        cv2.imshow('img', img)
        key = cv2.waitKey()
        graphics.listener(key)
        camara.listener(key)
        if key & 0xFF == ord('p'):
            break

    cv2.destroyAllWindows()
