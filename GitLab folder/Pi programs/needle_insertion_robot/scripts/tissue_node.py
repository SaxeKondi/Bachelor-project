#!/usr/bin/env python3
from statistics import median
import numpy as np
#from copy import deepcopy
from time import sleep
#import tkinter as tk
#from tkinter import messagebox
from matplotlib import pyplot as plt 

# Ros includes
import rospy
from std_msgs.msg import String
from quadra_msgs.msg import ImpedanceSpectrum

''' Measure impedance value '''
def measure_impedance():
    magnt = np.array([])
    phase = np.array([])
    n_sample = 4
    for i in range(n_sample):
        while True:
            try:
                msg = rospy.wait_for_message("/quadra/spectrum",ImpedanceSpectrum, timeout=5)
            except rospy.exceptions:
                continue
            break
        magnt = np.append(magnt, msg.magnitude)
        phase = np.append(phase, msg.phase)
    magnt = np.reshape(magnt, (n_sample, 15))
    phase = np.reshape(phase, (n_sample, 15))
    magnt = np.median(magnt, axis=0)
    phase = np.median(phase, axis=0)
    return magnt, phase




def tissue_idf():
    pub = rospy.Publisher('tissue_type', String, queue_size=10)
    rospy.init_node('tissue', anonymous=True)
    rate = rospy.Rate(200) # 200hz
    while not rospy.is_shutdown():
        # get impedance
        magnt, phase = measure_impedance()
        # value initialization: nothing
        res = "n"
        # check range
        if ((magnt[0] >= 0.003) & (magnt[0] <= 0.3) & (magnt[14] >= 0.003) & (magnt[14] <= 0.3)):
            # skin
            res = "s"
        elif ((magnt[0] >= 4) & (magnt[0] <= 9) & (magnt[14] >= 4) & (magnt[14] <= 9)):
            # fat
            res = "f"
        elif ((magnt[0] >= 40) & (magnt[0] <= 90) & (magnt[14] >= 40) & (magnt[14] <= 90)):
            # muscle
            res = "m"  

        elif ((magnt[0] >= 5000) & (magnt[0] <= 50000) & (magnt[14] >= 3000) & (magnt[14] <= 20000)):
            # muscle
            res = "b" 
        
        pub.publish(res)
        rospy.sleep(0.001)




if __name__ == '__main__':
    try:
        tissue_idf()
    except rospy.ROSInterruptException:
        pass



