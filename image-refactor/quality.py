import cv2
from cv2 import dnn_superres
import time

# Create an SR object
sr = dnn_superres.DnnSuperResImpl_create()

# Read image
image = cv2.imread('/home/pika/Downloads/GSR-Downloads/Tests/TNR12.png')

# Read the desired model
# path = "EDSR_x3.pb"
path="FSRCNN_x4.pb"
# path="ESPCN_x4.pb"
sr.readModel(path)

# Set the desired model and scale to get correct pre- and post-processing
# sr.setModel("edsr", 3)
sr.setModel("fsrcnn", 4)
# sr.setModel("espcn", 4)

# Upscale the image
t_s = time.time()
result = sr.upsample(image)
print('Time Taken='+str((time.time()- t_s) * 1000)+' ms')

# Save the image
cv2.imwrite("fsrcnn4.png", result)