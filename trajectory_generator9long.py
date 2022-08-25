#This version creates a long series of motion through many various points.
#This will enable the RL model to generalise on many different motions.
import math
import sys
print("Python version")
print (sys.version)
print("Version info.")
print (sys.version_info)
import random
#import tensorflow as tf
#from tensorflow import keras
import matplotlib.pyplot as plt
#import cv2
import numpy as np
import csv

#print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

############################################user variables###################################################
num_display_robots = 2
num_display_graphics_series = 2

link1 = 500 #mm length of link 1
link2 = 500 #mm length of link 2
#!!!!Link lengths must be identical, otherwise the calculations are wrong for angles.

x_max = 700#500#301#300 #end X position
x_min = 150#300#0 #Start X position
y_max = 700#801#850
y_min = 150#849#800

num_samples = 10 #number of robots
precision = 0.04 #used to control how precise the motion datapoints are, and how many are in the vectors. Gives 250 datapoints at 0.004 seconds/sample.
minimum_amount = 0 #minimum distance of movement.

time_upper_limit = 2 #number of seconds for motion to run
settling_time = 2  #number of seconds for the motion to settle after movement

maximum_velocity = 0.95#used to control the trapezoidal profile.


number_datapoints = int((time_upper_limit+settling_time)/precision) #number of datapoints in the matrix. This changes the precision of the motion.
print("Number of datapoints used in motion profile: ",number_datapoints)

###########################################################################################################



if num_display_graphics_series > num_samples:
    exit("User Error: There are a smaller number of robot samples than what is being displayed in graphics. Please increase the number of samples, or decrease the number of graphics samples.")
toolpath = np.ones((num_samples,number_datapoints))

#we need to input the m1 and m2 angles, and the link 1 and link 2 lengths
#[[v1,v2,v3,v4,time]]

time = np.arange(0, time_upper_limit, (time_upper_limit+settling_time)/precision)
#we have the time vector
#we need to have a target position path, time based
#we need to have a kinematic motion path for the target, based on the position equations


####################################setting the target path vector#####################################
#second integral of acceleration profiles
    # from numpy import diff
    # dx = 0.001
    # y = theta1_raw
    # theta1 = diff(y) / dx
    # #y = theta1
    # #theta1 = diff(y) / dx
    #
    # y = theta2_raw
    # theta2 = diff(y) / dx
    #y = theta2
    #theta2 = diff(y) / dx
from roboticstoolbox import *
q0 = 0
qf = 500
qd0 = 0
qdf = 0
t = number_datapoints
#tg = quintic(q0, qf, t)
#print(len(tg))
#print(tg)
#print(tg.q.shape)
#print(tg.p.shape)
#print(tg.t)
#print(tg.name)
#print(tg.s)
#print(tg.sd)
#plt.plot(tg.s)
#plt.show()
#plt.plot(tg.sd)
#plt.show()
#plt.plot(tg.sdd)
#plt.show()

#plot(tg.sd)
#qplot(tg.pd)
#qplot(tg.pdd)
#plt.plot(tg)
#xlabel('t')
#ylabel('y(t)')




x_starting_point = np.ones((num_samples,1))
y_starting_point = np.ones((num_samples,1))
x_ending_point = np.ones((num_samples,1))
y_ending_point = np.ones((num_samples,1))
#print(x_starting_point.shape)

#we want the first starting point to be user defined, and the first end point to be random.
#Then we want the second start point to be set to the first end point. Then the second end point is random. Repeat.
#Then we will combine all of the robot trajectories in MATLAB.


x_starting_point[0] = np.random.uniform(x_min,x_max,(1,1))
y_starting_point[0] = np.random.uniform(x_min,x_max,(1,1))
x_ending_point[0] = np.random.uniform(x_min,x_max-minimum_amount,(1,1))+minimum_amount
y_ending_point[0] = np.random.uniform(x_min,x_max-minimum_amount,(1,1))+minimum_amount

