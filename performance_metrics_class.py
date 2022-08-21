import numpy as np

class PerformanceMetrics(object):
    def __init__(self, position, traj):
        self.position = position
        self.traj = traj
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
