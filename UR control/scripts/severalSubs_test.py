#!/usr/bin/env python3

import os
import ast
from tkinter import Y
#from tokenize import String
import rtde_control
from std_msgs.msg import String, Bool
import rospy
import numpy as np
from geometry_msgs.msg import Point, Quaternion, Pose, Twist, Vector3
import ast

# Suscribirme a la info del sensor de presion.
from etherdaq import EtherDAQ
import time
import threading
 
class SubNode:

    def __init__(self, controller):
        self.controller = controller
        self.z_forces = []
        self.start_zforce = -1
        self.z_cal = False
        #self.pub = pub
        rospy.Subscriber("/xyPlane", Twist, self.callback1)     # Suscribirse a movimiento en el plano XY
        rospy.Subscriber("/zAxis", Twist, self.callback2)        # Suscribirse a movimiento en el eje Z
        rospy.Subscriber("/optoSensor", String, self.callback3)
        rospy.Subscriber("/zCal", Bool, self.callback4)
    
    def callback1(self, msg):
        print(msg)
        xy_velocities = [msg.linear.x, msg.linear.y, 0, 0, 0, 0] # msg.linear.x, msg.linear.y, msg.linear.z
        self.controller.speedL(xy_velocities) # los ultimos 3 valores son la orientacion? ESTOY ENVIANDO VELOCIDADES

    def callback2(self, msg):
        print(msg)
        z_velocity = [0, 0, msg.linear.z, 0, 0, 0]
        self.controller.speedL(z_velocity)

    def callback3(self, msg):
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

        self.controller.speedL([0, 0, z_velocity, 0, 0, 0])

    def callback4(self, msg):
        print(msg.data)
        if msg.data == True:
            self.z_cal = True



        

        
         


       
if __name__ == '__main__':
    try:
        #os.system('motion -m')
        rospy.init_node('ReadJoysticks', anonymous=True)
        robot_ip = '192.168.1.105'
        print("ROBOT starts!")
       
        #pub = rospy.Publisher('/endEffector', String, queue_size=10)
        SubNode(rtde_control.RTDEControlInterface(robot_ip))
        #PubNode.talker()
        
        rospy.spin()
    except rospy.ROSInterruptException:  pass


# Quizás sea más coherente tener una clase extra que sea capaz de publicar la informacion
# de las fuerzas medidas por el sensor de presion y también de publicar
# la posición trasladada hasta el visor de la cámara del Efector Final.
# Debo tener esta informacion disponible en topics para jugar con ella
# en la aplicacion de ROS-Mobile-SDU.

# Las callsback se ejecutan cuando alguien las invoque mediante la suscripción a uno de los topics activos.
# Solo puedo tener un nodo asociado a un script. Es decir, si quiero lanzar varios nodos,
# tendré que lanzar varios scripts.

# Ahora bien, este script tiene un nodo que se suscribe 

"""
if __name__ == '__main__':
    etherdaq = EtherDAQ('192.168.1.11')
    etherdaq.set_internal_filter_cutoff_frequency(15)
    etherdaq.set_readout_rate(1000)
    etherdaq.enable_internal_bias()

    etherdaq_thread = threading.Thread(target=etherdaq.run_read_loop)
    etherdaq_thread.start()

    
    try:
        while True:
            print(etherdaq.get_wrench())
            time.sleep(0.2)

    finally:
        etherdaq.stop_loop()
        etherdaq_thread.join()




---------------------------------------------------




>>> x = '[ "A","B","C" , " D"]'
>>> x = ast.literal_eval(x)
>>> x
['A', 'B', 'C', ' D']
>>> x = [n.strip() for n in x]
>>> x
['A', 'B', 'C', 'D']

-------------------------------------------


Como matar un nodo concreto desde una callback en caso de recibir X informacion por un topic concreto:

#!/usr/bin/env python
import os

nodes = os.popen("rosnode list").readlines()
for i in range(len(nodes)):
    nodes[i] = nodes[i].replace("\n","")

for node in nodes:
    os.system("rosnode kill "+ node)


"""

