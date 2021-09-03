import os
import calendar
import time

import cv2

def capture_save_video():
    if(os.path.isdir('./videos')):
        pass
    else:
        os.mkdir('./videos')

    video = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
    result = cv2.VideoWriter('./videos/'+str(calendar.timegm(time.gmtime()))+'.mp4', fourcc, 15.0, (640,  480))

    while(True):
        ret, frame = video.read()
        if not ret:
            print('Cannot recieve Frame! Exitting.')
            break
        
        result.write(frame)
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) == ord('s'):
            break
  
    video.release()
    result.release()
    cv2.destroyAllWindows()
  