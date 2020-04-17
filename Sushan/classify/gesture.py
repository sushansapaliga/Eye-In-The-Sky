
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
        elif wrist[0] < elbow[0]:
            return outerGesture
        else:
            return None

    return None

def __checkWakandaStyle__(R_elbow, R_wrist, L_elbow, L_wrist, neck, midHip, nose):
    midRightHand = []
    midRightHand.append( (R_elbow[0] + R_wrist[0])//2 )
    midRightHand.append( (R_elbow[1] + R_wrist[1])//2 )

    midLeftHand = []
    midLeftHand.append( (L_elbow[0] + L_wrist[0])//2 )
    midLeftHand.append( (L_elbow[1] + L_wrist[1])//2 )

    x = pow((midRightHand[0] - midLeftHand[0]), 2)
    y = pow((midRightHand[1] - midLeftHand[1]), 2)

    # the radius thing might need calibration [ for now the value is 10 pixel ]  
    if ( x + y ) < pow(10, 2):

        # check the hand location is it above the head or inside the body
        if nose[1] > midRightHand[1]:
            return "HandAboveHead"
        elif  neck[1] < midRightHand[1] and midRightHand[1] < midHip[1]:
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
    else:
        check_right = __checkHandAboveShoulderStyle__(R_wrist, R_elbow, R_shoulder, "leftDrone", "rightDrone")
        check_left = __checkHandAboveShoulderStyle__(L_wrist, L_elbow, L_shoulder, "forwardDrone", "backwardDrone")

        # only one gesture at a time is allowed - either right or left
        if check_right != None and check_left != None:
            return None
        elif check_right != None:
            return check_right
        elif check_left != None:
            return check_left
        else:
            return None
            #pass

        pass

    pass
