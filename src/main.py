#!/usr/bin/python

"""
    Main module of the Kinect Jarvis feature
"""
import sys
import getopt
import cv2
import commandrobot as cr
import trackerhand as th
from openni import openni2, nite2
from openni import _openni2 as c_api
import displaydepth as dp

def main(argv):
    """
        Main function that do the OpenNI and Nite loop

        parameters
        -------------------
        argv : should contains parameters to configure the broker
                -h : the hostname
    """
    
    #Read the parameters
    
    robot = cr.CommandRobot()

    try:
        opts, args = getopt.getopt(argv,"h",["hostname="])
    except getopt.GetoptError:
        print ('main.py -h <hostname>')
        sys.exit(2)

    for opt, arg in opts:
      if opt in ("-h", "--hostname"):
         robot.hostname = arg


    # Init OpenNi2 and Nite 2
    openni2.initialize()     # can also accept the path of the OpenNI redistribution
    nite2.initialize()

    dev = openni2.Device.open_any()
    print dev.get_device_info()


    try:
        handTracker = nite2.HandTracker(dev)
        handTracker.start_gesture_detection(nite2.GestureType.NITE_GESTURE_WAVE)

    except utils.NiteError as ne:
        logging.error("Unable to start the NiTE human tracker. Check "
                     "the error messages in the console. Model data "
                     "(s.dat, h.dat...) might be inaccessible.")
        print(ne)
        sys.exit(-1)

    gestureStarted = False
    oldPosition = None
    newPosition = None
    handId = None

    tracker_hand = th.TrackerHand(handTracker,robot)
    depth_display =  dp.DisplayDepth()

    cv2.namedWindow('Jarvis-View')

    while True:

        key = cv2.waitKey(10)

        if key==27:
            break

        frame = handTracker.read_frame()  
        img = depth_display.build_img(frame.depth_frame)
        tracker_hand.track_hand(frame, img)
        depth_display.show_frame(img)
        
                    
    nite2.unload()
    openni2.unload()

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main(sys.argv[1:])