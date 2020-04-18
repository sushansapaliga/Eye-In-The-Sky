
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

body_kp_to_id_dummy ={
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
    "LHip"          :   12,
    "REye"          :   15,
    "LEye"          :   16,
    "REar"          :   17,
    "LEar"          :   18,
    }

def __allValid__(bodyKeyPoints):
    body1 = bodyKeyPoints[0]

    for k in body_kp_to_id_dummy:
        x, y, config = body1[body_kp_to_id_dummy[k]]
        if x == 0 and y == 0:
            return True
        config = config + 1
        pass
    return False

def __checkHandAboveShoulderStyle__(wrist, elbow, shoulder, innerGesture, outerGesture):
    if shoulder[1] < elbow[1] and shoulder[1] > wrist[1]:
        if wrist[0] > elbow[0]:
            return innerGesture
        elif wrist[0] > elbow[0]:
            return outerGesture
        else:
            return None

    return None

def __checkingIntersectionPoint__(R_elbow, R_wrist, L_elbow, L_wrist):
    x, y = 0, 0
    try:
        slope_right = (R_elbow[1] - R_wrist[1]) / (R_elbow[0] - R_wrist[0])
        coeffi_right = R_elbow[1] - slope_right * R_elbow[0]

        slope_left = (L_elbow[1] - L_wrist[1]) / (L_elbow[0] - L_wrist[0])
        coeffi_left = L_elbow[1] - slope_left * L_elbow[0]

        x = (coeffi_left - coeffi_right) / (slope_right - slope_left)
        y = slope_right * x + coeffi_right
    except :
        return 0, 0
    finally:
        return x, y
    pass

def __checkWakandaStyle__(R_elbow, R_wrist, L_elbow, L_wrist, neck, midHip, nose):

    x, y = __checkingIntersectionPoint__(R_elbow, R_wrist, L_elbow, L_wrist)

    # the radius thing might need calibration [ for now the value is 10 pixel ]  
    if x != 0 and y != 0:
        maxY = max(R_elbow[1], R_wrist[1])
        minY = min(R_elbow[1], R_wrist[1])
        maxX = max(R_elbow[0], R_wrist[0])
        minX = min(R_elbow[0], R_wrist[0])
        if maxY > y and y > minY and maxX > x and x > minX:
            # check the hand location is it above the head or inside the body
            if nose[1] > y:
                return "HandAboveHead"
            elif neck[1] < y and y < midHip[1]:
                return "HandWithinBody"

    return None

def detectGesture(bodyKeyPoints):
    neck =  bodyKeyPoints[0][body_kp_to_id["Neck"]]
    nose =  bodyKeyPoints[0][body_kp_to_id["Nose"]]
    midHip = bodyKeyPoints[0][body_kp_to_id["MidHip"]]

    R_elbow = bodyKeyPoints[0][body_kp_to_id["RElbow"]]
    R_wrist = bodyKeyPoints[0][body_kp_to_id["RWrist"]]
    R_shoulder = bodyKeyPoints[0][body_kp_to_id["RShoulder"]]

    L_elbow = bodyKeyPoints[0][body_kp_to_id["LElbow"]]
    L_wrist = bodyKeyPoints[0][body_kp_to_id["LWrist"]]
    L_shoulder = bodyKeyPoints[0][body_kp_to_id["LShoulder"]]

    # if any one of the essential body keypoints is missing then dont guess the gesture made
    if __allValid__(bodyKeyPoints):
        return None

    check = __checkWakandaStyle__(R_elbow, R_wrist, L_elbow, L_wrist, neck, midHip, nose)
    if check != None:
        # wakanda style was successful
        if check == "HandWithinBody":    
            return "CapturePic"
        else:
            return "Recording"
        pass

    check_right = __checkHandAboveShoulderStyle__(R_wrist, R_elbow, R_shoulder, "leftDrone", "rightDrone")
    check_left = __checkHandAboveShoulderStyle__(L_wrist, L_elbow, L_shoulder, "forwardDrone", "backwardDrone")

    # only one gesture at a time is allowed - either right or left
    if check_right != None and check_left != None:
        return None
    elif check_right != None:
        return check_right
    elif check_left != None:
        return check_left

    # next gesture

    return None


if __name__=="__main__":
    #x, y = __checkingIntersectionPoint__([0,3],[1,5],[0,7],[1,6.5])
    x, y = __checkingIntersectionPoint__([0,3],[1,5],[0,3],[1,5])
    
    print(x)
    print(y)
    pass