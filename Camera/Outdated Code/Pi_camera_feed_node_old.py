#!/usr/bin/env python3
  
import rospy
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import os
import numpy as np

class cameraPublisher:
    def __init__(self):
        # Params
        self.image = None

        self.camera = PiCamera()
        self.camRes = (1920, 1080)
        self.camera.resolution = self.camRes
        self.pictureArray = PiRGBArray(self.camera, size = self.camRes)

        self.br = CvBridge()
        # Node cycle rate (in Hz).
        self.loop_rate = rospy.Rate(30)

        # Publishers
        self.pub = rospy.Publisher('camera_feed_compressed', CompressedImage, queue_size=1)


    def start(self):
        while not rospy.is_shutdown():
            self.camera.capture(self.pictureArray, format = "bgr", resize = self.camRes)

            self.image = self.pictureArray.array

            if self.image is not None:
                #self.image = cv2.resize(self.image, (720,576))
                self.pub.publish(self.br.cv2_to_compressed_imgmsg(self.image))

            #cv2.imshow("Video Capture", image)
            self.pictureArray.truncate(0)

            self.loop_rate.sleep()

  
def main():
    rospy.init_node('Camera', anonymous=True)

    publisher = cameraPublisher()
    time.sleep(2) 
    publisher.start()
    
  
if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass