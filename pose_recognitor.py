import numpy as np
from enum import Enum
import math


class Pose(Enum):
    other = 0
    # stand = 1
    right_arm_up = 2
    all_arms_left = 3
    # all_arms_right = 4
    forward1 = 5
    forward2 = 6
    all_arms_up = 7
    left_turn1 = 8
    left_turn2 = 9
    right_turn1 = 10
    right_turn2 = 11


COS_0 = math.cos(math.radians(0))
COS_20 = math.cos(math.radians(20))
COS_30 = math.cos(math.radians(30))
COS_60 = math.cos(math.radians(60))
COS_70 = math.cos(math.radians(70))
COS_90 = math.cos(math.radians(90))
COS_110 = math.cos(math.radians(110))
COS_120 = math.cos(math.radians(120))
COS_135 = math.cos(math.radians(135))
COS_150 = math.cos(math.radians(150))
COS_180 = math.cos(math.radians(180))


def calculate_angle(a, b, c):
    """

    Args:
        a: point coordinate, the first point
        b: point coordinate, the middle point
        c: point coordinate, the last point

    Returns:
        double: the degree of angle (b,a),(b,c)
    """
    x1 = a[0] - b[0]
    y1 = a[1] - b[1]
    x2 = c[0] - b[0]
    y2 = c[1] - b[1]
    v1 = np.array([x1, y1])
    v2 = np.array([x2, y2])
    len1 = np.linalg.norm(v1)
    len2 = np.linalg.norm(v2)
    if len1 == 0 or len2 == 0:
        return 0
    else:
        dot = np.dot(v1, v2)
        arccos = np.arccos(dot / (len1 * len2))
        angle_ = np.degrees(arccos)
        return angle_


def calculate_angle2(a, b, c, d):
    """

    Args:
        a: start of Vector A
        b: end of Vector A
        c: start of Vector B
        d: end of Vector B

    Returns:
        double: the degree of angle (a,b),(c,d)
    """
    x1 = a[0] - b[0]
    y1 = a[1] - b[1]
    x2 = c[0] - d[0]
    y2 = c[1] - d[1]
    angle_ = math.degrees(
        math.acos((x1 * x2 + y1 * y2) / (((x1 ** 2 + y1 ** 2) ** 0.5) * ((x2 ** 2 + y2 ** 2) ** 0.5))))
    return angle_


