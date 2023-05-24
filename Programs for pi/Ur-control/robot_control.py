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
from scipy.spatial.transform import Rotation as sciRot

def vecLength(vec):
    return np.sqrt(sum(i**2 for i in vec))

def normalizeVec(vec):
    return np.array(vec) / vecLength(vec)

def GiveVecLength(vec, length):
    return normalizeVec(vec) * length

def fixedAngleXYZ_2_RotMat(rx, ry, rz):
    Rx = np.array([[1, 0, 0],
                   [0, np.cos(rx), -np.sin(rx)],
                   [0, np.sin(rx), np.cos(rx)]])

    Ry = np.array([[np.cos(ry), 0, np.sin(ry)],
                   [0, 1, 0],
                   [-np.sin(ry), 0, np.cos(ry)]])

    Rz = np.array([[np.cos(rz), -np.sin(rz), 0],
                   [np.sin(rz), np.cos(rz), 0],
                   [0, 0, 1]])

    rotMat = np.matmul(np.matmul(Rz,Ry),Rx)

    return rotMat

def rotMat_2_FixedAngleXYZ(rotMat):
    x = np.arctan2(rotMat[2,1],rotMat[2,2])
    y = np.arcsin(-rotMat[2,0])
    z = np.arctan2(rotMat[1,0], rotMat[0,0])
    #print([x,y,z])

    return [x,y,z]

def rotVec_2_rotMat(rotVec):
    theta = vecLength(rotVec)
    ux = rotVec[0]/theta
    uy = rotVec[1]/theta
    uz = rotVec[2]/theta

    c = np.cos(theta)
    s = np.sin(theta)
    C = 1-np.cos(theta)

    rotMat = np.array([[ux*ux*C+c, ux*uy*C-uz*s, ux*uz*C+uy*s],
                          [uy*ux*C+uz*s, uy*uy*C+c, uy*uz*C-ux*s],
                          [uz*ux*C-uy*s, uz*uy*C+ux*s, uz*uz*C+c]])

    #print(f'theta: {theta}    u: {[ux, uy, uz]}')

    rotation = sciRot.from_rotvec(rotVec)

    return rotMat

def rotMat_2_rotVec(rotMat):
    rotation = sciRot.from_matrix(rotMat)


    return rotation.as_rotvec().round(10).tolist()
    

def TCPOffsetRotation(rx, ry, rz):

    rotMat = fixedAngleXYZ_2_RotMat(rx, ry, rz)

    rotVec = rotMat_2_rotVec(rotMat)

    return rotVec

def rotateTCP(rotVec, rx, ry, rz):
    Rbase2tcp = rotVec_2_rotMat(rotVec)

    # print(f'base til tcp: {Rbase2tcp}')

    Rtcp2tcpnew = fixedAngleXYZ_2_RotMat(rx, ry, rz)

    # print(f'TCP til new tcp: {Rtcp2tcpnew}')

    R = np.matmul(Rbase2tcp, Rtcp2tcpnew)

    # print(f'Base til new tcp: {R}')

    angles = rotMat_2_FixedAngleXYZ(R)

    return angles

def xySpeedTCP_2_base(rotVec, xySpeed):
    if(xySpeed == [0,0]):
        return [0,0]
    xyzSpeed = [xySpeed[0], xySpeed[1], 0]                  #Make 3D vector so it can be multiplied with rotation matrix
    RBase2TCP = rotVec_2_rotMat(rotVec)                     #Get rotation matrix from base to tcp
    xyzSpeedBase = np.matmul(RBase2TCP, np.array(xyzSpeed))           #Find the speed of the TCP seen from base
    xySpeedBase = xyzSpeedBase[0:2]  
                   #Remove z component of speed as a speed in only xy is desired
    xySpeedBase = GiveVecLength(xySpeedBase, vecLength(xySpeed))   #Give the xy-speed seen from base the desired velocity
    return xySpeedBase

def xyzSpeedTCP_2_base(rotVec, xyzSpeed):
    RBase2TCP = rotVec_2_rotMat(rotVec)                     #Get rotation matrix from base to tcp
    xyzSpeedBase = np.matmul(RBase2TCP, np.array(xyzSpeed))           #Find the speed of the TCP seen from base
    return xyzSpeedBase
 

