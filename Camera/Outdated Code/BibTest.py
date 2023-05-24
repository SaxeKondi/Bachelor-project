import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

controlPin = 26
frequency = 50
dutyCycle = 5

positivePulseWidth = 1/frequency * dutyCycle/100 * 1000

print(f'The positive pulsewidth is {positivePulseWidth} ms')

GPIO.setup(controlPin, GPIO.OUT)
pwm = GPIO.PWM(controlPin, frequency)
pwm.start(dutyCycle)

input()

pwm.stop()
GPIO.cleanup(controlPin)
