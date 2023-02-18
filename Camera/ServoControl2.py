import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

class ServoController:
    def __init__(self, controlPin, angle = 0, frequency = 100, updateInterval = 10):
        self.controlPin = controlPin

        self.maxAngle = 180
        self.minAngle = 0

        self.targetAngle = angle
        self.currentAngle = 0

        self.maxPulseWidth = 2550 #given in microseconds
        self.minPulseWidth = 400 #given in microseconds
        self.positivePulseWidth = (self.currentAngle / (self.maxAngle - self.minAngle)) * (self.maxPulseWidth - self.minPulseWidth) + self.minPulseWidth

        self.frequency = 100 #given in Hz
        
        self.dutyCycle = (self.positivePulseWidth / 1000000) / (1 / self.frequency) * 100 #Finds the duty cycle to achieve the desired pulse width given the frequency
        
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
            self.currentAngle += (self.currentAngle - self.targetAngle) / abs((self.currentAngle - self.targetAngle)) #Increments or decrements the current angle by 1
            self.positivePulseWidth = (self.currentAngle / (self.maxAngle - self.minAngle)) * (self.maxPulseWidth - self.minPulseWidth) + self.minPulseWidth #Finds the pulse width needed to achieve the desired angle
            self.dutyCycle = (self.positivePulseWidth / 1000000) / (1 / self.frequency) * 100 #Finds the duty cycle to achieve the desired pulse width given the frequency

            self.pwm.changeFrequency(self.frequency)
            self.pwm.changeDutyCycle(self.dutyCycle)

            self.lastUpdated = int(time.time()*1000)
            


