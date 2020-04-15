import sys
import cv2.cv2 as cv2
import os
from sys import platform
import argparse
import numpy as np
from imutils.video import VideoStream

class OP:
    def __init__(self):
        try:
            # Import Openpose (Windows/Ubuntu/OSX)
            dir_path = os.path.dirname(os.path.realpath(__file__))
            try:
                # Windows Import
                if platform == "win32":
                    # Change these variables to point to the correct folder (Release/x64 etc.)
                    sys.path.append(dir_path + '/../../python/openpose/Release')
                    os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + '/../../x64/Release;' +  dir_path + '/../../bin;'
                    import pyopenpose as op
                else:
                    # Change these variables to point to the correct folder (Release/x64 etc.)
                    sys.path.append('../../python')
                    # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
                    # sys.path.append('/usr/local/python')
                    from openpose import pyopenpose as op
            except ImportError as e:
                print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
                raise e
            # Flags
            parser = argparse.ArgumentParser()
            parser.add_argument("--image_path", default="../../../examples/media/COCO_val2014_000000000192.jpg", help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
            args = parser.parse_known_args()
            
            # Custom Params (refer to include/openpose/flags.hpp for more parameters)
            params = dict()
            params["model_folder"] = "../../../models/"
            params["net_resolution"] = "160x80"
            params["number_people_max"] = 1
            
            # Add others in path?
            for i in range(0, len(args[1])):
                curr_item = args[1][i]
                if i != len(args[1])-1: next_item = args[1][i+1]
                else: next_item = "1"
                if "--" in curr_item and "--" in next_item:
                    key = curr_item.replace('-','')
                    if key not in params:  params[key] = "1"
                elif "--" in curr_item and "--" not in next_item:
                    key = curr_item.replace('-','')
                    if key not in params: params[key] = next_item
            
            # Construct it from system arguments
            # op.init_argv(args[1])
            # oppython = op.OpenposePython()
             
            # Starting OpenPose
            self.opWrapper = op.WrapperPython()
            self.opWrapper.configure(params)
            self.opWrapper.start()
            
            # Process Image
            self.datum = op.Datum()

            # self dignosis and to speed up the process - [ underworking ]
            #imageToProcess = cv2.imread(args[0].image_path)
            #finalThing = detectBody(imageToProcess)
            
        except Exception as e:
            print(e)
            sys.exit(-1)

        pass

    def detectBody(self, frame):

        # processing the frame
        self.datum.cvInputData  = frame
        self.opWrapper.emplaceAndPop([self.datum])

        finalReturn ={}

        #return the generated frame
        if self.datum.poseKeypoints.shape:
            finalReturn["bodyPresent"] = True
            finalReturn["bodyKeyPoints"] = self.datum.poseKeypoints
            finalReturn["cvOutput"] = self.datum.cvOutputData
            pass

        else:
            finalReturn["bodyPresent"] = False
            finalReturn["bodyKeyPoints"] = []
            finalReturn["cvOutput"] = self.datum.cvOutputData
            pass

        return finalReturn


if __name__=="__main__":
    #vs = VideoStream(src=0).start()
    #op = OP()
    while True:
        frame = vs.read()
        result =  op.detectBody(frame)

        frame1 = result["cvOutput"]

        cv2.imshow("OpenPose WebCam-TESTING", frame1)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break
        pass
    vs.stop()
    cv2.destroyAllWindows()
    pass


