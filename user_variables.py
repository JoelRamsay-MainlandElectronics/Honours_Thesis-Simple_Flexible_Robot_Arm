class UserVariables(object):
    disable_controller = False #By default, have the vibration controller on.
    use_game_controller = True
    motor_methods = ["position", "velocity", "torque"]
    motor_method = motor_methods[1] #by default, select position control mode.
    point_to_point = True


    #PID Controller gains for TORQUE CONTROL MODE################################################################
    #Joint control
    Kp_j_elbow = 2#0.34#2#20 #2 %These will need to be adjusted because of the 0.17 scaling for the pixels to angle.
    Kd_j_elbow = 0.25#0.04#0.25#10 #0.25
    Ki_j_elbow = 0.15#0.02#0.15#0.00001 #0.15

    Kp_j_shoulder = 10#1.7#10#0 #10
    Kd_j_shoulder = 4#0.68#4#0.000001 #4
    Ki_j_shoulder = 0.15#0.02#0.15#0.000001 #0.15

    #Vibration Control
    Kp_v_lower_arm = 0.03#0.2#0.2#50 #0.2
    Kd_v_lower_arm = 0.01#0.01#50 #0.01
    Ki_v_lower_arm = 0

    Kp_v_upper_arm = 0#0.05#0.0 #0.05 #increasing this makes the robot more compliant
    Kd_v_upper_arm = 0#0.01#0.0 #0.01
    Ki_v_upper_arm = 0
    #################################################################################################################


    #PID Controller gains for POSITION CONTROL MODE################################################################
    # Joint control
    Kp_j_elbow_position = 1500  # 20 #2
    Kd_j_elbow_position = 0  # 10 #0.25
    Ki_j_elbow_position = 0.000001  # 0.00001 #0.15

    Kp_j_shoulder_position = 1500  # 0 #10
    Kd_j_shoulder_position = 0  # 0.000001 #4
    Ki_j_shoulder_position = 0.000001  # 0.000001 #0.15

    # Vibration Control
    Kp_v_lower_arm_position = 0.58  # 0.2#50 #0.2
    Kd_v_lower_arm_position = 0  # 0.01#50 #0.01
    Ki_v_lower_arm_position = 0

    Kp_v_upper_arm_position = 0.1  # 0.05#0.0 #0.05 #increasing this makes the robot more compliant
    Kd_v_upper_arm_position = 0  # 0.01#0.0 #0.01
    Ki_v_upper_arm_position = 0
    ####################################################################################################################


    # PID Controller gains for VELOCITY CONTROL MODE################################################################
    # Joint control
    Kp_j_elbow_velocity = 80  # 20 #2
    Kd_j_elbow_velocity = 0  # 10 #0.25
    Ki_j_elbow_velocity = 0.00001  # 0.00001 #0.15

    Kp_j_shoulder_velocity = 100  # 0 #10
    Kd_j_shoulder_velocity = 10  # 0.000001 #4
    Ki_j_shoulder_velocity = 0.0001  # 0.000001 #0.15

    # Vibration Control
    Kp_v_lower_arm_velocity = 10 #10  # 0.2#50 #0.2
    Kd_v_lower_arm_velocity = 0  # 0.01#50 #0.01
    Ki_v_lower_arm_velocity = 0

    Kp_v_upper_arm_velocity = 5  # 0.05#0.0 #0.05 #increasing this makes the robot more compliant
    Kd_v_upper_arm_velocity = 0  # 0.01#0.0 #0.01
    Ki_v_upper_arm_velocity = 0





    #Motor Current Limits
    elbow_current_lim = 2000
    shoulder_current_lim = 2000

    #Motor Position Limits
    elbow_position_min = 228
    elbow_position_max = 3389
    shoulder_position_min = 683
    shoulder_position_max = 3414

    #Motor Velocity Limits
    elbow_velocity_lim = 1023 #MAX 1023 ~50rpm
    shoulder_velocity_lim = 1023 #MAX 1023 ~50rpm

    #Uncropped frame height is 600, width is 400
    elbow_x1 = 0
    elbow_x2 = 400
    elbow_y1 = 250
    elbow_y2 = 150

    shoulder_x1 = 150  #crops the left of frame
    shoulder_x2 = 100  #crops the right of frame
    shoulder_y1 = 225  #crops the top of frame
    shoulder_y2 = 125  #crops the bottom of frame

    update_frequency = 60 #Hertz






    #Motion related variables
    elbow_start = 155
    elbow_end = 155
    shoulder_start = 155
    shoulder_end = 155
    timespan = 3 #time to move through motion

    #Home position
    elbow_home = 180
    shoulder_home = 180
    timespan_home = 3 #time to return home

    #pixels to degrees scaling factor
    deflection_scaling = 0.17

    camera_ISO = 1600
    camera_exposure = 1000




    # PID Controller gains for velocity control mode (internal Dynamixel gain parameters)
    Kp_velocity_elbow = 200
    Ki_velocity_elbow = 0

    Kp_velocity_shoulder = 200
    Ki_velocity_shoulder = 0
    #####################################################################################

    # PID Controller gains for position control mode (internal Dynamixel gain parameters)
    Kp_position_elbow = 250 #250 proportional and 0 d works great.
    Ki_position_elbow = 0
    Kd_position_elbow = 0

    Kp_position_shoulder = 500
    Ki_position_shoulder = 0
    Kd_position_shoulder = 0
    ########################################################################################
