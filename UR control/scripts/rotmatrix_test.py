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
 

class SubNode:
    def __init__(self, controller, receiver):
        self.controller = controller
        self.receiver = receiver
        controller.setTcp([(24.9 - 4.4) / 100, 0, (4 + 3.5) / 100, np.pi, np.pi / 2, 0])
        
        self.controll_speeds = receiver.getActualTCPPose() # [x, y, z, rx, ry, rz]
        self.rot_speed = 0.1
        self.xyz_speed = 0.1

    def move(self):
        self.controller.moveL(self.controll_speeds, 0.05)

    def xy_sub(self, msg):
        self.controll_speeds[0] = msg.linear.x
        self.controll_speeds[1] = msg.linear.y
        if (msg.linear.x == 0 and msg.linear.y == 0):
            self.move()
        else:
            self.move()

    def z_sub(self, msg):

        # print(msg)
        if msg.data == 1:
            self.controll_speeds[2] = self.z_speed
            self.move()
            # self.controller.speedL([0, 0, self.z_speed, 0, 0, 0])

        elif msg.data == -1:
            self.controll_speeds[2] = -self.z_speed
            self.move()
            # self.controller.speedL([0, 0, -self.z_speed, 0, 0, 0])

        elif msg.data == 0:
            self.controll_speeds[2] = 0
            self.move()
            # self.controller.speedL([0, 0, 0, 0, 0, 0], 10)

        else:
            self.controll_speeds[2] = 0
            self.move()
            # self.controller.speedL([0, 0, 0, 0, 0, 0], 10)


    def roll(self, msg):

        # print(msg)
        if msg.data == 1:
            self.controll_speeds[3] = self.rotation_max_speed
            self.move()
            # self.controller.speedL([0, 0, 0, self.controll_speeds[3], 0, 0])

        elif msg.data == -1:
            self.controll_speeds[3] = -self.rotation_max_speed
            self.move()
            # self.controller.speedL([0, 0, 0, self.controll_speeds[3], 0, 0])

        elif msg.data == 0:
            self.controll_speeds[3] = 0
            self.move()
            # self.controller.speedL([0, 0, 0, 0, 0, 0], 10)

        else:
            self.controll_speeds[3] = 0
            self.move()
            # self.controller.speedL([0, 0, 0, 0, 0, 0], 10)


    def pitch(self, msg):

        # print(msg)
        if msg.data == 1:
            self.controll_speeds[4] = self.rotation_max_speed
            self.move()
            # self.controller.speedL([0, 0, 0, 0, self.controll_speeds[4], 0])

        elif msg.data == -1:
            self.controll_speeds[4] = -self.rotation_max_speed
            self.move()
            # self.controller.speedL([0, 0, 0, 0, self.controll_speeds[4], 0])

        elif msg.data == 0:
            self.controll_speeds[4] = 0
            self.move()
            # self.controller.speedL([0, 0, 0, 0, self.controll_speeds[4], 0], 10)

        else:
            self.controll_speeds[4] = 0
            self.move()
            # self.controller.speedL([0, 0, 0, 0, self.controll_speeds[4], 0], 10)


    def yaw(self, msg):

        # print(msg)
        if msg.data == 1:
            self.controll_speeds[5] = self.rotation_max_speed
            self.move()
            # self.controller.speedL([0, 0, 0, 0, 0, self.controll_speeds[5]])

        elif msg.data == -1:
            self.controll_speeds[5] = -self.rotation_max_speed
            self.move()
            # self.controller.speedL([0, 0, 0, 0, 0, self.controll_speeds[5]])

        elif msg.data == 0:
            self.controll_speeds[5] = 0
            self.move()
            # self.controller.speedL([0, 0, 0, 0, 0, self.controll_speeds[5]], 10)

        else:
            self.controll_speeds[5] = 0
            self.move()
            # self.controller.speedL([0, 0, 0, 0, 0, self.controll_speeds[5]], 10) 

    def run(self):
        while(1):
            # print(self.controll_speeds)
            inp = input("input msg here: ")
            if inp == "rx+":
                self.controll_speeds[3] += self.rot_speed
            elif inp == "rx-":
                self.controll_speeds[3] -= self.rot_speed
                
            elif inp == "ry+":
                self.controll_speeds[4] += self.rot_speed
            elif inp == "ry-":
                self.controll_speeds[4] -= self.rot_speed

            elif inp == "rz+":
                self.controll_speeds[5] += self.rot_speed
            elif inp == "rz-":
                self.controll_speeds[5] -= self.rot_speed

            elif inp == "z+":
                self.controll_speeds[2] += self.xyz_speed
            elif inp == "z-":
                self.controll_speeds[2] -= self.xyz_speed

            elif inp == "x+":
                self.controll_speeds[0] += self.xyz_speed
            elif inp == "x-":
                self.controll_speeds[0] -= self.xyz_speed

            elif inp == "y+":
                self.controll_speeds[1] += self.xyz_speed
            elif inp == "y-":
                self.controll_speeds[1] -= self.xyz_speed
            self.move()

                


if __name__ == '__main__':

    try:
        robot_ip = '192.168.1.105'

        print("ROBOT starts!")

        controller = SubNode(rtde_control.RTDEControlInterface(robot_ip), rtde_receive.RTDEReceiveInterface(robot_ip))

        controller.run()
                
            
        
        

    except rospy.ROSInterruptException:  pass


