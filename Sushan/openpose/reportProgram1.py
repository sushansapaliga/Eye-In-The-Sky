# From Python
# It requires OpenCV installed for Python
import sys
import cv2.cv2 as cv2
import os
from sys import platform
import argparse
from datetime import datetime

body_kp_to_id ={
    "Nose"          :   0,
    "Neck"          :   1,
    "RShoulder"     :   2,
    "RElbow"        :   3,
    "RWrist"        :   4,
    "LShoulder"     :   5,
    "LElbow"        :   6,
    "LWrist"        :   7,
    "MidHip"        :   8,
    "RHip"          :   9,
    "RKnee"         :   10,
    "RAnkle"        :   11,
    "LHip"          :   12,
    "LKnee"         :   13,
    "LAnkle"        :   14,
    "REye"          :   15,
    "LEye"          :   16,
    "REar"          :   17,
    "LEar"          :   18,
    "LBigToe"       :   19,
    "LSmallToe"     :   20,
    "LHeel"         :   21,
    "RBigToe"       :   22,
    "RSmallToe"     :   23,
    "RHeel"         :   24,
    "Background"    :   25
    }


def reportLog(log):
    f = open("reportFile_1.txt", "a")

    now = "[ " + str(datetime.now().date()) + "  " + str(datetime.now().time()) + " ]:"
    f.write(now)
    f.write(log)
    f.write("\n")
    f.close()

    pass

try:
    reportLog("<=====================its starting===================>")

    reportLog("setting up things")
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

    reportLog("done setting up things")

    reportLog("ready to process the images")

    # Starting OpenPose
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

    # Process Image
    datum = op.Datum()
    imageToProcess = cv2.imread(args[0].image_path)

    for i in range(50):
        datum.cvInputData = imageToProcess
        opWrapper.emplaceAndPop([datum])

        # Display Image
        print("Body keypoints: \n" + str(datum.poseKeypoints))

        reportLog(str(datum.poseKeypoints))

        cv2.imshow("OpenPose 1.5.1 - Tutorial Python API", datum.cvOutputData)
        keyInput = cv2.waitKey(1) & 0xFF

    reportLog("<=============================It has ended======================>\n\n\n")


except Exception as e:
    print(e)
    reportLog(e)
    reportLog("<====================got an error ============================>\n\n\n")
    sys.exit(-1)
