from numpy import genfromtxt
import numpy as np

class MotionTraj(object):
    def __init__(self):
        self.position_elbow_vector = 0
        self.position_shoulder_vector = 0
        self.datapoints = 0
        return None

    def elbow(self):
        self.position_elbow_vector = genfromtxt('theta2.csv', delimiter=',')
        self.position_elbow_vector = self.position_elbow_vector[0:]
        self.position_elbow_vector = self.position_elbow_vector.astype(int)
        self.datapoints = len(self.position_elbow_vector)
        self.position_elbow_vector = np.reshape(self.position_elbow_vector, -1)
        self.datapoints = len(self.position_elbow_vector)
        #print(self.position_elbow_vector)
        return self.position_elbow_vector

    def shoulder(self):
        self.position_shoulder_vector = genfromtxt('theta1.csv', delimiter=',')
        self.position_shoulder_vector = self.position_shoulder_vector[0:] + 90
        self.position_shoulder_vector = self.position_shoulder_vector.astype(int)
        self.position_shoulder_vector = np.reshape(self.position_shoulder_vector, -1)
        return self.position_shoulder_vector