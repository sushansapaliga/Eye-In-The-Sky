from djitellopy.tello import Tello
from face_detection import FaceDetection
from time import sleep
import cv2.cv2 as cv2
from datetime import datetime

def reportLog(log):
    f = open("reportFile.txt", "a")

    now = "[ " + str(datetime.now().date()) + "  " + str(datetime.now().time()) + " ]:"
    f.write(now)
    f.write(log)
    f.write("\n")
    f.close()

    pass

if __name__=="__main__":
    
    tello = Tello()
    faceDetect = FaceDetection()
    sleep(2)

    reportLog("<====================Its starting========================>")

    status = {}
    # this status pin maintains wheather to quit the application or not 
    status["quit"] = False  

    # this status pin tells wheather the drone in the air
    status["is_drone_in_air"] = False 

    if not tello.connect():
        print("tello not connected") 
        reportLog("tello not connected")
        status["quit"] = True

    if not status["quit"] and not tello.streamoff() :
        print("could not stop video stream")
        reportLog("could not stop video stream")
        status["quit"] = True

    if not status["quit"] and not tello.streamon() :
        print("could not start video stream")
        reportLog("could not start video stream")
        status["quit"] = True
    

    if not status["quit"]:
        print("getting frame from drone")
        telloFrame = tello.get_frame_read()
        sleep(5) 
    
    while not status["quit"]:

        if telloFrame.stopped:
            telloFrame.stop()

        #if int(tello.get_battery()) < 35 :
        #    print("The battery level of the drone is critically low")
        #    if status["is_drone_in_air"]:
        #        tello.land()
        #        status["is_drone_in_air"] = False
        #    status["quit"] = True

        #reportLog(tello.get_battery())

        frame = telloFrame.frame

        cv2.imshow("Main Show", frame)
        key = cv2.waitKey(1) & 0xFF

        cord = faceDetect.get_face_coordinates(frame)
        if cord["face_status"]==True:
            startX, startY, endX, endY = cord["startX"], cord["startY"], cord["endX"], cord["endY"]
            cv2.rectangle(frame, (startX, startY), (endX, endY),(0, 0, 255), 2)

        cv2.imshow("Face detection",frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            status["quit"] = True

        if key == ord("t") and not status["is_drone_in_air"]:
            status["is_drone_in_air"] = True
            tello.takeoff()
            #sleep(3)
            #tello.send_rc_control(left_right_velocity= 0, forward_backward_velocity=0, up_down_velocity=5, yaw_velocity= 0)
            #tello.move_up(2)
            #sleep(1)
        
        if key == ord("l") :
            status["is_drone_in_air"] = False
            tello.land()

        if key == ord("u"):
            tello.move_up(20)

        if key == ord("s"):
            tello.send_rc_control(left_right_velocity= 0, forward_backward_velocity=0, up_down_velocity=5, yaw_velocity= 0)
    
    cv2.destroyAllWindows()
    tello.end()

    reportLog("<===================It has ended ============>\n\n\n")

    pass