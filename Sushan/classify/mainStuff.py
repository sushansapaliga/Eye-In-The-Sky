import cv2.cv2 as cv2
from imutils.video import VideoStream

inp = "ALT:  0 | SPD:  0 | BAT: 71 | WIFI: 90 | CAM:  0 | MODE:  6"
#inp = "ALT: 11 | SPD:  0 | BAT: 100 | WIFI: 90 | CAM:  0 | MODE:  6"
inp = inp.split("WIFI: ")[1].split(" ")[0]
print(inp)


# vs = VideoStream(src=0).start()
# while True:
#     frame = vs.read()
#     cv2.imshow("preview",frame)
#     key = cv2.waitKey(1) & 0xFF

#     print(cv2.countNonZero(frame))
#     if cv2.countNonZero(frame) == 0:
#         print("black")
#     else:
#         print("not black")

#     if key == ord("q"):
#         break

# vs.stop()
# cv2.destroyAllWindows()

