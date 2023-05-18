#!/usr/bin/env python3
  
import time
import rospy
from sensor_msgs.msg import Image, CompressedImage
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge
import os
import numpy as np
import cv2

class LatencyTester:
    def __init__(self):

        self.image = None
        self.cap = cv2.VideoCapture(0)
        self.pixelWidth = 640 * 1.4
        self.pixelHeight = 480 * 1.4

        #sets the resolution
        self.cap.set(3,self.pixelWidth)
        self.cap.set(4,self.pixelHeight)

        self.br = CvBridge()
        # Node cycle rate (in Hz).

        # Publishers
        self.pub = rospy.Publisher('/PiCamera', CompressedImage, queue_size=1)
        rospy.Subscriber('/PiCamerapub', CompressedImage, self.callback)

        self.sendTime = 0
        
        self.values = []
        self.ready = True

    def callback(self, msg):
        ping = time.time() * 1000 - self.sendTime
        self.values.append(ping/2)
        self.ready = True

    def run(self):
        input("start test ")
        while(len(self.values) < 50):
            if(self.ready):
                captured, self.image = self.cap.read()
                if(captured):
                    img = self.br.cv2_to_compressed_imgmsg(self.image)
                    self.sendTime = time.time()*1000
                    self.pub.publish(img)
                    self.ready = False
        while(not self.ready):
            pass
        print(self.values)


  
def main():
    rospy.init_node('LatencyTester', anonymous=True)

    publisher = LatencyTester()
      
    publisher.run()
    
  
if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass

