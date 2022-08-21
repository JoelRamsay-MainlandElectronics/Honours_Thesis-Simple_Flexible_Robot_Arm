import numpy as np
from user_variables import *

class point_to_point(object):
    def __init__(self):
        self.elbow_position = None
        self.shoudler_position = None
        self.datapoints = None
        return None

    def generate_trajectory_elbow(self, start_position, end_position, trajectory_timespan, trajectory_timespan_home, update_frequency):
        #generate a simple trajectory NOT using inverse kinematics. Joint space control.
        start = start_position
        end = end_position

        #motion trajectory
        datapoints_motion = int(update_frequency * trajectory_timespan)
        self.trajectory = np.linspace(start,end,datapoints_motion) #angle in degrees

        #home trajectory
        datapoints_home = int(update_frequency * trajectory_timespan_home)
        self.trajectory_home = np.linspace(UserVariables.elbow_home, UserVariables.elbow_home, datapoints_home)  # angle in degrees
        self.trajectory = np.concatenate((self.trajectory, self.trajectory_home), axis=None)

        self.datapoints = datapoints_motion + datapoints_home
        return self.trajectory

    def generate_trajectory_shoulder(self, start_position, end_position, trajectory_timespan, trajectory_timespan_home, update_frequency):
        # generate a simple trajectory NOT using inverse kinematics. Joint space control.
        start = start_position
        end = end_position

        # motion trajectory
        datapoints_motion = int(update_frequency * trajectory_timespan)
        self.trajectory = np.linspace(start, end, datapoints_motion)  # angle in degrees

        # home trajectory
        datapoints_home = int(update_frequency * trajectory_timespan_home)
        self.trajectory_home = np.linspace(UserVariables.shoulder_home, UserVariables.shoulder_home, datapoints_home)  # angle in degrees
        self.trajectory = np.concatenate((self.trajectory, self.trajectory_home), axis=None)

        self.datapoints = datapoints_motion + datapoints_home
        return self.trajectory