for i in range(num_samples-1):
    x_starting_point[i+1] = x_ending_point[i] #Starting point is the last ending point!
    y_starting_point[i+1] = y_ending_point[i]
    x_ending_point[i+1] = np.random.uniform(x_min,x_max,(1,1))
    y_ending_point[i+1] = np.random.uniform(x_min,x_max,(1,1))

    while np.abs(x_ending_point[i+1] - x_ending_point[i]) < minimum_amount:
        #Generate a new point until the sample is acceptable
        x_ending_point[i + 1] = np.random.uniform(x_min, x_max, (1, 1))
    while np.abs(y_ending_point[i+1] - y_ending_point[i]) < minimum_amount:
        #Generate a new point until the sample is acceptable
        y_ending_point[i + 1] = np.random.uniform(y_min, y_max, (1, 1))

    # if x_starting_point[i+1] > 500:
    #     print("x_starting_point:",x_starting_point[i])
    # if x_starting_point[i+1] > 500:
    #     print("y_starting_point:",x_starting_point[i])
    # if x_ending_point[i+1] > 500:
    #     print("x_ending_point:",x_ending_point[i])
    # if x_ending_point[i+1] > 500:
    #     print("y_ending_point:",x_ending_point[i])

print("x_starting_point:",x_starting_point)
print("y_starting_point:",x_starting_point)
print("x_ending_point:", x_ending_point)
print("y_ending_point:", x_ending_point)
x_target_path = np.ones((num_samples,number_datapoints))
y_target_path = np.ones((num_samples,number_datapoints))
#print("targetpath",x_target_path.shape)
#print(x_ending_point[0])
acceleration = 1
for i in range(num_samples):
    #for j in range(number_datapoints):
        #print(i,j)
        #x_target_path[i,j] = round(float((((x_ending_point[i] - x_starting_point[i])/number_datapoints)*j)+x_starting_point[i]),2)#linear interpolation of path between starting and ending point
        #y_target_path[i,j] = round(float((((y_ending_point[i] - y_starting_point[i])/number_datapoints)*j)+y_starting_point[i]),2)
    x1 = x_starting_point[i]
    x2 = x_ending_point[i]
    y1 = y_starting_point[i]
    y2 = y_ending_point[i]
    traj_angle = np.abs(np.arctan((y2 - y1) / (x2 - x1)))
    c_len = np.sqrt(np.square(x2-x1)+np.square(y2-y1))

    if (x2 - x1) > 0:
        if (y2 - y1) > 0:
            traj_angle = np.abs(np.arctan((y2 - y1) / (x2 - x1)))
            c_len = np.sqrt(np.square(x2 - x1) + np.square(y2 - y1))
            trajectory_c = quintic(0, c_len, number_datapoints)
            trajectory_x = x1 + np.squeeze(trajectory_c.s) * (np.cos(traj_angle))
            trajectory_y = y1 + np.squeeze(trajectory_c.s) * (np.sin(traj_angle))

        if (y2 - y1) < 0:
            traj_angle = np.abs(np.arctan((y2 - y1) / (x2 - x1)))
            c_len = np.sqrt(np.square(x2 - x1) + np.square(y2 - y1))
            trajectory_c = quintic(0, c_len, number_datapoints)
            trajectory_x = x1 + np.squeeze(trajectory_c.s) * (np.cos(traj_angle))
            trajectory_y = y1 - np.squeeze(trajectory_c.s) * (np.sin(traj_angle))

    elif (x2 - x1) < 0:
        if (y2 - y1) > 0:
            traj_angle = np.abs(np.arctan((y2 - y1) / (x2 - x1)))
            c_len = np.sqrt(np.square(x2 - x1) + np.square(y2 - y1))
            trajectory_c = quintic(0, c_len, number_datapoints)
            trajectory_x = x1 - np.squeeze(trajectory_c.s) * (np.cos(traj_angle))
            trajectory_y = y1 + np.squeeze(trajectory_c.s) * (np.sin(traj_angle))

        if (y2 - y1) < 0:
            traj_angle = np.abs(np.arctan((y2 - y1) / (x2 - x1)))
            c_len = np.sqrt(np.square(x2 - x1) + np.square(y2 - y1))
            trajectory_c = quintic(0, c_len, number_datapoints)
            trajectory_x = x1 - np.squeeze(trajectory_c.s) * (np.cos(traj_angle))
            trajectory_y = y1 - np.squeeze(trajectory_c.s) * (np.sin(traj_angle))

    # trajectory_x = x1 + np.squeeze(trajectory_c.s) * (np.cos(traj_angle))
    # trajectory_y = y1 + np.squeeze(trajectory_c.s) * (np.sin(traj_angle))

    x_target_path[i,:] = trajectory_x
    y_target_path[i,:] = trajectory_y
