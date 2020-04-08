import sys
import traceback
import tellopy
import av
import cv2.cv2 as cv2  # for avoidance of pylint error
import numpy
import time
from face_detection import FaceDetection
from datetime import datetime




# function to print status about the drone in a readable pattern
def handler(event, sender, data, **args):
    drone = sender
    if event is drone.EVENT_FLIGHT_DATA:
        print(data)

# report the log about the program
def reportLog(log):
    f = open("reportFile.txt", "a")

    now = "[ " + str(datetime.now().date()) + "  " + str(datetime.now().time()) + " ]:"
    f.write(now)
    f.write(log)
    f.write("\n")
    f.close()

    pass


# the face module: detect it and generate instruction 
def face_module(image):
    global face_final
    global face_frames_missed
    global instruction

    cord = faceDetect.get_face_coordinates(image)
    if cord["face_status"]==True:
        face_final["startX"], face_final["startY"], face_final["endX"], face_final["endY"] = cord["startX"], cord["startY"], cord["endX"], cord["endY"]
        face_frames_missed = 0

    else:

        if face_frames_missed > 200 :
            instruction["land"] = True
            reportLog("command for drone to land - no face found ")

        elif face_frames_missed > 50 :
            instruction["clockwise"] = 30
            reportLog("command for drone to rotate- trying to find a face ")
            pass

        else:
            reportLog("face not found")
            pass

        face_frames_missed = face_frames_missed + 1

    if face_frames_missed <= 50 :
        startX, startY, endX, endY = face_final["startX"], face_final["startY"], face_final["endX"], face_final["endY"]
        cv2.rectangle(image, (startX, startY), (endX, endY),(0, 0, 255), 2)

        instruction["clockwise"] = 0
        pass

    cv2.imshow("Face detection",image)
    cv2.waitKey(1) & 0xFF

    pass

# the main function 
def main():
    # global variables
    global instruction

    # starts 
    drone = tellopy.Tello()

    status = {}
    status["mode"] = "face_detection"
    status["drone_in_air"] = False

    try:
        # this is used to subscribe to the functionalality of the drone
        drone.subscribe(drone.EVENT_FLIGHT_DATA, handler)
        drone.connect()
        drone.wait_for_connection(60.0)

        # number of times it will retry to connect it with the drone 
        retry = 33
        container = None


        while container is None and 0 < retry:
            retry -= 1
            try:
                container = av.open(drone.get_video_stream())
            except av.AVError as ave:
                print(ave)
                print('retry...')

        # skip first 300 frames
        frame_skip = 300

        # frame controller
        check_frame = 4

        while True:
            key = 0
            for frame in container.decode(video=0):

                # frame are skipped due to bad picture
                if 0 < frame_skip:
                    frame_skip = frame_skip - 1
                    print("Frame Skipping")
                    continue

                # getting frame from the drone and display it
                start_time = time.time()
                image = cv2.cvtColor(numpy.array(frame.to_image()), cv2.COLOR_RGB2BGR)
                cv2.imshow('Original', image)
                key = cv2.waitKey(1) & 0xFF

                # Detect face from the frame and return its coordinate
                if status["drone_in_air"] and status["mode"] == "face_detection":
                    if check_frame == 0:
                        face_module(image)
                        check_frame = 4
                    
                    else:
                        check_frame = check_frame - 1


                # optional to take control of the drone [will be removed soon, used for fail safe]
                if key == ord("q"):
                    reportLog("closing of the application")
                    break

                if key == ord("t"):
                    drone.takeoff()
                    reportLog("drone taking off")
                    status["drone_in_air"] = True
                
                if key == ord("l"):
                    drone.land()
                    reportLog("drone landing")
                    cv2.destroyWindow("Face detection")
                    status["drone_in_air"] = False

                
                # instruction for the drone
                # instruction when drone is in air
                if status["drone_in_air"]:
                    if instruction["clockwise"] != None:
                        if instruction["clockwise"] >= 0:
                            drone.clockwise(instruction["clockwise"])
                            pass
                        
                        else :
                            drone.counter_clockwise(instruction["clockwise"])
                            pass

                        reportLog("clockwise "+ str(instruction["clockwise"]))
                        instruction["clockwise"] = None
                        pass
                    
                    if instruction["land"] != None and instruction["land"]:
                        drone.land()
                        reportLog("drone landing")
                        cv2.destroyWindow("Face detection")
                        status["drone_in_air"] = False
                        instruction["land"] = None
                        pass
                    pass
                # instruction when drone is not in air
                else:
                    pass

                # necessary to maintain the realtime frame from the drone
                if frame.time_base < 1.0/60:
                    time_base = 1.0/60
                else:
                    time_base = frame.time_base

                frame_skip = int((time.time() - start_time)/time_base)
            
            # to break the while
            if key == ord("q") :
                break
                    

    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        print(ex)
    finally:
        if status["drone_in_air"]:
            drone.land()
        drone.quit()
        cv2.destroyAllWindows()




# global variable here

# varible related to face
faceDetect = FaceDetection()
face_frames_missed = 80
face_final = {}

# variable related to drones
instruction ={}
instruction["up"] = None
instruction["right"] = None
instruction["clockwise"] = None
instruction["land"] = None



# when this program is executed it starts from here
if __name__ == '__main__':
    main()