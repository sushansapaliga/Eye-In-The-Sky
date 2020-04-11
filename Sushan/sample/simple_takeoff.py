from djitellopy.tello import Tello
import time


def simple_takeOff():
    tello = Tello()
    if not tello.connect():
        print("Tello not connected")
        return
    
    tello.takeoff()

    time.sleep(3)

    if input()=="q":
        tello.land()

    tello.end()
    
    pass

if input() == "q":
    simple_takeOff()