print("x_target_path",x_target_path)
print("y_target_path",y_target_path)
#print("c_len",c_len)



#print(x_target_path)
#print(y_target_path)


##########################Physical Simulated Toolpath (with added Gausian noise)#############################
#For now we take the actual path, and add a carrier signal to it, or some noise
x_noisy_path = np.ones((num_samples,number_datapoints))
y_noisy_path = np.ones((num_samples,number_datapoints))
for i in range(num_samples):
    for j in range(number_datapoints):
        #x_noisy_path[i,j] = round(float((((x_ending_point[i] - x_starting_point[i])/number_datapoints)*j)+x_starting_point[i]),2) + np.random.uniform(0,0.2,1)#+ 1*np.cos(j/10) #linear interpolation of path between starting and ending point
        #y_noisy_path[i,j] = round(float((((y_ending_point[i] - y_starting_point[i])/number_datapoints)*j)+y_starting_point[i]),2) + np.random.uniform(0,0.2,1)#- 1*np.cos(j/10)
        x_noisy_path[i, j] =  x_target_path[i,j] + np.random.uniform(0, 0.2, 1) # + 1*np.cos(j/10) #linear interpolation of path between starting and ending point
        y_noisy_path[i, j] =  y_target_path[i,j]+ np.random.uniform(0, 0.2, 1)  # - 1*np.cos(j/10)

#########################################Kinematics of Robot arm###########################################################

#for each point in the toolpath, calculate the angles for joint one and two.
#we can set both joint angles equal to each other, prior to offsetting


reach = np.ones((num_samples,number_datapoints)) #initialise the reach array
for i in range(num_samples):
    for j in range(number_datapoints):
        reach[i,j] = np.sqrt(   np.square(x_target_path[i,j]) + np.square(y_target_path[i,j]) ) #mm

a = link2 #link 2 is connected to the actuator
b = link1 #link 1 is connected to the ground link
c = reach
#print("reach:",reach)

###############################determining theta vector########################################
theta = np.ones((num_samples,number_datapoints)) #initialise the theta array
for i in range(num_samples):
    for j in range(number_datapoints): #for each datapoint position of the tool, determine theta
        theta[i,j] = np.degrees(np.arccos((np.square(b) + np.square(c[i,j]) - np.square(a))/(2*b*c[i,j]))) #theta is in degrees


#############################calculating the shoulder offset angle for joint 2 (ground link joint)########################
# theta_offset = np.ones((num_samples,1)) #initialise the theta offset array
# for i in range(num_samples):
#     theta_offset[i] = np.degrees(np.arctan(y_ending_point/x_ending_point))

#print(theta_offset[0,0])
#print(theta[0,0])
theta_ground_link = np.ones((num_samples,number_datapoints))
for i in range (num_samples):
    for j in range(number_datapoints):
        theta_ground_link[i,j] = theta[i,j] #vector of theta for ground link joint
#print(theta_ground_link)
#############################Theta path############################################################
#Put the angles of the motors into vectors so that the motion is smooth
theta_start_point = np.ones((num_samples,number_datapoints)) #initialise the theta offset array
theta_path_ground_link = np.ones((num_samples, number_datapoints))  # initialise the theta offset array
theta_path_tool_link = np.ones((num_samples, number_datapoints))
for i in range(num_samples):
    for j in range(number_datapoints):
        #print("j",j)
        theta_start_point[i,j] = np.degrees(np.arctan(y_target_path[i,j] / x_target_path[i,j]))
        theta_path_ground_link[i, j] = theta_ground_link[i, j] + theta_start_point[i,j]
        theta_path_tool_link[i, j] = 180 - (2*theta[i, j])


###############################draw start and end positions of robot arm on the path graphs#########################
def draw_angle(angle, angle_offset, centre_position_x,centre_position_y):
    iterations = 200
    for i in range(iterations):
        angle_split = angle/iterations
        offset_x = 50*np.cos(np.radians((angle_split*i)-angle_offset))
        offset_y = 50*np.sin(np.radians((angle_split*i)-angle_offset))
        plt.scatter(centre_position_x+offset_x,centre_position_y+offset_y, c="black",s=0.1)

# def draw_gripper(position, angle):
#     if position == "start":
#         rectangle = plt.Rectangle((x_target_path[i,0], y_target_path[i,0]), 50, 10, fc='blue', ec='blue',zorder=0)
#         plt.gca().add_patch(rectangle)





