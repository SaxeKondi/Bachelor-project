import pigpio

pi = pygpio.pi()

pi.set_servo_pulsewidth(12,400)

while(1):
    pass