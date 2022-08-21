#import gamecontroller_class
import performance_metrics_class
import traj_motion_class
from camera_class import *
from image_processing_class import *
from servo_motor_class import *
from user_variables import *
from plot_class import *
from numpy import genfromtxt
from traj_p2p_class import *
from control_loop_class import *
from robot_graphics_class import *
from traj_motion_class import *
from performance_metrics_class import *
import sys
from msvcrt import getch,kbhit
#import depthai as dai
import numpy as np
import time

from time import perf_counter
import threading

# import sys
# print("Python version")
# print (sys.version)
# print("Version info.")
# print (sys.version_info)
# import sys, os
# os.path.dirname(sys.executable)

# axs = plt.subplot(141)
# axs = plt.subplot(142)
# axs.set_xlim([0,5])
# plt.show()

#Determine initial elbow and shoulder link deflections (automatic home offset). This is the first measurement that comes in.

#Construct motor initialisation object
handler = initialise_Dynamixel()
portHandler = handler.portHandler
packetHandler = handler.packetHandler
groupread_num = handler.initialise_bulk_read() #only one of these variables exists
groupwrite_num = handler.initialise_bulk_write() #only one of these variables exists

#Construct elbow motor object
elbow_motor = motor(portHandler,packetHandler, groupread_num, groupwrite_num, "Elbow")
shoulder_motor = motor(portHandler,packetHandler, groupread_num, groupwrite_num, "Shoulder")

#Reboot the motors
elbow_motor.reboot_motor()
shoulder_motor.reboot_motor()
time.sleep(0.1)

#Set mode of the motors
elbow_motor.set_mode()
shoulder_motor.set_mode()

#Enable the motors
elbow_motor.enable_motor()
shoulder_motor.enable_motor()

#initialise BulkRead and BulkWrite
# if UserVariables.motor_method == "torque":
#     elbow_motor.add_read_param()
#     shoulder_motor.add_read_param()
# elif UserVariables.motor_method == "velocity":
#     elbow_motor.add_read_param()
#     shoulder_motor.add_read_param()
elbow_motor.add_read_param()
shoulder_motor.add_read_param()

SendRecieveBulk(groupread_num,groupwrite_num).transmit_read()
SendRecieveBulk(groupread_num,groupwrite_num).clear_write_param()

#Construct the camera objects
elbow_camera = Camera("Elbow", UserVariables.camera_exposure, UserVariables.camera_ISO)#20,100
shoulder_camera = Camera("Shoulder", UserVariables.camera_exposure, UserVariables.camera_ISO)
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
    quit("User Variable Error. Point to Point.")

#construct control loop objects
elbow_positioning_control = control_system("Elbow", elbow_frame_processing) #passing in the disable controller flag
shoulder_positioning_control = control_system("Shoulder", shoulder_frame_processing)

#run the robot graphics on screen in real time to see where robot should be.
robot_graphics = Graphics(0.15,1) #ideal, real
#robot_graphics_actual = Graphics(1)

#start the gamecontroller object
#joystick = gamecontroller_class.XboxController()

