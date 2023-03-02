import math
from enum import Enum


class DfaState(Enum):
    state_start = 0
    state_get_0 = 1
    state_get_1 = 2
    state_release_0 = 3
    state_release_1 = 4
    state_stop_0 = 5
    state_stop_1 = 6


class DfaAction(Enum):
    only_right_arm_up = 0
    all_arms_up = 1
    all_arms_horizontal = 2
    release_action = 3


def calculate_angle(a, b, c):
    """

    Args:
        a: point coordinate, the first point
        b: point coordinate, the middle point
        c: point coordinate, the last point

    Returns:
        double: the degree of angle (a,b),(b,c)
    """
    x1 = b[0] - a[0]
    y1 = b[1] - a[1]
    x2 = b[0] - c[0]
    y2 = b[1] - c[1]
    angle_ = math.degrees(
        math.acos((x1 * x2 + y1 * y2) / (((x1 ** 2 + y1 ** 2) ** 0.5) * ((x2 ** 2 + y2 ** 2) ** 0.5))))
    return angle_


def check_right_arm_vertical(points, thresh=100):
    """
    Args:
        points: points list
        thresh: threshold angle
    Returns:
        boolean:  the right arm is up
    """
    prev = points[12][1]
    for i in [14, 16]:
        cur = points[i][1]
        if cur - prev < 0:
            prev = cur
        else:
            return False
    angle_ = calculate_angle(points[14], points[12], points[24])
    if angle_ < thresh:
        return False
    return True


def check_left_arm_vertical(points, thresh=100):
    """
    Args:
        points: points list
        thresh: threshold angle
    Returns:
        boolean:  the left arm is up
    """
    prev = points[11][1]
    for i in [13, 15]:
        cur = points[i][1]
        if cur - prev < 0:
            prev = cur
        else:
            return False
    angle_ = calculate_angle(points[13], points[11], points[23])
    if angle_ < thresh:
        return False
    return True


def check_right_arm_horizontal(points, thresh_1=80, thresh_2=100):
    """
    Args:
        points: points list
        thresh_1: low threshold angle
        thresh_2: high threshold angle
    Returns:
        Boolean:
    """
    prev = points[12][0]
    for i in [14, 16]:
        cur = points[i][0]
        if cur < prev:
            prev = cur
        else:
            return False
    angle_ = calculate_angle(points[14], points[12], points[24])
    if angle_ < thresh_1 or angle_ > thresh_2:
        return False
    return True


def check_left_arm_horizontal(points, thresh_1=80, thresh_2=100):
    """
    Args:
        points:
        thresh_1: low threshold angle
        thresh_2: high threshold angle

    Returns:
        Boolean:
    """
    prev = points[11][0]
    for i in [13, 15]:
        cur = points[i][0]
        if cur > prev:
            prev = cur
        else:
            return False
    angle_ = calculate_angle(points[13], points[11], points[23])
    if angle_ < thresh_1 or angle_ > thresh_2:
        return False
    return True


def get_action(points):
    if check_right_arm_vertical(points):
        if check_left_arm_vertical(points):
            return DfaAction.all_arms_up
        else:
            return DfaAction.only_right_arm_up

    if check_left_arm_horizontal(points):
        if check_right_arm_vertical(points):
            return DfaAction.all_arms_horizontal



class Dfa:
    def __init__(self):
        self.cur_state = DfaState.state_start
        self.end_state_count = 0

    def process(self, points):
        action = get_action(points)
        if self.cur_state == DfaState.state_start:
            if action == DfaAction.only_right_arm_up:
                self.cur_state = DfaState.state_get_0
            elif action == DfaAction.all_arms_up:
                self.cur_state = DfaState.state_stop_0
            else:
                self.cur_state = DfaState.state_start
        elif self.cur_state == DfaState.state_get_0:
            if action == DfaAction.only_right_arm_up:
                self.cur_state = DfaState.state_get_1
                self.end_state_count += 1
                print(str(self.end_state_count)+" get")

            else:
                self.cur_state = DfaState.state_start
        elif self.cur_state == DfaState.state_get_1:
            if action == DfaAction.only_right_arm_up:
                self.cur_state = DfaState.state_get_1
                # print("get")
            else:
                self.cur_state = DfaState.state_start
        elif self.cur_state == DfaState.state_stop_0:
            if action == DfaAction.all_arms_up:
                self.cur_state = DfaState.state_stop_1
                self.end_state_count += 1
                print(str(self.end_state_count)+" stop")
            else:
                self.cur_state = DfaState.state_start
        elif self.cur_state == DfaState.state_stop_1:
            if action == DfaAction.all_arms_up:
                self.cur_state = DfaState.state_stop_1
                # print("stop")
            else:
                self.cur_state = DfaState.state_start

    def get_state(self):
        return self.cur_state
