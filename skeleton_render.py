import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt



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
    
    def render_3d(self, points):
        ap0 = [[ 1.19136230e+02,  9.61853027e+01, -2.05195312e+02],
                [ 1.24241211e+02,  9.00842285e+01, -1.91125488e+02],
                [ 1.27229492e+02,  9.00842285e+01 ,-1.91125488e+02],
                [ 1.30466797e+02,  9.01464844e+01, -1.91125488e+02],
                [ 1.15649902e+02,  9.03332520e+01 ,-1.86269531e+02],
                [ 1.12910645e+02,  9.03955078e+01, -1.86269531e+02],
                [ 1.10171387e+02,  9.05200195e+01 ,-1.86269531e+02],
                [ 1.35945312e+02,  9.59362793e+01 ,-1.14114990e+02],
                [ 1.08179199e+02,  9.61230469e+01, -9.26989746e+01],
                [ 1.25735352e+02,  1.05150146e+02, -1.78051758e+02],
                [ 1.14653809e+02,  1.05274658e+02 ,-1.72199707e+02],
                [ 1.61345703e+02,  1.50783691e+02, -7.28393555e+01],
                [ 9.03740234e+01,  1.37709961e+02, -3.73846436e+01],
                [ 1.77034180e+02, 2.08557129e+02, -3.26531982e+01],
                [ 6.24833984e+01 , 9.10803223e+01 ,-6.61468506e-02],
                [ 1.78279297e+02,  2.62719727e+02 ,-4.09643555e+01],
                [ 7.53081055e+01 , 4.67541504e+01 , 5.38513184e+01],
                [ 1.80769531e+02 , 2.79155273e+02 ,-5.14544678e+01],
                [ 7.75493164e+01 , 3.43652344e+01 , 3.93768311e+01],
                [ 1.75041992e+02 , 2.79155273e+02, -7.48315430e+01],
                [ 8.01640625e+01 , 3.75714111e+01 , 3.94390869e+01],
                [ 1.70061523e+02 , 2.72680664e+02 ,-5.01782227e+01],
                [ 8.09111328e+01 , 4.27075195e+01 , 4.89953613e+01],
                [ 1.44412109e+02 , 2.58486328e+02 ,-5.89874268e+00],
                [ 1.02078125e+02 , 2.59233398e+02 , 5.83259583e+00],
                [ 1.38933594e+02 , 3.46391602e+02 , 2.04043579e+01],
                [ 1.02451660e+02 , 3.45644531e+02 , 2.53498077e+00],
                [ 1.36443359e+02 , 4.25581055e+02 , 1.32355957e+02],
                [ 1.03945801e+02  ,4.23339844e+02 , 1.16667480e+02],
                [ 1.32957031e+02 , 4.36289062e+02 , 1.38083496e+02],
                [ 1.07432129e+02 , 4.31308594e+02 , 1.22457275e+02],
                [ 1.41672852e+02 , 4.53720703e+02 , 2.89645386e+01],
                [ 1.06436035e+02 , 4.56210938e+02 , 1.43188477e+01],
                [ 1.23245117e+02 , 2.59233398e+02 , 4.82422113e-02],
                [ 1.27727539e+02 , 3.66375732e+01 , 3.87153625e-01],
                [ 1.76785156e+02 , 2.79155273e+02 , 1.45061016e-01],
                [ 1.78528320e+02 , 2.62719727e+02 , 1.91996098e-01],
                [ 7.91679688e+01 , 3.68554688e+01 , 2.73281336e-02],
                [ 7.51835938e+01 , 4.67541504e+01 ,-3.84539366e-02]]
        ap = np.array(ap0, dtype='float32')
        np_data = ap
        xp = np_data.T[0].T
        yp = np_data.T[1].T
        zp = np_data.T[2].T + 0.25
        
        ax = plt.axes(projection='3d')
        
        radius = 250
        ax.set_xlim3d([0, radius])
        ax.set_zlim3d([-radius / 2, radius / 2])
        ax.set_ylim3d([0, radius])
        ax.view_init(elev=15., azim=70)
        ax.dist = 7.5
        
        # 3D scatter
        ax.scatter3D(xp, yp, zp, cmap='Greens')

        for connection in self.connections:
            ax.plot([xp[connection[0]],xp[connection[1]]],[yp[connection[0]],yp[connection[1]]],[zp[connection[0]],zp[connection[1]]],ls='-', color='red')
        
        # # left leg, node [0, 1, 2, 3]
        # ax.plot(xp[0:4], yp[0:4], zp[0:4], ls='-', color='red')
        
        # # right leg
        # ax.plot(np.hstack((xp[0], xp[4:7])),
        #         np.hstack((yp[0], yp[4:7])),
        #         np.hstack((zp[0], zp[4:7])),
        #         ls='-', color='blue')
        
        # # spine, node [0, 7, 8, 9, 10]
        # ax.plot(np.hstack((xp[0], xp[7:11])),
        #         np.hstack((yp[0], yp[7:11])),
        #         np.hstack((zp[0], zp[7:11])),
        #         ls='-', color='gray')
        
        # # right arm, node [8, 11, 12, 13]
        # ax.plot(np.hstack((xp[8], xp[11:14])),
        #         np.hstack((yp[8], yp[11:14])),
        #         np.hstack((zp[8], zp[11:14])),
        #         ls='-', color='blue')
        
        # # left arm, node [8, 14, 15, 16]
        # ax.plot(np.hstack((xp[8], xp[14:])),
        #         np.hstack((yp[8], yp[14:])),
        #         np.hstack((zp[8], zp[14:])),
        #         ls='-', color='red')
        plt.savefig('skeleton.jpg')
