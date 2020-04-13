import cv2.cv2 as cv2
import numpy as np
#import pyautogui
from imutils.video import VideoStream

screen_size=(640,480)
fourcc=cv2.VideoWriter_fourcc(*"XVID")
out=cv2.VideoWriter("output.avi",fourcc,20.0,(screen_size))

print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()

while True:
    #img=pyautogui.screenshot()
    #frame=np.array(img)
    #frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    frame = vs.read()
    out.write(frame)
    cv2.imshow("show",frame)
    if cv2.waitKey(1)==ord("q"):
        break

cv2.destroyAllWindows()
vs.stop()