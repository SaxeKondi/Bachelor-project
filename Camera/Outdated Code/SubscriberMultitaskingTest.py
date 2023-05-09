#!/usr/bin/env python3
  
import rospy
# in this example we try to obtain linear
# and angular velocity related information.
# So we import Twist
from geometry_msgs.msg import Twist
from std_msgs.msg import Int8
  
  
class basic_subscriber:
  
    def __init__(self):
        # initialize the subscriber node now.
        self.sub1 = rospy.Subscriber("/task1", Twist, self.task1)
        self.sub2 = rospy.Subscriber("/task2", Twist, self.task2)
        self.run = 0
  
    def task1(self, msg):
        if(self.run == 1):
            self.run = 2
        if(self.run == 0):
            self.run = 1
        while self.run == 1:
            print(1)
            print(2)
            print(3)
            print(4)
            print(5)
            print(6)
            print(7)
            print(8)
            print(9)
            print(10)

    def task2(self, msg):
        print("stop")
        self.run = 2
  
  
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
