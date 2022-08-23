#Import Classes========================
import os

from camera_class import *
from image_processing_class import *
from servo_motor_class import *
from plot_class import *
from traj_p2p_class import *
from control_loop_class import *
from robot_graphics_class import *
from performance_metrics_class import *
from save_vectors_class import *
from traj_motion_class import *
from globals import *

#Import libraries=====================
import sys
import numpy as np
import time
import tkinter as tk
import tkinter.ttk as ttk
import threading
import sys



class MainClass(object):
    def __init__(self):
        # Construct dynamixel motor related objects
        self.handler = initialise_Dynamixel()
        self.portHandler = self.handler.portHandler
        self.packetHandler = self.handler.packetHandler
        self.groupread_num = self.handler.initialise_bulk_read()  # only one of these variables exists
        self.groupwrite_num = self.handler.initialise_bulk_write()  # only one of these variables exists

        # Construct elbow and shoulder motor objects
        self.elbow_motor = motor(self.portHandler, self.packetHandler, self.groupread_num, self.groupwrite_num, "Elbow")
        self.shoulder_motor = motor(self.portHandler, self.packetHandler, self.groupread_num, self.groupwrite_num, "Shoulder")

        # Reboot the elbow and shoulder motors (rebooting resets any errors)
        self.elbow_motor.reboot_motor()
        self.shoulder_motor.reboot_motor()
        time.sleep(0.1)

        # Set drive mode of the motors (torque, velcoticy or position mode, determined in uservariabled class)
        self.elbow_motor.set_mode()
        self.shoulder_motor.set_mode()

        # Enable the motors (set the torque to 'on')
        self.elbow_motor.enable_motor()
        self.shoulder_motor.enable_motor()

        # add the elbow and shoulder bulkread parameters (only needs to be done once)
        self.elbow_motor.add_read_param()
        self.shoulder_motor.add_read_param()
        SendRecieveBulk(self.groupread_num, self.groupwrite_num).transmit_read()
        SendRecieveBulk(self.groupread_num, self.groupwrite_num).clear_write_param()

        # Construct the elbow and shoulder camera objects
        self.elbow_camera = Camera("Elbow")
        self.shoulder_camera = Camera("Shoulder")
        time.sleep(4)  # allow time for thread to start
        self.elbow_frame_processing = ImageProcessing("Elbow", self.elbow_camera)
        self.shoulder_frame_processing = ImageProcessing("Shoulder", self.shoulder_camera)
        time.sleep(1)  # allow time for thread to start

        # generate simple joint space trajectories
        if UserVariables.point_to_point == True:
            self.elbow_trajectory_generator = point_to_point()
            self.shoulder_trajectory_generator = point_to_point()
            self.elbow_traj = self.elbow_trajectory_generator.generate_trajectory_elbow(UserVariables.elbow_start, UserVariables.elbow_end, UserVariables.timespan, UserVariables.timespan_home,
                                                                                        UserVariables.update_frequency)
            self.shoulder_traj = self.elbow_trajectory_generator.generate_trajectory_shoulder(UserVariables.shoulder_start, UserVariables.shoulder_end, UserVariables.timespan,
                                                                                              UserVariables.timespan_home,
                                                                                              UserVariables.update_frequency)
        elif UserVariables.point_to_point == False:
            self.elbow_trajectory_generator = MotionTraj()
            self.shoulder_trajectory_generator = MotionTraj()
            self.elbow_traj = self.elbow_trajectory_generator.elbow()
            self.shoulder_traj = self.shoulder_trajectory_generator.shoulder()
            print(self.elbow_traj)
        else:
            quit("User Variable Error. Check if Point to Point TRUE/FALSE is defined correctly in user variables class.")

        # construct control loop objects
        self.elbow_positioning_control = control_system("Elbow", self.elbow_frame_processing)  # passing in the disable controller flag
        self.shoulder_positioning_control = control_system("Shoulder", self.shoulder_frame_processing)

        # run the robot graphics on screen in real time to see where robot should be.
        self.robot_graphics = Graphics(0.15, 1)  # ideal robot opacity, real robot opacity

        # start the gamecontroller object
        # joystick = gamecontroller_class.XboxController()
        self.run()
        return None

    def run(self):
        print("Running Main...")
        breakloop = False
        finished_flag = 0
        globals.cycle_start_flag = 0  # reset cycle start flag to avoid unintentional activation.
        while True:
            #if the mode buttons have been moved, then reset the motor modes
            print(globals.controller_checkbox_flag)
            print(globals.mode_changed_flag or globals.controller_checkbox_flag)
            if (globals.mode_changed_flag or globals.controller_checkbox_flag) == 1:
                print("Entered!")
                globals.mode_changed_flag = 0 #reset the flag.
                globals.controller_checkbox_flag = 0

                if globals.mode == "position":
                    UserVariables.motor_method = UserVariables.motor_methods[0] #position mode
                    print(UserVariables.disable_controller)
                    self.elbow_positioning_control.__init__("Elbow", self.elbow_frame_processing) #reinitialising the control loop with the new gains from the mode switching
                    self.shoulder_positioning_control.__init__("Shoulder", self.shoulder_frame_processing)
                    # Reboot the elbow and shoulder motors (rebooting resets any errors)
                    self.elbow_motor.reboot_motor()
                    self.shoulder_motor.reboot_motor()
                    time.sleep(0.1)

                    # Set drive mode of the motors (torque, velcoticy or position mode, determined in uservariabled class)
                    self.elbow_motor.set_mode()
                    self.shoulder_motor.set_mode()

                    # Enable the motors (set the torque to 'on')
                    self.elbow_motor.enable_motor()
                    self.shoulder_motor.enable_motor()

                    # add the elbow and shoulder bulkread parameters (only needs to be done once)
                    # self.elbow_motor.add_read_param()
                    # self.shoulder_motor.add_read_param()
                    # SendRecieveBulk(self.groupread_num, self.groupwrite_num).transmit_read()
                    SendRecieveBulk(self.groupread_num, self.groupwrite_num).clear_write_param()

                if globals.mode == "velocity":
                    UserVariables.motor_method = UserVariables.motor_methods[1] #velocity mode
                    self.elbow_positioning_control.__init__("Elbow", self.elbow_frame_processing) #reinitialising the control loop with the new gains from the mode switching
                    self.shoulder_positioning_control.__init__("Shoulder", self.shoulder_frame_processing)
                    # Reboot the elbow and shoulder motors (rebooting resets any errors)
                    self.elbow_motor.reboot_motor()
                    self.shoulder_motor.reboot_motor()
                    time.sleep(0.1)

                    # Set drive mode of the motors (torque, velcoticy or position mode, determined in uservariabled class)
                    self.elbow_motor.set_mode()
                    self.shoulder_motor.set_mode()

                    # Enable the motors (set the torque to 'on')
                    self.elbow_motor.enable_motor()
                    self.shoulder_motor.enable_motor()

                    # add the elbow and shoulder bulkread parameters (only needs to be done once)
                    # self.elbow_motor.add_read_param()
                    # self.shoulder_motor.add_read_param()
                    # SendRecieveBulk(self.groupread_num, self.groupwrite_num).transmit_read()
                    SendRecieveBulk(self.groupread_num, self.groupwrite_num).clear_write_param()

                if globals.mode == "torque":
                    UserVariables.motor_method = UserVariables.motor_methods[2] #torque mode
                    self.elbow_positioning_control.__init__("Elbow", self.elbow_frame_processing) #reinitialising the control loop with the new gains from the mode switching
                    self.shoulder_positioning_control.__init__("Shoulder", self.shoulder_frame_processing)
                    # Reboot the elbow and shoulder motors (rebooting resets any errors)
                    self.elbow_motor.reboot_motor()
                    self.shoulder_motor.reboot_motor()
                    time.sleep(0.1)

                    # Set drive mode of the motors (torque, velcoticy or position mode, determined in uservariabled class)
                    self.elbow_motor.set_mode()
                    self.shoulder_motor.set_mode()

                    # Enable the motors (set the torque to 'on')
                    self.elbow_motor.enable_motor()
                    self.shoulder_motor.enable_motor()

                    # add the elbow and shoulder bulkread parameters (only needs to be done once)
                    # self.elbow_motor.add_read_param()
                    # self.shoulder_motor.add_read_param()
                    # SendRecieveBulk(self.groupread_num, self.groupwrite_num).transmit_read()
                    SendRecieveBulk(self.groupread_num, self.groupwrite_num).clear_write_param()



            print("Press CYCLE START to run.")
            # if estop has been reset and cycle start is on, then run
            if globals.cycle_start_flag == 1 and globals.reset_flag == 0 and globals.estop_flag == 0:  # loop forever until the cycle start signal is given by the user. This will initiate the trajectory to run.
                index = 0
                self.elbow_motor.enable_motor()  # enable the motors
                self.shoulder_motor.enable_motor()
                # time.sleep(0.1)

                while index < self.elbow_trajectory_generator.datapoints:
                    # robot_gui.status_display(message="Running")
                    globals.robot_gui.STATUSMESSAGE.configure(text='''Running''')
                    globals.robot_gui.STATUSMESSAGE.configure(foreground="#00ff00")
                    if globals.estop_flag == 1:  # If estop is pressed, break out
                        globals.cycle_start_flag = 0
                        globals.feedhold_flag = 0
                        globals.reset_flag = 0
                        self.elbow_motor.disable_motor()  # disable the motors
                        self.shoulder_motor.disable_motor()
                        globals.robot_gui.TProgressbar1.configure(value=0)  # update the progress bar on the gui
                        globals.robot_gui.STATUSMESSAGE.configure(text='''Emergency Stop!\nWaiting for RESET''')
                        globals.robot_gui.STATUSMESSAGE.configure(foreground="#ff0000")
                        finished_flag = 1
                        # time.sleep(0.1)
                        # breakloop = True#Causes program to crash
                        break

                    elif globals.reset_flag == 1:  # If reset is pressed, break out but keep motors active
                        globals.cycle_start_flag = 0
                        globals.feedhold_flag = 0
                        globals.robot_gui.TProgressbar1.configure(value=0)  # update the progress bar on the gui
                        # robot_gui.STATUSMESSAGE.configure(text='''Ready''')
                        # robot_gui.STATUSMESSAGE.configure(foreground="#00ff00")
                        # time.sleep(0.1)
                        # globals.reset_flag = 0
                        # breakloop = True
                        finished_flag = 1
                        break

                    elif globals.feedhold_flag == 1:  # If feedhold is pressed, stop the motion until cycle start is pressed
                        globals.cycle_start_flag = 0
                        globals.robot_gui.STATUSMESSAGE.configure(text='''Feed Hold''')
                        globals.robot_gui.STATUSMESSAGE.configure(foreground="#ff8040")
                        while globals.feedhold_flag == 1:
                            if globals.estop_flag == 1 or globals.reset_flag == 1:
                                break

                            if globals.cycle_start_flag == 1:
                                globals.feedhold_flag = 0  # reset the feedhold flag
                                break

                    # Quick shutdown without waiting for motion to finish
                    if globals.shutdown_flag == 1:
                        break

                    SendRecieveBulk(self.groupread_num, self.groupwrite_num).transmit_read()  # Request for new data

                    self.elbow_motor.read_motor_encoder()  # read encoder
                    self.shoulder_motor.read_motor_encoder()  # read encoder

                    self.elbow_frame_processing.record_deflection()  # record the deflection to the vector
                    self.shoulder_frame_processing.record_deflection()  # record the deflection to the vector

                    if UserVariables.motor_method == "torque":
                        self.elbow_positioning_control.joint_torque_calculator(self.elbow_traj, index, self.elbow_motor, self.elbow_frame_processing)  # calculate new motor torques
                        self.shoulder_positioning_control.joint_torque_calculator(self.shoulder_traj, index, self.shoulder_motor,
                                                                                  self.shoulder_frame_processing)  # calculate new motor torques. Inputs of position are vectors of recorded past positions.

                        self.elbow_motor.move_torque(int(self.elbow_positioning_control.joint_torque))
                        self.shoulder_motor.move_torque(int(self.shoulder_positioning_control.joint_torque))

                    elif UserVariables.motor_method == "position":
                        self.elbow_positioning_control.joint_position_calculator(self.elbow_traj, index, self.elbow_motor, self.elbow_frame_processing)  # calculate new motor torques
                        self.shoulder_positioning_control.joint_position_calculator(self.shoulder_traj, index, self.shoulder_motor,
                                                                                    self.shoulder_frame_processing)  # calculate new motor torques. Inputs of position are vectors of recorded past positions.

                        self.elbow_motor.move_position(int(self.elbow_positioning_control.joint_position))
                        self.shoulder_motor.move_position(int(self.shoulder_positioning_control.joint_position))

                    elif UserVariables.motor_method == "velocity":
                        self.elbow_positioning_control.joint_velocity_calculator(self.elbow_traj, index, self.elbow_motor, self.elbow_frame_processing)  # calculate new motor torques
                        self.shoulder_positioning_control.joint_velocity_calculator(self.shoulder_traj, index, self.shoulder_motor,
                                                                                    self.shoulder_frame_processing)  # calculate new motor torques. Inputs of position are vectors of recorded past positions.

                        self.elbow_motor.move_velocity(int(self.elbow_positioning_control.joint_velocity))
                        self.shoulder_motor.move_velocity(int(self.shoulder_positioning_control.joint_velocity))

                    SendRecieveBulk(self.groupread_num, self.groupwrite_num).transmit_write()  # TxRx write new currents
                    SendRecieveBulk(self.groupread_num, self.groupwrite_num).clear_write_param()  # Clear the param

                    self.robot_graphics.elbowideal = np.radians(self.elbow_traj[index] + 180)
                    self.robot_graphics.shoulderideal = np.radians(self.shoulder_traj[index] - 180)

                    self.robot_graphics.elbowreal = np.radians(self.elbow_motor.record_data.position_data[-1] + 180)
                    self.robot_graphics.shoulderreal = np.radians(self.shoulder_motor.record_data.position_data[-1] - 180)

                    percent_complete = index / len(self.elbow_traj) * 100
                    globals.robot_gui.TProgressbar1.configure(value=percent_complete)  # update the progress bar on the gui

                    # cv2.imshow('ELBOWraw', np.asarray(elbow_camera.frame))
                    # #
                    # cv2.imshow('ELBOW', np.asarray(elbow_frame_processing.frame))
                    # cv2.imshow('SHOULDER', np.asarray(shoulder_frame_processing.frame))
                    # cv2.waitKey(1)

                    time.sleep(0.0015)  # 0.0015
                    # time.sleep(0.01)
                    # time.sleep(1/UserVariables.update_frequency)
                    index = index + 1

            # Disable the motors
            self.elbow_motor.disable_motor()
            self.shoulder_motor.disable_motor()
            globals.cycle_start_flag = 0  # reset cycle start flag.

            while True:
                if finished_flag == 0 and globals.estop_flag == 0:  # if the motion finished and etop is off
                    globals.robot_gui.STATUSMESSAGE.configure(text='''Ready''')
                    globals.robot_gui.STATUSMESSAGE.configure(foreground="#00ff00")

                # cycle start button monitoring
                if globals.cycle_start_flag == 1:
                    globals.reset_flag = 0
                    time.sleep(0.1)
                    break

                # if globals.reset_flag == 1:
                #     robot_gui.STATUSMESSAGE.configure(text='''Ready''')
                #     robot_gui.STATUSMESSAGE.configure(foreground="#00ff00")

                # Shutdown flag monitoring
                if globals.shutdown_flag == 1:
                    breakloop = True
                    break

                if globals.estop_flag == 1:  # If estop or reset is pressed, set the progress bar to zero. This loop is engaged when the motion is completed.
                    globals.robot_gui.STATUSMESSAGE.configure(text='''Emergency Stop!\nWaiting for RESET''')
                    globals.robot_gui.STATUSMESSAGE.configure(foreground="#ff0000")
                    globals.robot_gui.TProgressbar1.configure(value=0)  # update the progress bar on the gui
                    globals.reset_flag = 0

                if globals.reset_flag == 1:
                    globals.robot_gui.TProgressbar1.configure(value=0)  # update the progress bar on the gui
                    globals.estop_flag = 0
                    finished_flag = 0

                    # time.sleep(0.1)

            if breakloop == True:
                print("Quitting!")
                break  # break the main loop.
            print("running loop")

        #if shutting down
        self.close_port()

        self.write_variables()
        self.display_graphs()
        self.close_GUI() #The main thread is destroyed when the gui is closed.


    def close_port(self):
        # Close serial port
        self.handler.close_port()

    def write_variables(self):
        write_csv(self.elbow_motor, self.shoulder_motor, self.elbow_frame_processing, self.shoulder_frame_processing, self.elbow_traj,
                  self.shoulder_traj)  # write the recorded various data to CSV files for MATLAB to use in the system identification tool.

    def display_graphs(self):
        #print("Making graphs...")
        overshoot_elbow = PerformanceMetrics(self.elbow_motor, self.elbow_frame_processing, self.elbow_traj).overshoot_percentage()  # calculate the overshoot percentage
        overshoot_shoulder = PerformanceMetrics(self.shoulder_motor, self.shoulder_frame_processing, self.shoulder_traj).overshoot_percentage()

        print("Elbow Maximum Overshoot during run", "{x:.2f}".format(x=overshoot_elbow * 100), "%")
        print("Shoulder Maximum Overshoot during run", "{x:.2f}".format(x=overshoot_shoulder * 100), "%")

        plots = PlotData()
        plots.joint(self.elbow_motor, self.elbow_positioning_control, self.elbow_traj, "Elbow")  # plot the joint data
        plots.joint(self.shoulder_motor, self.shoulder_positioning_control, self.shoulder_traj, "Shoulder")

        plots.link(self.elbow_frame_processing, self.elbow_positioning_control, self.elbow_traj, "Lower Arm")  # plot the link data
        plots.link(self.shoulder_frame_processing, self.shoulder_positioning_control, self.shoulder_traj, "Upper Arm")

        plots.true_position(self.elbow_motor, self.elbow_positioning_control, self.elbow_frame_processing, self.elbow_traj, "Lower Arm")
        plots.true_position(self.shoulder_motor, self.shoulder_positioning_control, self.shoulder_frame_processing, self.shoulder_traj, "Upper Arm")

    def close_GUI(self):
        globals.root.destroy()  # close the GUI