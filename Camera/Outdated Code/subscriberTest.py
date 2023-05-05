
#!/usr/bin/env python
  
import rospy
# in this example we try to obtain linear
# and angular velocity related information.
# So we import Twist
from geometry_msgs.msg import Twist
from std_msgs.msg import Int8
  
  
class basic_subscriber:
  
    def __init__(self):
        # initialize the subscriber node now.
        self.image_sub = rospy.Subscriber("/ZCal", Int8, self.cameraControlSub)
  
    def cameraControlSub(self, msg):
        print(msg.data)
  
  
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
