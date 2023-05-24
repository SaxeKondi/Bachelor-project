import time
import pigpio

controlPin = 26
frequency = 50
dutyCycle = 5

positivePulseWidth = 1/frequency * dutyCycle/100 * 1000 #pulsewidth in milliseconds

print(f'The positive pulsewidth is {positivePulseWidth} ms')

pi = pigpio.pi()

pi.set_servo_pulsewidth(controlPin, positivePulseWidth * 1000) #pulsewidth in microseconds

input()

pi.set_servo_pulsewidth(controlPin, 0)
pi.stop()