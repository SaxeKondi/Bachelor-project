import cv2

def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

image = None
cap = cv2.VideoCapture(4)  #Might need to be changed depending on which id the ultrasound scanner gets
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

img_counter = 1

while True:
    frameCaptured, image = cap.read()

    if(not frameCaptured):
        break

    #image = image[starty:endy , startx:endx]
    #cv2.line(image, startLinePoint, endLinePoint, (0,0,255), 2)
    cv2.imshow("ultrasound", image)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, image)
        print("{} written!".format(img_name))
        img_counter += 1

cap.release()
cv2.destroyAllWindows()

