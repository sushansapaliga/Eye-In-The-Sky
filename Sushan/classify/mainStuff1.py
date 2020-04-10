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
        try:
            bat_per = int(str(data).split("BAT: ")[1].split(" ")[0])
            wifi = int(str(data).split("WIFI: ")[1].split(" ")[0])
        except :
            bat_per = 100
            wifi = 100
        finally:
            global instruction
            global stDrone

            stDrone["battery"] = bat_per
            stDrone["wifi"] = wifi
            if bat_per < 25:
                instruction["emergency"] = True
                instruction["reason"] = "Critically low battery level"
                pass

            elif wifi < 30:
                instruction["emergency"] = True
                instruction["reason"] = "Drone out of the range"
                pass
 

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
            face_frames_missed = 75
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

        instr = faceDetect.face_instruction_for_drone(startX, startY, endX, endY, 480, 345)

        instruction["clockwise"] = instr["clockwise"]
        instruction["up"] = instr["up"]
        instruction["front"] = instr["front"]
        instruction["right"] = instr["right"]

        pass

    image = cv2.resize(image, (430,320),interpolation = cv2.INTER_LINEAR)
    cv2.imshow("Face detection",image)
    cv2.moveWindow("Face detection", 1000,50)
    cv2.waitKey(1) & 0xFF

    pass

# the main function 
def main():
    # global variables
    global instruction
    global stDrone

    # starts 
    drone = tellopy.Tello()

    # image for background
    

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
                #temp_image = cv2.resize(image, ())
                cv2.imshow('Original', image)
                cv2.moveWindow("Original", 10,50)
                key = cv2.waitKey(1) & 0xFF

                # Detect face from the frame and return its coordinate
                if status["drone_in_air"] and status["mode"] == "face_detection":
                    if check_frame == 0:
                        face_module(image)
                        check_frame = 4
                        pass
                    else:
                        check_frame = check_frame - 1
                        pass
                    pass

                # show status Window
                temp_black1 = cv2.imread("black.jpg")
                temp_black1 = cv2.resize(temp_black1, (430,320),interpolation = cv2.INTER_LINEAR)
                temp_black1 = cv2.putText(temp_black1, "Feature Activated: " + status["mode"], (0,15),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255,255,255))
                
                temp_black1 = cv2.putText(temp_black1, "Instructions:", (0,40),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255,255,255))
                temp_black1 = cv2.putText(temp_black1, "Up: " + str(instruction["up"]), (5,55),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255,255,255))
                temp_black1 = cv2.putText(temp_black1, "Clockwise: " + str(instruction["clockwise"]), (140,55),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255,255,255))
                temp_black1 = cv2.putText(temp_black1, "Front: " + str(instruction["front"]), (5,70),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255,255,255))
                temp_black1 = cv2.putText(temp_black1, "Right: " + str(instruction["right"]), (140,70),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255,255,255))

                temp_black1 = cv2.putText(temp_black1, "Drone Status: ", (0,95),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255,255,255))
                temp_black1 = cv2.putText(temp_black1, "WiFi: " + str(stDrone["wifi"]), (5,110),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255,255,255))
                temp_black1 = cv2.putText(temp_black1, "Battery: " + str(stDrone["battery"]), (140,110),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255,255,255))
                temp_black1 = cv2.putText(temp_black1, "Is drone in AIR: " + str(status["drone_in_air"]), (5,125),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255,255,255))

                cv2.imshow("Status Window",temp_black1)
                cv2.waitKey(1) & 0xFF
                cv2.moveWindow("Status Window", 1000, 450)

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

                # if any emergency occurs raise the error and close the application
                if instruction["emergency"] != None and instruction["emergency"]:
                    reportLog("Emergency activated : " + instruction["reason"] )
                    raise Exception(instruction["reason"])

                # instruction for the drone
                # instruction when drone is in air
                if status["drone_in_air"]:
                    if instruction["clockwise"] != None:
                        if instruction["clockwise"] >= 0:
                            drone.clockwise(instruction["clockwise"])
                            pass
                        
                        else :
                            drone.counter_clockwise(-1 *  instruction["clockwise"])
                            pass

                        reportLog("clockwise "+ str(instruction["clockwise"]))
                        instruction["clockwise"] = None
                        pass

                    if instruction["up"] != None:
                        if instruction["up"] >= 0:
                            drone.up(instruction["up"])
                            pass
                        else:
                            drone.down(-1 * instruction["up"])
                            pass

                        reportLog("up " + str(instruction["up"]))
                        instruction["up"] = None
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
instruction["front"] = None
instruction["land"] = None
instruction["emergency"] = None
instruction["reason"] = None # reason why the emergency bit was activated

# drone status
stDrone = {}
stDrone["battery"] = 100
stDrone["wifi"] = 100



# when this program is executed it starts from here
if __name__ == '__main__':
    main()