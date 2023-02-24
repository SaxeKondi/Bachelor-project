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

def distance(): 
    rospy.init_node('DistanceToGoal', anonymous=True)
    pub = rospy.Publisher("dist_test", String, queue_size=10)
    receiver = rtde_receive.RTDEReceiveInterface("192.168.1.105")
    while not rospy.is_shutdown():
        
        ef_vector = receiver.getActualTCPPose()
        ef = [ef_vector[0], ef_vector[1], ef_vector[2]]
        #goal = [0, 0, 0] # base

        """
        radio de seguridad
        
        """
        goal = [0.122, -0.45522, 0.12652] # box Tomar las coordenadas que me interesa


        s_sq_difference = 0
        for p_i,q_i in zip(ef,goal):
            # sum of squared difference between coordinates
            s_sq_difference += (p_i - q_i)**2
            # take sq root of sum of squared difference
        distance = s_sq_difference**0.5
        pub.publish(str(distance))
   
        #pub.publish(str(ef))
        rate = rospy.Rate(10)
        rate.sleep()

if __name__ == '__main__':
       distance()

# Description:
# ROS node which publishes the distance between the end-effector (EF) and any other point (P) of the space.
# This publisher ROS node has to be launched together with the subscriber ROS node associated with the teleoperation.
# With the purpose of having a high efficiency, the Cartesian space coordinates have to belong to an AR marker.

# In order to keep the efficiency of the code as high as possible, the coordinates of the target point should be those of a marker.
# In order to be as efficient as possible...

# Nodo publicador de la distancia entre el EF y otro punto del espacio.
# Este nodo debe ser lanzado a la vez que el nodo asociado a la teleoperación.
# Ahora bien, para que sea útil, las coordenadas objetivo deben ser las de un marker.

# Crear un suscriptor de la posición del EF que juege con ella. Si la Z es menor de 0.20, entonces el nodo que publique
# en el joystick XY debe ignorarse.