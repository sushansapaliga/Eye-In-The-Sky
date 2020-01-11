import numpy as np 
import cv2
import threading
from imutils.video import VideoStream
import argparse
import imutils
import time

def acc_detect(): # function to detect Face in video cam 

    print("[INFO] loading model...")
    net = cv2.dnn.readNetFromCaffe("MAIN/deploy.prototxt.txt", "MAIN/res10_300x300_ssd_iter_140000.caffemodel")
    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()
    prev_x, prev_y, prev_endX, prev_endY, prev_word_y =0, 0, 0, 0, 0
    while True:
        frame = vs.read()
        frame = imutils.resize(frame, width=800)
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
        net.setInput(blob)
        detections = net.forward()

        check_flag=1 # to check whether there is face or not

        for i in range(0, detections.shape[2]): # if face is present 
            confidence = detections[0, 0, i, 2]
            if confidence < 0.5:
                continue

            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            text = "{:.2f}%".format(confidence * 100)
            y = startY - 10 if startY - 10 > 10 else startY + 10

            prev_x, prev_y, prev_endX, prev_endY, prev_word_y = startX, startY, endX, endY, y
            check_flag=0

            cv2.rectangle(frame, (startX, startY), (endX, endY),(0, 0, 255), 2)
            cv2.putText(frame, text, (startX, y),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
            center = ((startX + endX)//2, (startY + endY)//2) 
            cv2.circle(frame, center, 2, (0, 255, 0), 2)


        if check_flag==1: # if face is not present then show the last seen face position

            startX, startY, endX, endY, y = prev_x, prev_y, prev_endX, prev_endY, prev_word_y

            cv2.rectangle(frame, (startX, startY), (endX, endY),(0, 255, 0), 2)
            cv2.putText(frame, "last seen", (startX, y),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
            center = ((startX + endX)//2, (startY + endY)//2) 
            cv2.circle(frame, center, 2, (255, 0, 0), 2)


        cv2.imshow("Face Detection", frame) # display the frame
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

        #time.sleep(0.06) #  to save CPU from burning off !!
    

    cv2.destroyAllWindows()
    vs.stop()
    pass


  
if __name__ == "__main__":

    detect_face = threading.Thread(target=acc_detect, args=())  # creating the thread 
    
    detect_face.start() # starting the thread for detecting the face
    detect_face.join() # when the process is over the control will come back over here 
    

    
  
    print("\n\nDone!") 
