import cv2
import numpy as np

img = cv2.imread('TNR18.png',0)

#3 X 3 WHITE CROSS
kernel = np.array([[0,1,0],
                   [1,1,1],
                   [0,1,0]], np.uint8)

erosion = cv2.erode(img,kernel,iterations = 1)
dialtion = cv2.dilate(img, kernel, iterations = 1)

cv2.imwrite("./kernel-ops-18/3x3_white_cross_E.png", erosion)
cv2.imwrite("./kernel-ops-18/3x3_white_cross_D.png", dialtion)

#3 X 3 BLACK CROSS
kernel = np.array([[1,0,1],
                   [0,0,0],
                   [1,0,1]], np.uint8)

erosion = cv2.erode(img,kernel,iterations = 1)
dialtion = cv2.dilate(img, kernel, iterations = 1)

cv2.imwrite("./kernel-ops-18/3x3_black_cross_E.png", erosion)
cv2.imwrite("./kernel-ops-18/3x3_black_cross_D.png", dialtion)

#5 X 5 BLACK 1
kernel = np.array([[0,0,1,0,0],
                   [0,1,1,1,0],
                   [1,1,1,1,1],
                   [0,1,1,1,0],
                   [0,0,1,0,0]], np.uint8)

erosion = cv2.erode(img,kernel,iterations = 1)
dialtion = cv2.dilate(img, kernel, iterations = 1)

cv2.imwrite("./kernel-ops-18/5x5_black_1_E.png", erosion)
cv2.imwrite("./kernel-ops-18/5x5_black_1_D.png", dialtion)

#5 X 5 BLACK 2
kernel = np.array([[0,1,1,1,0],
                   [1,1,1,1,1],
                   [1,1,1,1,1],
                   [1,1,1,1,1],
                   [0,1,1,1,0]], np.uint8)

erosion = cv2.erode(img,kernel,iterations = 1)
dialtion = cv2.dilate(img, kernel, iterations = 1)

cv2.imwrite("./kernel-ops-18/5x5_black_2_E.png", erosion)
cv2.imwrite("./kernel-ops-18/5x5_black_2_D.png", dialtion)