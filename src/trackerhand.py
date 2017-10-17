from openni import openni2, nite2
from openni import _openni2 as c_api_openni2
from openni import _nite2 as c_api_nite2
import commandrobot as cr

MIN_MOVE_VALIDATION=50


class TrackerHand(object):
    def __init__(self, trackerNi, command_robot):
        self.trackerNi = trackerNi
        #Positive is UP, negative is down
        self.last_move = None
        self.last_position = None
        self.following_started = False
        self.hand_id = None
        self.robot = command_robot
        
    def track_hand(self, frame):


        if frame.gestures:

                print("gestures !")
                
                for gesture in frame.gestures:

                    if gesture.state == c_api_nite2.NiteGestureState.NITE_GESTURE_STATE_COMPLETED:
                        
                        print("New gesture complete")
                        
                        if gesture.type == nite2.GestureType.NITE_GESTURE_WAVE:
                            print("Wave !!")
                            print gesture
                            self.following_started=not self.following_started

                            if self.following_started:
                                self.last_position = gesture.currentPosition.y
                                self.hand_id = self.trackerNi.start_hand_tracking(gesture.currentPosition)
                            else:
                                #Robot say Goodbye with arm and hand
                                self.robot.say_goodbye()
                                self.trackerNi.stop_hand_tracking(self.hand_id)

        if frame.hands :

            for hand in frame.hands:

                if hand.state == c_api_nite2.NiteHandState.NITE_HAND_STATE_TRACKED:

                
                    new_position = hand.position.y

                    if new_position != self.last_position:

                        new_move, last_move = self.is_new_move(new_position)
                        
                        if new_move:
                            self.last_position = new_position
                            self.last_move = last_move

                            if last_move < 0:
                                self.robot.move_right_arm_down()
                            else:
                                self.robot.move_right_arm_up()

                
                elif hand.state == 6:
                    print "hand lost"
                    self.trackerNi.stop_hand_tracking(self.hand_id)
                    self.following_started = False

    def is_new_move(self, new_position):

        #print "is new move : last_position = {0}, new_position = {1}".format(self.last_position, new_position)
        
        new_move = False
        last_move = 0

        if self.last_position != new_position :
            last_move = new_position - self.last_position

        if  abs(last_move) >  MIN_MOVE_VALIDATION and (self.last_move is None or (last_move * self.last_move < 0)):
            new_move = True

        return [new_move, last_move]