print("Running Main...")
breakloop = False
while True:
    index = 0
    #enable the motors
    elbow_motor.enable_motor()
    shoulder_motor.enable_motor()
    time.sleep(0.1)

    while index < elbow_trajectory_generator.datapoints:
        #print("Elbow: ", elbow_motor.read_motor_encoder(), "Shoulder: ", shoulder_motor.read_motor_encoder())
        #print("Elbow: ", elbow_motor.read_motor_encoder())

        SendRecieveBulk(groupread_num, groupwrite_num).transmit_read()  # Request for new data

        elbow_motor.read_motor_encoder() #read encoder
        shoulder_motor.read_motor_encoder() #read encoder

        elbow_frame_processing.record_deflection()  # record the deflection to the vector
        shoulder_frame_processing.record_deflection() #record the deflection to the vector

        if UserVariables.motor_method == "torque":
            elbow_positioning_control.joint_torque_calculator(elbow_traj, index, elbow_motor.record_data.position_data, elbow_frame_processing.record_data.position_data)  # calculate new motor torques
            shoulder_positioning_control.joint_torque_calculator(shoulder_traj, index, shoulder_motor.record_data.position_data, shoulder_frame_processing.record_data.position_data)  # calculate new motor torques. Inputs of position are vectors of recorded past positions.

            elbow_motor.move_torque(int(elbow_positioning_control.joint_torque))
            shoulder_motor.move_torque(int(shoulder_positioning_control.joint_torque))

        elif UserVariables.motor_method == "position":
            elbow_positioning_control.joint_position_calculator(elbow_traj, index, elbow_motor.record_data.position_data, elbow_frame_processing.record_data.position_data)  # calculate new motor torques
            shoulder_positioning_control.joint_position_calculator(shoulder_traj, index, shoulder_motor.record_data.position_data,  shoulder_frame_processing.record_data.position_data)  # calculate new motor torques. Inputs of position are vectors of recorded past positions.

            elbow_motor.move_position(int(elbow_positioning_control.joint_position))
            shoulder_motor.move_position(int(shoulder_positioning_control.joint_position))

        elif UserVariables.motor_method == "velocity":
            elbow_positioning_control.joint_velocity_calculator(elbow_traj, index, elbow_motor.record_data.position_data, elbow_frame_processing.record_data.position_data)  # calculate new motor torques
            shoulder_positioning_control.joint_velocity_calculator(shoulder_traj, index, shoulder_motor.record_data.position_data,  shoulder_frame_processing.record_data.position_data)  # calculate new motor torques. Inputs of position are vectors of recorded past positions.

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




    #print("Exit")

    #input_char = input("Press ENTER to run again.")

    #if input_char == '\x0D':
    #    break




# #generate home trajectory
# elbow_trajectory_generator = point_to_point()
# shoulder_trajectory_generator = point_to_point()
# elbow_traj = elbow_trajectory_generator.generate_trajectory_elbow(UserVariables.elbow_home, UserVariables.elbow_home, UserVariables.timespan_home, UserVariables.update_frequency)
# shoulder_traj = elbow_trajectory_generator.generate_trajectory_shoulder(UserVariables.shoulder_home, UserVariables.shoulder_home, UserVariables.timespan_home, UserVariables.update_frequency)


# #enable the motors
# elbow_motor.enable_motor()
# shoulder_motor.enable_motor()

#Disable the motors
# elbow_motor.disable_motor()
# shoulder_motor.disable_motor()

ElbowTruePosition = list(map(add, elbow_motor.record_data.position_data, elbow_frame_processing.record_data.position_data))
ShoulderTruePosition = list(map(add, shoulder_motor.record_data.position_data, shoulder_frame_processing.record_data.position_data))

elbow_metrics = PerformanceMetrics(ElbowTruePosition, elbow_traj)
shoulder_metrics = PerformanceMetrics(ShoulderTruePosition, shoulder_traj)

overshoot_elbow = elbow_metrics.overshoot_percentage()
overshoot_shoulder = shoulder_metrics.overshoot_percentage()



print("Elbow Maximum Overshoot during run","{x:.2f}".format(x=overshoot_elbow*100),"%")



if UserVariables.disable_controller == True:
    np.savetxt("ElbowInputSignalControllerDisabled.csv", np.asarray(elbow_traj), delimiter=",")
    np.savetxt("ShoulderInputSignalControllerDisabled.csv", np.asarray(shoulder_traj), delimiter=",")
    np.savetxt("ElbowTruePositionRealControllerDisabled.csv", np.asarray(ElbowTruePosition), delimiter=",")
    np.savetxt("ShoulderTruePositionRealControllerDisabled.csv", np.asarray(ShoulderTruePosition), delimiter=",")

if UserVariables.disable_controller == False:
    np.savetxt("ElbowInputSignalControllerEnabled.csv", np.asarray(elbow_traj), delimiter=",")
    np.savetxt("ShoulderInputSignalControllerEnabled.csv", np.asarray(shoulder_traj), delimiter=",")
    np.savetxt("ElbowTruePositionRealControllerEnabled.csv", np.asarray(ElbowTruePosition), delimiter=",")
    np.savetxt("ShoulderTruePositionRealControllerEnabled.csv", np.asarray(ShoulderTruePosition), delimiter=",")

