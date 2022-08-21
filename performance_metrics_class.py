from operator import add

import numpy as np

class PerformanceMetrics(object):
    def __init__(self, motor, frame_processing, traj):
        """

        :param motor: the motor object.
        :param frame_processing: the image frame processing object containing the angular deflection data.
        :param traj: the commanded trajectory vector.

        This class performs some simple analysis on the data collected from the robot. Overshoot, settling time, and rise time.
        """
        position = list(map(add, motor.record_data.position_data, frame_processing.record_data.position_data)) #element-wise addition of the joint angle and the deflection angles.
        self.position = position
        self.traj = traj
        #self.overshoot_percentage()
        return None

    def overshoot_percentage(self):
        maximum = np.max(self.position)
        setpoint = self.traj[-1]
        self.overshoot_percent = (maximum-setpoint)/setpoint
        return self.overshoot_percent

    def settling_time(self):
        return None
    def rise_time(self):
        return None
