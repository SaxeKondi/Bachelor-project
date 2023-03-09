import cv2

cap = cv2.VideoCapture(0)
pixelWidth = 1920
pixelHeight = 1080

#sets the resolution
cap.set(3,pixelWidth)
cap.set(4,pixelHeight)

while True:
    _, img = cap.read()
    print(img)

    cv2.imshow("Face Detector", img)

    #If q is pressed
    if cv2.waitKey(1) == ord('q'):
        #exit while loop
        break

cap.release()
cv2.destroyAllWindows()