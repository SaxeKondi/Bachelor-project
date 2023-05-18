#!/usr/bin/env python3
  
import rospy
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge
import time
import cv2
import os
import numpy as np

class cameraPublisher:
    def __init__(self):
        # Params
        self.image = None
        self.cap = cv2.VideoCapture(0)

        self.pixelWidth = 640 * 1,4
        self.pixelHeight = 480 * 1,4

        #sets the resolution
        self.cap.set(3,self.pixelWidth)
        self.cap.set(4,self.pixelHeight)

        self.br = CvBridge()
        # Node cycle rate (in Hz).
        self.loop_rate = rospy.Rate(30)

        # Publishers
        self.pub = rospy.Publisher('PiCamera', CompressedImage, queue_size=1)


    def start(self):
        while not rospy.is_shutdown():
            captured, self.image = self.cap.read()

            if captured:
                #self.image = cv2.resize(self.image, (720,576))
                self.pub.publish(self.br.cv2_to_compressed_imgmsg(self.image))

            #cv2.imshow("Video Capture", image)

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