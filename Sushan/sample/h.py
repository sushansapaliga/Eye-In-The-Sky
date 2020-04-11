import sys
import traceback
import tellopy
import av
import cv2.cv2 as cv2  # for avoidance of pylint error
import numpy
import time


def handler(event, sender, data, **args):
    drone = sender
    if event is drone.EVENT_FLIGHT_DATA:
        #print(data)
        pass

drone = tellopy.Tello()

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

        if key == ord("q"):
            break

        if key == ord("t"):
            drone.takeoff()

        if key == ord("l"):
            drone.land()
        
        if key == ord("c"):
            drone.clockwise(10)
            print("clockwise 10")

        if key == ord("a"):
            drone.counter_clockwise(10)
            print("counter clockwise 10")

        if key == ord("s"):
            drone.clockwise(0)
            print("stop clockwise 0")


        # necessary to maintain the realtime frame from the drone
        if frame.time_base < 1.0/60:
            time_base = 1.0/60
        else:
            time_base = frame.time_base

        frame_skip = int((time.time() - start_time)/time_base)
                    

except Exception as ex:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_traceback)
    print(ex)
finally:
    drone.quit()
    cv2.destroyAllWindows()

