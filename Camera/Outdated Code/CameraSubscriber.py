#!/usr/bin/env python
  
import rospy
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge
import cv2
import os
import numpy as np

class cameraSubscriber:
    def __init__(self):
        # Params
        self.image = None

        self.br = CvBridge()

        # rospy.Subscriber('/cam_feed',Image,self.callback)
        rospy.Subscriber('/USCamera',CompressedImage,self.callback)



    def callback(self, msg):
        # self.image = self.br.imgmsg_to_cv2(msg)
        self.image = self.br.compressed_imgmsg_to_cv2(msg)



    def start(self):
        while not rospy.is_shutdown():

            if self.image is not None:
                # self.image = cv2.resize(self.image, (720,576))
                cv2.imshow("cam_feed", self.image)

            if cv2.waitKey(1) == ord('q'):
                #exit while loop
                break
            # self.loop_rate.sleep()

  
def main():
    rospy.init_node('CameraSub', anonymous=True)

    subscriber = cameraSubscriber()
      
    subscriber.start()
    
  
if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
