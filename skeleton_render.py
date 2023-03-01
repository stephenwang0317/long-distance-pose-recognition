import cv2
import numpy as np



class SkeletonRender:
    def __init__(self):
        self.connections = [
            (28, 30), (30, 32), (28, 32),  # 右脚
            (38, 37), (38, 22), (38, 20), (38, 18), (38, 16),  # 右手
            (27, 29), (27, 31), (29, 31),  # 左脚
            (36, 35), (36, 21), (36, 19), (36, 17), (36, 15),  # 左手
            (24, 26), (26, 28),  # 右腿
            (23, 25), (25, 27),  # 左腿
            (24, 33), (33, 23),  # 胯
            (12, 14), (14, 38),  # 右臂
            (11, 13), (13, 36),  # 左臂
            (12, 24),  # 右肋
            (11, 23),  # 左肋
            (11, 12),  # 肩膀
        ]
        self.point_color = (0, 255, 0)
        self.connection_color = (255, 0, 0)
        self.thickness = 2
        self.hull_thickness = 2

    def _draw_points_and_connections(self, points, image, zero_point):
        if points is not None:
            for index, point in enumerate(points):
                x, y = point
                x += zero_point[0]
                y += zero_point[1]
                cv2.circle(image, (int(x), int(y)), self.thickness * 2, self.point_color, self.hull_thickness)
                text = str(index)
                cv2.putText(image, text, (int(x), int(y)), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1)
            for connection in self.connections:
                x0, y0 = points[connection[0]]
                x0 += zero_point[0]
                y0 += zero_point[1]
                x1, y1 = points[connection[1]]
                x1 += zero_point[0]
                y1 += zero_point[1]
                cv2.line(image, (int(x0), int(y0)), (int(x1), int(y1)), self.connection_color, self.thickness)
        return image

    def render(self, image, points, zero_point):
        rendered_img = self._draw_points_and_connections(points, image, zero_point)
        return rendered_img
