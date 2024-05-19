import argparse
from pathlib import Path
import numpy as np
import cv2



def img_birightnmess(image):
    # Calculate mean brightness as percentage
    im = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
    meanpercent = np.mean(im) * 100 / 255
    return meanpercent

def extract_images_from_video(video_file, image_1, image_2):
    count = 0
    vidcap = cv2.VideoCapture(video_file)
    success,image = vidcap.read()
    success = True
    light_seen = False
    while success:
        # skip milliseconds
        vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*500))    
        success,image = vidcap.read()

        try:
            ib  = img_birightnmess(image)
        except Exception as e:
            # end of video stream
            return
                    
        if (ib>30.0):
            if (not light_seen):
                # Light just turned on
                cv2.imwrite(image_1, image)
                light_seen = True
            else:
                # Light has been on for a while - save image in case it's the last lit one
                cv2.imwrite(image_2, image)

        count += 1