print("Processing Complete. Displaying Graphics.")
#for i in range(num_display_robots):
for i in range(1):
    #print the theta values to debug console
    elbow_pos_x_start = np.ones((num_samples, 1))  # initialise the elbow position array
    elbow_pos_y_start = np.ones((num_samples, 1))
    elbow_pos_x_end = np.ones((num_samples, 1))
    elbow_pos_y_end = np.ones((num_samples, 1))

    elbow_pos_x_start[i] = link1 * np.cos(np.radians(theta_path_ground_link[i, 0]))  # get the positions for various plotting features
    elbow_pos_y_start[i] = link1 * np.sin(np.radians(theta_path_ground_link[i, 0]))
    elbow_pos_x_end[i] = link1 * np.cos(np.radians(theta_path_ground_link[i, -1]))
    elbow_pos_y_end[i] = link1 * np.sin(np.radians(theta_path_ground_link[i, -1]))

    verified_link1_start = np.ones((num_samples, 1))
    verified_link2_start = np.ones((num_samples, 1))
    verified_link1_end = np.ones((num_samples, 1))
    verified_link2_end = np.ones((num_samples, 1))

    verified_link1_start[i] = np.sqrt(np.square(elbow_pos_x_start[i]) + np.square(elbow_pos_y_start[i]))
    verified_link2_start[i] = np.sqrt(np.square(x_target_path[i, 0] - elbow_pos_x_start[i]) + np.square(y_target_path[i, 0] - elbow_pos_y_start[i]))
    verified_link1_end[i] = np.sqrt(np.square(elbow_pos_x_start[i]) + np.square(elbow_pos_y_start[i]))
    verified_link2_end[i] = np.sqrt(np.square(x_target_path[i, -1] - elbow_pos_x_end[i]) + np.square(y_target_path[i, -1] - elbow_pos_y_end[i]))

    print(theta[i, 0], theta[i, -1])
    print("Shoulder Joint Angle Start: ", int(theta_path_ground_link[i, 0]), "degrees.", "\tShoulder Joint Angle End: ", int(theta_path_ground_link[i, -1]), "degrees.")
    print("Shoulder Joint Angle Offset Start: ", int(theta_start_point[i, 0]), "degrees.", "\tShoulder Joint Angle Offset End: ", int(theta_start_point[i, -1]), "degrees.")
    print("Elbow Joint Angle Start:", int(theta_path_tool_link[i, 0]), "\tElbow Joint Angle End:", int(theta_path_tool_link[i, -1]))
    print("Reach[i,0]: ", int(reach[i, 0]), "\tReach[i,-1]: ", int(reach[i, -1]))
    print("Link1 Length: ", int(link1), "mm\t", "Link2 Length: ", int(link2), "mm")

    print("Verified Link1 Length Start: ", int(verified_link1_start[i]), "mm\t", "Verified Link2 Length Start: ", int(verified_link2_start[i]), "mm")
    print("Verified Link1 Length End: ", int(verified_link1_end[i]), "mm\t", "Verified Link2 Length End: ", int(verified_link2_end[i]), "mm")
    print("Elbow Joint Position:", (int(elbow_pos_x_start[i]), int(elbow_pos_y_start[i])))

    p1 = np.ones((num_samples, 2))
    p2 = np.ones((num_samples, 2))
    p3 = np.ones((num_samples, 2))
    p4 = np.ones((num_samples, 2))
    p1[i] = [0, elbow_pos_x_start[i]]
    p2[i] = [0, elbow_pos_y_start[i]]
    p3[i] = [0, elbow_pos_x_end[i]]
    p4[i] = [0, elbow_pos_y_end[i]]
    alpha = 0.7
    plt.plot(x_target_path[i], y_target_path[i],linestyle='--') #plot the target path
    plt.plot(p1[i],p2[i], color='green',linewidth=10,zorder=0,alpha=alpha) #draw ground link (start of movement)
    plt.plot(p3[i], p4[i], color='red', linewidth=10, zorder=1,alpha=alpha)  # draw ground link (end of movement)

    p1[i] = [elbow_pos_x_start[i],x_starting_point[i]]#
    p2[i] = [elbow_pos_y_start[i],y_starting_point[i]]
    p3[i] = [elbow_pos_x_end[i], x_ending_point[i]]
    p4[i] = [elbow_pos_y_end[i], y_ending_point[i]]

    plt.plot(p1[i], p2[i], color='green',linewidth=5,zorder=0,alpha=alpha) #draw tool link (start of movement)
    plt.plot(p3[i], p4[i], color='red',linewidth=5, zorder=1,alpha=alpha) #draw tool link (end of movement)

    plt.text(x_target_path[i, 0], y_target_path[i, 0], "Start\n("+str(int(x_target_path[i, 0])) + "," + str(int(y_target_path[i, 0])) + ")", zorder=20)
    plt.text(x_target_path[i, -1], y_target_path[i, -1], "End\n("+str(int(x_target_path[i, -1])) + "," + str(int(y_target_path[i, -1])) + ")", zorder=20)

    plt.text(elbow_pos_x_start[i], elbow_pos_y_start[i], "J2\n(" + str(int(elbow_pos_x_start[i])) + "," + str(int(elbow_pos_y_start[i])) + ")", zorder=20) #elbow joint position label
    plt.text(elbow_pos_x_end[i], elbow_pos_y_end[i], "J2'\n(" + str(int(elbow_pos_x_end[i])) + "," + str(int(elbow_pos_y_end[i])) + ")", zorder=20)  # elbow joint position label

    plt.scatter(elbow_pos_x_start[i], elbow_pos_y_start[i], c='green', linewidths=10, zorder=10,alpha=alpha) #draw the elbow joint
    plt.scatter(elbow_pos_x_end[i], elbow_pos_y_end[i], c='red', linewidths=10, zorder=10,alpha=alpha)  # draw the elbow joint

    plt.scatter(x_target_path[i, 1], y_target_path[i, 1], c='green', linewidths=3, zorder=10,alpha=alpha)  # draw the tool
    plt.scatter(x_target_path[i, -1], y_target_path[i, -1], c='red', linewidths=3, zorder=10,alpha=alpha)  # draw the tool

    draw_angle(theta_path_ground_link[i,0], 0, 0, 0)  # draw the ground link angle
    draw_angle(theta_path_tool_link[i, 0], (180 - theta_path_ground_link[i, 0]), elbow_pos_x_start[i], elbow_pos_y_start[i])  # draw the tool link angle
    draw_angle(theta_path_tool_link[i, -1], (180 - theta_path_ground_link[i, -1]), elbow_pos_x_end[i], elbow_pos_y_end[i])  # draw the tool link angle



