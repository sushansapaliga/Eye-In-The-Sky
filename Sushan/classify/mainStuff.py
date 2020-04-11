import cv2.cv2 as cv2
import numpy as np
from imutils.video import VideoStream

def checkBrightness(frame):
    brightness = np.mean(frame)
    print(brightness)
    pass

vs = VideoStream(src=0).start()
while True:
    frame = vs.read()
    cv2.imshow("preview",frame)
    key = cv2.waitKey(1) & 0xFF

    checkBrightness(frame)

    if key == ord("q"):
        break

vs.stop()
cv2.destroyAllWindows()

