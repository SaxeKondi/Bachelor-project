#!/usr/bin/env python3
import os
import ast
from tkinter import Y
#from tokenize import String
import rtde_control
from std_msgs.msg import String, Bool
import rospy
import numpy as np
from geometry_msgs.msg import Point, Quaternion, Pose, Twist, Vector3, Int8
import ast
# Suscribirme a la info del sensor de presion.
from etherdaq import EtherDAQ
import time
import threading
 

class SubNode:
    def __init__(self, controller):
        self.controller = controller
        #TCP-offset = 3.5 + 22.4 cm (3.5 = TCP->optoSensor, 24.9 = optoSensor->new_TCP)
        controller.setTcp([0, 0, (24.9 + 3.5) / 100, 0, 0, 0])

        self.z_forces = []
        self.start_zforce = -1
        self.z_cal = False
        
        self.controll_speeds = [0, 0, 0, 0, 0, 0]

        self.rotation_max_speed = 0.1

        rospy.Subscriber("/xyPlane", Twist, self.xy_sub)     # Suscribirse a movimiento en el plano XY
        rospy.Subscriber("/zAxis", Twist, self.z_sub)        # Suscribirse a movimiento en el eje Z
        rospy.Subscriber("/optoSensor", String, self.optoSensor_sub)
        rospy.Subscriber("/zCal", Bool, self.zCal_sub)
        rospy.Subscriber("/Roll", Int8, self.roll)
        rospy.Subscriber("/Pitch", Int8, self.pitch)
        rospy.Subscriber("/Yaw", Int8, self.yaw)

    def move(self):

        self.controller.speedL(self.controll_speeds)

    def xy_sub(self, msg):

        print(msg)
        xy_velocities = [msg.linear.x, msg.linear.y, 0, 0, 0, 0] # msg.linear.x, msg.linear.y, msg.linear.z
        self.controll_speeds[0] = msg.linear.x
        self.controll_speeds[1] = msg.linear.y
        # move()
        self.controller.speedL(xy_velocities) # los ultimos 3 valores son la orientacion? ESTOY ENVIANDO VELOCIDADES

    def z_sub(self, msg):

        print(msg)
        z_velocity = [0, 0, msg.linear.z, 0, 0, 0]
        self.controll_speeds[2] = msg.linear.z
        # move()
        self.controller.speedL(z_velocity)

    def optoSensor_sub(self, msg):

        #print(msg)
        z_velocity = 0
        z_force = ast.literal_eval(msg.data)[2]
        
        if self.z_cal:

            self.start_zforce = -1
            if len(self.z_forces) != 5:
                self.z_forces.append(z_force)
                print(len(self.z_forces))

            elif self.start_zforce == -1:

                self.start_zforce = sum(self.z_forces) / len(self.z_forces)
                print(f"Done calibrating z_force: {self.start_zforce}")
                self.z_cal = False

        if self.start_zforce > 0:
            if self.start_zforce - z_force >= 5:

                z_velocity = 0.01

            elif self.start_zforce - z_force <= -5:

                z_velocity = -0.01

            else:
                z_velocity = 0

        # move()
        self.controller.speedL([self.x_speed, self.y_speed, z_velocity, 0, 0, 0])

    def zCal_sub(self, msg):

        print(msg.data)
        if msg.data == True:
            self.z_cal = True  


    def roll(self, msg):

        print(msg)
        if msg.data == 1:
            self.controll_speeds[3] = self.rotation_max_speed
            # move()
            self.controller.speedL([0, 0, 0, self.rotation_max_speed, 0, 0])

        elif msg.data == -1:
            self.controll_speeds[3] = -self.rotation_max_speed
            # move()
            self.controller.speedL([0, 0, 0, -self.rotation_max_speed, 0, 0])

        elif msg.data == 0:
            self.controll_speeds[3] = 0
            # move()
            self.controller.speedL([0, 0, 0, 0, 0, 0])

        else:
            self.controll_speeds[3] = 0
            # move()
            self.controller.speedL([0, 0, 0, 0, 0, 0])


    def pitch(self, msg):

        print(msg)
        if msg.data == 1:
            self.controll_speeds[4] = self.rotation_max_speed
            # move()
            self.controller.speedL([0, 0, 0, 0, self.rotation_max_speed, 0])

        elif msg.data == -1:
            self.controll_speeds[4] = -self.rotation_max_speed
            # move()
            self.controller.speedL([0, 0, 0, 0, -self.rotation_max_speed, 0])

        elif msg.data == 0:
            self.controll_speeds[4] = 0
            # move()
            self.controller.speedL([0, 0, 0, 0, 0, 0])

        else:
            self.controll_speeds[4] = 0
            # move()
            self.controller.speedL([0, 0, 0, 0, 0, 0])


    def yaw(self, msg):

        print(msg)
        if msg.data == 1:
            self.controll_speeds[5] = self.rotation_max_speed
            # move()
            self.controller.speedL([0, 0, 0, 0, 0, self.rotation_max_speed])

        elif msg.data == -1:
            self.controll_speeds[5] = -self.rotation_max_speed
            # move()
            self.controller.speedL([0, 0, 0, 0, 0, -self.rotation_max_speed])

        elif msg.data == 0:
            self.controll_speeds[5] = 0
            # move()
            self.controller.speedL([0, 0, 0, 0, 0, 0])

        else:
            self.controll_speeds[5] = 0
            # move()
            self.controller.speedL([0, 0, 0, 0, 0, 0]) 

if __name__ == '__main__':

    try:

        #os.system('motion -m')

        rospy.init_node('RobotControl', anonymous=True)

        robot_ip = '192.168.1.105'

        print("ROBOT starts!")
       

        # pub = rospy.Publisher('/endEffector', String, queue_size=10)

        SubNode(rtde_control.RTDEControlInterface(robot_ip))

        #PubNode.talker()
        

        rospy.spin()

    except rospy.ROSInterruptException:  pass


