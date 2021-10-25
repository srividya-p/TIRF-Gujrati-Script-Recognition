import cv2
import numpy as np

img = cv2.imread('TNR12-rs.png',0)
kernel = np.ones((5,5),np.uint8)

erosion = cv2.erode(img,kernel,iterations = 1)
dialtion = cv2.dilate(img, kernel, iterations = 1)
opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

cv2.imwrite("./basic/tnr12E.png", erosion)
cv2.imwrite("./basic/tnr12D.png", dialtion)
cv2.imwrite("./basic/tnr12O.png", opening)
cv2.imwrite("./basic/tnr12C.png", closing)
