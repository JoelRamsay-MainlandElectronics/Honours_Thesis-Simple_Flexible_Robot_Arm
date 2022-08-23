from user_variables import UserVariables

class globals(object):
    #Globals=====================
    # global estop_flag
    # global cycle_start_flag
    # global shutdown_flag

    cycle_start_flag = 0
    estop_flag = 0  # 1 for estop condition, 0 for normal operation.
    shutdown_flag = 0
    feedhold_flag = 0
    reset_flag = 0

    root = 0
    robot_gui = 0
    stop_threads = 0
    mode = UserVariables.motor_method
    mode_changed_flag = 0
    controller_checkbox_flag = 0