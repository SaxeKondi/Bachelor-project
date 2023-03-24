#!/usr/bin/env python 
import rospy
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge
import cv2
import os
import numpy as np

class ultrasoundPublisher:
    def __init__(self):
        # Params
        self.image = None
        self.cap = cv2.VideoCapture(4)  #Might need to be changed depending on which id the ultrasound scanner gets
        self.pixelWidth = 720
        self.pixelHeight = 480

        #sets the resolution
        self.cap.set(3,self.pixelWidth)
        self.cap.set(4,self.pixelHeight)

        self.br = CvBridge()
        # Node cycle rate (in Hz).
        self.loop_rate = rospy.Rate(15)

        # Publishers
        self.pub = rospy.Publisher('ultrasound_feed', CompressedImage, queue_size=1)


    def start(self):
        while not rospy.is_shutdown():
            _, self.image = self.cap.read()

            if self.image is not None:
                #self.image = cv2.resize(self.image, (720,576))
                self.pub.publish(self.br.cv2_to_compressed_imgmsg(self.image))

            self.loop_rate.sleep()

  
def main():
    rospy.init_node('Ultrasound', anonymous=True)

    publisher = ultrasoundPublisher()
      
    publisher.start()
    
  
if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
