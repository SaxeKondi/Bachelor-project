import time

class ServoController:
    def __init__(self, controlPin, updateInterval = 10):
        self.controlPin = controlPin
        self.currentAngle = 0
        self.targetAngle = 0
        self.updateInterval = updateInterval
        self.lastUpdated = int(time.time()*1000)

    def setTargetAngle(self, angle):
        self.targetAngle = angle

    def updateAngle(self):
        if(int(time.time()*1000) - self.lastUpdated >= self.updateInterval):
            



