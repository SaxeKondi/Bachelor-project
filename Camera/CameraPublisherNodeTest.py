#!/usr/bin/env python
  
import rospy
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge
import cv2
import os
import numpy as np

class cameraPublisher:
    def __init__(self):
        # Params
        self.image = None
        self.cap = cv2.VideoCapture(0)
        self.pixelWidth = 1920
        self.pixelHeight = 1080

        #sets the resolution
        self.cap.set(3,self.pixelWidth)
        self.cap.set(4,self.pixelHeight)

        self.br = CvBridge()
        # Node cycle rate (in Hz).
        self.loop_rate = rospy.Rate(30)

        # Publishers
        self.pubComp = rospy.Publisher('cam_feed_comp', CompressedImage, queue_size=10)
        self.pubRaw = rospy.Publisher('cam_feed_raw', Image, queue_size=10)

        # rospy.Subscriber('/cam_feed',Image,self.callback)
        rospy.Subscriber('/cam_feed_comp',CompressedImage,self.callback)



    def callback(self, msg):
        # self.image = self.br.imgmsg_to_cv2(msg)
        self.image = self.br.compressed_imgmsg_to_cv2(msg)



    def start(self):
        while not rospy.is_shutdown():
            _, img = self.cap.read()

            if self.image is not None:
                # self.image = cv2.resize(self.image, (720,576))
                cv2.imshow("cam_feed", self.image)

            if img is not None:
                img = cv2.resize(img, (720,576))
                self.pubRaw.publish(self.br.cv2_to_imgmsg(img))
                self.pubComp.publish(self.br.cv2_to_compressed_imgmsg(img))

            if cv2.waitKey(1) == ord('q'):
                #exit while loop
                break
            # self.loop_rate.sleep()

  
def main():
    rospy.init_node('Camera', anonymous=True)

    publisher = cameraPublisher()
      
    publisher.start()
    
  
if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
