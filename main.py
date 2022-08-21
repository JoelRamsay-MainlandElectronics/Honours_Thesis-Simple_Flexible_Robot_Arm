#Import Classes========================
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

#Import libraries=====================
import sys, os
import numpy as np
import time
from time import perf_counter

print("Python version")
print (sys.version)
#print("Version info.")
#print (sys.version_info)
#print(os.path.dirname(sys.executable))


#========================================


#Construct dynamixel motor related objects
handler = initialise_Dynamixel()
portHandler = handler.portHandler
packetHandler = handler.packetHandler
groupread_num = handler.initialise_bulk_read() #only one of these variables exists
groupwrite_num = handler.initialise_bulk_write() #only one of these variables exists

#Construct elbow and shoulder motor objects
elbow_motor = motor(portHandler,packetHandler, groupread_num, groupwrite_num, "Elbow")
shoulder_motor = motor(portHandler,packetHandler, groupread_num, groupwrite_num, "Shoulder")

#Reboot the elbow and shoulder motors (rebooting resets any errors)
elbow_motor.reboot_motor()
shoulder_motor.reboot_motor()
time.sleep(0.1)

#Set drive mode of the motors (torque, velcoticy or position mode, determined in uservariabled class)
elbow_motor.set_mode()
shoulder_motor.set_mode()

#Enable the motors (set the torque to 'on')
elbow_motor.enable_motor()
shoulder_motor.enable_motor()

#add the elbow and shoulder bulkread parameters (only needs to be done once)
elbow_motor.add_read_param()
shoulder_motor.add_read_param()
SendRecieveBulk(groupread_num,groupwrite_num).transmit_read()
SendRecieveBulk(groupread_num,groupwrite_num).clear_write_param()

#Construct the elbow and shoulder camera objects
elbow_camera = Camera("Elbow")
shoulder_camera = Camera("Shoulder")
time.sleep(4)   #allow time for thread to start
elbow_frame_processing = ImageProcessing("Elbow", elbow_camera)
shoulder_frame_processing = ImageProcessing("Shoulder", shoulder_camera)
time.sleep(1)   #allow time for thread to start

#generate simple joint space trajectories
if UserVariables.point_to_point == True:
    elbow_trajectory_generator = point_to_point()
    shoulder_trajectory_generator = point_to_point()
    elbow_traj = elbow_trajectory_generator.generate_trajectory_elbow(UserVariables.elbow_start, UserVariables.elbow_end, UserVariables.timespan, UserVariables.timespan_home, UserVariables.update_frequency)
    shoulder_traj = elbow_trajectory_generator.generate_trajectory_shoulder(UserVariables.shoulder_start, UserVariables.shoulder_end, UserVariables.timespan, UserVariables.timespan_home, UserVariables.update_frequency)
elif UserVariables.point_to_point == False:
    elbow_trajectory_generator = MotionTraj()
    shoulder_trajectory_generator = MotionTraj()
    elbow_traj = elbow_trajectory_generator.elbow()
    shoulder_traj = shoulder_trajectory_generator.shoulder()
    print(elbow_traj)
else:
    quit("User Variable Error. Check if Point to Point TRUE/FALSE is defined correctly in user variables class.")

#construct control loop objects
elbow_positioning_control = control_system("Elbow", elbow_frame_processing) #passing in the disable controller flag
shoulder_positioning_control = control_system("Shoulder", shoulder_frame_processing)

#run the robot graphics on screen in real time to see where robot should be.
robot_graphics = Graphics(0.15,1) #ideal robot opacity, real robot opacity

#start the gamecontroller object
#joystick = gamecontroller_class.XboxController()

