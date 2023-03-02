#!/usr/bin/env python
import sys
import time
import random
#import pigpio
import numpy as np
import rospy
from std_msgs.msg import String, Bool




class needle:
    #pi = pigpio.pi()
    def __init__(self):
        self.controlPin = 12
        self.frequency = 1000
        self.resolution = 1000

        #pi.set_PWM_frequency(conrtolPin)

        #pi.set_PWM_range(conrtolPin,1000)

        #pi.set_PWM_dutycycle(conrtolPin,1)
        self.v = 10.5
        self.b = 90
        self.c = 126.155
        self.x1 = 0
        self.x2 = 23
        self.y1 = 0
        self.depth = 20.0
        self.ldepth = 19.0
        self.min_length = 118
        self.max_length = 168
        self.ratio = (self.max_length - self.min_length)/self.resolution
        self.y2 = -1 - self.depth
        self.length =  np.sqrt((self.b**2) + (self.c**2) - np.cos(np.arctan((self.y2-self.y1)/(self.x2-self.x1))+ (self.v * np.pi/180) + (np.pi/2))*2*self.b*self.c)-self.min_length
        self.duty = self.length/self.ratio
        #pi.set_PWM_dutycycle(conrtolPin,duty)
        self.old_time = rospy.get_time()
        self.pub = rospy.Publisher('/depth', String, queue_size = 10)
        rospy.Subscriber("/chatter", Bool, self.callback)
    def callback(self, msg):
        self.old_time
        curr_time = rospy.get_time()
        if msg.data == True:
            self.depth += 0.5
            y2 = -1 - self.depth
            self.length =  np.sqrt((self.b**2) + (self.c**2) - np.cos(np.arctan((self.y2-self.y1)/(self.x2-self.x1))+ (self.v * np.pi/180) + (np.pi/2))*2*self.b*self.c)-self.min_length
            self.duty = self.length/self.ratio
            #pi.set_PWM_dutycycle(conrtolPin,duty)
            self.old_time = curr_time
            print_string = str(self.depth)
            self.pub.publish(print_string)
            print(self.depth)
            #rospy.sleep(0.2)
            
        
if __name__ == '__main__':
    rospy.init_node('needle', anonymous=True)
    print("running")
    needle()
    rospy.spin()