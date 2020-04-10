import cv2.cv2 as cv2
from imutils.video import VideoStream

vs = VideoStream(src=0).start()
while True:
    frame = vs.read()
    cv2.imshow("preview",frame)
    key = cv2.waitKey(1) & 0xFF
    cv2.moveWindow("preview", 10,10)

    frame = cv2.resize(frame, (100,100),interpolation = cv2.INTER_LINEAR)
    cv2.imshow("preview1", frame)
    cv2.waitKey(1) & 0xFF
    cv2.moveWindow("preview1",800,50)

    if key == ord("q"):
        break

vs.stop()
cv2.destroyAllWindows()

