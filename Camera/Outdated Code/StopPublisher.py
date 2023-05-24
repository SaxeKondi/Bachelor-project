#!/usr/bin/env python
  
import rospy
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge
from std_msgs.msg import String, Bool, Int8
import cv2
import os
import numpy as np

class stopPublisher:
    def __init__(self):
        # Params


        self.loop_rate = rospy.Rate(30)

        # Publishers
        self.pub = rospy.Publisher('/NeedleStop', Int8, queue_size=1)

    def start(self):
        while not rospy.is_shutdown():
            input()
            self.pub.publish(4)

  
def main():
    rospy.init_node('stopper', anonymous=True)

    publisher = stopPublisher()
      
    publisher.start()
    
  
if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
