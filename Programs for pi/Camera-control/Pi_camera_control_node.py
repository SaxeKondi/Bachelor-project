#!/usr/bin/env python3
  
import rospy
# in this example we try to obtain linear
# and angular velocity related information.
# So we import Twist
from geometry_msgs.msg import Twist
import ServoControl

horizontalControlPin = 16
verticalControlPin = 26

horizontalController = ServoControl.ServoController(horizontalControlPin, defaultAngle = 42, maxAngle = 146)
verticalController = ServoControl.ServoController(verticalControlPin, defaultAngle = 5)
  
class basic_subscriber:
  
    def __init__(self):
        # initialize the subscriber node now.
        self.image_sub = rospy.Subscriber("/CameraControl", Twist, self.cameraControlSub)
  
    def cameraControlSub(self, msg):
        horizontalController.changeAngle(round(msg.linear.x))
        verticalController.changeAngle(round(msg.linear.y))
  
  
def main():
    # create a subscriber instance
    sub = basic_subscriber()
      
    # initializing the subscriber node
    rospy.init_node('CameraControl', anonymous=True)
    rospy.spin()
  
if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
