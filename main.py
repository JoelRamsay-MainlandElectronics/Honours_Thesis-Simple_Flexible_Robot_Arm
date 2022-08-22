#Import Classes========================
import os

from camera_class import *
from image_processing_class import *
from servo_motor_class import *
from plot_class import *
from traj_p2p_class import *
from control_loop_class import *
from robot_graphics_class import *
from performance_metrics_class import *
from save_vectors_class import *
from traj_motion_class import *
from globals import *

#Import libraries=====================
import sys
import numpy as np
import time
import tkinter as tk
import tkinter.ttk as ttk
import threading
import sys





print("Python version")
print (sys.version)
#print("Version info.")
#print (sys.version_info)
#print(os.path.dirname(sys.executable))


#========================================
class GUI:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#ececec'  # Closest X11 color: 'gray92'
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.', background=_bgcolor)
        self.style.configure('.', foreground=_fgcolor)
        self.style.map('.', background=
        [('selected', _compcolor), ('active', _ana2color)])

        top.geometry("651x480+679+235")
        top.minsize(120, 1)
        top.maxsize(1924, 2141)
        top.resizable(1, 1)
        top.title("Toplevel 0")
        top.configure(background="#3e3e3e")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        self.top = top

        self.menubar = tk.Menu(top, font="TkMenuFont", bg='#c0c0c0', fg=_fgcolor)
        top.configure(menu=self.menubar)

        self.TProgressbar1 = ttk.Progressbar(self.top)
        self.TProgressbar1.place(relx=0.015, rely=0.667, relwidth=0.306
                                 , relheight=0.0, height=22)
        self.TProgressbar1.configure(length="199")

        self.Label1 = tk.Label(self.top)
        self.Label1.place(relx=0.031, rely=0.604, height=21, width=174)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(activeforeground="black")
        self.Label1.configure(background="#3e3e3e")
        self.Label1.configure(compound='left')
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(font="-family {Segoe UI} -size 14 -weight bold")
        self.Label1.configure(foreground="#ffffff")
        self.Label1.configure(highlightbackground="#d9d9d9")
        self.Label1.configure(highlightcolor="black")
        self.Label1.configure(text='''Motion Progress''')

        self.ESTOP = tk.Button(self.top)
        self.ESTOP.place(relx=0.031, rely=0.042, height=104, width=197)
        self.ESTOP.configure(activebackground="#ececec")
        self.ESTOP.configure(activeforeground="#000000")
        self.ESTOP.configure(background="#ff0000")
        self.ESTOP.configure(borderwidth="10")
        self.ESTOP.configure(compound='left')
        self.ESTOP.configure(cursor="fleur")
        self.ESTOP.configure(disabledforeground="#a3a3a3")
        self.ESTOP.configure(font="-family {Segoe UI} -size 36 -weight bold")
        self.ESTOP.configure(foreground="#ffffff")
        self.ESTOP.configure(highlightbackground="#d9d9d9")
        self.ESTOP.configure(highlightcolor="black")
        self.ESTOP.configure(pady="0")
        self.ESTOP.configure(text='''ESTOP''')

        self.RESET = tk.Button(self.top)
        self.RESET.place(relx=0.215, rely=0.292, height=34, width=77)
        self.RESET.configure(activebackground="#ececec")
        self.RESET.configure(activeforeground="#000000")
        self.RESET.configure(background="#ff8040")
        self.RESET.configure(borderwidth="5")
        self.RESET.configure(compound='left')
        self.RESET.configure(disabledforeground="#a3a3a3")
        self.RESET.configure(foreground="#ffffff")
        self.RESET.configure(highlightbackground="#d9d9d9")
        self.RESET.configure(highlightcolor="black")
        self.RESET.configure(pady="0")
        self.RESET.configure(text='''Reset''')

        self.CYCLESTART = tk.Button(self.top)
        self.CYCLESTART.place(relx=0.015, rely=0.875, height=44, width=87)
        self.CYCLESTART.configure(activebackground="#ececec")
        self.CYCLESTART.configure(activeforeground="#000000")
        self.CYCLESTART.configure(background="#00b300")
        self.CYCLESTART.configure(borderwidth="5")
        self.CYCLESTART.configure(compound='left')
        self.CYCLESTART.configure(disabledforeground="#a3a3a3")
        self.CYCLESTART.configure(font="-family {Segoe UI} -size 11 -weight bold")
        self.CYCLESTART.configure(foreground="#ffffff")
        self.CYCLESTART.configure(highlightbackground="#d9d9d9")
        self.CYCLESTART.configure(highlightcolor="black")
        self.CYCLESTART.configure(pady="0")
        self.CYCLESTART.configure(text='''Cycle Start''')

        self.SHUTDOWN = tk.Button(self.top)
        self.SHUTDOWN.place(relx=0.031, rely=0.292, height=34, width=87)
        self.SHUTDOWN.configure(activebackground="#ececec")
        self.SHUTDOWN.configure(activeforeground="#000000")
        self.SHUTDOWN.configure(background="#ff0000")
        self.SHUTDOWN.configure(borderwidth="5")
        self.SHUTDOWN.configure(compound='left')
        self.SHUTDOWN.configure(disabledforeground="#a3a3a3")
        self.SHUTDOWN.configure(foreground="#ffffff")
        self.SHUTDOWN.configure(highlightbackground="#d9d9d9")
        self.SHUTDOWN.configure(highlightcolor="black")
        self.SHUTDOWN.configure(pady="0")
        self.SHUTDOWN.configure(text='''Shutdown''')

        self.FEEDHOLD = tk.Button(self.top)
        self.FEEDHOLD.place(relx=0.169, rely=0.875, height=44, width=87)
        self.FEEDHOLD.configure(activebackground="#ececec")
        self.FEEDHOLD.configure(activeforeground="#000000")
        self.FEEDHOLD.configure(background="#ff0000")
        self.FEEDHOLD.configure(borderwidth="5")
        self.FEEDHOLD.configure(compound='left')
        self.FEEDHOLD.configure(disabledforeground="#a3a3a3")
        self.FEEDHOLD.configure(font="-family {Segoe UI} -size 11 -weight bold")
        self.FEEDHOLD.configure(foreground="#ffffff")
        self.FEEDHOLD.configure(highlightbackground="#ffffff")
        self.FEEDHOLD.configure(highlightcolor="black")
        self.FEEDHOLD.configure(pady="0")
        self.FEEDHOLD.configure(text='''Feed Hold''')


        #Set callbacks
        self.ESTOP.configure(command=self.set_estop_flag)
        self.RESET.configure(command=self.reset_flag)
        self.SHUTDOWN.configure(command=self.set_shutdown_flag)
        self.CYCLESTART.configure(command=self.set_cyclestart_flag)
        self.FEEDHOLD.configure(command=self.set_feedhold_flag)

    def set_estop_flag(self):
        print("estop")
        globals.estop_flag = 1 #sets the estop flag to 1, so the program turns off the motors and waits until reset and cycle start.

    def reset_flag(self):
        print("reset")#sets the estop flag to 1, so the program turns off the motors and waits until reset and cycle start.
        globals.reset_flag = 1
        globals.estop_flag = 0

    def set_shutdown_flag(self):
        print("shutdown")
        globals.shutdown_flag = 1 #sets the estop flag to 1, so the program turns off the motors and quits.

    def set_cyclestart_flag(self):
        print("cyclestart")
        globals.cycle_start_flag = 1 #sets the estop flag to 1, so the program turns off the motors and quits.


    def set_feedhold_flag(self):
        print("feedhold")
        globals.feedhold_flag = 1 #feedhold while in motion (stays at last position when in position mode)


