#!/usr/bin/env python3

from std_msgs.msg import String
import rospy
import ast
import time

measurement = []
timer = time.time() + 60 * 5

def listener():
    rospy.Subscriber("/optoSensor", String, drift_test)

def drift_test(msg):

        #print(msg)
        z_force = ast.literal_eval(msg.data)[2]
        if time.time() < timer:
            measurement.append(z_force)
            print(f'Start: {measurement[0]}')
            print(f'Current measurement: {z_force}')
            print(f'Largest: {max(measurement)}')
            print(f'Smallest: {min(measurement)}')
            print(f'After 5 min: {sum(measurement) / len(measurement)}')
            
        
    
if __name__ == '__main__':
    try:
        rospy.init_node('GetOptoSensorMeasurements', anonymous=True)
        listener()
        rospy.spin()
    except rospy.ROSInterruptException:  pass
