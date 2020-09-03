import gesture
from openposepy import OP
import cv2.cv2 as cv2
from imutils.video import VideoStream

if __name__=="__main__":
    vs = VideoStream(src=0).start()
    op = OP()
    while True:
        frame = vs.read()
        result =  op.detectBody(frame)

        frameOutput = result["cvOutput"]
        if result["bodyPresent"]:
            bodyKeyPoints = result["bodyKeyPoints"]
            resultGesture = gesture.detectGesture(bodyKeyPoints)

            if resultGesture != None:
                print(resultGesture)
                cv2.imshow(resultGesture, frameOutput)
                cv2.waitKey(1) & 0xFF

        cv2.imshow("OpenPose and Gesture-TESTING", frameOutput)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break
        pass
    vs.stop()
    cv2.destroyAllWindows()
    pass
