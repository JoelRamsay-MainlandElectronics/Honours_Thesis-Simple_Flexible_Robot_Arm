import numpy as np
import matplotlib.pyplot as plt
from user_variables import *
from operator import add
class PlotData(object):
    def __init__(self):
        self.Kp_j = -1
        self.Ki_j = -1
        self.Kd_j = -1
        self.Kp_v = -1
        self.Ki_v = -1
        self.Kd_v = -1
        self.dpi = 30

        return None

    def joint(self, position, velocity, acceleration, torque, setpoint, identity):
        if identity == "Elbow":
            if UserVariables.motor_method == "torque":
                self.Kp_j = UserVariables.Kp_j_elbow
                self.Ki_j = UserVariables.Ki_j_elbow
                self.Kd_j = UserVariables.Kd_j_elbow
            elif UserVariables.motor_method == "position":
                self.Kp_j = UserVariables.Kp_j_elbow_position
                self.Ki_j = UserVariables.Ki_j_elbow_position
                self.Kd_j = UserVariables.Kd_j_elbow_position
            elif UserVariables.motor_method == "velocity":
                self.Kp_j = UserVariables.Kp_j_elbow_velocity
                self.Ki_j = UserVariables.Ki_j_elbow_velocity
                self.Kd_j = UserVariables.Kd_j_elbow_velocity
            ylim_pos = 250
            ylim_vel = 650
            ylim_acc = 4000
            ylim_torque = UserVariables.elbow_current_lim +50
        elif identity == "Shoulder":
            if UserVariables.motor_method == "torque":
                self.Kp_j = UserVariables.Kp_j_shoulder
                self.Ki_j = UserVariables.Ki_j_shoulder
                self.Kd_j = UserVariables.Kd_j_shoulder
            elif UserVariables.motor_method == "position":
                self.Kp_j = UserVariables.Kp_j_shoulder_position
                self.Ki_j = UserVariables.Ki_j_shoulder_position
                self.Kd_j = UserVariables.Kd_j_shoulder_position
            elif UserVariables.motor_method == "velocity":
                self.Kp_j = UserVariables.Kp_j_shoulder_velocity
                self.Ki_j = UserVariables.Ki_j_shoulder_velocity
                self.Kd_j = UserVariables.Kd_j_shoulder_velocity
            ylim_pos = 250
            ylim_vel = 100
            ylim_acc = 2500
            ylim_torque = UserVariables.shoulder_current_lim + 50
        else:
            print("Unknown Identity")

        # Determine how many motions have bene completed, for plotting the setpoint
        number_of_runs = int(len(position) / len(setpoint))
        x = np.linspace(0, (UserVariables.timespan+UserVariables.timespan_home)*number_of_runs, len(position))
        linewidth = 0.5
        #dpi = 150

        setpoint_plot = [] #initialise
        for _ in range(number_of_runs):
            setpoint_plot = np.concatenate((setpoint_plot,setpoint), axis=None)

        cm_width = 30
        cm_height = 15

        if UserVariables.motor_method == "torque":
            numplots = 4
        else:
            numplots = 3

        fig, axs = plt.subplots(numplots, sharex=True, dpi=self.dpi, figsize=(cm_width / 2.54, cm_height / 2.54))
        plt.suptitle(identity + " Joint Data\n"+ UserVariables.motor_method.capitalize() +" Mode"+"\nKp= " + str(self.Kp_j) + ", Ki= " + str(self.Ki_j) + ", Kd=" + str(self.Kd_j))
        plt.xlabel("Time (s)")

        axs[0].plot(x, setpoint_plot, 'k:', label='setpoint', linewidth=linewidth)  # position graph

        axs[0].plot(x,position, 'tab:blue', linewidth=linewidth) #position graph
        axs[0].set(ylabel='Position (\u03B8)', ylim=[0, 360])
        axs[1].plot(x,velocity, 'tab:orange',linewidth=linewidth) #velocity graph
        axs[1].set(ylabel='Velocity ('r'$\omega$)',ylim=[-ylim_vel, ylim_vel])
        axs[2].plot(x,acceleration, 'tab:red',linewidth=linewidth) #acceleration graph
        axs[2].set(ylabel='Acceleration ('r'$\alpha$)',ylim=[-ylim_acc, ylim_acc])

        if UserVariables.motor_method == "torque":
            axs[3].plot(x,torque, 'tab:green',linewidth=linewidth) #torque graph
            axs[3].set(ylabel='Torque ('r'$\tau$)',ylim=[-ylim_torque, ylim_torque])

        #Adding colour boxes to the graphs, to make it easier to see time spans (for higher than one motion)
        for i in range(len(axs)):
            index = 0
            for j in range(number_of_runs):
                axs[i].axvline(x=(j * (UserVariables.timespan + UserVariables.timespan_home)), color='k', alpha=0.5, linewidth=0.5)
                axs[i].axvline(x=j * (UserVariables.timespan + UserVariables.timespan_home) + UserVariables.timespan + UserVariables.timespan_home, color='k', alpha=0.5, linewidth=0.5)
                if (index % 2) == 1:

                    axs[i].axvspan(j * (UserVariables.timespan + UserVariables.timespan_home),
                                   j * (UserVariables.timespan + UserVariables.timespan_home) + (UserVariables.timespan + UserVariables.timespan_home), facecolor='k', alpha=0.1)
                else:
                    axs[i].axvspan(j * (UserVariables.timespan + UserVariables.timespan_home),
                                   j * (UserVariables.timespan + UserVariables.timespan_home) + (UserVariables.timespan + UserVariables.timespan_home), facecolor='k', alpha=0.05)
                index = index + 1
        plt.show()
        return None

    def link(self, position, velocity, acceleration,  Kp_v, Ki_v, Kd_v, setpoint, identity):

        if identity == "Lower Arm":
            ylim_pos = 60
            ylim_vel = 5000
            ylim_acc = 250000
        elif identity == "Upper Arm":
            ylim_pos = 40
            ylim_vel = 500
            ylim_acc = 50000
        else:
            quit("Unknown Identity")

        number_of_runs = int(len(position) / len(setpoint))
        x = np.linspace(0, (UserVariables.timespan+UserVariables.timespan_home)*number_of_runs, len(position))
        linewidth = 0.5
        # dpi = 150
        cm_width = 30
        cm_height = 15
        fig, axs = plt.subplots(3, sharex=True, dpi=self.dpi, figsize=(cm_width/2.54,cm_height/2.54))
        plt.suptitle(identity + " Deflection Data\n"+ UserVariables.motor_method.capitalize() +" Mode"+"\nKp= " + str(Kp_v) + ", Ki= " + str(Ki_v) + ", Kd=" + str(Kd_v))
        plt.xlabel("Time (s)")
        axs[0].plot(x, position, 'tab:blue', linewidth=linewidth, )  # position graph
        axs[0].set(ylabel='Position (\u03B8)',ylim=[-ylim_pos, ylim_pos])
        axs[1].plot(x, velocity, 'tab:orange', linewidth=linewidth, )  # velocity graph
        axs[1].set(ylabel='Velocity ('r'$\omega$)',ylim=[-ylim_vel, ylim_vel])
        axs[2].plot(x, acceleration, 'tab:red', linewidth=linewidth, )  # acceleration graph
        axs[2].set(ylabel='Acceleration ('r'$\alpha$)',ylim=[-ylim_acc, ylim_acc])

        # Adding colour boxes to the graphs, to make it easier to see time spans (for higher than one motion)
        for i in range(len(axs)):
            index = 0
            for j in range(number_of_runs):
                axs[i].axvline(x=(j * (UserVariables.timespan + UserVariables.timespan_home)), color='k', alpha=0.5, linewidth=0.5)
                axs[i].axvline(x=j * (UserVariables.timespan + UserVariables.timespan_home) + UserVariables.timespan + UserVariables.timespan_home, color='k', alpha=0.5, linewidth=0.5)
                if (index % 2) == 1:

                    axs[i].axvspan(j * (UserVariables.timespan + UserVariables.timespan_home),
                                   j * (UserVariables.timespan + UserVariables.timespan_home) + (UserVariables.timespan + UserVariables.timespan_home), facecolor='k', alpha=0.1)
                else:
                    axs[i].axvspan(j * (UserVariables.timespan + UserVariables.timespan_home),
                                   j * (UserVariables.timespan + UserVariables.timespan_home) + (UserVariables.timespan + UserVariables.timespan_home), facecolor='k', alpha=0.05)
                index = index + 1
        plt.show()
        return None


    def true_position(self, motor_object, positioning_control_object,link_deflection_data_object, Kp_v, Ki_v, Kd_v, setpoint, identity):


        joint_position = motor_object.record_data.position_data
        deflection_position = link_deflection_data_object.record_data.position_data

        joint_velocity = positioning_control_object.record_data.velocity_data
        deflection_velocity = link_deflection_data_object.record_data.velocity_data

        joint_acceleration = positioning_control_object.record_data.acceleration_data
        deflection_acceleration = link_deflection_data_object.record_data.acceleration_data


        position = list(map(add, joint_position, deflection_position))
        velocity = list(map(add, joint_velocity, deflection_velocity))
        acceleration = list(map(add, joint_acceleration, deflection_acceleration))

        if identity == "Lower Arm":
            ylim_vel = 5000
            ylim_acc = 250000
        elif identity == "Upper Arm":
            ylim_vel = 500
            ylim_acc = 50000
        else:
            quit("Unknown Identity")

        number_of_runs = int(len(position) / len(setpoint))
        x = np.linspace(0, (UserVariables.timespan+UserVariables.timespan_home)*number_of_runs, len(position))
        linewidth = 0.5
        # dpi = 150
        cm_width = 30
        cm_height = 15

        setpoint_plot = [] #initialise
        for _ in range(number_of_runs):
            setpoint_plot = np.concatenate((setpoint_plot,setpoint), axis=None)

        fig, axs = plt.subplots(3, sharex=True, dpi=self.dpi, figsize=(cm_width/2.54,cm_height/2.54))
        plt.suptitle(identity + " True Position Data\n"+ UserVariables.motor_method.capitalize() +" Mode"+"\nKp= " + str(Kp_v) + ", Ki= " + str(Ki_v) + ", Kd=" + str(Kd_v))
        plt.xlabel("Time (s)")

        axs[0].plot(x, setpoint_plot, 'k:', label='setpoint', linewidth=linewidth)  # position graph set point

        axs[0].plot(x, position, 'tab:blue', linewidth=linewidth, )  # position graph
        axs[0].set(ylabel='Position (\u03B8)', ylim=[0, 360])
        axs[1].plot(x, velocity, 'tab:orange', linewidth=linewidth, )  # velocity graph
        axs[1].set(ylabel='Velocity ('r'$\omega$)', ylim=[-ylim_vel, ylim_vel])
        axs[2].plot(x, acceleration, 'tab:red', linewidth=linewidth, )  # acceleration graph
        axs[2].set(ylabel='Acceleration ('r'$\alpha$)', ylim=[-ylim_acc, ylim_acc])


        # Adding colour boxes to the graphs, to make it easier to see time spans (for higher than one motion)
        for i in range(len(axs)):
            index = 0
            for j in range(number_of_runs):
                axs[i].axvline(x=(j * (UserVariables.timespan + UserVariables.timespan_home)), color='k', alpha=0.5, linewidth=0.5)
                axs[i].axvline(x=j * (UserVariables.timespan + UserVariables.timespan_home) + UserVariables.timespan + UserVariables.timespan_home, color='k', alpha=0.5, linewidth=0.5)
                if (index % 2) == 1:

                    axs[i].axvspan(j * (UserVariables.timespan + UserVariables.timespan_home),
                                   j * (UserVariables.timespan + UserVariables.timespan_home) + (UserVariables.timespan + UserVariables.timespan_home), facecolor='k', alpha=0.1)
                else:
                    axs[i].axvspan(j * (UserVariables.timespan + UserVariables.timespan_home),
                                   j * (UserVariables.timespan + UserVariables.timespan_home) + (UserVariables.timespan + UserVariables.timespan_home), facecolor='k', alpha=0.05)
                index = index + 1
        plt.show()
        return None