#adding noise to theta inputs for the neural network to learn the transfer function dynamics of the robot arm
theta_path_ground_link_noisy = np.ones((num_samples,number_datapoints))
theta_path_tool_link_noisy = np.ones((num_samples,number_datapoints))
#low freq
A1 = random.uniform(0.2,0.5)
D1 = random.randrange(0,10)
freq1 = random.randrange(20,21)
#medium freq
A2 = random.randrange(1,2)
D2 = random.randrange(0,10)
freq2 = random.randrange(3,6)
#high freq
A3 = random.randrange(1,2)
D3 = random.randrange(0,10)
freq3 = random.randrange(1,3)

import random
for i in range(num_samples):
    for j in range(number_datapoints):
        theta_path_ground_link_noisy[i,j] = theta_path_ground_link[i,j] + A1*np.cos(j/freq1-D1) + A2*np.cos(j/freq2-D2) + A3*np.cos(j/freq3-D3)

#low freq
A1 = random.uniform(0.2,0.5)
D1 = random.randrange(0,10)
freq1 = random.randrange(20,21)
#medium freq
A2 = random.uniform(0.2,0.5)
D2 = random.randrange(0,10)
freq2 = random.randrange(3,6)
#high freq
A3 = random.uniform(0.2,0.5)
D3 = random.randrange(0,10)
freq3 = random.randrange(1,3)

import random
for i in range(num_samples):
    for j in range(number_datapoints):
        theta_path_tool_link_noisy[i,j] = theta_path_tool_link[i,j] + A1*np.cos(j/freq1-D1) + A2*np.cos(j/freq2-D2) + A3*np.cos(j/freq3-D3)


