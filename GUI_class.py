import user_variables
from imports_file import *
from imports_file import tk,sys

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
        self.style.configure('.', font="TkDefaultFont")
        self.style.map('.', background=
        [('selected', _compcolor), ('active', _ana2color)])

        top.geometry("1133x816+440+78")
        top.minsize(120, 1)
        top.maxsize(1924, 2141)
        top.resizable(1, 1)
        top.title("Toplevel 0")
        top.configure(background="#3e3e3e")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        self.top = top
        self.mode = tk.IntVar()
        self.controller = tk.IntVar()

        self.menubar = tk.Menu(top, font="TkMenuFont", bg='#c0c0c0', fg=_fgcolor)
        top.configure(menu=self.menubar)

        self.TProgressbar1 = ttk.Progressbar(self.top)
        self.TProgressbar1.place(relx=0.026, rely=0.784, relwidth=0.177
                                 , relheight=0.0, height=22)
        self.TProgressbar1.configure(length="197")

        self.Label1 = tk.Label(self.top)
        self.Label1.place(relx=0.026, rely=0.735, height=36, width=192)
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
        self.ESTOP.configure(disabledforeground="#a3a3a3")
        self.ESTOP.configure(font="-family {Segoe UI} -size 36 -weight bold")
        self.ESTOP.configure(foreground="#ffffff")
        self.ESTOP.configure(highlightbackground="#d9d9d9")
        self.ESTOP.configure(highlightcolor="black")
        self.ESTOP.configure(pady="0")
        self.ESTOP.configure(text='''ESTOP''')

        self.RESET = tk.Button(self.top)
        self.RESET.place(relx=0.132, rely=0.208, height=34, width=77)
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
        self.CYCLESTART.place(relx=0.018, rely=0.895, height=44, width=87)
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
        self.SHUTDOWN.place(relx=0.035, rely=0.208, height=34, width=87)
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
        self.FEEDHOLD.place(relx=0.124, rely=0.895, height=44, width=87)
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

        self.Frame1 = tk.Frame(self.top)
        self.Frame1.place(relx=0.035, rely=0.282, relheight=0.157
                          , relwidth=0.169)
        self.Frame1.configure(relief='raised')
        self.Frame1.configure(borderwidth="5")
        self.Frame1.configure(relief="raised")
        self.Frame1.configure(background="#d9d9d9")
        self.Frame1.configure(highlightbackground="#d9d9d9")
        self.Frame1.configure(highlightcolor="black")

        self.STATUSMESSAGE = tk.Label(self.Frame1)
        self.STATUSMESSAGE.place(relx=0.052, rely=0.156, height=87, width=170)
        self.STATUSMESSAGE.configure(activebackground="#f9f9f9")
        self.STATUSMESSAGE.configure(activeforeground="black")
        self.STATUSMESSAGE.configure(anchor='nw')
        self.STATUSMESSAGE.configure(background="#000000")
        self.STATUSMESSAGE.configure(compound='left')
        self.STATUSMESSAGE.configure(disabledforeground="#a3a3a3")
        self.STATUSMESSAGE.configure(font="-family {Segoe UI} -size 12 -weight bold")
        self.STATUSMESSAGE.configure(foreground="#00ff00")
        self.STATUSMESSAGE.configure(highlightbackground="#d9d9d9")
        self.STATUSMESSAGE.configure(highlightcolor="black")
        self.STATUSMESSAGE.configure(justify='left')

        self.style.configure('TNotebook.Tab', background=_bgcolor)
        self.style.configure('TNotebook.Tab', foreground=_fgcolor)
        self.style.map('TNotebook.Tab', background=
        [('selected', _compcolor), ('active', _ana2color)])
        self.TNotebook1 = ttk.Notebook(self.top)
        self.TNotebook1.place(relx=0.45, rely=0.355, relheight=0.608
                              , relwidth=0.467)
        self.TNotebook1.configure(takefocus="")
        self.TNotebook1.configure(cursor="fleur")
        self.TNotebook1_t1 = tk.Frame(self.TNotebook1)
        self.TNotebook1.add(self.TNotebook1_t1, padding=3)
        self.TNotebook1.tab(0, text='''Position''', compound="left"
                            , underline='''-1''', )
        self.TNotebook1_t1.configure(background="#d9d9d9")
        self.TNotebook1_t1.configure(highlightbackground="#d9d9d9")
        self.TNotebook1_t1.configure(highlightcolor="black")
        self.TNotebook1_t2 = tk.Frame(self.TNotebook1)
        self.TNotebook1.add(self.TNotebook1_t2, padding=3)
        self.TNotebook1.tab(1, text='''Velocity''', compound="left"
                            , underline='''-1''', )
        self.TNotebook1_t2.configure(background="#d9d9d9")
        self.TNotebook1_t2.configure(highlightbackground="#d9d9d9")
        self.TNotebook1_t2.configure(highlightcolor="black")
        self.TNotebook1_t3 = tk.Frame(self.TNotebook1)
        self.TNotebook1.add(self.TNotebook1_t3, padding=3)
        self.TNotebook1.tab(2, text='''Torque''', compound="left"
                            , underline='''-1''', )
        self.TNotebook1_t3.configure(background="#d9d9d9")
        self.TNotebook1_t3.configure(highlightbackground="#d9d9d9")
        self.TNotebook1_t3.configure(highlightcolor="black")

        self.Label2 = tk.Label(self.TNotebook1_t1)
        self.Label2.place(relx=0.032, rely=0.051, height=70, width=480)
        self.Label2.configure(activebackground="#f9f9f9")
        self.Label2.configure(activeforeground="black")
        self.Label2.configure(anchor='nw')
        self.Label2.configure(background="#ffffff")
        self.Label2.configure(borderwidth="0.5")
        self.Label2.configure(compound='left')
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(highlightbackground="#d9d9d9")
        self.Label2.configure(highlightcolor="black")
        self.Label2.configure(justify='left')
        self.Label2.configure(relief="solid")
        self.Label2.configure(text='''Actuator Control: Position Control (position commands supplied to motor)
    Vibration Control: PID''')
        self.Label2.configure(wraplength="284")

        self.TScale1 = ttk.Scale(self.TNotebook1_t1, from_=0, to=1.0)
        self.TScale1.place(relx=0.438, rely=0.302, relheight=0.174
                           , relwidth=0.333)
        self.TScale1.configure(length="175")
        self.TScale1.configure(takefocus="")

        self.Label3 = tk.Label(self.TNotebook1_t1)
        self.Label3.place(relx=0.057, rely=0.27, height=23, width=114)
        self.Label3.configure(activebackground="#f9f9f9")
        self.Label3.configure(activeforeground="black")
        self.Label3.configure(anchor='w')
        self.Label3.configure(background="#d9d9d9")
        self.Label3.configure(compound='left')
        self.Label3.configure(disabledforeground="#a3a3a3")
        self.Label3.configure(foreground="#000000")
        self.Label3.configure(highlightbackground="#d9d9d9")
        self.Label3.configure(highlightcolor="black")
        self.Label3.configure(text='''Motor Parameters''')

        self.Label3_1 = tk.Label(self.TNotebook1_t1)
        self.Label3_1.place(relx=0.057, rely=0.317, height=23, width=34)
        self.Label3_1.configure(activebackground="#f9f9f9")
        self.Label3_1.configure(activeforeground="black")
        self.Label3_1.configure(anchor='w')
        self.Label3_1.configure(background="#d9d9d9")
        self.Label3_1.configure(compound='left')
        self.Label3_1.configure(disabledforeground="#a3a3a3")
        self.Label3_1.configure(font="-family {Segoe UI} -size 14")
        self.Label3_1.configure(foreground="#000000")
        self.Label3_1.configure(highlightbackground="#d9d9d9")
        self.Label3_1.configure(highlightcolor="black")
        self.Label3_1.configure(text='''Kp''')

        self.Label3_1_1 = tk.Label(self.TNotebook1_t1)
        self.Label3_1_1.place(relx=0.057, rely=0.366, height=23, width=24)
        self.Label3_1_1.configure(activebackground="#f9f9f9")
        self.Label3_1_1.configure(activeforeground="black")
        self.Label3_1_1.configure(anchor='w')
        self.Label3_1_1.configure(background="#d9d9d9")
        self.Label3_1_1.configure(compound='left')
        self.Label3_1_1.configure(disabledforeground="#a3a3a3")
        self.Label3_1_1.configure(font="-family {Segoe UI} -size 14")
        self.Label3_1_1.configure(foreground="#000000")
        self.Label3_1_1.configure(highlightbackground="#d9d9d9")
        self.Label3_1_1.configure(highlightcolor="black")
        self.Label3_1_1.configure(text='''Ki''')

        self.Label3_1_1_1 = tk.Label(self.TNotebook1_t1)
        self.Label3_1_1_1.place(relx=0.057, rely=0.445, height=23, width=24)
        self.Label3_1_1_1.configure(activebackground="#f9f9f9")
        self.Label3_1_1_1.configure(activeforeground="black")
        self.Label3_1_1_1.configure(anchor='w')
        self.Label3_1_1_1.configure(background="#d9d9d9")
        self.Label3_1_1_1.configure(compound='left')
        self.Label3_1_1_1.configure(disabledforeground="#a3a3a3")
        self.Label3_1_1_1.configure(font="-family {Segoe UI} -size 14")
        self.Label3_1_1_1.configure(foreground="#000000")
        self.Label3_1_1_1.configure(highlightbackground="#d9d9d9")
        self.Label3_1_1_1.configure(highlightcolor="black")
        self.Label3_1_1_1.configure(text='''Kd''')

        self.Label2_1 = tk.Label(self.TNotebook1_t2)
        self.Label2_1.place(relx=0.0, rely=0.0, height=1, width=1)
        self.Label2_1.configure(activebackground="#f9f9f9")
        self.Label2_1.configure(activeforeground="black")
        self.Label2_1.configure(anchor='nw')
        self.Label2_1.configure(background="#ffffff")
        self.Label2_1.configure(borderwidth="0.5")
        self.Label2_1.configure(compound='left')
        self.Label2_1.configure(disabledforeground="#a3a3a3")
        self.Label2_1.configure(foreground="#000000")
        self.Label2_1.configure(highlightbackground="#d9d9d9")
        self.Label2_1.configure(highlightcolor="black")
        self.Label2_1.configure(justify='left')
        self.Label2_1.configure(relief="solid")
        self.Label2_1.configure(text='''Actuator Control: Velocity Control (velocity commands supplied to motor)

    Vibration Control: PID''')
        self.Label2_1.configure(wraplength="284")

        self.Label2_1_1 = tk.Label(self.TNotebook1_t3)
        self.Label2_1_1.place(relx=0.0, rely=0.0, height=1, width=1)
        self.Label2_1_1.configure(activebackground="#f9f9f9")
        self.Label2_1_1.configure(activeforeground="black")
        self.Label2_1_1.configure(anchor='nw')
        self.Label2_1_1.configure(background="#ffffff")
        self.Label2_1_1.configure(borderwidth="0.5")
        self.Label2_1_1.configure(compound='left')
        self.Label2_1_1.configure(disabledforeground="#a3a3a3")
        self.Label2_1_1.configure(foreground="#000000")
        self.Label2_1_1.configure(highlightbackground="#d9d9d9")
        self.Label2_1_1.configure(highlightcolor="black")
        self.Label2_1_1.configure(justify='left')
        self.Label2_1_1.configure(relief="solid")
        self.Label2_1_1.configure(text='''Actuator Control: Torque Control (electrical current commands supplied to motor)

    Vibration Control: PID''')
        self.Label2_1_1.configure(wraplength="284")

        self.style.map('TRadiobutton', background=
        [('selected', _bgcolor), ('active', _ana2color)])
        self.POSITION = ttk.Radiobutton(self.top)
        self.POSITION.place(relx=0.441, rely=0.074, relwidth=0.064, relheight=0.0
                            , height=23)
        self.POSITION.configure(variable=self.mode)
        self.POSITION.configure(text='''Position''')
        self.POSITION.configure(compound='left')

        self.VELOCITY = ttk.Radiobutton(self.top)
        self.VELOCITY.place(relx=0.441, rely=0.098, relwidth=0.064, relheight=0.0
                            , height=23)
        self.VELOCITY.configure(variable=self.mode)
        self.VELOCITY.configure(value='2')
        self.VELOCITY.configure(text='''Velocity''')
        self.VELOCITY.configure(compound='left')

        self.TORQUE = ttk.Radiobutton(self.top)
        self.TORQUE.place(relx=0.441, rely=0.123, relwidth=0.064, relheight=0.0
                          , height=23)
        self.TORQUE.configure(variable=self.mode)
        self.TORQUE.configure(value='3')
        self.TORQUE.configure(text='''Torque''')
        self.TORQUE.configure(compound='left')

        self.Label1_1 = tk.Label(self.top)
        self.Label1_1.place(relx=0.507, rely=0.0, height=53, width=394)
        self.Label1_1.configure(activebackground="#f9f9f9")
        self.Label1_1.configure(activeforeground="black")
        self.Label1_1.configure(background="#3e3e3e")
        self.Label1_1.configure(compound='left')
        self.Label1_1.configure(disabledforeground="#a3a3a3")
        self.Label1_1.configure(font="-family {Segoe UI} -size 12")
        self.Label1_1.configure(foreground="#ffffff")
        self.Label1_1.configure(highlightbackground="#d9d9d9")
        self.Label1_1.configure(highlightcolor="black")
        self.Label1_1.configure(text='''Actuator Internal Control Mode''')

        self.style.map('TCheckbutton', background=
        [('selected', _bgcolor), ('active', _ana2color)])
        self.DISABLEVIBRATIONCONTROLLER = ttk.Checkbutton(self.top)
        self.DISABLEVIBRATIONCONTROLLER.place(relx=0.035, rely=0.502
                                              , relwidth=0.162, relheight=0.0, height=30)
        self.DISABLEVIBRATIONCONTROLLER.configure(variable=self.controller)
        self.DISABLEVIBRATIONCONTROLLER.configure(takefocus="")
        self.DISABLEVIBRATIONCONTROLLER.configure(text='''Disable Vibration Controller''')
        self.DISABLEVIBRATIONCONTROLLER.configure(compound='left')
        self.DISABLEVIBRATIONCONTROLLER.configure(cursor="fleur")


        #Set callbacks
        self.ESTOP.configure(command=self.set_estop_flag)
        self.RESET.configure(command=self.reset_flag)
        self.SHUTDOWN.configure(command=self.set_shutdown_flag)
        self.CYCLESTART.configure(command=self.set_cyclestart_flag)
        self.FEEDHOLD.configure(command=self.set_feedhold_flag)

        self.POSITION.configure(command=self.position_selected)
        self.VELOCITY.configure(command=self.velocity_selected)
        self.TORQUE.configure(command=self.torque_selected)

        self.DISABLEVIBRATIONCONTROLLER.configure(command=self.disable_vibration_controller_flag)

        if UserVariables.motor_method == "position":
            self.mode.set(1) #set the radio button to the default (in UserVariables) when starting the program
        elif UserVariables.motor_method == "velocity":
            self.mode.set(2)
        elif UserVariables.motor_method == "torque":
            self.mode.set(3)

    def disable_vibration_controller_flag(self):
        if self.controller.get() == 0:
            print("Vibration Controller Enabled.")
            globals.controller_checkbox_flag = 1 #flag to tell program the checkbox has been adjusted
            UserVariables.disable_controller = False

        elif self.controller.get() == 1:
            print("Vibration Controller Disabled.")
            globals.controller_checkbox_flag = 1
            UserVariables.disable_controller = True

    def position_selected(self):
        globals.mode = "position"
        globals.mode_changed_flag = 1
        print("position mode")

    def velocity_selected(self):
        globals.mode = "velocity"
        globals.mode_changed_flag = 1
        print("Velocity mode")

    def torque_selected(self):
        globals.mode = "torque"
        globals.mode_changed_flag = 1
        print("Torque mode")


    def status_display(self,message):
        self.STATUSMESSAGE.configure(text=message)

    def set_estop_flag(self):
        print("estop")
        globals.estop_flag = 1 #sets the estop flag to 1, so the program turns off the motors and waits until reset and cycle start.
        self.STATUSMESSAGE.configure(text='''Emergency Stop!\nWaiting for RESET''')
        self.STATUSMESSAGE.configure(foreground="#ff0000")
        #self.("Emergency Stop!\nWaiting for RESET.")

    def reset_flag(self):
        print("reset")#sets the estop flag to 1, so the program turns off the motors and waits until reset and cycle start.
        globals.reset_flag = 1
        globals.estop_flag = 0
        self.STATUSMESSAGE.configure(text='''Ready''')
        self.STATUSMESSAGE.configure(foreground="#00ff00")

    def set_shutdown_flag(self):
        print("shutdown")
        globals.shutdown_flag = 1 #sets the estop flag to 1, so the program turns off the motors and quits.
        self.STATUSMESSAGE.configure(text='''Shutting Down...''')
        self.STATUSMESSAGE.configure(foreground="#ff0000")

    def set_cyclestart_flag(self):
        print("cyclestart")
        globals.cycle_start_flag = 1 #sets the estop flag to 1, so the program turns off the motors and quits.


    def set_feedhold_flag(self):
        print("feedhold")
        globals.feedhold_flag = 1 #feedhold while in motion (stays at last position when in position mode)