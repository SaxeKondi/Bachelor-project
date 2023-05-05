import time
import pigpio

pin = 12
frequency = 50


pi = pigpio.pi()

positivePulseWidth = 1467.5

dutyCycle = (positivePulseWidth / 1000000) / (1 / frequency) * 100

pi.set_servo_pulsewidth(16, positivePulseWidth)
pi.set_servo_pulsewidth(26, positivePulseWidth)

pi.hardware_PWM(12, frequency, 500000)
pi.hardware_PWM(13, frequency, 500000)

time.sleep(20)

pi.set_servo_pulsewidth(16, 0)
pi.set_servo_pulsewidth(26, 0)

pi.hardware_PWM(12, frequency, 0)
pi.hardware_PWM(13, frequency, 0)

pi.stop()