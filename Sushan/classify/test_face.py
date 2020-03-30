from face_detection import FaceDetection
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2

face = FaceDetection()
# takes time to load the model 
    
# starts the video stream 
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(3)

while True:
    frame = vs.read()

    cord = face.get_face_coordinates(frame)
    print(cord["face_status"])

    if cord["face_status"]==True:
        startX, startY, endX, endY = cord["startX"], cord["startY"], cord["endX"], cord["endY"]
        cv2.rectangle(frame, (startX, startY), (endX, endY),(0, 0, 255), 2)
        
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

    time.sleep(0.5)

cv2.destroyAllWindows()
vs.stop()