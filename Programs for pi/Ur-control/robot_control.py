#!/usr/bin/env python3
import os
import ast
from tkinter import Y
#from tokenize import String
import rtde_control
import rtde_receive
from std_msgs.msg import String, Bool, Int8
import rospy
import numpy as np
from geometry_msgs.msg import Point, Quaternion, Pose, Twist, Vector3
import ast
# Suscribirme a la info del sensor de presion.
from etherdaq import EtherDAQ
import time
import threading
from kinematics import *
 
class SubNode:
    def __init__(self, controller, receiver):
        self.controller = controller
        self.receiver = receiver

        self.tcpOffset = [(24.9 - 4.4) / 100, 0, (4 + 3.5) / 100]
        self.tcpOffsetRotation = TCPOffsetRotation([np.pi, np.pi / 2, 0])
        controller.setTcp(self.tcpOffset + self.tcpOffsetRotation)

        self.z_forces = []
        self.start_zforce = 0
        self.z_cal = False

        self.z_control = False
        
        self.controll_pos = self.receiver.getActualTCPPose()
        self.baseSpeeds = [0, 0, 0, 0, 0, 0] # [x, y, z, rx, ry, rz]
        self.TCPSpeeds = [0, 0, 0, 0, 0, 0] # [x, y, z, rx, ry, rz]

        self.rotationSlow = 0.05 # rad / s
        self.rotationFast= 0.1 # rad / s

        self.z_speed = 0.05 # m / s
        self.z_admittance_speed = 0.01 # m / s

        self.lastUpdatedRotation = time.time() * 1000
        self.lastUpdatedTranslation = time.time() * 1000

        self.rotating = False

        rospy.Subscriber("/RobotControl", Twist, self.xy_sub)     # Suscribirse a movimiento en el plano XY
        rospy.Subscriber("/ZAxis", Int8, self.z_sub)        # Suscribirse a movimiento en el eje Z
        rospy.Subscriber("/optoSensor", String, self.optoSensor_sub)
        rospy.Subscriber("/ZCal", Int8, self.zCal_sub)
        rospy.Subscriber("/Roll", Int8, self.roll)
        rospy.Subscriber("/Pitch", Int8, self.pitch)
        rospy.Subscriber("/Yaw", Int8, self.yaw)
        rospy.Timer(rospy.Duration(0.045), self.timerCallback)

    def move(self):
        if(self.controller.isConnected() == False):
            self.controller.reconnect()
        
        if (all(v == 0 for v in self.TCPSpeeds)):                      #If the TCP should be stationary
            self.baseSpeeds = [0,0,0,0,0,0]
            self.controller.speedL(self.baseSpeeds, 3)

        elif (not all(v == 0 for v in self.TCPSpeeds[3:6])):               #If the TCP is rotating
            self.rotating = True
            self.baseSpeeds[0:3] = [0,0,0]                                  #Set translation to zero 
            self.controller.speedL(self.baseSpeeds, 1.2)

        elif (all(v == 0 for v in self.TCPSpeeds[3:6])):               #If the TCP should only translate
            if(self.rotating):
                self.controller.speedL([0,0,0,0,0,0], 1.2)
                if self.receiver.isConnected() == False:
                    self.receiver.reconnect()
                self.controll_pos = self.receiver.getActualTCPPose()
                self.rotating = False
                
            else:
                self.baseSpeeds[3:6] = [0,0,0]                              #Set rotation to zero 
                self.controller.speedL(self.baseSpeeds, 1.2)
            


    def xy_sub(self, msg):
        #Max speed set to 0.05 m/s in Android app
        self.lastUpdatedTranslation = time.time() * 1000
        xy_velocities = [msg.linear.x, msg.linear.y, 0, 0, 0, 0] # msg.linear.x, msg.linear.y, msg.linear.z
        self.TCPSpeeds[0] = msg.linear.x
        self.TCPSpeeds[1] = msg.linear.y
        self.baseSpeeds[0:3] = speedTCP_2_base(self.controll_pos[3:6], self.TCPSpeeds[0:3])
        self.move()


    def z_sub(self, msg):
        self.lastUpdatedTranslation = time.time() * 1000
        if msg.data == 2:
            self.TCPSpeeds[2] = self.z_admittance_speed

        elif msg.data == 1:
            self.TCPSpeeds[2] = self.z_speed

        elif msg.data == -1:
            self.TCPSpeeds[2] = -self.z_speed

        elif msg.data == -2:
            self.TCPSpeeds[2] = -self.z_admittance_speed

        elif msg.data == 0:
            self.TCPSpeeds[2] = 0
            
        self.baseSpeeds[0:3] = speedTCP_2_base(self.controll_pos[3:6], self.TCPSpeeds[0:3])
        self.move()

    def optoSensor_sub(self, msg):

        # print(msg)
        z_force = -(ast.literal_eval(msg.data)[1])
        
        if self.z_cal:

            if len(self.z_forces) != 5:
                self.z_forces.append(z_force)
                print(len(self.z_forces))

            elif len(self.z_forces) == 5:

                self.start_zforce = sum(self.z_forces) / len(self.z_forces)
                print(f"Done calibrating z_force: {self.start_zforce}")
                self.z_cal = False

        if self.z_cal == False and len(self.z_forces) == 5:
            if self.start_zforce - z_force >= 5:
                print(self.start_zforce - z_force)
                self.z_control = True
                self.TCPSpeeds[2] = self.z_admittance_speed
                self.baseSpeeds[0:3] = speedTCP_2_base(self.controll_pos[3:6], self.TCPSpeeds[0:3])
                self.move()

            elif self.z_control:
                self.z_control = False
                self.TCPSpeeds[2] = 0
                self.baseSpeeds[0:3] = speedTCP_2_base(self.controll_pos[3:6], self.TCPSpeeds[0:3])
                self.move()


    def zCal_sub(self, msg):
        if msg.data == 0:
            self.z_cal = True  


    def roll(self, msg):
        self.lastUpdatedRotation = time.time() * 1000
        if msg.data == 2:
            self.TCPSpeeds[3] = self.rotationSlow
            
        elif msg.data == 1:
            self.TCPSpeeds[3] = self.rotationFast

        elif msg.data == -1:
            self.TCPSpeeds[3] = -self.rotationFast

        elif msg.data == -2:
            self.TCPSpeeds[3] = -self.rotationSlow

        elif msg.data == 0:
            self.TCPSpeeds[3] = 0

        self.baseSpeeds[3:6] = speedTCP_2_base(self.controll_pos[3:6], self.TCPSpeeds[3:6])
        self.move()

    def pitch(self, msg):
        self.lastUpdatedRotation = time.time() * 1000
        if msg.data == 2:
            self.TCPSpeeds[4] = self.rotationSlow
            
        elif msg.data == 1:
            self.TCPSpeeds[4] = self.rotationFast

        elif msg.data == -1:
            self.TCPSpeeds[4] = -self.rotationFast

        elif msg.data == -2:
            self.TCPSpeeds[4] = -self.rotationSlow

        elif msg.data == 0:
            self.TCPSpeeds[4] = 0

        self.baseSpeeds[3:6] = speedTCP_2_base(self.controll_pos[3:6], self.TCPSpeeds[3:6])
        self.move()


    def yaw(self, msg):
        self.lastUpdatedRotation = time.time() * 1000
        if msg.data == 2:
            self.TCPSpeeds[5] = self.rotationSlow
            
        elif msg.data == 1:
            self.TCPSpeeds[5] = self.rotationFast

        elif msg.data == -1:
            self.TCPSpeeds[5] = -self.rotationFast

        elif msg.data == -2:
            self.TCPSpeeds[5] = -self.rotationSlow

        elif msg.data == 0:
            self.TCPSpeeds[5] = 0

        self.baseSpeeds[3:6] = speedTCP_2_base(self.controll_pos[3:6], self.TCPSpeeds[3:6])
        self.move()

    def timerCallback(self, data):
        if (not all(v == 0 for v in self.TCPSpeeds[0:3])):
            if(time.time() * 1000 - self.lastUpdatedTranslation > 100):
                self.TCPSpeeds[0:3] = [0, 0, 0]
                self.move()
        if (not all(v == 0 for v in self.TCPSpeeds[3:6])):
            if(time.time() * 1000 - self.lastUpdatedRotation > 100):
                self.TCPSpeeds[3:6] = [0, 0, 0]
                self.move()



if __name__ == '__main__':

    try:

        rospy.init_node('RobotControl', anonymous=True)

        robot_ip = '192.168.1.105'

        print("ROBOT starts!")

        SubNode(rtde_control.RTDEControlInterface(robot_ip), rtde_receive.RTDEReceiveInterface(robot_ip))
        
        rospy.spin()

    except rospy.ROSInterruptException:  pass


