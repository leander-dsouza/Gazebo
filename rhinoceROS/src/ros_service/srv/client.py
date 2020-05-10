#!/usr/bin/env python
import rospy
from ros_service.srv import Path


global coords

def gps_client():
    rospy.wait_for_service('gps_service')
    try:
        ob1 = rospy.ServiceProxy('gps_service', Path)
        resp = ob1()
        return resp.lat, resp.lon
    except rospy.ServiceException:
	print("Error")
        pass

if __name__ == "__main__":
    print(gps_client())
