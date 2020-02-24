from djitellopy.tello import Tello
import cv2



class Video_stream(object):

    def __init__(self):

        self.tello = Tello()


        pass

    def run(self):
        if not self.tello.connect():
            print("tello not connected")
            return

        if not self.tello.streamoff():
            print("could not stop video stream")
            return

        if not self.tello.streamon():
            print("could not start video stream")
            return
        
        frame_read = self.tello.get_frame_read()

        while True:
            if frame_read.stopped:
                frame_read.stop()
                break

            frame = frame_read.frame
            cv2.imshow("Tello stream", frame)
            key = cv2.waitKey(1)& 0xFF

            if key == 'q':
                break

        cv2.destroyAllWindows()
        self.tello.end()



def main():
    video = Video_stream()
    video.run()

if __name__ == '__main__':
    main()