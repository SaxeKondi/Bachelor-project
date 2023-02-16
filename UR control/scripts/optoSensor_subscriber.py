#!/usr/bin/env python3

from std_msgs.msg import String
import rospy
 
def callback(msg):
    print(msg)

def listener():

    rospy.init_node('GetOptoSensorMeasurements', anonymous=True)
    rospy.Subscriber("optoSensor", String, callback)
    rospy.spin()
    
if __name__ == '__main__':
    try:
        listener()
        rospy.spin()
    except rospy.ROSInterruptException:  pass