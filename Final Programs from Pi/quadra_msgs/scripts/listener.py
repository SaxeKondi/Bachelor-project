#!/usr/bin/env python

from __future__ import print_function

import sys
import rospy
from quadra_msgs.msg import *


def callback(data):
    print(data)
    #rospy.loginfo(data)
    
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("quadra_node", ImpedanceSpectrum, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == "__main__": 
    listener()