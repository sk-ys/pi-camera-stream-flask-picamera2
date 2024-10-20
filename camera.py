#Modified by smartbuilds.io
#Date: 27.09.20
#Desc: This scrtipt script..

import cv2 as cv
from picamera2 import Picamera2
import time
from datetime import datetime
import numpy as np

class VideoCamera(object):
    def __init__(self, flip = False, file_type  = ".jpg", photo_string= "stream_photo"):
        self.camera = Picamera2()
        # config = self.camera.create_still_configuration(main={"size": (1920, 1080)})
        # self.camera.configure(config)
        self.camera.start()

        self.flip = flip # Flip frame vertically
        self.file_type = file_type # image type i.e. .jpg
        self.photo_string = photo_string # Name to save the photo
        time.sleep(2.0)

    def __del__(self):
        self.camera.stop()

    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame

    def get_frame(self):
        frame = self.camera.capture_array()
        frame = self.flip_if_needed(frame)
        return frame
    
    def get_jpeg(self):
        frame = self.get_frame()
        ret, jpeg = cv.imencode(self.file_type, frame)
        return jpeg.tobytes()

    # Take a photo, called by camera button
    def take_picture(self):
        frame = self.get_frame()
        today_date = datetime.now().strftime("%m%d%Y-%H%M%S") # get current time
        cv.imwrite(str(self.photo_string + "_" + today_date + self.file_type), frame)
