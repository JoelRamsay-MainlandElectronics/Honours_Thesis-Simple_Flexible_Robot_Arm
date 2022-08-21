import time

import roboticstoolbox as rtb
import swift
import numpy as np
import spatialmath as sm
import spatialgeometry as sg
#from gamecontroller_class import *
import threading

class Graphics(object):
    def __init__(self,alphaideal,alphareal):
        self.alphaideal = alphaideal
        self.alphareal = alphareal
        self.shoulderideal = 0
        self.elbowideal = 0
        self.shoulderreal = 0
        self.elbowreal = 0
        #print("in2")
        t1 = threading.Thread(target=self.run, args=[], daemon=True)
        t1.start()
        return None

    def run(self):
        #print("in1")
        #joy = XboxController()
        # create swift instance
        env = swift.Swift()
        env.launch(realtime=True)
        # initialise the robot
        robotideal = rtb.models.EGH400_robot_grey()
        robotreal = rtb.models.EGH400_robot()
        # Add robot to switf
        env.add(robotideal, robot_alpha=self.alphaideal, collision_alpha=0.5)
        env.add(robotreal, robot_alpha=self.alphareal, collision_alpha=0.5)
        # Time step
        dt = 0.01
        while True:
            #self.x = -joy.read()[0]
            #self.y = joy.read()[1]
            robotideal.q = [self.shoulderideal, self.elbowideal]
            robotreal.q = [self.shoulderreal, self.elbowreal]
            env.step(dt)

        # stop the browser tab from closing
        env.hold()
        return None

# graphics = Graphics()
# while True:
#     graphics.elbow = 1
#     graphics.shoulder = 1
#     time.sleep(0)