import time
import pigpio
import numpy as np
import rospy

class NeedleController:
    def __init__(self, anglePin = 12, needlePin = 13, frequency = 1500):
        self.pi = pigpio.pi()
        self.anglePin = anglePin
        self.needlePin = needlePin
        self.frequency = frequency
        self.resolution = 1000000
        self.angleDuty = 0
        self.needleDuty = 0

        self.angleServoMinLength = 93.814 + 4.25 #4.25 is the hole diameter
        self.angleServoMaxLength = 141.948 + 4.25 #4.25 is the hole diameter
        self.angleServoLength = self.angleServoMinLength
        self.angleRatio = self.resolution / (self.angleServoMaxLength - self.angleServoMinLength)

        self.needleServoMinLength = 168
        self.needleServoMaxLength = 268
        self.needleServoLength = self.needleServoMinLength
        self.needleRatio = self.resolution / (self.needleServoMaxLength - self.needleServoMinLength)
        self.needelSpeed = 10 #mm/s
        self.needleQuantization = 0.1 #mm

        #Set both of the actuators length to 0
        self.pi.hardware_PWM(self.anglePin, self.frequency, 5000)
        self.pi.hardware_PWM(self.needlePin, self.frequency, 5000)
        time.sleep(2)
        self.pi.hardware_PWM(self.anglePin, self.frequency, self.angleDuty)
        self.pi.hardware_PWM(self.needlePin, self.frequency, self.needleDuty)

        self.depth = 0
        self.v = 8.775 //actual value: 10.643
        self.b = 90
        self.c = 150.765 // actaul value: 151.608
        self.xPivot = 23   //actual value: 28
        self.yPivot = self.depth

        self.inserting = False
        self.stopped = True

    def setDepth(self, depth):
        if(not self.inserting and self.needleServoLength == self.needleServoMinLength):
            self.depth = depth
            self.yPivot = self.depth
            self.angleServoLength = np.sqrt(self.b**2 + self.c**2 - np.cos(np.pi/2 + self.v * np.pi / 180 - np.arctan2(self.yPivot, self.xPivot)) * 2 * self.b * self.c) - self.angleServoMinLength
            self.angleDuty = round(self.angleServoLength * self.angleRatio)
            print(self.angleDuty)
            self.pi.hardware_PWM(self.anglePin, self.frequency, int(self.angleDuty))

    def insertNeedle(self):
        self.inserting = True
        self.stopped = False
        while(self.inserting):
            self.needleServoLength += self.needleQuantization
            if(self.needleServoLength > self.needleServoMaxLength):
                self.needleServoLength = self.needleServoMaxLength
                self.inserting = False
            self.needleDuty = round((self.needleServoLength - self.needleServoMinLength) * self.needleRatio)
            print(self.needleDuty)
            self.pi.hardware_PWM(self.needlePin, self.frequency, int(self.needleDuty))
            rospy.sleep(self.needleQuantization / self.needelSpeed)
        self.stopped = True
    
    def stopInsertion(self):
        self.inserting = False

    def retractNeedle(self):
        self.inserting = False
        print("here")
        while(not self.stopped):
            pass
        print("here2")
        self.needleServoLength = self.needleServoMinLength
        self.needleDuty = round((self.needleServoLength - self.needleServoMinLength)  * self.needleRatio)
        print(self.needleDuty)
        self.pi.hardware_PWM(self.needlePin, self.frequency, int(self.needleDuty))



