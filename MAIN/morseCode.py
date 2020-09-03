import numpy as np

def checkBrightness(frame):
    
    threshold = 35

    brightness = np.mean(frame)

    return threshold > brightness