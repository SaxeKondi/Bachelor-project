#!/usr/bin/env python3

from std_msgs.msg import String, Int8
import rospy
import ast
import time

measurement_x = []
measurement_y = []
measurement_z = []
timer = time.time() + 60 * 30

def listener():
    rospy.Subscriber("/optoSensor", String, drift_test)
    # rospy.Subscriber("/ZCal", Int8, drift_test)

def drift_test(msg):

        # print(msg.data)
        x_force = ast.literal_eval(msg.data)[0]
        y_force = ast.literal_eval(msg.data)[1]
        z_force = ast.literal_eval(msg.data)[2]
        if time.time() < timer:
            measurement_x.append(x_force)
            measurement_y.append(y_force)
            measurement_z.append(z_force)
            print(f'Start: {measurement_x[0]}')
            print(f'Current measurement: {x_force}')
            print(f'Largest: {max(measurement_x)}')
            print(f'Smallest: {min(measurement_x)}')
            print(f'After 5 min: {sum(measurement_x) / len(measurement_x)}')
            

            print(f'Start: {measurement_y[0]}')
            print(f'Current measurement: {y_force}')
            print(f'Largest: {max(measurement_y)}')
            print(f'Smallest: {min(measurement_y)}')
            print(f'After 5 min: {sum(measurement_y) / len(measurement_y)}')


            print(f'Start: {measurement_z[0]}')
            print(f'Current measurement: {z_force}')
            print(f'Largest: {max(measurement_z)}')
            print(f'Smallest: {min(measurement_z)}')
            print(f'After 5 min: {sum(measurement_z) / len(measurement_z)}')
        
    
if __name__ == '__main__':
    try:
        rospy.init_node('GetOptoSensorMeasurements', anonymous=True)
        listener()
        rospy.spin()
    except rospy.ROSInterruptException:  pass
