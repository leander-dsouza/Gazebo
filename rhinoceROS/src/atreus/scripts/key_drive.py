#! /usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
import time
from pynput import keyboard
from pynput.keyboard import Key

ob1 = Twist()


def forward():
    global  ob1
    #print("FORWARD")
    ob1.linear.x = 4
    ob1.linear.y = 0
    ob1.linear.z = 0

    ob1.angular.x = 0
    ob1.angular.y = 0
    ob1.angular.z = 0
    pub.publish(ob1)

def backward():
    # print("BACKWARD")
    global ob1
    ob1.linear.x = -2
    ob1.linear.y = 0
    ob1.linear.z = 0

    ob1.angular.x = 0
    ob1.angular.y = 0
    ob1.angular.z = 0

    pub.publish(ob1)


def right():
    # print("RIGHT")
    global ob1
    ob1.linear.x = 0
    ob1.linear.y = 0
    ob1.linear.z = 0

    ob1.angular.x = 0
    ob1.angular.y = 0
    ob1.angular.z = 10
    pub.publish(ob1)


def left():
    # print("LEFT")
    ob1.linear.x = 0
    ob1.linear.y = 0
    ob1.linear.z = 0

    ob1.angular.x = 0
    ob1.angular.y = 0
    ob1.angular.z = -10
    pub.publish(ob1)


def brutestop():
    ob1 = Twist()
    pub.publish(ob1)



def talker():

    def callb(key):  # what to do on key-release

        brutestop()
        return False  # stop detecting more key-releases

    def callb1(key):  # what to do on key-press
        if key == Key.up:
            forward()

        elif key == Key.down:
            backward()

        elif key == Key.right:
            right()

        elif key == Key.left:
            left()

        return False  # stop detecting more key-presses

    while not rospy.is_shutdown():

        with keyboard.Listener(on_press=callb1) as listener1:  # setting code for listening key-press
            listener1.join()

        with keyboard.Listener(on_release=callb) as listener:  # setting code for listening key-release
            listener.join()

        rate.sleep()

if __name__ == '__main__':

    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.init_node('key_teleop', anonymous=True)
    rate = rospy.Rate(50)

    try:
        talker()
    except rospy.ROSInterruptException:
        pass
