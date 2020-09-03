from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2.cv2 as cv2

from datetime import datetime

class FaceDetection:

    def __init__(self):

        # construct the argument parse and parse the arguments
        # load our serialized model from disk
        print("[Face Detection][INFO] loading model...")
        self.net_global = cv2.dnn.readNetFromCaffe("media/models/deploy.prototxt.txt", "media/models/res10_300x300_ssd_iter_140000.caffemodel")


        pass

    def get_face_coordinates(self,frame):
        net = self.net_global
        #frame = imutils.resize(frame, width=800)
 
	    # grab the frame dimensions and convert it to a blob
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
		    (300, 300), (104.0, 177.0, 123.0))
 
	    # pass the blob through the network and obtain the detections and
	    # predictions
        net.setInput(blob)
        detections = net.forward()

        #coordinates of the face 
        face_dict ={"face_status": False}

        #save the algorithm from detecting from more people
        discontinue_bit = 0

	    # loop over the detections
        for i in range(0, detections.shape[2]):
		    # extract the confidence (i.e., probability) associated with the
		    # prediction
            confidence = detections[0, 0, i, 2]

		    # filter out weak detections by ensuring the `confidence` is
		    # greater than the minimum confidence
            if confidence < 0.5:
                continue

            #discontinue if more than one people are detected
            discontinue_bit += 1

            if discontinue_bit > 1:
                break

		    # compute the (x, y)-coordinates of the bounding box for the
		    # object
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (face_dict["startX"], face_dict["startY"], face_dict["endX"], face_dict["endY"]) = box.astype("int")

            face_dict["face_status"] = True
 
		    # draw the bounding box of the face along with the associated
		    # probability
		    #text = "{:.2f}%".format(confidence * 100)
		    #y = startY - 10 if startY - 10 > 10 else startY + 10
		    #cv2.rectangle(frame, (startX, startY), (endX, endY),
			#    (0, 0, 255), 2)
		    #cv2.putText(frame, text, (startX, y),
			#    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

	    # show the output frame
        return face_dict

    def __limitIt__(self, val):
        if val > 20:
            val = 20
        elif val < -20:
            val = -20
        elif val < 2 or val < -2:
            val = 0 
        return val

    def reportLog(self, log):
        f = open("reportFileFaceRelated.txt", "a")

        now = "[ " + str(datetime.now().date()) + "  " + str(datetime.now().time()) + " ]:"
        f.write(now)
        f.write(log)
        f.write("\n")
        f.close()

        pass

    def __getSafeDistance__ (self, startX, startY, endX, endY):
        front = 0

        x = startX - endX
        y = startY - endY

        if x < 0 :
            x = x * -1
            pass

        if y < 0 :
            y = y * -1
            pass

        z = x + y

        self.reportLog(str(z))

        if z > 220:
            front = -18
            pass
        elif z < 150:
            front = 18
            pass

        return front
        pass
            
    def face_instruction_for_drone(self, startX, startY, endX, endY, drone_centreX, drone_centreY):

        face_centreX = (startX + endX)/2
        face_centreY = (startY + endY)/2

        instrction = {"up" : 0, "clockwise" : 0, "right" : 0, "front" : 0}

        up =-1 * (face_centreY - drone_centreY)//10
        up = self.__limitIt__(up)
        clockwise = (face_centreX - drone_centreX)//10
        clockwise = self.__limitIt__(clockwise)

        instrction["up"] = up 
        instrction["clockwise"] = clockwise

        safeDistanceBit =  True

        if safeDistanceBit:
            instrction["front"] = self.__getSafeDistance__(startX, startY, endX, endY)
        
        return instrction

if __name__=="__main__":  
    face = FaceDetection()
    # takes time to load the model 
    
    # starts the video stream 
    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()
    time.sleep(3)

    while True:
        frame = vs.read()

        cord = face.get_face_coordinates(frame)
        #print(cord["face_status"])

        if cord["face_status"]==True:
            startX, startY, endX, endY = cord["startX"], cord["startY"], cord["endX"], cord["endY"]
            cv2.rectangle(frame, (startX, startY), (endX, endY),(0, 0, 255), 2)
        
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        
        time.sleep(0.1)

    cv2.destroyAllWindows()
    vs.stop()
        

    