print("Running Main...")
breakloop = False
while True:
    index = 0
    elbow_motor.enable_motor()#enable the motors
    shoulder_motor.enable_motor()
    time.sleep(0.1)

    while index < elbow_trajectory_generator.datapoints:
        SendRecieveBulk(groupread_num, groupwrite_num).transmit_read()  # Request for new data

        elbow_motor.read_motor_encoder() #read encoder
        shoulder_motor.read_motor_encoder() #read encoder

        elbow_frame_processing.record_deflection()  # record the deflection to the vector
        shoulder_frame_processing.record_deflection() #record the deflection to the vector

        if UserVariables.motor_method == "torque":
            elbow_positioning_control.joint_torque_calculator(elbow_traj, index, elbow_motor, elbow_frame_processing)  # calculate new motor torques
            shoulder_positioning_control.joint_torque_calculator(shoulder_traj, index, shoulder_motor, shoulder_frame_processing)  # calculate new motor torques. Inputs of position are vectors of recorded past positions.

            elbow_motor.move_torque(int(elbow_positioning_control.joint_torque))
            shoulder_motor.move_torque(int(shoulder_positioning_control.joint_torque))

        elif UserVariables.motor_method == "position":
            elbow_positioning_control.joint_position_calculator(elbow_traj, index, elbow_motor, elbow_frame_processing)  # calculate new motor torques
            shoulder_positioning_control.joint_position_calculator(shoulder_traj, index, shoulder_motor, shoulder_frame_processing)  # calculate new motor torques. Inputs of position are vectors of recorded past positions.

            elbow_motor.move_position(int(elbow_positioning_control.joint_position))
            shoulder_motor.move_position(int(shoulder_positioning_control.joint_position))

        elif UserVariables.motor_method == "velocity":
            elbow_positioning_control.joint_velocity_calculator(elbow_traj, index, elbow_motor, elbow_frame_processing)  # calculate new motor torques
            shoulder_positioning_control.joint_velocity_calculator(shoulder_traj, index, shoulder_motor, shoulder_frame_processing)  # calculate new motor torques. Inputs of position are vectors of recorded past positions.

            elbow_motor.move_velocity(int(elbow_positioning_control.joint_velocity))
            shoulder_motor.move_velocity(int(shoulder_positioning_control.joint_velocity))

        SendRecieveBulk(groupread_num, groupwrite_num).transmit_write() #TxRx write new currents
        SendRecieveBulk(groupread_num, groupwrite_num).clear_write_param() #Clear the param

        robot_graphics.elbowideal = np.radians(elbow_traj[index]+180)
        robot_graphics.shoulderideal = np.radians(shoulder_traj[index]-180)

        robot_graphics.elbowreal = np.radians(elbow_motor.record_data.position_data[-1] + 180)
        robot_graphics.shoulderreal = np.radians(shoulder_motor.record_data.position_data[-1] - 180)

        # cv2.imshow('ELBOWraw', np.asarray(elbow_camera.frame))
        # #
        # cv2.imshow('ELBOW', np.asarray(elbow_frame_processing.frame))
        # cv2.imshow('SHOULDER', np.asarray(shoulder_frame_processing.frame))
        # cv2.waitKey(1)

        time.sleep(0.0015)#0.0015
        #time.sleep(0.01)
        #time.sleep(1/UserVariables.update_frequency)
        index = index + 1

    # Disable the motors
    elbow_motor.disable_motor()
    shoulder_motor.disable_motor()

    print("Press 'e' to exit. Press ENTER to run again:")
    for line in sys.stdin:
        if 'e' == line.rstrip():
            print(f'Input : {line}')
            breakloop = True #quit when user types 'e'.
            break
        elif '\n' == line: #Run again, when user types 'enter' key.
            print(f'Input : {line}')
            print("Running again...")
            break
        else:
            print(f'Input : {line} Bad Input!') #else print the bad input.

    if breakloop == True:
        print("Quitting!")
        break  #break the main loop.
    print("running loop")

#Close serial port
handler.close_port()

write_csv(elbow_motor, shoulder_motor, elbow_frame_processing, shoulder_frame_processing, elbow_traj, shoulder_traj) #write the recorded various data to CSV files for MATLAB to use in the system identification tool.

overshoot_elbow = PerformanceMetrics(elbow_motor, elbow_frame_processing, elbow_traj).overshoot_percentage() #calculate the overshoot percentage
overshoot_shoulder = PerformanceMetrics(shoulder_motor, shoulder_frame_processing, shoulder_traj).overshoot_percentage()

print("Elbow Maximum Overshoot during run","{x:.2f}".format(x=overshoot_elbow*100),"%")
print("Shoulder Maximum Overshoot during run","{x:.2f}".format(x=overshoot_shoulder*100),"%")

plots = PlotData()
plots.joint(elbow_motor, elbow_positioning_control, elbow_traj, "Elbow")  #plot the joint data
plots.joint(shoulder_motor, shoulder_positioning_control, shoulder_traj, "Shoulder")

plots.link(elbow_frame_processing, elbow_positioning_control, elbow_traj, "Lower Arm")  #plot the link data
plots.link(shoulder_frame_processing, shoulder_positioning_control, shoulder_traj,"Upper Arm")

plots.true_position(elbow_motor, elbow_positioning_control, elbow_frame_processing, elbow_traj, "Lower Arm")
plots.true_position(shoulder_motor, shoulder_positioning_control, shoulder_frame_processing, shoulder_traj, "Upper Arm")
