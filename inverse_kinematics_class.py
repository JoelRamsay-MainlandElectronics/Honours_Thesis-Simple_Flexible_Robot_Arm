import robot_physical_properties_class
from imports_file import *
from globals import *

class inv_kinematics(object):
    def __init__(self):
        self.calculate_joint_trajectory()
        return None

    def calculate_joint_trajectory(self):
        """
        :param end_effector_position: (x,y) position of end effector
        :return: joint angle of shoulder and elbow
        """
        x_trajectory, y_trajectory = trajectory_generator().generate_linear_path_trajectory(UserVariables.feedrate)  # make a trajectory
        #print(x_trajectory)
        num_samples = len(x_trajectory)
        #print(num_samples)
        reach = np.ones(len(x_trajectory))  # initialise the reach array
        for i in range(num_samples):
            for j in range(len(x_trajectory)):
                reach[i, j] = np.sqrt(np.square(x_trajectory[i, j]) + np.square(y_trajectory[i, j]))  # mm

        a = robot_physical().upper_link_length  # link 2 is connected to the actuator
        b = robot_physical().lower_link_length  # link 1 is connected to the ground link
        c = reach

        theta_elbow = np.ones((num_samples, x_trajectory.shape[1]))  # initialise the theta array
        for i in range(num_samples):
            for j in range(x_trajectory.shape[1]):  # for each datapoint position of the tool, determine theta
                theta_elbow[i, j] = np.degrees(np.arccos((np.square(b) + np.square(c[i, j]) - np.square(a)) / (2 * b * c[i, j])))  # theta is in degrees

        theta_shoulder = np.ones((num_samples, x_trajectory.shape[1]))
        for i in range(num_samples):
            for j in range(x_trajectory.shape[1]):
                theta_shoulder[i, j] = theta_elbow[i, j]  # vector of theta for ground link joint

        theta_start_point = np.ones((num_samples, x_trajectory.shape[1]))  # initialise the theta offset array
        theta_path_ground_link = np.ones((num_samples, x_trajectory.shape[1]))  # initialise the theta offset array
        theta_path_tool_link = np.ones((num_samples, x_trajectory.shape[1]))
        for i in range(num_samples):
            for j in range(x_trajectory.shape[1]):
                # print("j",j)
                theta_start_point[i, j] = np.degrees(np.arctan(y_trajectory[i, j] / x_trajectory[i, j]))
                theta_path_ground_link[i, j] = theta_shoulder[i, j] + theta_start_point[i, j]
                theta_path_tool_link[i, j] = 180 - (2 * theta_elbow[i, j])

        trajectory_generator
        return shoulder,elbow



if __name__ == "__main__":
    shoulder,elbow = inv_kinematics()
    print("Shoulder: ",shoulder,"\tElbow: ",elbow)