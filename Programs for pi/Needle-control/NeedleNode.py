#!/usr/bin/env python3
  
import rospy
# in this example we try to obtain linear
# and angular velocity related information.
# So we import Twist
from std_msgs.msg import String, Bool, Int8
import NeedleController

anglePin = 12
needlePin = 13

NeedleControl = NeedleController(anglePin, needlePin)
  
class basic_subscriber:
  
    def __init__(self):
        # initialize the subscriber node now.
        self.image_sub = rospy.Subscriber("/NeedleDepthAngle", string, self.setAngle)
        self.image_sub = rospy.Subscriber("/NeedleAutoStart", Int8, self.insert)
        self.image_sub = rospy.Subscriber("/NeedleRetract", Int8, self.retract)
  
    def setAngle(self, msg):
        depth = float(msg.data)
        if(depth > 10 and depth < 41):
            NeedleControl.setDepth(depth)

    def insert(self, msg):
        NeedleControl.insertNeedle()

    def retract(self, msg):
        NeedleControl.stopInsertion()
  
  
def main():
    # create a subscriber instance
    sub = basic_subscriber()
      
    # initializing the subscriber node
    rospy.init_node('NeedleControl', anonymous=True)
    rospy.spin()
  
if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass

