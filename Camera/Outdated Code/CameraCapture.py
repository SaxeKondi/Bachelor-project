import cv2

def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

cap = cv2.VideoCapture(4)
pixelWidth = 720
pixelHeight = 480
cap.set(3,pixelWidth)
cap.set(4,pixelHeight)

while True:
    frameCaptured, frame = cap.read()

    if(not frameCaptured):
        break

    #frame = rescale_frame(img, 50)
    cv2.imshow("Video Capture", frame)

    #If q is pressed
    if cv2.waitKey(1) == ord('q'):
        #exit while loop
        break

cap.release()
cv2.destroyAllWindows()

