import numpy as np
from roboticstoolbox import quintic

from globals import *
from imports_file import *
from globals import *
from user_variables import *
import numpy as np

class trajectory_generator(object):
    def __init__(self):
        return None

    def generate_linear_path_trajectory(self, feedrate):
        """
        :param start: the end effector starting position, (x,y)
        :param end: the end effector ending position, (x,y)
        :param feedrate: the feedrate of the end effector (mm/minute)
        """

        x = []
        y = []

        for i in range(UserVariables.number_random_motions):
            x = np.ones((UserVariables.number_random_motions,1))
            y = np.ones((UserVariables.number_random_motions,1))

        x_trajectory = []
        y_trajectory = []

        for i in range(UserVariables.number_random_motions-1):
            #calculate the linear distance between end effector start and end points
            distance = np.abs(np.sqrt(np.square(x[i + 1] - x[i]) + np.square(y[i + 1] - y[i]))) #linear distance of motion between points
            time_motion = distance / feedrate #feedrate
            num_steps = time_motion * UserVariables.update_frequency
            #print(int(x[i]))
            x_trajectory.append(np.linspace(int(x[i]), int(x[i+1]), int(num_steps)))
            y_trajectory.append(np.linspace(int(y[i]), int(y[i + 1]), int(num_steps))) #a matrix containing vectors of position as a function of time.
            linear_trajectory = quintic(0, distance, num_steps)
            traj_angle = np.abs(np.arctan((y[i+1] - y[i]) / (x[i+1] - x[i])))

            #set the trajectories based on the direction of the x and y motion
            if ((int(x[i+1]) - int(x[i])) > 0) and ((int(y[i+1]) - int(y[i])) > 0):
                x_trajectory[i] = x(i) + np.squeeze(linear_trajectory.s) * (np.cos(traj_angle))
                y_trajectory[i] = y(i) + np.squeeze(linear_trajectory.s) * (np.sin(traj_angle))

            elif ((int(x[i+1]) - int(x[i])) > 0) and ((int(y[i+1]) - int(y[i])) < 0):
                x_trajectory[i] = x(i) + np.squeeze(linear_trajectory.s) * (np.cos(traj_angle))
                y_trajectory[i] = y(i) - np.squeeze(linear_trajectory.s) * (np.sin(traj_angle))

            elif ((int(x[i+1]) - int(x[i])) < 0) and ((int(y[i+1]) - int(y[i])) > 0):
                x_trajectory[i] = x(i) - np.squeeze(linear_trajectory.s) * (np.cos(traj_angle))
                y_trajectory[i] = y(i) + np.squeeze(linear_trajectory.s) * (np.sin(traj_angle))

            elif ((int(x[i+1]) - int(x[i])) < 0) and ((int(y[i+1]) - int(y[i])) < 0):
                x_trajectory[i] = x(i) - np.squeeze(linear_trajectory.s) * (np.cos(traj_angle))
                y_trajectory[i] = y(i) - np.squeeze(linear_trajectory.s) * (np.sin(traj_angle))
        print(x_trajectory[0])
        return x_trajectory,y_trajectory

