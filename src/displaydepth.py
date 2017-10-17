from openni import openni2
from openni import _openni2 as c_api
import cv2
import numpy as np
import scipy.misc as scmi
import time


JARVIS_IMG_PATH="img/kinect_jarvis_invert.png"
REINIT_IMG_EACH_NB=100
MS_WAIT_BEFORE_NEXT_IMG_WRITE=100

def applyCustomColorMap(im_gray):

    rgb = scmi.imread(JARVIS_IMG_PATH)

    lut = np.zeros((256, 1, 3), dtype=np.uint8)
    lut[:, 0, 0] = rgb[1,:,2]
    lut[:, 0, 1] = rgb[1,:,1]
    lut[:, 0, 2] = rgb[1,:,0]


    im_color = cv2.LUT(im_gray, lut)

    return im_color


class DisplayDepth(object):

    #def __init__(self):
        #self.last_time = int(round(time.time() * 1000))
        #self.cpt = 0
    
    def show_frame(self, frame):
   
        dmap = np.fromstring(frame.get_buffer_as_uint16(),dtype=np.uint16).reshape(480,640)  # Works & It's FAST
        im_gray = np.uint8(dmap.astype(float) *255/ 2**12-1) # Correct the range. Depth images are 12bits
        im_gray = cv2.cvtColor(im_gray,cv2.COLOR_GRAY2RGB)
        im_color = applyCustomColorMap(im_gray)
        cv2.GaussianBlur(im_color,(5,5), 0)

        cv2.imshow('Jarvis-View', im_color)
        #current_time = int(round(time.time() * 1000))
       
        #if (current_time-self.last_time) > MS_WAIT_BEFORE_NEXT_IMG_WRITE:
        #    self.last_time = current_time
        cv2.imwrite("/tmp/kinect/kinect_jarvis.jpg",im_color)

        #    if self.cpt < REINIT_IMG_EACH_NB:
        #        self.cpt += 1
        #    else:
        #        self.cpt = 0

        