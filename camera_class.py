import cv2
import depthai as dai

from user_variables import *

print(dai.__version__)
import numpy as np
import time
from time import perf_counter
import threading
from record_data_class import *
from record_data_class import *

class Camera(object):

    def __init__(self,camera_selection):
        self.ID = None
        self.camera_selection = camera_selection
        self.frame = None
        self.pipeline = None
        self.resolution = None
        self.ISO = UserVariables.camera_ISO
        self.exposure_time = UserVariables.camera_exposure
        self.device_info = None
        self.camera_queue = None
        self.shoulder_ID = "184430101101A51200"
        self.elbow_ID = "1844301071C8A01200"
        self.list_cameras()
        self.check_exists()  # Check if selected camera exists

        t1 = threading.Thread(target=self.create_mono_camera, args=[], daemon=True)
        t1.start()

    def list_cameras(self):
        # Finding the IDs of all connected cameras
        cameras = [] #initialise
        for device in dai.Device.getAllAvailableDevices():
            cameras.append(device.getMxId())
        print("Attached Camera IDs: " + str(cameras))

        return cameras

    def check_exists(self): #elbow or shoulder
        #Set Camera ID when given input as Shoulder or Elbow
        if self.camera_selection == "Shoulder":
            self.ID = self.shoulder_ID
        elif self.camera_selection == "Elbow":
            self.ID = self.elbow_ID
        else:
            self.camera_selection = "Unknown Camera ID."
        #Check if specified camera can be found, and return error if not found.
        found, self.device_info = dai.Device.getDeviceByMxId(self.ID)
        if found and self.camera_selection == "Shoulder":
            print("Shoulder Camera Found!")
        if found and self.camera_selection == "Elbow":
            print("Elbow Camera Found!")
        if not found:
            raise RuntimeError(self.camera_selection + " Camera not found!")

        return None

    #dai.MonoCameraProperties.SensorResolution =

    def create_mono_camera(self):
        self.pipeline = dai.Pipeline()# Create pipeline
        mono = self.pipeline.createMonoCamera()
        #mono.setResolution((640,480))
        #mono.setResolution(dai.MonoCameraProperties.SensorResolution(240))
        #mono.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
        mono.setResolution(dai.MonoCameraProperties.SensorResolution.THE_480_P)
        print("Old FPS: " + str(mono.getFps()))
        mono.setFps(99)#Max 117 at 400px. 99 for 480px frame width.
        print("New FPS: " + str(mono.getFps()))
        #mono.setVideoSize(20, 150)
        mono.setBoardSocket(dai.CameraBoardSocket.LEFT)

        xout = self.pipeline.createXLinkOut()
        xout.input.setQueueSize(1)
        xout.input.setBlocking(False)
        xout.setStreamName("left")

        mono.out.link(xout.input)
        controlIn = self.pipeline.createXLinkIn()
        controlIn.setStreamName('control')
        controlIn.out.link(mono.inputControl)

        camera = dai.Device(self.pipeline, self.device_info)
        self.camera_queue = camera.getOutputQueue(name="left", maxSize=1, blocking=False)
        camera_control_Queue = camera.getInputQueue(controlIn.getStreamName())
        camera_ctrl = dai.CameraControl()
        camera_ctrl.setManualExposure(self.exposure_time, self.ISO)
        camera_control_Queue.send(camera_ctrl)
        index = 1
        cumulative_time = 0
        while True:
            times = perf_counter()
            frame = self.camera_queue.get()  # get frame
            frame = frame.getCvFrame()
            self.frame = np.rot90(frame, k=3, axes=(1, 0))
            time.sleep(0)#yield


