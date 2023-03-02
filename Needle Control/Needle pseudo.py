#!/usr/bin/env python
import sys
import time
import random
import pigpio
import numpy as np
import rospy
from std_msgs.msg import String, Bool

#pi = pigpio.pi()

controlPin = 12
frequency = 1000
resolution = 1000

#pi.set_PWM_frequency(conrtolPin)

#pi.set_PWM_range(conrtolPin,1000)

#pi.set_PWM_dutycycle(conrtolPin,1)

b = 90
c = 126.155
x1 = 0
x2 = 23
y1 = 0
depth = 20.0
ldepth = depth
min_length = 118
max_length = 168
ratio = (max_length - min_length)/resolution
y2 = -1 - depth
length =  np.sqrt((b**2) + (c**2) - np.cos(np.arctan((y2-y1)/(x2-x1))+ (v * np.pi/180) + (np.pi/2))*2*b*c)-min_length
duty = length/ratio
#pi.set_PWM_dutycycle(conrtolPin,duty)
old_time = rospy.get_time()


def callback(msg):
    curr_time = rospy.get_time()
    if msg.data == True and curr_time - oldetime >= 0.5:
        depth += 0.5
        y2 = -1 - depth
        length =  np.sqrt((b**2) + (c**2) - np.cos(np.arctan((y2-y1)/(x2-x1))+ (v * np.pi/180) + (np.pi/2))*2*b*c)-min_length
        duty = length/ratio
        #pi.set_PWM_dutycycle(conrtolPin,duty)
        old_time = currtime
     
def listener():
    rospy.Subscriber("chatter", Bool, callback)
def talker():
    pub = rospy.Publisher('depth', String)
    if depth != ldepth:
        pub.publish(depth)
        ldepth = depth
        print(depth)
if __name__ == '__main__':
    rospy.init_node('needle', anonymous=True)
    listener()
    talker()
    rospy.spin()



