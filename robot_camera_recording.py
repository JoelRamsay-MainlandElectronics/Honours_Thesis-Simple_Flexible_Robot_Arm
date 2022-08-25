import cv2
import numpy as np

video = cv2.VideoCapture('vel_disabled.mp4') #create video object
num_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT)) #get number of frames
#print(num_frames)

frame_rate = 50
seconds = 0
minutes = 0
frame_number = int(frame_rate*(minutes*60 + seconds))
time_increment = 1 #seconds. How many seconds to sample the video.
weighted_frame = video.set(cv2.CAP_PROP_POS_MSEC, 0) #get the initial frame
frames_array = []
while True:

    frame_number = int(frame_rate * (minutes * 60 + seconds))
    print(frame_number)
    if frame_number > num_frames:
        break
    video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = video.read()
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("/images/controller_disabled/image"+str(frame_number)+".jpg",image)
    minutes = 0
    seconds = seconds + time_increment
    frames_array.append(frame)

    #weighted_frame = cv2.addWeighted(frame,0.7,weighted_frame,0.5,0)
    # output = frames_array[0]
# weighted_frame = 0
# print("len",len(frames_array))
# for i in range(len(frames_array)):
#     alpha = 1.0 / (i+0.001)
#     beta = 1.0 - alpha
#     weighted_frame = cv2.addWeighted(weighted_frame,1,frames_array[i],1/64,0)
# weighted_frame = 0
# for i in range(len(frames_array)):
#     #alpha = 1/(len(frames_array))
#     alpha = 0.1/len(frames_array)
#     weighted_frame = weighted_frame + frames_array[i]*0.01

# weighted_frame = cv2.addWeighted(frames_array[5],0.5,frames_array[30],0.5,0)
# weighted_frame = cv2.addWeighted(weighted_frame,0.5,frames_array[2],0.5,0)
#weighted_frame = weighted_frame / 100

#weighted_frame.astype(np.uint8)
# cv2.imshow("image", weighted_frame)
# cv2.waitKey(0)
