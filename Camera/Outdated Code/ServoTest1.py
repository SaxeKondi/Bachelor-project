from gpiozero import Servo
import math
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory()

servo = Servo(12, min_pulse_width=0.400/1000, max_pulse_width=2.500/1000, pin_factory=factory)

servo.value = 1
while True:
    pass

