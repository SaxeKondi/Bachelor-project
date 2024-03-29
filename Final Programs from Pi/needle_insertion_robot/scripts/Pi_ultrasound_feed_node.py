#!/usr/bin/env python3 
import rospy
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge
import cv2
import os
import numpy as np

class ultrasoundPublisher:
    def __init__(self):
        # Params
        self.image = None
        self.cap = cv2.VideoCapture(1)  #Might need to be changed depending on which id the ultrasound scanner gets
        self.pixelWidth = 720
        self.pixelHeight = 480

        self.startx = int(self.pixelWidth/15)
        self.endx = int(self.pixelWidth - self.pixelWidth/20)
        self.starty = int(self.pixelHeight/9)
        self.endy = int(self.pixelHeight - self.pixelHeight/9)
        
        #needle line
        #y = a*x+b
        self.a = 12.25
        self.b = -2435.75
        self.startLinePoint = (int((0-self.b)/self.a),0)
        self.endLinePoint = (int(((self.endy-self.starty)-self.b)/self.a),(self.endy-self.starty))

        #sets the resolution
        self.cap.set(3,self.pixelWidth)
        self.cap.set(4,self.pixelHeight)

        self.br = CvBridge()
        # Node cycle rate (in Hz).
        self.loop_rate = rospy.Rate(14)

        # Publishers
        self.pub = rospy.Publisher('USCamera', CompressedImage, queue_size=1)


    def start(self):
        while not rospy.is_shutdown():
            _, self.image = self.cap.read()

            

            if self.image is not None:
                self.image = self.image[self.starty:self.endy , self.startx:self.endx]
                cv2.line(self.image, self.startLinePoint, self.endLinePoint, (0,0,255), 2)
                # cv2.imshow("ultrasound", self.image)
                # if cv2.waitKey(1) == ord('q'):
                #     #exit while loop
                #     break
                self.pub.publish(self.br.cv2_to_compressed_imgmsg(self.image))

            self.loop_rate.sleep()

  
def main():
    rospy.init_node('Ultrasound', anonymous=True)

    publisher = ultrasoundPublisher()
      
    publisher.start()
    
  
if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
