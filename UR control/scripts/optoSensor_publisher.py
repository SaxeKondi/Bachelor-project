#!/usr/bin/env python3

from std_msgs.msg import String
from std_msgs.msg import UInt8
import rospy
from etherdaq import EtherDAQ
import time
import threading

def pubData(msg): 
    
    while not rospy.is_shutdown():
        pub.publish(msg)
        rate = rospy.Rate(5)
        rate.sleep()

if __name__ == '__main__':
    etherdaq = EtherDAQ('192.168.1.11')
    etherdaq.set_internal_filter_cutoff_frequency(15)
    etherdaq.set_readout_rate(1000)
    etherdaq.enable_internal_bias()
    etherdaq_thread = threading.Thread(target=etherdaq.run_read_loop)
    etherdaq_thread.start()

    rospy.init_node('OptoSensorMeasurements', anonymous=True)
    pub = rospy.Publisher("/optoSensor", String, queue_size=10)
    pub2 = rospy.Publisher("/warning", UInt8, queue_size=10)

    try:
       
        while not rospy.is_shutdown(): 
         
            time.sleep(0.2) # pequeña espera para tener datos.
            lectura = etherdaq.get_wrench()
            forces = [lectura[0], lectura[1], lectura[2]]
            torques = [lectura[3], lectura[4], lectura[5]]

            print("Forces:" + str(forces))
            #print("Torques:" + str(torques))

            pub.publish(str(forces[2]))
            
            if forces[2] > 8:
                pub2.publish(0)

            elif 6 <= forces[2] <= 8:
                pub2.publish(1)

            elif forces[2] < 6:
                pub2.publish(2)
            
            time.sleep(0.2)

    except rospy.ROSInterruptException:
        etherdaq.stop_loop()
        etherdaq_thread.join()
