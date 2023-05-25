import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

class ServoController:
    def __init__(self, controlPin = 12, angle = 0, updateInterval = 10):
        self.controlPin = controlPin

        self.maxAngle = 180
        self.minAngle = 0
        self.maxFrequency = 330
        self.minFrequency = 50

        self.targetAngle = angle
        self.currentAngle = 0

        self.frequency = (self.currentAngle / (self.maxAngle - self.minAngle)) * (self.maxFrequency - self.minFrequency) + self.minFrequency
        self.positivePulseWidth = 1000 #given in microseconds
        self.dutyCycle = (self.positivePulseWidth / 1000000) / (1 / self.frequency) * 100 #Finds the duty cycle to achieve constant positive pulse width no matter the frequency
        
        self.updateInterval = updateInterval #Time in millisecons
        self.lastUpdated = int(time.time()*1000)

        GPIO.setup(self.controlPin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.controlPin, frequency)
        self.pwm.start(self.dutyCycle)

    def __del__(self):
        self.pwm.stop()
        GPIO.cleanup(self.controlPin)

    def setTargetAngle(self, angle):
        if(angle > 180):
            self.targetAngle = 180
        elif(angle < 0):
            self.targetAngle = 0
        else:
            self.targetAngle = angle

    def updateAngle(self):
        if(int(time.time()*1000) - self.lastUpdated >= self.updateInterval):
            if(self.currentAngle != self.targetAngle):
                self.currentAngle += (self.currentAngle - self.targetAngle) / abs((self.currentAngle - self.targetAngle)) #Increments or decrements the current angle by 1
            self.frequency = (self.currentAngle / (self.maxAngle - self.minAngle)) * (self.maxFrequency - self.minFrequency) + self.minFrequency #Finds the frequncy needed to achieve the desired angle
            self.dutyCycle = (self.positivePulseWidth / 1000000) / (1 / self.frequency) * 100 #Finds the duty cycle to achieve constant positive pulse width no matter the frequency

            self.pwm.ChangeFrequency(self.frequency)
            self.pwm.ChangeDutyCycle(self.dutyCycle)

            self.lastUpdated = int(time.time()*1000)
            


