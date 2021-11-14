from openni import openni2
from openni import _openni2 as c_api
import cv2
import numpy as np
import scipy.misc as scmi
import time

JARVIS_IMG_PATH="img/kinect_jarvis_invert.png"
TIME_TO_DISPLAY_TEXT=2000

def applyCustomColorMap(im_gray):

    rgb = scmi.imread(JARVIS_IMG_PATH)

    lut = np.zeros((256, 1, 3), dtype=np.uint8)
    lut[:, 0, 0] = rgb[1,:,2]
    lut[:, 0, 1] = rgb[1,:,1]
    lut[:, 0, 2] = rgb[1,:,0]


    im_color = cv2.LUT(im_gray, lut)

    return im_color


class DisplayDepth(object):
    
    def __init__(self):
        self.width = 640
        self.height = 480
        self.text_start_time = None
        self.text = None
        self.img = None
        self.color = (2,2,254)
    
    def build_img(self, frame):
        
        dmap = np.fromstring(frame.get_buffer_as_uint16(),dtype=np.uint16).reshape(self.height , self.width)  # Works & It's FAST
        im_gray = np.uint8(dmap.astype(float) *255/ 2**12-1) # Correct the range. Depth images are 12bits
        im_gray = cv2.cvtColor(im_gray,cv2.COLOR_GRAY2RGB)
        im_color = applyCustomColorMap(im_gray)
        cv2.GaussianBlur(im_color,(5,5), 0)

        self.img = im_color

    def draw_hand_at(self, position):
        cv2.circle(self.img,(int(position.x+self.width/2),int(-position.y+self.height/2)), 5, self.color, -1)

    def draw_goodbye(self):
        self.text = "Goodbye !"
        self.text_start_time = int(round(time.time() * 1000))
        
    def draw_hello(self):
        self.text = "Hello !"
        self.text_start_time = int(round(time.time() * 1000))
        
    def draw_up(self):
        self.text = "UP !"
        self.text_start_time = int(round(time.time() * 1000))
        
    def draw_down(self):
        self.text = "DOWN !"
        self.text_start_time = int(round(time.time() * 1000))
        

    
    def show_frame(self):
        
        current_time = int(round(time.time() * 1000))

        if  self.text is not None and self.text_start_time is not None:
            if (current_time - self.text_start_time) < TIME_TO_DISPLAY_TEXT:
                cv2.putText(self.img, self.text, (self.width*10/100, self.height*15/100), cv2.FONT_HERSHEY_PLAIN, 5, self.color, 8)
            else:
                self.text = None
                self.text_start_time = None
 
        cv2.imshow('Jarvis-View', self.img)
        cv2.imwrite("/tmp/kinect/kinect_jarvis.jpg",self.img)
 
