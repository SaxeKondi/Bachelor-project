import time
import pigpio

controlpin = 12

pi = pygpio.pi()

pi.set_PWM_frequency(controlpin, 1000)

pi.set_PWM_range(controlpin, 100)

pi.set_PWM_dutycycle(controlpin, 0)

time.sleep(10)

pi.set_PWM_dutycycle(controlpin, 100)

time.sleep(10)

pi.stop()