class PoseRecognitor:
    def __init__(self):
        self.keypoints = None

    def cos(self, point_c: int, point_s1: int, point_s2: int):

        vec1 = self.keypoints[point_s1] - self.keypoints[point_c]
        vec2 = self.keypoints[point_s2] - self.keypoints[point_c]
        vec1_len = math.sqrt(vec1[0] ** 2 + vec1[1] ** 2)
        vec2_len = math.sqrt(vec2[0] ** 2 + vec2[1] ** 2)
        cos = (vec1[0] * vec2[0] + vec1[1] * vec2[1]) / (vec1_len * vec2_len)
        return cos

    def cos_vec(self, vec1: np.array, vec2: np.array):
        vec1_len = math.sqrt(vec1[0] ** 2 + vec1[1] ** 2)
        vec2_len = math.sqrt(vec2[0] ** 2 + vec2[1] ** 2)
        cos = (vec1[0] * vec2[0] + vec1[1] * vec2[1]) / (vec1_len * vec2_len)
        return cos

    def recognize(self, keypoints: list):
        self.keypoints = keypoints
        left_elbow = calculate_angle(keypoints[11], keypoints[13], keypoints[15])
        right_elbow = calculate_angle(keypoints[12], keypoints[14], keypoints[16])
        left_armpit = calculate_angle(keypoints[13], keypoints[11], keypoints[23])
        right_armpit = calculate_angle(keypoints[14], keypoints[12], keypoints[24])

        # 姿势二（右手上举过头顶）：
        # 左肘关节角度：120°~180°
        # 右肘关节角度：120°~180°
        # 左肩腋下角度：0°~30°
        # 右肩腋下角度：120°~180°

        # 姿势三（双臂上举）
        # 左肘关节角度：150°~180°
        # 右肘关节角度：150°~180°
        # 左肩腋下角度：120°~180°
        # 右肩腋下角度：120°~180°

        if 120 < right_armpit < 180 and 120 < right_elbow < 180:
            if 120 < left_armpit < 180 and 120 < left_elbow < 180:
                return Pose.all_arms_up
            else:
                return Pose.right_arm_up

        # 姿势三（双手指向左侧）：
        # 左肘关节角度：150°~180°
        # 左肩腋下角度：70°~110°
        # 右前臂和双肩代表水平方向的夹角：0°~20°
        # 右腕关节点的X坐标大于右肘关节点的坐标
        #
        # if COS_180 < cos_left_elbow < COS_150 \
        #         and COS_110 < cos_left_armpit < COS_70 \
        #         and COS_20 < self.cos_vec(self.keypoints[38] - self.keypoints[14],
        #                                   self.keypoints[11] - self.keypoints[12]) < COS_0 \
        #         and self.keypoints[38][0] > self.keypoints[14][0]:
        #     return Pose.all_arms_left

        # 姿势四（双手指向右侧）
        # 右肘关节角度：150°~180°
        # 右肩腋下角度：70°~110°
        # 左前臂和双肩代表水平方向的夹角：0°~20°
        # 左腕关节的X坐标小于左肘关节点的坐标
        if 120 < left_elbow < 180 and 60 < left_armpit < 120 \
                and 0 < calculate_angle2(keypoints[12], keypoints[11], keypoints[14], keypoints[16]) < 30:
            return Pose.all_arms_left

        # 姿势五（双臂斜向外张开）
        # 左肘关节角度：60°~110°
        # 右肘关节角度：60°~110°
        # 左肩腋下角度：0°~30°
        # 右肩腋下角度：0°~30°
        # 左腕关节点X坐标大于左肘关节点坐标
        # 右腕关节点X坐标小于右肘关节点坐标
        if 150 < left_elbow < 180 and 150 < right_elbow < 180 \
                and 50 < left_armpit < 90 and 50 < right_armpit < 90:
            return Pose.forward1

        # 姿势六（双臂曲折收缩）
        # 左肘关节角度：0°~30°
        # 右肘关机角度：0°~30°
        # 左肩腋下角度：0°~30°
        # 右肩腋下角度：0°~30°

        if 0 < left_elbow < 30 and 0 < right_elbow < 30 \
                and 50 < left_armpit < 90 and 50 < right_armpit < 90:
            return Pose.forward2
        #
        # # 姿势八（左转1）
        # # 左肘关节角度：90°~180°
        # # 右肘关节角度：150°~180°
        # # 左腕关节点Y坐标小于左肘坐标
        # # 左肩腋下角度：70°~110°
        # # 右肩腋下角度：70°~110°
        # # 左肘关节点X坐标大于左肩关节点坐标
        # # 右肘关节点X坐标小于右肩关节点坐标
        # if COS_180 < cos_left_elbow < COS_90 and COS_180 < cos_right_elbow < COS_150 \
        #         and COS_110 < cos_left_armpit < COS_70 and COS_110 < cos_right_armpit < COS_70 \
        #         and self.keypoints[36][1] < self.keypoints[13][1] \
        #         and self.keypoints[13][0] > self.keypoints[11][0] \
        #         and self.keypoints[14][0] < self.keypoints[12][0]:
        #     return Pose.left_turn1
        #
        # # 姿势九（左转完成姿势）
        # # 左肘关节角度：20°~90°
        # # 左腕关节点Y坐标小于左肘坐标
        # # 右肘关节角度：150°~180°
        # # 左肩腋下角度：70°~110°
        # # 右肩腋下角度：70°~110°
        # # 左肘关节点X坐标大于左肩关节点坐标
        # # 右肘关节点X坐标小于右肩关节点坐标
        # if COS_90 < cos_left_elbow < COS_20 and COS_180 < cos_right_elbow < COS_150 \
        #         and COS_110 < cos_left_armpit < COS_70 and COS_110 < cos_right_armpit < COS_70 \
        #         and self.keypoints[36][1] < self.keypoints[13][1] \
        #         and self.keypoints[13][0] > self.keypoints[11][0] \
        #         and self.keypoints[14][0] < self.keypoints[12][0]:
        #     return Pose.left_turn2
        #
        # # 姿势十（右转1）
        # # 左肘关节角度：150°~180°
        # # 右肘关节角度：90°~180°
        # # 右腕关节点Y坐标小于右肘坐标
        # # 左肩腋下角度：70°~110°
        # # 右肩腋下角度：70°~110°
        # # 左肘关节点X坐标大于左肩关节点坐标
        # # 右肘关节点X坐标小于右肩关节点坐标
        # if COS_180 < cos_left_elbow < COS_150 and COS_180 < cos_right_elbow < COS_90 \
        #         and COS_110 < cos_left_armpit < COS_70 and COS_110 < cos_right_armpit < COS_70 \
        #         and self.keypoints[38][1] < self.keypoints[14][1] \
        #         and self.keypoints[13][0] > self.keypoints[11][0] \
        #         and self.keypoints[14][0] < self.keypoints[12][0]:
        #     return Pose.right_turn1
        #
        # # 姿势十一（右转完成姿势）
        # # 左肘关节角度：150°~180°
        # # 右肘关节角度：20°~60°
        # # 右腕关节点Y坐标小于右肘坐标
        # # 左肩腋下角度：70°~110°
        # # 右肩腋下角度：70°~110°
        # # 左肘关节点X坐标大于左肩关节点坐标
        # # 右肘关节点X坐标小于右肩关节点坐标
        #
        # if COS_180 < cos_left_elbow < COS_150 and COS_60 < cos_right_elbow < COS_20 \
        #         and COS_110 < cos_left_armpit < COS_70 and COS_110 < cos_right_armpit < COS_70 \
        #         and self.keypoints[38][1] < self.keypoints[14][1] \
        #         and self.keypoints[13][0] > self.keypoints[11][0] \
        #         and self.keypoints[14][0] < self.keypoints[12][0]:
        #     return Pose.right_turn2

        return Pose.other
