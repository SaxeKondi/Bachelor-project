import cv2

def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

image = None
cap = cv2.VideoCapture(0)  #Might need to be changed depending on which id the ultrasound scanner gets
pixelWidth = 720
pixelHeight = 480
startx = int(pixelWidth/15)
endx = int(pixelWidth - pixelWidth/20)
starty = int(pixelHeight/9)
endy = int(pixelHeight - pixelHeight/9)

a = 12.25
b = -2435.75
startLinePoint = (int((0-b)/a),0)
endLinePoint = (int(((endy-starty)-b)/a),(endy-starty))

cap.set(3,pixelWidth)
cap.set(4,pixelHeight)

while True:
    _, image = cap.read()

            

    if image is not None:
        image = image[starty:endy , startx:endx]
        cv2.line(image, startLinePoint, endLinePoint, (0,0,255), 3)
        cv2.imshow("ultrasound", image)
        if cv2.waitKey(1) == ord('q'):
            #exit while loop
            break

cap.release()
cv2.destroyAllWindows()

