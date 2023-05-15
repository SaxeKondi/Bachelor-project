#!/usr/bin/env python3
  
import rospy
from sensor_msgs.msg import Image, CompressedImage
from geometry_msgs.msg import Twist
import os
import numpy as np

class LatencyTester:
    def __init__(self):

        # Publishers
        self.pub = rospy.Publisher('/Latency', Twist, queue_size=1)

        # rospy.Subscriber('/cam_feed',Image,self.callback)
        rospy.Subscriber('/RobotControl', Twist, self.callback)

    def callback(self, msg):
        self.pub.publish(msg)
        print(msg.data)


  
def main():
    rospy.init_node('LatencyTester', anonymous=True)

    publisher = LatencyTester()
      
    rospy.spin()
    
  
if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
