from playsound import playsound
import threading

# global
number = 1 

def __playSound__():
    global number

    for i in range(number):
        playsound("media/sounds/beep-06.mp3")
        i = i + 1
    pass

def playMusic(actionType):
    global number
    
    invalid = False
    # creating a thread so that the program runs in background
    main_stream = threading.Thread(target=__playSound__, args=())
    if actionType == "take_off" or actionType == "land":
        number = 5
        pass
    elif actionType == "attention":
        number = 1
        pass
    else:
        invalid = True
        pass

    if not invalid:
        main_stream.start()
        pass

    pass


if __name__ == "__main__":

    #playMusic("land")
    playMusic("attention")

    print("Im done over here")
    pass