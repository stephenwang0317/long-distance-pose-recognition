from enum import Enum
from pose_recognitor import Pose


class DfaState(Enum):
    state_start = 0
    state_get_0 = 1
    state_get_1 = 2
    state_release_0 = 3
    state_release_1 = 4
    state_forward_0 = 5
    state_forward_1 = 6
    state_stop_0 = 7
    state_stop_1 = 8
    state_left_turn_0 = 9
    state_left_turn_1 = 10
    state_right_turn_0 = 11
    state_right_turn_1 = 12


class ActionRecognitor:
    def __init__(self) -> None:
        self.cur_state = DfaState.state_start
        self.next_state = DfaState.state_start
        self.end_state = [DfaState.state_get_1,
                          DfaState.state_stop_1,
                          DfaState.state_release_1,
                          DfaState.state_forward_1,
                          DfaState.state_left_turn_1,
                          DfaState.state_right_turn_1]
        self.end_state_count = 0
        self.state_table = {DfaState.state_start: {Pose.right_arm_up: DfaState.state_get_0,
                                                   Pose.all_arms_left: DfaState.state_release_0,
                                                   Pose.forward1: DfaState.state_forward_0,
                                                   Pose.all_arms_up: DfaState.state_stop_0,
                                                   Pose.left_turn1: DfaState.state_left_turn_0,
                                                   Pose.right_turn1: DfaState.state_right_turn_0,
                                                   Pose.other: DfaState.state_start,
                                                   Pose.forward2: DfaState.state_start,
                                                   Pose.left_turn2: DfaState.state_start,
                                                   Pose.right_turn2: DfaState.state_start
                                                   },
                            DfaState.state_get_0: {Pose.right_arm_up: DfaState.state_get_1,
                                                   Pose.other: DfaState.state_start,
                                                   Pose.all_arms_left: DfaState.state_start,
                                                   Pose.forward1: DfaState.state_start,
                                                   Pose.all_arms_up: DfaState.state_start,
                                                   Pose.left_turn1: DfaState.state_start,
                                                   Pose.right_turn1: DfaState.state_start,
                                                   Pose.forward2: DfaState.state_start,
                                                   Pose.left_turn2: DfaState.state_start,
                                                   Pose.right_turn2: DfaState.state_start
                                                   },
                            DfaState.state_get_1: {Pose.right_arm_up: DfaState.state_get_1,
                                                   Pose.other: DfaState.state_start,
                                                   Pose.all_arms_left: DfaState.state_start,
                                                   Pose.forward1: DfaState.state_start,
                                                   Pose.all_arms_up: DfaState.state_start,
                                                   Pose.left_turn1: DfaState.state_start,
                                                   Pose.right_turn1: DfaState.state_start,
                                                   Pose.forward2: DfaState.state_start,
                                                   Pose.left_turn2: DfaState.state_start,
                                                   Pose.right_turn2: DfaState.state_start
                                                   },
                            DfaState.state_release_0: {Pose.all_arms_left: DfaState.state_release_1,
                                                       Pose.other: DfaState.state_start,
                                                       Pose.forward1: DfaState.state_start,
                                                       Pose.right_arm_up: DfaState.state_start,
                                                       Pose.left_turn1: DfaState.state_start,
                                                       Pose.right_turn1: DfaState.state_start,
                                                       Pose.forward2: DfaState.state_start,
                                                       Pose.left_turn2: DfaState.state_start,
                                                       Pose.right_turn2: DfaState.state_start
                                                       },
                            DfaState.state_release_1: {Pose.all_arms_left: DfaState.state_release_1,
                                                       Pose.other: DfaState.state_start,
                                                       Pose.forward1: DfaState.state_start,
                                                       Pose.right_arm_up: DfaState.state_start,
                                                       Pose.left_turn1: DfaState.state_start,
                                                       Pose.right_turn1: DfaState.state_start,
                                                       Pose.forward2: DfaState.state_start,
                                                       Pose.left_turn2: DfaState.state_start,
                                                       Pose.right_turn2: DfaState.state_start
                                                       },
                            DfaState.state_forward_0: {Pose.forward1: DfaState.state_forward_0,
                                                       Pose.forward2: DfaState.state_forward_1,
                                                       Pose.other: DfaState.state_start,
                                                       Pose.all_arms_left: DfaState.state_start,
                                                       Pose.all_arms_up: DfaState.state_start,
                                                       Pose.right_arm_up: DfaState.state_start,
                                                       Pose.left_turn1: DfaState.state_start,
                                                       Pose.right_turn1: DfaState.state_start,
                                                       Pose.left_turn2: DfaState.state_start,
                                                       Pose.right_turn2: DfaState.state_start
                                                       },
                            DfaState.state_forward_1: {Pose.forward2: DfaState.state_forward_1,
                                                       Pose.other: DfaState.state_start,
                                                       Pose.all_arms_left: DfaState.state_start,
                                                       Pose.all_arms_up: DfaState.state_start,
                                                       Pose.right_arm_up: DfaState.state_start,
                                                       Pose.forward1: DfaState.state_start,
                                                       Pose.left_turn1: DfaState.state_start,
                                                       Pose.right_turn1: DfaState.state_start,
                                                       Pose.left_turn2: DfaState.state_start,
                                                       Pose.right_turn2: DfaState.state_start
                                                       },
                            DfaState.state_stop_0: {Pose.all_arms_up: DfaState.state_stop_1,
                                                    Pose.other: DfaState.state_start,
                                                    Pose.all_arms_left: DfaState.state_start,
                                                    Pose.forward2: DfaState.state_start,
                                                    Pose.right_arm_up: DfaState.state_start,
                                                    Pose.forward1: DfaState.state_start,
                                                    Pose.left_turn1: DfaState.state_start,
                                                    Pose.right_turn1: DfaState.state_start,
                                                    Pose.left_turn2: DfaState.state_start,
                                                    Pose.right_turn2: DfaState.state_start
                                                    },
                            DfaState.state_stop_1: {Pose.all_arms_up: DfaState.state_stop_1,
                                                    Pose.other: DfaState.state_start,
                                                    Pose.all_arms_left: DfaState.state_start,
                                                    Pose.forward2: DfaState.state_start,
                                                    Pose.right_arm_up: DfaState.state_start,
                                                    Pose.forward1: DfaState.state_start,
                                                    Pose.left_turn1: DfaState.state_start,
                                                    Pose.right_turn1: DfaState.state_start,
                                                    Pose.left_turn2: DfaState.state_start,
                                                    Pose.right_turn2: DfaState.state_start
                                                    },
                            DfaState.state_left_turn_0: {Pose.left_turn1: DfaState.state_left_turn_0,
                                                         Pose.left_turn2: DfaState.state_left_turn_1,
                                                         Pose.other: DfaState.state_start,
                                                         Pose.all_arms_left: DfaState.state_start,
                                                         Pose.forward2: DfaState.state_start,
                                                         Pose.right_arm_up: DfaState.state_start,
                                                         Pose.forward1: DfaState.state_start,
                                                         Pose.all_arms_up: DfaState.state_start,
                                                         Pose.right_turn1: DfaState.state_start,
                                                         Pose.right_turn2: DfaState.state_start
                                                         },
                            DfaState.state_left_turn_1: {Pose.left_turn2: DfaState.state_left_turn_1,
                                                         Pose.other: DfaState.state_start,
                                                         Pose.all_arms_left: DfaState.state_start,
                                                         Pose.forward2: DfaState.state_start,
                                                         Pose.right_arm_up: DfaState.state_start,
                                                         Pose.forward1: DfaState.state_start,
                                                         Pose.left_turn1: DfaState.state_start,
                                                         Pose.right_turn1: DfaState.state_start,
                                                         Pose.all_arms_up: DfaState.state_start,
                                                         Pose.right_turn2: DfaState.state_start
                                                         },
                            DfaState.state_right_turn_0: {Pose.right_turn1: DfaState.state_right_turn_0,
                                                          Pose.right_turn2: DfaState.state_right_turn_1,
                                                          Pose.other: DfaState.state_start,
                                                          Pose.all_arms_left: DfaState.state_start,
                                                          Pose.forward2: DfaState.state_start,
                                                          Pose.right_arm_up: DfaState.state_start,
                                                          Pose.forward1: DfaState.state_start,
                                                          Pose.all_arms_up: DfaState.state_start,
                                                          Pose.left_turn1: DfaState.state_start,
                                                          Pose.left_turn2: DfaState.state_start
                                                          },
                            DfaState.state_right_turn_1: {Pose.right_turn2: DfaState.state_right_turn_1,
                                                          Pose.other: DfaState.state_start,
                                                          Pose.all_arms_left: DfaState.state_start,
                                                          Pose.forward2: DfaState.state_start,
                                                          Pose.right_arm_up: DfaState.state_start,
                                                          Pose.forward1: DfaState.state_start,
                                                          Pose.left_turn1: DfaState.state_start,
                                                          Pose.right_turn1: DfaState.state_start,
                                                          Pose.all_arms_up: DfaState.state_start,
                                                          Pose.left_turn2: DfaState.state_start
                                                          }
                            }

    def forward(self, input):
        pose_id = input
        self.next_state = self.state_table.get(self.cur_state).get(pose_id)
        if self.next_state in self.end_state and self.next_state != self.cur_state:
            self.end_state_count += 1
            print(str(self.end_state_count) + ": " + self.next_state.name)
        self.cur_state = self.next_state
        return self.cur_state
