from operator import add

import numpy as np
from numpy import genfromtxt
from user_variables import *


class write_csv(object):
    def __init__(self, elbow_motor, shoulder_motor, elbow_frame_processing, shoulder_frame_processing, elbow_traj, shoulder_traj):

        ElbowTruePosition = list(map(add, elbow_motor.record_data.position_data, elbow_frame_processing.record_data.position_data))
        ShoulderTruePosition = list(map(add, shoulder_motor.record_data.position_data, shoulder_frame_processing.record_data.position_data))

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
        return None