class MainClass(object):
    def __init__(self):
        # Construct dynamixel motor related objects
        self.handler = initialise_Dynamixel()
        self.portHandler = self.handler.portHandler
        self.packetHandler = self.handler.packetHandler
        self.groupread_num = self.handler.initialise_bulk_read()  # only one of these variables exists
        self.groupwrite_num = self.handler.initialise_bulk_write()  # only one of these variables exists

        # Construct elbow and shoulder motor objects
        self.elbow_motor = motor(self.portHandler, self.packetHandler, self.groupread_num, self.groupwrite_num, "Elbow")
        self.shoulder_motor = motor(self.portHandler, self.packetHandler, self.groupread_num, self.groupwrite_num, "Shoulder")

        # Reboot the elbow and shoulder motors (rebooting resets any errors)
        self.elbow_motor.reboot_motor()
        self.shoulder_motor.reboot_motor()
        time.sleep(0.1)

        # Set drive mode of the motors (torque, velcoticy or position mode, determined in uservariabled class)
        self.elbow_motor.set_mode()
        self.shoulder_motor.set_mode()

        # Enable the motors (set the torque to 'on')
        self.elbow_motor.enable_motor()
        self.shoulder_motor.enable_motor()

        # add the elbow and shoulder bulkread parameters (only needs to be done once)
        self.elbow_motor.add_read_param()
        self.shoulder_motor.add_read_param()
        SendRecieveBulk(self.groupread_num, self.groupwrite_num).transmit_read()
        SendRecieveBulk(self.groupread_num, self.groupwrite_num).clear_write_param()

        # Construct the elbow and shoulder camera objects
        self.elbow_camera = Camera("Elbow")
        self.shoulder_camera = Camera("Shoulder")
        time.sleep(4)  # allow time for thread to start
        self.elbow_frame_processing = ImageProcessing("Elbow", self.elbow_camera)
        self.shoulder_frame_processing = ImageProcessing("Shoulder", self.shoulder_camera)
        time.sleep(1)  # allow time for thread to start

        # generate simple joint space trajectories
        if UserVariables.point_to_point == True:
            self.elbow_trajectory_generator = point_to_point()
            self.shoulder_trajectory_generator = point_to_point()
            self.elbow_traj = self.elbow_trajectory_generator.generate_trajectory_elbow(UserVariables.elbow_start, UserVariables.elbow_end, UserVariables.timespan, UserVariables.timespan_home,
                                                                              UserVariables.update_frequency)
            self.shoulder_traj = self.elbow_trajectory_generator.generate_trajectory_shoulder(UserVariables.shoulder_start, UserVariables.shoulder_end, UserVariables.timespan, UserVariables.timespan_home,
                                                                                    UserVariables.update_frequency)
        elif UserVariables.point_to_point == False:
            self.elbow_trajectory_generator = MotionTraj()
            self.shoulder_trajectory_generator = MotionTraj()
            self.elbow_traj = self.elbow_trajectory_generator.elbow()
            self.shoulder_traj = self.shoulder_trajectory_generator.shoulder()
            print(self.elbow_traj)
        else:
            quit("User Variable Error. Check if Point to Point TRUE/FALSE is defined correctly in user variables class.")

        # construct control loop objects
        self.elbow_positioning_control = control_system("Elbow", self.elbow_frame_processing)  # passing in the disable controller flag
        self.shoulder_positioning_control = control_system("Shoulder", self.shoulder_frame_processing)

        # run the robot graphics on screen in real time to see where robot should be.
        self.robot_graphics = Graphics(0.15, 1)  # ideal robot opacity, real robot opacity

        # start the gamecontroller object
        # joystick = gamecontroller_class.XboxController()
        self.run()
        return None

    def run(self):
        print("Running Main...")
        breakloop = False
        globals.cycle_start_flag = 0  # reset cycle start flag to avoid unintentional activation.
        while True:
            print("Press CYCLE START to run.")
            #if estop has been reset and cycle start is on, then run
            if globals.cycle_start_flag == 1 and globals.reset_flag == 0 and globals.estop_flag == 0: #loop forever until the cycle start signal is given by the user. This will initiate the trajectory to run.
                index = 0
                self.elbow_motor.enable_motor()#enable the motors
                self.shoulder_motor.enable_motor()
                time.sleep(0.1)

                while index < self.elbow_trajectory_generator.datapoints:

                    if globals.estop_flag == 1:  #If estop is pressed, break out
                        globals.cycle_start_flag = 0
                        globals.feedhold_flag = 0
                        globals.reset_flag = 0
                        self.elbow_motor.disable_motor()  # disable the motors
                        self.shoulder_motor.disable_motor()
                        robot_gui.TProgressbar1.configure(value=0)  # update the progress bar on the gui
                        #breakloop = True
                        break

                    elif globals.reset_flag == 1: #If reset is pressed, break out but keep motors active
                        globals.cycle_start_flag = 0
                        globals.feedhold_flag = 0
                        robot_gui.TProgressbar1.configure(value=0)  # update the progress bar on the gui
                        #globals.reset_flag = 0
                        #breakloop = True
                        break

                    elif globals.feedhold_flag == 1: #If feedhold is pressed, stop the motion until cycle start is pressed
                        globals.cycle_start_flag = 0
                        while globals.feedhold_flag == 1:
                            if globals.cycle_start_flag == 1:
                                globals.feedhold_flag = 0 #reset the feedhold flag
                                break


                    # Quick shutdown without waiting for motion to finish
                    if globals.shutdown_flag == 1:
                        break

                    # while globals.feedhold_flag == 1:
                    #     #return_reset = self.check_changes()  # Check variables for changes from gui
                    #
                    #
                    #
                    #
                    #
                    #     if (globals.estop_flag == 1) and (globals.reset_flag):
                    #         robot_gui.TProgressbar1.configure(value=0)  # update the progress bar on the gui
                    #
                    #
                    #     if return_reset == 1:  # if the estop and the reset has been pressed, stop execution and wait for go signal.
                    #         robot_gui.TProgressbar1.configure(value=0)  # update the progress bar on the gui
                    #         break
                    #
                    #     # Quick shutdown without waiting for motion to finish
                    #     if globals.shutdown_flag == 1:
                    #         break
                    #     time.sleep(0)


                    # return_reset = self.check_changes()# Check variables for changes from gui
                    # if return_reset == 1: #if the estop and the reset has been pressed, stop execution and wait for go signal.
                    #     robot_gui.TProgressbar1.configure(value=0)  # update the progress bar on the gui
                    #     break




                    SendRecieveBulk(self.groupread_num, self.groupwrite_num).transmit_read()  # Request for new data

                    self.elbow_motor.read_motor_encoder() #read encoder
                    self.shoulder_motor.read_motor_encoder() #read encoder

                    self.elbow_frame_processing.record_deflection()  # record the deflection to the vector
                    self.shoulder_frame_processing.record_deflection() #record the deflection to the vector

                    if UserVariables.motor_method == "torque":
                        self.elbow_positioning_control.joint_torque_calculator(self.elbow_traj, index, self.elbow_motor, self.elbow_frame_processing)  # calculate new motor torques
                        self.shoulder_positioning_control.joint_torque_calculator(self.shoulder_traj, index, self.shoulder_motor, self.shoulder_frame_processing)  # calculate new motor torques. Inputs of position are vectors of recorded past positions.

                        self.elbow_motor.move_torque(int(self.elbow_positioning_control.joint_torque))
                        self.shoulder_motor.move_torque(int(self.shoulder_positioning_control.joint_torque))

                    elif UserVariables.motor_method == "position":
                        self.elbow_positioning_control.joint_position_calculator(self.elbow_traj, index, self.elbow_motor, self.elbow_frame_processing)  # calculate new motor torques
                        self.shoulder_positioning_control.joint_position_calculator(self.shoulder_traj, index, self.shoulder_motor, self.shoulder_frame_processing)  # calculate new motor torques. Inputs of position are vectors of recorded past positions.

                        self.elbow_motor.move_position(int(self.elbow_positioning_control.joint_position))
                        self.shoulder_motor.move_position(int(self.shoulder_positioning_control.joint_position))

                    elif UserVariables.motor_method == "velocity":
                        self.elbow_positioning_control.joint_velocity_calculator(self.elbow_traj, index, self.elbow_motor, self.elbow_frame_processing)  # calculate new motor torques
                        self.shoulder_positioning_control.joint_velocity_calculator(self.shoulder_traj, index, self.shoulder_motor, self.shoulder_frame_processing)  # calculate new motor torques. Inputs of position are vectors of recorded past positions.

                        self.elbow_motor.move_velocity(int(self.elbow_positioning_control.joint_velocity))
                        self.shoulder_motor.move_velocity(int(self.shoulder_positioning_control.joint_velocity))

                    SendRecieveBulk(self.groupread_num, self.groupwrite_num).transmit_write() #TxRx write new currents
                    SendRecieveBulk(self.groupread_num, self.groupwrite_num).clear_write_param() #Clear the param

                    self.robot_graphics.elbowideal = np.radians(self.elbow_traj[index]+180)
                    self.robot_graphics.shoulderideal = np.radians(self.shoulder_traj[index]-180)

                    self.robot_graphics.elbowreal = np.radians(self.elbow_motor.record_data.position_data[-1] + 180)
                    self.robot_graphics.shoulderreal = np.radians(self.shoulder_motor.record_data.position_data[-1] - 180)


                    percent_complete = index/len(self.elbow_traj) * 100
                    robot_gui.TProgressbar1.configure(value=percent_complete) #update the progress bar on the gui




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
            self.elbow_motor.disable_motor()
            self.shoulder_motor.disable_motor()
            globals.cycle_start_flag = 0  # reset cycle start flag.

            while True:
                #cycle start button monitoring
                if globals.cycle_start_flag == 1:
                    globals.reset_flag = 0
                    time.sleep(0.1)
                    break

                #Shutdown flag monitoring
                if globals.shutdown_flag == 1:
                    breakloop = True
                    break

            if breakloop == True:
                print("Quitting!")
                break  #break the main loop.
            print("running loop")

        #Close serial port
        self.handler.close_port()

        # write_csv(self.elbow_motor, self.shoulder_motor, self.elbow_frame_processing, self.shoulder_frame_processing, self.elbow_traj, self.shoulder_traj) #write the recorded various data to CSV files for MATLAB to use in the system identification tool.
        #
        # overshoot_elbow = PerformanceMetrics(self.elbow_motor, self.elbow_frame_processing, self.elbow_traj).overshoot_percentage() #calculate the overshoot percentage
        # overshoot_shoulder = PerformanceMetrics(self.shoulder_motor, self.shoulder_frame_processing, self.shoulder_traj).overshoot_percentage()
        #
        # print("Elbow Maximum Overshoot during run","{x:.2f}".format(x=overshoot_elbow*100),"%")
        # print("Shoulder Maximum Overshoot during run","{x:.2f}".format(x=overshoot_shoulder*100),"%")
        #
        # plots = PlotData()
        # plots.joint(self.elbow_motor, self.elbow_positioning_control, self.elbow_traj, "Elbow")  #plot the joint data
        # plots.joint(self.shoulder_motor, self.shoulder_positioning_control, self.shoulder_traj, "Shoulder")
        #
        # plots.link(self.elbow_frame_processing, self.elbow_positioning_control, self.elbow_traj, "Lower Arm")  #plot the link data
        # plots.link(self.shoulder_frame_processing, self.shoulder_positioning_control, self.shoulder_traj,"Upper Arm")
        #
        # plots.true_position(self.elbow_motor, self.elbow_positioning_control, self.elbow_frame_processing, self.elbow_traj, "Lower Arm")
        # plots.true_position(self.shoulder_motor, self.shoulder_positioning_control, self.shoulder_frame_processing, self.shoulder_traj, "Upper Arm")

        total_shutdown()
        #global stop_threads
        #stop_threads = True
        #t1.join()
        #print('thread killed')
        #return

    def check_changes(self):
        # global globals.estop_flag
        if globals.estop_flag == 1:
            self.elbow_motor.disable_motor()
            self.shoulder_motor.disable_motor()
            time.sleep(0.1)
            estop()
            return 1
        return 0

def estop():
    print("ESTOP!")
    while True: #Check if reset button has been pressed
        if globals.estop_flag == 0:
            reset_estop()
            break

def reset_estop():
    print("RESET")

def total_shutdown():
    global stop_threads

    print("Shutting down...")
    root.destroy()
    #stop_threads = True
    #t1.join()
    #print('thread killed')
    #quit("Exit.")

if __name__ == "__main__":
    global root, robot_gui, stop_threads
    root = tk.Tk()
    stop_threads = False
    t1 = threading.Thread(target=MainClass, args=[], daemon=True)
    t1.start()
    robot_gui = GUI(root)
    root.mainloop()
    sys.exit()

