from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

cam_res = (1920,1080)
disp_res = (480,360)

camera = PiCamera()
camera.resolution = cam_res
rawCapture = PiRGBArray(camera, size = disp_res)

time.sleep(2)
print("sir")
while True:
    camera.capture(rawCapture, format="bgr", resize = disp_res)
    image = rawCapture.array

    cv2.imshow("Video Capture", image)
    rawCapture.truncate(0)

    #If q is pressed
    if cv2.waitKey(1) == ord('q'):
        #exit while loop
        break
