import cv2
import ServoControl
import ServoControl2

pwmMode = True
running = True
angle = 0
print("starting pwm mode")
pwm = ServoControl2.ServoController()


while(1):
    if(pwmMode):
        pwm.updateAngle()
    else:
        ppm.updateAngle()


    if cv2.waitKey(1) == ord('w'):
        print("starting pwm mode")
        if(running):
            if(not pwmMode):
                del ppm
            else:
                del pwm
        pwm = ServoControl2.ServoController()
        pwm.setTargetAngle(angle)
        pwmMode = True
        running = True

    if cv2.waitKey(1) == ord('p'):
        print("starting ppm mode")
        if(running):
            if(pwmMode):
                del pwm
            else:
                del ppm
        ppm = ServoControl.ServoController()
        ppm.setTargetAngle(angle)
        pwmMode = False
        running = True

    if cv2.waitKey(1) == ord('a'):
        print("Input angle: ")
        angle = int(input())
        if(running):
            if(pwmMode):
                pwm.setTargetAngle(angle)
            else:
                ppm.setTargetAngle(angle)

    if cv2.waitKey(1) == ord('s'):
        if(running):
            print("Stopping")
            if(pwmMode):
                del pwm
            else:
                del ppm
            
            running = False

    if cv2.waitKey(1) == ord('t'):
        break
    
        

        