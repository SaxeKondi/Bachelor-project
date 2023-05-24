#!/usr/bin/env python3
  
import rospy
# in this example we try to obtain linear
# and angular velocity related information.
# So we import Twist
from std_msgs.msg import String, Bool, Int8
import NeedleControl

anglePin = 12
needlePin = 13

NeedleControl = NeedleControl.NeedleController(anglePin, needlePin)
  
class basic_subscriber:
  
    def __init__(self):
        # initialize the subscriber node now.
        self.image_sub = rospy.Subscriber("/NeedleDepthAngle", String, self.setAngle)
        self.image_sub = rospy.Subscriber("/NeedleAutoStart", Int8, self.insert)
        self.image_sub = rospy.Subscriber("/NeedleRetract", Int8, self.retract)
        self.image_sub = rospy.Subscriber("/NeedleStop", Int8, self.stop)
  
    def setAngle(self, msg):
        depth = float(msg.data)
        if(depth >= 13 and depth <= 40):
            NeedleControl.setDepth(depth)

    def insert(self, msg):
        NeedleControl.insertNeedle()

    def retract(self, msg):
        NeedleControl.retractNeedle()

    def stop(self, msg):
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


