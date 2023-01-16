import cv2
import numpy as np

# load image
img = cv2.imread("0.png")

# convert to gray
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# threshold the grayscale image
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# use morphology erode to blur horizontally
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (151, 3))
morph = cv2.morphologyEx(thresh, cv2.MORPH_DILATE, kernel)

# use morphology open to remove thin lines from dotted lines
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 17))
morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)

# find contours
cntrs = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cntrs = cntrs[0] if len(cntrs) == 2 else cntrs[1]

# find the topmost box
ythresh = 1000000
for c in cntrs:
    box = cv2.boundingRect(c)
    x,y,w,h = box
    if y < ythresh:
        topbox = box
        ythresh = y

# Draw contours excluding the topmost box
result = img.copy()
for c in cntrs:
    box = cv2.boundingRect(c)
    if box != topbox:
        x,y,w,h = box
        cv2.rectangle(result, (x, y), (x+w, y+h), (0, 0, 255), 2)

# write result to disk
cv2.imwrite("text_above_lines_threshold.png", thresh)
cv2.imwrite("text_above_lines_morph.png", morph)
cv2.imwrite("text_above_lines_lines.jpg", result)

#cv2.imshow("GRAY", gray)
cv2.imshow("THRESH", thresh)
cv2.imshow("MORPH", morph)
cv2.imshow("RESULT", result)
cv2.waitKey(0)
cv2.destroyAllWindows()