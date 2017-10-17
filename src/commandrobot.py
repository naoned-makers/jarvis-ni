import paho.mqtt.client as mqtt
import socket

DEFAULT_BROKER_HOSTNAME = "naonedmakers"
CMD_MOVE_LEFT_ARM_NAME = "im/command/leftarm/move"
CMD_MOVE_RIGHT_ARM_NAME = "im/command/rightarm/move"
CMD_MOVE_LEFT_HAND_NAME = "im/command/lefthand/move"
CMD_MOVE_RIGHT_HAND_NAME = "im/command/righthand/move"

CMD_UP_RIGHT_ARM_NAME = "im/command/rightarm/up"
CMD_DOWN_RIGHT_ARM_NAME = "im/command/rightarm/down"

class CommandRobot(object):
    """
        Launch command to the broker
    """

    def __init__(self, hostname = DEFAULT_BROKER_HOSTNAME):
        print "_init robot"
        self.hostname = hostname
        self.mqtt_client = mqtt.Client(client_id="kinect_"+socket.gethostname())
        self.mqtt_client.connect(hostname, 1883, 60)

    def move_right_arm_up(self):
        """
            Method to publish a move event to the broker
        """
        self.mqtt_client.publish(CMD_UP_RIGHT_ARM_NAME, "{\"origin\":\"kinect\"}")
        print "move up"


    def move_right_arm_down(self):
        """
            Method to publish a move event to the broker
        """
        self.mqtt_client.publish(CMD_UP_RIGHT_ARM_NAME, "{\"origin\":\"kinect\"}")
        print "move down"


    def say_goodbye(self):
        print ("Goodbye")

        self.mqtt_client.publish(CMD_MOVE_RIGHT_ARM_NAME, "{\"origin\":\"kinect\"}")
        self.mqtt_client.publish(CMD_MOVE_RIGHT_HAND_NAME, "{\"origin\":\"kinect\"}")
