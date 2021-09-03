import cv2

ref_point = []

def shape_selection(event, x, y, flags, param):
    global ref_point
    if event == cv2.EVENT_LBUTTONDOWN:
        ref_point = [(x, y)]

    elif event == cv2.EVENT_LBUTTONUP:
        ref_point.append((x, y))
        cv2.rectangle(image, ref_point[0], ref_point[1], (0, 255, 0), 2)
        cv2.imshow("image", image)


image = cv2.imread('./images/kitten1.jpg')
cv2.namedWindow("image")
cv2.setMouseCallback("image", shape_selection)

while True:
    cv2.imshow("image", image)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("c"):
        break

cv2.destroyAllWindows() 