plots = PlotData()
plots.joint(elbow_motor.record_data.position_data,  elbow_positioning_control.record_data.velocity_data, elbow_positioning_control.record_data.acceleration_data,    elbow_positioning_control.record_data.current_data, elbow_traj,  "Elbow")  #plot the joint data
plots.joint(shoulder_motor.record_data.position_data,   shoulder_positioning_control.record_data.velocity_data, shoulder_positioning_control.record_data.acceleration_data, shoulder_positioning_control.record_data.current_data, shoulder_traj, "Shoulder")

plots.link(elbow_frame_processing.record_data.position_data,    elbow_frame_processing.record_data.velocity_data,   elbow_frame_processing.record_data.acceleration_data, elbow_positioning_control.Kp_v,  elbow_positioning_control.Ki_v,  elbow_positioning_control.Kd_v,  elbow_traj,     "Lower Arm")  #plot the link data
plots.link(shoulder_frame_processing.record_data.position_data, shoulder_frame_processing.record_data.velocity_data,    shoulder_frame_processing.record_data.acceleration_data,    elbow_positioning_control.Kp_v,  elbow_positioning_control.Ki_v,  elbow_positioning_control.Kd_v,   shoulder_traj,  "Upper Arm")

plots.true_position(elbow_motor, elbow_positioning_control, elbow_frame_processing, elbow_positioning_control.Kp_v,  elbow_positioning_control.Ki_v,  elbow_positioning_control.Kd_v,   elbow_traj,  "Lower Arm")
plots.true_position(shoulder_motor, shoulder_positioning_control, shoulder_frame_processing, shoulder_positioning_control.Kp_v,  shoulder_positioning_control.Ki_v,  shoulder_positioning_control.Kd_v, shoulder_traj,  "Upper Arm")


# time1 = time.time()
# index = 0
# while time.time() < time1+2:
#
#     elbow_positioning_control.position_torque(elbow_traj, index, elbow_trajectory_generator.datapoints, elbow_motor.record_data.position_data)  # calculate new motor torques
#     shoulder_positioning_control.position_torque(shoulder_traj, index, shoulder_trajectory_generator.datapoints, shoulder_motor.record_data.position_data)  # calculate new motor torques
#     elbow_motor.move(int(elbow_positioning_control.motor_torque))
#     shoulder_motor.move(int(shoulder_positioning_control.motor_torque))

    #shoulder_motor.move(100)
    #print("Elbow: ", elbow_motor.read_motor_encoder(), "Shoulder: ", shoulder_motor.read_motor_encoder())

    # elbow_motor.read_motor_encoder() #read encoder
    # shoulder_motor.read_motor_encoder() #read encoder
    # shoulder_frame_processing.record_deflection() #record the deflection to the vector
    # elbow_motor.move(-10)
    # #shoulder_motor.move(-100)
    # #print("Elbow: ", elbow_motor.read_motor_encoder(), "Shoulder: ", shoulder_motor.read_motor_encoder())
    # time.sleep(0.1)








#Close serial port
handler.close_port()


#     cv2.imshow('stream1', np.asarray(Elbow_frame_processing.frame))
#     cv2.imshow('stream2', np.asarray(Shoulder_frame_processing.frame))
#     cv2.waitKey(1)


# while True:



# print(Elbow_camera.frame)
# time.sleep(3)
# print('Checkpoint')
# time.sleep(2)
# print('Bye')

# Set up the detector with default parameters.


# detector = cv2.SimpleBlobDetector_create()
# while True:
#     time = perf_counter()
#     img1 = a = np.asarray(Elbow_camera.frame)
#     cv2.imshow('stream1', img1)
#     img2 = a = np.asarray(Shoulder_camera.frame)
#     cv2.imshow('stream2', img2)
#     #print(perf_counter() - time)
#     cv2.waitKey(1)







    # Detect blobs.
    #keypoints = detector.detect(img2)
    # Draw detected blobs as red circles.
    #cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
    #im_with_keypoints = cv2.drawKeypoints(img2, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    # Show keypoints
    #cv2.imshow("Keypoints", im_with_keypoints)
    #cv2.waitKey(0)

    # for keyPoint in keypoints:
    #     x = keyPoint.pt[0]
    #     y = keyPoint.pt[1]
    #     s = keyPoint.size
    #     print(x, y)
    # cv2.waitKey(1)
