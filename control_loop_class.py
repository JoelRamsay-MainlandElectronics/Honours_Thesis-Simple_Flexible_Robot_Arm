from user_variables import *
from record_data_class import *


class control_system(object):
    def __init__(self, identity, frame_processing_object):
        self.identity = identity
        self.e_i = 0
        self.e_d = 0
        self.position_error_last = 0
        #self.disable_processing_flag = frame_processing_object
        self.frame_processing_object = frame_processing_object
        #print(frame_processing_object.disable_controller_flag)

        if self.identity == "Elbow":
            if UserVariables.motor_method == "torque":
                self.Kp_j = UserVariables.Kp_j_elbow
                self.Ki_j = UserVariables.Ki_j_elbow
                self.Kd_j = UserVariables.Kd_j_elbow

                self.Kp_v = UserVariables.Kp_v_lower_arm
                self.Ki_v = UserVariables.Ki_v_lower_arm
                self.Kd_v = UserVariables.Kd_v_lower_arm

            elif UserVariables.motor_method == "position":
                self.Kp_j = UserVariables.Kp_j_elbow_position
                self.Ki_j = UserVariables.Ki_j_elbow_position
                self.Kd_j = UserVariables.Kd_j_elbow_position

                self.Kp_v = UserVariables.Kp_v_lower_arm_position
                self.Ki_v = UserVariables.Ki_v_lower_arm_position
                self.Kd_v = UserVariables.Kd_v_lower_arm_position

            elif UserVariables.motor_method == "velocity":
                self.Kp_j = UserVariables.Kp_j_elbow_velocity
                self.Ki_j = UserVariables.Ki_j_elbow_velocity
                self.Kd_j = UserVariables.Kd_j_elbow_velocity

                self.Kp_v = UserVariables.Kp_v_lower_arm_velocity
                self.Ki_v = UserVariables.Ki_v_lower_arm_velocity
                self.Kd_v = UserVariables.Kd_v_lower_arm_velocity


            self.current_limit = UserVariables.elbow_current_lim
            self.position_min = UserVariables.elbow_position_min
            self.position_max = UserVariables.elbow_position_max
            self.velocity_limit = UserVariables.elbow_velocity_lim

        elif self.identity == "Shoulder":
            if UserVariables.motor_method == "torque":
                self.Kp_j = UserVariables.Kp_j_shoulder
                self.Ki_j = UserVariables.Ki_j_shoulder
                self.Kd_j = UserVariables.Kd_j_shoulder

                self.Kp_v = UserVariables.Kp_v_upper_arm
                self.Ki_v = UserVariables.Ki_v_upper_arm
                self.Kd_v = UserVariables.Kd_v_upper_arm

            elif UserVariables.motor_method == "position":
                self.Kp_j = UserVariables.Kp_j_shoulder_position
                self.Ki_j = UserVariables.Ki_j_shoulder_position
                self.Kd_j = UserVariables.Kd_j_shoulder_position

                self.Kp_v = UserVariables.Kp_v_upper_arm_position
                self.Ki_v = UserVariables.Ki_v_upper_arm_position
                self.Kd_v = UserVariables.Kd_v_upper_arm_position

            elif UserVariables.motor_method == "velocity":
                self.Kp_j = UserVariables.Kp_j_shoulder_velocity
                self.Ki_j = UserVariables.Ki_j_shoulder_velocity
                self.Kd_j = UserVariables.Kd_j_shoulder_velocity

                self.Kp_v = UserVariables.Kp_v_upper_arm_velocity
                self.Ki_v = UserVariables.Ki_v_upper_arm_velocity
                self.Kd_v = UserVariables.Kd_v_upper_arm_velocity

            self.current_limit = UserVariables.shoulder_current_lim
            self.position_min = UserVariables.shoulder_position_min
            self.position_max = UserVariables.shoulder_position_max
            self.velocity_limit = UserVariables.shoulder_velocity_lim


        if UserVariables.disable_controller == True:
            self.Kp_v = 0
            self.Kd_v = 0
            self.Ki_v = 0

        self.record_data = RecordMotorData() #data recording objct for motor

        return None

    def position_position_calculator(self, trajectory, trajectory_index, position):  # torque to control the joint position (independent of link deflection)
        self.position_position = trajectory[trajectory_index]

        n = 2  # number of averages
        if len(position) >= n + 2:  # Calculating velocity (theta dot)
            velocity = 0  # initialise
            for i in range(n):
                dt = 1 / UserVariables.update_frequency
                velocity = velocity + ((position[-i - 1] - position[-i - 3]) / (2 * dt))
                self.velocity = velocity / n
        else:
            self.velocity = 0

        n = 2  # number of averages
        if len(position) >= n + 4:  # Calculating acceleration (theta double dot)
            acceleration = 0
            for i in range(n):
                dt = 1 / UserVariables.update_frequency
                acceleration = acceleration + ((position[-i - 1] - 2 * (position[-i - 2]) + position[-i - 3]) / (dt ** 2))
                self.acceleration = acceleration / n
        else:
            self.acceleration = 0

        self.record_data.velocity(self.velocity)  # record the change in position.
        self.record_data.acceleration(self.acceleration)  # record a new position datapoint
        self.record_data.position(self.position_position)  # record a new position datapoint
        # print(self.record_data.current_data)

        return self.position_position

    def position_velocity_calculator(self, trajectory, trajectory_index, position):  # torque to control the joint position (independent of link deflection)
        # PID CONTROLLER
        position_error = trajectory[trajectory_index] - position[-1]
        dt = 1 / UserVariables.update_frequency

        number_datapoints = len(trajectory)
        if number_datapoints != None:
            # integral of error
            if trajectory_index >= (int(number_datapoints) * 0.75):  # Preventing windup of integral term when there is no motion
                self.e_i = self.e_i + position_error * dt
                lim = self.velocity_limit / self.Ki_j  # this number represents the maximum current the motor can use to compensate for steady state error.
                if self.e_i > lim:
                    self.e_i = lim
                if self.e_i < -lim:
                    e_i = -lim
            else:
                self.e_i = 0

        if trajectory_index == 1:
            self.e_i = 0  # reset the integral error accumulation

        # derivative of error
        self.e_d = (position_error - self.position_error_last) / dt

        # pid control - these values are sent to the motors.These are the motor currents.These can be converted into torques, if required.
        position_velocity = (self.Kp_j * position_error + self.Ki_j * self.e_i + (self.Kd_j * self.e_d))

        # Average smoothing of motor torque
        n = 2  # number of averages
        if len(self.record_data.velocity_data) >= 4:  # Smoothing the motor torque
            # position_torque_sum = position_torque
            # for i in range(n):
            # position_torque_sum = position_torque_sum + (self.record_data.current_data[-i - 1] + self.record_data.current_data[-i - 2])
            # position_torque = position_torque_sum / n
            position_velocity = (position_velocity + self.record_data.velocity_data[-1] + self.record_data.velocity_data[-2] + self.record_data.velocity_data[-3]) / 4

        # clamp the elbow and  currents to the parameter set above.
        if position_velocity > self.velocity_limit:
            position_velocity = self.velocity_limit

        elif position_velocity < -self.velocity_limit:
            position_velocity = -self.velocity_limit
        else:
            position_velocity = position_velocity

        self.position_velocity = position_velocity

        n = 2  # number of averages
        if len(position) >= n + 2:  # Calculating velocity (theta dot)
            velocity = 0  # initialise
            for i in range(n):
                dt = 1 / UserVariables.update_frequency
                velocity = velocity + ((position[-i - 1] - position[-i - 3]) / (2 * dt))
                # velocity = velocity + int(int(position[-i-1]) - int(position[-i-2]))
                self.velocity = velocity / n
        else:
            self.velocity = 0

        n = 2  # number of averages
        if len(position) >= n + 4:  # Calculating acceleration (theta double dot)
            acceleration = 0
            for i in range(n):
                dt = 1 / UserVariables.update_frequency
                acceleration = acceleration + ((position[-i - 1] - 2 * (position[-i - 2]) + position[-i - 3]) / (dt ** 2))
                self.acceleration = acceleration / n
        else:
            self.acceleration = 0

        # Set the last error to the current error.
        self.position_error_last = position_error

        self.record_data.velocity(self.velocity)  # record the change in position.
        self.record_data.acceleration(self.acceleration)  # record a new position datapoint
        #self.record_data.current(self.position_torque)  # record a new position datapoint
        # print(self.record_data.current_data)

        return self.position_velocity

    def position_torque_calculator(self,trajectory,trajectory_index,position): #torque to control the joint position (independent of link deflection)
        #PID CONTROLLER
        position_error = trajectory[trajectory_index] - position[-1]
        dt = 1 / UserVariables.update_frequency

        number_datapoints = len(trajectory)
        if number_datapoints != None:
            #integral of error
            if trajectory_index >= (int(number_datapoints)*0.75): #Preventing windup of integral term when there is no motion
                self.e_i = self.e_i + position_error * dt
                lim = self.current_limit / self.Ki_j #this number represents the maximum current the motor can use to compensate for steady state error.
                if self.e_i > lim:
                    self.e_i = lim
                if self.e_i < -lim:
                    e_i = -lim
            else:
                self.e_i = 0

        if trajectory_index == 1:
            self.e_i = 0 #reset the integral error accumulation

        #derivative of error
        self.e_d = (position_error - self.position_error_last) / dt

        #pid control - these values are sent to the motors.These are the motor currents.These can be converted into torques, if required.
        position_torque = (self.Kp_j * position_error + self.Ki_j * self.e_i + (self.Kd_j * self.e_d))

        #Average smoothing of motor torque
        n = 2  # number of averages
        if len(self.record_data.current_data) >= 4:  # Smoothing the motor torque
            #position_torque_sum = position_torque
            #for i in range(n):
                #position_torque_sum = position_torque_sum + (self.record_data.current_data[-i - 1] + self.record_data.current_data[-i - 2])
            #position_torque = position_torque_sum / n
            position_torque = (position_torque + self.record_data.current_data[-1] + self.record_data.current_data[-2] + self.record_data.current_data[-3])/4


        #clamp the elbow and  currents to the parameter set above.
        if position_torque > self.current_limit:
            position_torque = self.current_limit

        elif position_torque < -self.current_limit:
            position_torque = -self.current_limit
        else:
            position_torque = position_torque

        self.position_torque = position_torque


        n=2 #number of averages
        if len(position) >= n + 2: #Calculating velocity (theta dot)
            velocity = 0 #initialise
            for i in range(n):
                dt = 1 / UserVariables.update_frequency
                velocity = velocity + ((position[-i-1]-position[-i-3])/(2*dt))
                #velocity = velocity + int(int(position[-i-1]) - int(position[-i-2]))
                self.velocity = velocity/n
        else:
            self.velocity = 0

        n = 2  # number of averages
        if len(position) >= n + 4:  #Calculating acceleration (theta double dot)
            acceleration = 0
            for i in range(n):
                dt = 1/UserVariables.update_frequency
                acceleration = acceleration + ((position[-i-1] - 2*(position[-i-2]) + position[-i-3])/(dt ** 2))
                self.acceleration = acceleration/n
        else:
            self.acceleration = 0


        # Set the last error to the current error.
        self.position_error_last = position_error

        self.record_data.velocity(self.velocity)  # record the change in position.
        self.record_data.acceleration(self.acceleration)  # record a new position datapoint
        self.record_data.current(self.position_torque)  # record a new position datapoint
        #print(self.record_data.current_data)


        return self.position_torque


    def deflection_position_calculator(self,deflection): #torque to control the link deflection (independent of the joint position)
        # PID CONTROLLER
        dt = 1 / UserVariables.update_frequency
        if len(deflection) > 2:
            e_d = (deflection[-1] - deflection[-2]) / dt   # derivative of error
            self.deflection_position = (self.Kp_v * deflection[-1] + (self.Kd_v * e_d))
        else:
            self.deflection_position=0

    def deflection_velocity_calculator(self,deflection): #torque to control the link deflection (independent of the joint position)
        # PID CONTROLLER

        dt = 1 / UserVariables.update_frequency
        if len(deflection) > 2:
            e_d = (deflection[-1] - deflection[-2]) / dt   # derivative of error
            self.deflection_velocity = (self.Kp_v * deflection[-1] + (self.Kd_v * e_d))
        else:
            self.deflection_velocity=0

    def deflection_torque_calculator(self,deflection): #torque to control the link deflection (independent of the joint position)
        # PID CONTROLLER

        dt = 1 / UserVariables.update_frequency
        if len(deflection) > 2:
            e_d = (deflection[-1] - deflection[-2]) / dt   # derivative of error
            self.deflection_torque = (self.Kp_v * deflection[-1] + (self.Kd_v * e_d))
        else:
            self.deflection_torque=0


    def joint_position_calculator(self,trajectory, trajectory_index, elbow_motor, elbow_frame_processing):
        position = elbow_motor.record_data.position_data
        deflection_position = elbow_frame_processing.record_data.position_data
        self.position_position_calculator(trajectory, trajectory_index, position)
        self.deflection_position_calculator(deflection_position)

        joint_position = self.position_position - self.deflection_position

        self.disable_processing_flag = self.frame_processing_object.disable_controller_flag

        if self.disable_processing_flag == 1:
            joint_position = self.position_position #don't include the defleciton is the controller is disabled due to the signal being blocked
            #print("Controller disabled")
        else:
            joint_position = self.position_position - self.deflection_position
            #print("Controller enabled")

            #print("vibration controller disabled")
        # clamp the elbow and  currents to the parameter set above.
        if joint_position > self.position_max:
            joint_position = self.position_max

        elif joint_position < -self.position_min:
            joint_position = -self.position_min
        else:
            joint_position = joint_position

        self.joint_position = joint_position

    def joint_velocity_calculator(self,trajectory, trajectory_index, elbow_motor, elbow_frame_processing): #the combined positioning torque and vibration control torques
        position = elbow_motor.record_data.position_data
        deflection_position = elbow_frame_processing.record_data.position_data
        self.position_velocity_calculator(trajectory, trajectory_index, position)
        self.deflection_velocity_calculator(deflection_position)


        joint_velocity =  self.position_velocity - self.deflection_velocity

        self.disable_processing_flag = self.frame_processing_object.disable_controller_flag

        if self.disable_processing_flag == 1:
            joint_velocity = self.position_velocity

        # clamp the elbow and  currents to the parameter set above.
        if joint_velocity > self.velocity_limit:
            joint_velocity = self.velocity_limit

        elif joint_velocity < -self.velocity_limit:
            joint_velocity = -self.velocity_limit
        else:
            joint_velocity = joint_velocity

        self.joint_velocity = joint_velocity

    def joint_torque_calculator(self, trajectory, trajectory_index, elbow_motor, elbow_frame_processing): #the combined positioning torque and vibration control torques
        position = elbow_motor.record_data.position_data
        deflection_position = elbow_frame_processing.record_data.position_data
        self.position_torque_calculator(trajectory, trajectory_index, position)
        self.deflection_torque_calculator(deflection_position)

        self.disable_processing_flag = self.frame_processing_object.disable_controller_flag

        if self.disable_processing_flag == 1:
            joint_torque = self.position_torque
            #print("Controller disabled")
        else:
            joint_torque = self.position_torque - self.deflection_torque
            #print("Controller enabled")

        # clamp the elbow and  currents to the parameter set above.
        if joint_torque > self.current_limit:
            joint_torque = self.current_limit

        elif joint_torque < -self.current_limit:
            joint_torque = -self.current_limit
        else:
            joint_torque = joint_torque

        self.joint_torque = joint_torque



