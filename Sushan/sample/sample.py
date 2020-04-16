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
finale = []
for i in body_kp_to_id_dummy:
    finale.append(body_kp_to_id_dummy[i])

print(finale)