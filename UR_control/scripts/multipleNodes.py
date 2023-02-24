#!/usr/bin/env python3

from tkinter import Y
import rtde_receive
from std_msgs.msg import String
import rospy
import numpy as np
from geometry_msgs.msg import Point, Quaternion, Pose, Twist, Vector3

from etherdaq import EtherDAQ
import time
import threading

class Receptor():

    def joints(self): 

        joints_vector = self.receiver_UR.getActualQ()
        rad2grad = 180/3.141592
        x = []
        for joint in joints_vector: 
            x.append(joint * rad2grad)        
        self.joints_msg = str(x)
        self.send_joints_msg_ = True
   

    def TCP_position(self): 

        ef_vector = self.receiver_UR.getActualTCPPose()
        self.x = [ef_vector[0], ef_vector[1], ef_vector[2]]
        self.y = [ef_vector[0], ef_vector[1], ef_vector[2], ef_vector[3], ef_vector[4], ef_vector[5]]

        self.ef = str(self.x)
        self.pose = str(self.y)

    
    def distanceToGoal(self): 

        s_sq_difference = 0
        for p_i,q_i in zip(self.x, self.goal):
            s_sq_difference += (p_i - q_i)**2
        self.distance = s_sq_difference**0.5


    def __init__(self) -> None:
        self.receiver_UR = rtde_receive.RTDEReceiveInterface("192.168.1.105")
        self.ef = ""
        self.pose = ""
        self.distance = 0.0
        self.joints_msg = []
        self.goal  = [-0.251, 0.127, 0.291]  # Center of the phantom

        self.pub_jointsPR = rospy.Publisher("jointsPR", String, queue_size=10) 
        self.pub_ef = rospy.Publisher("end_effector", String, queue_size=10)
        self.pub_dist = rospy.Publisher("distanceToGoal", String, queue_size=10)

        while not rospy.is_shutdown():
            
            self.joints()
            self.pub_jointsPR.publish(self.joints_msg)
           
            self.TCP_position()
            self.pub_ef.publish(self.pose)
           
            self.distanceToGoal()
            self.pub_dist.publish(str(self.distance))

            rate = rospy.Rate(10)
            rate.sleep()

if __name__ == '__main__':
    rospy.init_node('JointsNode', anonymous=False)
    Receptor() 