import numpy as np
import cv2

def nimic(_x):
    pass

def toggleCheckbox(_x):
    pass


brushThickness = 10
xp, yp = 0, 0

numeFereastra = 'Masca'

cv2.namedWindow(numeFereastra, cv2.WINDOW_AUTOSIZE)

cv2.createTrackbar("lowH", numeFereastra, 90, 179, nimic)
cv2.createTrackbar("highH", numeFereastra, 120, 179, nimic)

cv2.createTrackbar("lowS", numeFereastra, 100, 255, nimic)
cv2.createTrackbar("highS", numeFereastra, 255, 255, nimic)

cv2.createTrackbar("lowV", numeFereastra, 100, 255, nimic)
cv2.createTrackbar("highV", numeFereastra, 255, 255, nimic)

cv2.createTrackbar("Show Contours", numeFereastra, 0, 1, toggleCheckbox)
cv2.createTrackbar("Delete", numeFereastra, 0, 1, toggleCheckbox)

cap = cv2.VideoCapture(0)

_, frame = cap.read()
height, width, _ = frame.shape
imgCanvas = np.zeros((height, width, 3), np.uint8)

while True:
    _ret, frame = cap.read()

    lowH = cv2.getTrackbarPos("lowH", numeFereastra)
    highH = cv2.getTrackbarPos("highH", numeFereastra)
    lowS = cv2.getTrackbarPos("lowS", numeFereastra)
    highS = cv2.getTrackbarPos("highS", numeFereastra)
    lowV = cv2.getTrackbarPos("lowV", numeFereastra)
    highV = cv2.getTrackbarPos("highV", numeFereastra)
    checkbox = cv2.getTrackbarPos("Show Contours", numeFereastra)
    delete = cv2.getTrackbarPos("Delete", numeFereastra)

    formatHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    masca = cv2.inRange(formatHSV, np.array([lowH, lowS, lowV]), np.array([highH, highS, highV]))

    kernel = np.ones((3, 3), np.uint8)
    dilatata = cv2.dilate(masca, kernel, iterations=2)
    erodata = cv2.erode(dilatata, kernel, iterations=2)

    cv2.imshow(numeFereastra, erodata)

    formatHSV1 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    contours, _ = cv2.findContours(masca, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        x, y, w, h = cv2.boundingRect(contours[0])
        center_x = x + w // 2
        center_y = y + h // 2

        if xp == 0 and yp == 0:
            xp, yp = center_x, center_y

        if checkbox:
            cv2.line(imgCanvas, (xp, yp), (center_x, center_y), (0, 0, 255), brushThickness)

        if delete:
            imgCanvas = np.zeros((height, width, 3), np.uint8)

        xp, yp = center_x, center_y

    frame = cv2.addWeighted(frame, 1.0, imgCanvas, 1.0, 0)
    cv2.imshow('Original Frame', frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
cv2.waitKey(1)
