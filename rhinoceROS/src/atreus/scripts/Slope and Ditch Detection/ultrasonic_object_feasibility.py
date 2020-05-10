#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Range
from geometry_msgs.msg import Twist
from math import atan, pi, sin, degrees

threshold = 0.5

ob1 = Twist()

psd1L = 0.00
psd1R = 0.00
psd2L = 0.00
psd2R = 0.00

X1_slope = 0.00
slope_angle = 0.00
ditch_depth =0.00
X2o = 0.79
X2T = 0.02
X1o = 0.95
X1T = 0.02

alpha = 45
L = 0.1326




def callback_1l(msg):
    global psd1L
    psd1L = round(msg.range,2)
    
def callback_1r(msg):
    global psd1R
    psd1R = round(msg.range,2)

def callback_2l(msg):
    global psd2L
    psd2L = round(msg.range,2)

def callback_2r(msg):
    global psd2R
    psd2R = round(msg.range,2)



def calculate():
    global psd1L, psd1R, psd2L, psd2R, slope_angle, ditch_depth, X1_slope
    X1 = psd1L
    X2 = psd2L

    #FLAT CONDITION:
    if abs(X1-X1o)<=X1T and abs(X2-X2o)<=X2T:
        print("FLAT")

    #DITCH CONDITION:
    if X1-X1o>X1T and X2-X2o>X2T and abs(X1-X1o)-X1T<abs(X2-X2o)+X2T:
        ditch_depth = (X2o-X2)*sin(pi/2)
        print("DITCH APPROACHING","DITCH DEPTH = " + str(ditch_depth) + "m")

    #SLOPE CONDITION:
    if abs(X1-X1o)>X1T and abs(X2-X2o)>X2T and X1-X1o-X1T < X2-X2o+X2T:
        slope_angle = 90 - alpha - degrees(atan((psd1L - psd2L) / L))
        if -5 < slope_angle < 5:
            return
        print("UPWARD SLOPE APPROACHING", "SLOPE ANGLE = " + str(slope_angle) + "deg")


    if abs(X1-X1o)>X1T and abs(X2-X2o)>X2T and X1-X1o-X1T > X2-X2o+X2T:
        slope_angle = 90 - alpha - degrees(atan((X1 - X2) / L))
        if -5 < slope_angle < 5:
            return
        print("DOWNWARD SLOPE APPROACHING", "SLOPE ANGLE = " + str(slope_angle) + "deg")



def listener():
    rospy.Subscriber("/psd1l_topic", Range, callback_1l)
    rospy.Subscriber("/psd1r_topic", Range, callback_1r)
    rospy.Subscriber("/psd2l_topic", Range, callback_2l)
    rospy.Subscriber("/psd2r_topic", Range, callback_2r)

    while not rospy.is_shutdown():
        calculate()
        rospy.sleep(0.01)


if __name__ == '__main__':
    try:

        rospy.init_node('Communication', anonymous=True, disable_signals=True)
        rate = rospy.Rate(50)

        listener()

    except rospy.ROSInterruptException:
        pass
