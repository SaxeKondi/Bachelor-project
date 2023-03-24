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
        self.controlPin = 13
        self.frequency = 1000
        self.resolution = 1000

        #pi.set_PWM_frequency(conrtolPin)
        #pi.set_PWM_frequency(conrtolPin2)

        #pi.set_PWM_range(conrtolPin,1000)
        #pi.set_PWM_range(conrtolPin2,1000)

        #pi.set_PWM_dutycycle(conrtolPin,1)
        #pi.set_PWM_dutycycle(conrtolPin2,1)
        self.v = 10.5
        self.b = 90
        self.c = 126.155
        self.x1 = 0
        self.x2 = 23
        self.y1 = 0
        self.depth = 0.0
        #self.ldepth = 19.0
        self.min_length = 97
        self.max_length = 147
        self.ratio = (self.max_length - self.min_length)/self.resolution
        self.y2 = -1 - self.depth
        self.length =  np.sqrt((self.b**2) + (self.c**2) - np.cos(np.arctan((self.y2-self.y1)/(self.x2-self.x1))+ (self.v * np.pi/180) + (np.pi/2))*2*self.b*self.c)-self.min_length
        self.duty = self.length/self.ratio
        self.duty2 = 0.0
        #pi.set_PWM_dutycycle(conrtolPin,duty)
        self.old_time = rospy.get_time()
        self.start = False
        #self.pub = rospy.Publisher('/depth', String, queue_size = 10)
        rospy.Subscriber("/chatter", String, self.callback)
        #rospy.Subscriber("/chatter", Bool, self.callback)
        rospy.Subscriber("/start", Bool, self.callback2)
        rospy.Subscriber("/stop", Bool, self.callback3)
        #rospy.Subscriber("/chatter2", Bool, self.callback4)
    def callback(self, msg):
        #self.old_time
        #curr_time = rospy.get_time()
        self.depth = float(msg.data)
        y2 = -1 - self.depth
        length =  np.sqrt((self.b**2) + (self.c**2) - np.cos(np.arctan((y2-self.y1)/(self.x2-self.x1))+ (self.v * np.pi/180) + (np.pi/2))*2*self.b*self.c)-self.min_length
        self.duty = length/self.ratio
        #pi.set_PWM_dutycycle(conrtolPin,duty)
        #self.old_time = curr_time
        print(self.depth)
        print(self.duty)
        #rospy.sleep(0.2)


    # def callback(self, msg):
    #     #self.old_time
    #     #curr_time = rospy.get_time()
    #     if msg.data == True:
    #         if self.depth <16:
    #             self.depth += 0.5
    #         y2 = -1 - self.depth
    #         length =  np.sqrt((self.b**2) + (self.c**2) - np.cos(np.arctan((y2-self.y1)/(self.x2-self.x1))+ (self.v * np.pi/180) + (np.pi/2))*2*self.b*self.c)-self.min_length
    #         self.duty = length/self.ratio
    #         #pi.set_PWM_dutycycle(conrtolPin,duty)
    #         #self.old_time = curr_time
    #         print_string = str(self.depth)
    #         self.pub.publish(print_string)
    #         print(self.depth)
    #         print(self.duty)
    #         #rospy.sleep(0.2)
    # def callback4(self, msg):
    #     #self.old_time
    #     #curr_time = rospy.get_time()
    #     if msg.data == True:
    #         if self.depth >0:
    #             self.depth -= 0.5
    #         y2 = -1 - self.depth
    #         length =  np.sqrt((self.b**2) + (self.c**2) - np.cos(np.arctan((y2-self.y1)/(self.x2-self.x1))+ (self.v * np.pi/180) + (np.pi/2))*2*self.b*self.c)-self.min_length
    #         self.duty = length/self.ratio
    #         #pi.set_PWM_dutycycle(conrtolPin,duty)
    #         #self.old_time = curr_time
    #         print_string = str(self.depth)
    #         self.pub.publish(print_string)
    #         print(self.depth)
    #         print(self.duty)
    #         #rospy.sleep(0.2)
            
    def callback2(self,msg):
        if msg.data == True:
            self.start = True
        # if self.start == True:
        #     print("sut mig")
        while self.start == True:
            self.duty2 += 1
            print(self.duty2)
            #pi.set_PWM_dutycycle(conrtolPin2,duty2)
            rospy.sleep(1)

    def callback3(self,msg):
        if msg.data == True:
            self.start = False

if __name__ == '__main__':
    rospy.init_node('needle', anonymous=True)
    print("running")
    needle()
    rospy.spin()
