from enum import Enum

class DfaState():
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

class pose():
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


class ActionRecognitor:
    def __init__(self) -> None:
        self.cur_state = DfaState.state_start
        self.next_state = DfaState.state_start
        self.state_table = {DfaState.state_start: {pose.right_arm_up:DfaState.state_get_0, 
                                                   pose.all_arms_left:DfaState.state_release_0, 
                                                   pose.forward1:DfaState.state_forward_0,
                                                   pose.all_arms_up:DfaState.state_stop_0,
                                                   pose.left_turn1:DfaState.state_left_turn_0,
                                                   pose.right_turn1:DfaState.state_right_turn_0,
                                                   
                                                   pose.other:DfaState.state_start,
                                                   pose.forward2:DfaState.state_start,
                                                   pose.left_turn2:DfaState.state_start,
                                                   pose.right_turn2:DfaState.state_start
                                                   }, 
                            DfaState.state_get_0: {pose.right_arm_up:DfaState.state_get_1,
                                                   
                                                   pose.other:DfaState.state_start,
                                                   pose.all_arms_left:DfaState.state_start, 
                                                   pose.forward1:DfaState.state_start,
                                                   pose.all_arms_up:DfaState.state_start,
                                                   pose.left_turn1:DfaState.state_start,
                                                   pose.right_turn1:DfaState.state_start,
                                                   pose.forward2:DfaState.state_start,
                                                   pose.left_turn2:DfaState.state_start,
                                                   pose.right_turn2:DfaState.state_start},
                            DfaState.state_get_1: {pose.right_arm_up:DfaState.state_get_1,
                                                   
                                                   pose.other:DfaState.state_start,
                                                   pose.all_arms_left:DfaState.state_start, 
                                                   pose.forward1:DfaState.state_start,
                                                   pose.all_arms_up:DfaState.state_start,
                                                   pose.left_turn1:DfaState.state_start,
                                                   pose.right_turn1:DfaState.state_start,
                                                   pose.forward2:DfaState.state_start,
                                                   pose.left_turn2:DfaState.state_start,
                                                   pose.right_turn2:DfaState.state_start},
                            DfaState.state_release_0: {pose.all_arms_left:DfaState.state_release_1,
                                                       
                                                        pose.other:DfaState.state_start,
                                                        pose.all_arms_left:DfaState.state_start, 
                                                        pose.forward1:DfaState.state_start,
                                                        pose.right_arm_up:DfaState.state_start,
                                                        pose.left_turn1:DfaState.state_start,
                                                        pose.right_turn1:DfaState.state_start,
                                                        pose.forward2:DfaState.state_start,
                                                        pose.left_turn2:DfaState.state_start,
                                                        pose.right_turn2:DfaState.state_start
                                                       },
                            DfaState.state_release_1: {pose.all_arms_left:DfaState.state_release_1,
                                                       
                                                        pose.other:DfaState.state_start,
                                                        pose.all_arms_left:DfaState.state_start, 
                                                        pose.forward1:DfaState.state_start,
                                                        pose.right_arm_up:DfaState.state_start,
                                                        pose.left_turn1:DfaState.state_start,
                                                        pose.right_turn1:DfaState.state_start,
                                                        pose.forward2:DfaState.state_start,
                                                        pose.left_turn2:DfaState.state_start,
                                                        pose.right_turn2:DfaState.state_start},
                            DfaState.state_forward_0: {pose.forward1:DfaState.state_forward_0, 
                                                       pose.forward2:DfaState.state_forward_1,
                                                       
                                                        pose.other:DfaState.state_start,
                                                        pose.all_arms_left:DfaState.state_start, 
                                                        pose.all_arms_up:DfaState.state_start,
                                                        pose.right_arm_up:DfaState.state_start,
                                                        pose.left_turn1:DfaState.state_start,
                                                        pose.right_turn1:DfaState.state_start,
                                                        pose.left_turn2:DfaState.state_start,
                                                        pose.right_turn2:DfaState.state_start
                                                       },
                            DfaState.state_forward_1: {pose.forward2:DfaState.state_forward_1,
                                                       
                                                        pose.other:DfaState.state_start,
                                                        pose.all_arms_left:DfaState.state_start, 
                                                        pose.all_arms_up:DfaState.state_start,
                                                        pose.right_arm_up:DfaState.state_start,
                                                        pose.forward1:DfaState.state_start,
                                                        pose.left_turn1:DfaState.state_start,
                                                        pose.right_turn1:DfaState.state_start,
                                                        pose.left_turn2:DfaState.state_start,
                                                        pose.right_turn2:DfaState.state_start},
                            DfaState.state_stop_0: {pose.all_arms_up:DfaState.state_stop_1,
                                                    
                                                    pose.other:DfaState.state_start,
                                                    pose.all_arms_left:DfaState.state_start, 
                                                    pose.forward2:DfaState.state_start,
                                                    pose.right_arm_up:DfaState.state_start,
                                                    pose.forward1:DfaState.state_start,
                                                    pose.left_turn1:DfaState.state_start,
                                                    pose.right_turn1:DfaState.state_start,
                                                    pose.left_turn2:DfaState.state_start,
                                                    pose.right_turn2:DfaState.state_start},
                            DfaState.state_stop_1: {pose.all_arms_up:DfaState.state_stop_1,
                                                    
                                                    pose.other:DfaState.state_start,
                                                    pose.all_arms_left:DfaState.state_start, 
                                                    pose.forward2:DfaState.state_start,
                                                    pose.right_arm_up:DfaState.state_start,
                                                    pose.forward1:DfaState.state_start,
                                                    pose.left_turn1:DfaState.state_start,
                                                    pose.right_turn1:DfaState.state_start,
                                                    pose.left_turn2:DfaState.state_start,
                                                    pose.right_turn2:DfaState.state_start},
                            DfaState.state_left_turn_0: {pose.left_turn1:DfaState.state_left_turn_0,
                                                         pose.left_turn2:DfaState.state_left_turn_1,
                                                         
                                                            pose.other:DfaState.state_start,
                                                            pose.all_arms_left:DfaState.state_start, 
                                                            pose.forward2:DfaState.state_start,
                                                            pose.right_arm_up:DfaState.state_start,
                                                            pose.forward1:DfaState.state_start,
                                                            pose.all_arms_up:DfaState.state_start,
                                                            pose.right_turn1:DfaState.state_start,
                                                            pose.right_turn2:DfaState.state_start},
                            DfaState.state_left_turn_1: {pose.left_turn2:DfaState.state_left_turn_1,
                                                         
                                                            pose.other:DfaState.state_start,
                                                            pose.all_arms_left:DfaState.state_start, 
                                                            pose.forward2:DfaState.state_start,
                                                            pose.right_arm_up:DfaState.state_start,
                                                            pose.forward1:DfaState.state_start,
                                                            pose.left_turn1:DfaState.state_start,
                                                            pose.right_turn1:DfaState.state_start,
                                                            pose.all_arms_up:DfaState.state_start,
                                                            pose.right_turn2:DfaState.state_start},
                            DfaState.state_right_turn_0: {pose.right_turn1:DfaState.state_right_turn_0, 
                                                          pose.right_turn2:DfaState.state_right_turn_1,

                                                            pose.other:DfaState.state_start,
                                                            pose.all_arms_left:DfaState.state_start, 
                                                            pose.forward2:DfaState.state_start,
                                                            pose.right_arm_up:DfaState.state_start,
                                                            pose.forward1:DfaState.state_start,
                                                            pose.all_arms_up:DfaState.state_start,
                                                            pose.left_turn1:DfaState.state_start,
                                                            pose.left_turn2:DfaState.state_start},
                            DfaState.state_right_turn_1: {pose.right_turn2:DfaState.state_right_turn_1,
                                                          
                                                            pose.other:DfaState.state_start,
                                                            pose.all_arms_left:DfaState.state_start, 
                                                            pose.forward2:DfaState.state_start,
                                                            pose.right_arm_up:DfaState.state_start,
                                                            pose.forward1:DfaState.state_start,
                                                            pose.left_turn1:DfaState.state_start,
                                                            pose.right_turn1:DfaState.state_start,
                                                            pose.all_arms_up:DfaState.state_start,
                                                            pose.left_turn2:DfaState.state_start}}

    def forward(self, input):
        pose_id = input
        self.next_state = self.state_table.get(self.cur_state).get(pose_id)
        self.cur_state = self.next_state
        return self.cur_state

        