plt.suptitle("Robot Arm")
ax = plt.gca()
ax.set_aspect('equal', adjustable='box')
ax.set_xlim([-x_max, x_max])
ax.set_ylim([-y_max, y_max])
plt.xlabel("X axis")
plt.ylabel("Y axis")
plt.text(25, -10, "Origin", zorder=20)
plt.scatter(0, 0, c='black', s=500)
rectangle = plt.Rectangle((-26,-25), 52, 25, fc='black', ec='black')
plt.gca().add_patch(rectangle)
plt.show()


length = len(time)
for i in range(num_display_graphics_series):
    plt.plot(x_target_path[i], y_target_path[i],linestyle='--')
    #plt.text(x_target_path[i,0],y_target_path[i,0], "Start")
    #plt.text(x_target_path[i, -1], y_target_path[i, -1], "End")
plt.text(10,10, "Origin")
plt.scatter(0,0,c='black',linewidths=10) #draw the origin point
plt.suptitle("Target Path")


ax = plt.gca()
ax.set_aspect('equal', adjustable='box')
ax.set_xlim([0, x_max])
ax.set_ylim([0, y_max])
plt.xlabel("X axis")
plt.ylabel("Y axis")
plt.show()

for i in range(num_display_graphics_series):
    plt.plot(x_noisy_path[i],y_noisy_path[i],linestyle='--')
plt.suptitle("Simulated Physical Path (Noisy)")
ax = plt.gca()
ax.set_aspect('equal', adjustable='box')
ax.set_xlim([0, x_max])
ax.set_ylim([0, y_max])
plt.xlabel("X axis")
plt.ylabel("Y axis")
plt.show()


for i in range(num_display_graphics_series):
    plt.plot(theta_path_tool_link[i,:])
plt.suptitle("Theta (Tool Joint)")
ax = plt.gca()
#ax.set_aspect('equal', adjustable='box')
#ax.set_xlim([0, x_max])
#ax.set_ylim([0, y_max])
plt.xlabel("Time")
plt.ylabel("Theta (Tool Joint)")
plt.show()

for i in range(num_display_graphics_series):
    plt.plot(theta_path_tool_link_noisy[i,:])
plt.suptitle("Theta Tool Joint Noisy")
ax = plt.gca()
#ax.set_aspect('equal', adjustable='box')
#ax.set_xlim([0, x_max])
#ax.set_ylim([0, y_max])
plt.xlabel("Time")
plt.ylabel("Theta (Tool Joint)")
plt.show()


for i in range(num_display_graphics_series):
    plt.plot(theta_path_ground_link[i,:])
plt.suptitle("Theta Ground Link")
ax = plt.gca()
#ax.set_aspect('equal', adjustable='box')
#ax.set_xlim([0, len(time)])
#ax.set_ylim([0, y_max])
plt.xlabel("Time")
plt.ylabel("Theta (Ground Joint)")
plt.show()

for i in range(num_display_graphics_series):
    plt.plot(theta_path_ground_link_noisy[i,:])
plt.suptitle("Theta Ground Link Noisy")
ax = plt.gca()
#ax.set_aspect('equal', adjustable='box')
#ax.set_xlim([0, len(time)])
#ax.set_ylim([0, y_max])
plt.xlabel("Time")
plt.ylabel("Theta (Ground Joint)")
plt.show()



#########################writing data text files#############################

#extend the theta_path_ground_link and theta_path_tool_link vectors to include a settling time where the last angle does not change

time_plus_settle = np.arange(0, time_upper_limit+settling_time, (time_upper_limit+settling_time)/number_datapoints)
time_step = time_upper_limit/number_datapoints

number_datapoints_settle = int(settling_time / time_step)
last_val1 = np.zeros((num_samples, number_datapoints + number_datapoints_settle)) #theta1
last_val2 = np.zeros((num_samples, number_datapoints + number_datapoints_settle)) #theta2
last_val3 = np.zeros((num_samples, number_datapoints + number_datapoints_settle)) #theta1 noisy
last_val4 = np.zeros((num_samples, number_datapoints + number_datapoints_settle)) #theta2 noisy
print("datapoints: ",number_datapoints,number_datapoints_settle)
for i in range(num_samples):
    for j in range(number_datapoints + number_datapoints_settle):
        last_val1[i, j] = theta_path_ground_link[i, -1]
        last_val2[i, j] = theta_path_tool_link[i, -1]
        last_val3[i, j] = theta_path_ground_link[i, -1]#theta_path_ground_link_noisy gives variance in end points
        last_val4[i, j] = theta_path_tool_link[i, -1]

