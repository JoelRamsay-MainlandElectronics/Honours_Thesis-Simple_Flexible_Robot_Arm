import threading
import time
from user_variables import *
from record_data_class import *
import cv2
import numpy as np

class ImageProcessing(object):

    def __init__(self, identity, camera):
        self.frame = None #initialise the frame that the class will process once grabbed
        self.camera = camera #bring the camera object into this class
        self.identity = identity #Whether the image processing is done on shoulder or elbow images
        self.x = None #centroid position of IR LEDs
        self.y = None
        self.x_home_offset = 0 #initialise
        self.y_home_offset = 0
        self.disable_controller_flag = 0


        if self.identity == "Elbow":    #setting the crop variables based on the shoulder or elbow
            self.x1 = UserVariables.elbow_x1
            self.x2 = UserVariables.elbow_x2
            self.y1 = UserVariables.elbow_y1
            self.y2 = UserVariables.elbow_y2
        elif self.identity == "Shoulder":
            self.x1 = UserVariables.shoulder_x1
            self.x2 = UserVariables.shoulder_x2
            self.y1 = UserVariables.shoulder_y1
            self.y2 = UserVariables.shoulder_y2

        #Create BLOB detector with paramerters.
        self.params = cv2.SimpleBlobDetector_Params()
        # Change thresholds
        self.params.minThreshold = 75
        self.params.maxThreshold = 255

        # Filter by Area.
        self.params.filterByArea = True
        self.params.minArea = 1
        self.detector = cv2.SimpleBlobDetector_create(self.params)

        self.record_data = RecordLinkData() #Construct data recording object

        t1 = threading.Thread(target=self.threading_process, args=[], daemon=True)
        t1.start()

    def get_frame(self):
        frame = self.camera.frame #get frame from camera object
        return frame

    def convert_greyscale(self,frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return frame

    def crop(self, frame):
        frame = frame[int(self.y1):int(self.y1 + self.y2), int(self.x1):int(self.x1 + self.x2)]  #crop the frame
        return frame

    def binary_threshold(self, frame):

        _, frame = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY) #127
        #print(frame)
        return frame

    def detect_if_blank(self, frame):
        #frame = np.zeros([100,100,1],dtype=np.uint8) #Black image for testing
        #frame.fill(0)
        if cv2.countNonZero(frame) == 0:
            self.disable_controller_flag = 1 #Disable the controller.
            #print("Black")
        else:
            self.disable_controller_flag = 0 #Enable the controller
            #print("Not Black")

    def blob_analysis(self, frame):
        # calculate moments for each contour
        M = cv2.moments(frame)

        # calculate x,y coordinate of center
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0

        cv2.circle(frame, (cX, cY), 5, (255, 255, 255), -1)
        text = "Centroid: " + str(cX - self.x_home_offset)
        cv2.putText(frame, text, (cX - 25, cY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        cX = cX * UserVariables.deflection_scaling #rescale from pixels to degrees of deflection
        #cY= cY * UserVariables.deflection_scaling
        return frame, cX

    def getHomePosition(self):
        while (self.x_home_offset == None) or (self.x_home_offset == 0): #Make the we get a non zero initial value.
            frame = self.get_frame()
            frame = self.crop(frame)
            frame = self.binary_threshold(frame)
            _, self.x_home_offset = self.blob_analysis(frame)
            #print("X offset: ", self.x_home_offset, " px", "\tY offset: ", self.y_home_offset, " px")

        return None

    def record_deflection(self):
        self.record_data.position(self.x)  # record a new position datapoint
        self.calculate_velocity(self.record_data.position_data)
        self.calculate_acceleration(self.record_data.position_data)
        return None

    def calculate_acceleration(self, position):
        n = 2  # number of averages
        if len(position) >= n + 4:  # Calculating acceleration (theta double dot)
            acceleration = 0
            for i in range(n):
                dt = 1 / UserVariables.update_frequency
                acceleration = acceleration + ((position[-i - 1] - 2 * (position[-i - 2]) + position[-i - 3]) / (dt ** 2))
                self.acceleration = acceleration / n
        else:
            self.acceleration = 0
        self.record_data.acceleration(self.acceleration)  # record a new position datapoint

    def calculate_velocity(self, position):
        n = 2  # number of averages
        if len(position) >= n + 2:  # Calculating velocity (theta dot)
            velocity = 0  # initialise
            for i in range(n):
                dt = 1 / UserVariables.update_frequency
                velocity = velocity + ((position[-i - 1] - position[-i - 3]) / (2 * dt))
                self.velocity = velocity / n
        else:
            self.velocity = 0
        self.record_data.velocity(self.velocity)


    def threading_process(self):
        self.getHomePosition() #Find the static defleciton under rest.
        while True:
            frame = self.get_frame()
            #frame = self.convert_greyscale(frame) %Convert the frame to grayscale if it is not. The OAK-D Lites already send mono images.
            frame = self.crop(frame)
            frame = self.binary_threshold(frame)
            self.detect_if_blank(frame) #Sets the controller disable flag is there isn't a blob detected (if the image is full black)
            frame, x = self.blob_analysis(frame)
            self.x = x - self.x_home_offset
            self.frame = frame
            time.sleep(0)#yield
