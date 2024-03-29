import time
import pigpio

class ServoController:
    def __init__(self, controlPin, defaultAngle = 0, updateInterval = 10, maxAngle = 180, minAngle = 0):
        self.pi = pigpio.pi()
        self.controlPin = controlPin

        self.maxRotation = 200
        self.maxAngle = maxAngle
        self.minAngle = minAngle

        self.targetAngle = defaultAngle
        self.currentAngle = defaultAngle

        self.positivePulseRange = [400, 2550]
        self.zeroDegreePulseWidth = 500
        self.minPulseWidth = self.zeroDegreePulseWidth + ((self.positivePulseRange[1] - self.positivePulseRange[0]) / self.maxRotation) * self.minAngle #given in microseconds
        self.maxPulseWidth = self.minPulseWidth + ((self.positivePulseRange[1] - self.positivePulseRange[0]) / self.maxRotation) * (self.maxAngle - self.minAngle) #given in microseconds
        
        self.positivePulseWidth = (self.currentAngle / (self.maxAngle - self.minAngle)) * (self.maxPulseWidth - self.minPulseWidth) + self.minPulseWidth
        
        self.updateInterval = updateInterval #Time in millisecons
        self.lastUpdated = int(time.time()*1000)


        self.pi.set_servo_pulsewidth(self.controlPin, self.positivePulseWidth)

    def __del__(self):
        self.pi.set_servo_pulsewidth(self.controlPin, 0)
        self.pi.stop()

    def setTargetAngle(self, angle):
        if(angle > self.maxAngle):
            self.targetAngle = self.maxAngle
        elif(angle < self.minAngle):
            self.targetAngle = self.minAngle
        else:
            self.targetAngle = angle

        self.positivePulseWidth = (self.targetAngle / (self.maxAngle - self.minAngle)) * (self.maxPulseWidth - self.minPulseWidth) + self.minPulseWidth #Finds the pulse width needed to achieve the desired angle
        self.pi.set_servo_pulsewidth(self.controlPin, self.positivePulseWidth)

    def changeAngle(self, value):
        if(int(time.time()*1000) - self.lastUpdated >= self.updateInterval):
            self.targetAngle = self.currentAngle + value
            if(self.targetAngle > self.maxAngle):
                self.targetAngle = self.maxAngle
            elif(self.targetAngle < self.minAngle):
                self.targetAngle = self.minAngle

            self.positivePulseWidth = ((self.targetAngle - self.minAngle) / (self.maxAngle - self.minAngle)) * (self.maxPulseWidth - self.minPulseWidth) + self.minPulseWidth #Finds the pulse width needed to achieve the desired angle
            self.pi.set_servo_pulsewidth(self.controlPin, self.positivePulseWidth)
        
            self.currentAngle = self.targetAngle
            self.lastUpdated = int(time.time()*1000)

        
            


