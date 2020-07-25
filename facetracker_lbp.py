#!/usr/bin/env python
from picamera.array import PiRGBArray
from picamera import PiCamera
from pantilthat import *
import time
import cv2

# Set frame size
FRAME_W=640
FRAME_H=480

# Initialize camera
camera = PiCamera()
camera.resolution = (FRAME_W, FRAME_H)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(FRAME_W, FRAME_H))
time.sleep(0.1)

# Pan/tilt defaults
cam_pan = 90
cam_tilt = 60
pan(cam_pan-90)
tilt(cam_tilt-90)

# Set up the CascadeClassifier for face tracking
cascPath = '/usr/share/opencv/lbpcascades/lbpcascade_frontalface.xml'
faceCascade = cv2.CascadeClassifier(cascPath)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        image = cv2.flip(image, -1)

        faces = faceCascade.detectMultiScale(image, 1.1, 3, 0, (10,10))

        for(x, y, w, h) in faces:
                cv2.rectangle(image, (x,y), (x+w, y+h), (0,255,0), 2)
                x = x+(w/2)
                y = y+(h/2)
                turn_x = float(x - (FRAME_W/2))
                turn_y = float(y - (FRAME_H/2))
                turn_x /= float(FRAME_W/2)
                turn_y /= float(FRAME_H/2)
                turn_x *= 2.5
                turn_y *= 2.5
                cam_pan += -turn_x
                cam_tilt += turn_y
                print(cam_pan-90, cam_tilt-90)

                cam_pan = max(0,min(180,cam_pan))
                cam_tilt = max(0,min(180,cam_tilt))
                pan(int(cam_pan-90))
                tilt(int(cam_tilt-90))
                break

        cv2.imshow("Frame",image)

        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
                break
