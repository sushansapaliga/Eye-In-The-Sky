import numpy as np 
import cv2
import threading
from imutils.video import VideoStream
import argparse
import imutils
import time
from djitellopy.tello import Tello

status={ "facedetection" : 1 , "quit": 0 }
main_frame = None

def acc_detect(): # function to detect Face in the frame given to it 

    print("[INFO] loading model...")
    net = cv2.dnn.readNetFromCaffe("MAIN/deploy.prototxt.txt", "MAIN/res10_300x300_ssd_iter_140000.caffemodel")
    print("[INFO] starting video stream...")
    prev_x, prev_y, prev_endX, prev_endY, prev_word_y =0, 0, 0, 0, 0
    while True:
        frame = main_frame
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

        #:
        if status["facedetection"] == 1 :
            break

        time.sleep(0.06) #  to save CPU from burning off !!
    

    cv2.destroyAllWindows()
    pass



def controller(): # function to control all the features
    detect_face = threading.Thread(target=acc_detect, args=())
    while status["quit"] == 0:
        ch = input("enter the input:\n 1- start facedetection \n 2- stop facedetection \n q - quit \n")
        if ch == "1" :
            if status["facedetection"] == 1:
                status["facedetection"] = 0
                detect_face = threading.Thread(target=acc_detect, args=())
                detect_face.start()
                time.sleep(3)
                print("face detection has been started")
            else:
                print("facedetection already started")
        
        elif ch == "2":
            if status["facedetection"] == 0:
                status["facedetection"] = 1
                detect_face.join()
                print("face detection has been stopped")
            else:
                print("face detection has not yet started")
        
        elif ch == "q":
            if status["facedetection"] == 0:
                status["facedetection"] = 1
                detect_face.join()
                print("face detection has been stopped")

            status["quit"] = 1

        else : 
            print("invalid input")


    pass

def main_stream():

    global main_frame
    tello = Tello()

    if not tello.connect():
        print("tello not connected")

    if not tello.streamoff():
        print("could not stop video stream")

    if not tello.streamon():
        print("could not start video stream")

    frame_read = tello.get_frame_read()
    while status["quit"] == 0:

        if frame_read.stopped:
            frame_read.stop()

        
        main_frame = frame_read.frame

        frame = main_frame
        cv2.imshow("Main Stream", frame) # display the frame
        key = cv2.waitKey(1) & 0xFF

    cv2.destroyAllWindows()
    pass

  
if __name__ == "__main__":

    controller = threading.Thread(target=controller, args=()) # creating a controller
    main_stream = threading.Thread(target=main_stream, args=())

    controller.start()
    main_stream.start()
    controller.join()
    main_stream.join()

    print("\n\nDone!") 