class SubNode:
    def __init__(self, controller, receiver):
        self.controller = controller
        self.receiver = receiver

        self.tcpOffset = [(24.9 - 4.4) / 100, 0, (4 + 3.5) / 100]
        self.tcpOffsetRotation = TCPOffsetRotation(np.pi, np.pi / 2, 0)
        controller.setTcp(self.tcpOffset + self.tcpOffsetRotation)

        self.z_forces = []
        self.start_zforce = 0
        self.z_cal = False

        self.z_control = False

        self.placeholder = False
        
        self.controll_pos = self.receiver.getActualTCPPose()
        self.controll_speeds = [0, 0, 0, 0, 0, 0] # [x, y, z, rx, ry, rz]

        self.rotation_max_speed = 0.1 # rad / s
        self.z_speed = 0.05 # m / s
        self.z_admittance_speed = 0.01 # m / s

        self.lastUpdated = time.time() * 1000
        self.lastUpdatedRX = time.time() * 1000
        self.lastUpdatedRY = time.time() * 1000
        self.lastUpdatedRZ = time.time() * 1000
        self.movingRX = False
        self.movingRY = False
        self.movingRZ = False

        rospy.Subscriber("/RobotControl", Twist, self.xy_sub)     # Suscribirse a movimiento en el plano XY
        rospy.Subscriber("/ZAxis", Int8, self.z_sub)        # Suscribirse a movimiento en el eje Z
        rospy.Subscriber("/optoSensor", String, self.optoSensor_sub)
        rospy.Subscriber("/ZCal", Int8, self.zCal_sub)
        rospy.Subscriber("/Roll", Int8, self.roll)
        rospy.Subscriber("/Pitch", Int8, self.pitch)
        rospy.Subscriber("/Yaw", Int8, self.yaw)
        rospy.Timer(rospy.Duration(0.045), self.timerCallback)

    def move(self):
        
        self.lastUpdated = time.time() * 1000
        if (all(v == 0 for v in self.controll_speeds) and not self.placeholder):
            self.placeholder = True
            self.controller.speedL(self.controll_speeds, 1.2)
            # time.sleep(0.05)
            self.controller.speedStop(3)
            
        else:
            self.controller.speedL(self.controll_speeds, 1.2)
            self.placeholder = False

        self.controll_pos = self.receiver.getActualTCPPose()
        

    def rotate(self):
        print("start")
        print(self.receiver.getActualTCPSpeed())
        self.controller.moveL(self.controll_pos, 0.05, 1.2, True)

    def stopRotation(self):
        print("stop")
        self.movingRX = False 
        self.movingRY = False 
        self.movingRZ = False
        self.controller.stopL(3)
        self.controll_pos = self.receiver.getActualTCPPose()

        


    def xy_sub(self, msg):

        #print(msg)
        #Max speed set to 0.05 m/s in Android app
        xy_velocities = [msg.linear.x, msg.linear.y, 0, 0, 0, 0] # msg.linear.x, msg.linear.y, msg.linear.z
        self.controll_speeds[0] = msg.linear.x
        self.controll_speeds[1] = msg.linear.y
        self.controll_speeds[2] = 0
        self.controll_speeds[0:3] = xyzSpeedTCP_2_base(self.controll_pos[3:6], self.controll_speeds[0:3])
        self.move()
            # self.controller.speedL(xy_velocities) # los ultimos 3 valores son la orientacion? ESTOY ENVIANDO VELOCIDADES

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
                self.controll_speeds[2] = self.z_admittance_speed
                # self.controller.speedL([self.controll_speeds[0], self.controll_speeds[1], self.controll_speeds[2], self.controll_speeds[3], self.controll_speeds[4], self.controll_speeds[5]])
                self.move()
            elif self.z_control:
                self.z_control = False
                self.controll_speeds[2] = 0
                # self.controller.speedL([self.controll_speeds[0], self.controll_speeds[1], 0, self.controll_speeds[3], self.controll_speeds[4], self.controll_speeds[5]])
                self.move()


    def zCal_sub(self, msg):

        print(msg.data)
        if msg.data == 0:
            self.z_cal = True  


    def roll(self, msg):
        self.lastUpdatedRX = time.time() * 1000
        # print(msg)
        if msg.data == 0:
            self.stopRotation()

        elif(not self.movingRX and not self.movingRY and not self.movingRZ):
            if msg.data == 1:
                self.movingRX = True
                self.controll_pos[3:6] = rotateTCP(self.controll_pos[3:6], np.pi/4, 0, 0)
                self.rotate()

            elif msg.data == -1:
                self.movingRX = True
                self.controll_pos[3:6] = rotateTCP(self.controll_pos[3:6], -np.pi/4, 0, 0)
                self.rotate()


    def pitch(self, msg):
        self.lastUpdatedRY = time.time() * 1000
        # print(msg)
        if msg.data == 0:
            self.stopRotation()

        elif(not self.movingRX and not self.movingRY and not self.movingRZ):
            if msg.data == 1:
                self.movingRY = True
                self.controll_pos[3:6] = rotateTCP(self.controll_pos[3:6], 0, np.pi/4, 0)
                self.rotate()

            elif msg.data == -1:
                self.movingRY = True
                self.controll_pos[3:6] = rotateTCP(self.controll_pos[3:6], 0, -np.pi/4, 0)
                self.rotate()


    def yaw(self, msg):

        self.lastUpdatedRZ = time.time() * 1000
        # print(msg)
        if msg.data == 0:
            self.stopRotation()

        elif(not self.movingRX and not self.movingRY and not self.movingRZ):
            if msg.data == 1:
                self.movingRZ = True
                self.controll_pos[3:6] = rotateTCP(self.controll_pos[3:6], 0, 0, np.pi/4)
                self.rotate()

            elif msg.data == -1:
                self.movingRZ = True
                self.controll_pos[3:6] = rotateTCP(self.controll_pos[3:6], 0, 0, -np.pi/4)
                self.rotate()

    def timerCallback(self, data):
        if (not all(v == 0 for v in self.controll_speeds)):
            if(time.time() * 1000 - self.lastUpdated > 100):
                self.controll_speeds = [0, 0, 0, 0, 0, 0]
                self.move()
        if(self.movingRX and time.time() * 1000 - self.lastUpdatedRX > 100):
            self.stopRotation()
        if(self.movingRY and time.time() * 1000 - self.lastUpdatedRY > 100):
            self.stopRotation()
        if(self.movingRZ and time.time() * 1000 - self.lastUpdatedRZ > 100):
            self.stopRotation()


if __name__ == '__main__':

    try:

        rospy.init_node('RobotControl', anonymous=True)

        robot_ip = '192.168.1.105'

        print("ROBOT starts!")

        SubNode(rtde_control.RTDEControlInterface(robot_ip), rtde_receive.RTDEReceiveInterface(robot_ip))
        
        rospy.spin()

    except rospy.ROSInterruptException:  pass


