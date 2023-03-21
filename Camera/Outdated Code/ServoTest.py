import cv2
import ServoControl

angle = 0
print("starting pwm mode")
pwm = ServoControl.ServoController()


while(1):

    if cv2.waitKey(1) == ord('a'):
        print("Input change in angle: ")
        angle = int(input())
        pwm.changeAngle(angle)
        print(f'Angle is currently {pwm.currentAngle} degrees')

    if cv2.waitKey(1) == ord('t'):
        print("Input target angle: ")
        angle = int(input())
        pwm.setTargetAngle(angle)
        print(f'Angle is currently {pwm.currentAngle} degrees')

    if cv2.waitKey(1) == ord('q'):
        break
    
        

        