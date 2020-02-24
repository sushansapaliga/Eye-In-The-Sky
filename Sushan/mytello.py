import tellopy
import cv2
import time


def handler(event, sender, data, **args):
    drone = sender
    if event is drone.EVENT_FLIGHT_DATA:
        #print(data)
        pass


def main():

    drone = tellopy.Tello()
    try:
        drone.subscribe(drone.EVENT_FLIGHT_DATA,handler)

        drone.connect()
        drone.wait_for_connection(60.0)
        vs = drone.get_video_stream()
        print(vs)

        he=input("\n\nhello:enter--")

        while he=="h":
            frame = vs.read("1024")

            cv2.imshow("Face Detection", frame) # display the frame
            key = cv2.waitKey(1) & 0xFF

            if key == "q":
                break

            time.sleep(0.5)

        pass
    except Exception as ex:
        print(ex)

        pass
    finally:
        cv2.destroyAllWindows()
        drone.quit()
        pass
    pass


if __name__ == "__main__":
    main()
    pass