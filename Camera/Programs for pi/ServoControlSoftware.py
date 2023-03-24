import time
import pigpio

class ServoController:
    def __init__(self, controlPin, angle, updateInterval = 0):
        self.pi = pigpio.pi()
        self.controlPin = controlPin

        self.maxAngle = 180
        self.minAngle = 0

        self.targetAngle = angle
        self.currentAngle = angle

        self.minPulseWidth = 500 #given in microseconds
        self.maxPulseWidth = self.minPulseWidth + ((2550 - 400) / 200) * 180 #given in microseconds
        
        self.positivePulseWidth = (self.currentAngle / (self.maxAngle - self.minAngle)) * (self.maxPulseWidth - self.minPulseWidth) + self.minPulseWidth
        
        self.updateInterval = updateInterval #Time in millisecons
        self.lastUpdated = int(time.time()*1000)


        self.pi.set_servo_pulsewidth(self.controlPin, self.positivePulseWidth)

    def __del__(self):
        self.pi.set_servo_pulsewidth(self.controlPin, 0)
        self.pi.stop()

    def setTargetAngle(self, angle):
        if(angle > 180):
            self.targetAngle = 180
        elif(angle < 0):
            self.targetAngle = 0
        else:
            self.targetAngle = angle

        self.positivePulseWidth = (self.targetAngle / (self.maxAngle - self.minAngle)) * (self.maxPulseWidth - self.minPulseWidth) + self.minPulseWidth #Finds the pulse width needed to achieve the desired angle
        self.pi.set_servo_pulsewidth(self.controlPin, self.positivePulseWidth)

    def changeAngle(self, value):
        self.targetAngle = self.currentAngle + value

        if(self.targetAngle > 180):
            self.targetAngle = 180
        elif(self.targetAngle < 0):
            self.targetAngle = 0

        if(int(time.time()*1000) - self.lastUpdated >= self.updateInterval):
            self.positivePulseWidth = (self.targetAngle / (self.maxAngle - self.minAngle)) * (self.maxPulseWidth - self.minPulseWidth) + self.minPulseWidth #Finds the pulse width needed to achieve the desired angle
            self.pi.set_servo_pulsewidth(self.controlPin, self.positivePulseWidth)
        
            self.currentAngle = self.targetAngle
            self.lastUpdated = int(time.time()*1000)

        
            


