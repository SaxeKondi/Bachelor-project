import time
import pigpio
import numpy as np

class NeedleController:
    def __init__(self, anglePin = 12, needlePin = 13, frequency = 1500, updateInterval = 0):
        self.pi = pigpio.pi()
        self.anglePin = anglePin
        self.needlePin = needlePin
        self.frequency = frequency
        self.resolution = 1000000
        self.angleDuty = 0
        self.needleDuty = 0

        self.angleServoMinLength = 92.922
        self.angleServoMaxLength = 142.114
        self.angleServoLength = self.angleServoMinLength
        self.angleRatio = self.resolution / (self.angleServoMaxLength - self.angleServoMinLength)

        self.needleServoMinLength = "?"
        self.needleServoMaxLength = "??"
        self.needleServoLength = self.needleServoMinLength
        self.needleRatio = self.resolution / (self.needleServoMaxLength - self.needleServoMinLength)

        #Set both of the actuators length to 0
        self.pi.hardware_PWM(self.anglePin, self.frequency, 5000)
        self.pi.hardware_PWM(self.needlePin, self.frequency, 5000)
        time.sleep(0.1)
        self.pi.hardware_PWM(self.anglePin, self.frequency, self.angleDuty)
        self.pi.hardware_PWM(self.needlePin, self.frequency, self.needleDuty)

        self.depth = 0
        self.v = 8.775
        self.b = 90
        self.xPivot = 23
        self.yPivot = -1 - self.depth #de der -1 giver ikke rigtig mening da det vil gøre at det ikke er en retvinklet trekant og vi derfor ikke kan bruge tangens

        self.inserting = False

    def setDepth(self, depth):
        if(not self.inserting and self.needleServoLength == self.needleServoMinLength):
            self.depth = depth
            self.yPivot = -1 - self.depth #de der -1 giver ikke rigtig mening da det vil gøre at det ikke er en retvinklet trekant og vi derfor ikke kan bruge tangens
            self.angleServoLength = np.sqrt(self.b**2 + self.c**2 - np.cos(np.pi/2 + self.v * pi / 180 - np.arctan2(self.yPivot, self.xPivot)) * 2 * self.b * self.c) - angleServoMinLength
            self.angleDuty = self.angleServoLength * self.angleRatio
            self.pi.hardware_PWM(self.anglePin, self.frequency, self.angleDuty)

    def insertNeedle(self):
        self.inserting = True
        while(self.inserting):
            #mangler lige det her shit, men vi skal lige finde ud af hvor hurtigt nålen bevæger sig
            pass
    
    def stopInsertion(self):
        self.inserting = False

    def retractNeedle(self):
        self.inserting = False
        self.angleServoLength = 0
        self.angleDuty = self.angleServoLength * self.angleRatio
        self.pi.hardware_PWM(self.anglePin, self.frequency, self.angleDuty)