for i in range(num_samples):
    for j in range(number_datapoints):
        last_val1[i, j] = theta_path_ground_link[i, j] #copy the original values into the settle time matrix
        last_val2[i, j] = theta_path_tool_link[i, j]  # copy the original values into the settle time matrix
        last_val3[i, j] = theta_path_ground_link_noisy[i, j]  # copy the original values into the settle time matrix
        last_val4[i, j] = theta_path_tool_link_noisy[i, j]  # copy the original values into the settle time matrix


theta_path_ground_link = last_val1 #update the original matrix
theta_path_tool_link = last_val2 #update the original matrix
theta_path_ground_link_noisy = last_val3 #update the original matrix
theta_path_tool_link_noisy = last_val4 #update the original matrix

# #copy the first value into the noisy array
for i in range(num_samples):
    theta_path_ground_link_noisy[i, 0] = theta_path_ground_link[i, 0]  # copy the original values into the settle time matrix
    theta_path_tool_link_noisy[i, 0] = theta_path_tool_link[i, 0]  # copy the original values into the settle time matrix



#print(len(theta_path_tool_link[1]))
# with open('theta1.txt', 'w') as f:
#     for i in range(1):
#         for j in range(len(theta_path_ground_link[1])):
#             f.write(str(round(theta_path_ground_link[i, j], 3)))
#             f.write('\n')

# with open('theta2.txt', 'w') as f:
#     for i in range(1):
#         for j in range(len(theta_path_tool_link[1])):
#             f.write(str(round(theta_path_tool_link[i, j], 3)))
#             f.write('\n')

# with open('x_path_rigid.txt', 'w') as f:
#     for i in range(1):
#         for j in range(len(x_target_path[1])):
#             f.write(str(round(x_target_path[i, j], 3)))
#             f.write('\n')

# with open('y_path_rigid.txt', 'w') as f:
#     for i in range(1):
#         for j in range(len(y_target_path[1])):
#             f.write(str(round(y_target_path[i, j], 3)))
#             f.write('\n')



#write the full data for each robot to a CVS file
print(theta_path_tool_link.shape)
np.savetxt("theta1.csv", np.asarray(theta_path_ground_link), delimiter=",")
np.savetxt("theta2.csv", np.asarray(theta_path_tool_link), delimiter=",")
# print(theta_path_tool_link_noisy.shape)
# np.savetxt("theta1_noisy.csv", np.asarray(theta_path_ground_link_noisy), delimiter=",")
# np.savetxt("theta2_noisy.csv", np.asarray(theta_path_tool_link_noisy), delimiter=",")
#
# print(x_target_path.shape)
# np.savetxt("x_path_rigid.csv", np.asarray(x_target_path), delimiter=",")
# np.savetxt("y_path_rigid.csv", np.asarray(y_target_path), delimiter=",")




#print(x_target_path[1][0],y_target_path[1][0])

#print(theta_path_tool_link)


#we can get the machine learning to determine the theta1 and theta2 at each time point to give us the target path
#x_target_vector = d1*np.cos(theta1) + d2*np.cos(theat2) #this is the path vector for the arm tool
#y_target_vector = d1*np.sin(theta1) + d2*np.sin(theat2)

#x_target is a single position, also y_target
#the theta variables are changed with time to get to the target

#over the length of the time vector, split the theta movements into equal chunks



##############################################Flexible Robot Forward Kinematics#######################################################
#Now we can apply forward kinematics to a flexible robot model, so we can determine the flexible toolpath, then run a simulation to adjust the motor parameters after



#notes for 13/03/2021
#make vectors for motor position (done), aswell as its first and second derivatives.
#Make motor velocity and acceleration vectors.
#We will make our dynamic model, and we will likely tune the acceleration, velocity, and position vectors all together, to achieve the ideal toolpath.

#We need to make a flexible model of our robot using equations of motion, so we can do a forward kinematics simulation and determine the tool position as a function of time.
#Then we can pass the motor positions and the tool position and train an artificial neural network to determine the ideal path of the motors.
#Since the motor position and the velocity and acceleration are all linked to each other, we only really need to pass in the motor position as a function of time, into the artificial neural network.

#For the flexible robot analysis, we will do a three stage analysis.
#stage one will be position as a function of time, then velocity as a function of time, then acceleration as a function of time, of the tool tip.
#perhaps it will be best to actually run a model in a physics engine.
