#! /usr/bin/env python
import rospy
from geometry_msgs.msg import Vector3
from sensor_msgs.msg import Imu
from barc.msg import ECU
import numpy as np
from marvelmind_nav.msg import hedge_pos
from math import atan2, sqrt

global LA_tol, LA_d
LA_d = .5
LA_tol = .1

#wait_for_heading_angle = rospy.get_param('heading_angle_flag')
#while wait_for_heading_angle:
#	wait_for_heading_angle = rospy.get_param('heading_angle_flag')

def get_xy(msg):
    global curr_x,curr_y
    curr_x = msg.x_m
    curr_y = msg.y_m

def get_Psi(msg):
    global curr_psi
    curr_psi = msg.z

def grab_waypoints(msg):
    global wp_list
    wp_list = msg.Data

def find_rad_of_curve(x,y):
    global curr_x,curr_y,curr_psi
    loc_x = (x-curr_x)*cos(curr_psi) - (y-curr_y)*sin(curr_psi)
    loc_y = (x-curr_x)*sin(curr_psi) + (y-curr_y)*cos(curr_psi)
    loc_dist = sqrt(loc_x^2 + loc_y^2)
    return (loc_dist^2)/(2*loc_x)

def look_ahead():
        global wp_list, curr_x, curr_y, LA_d, LA_tol
	within_bubble = [[v[0], v[1],find_rad_of_curve(v),sqrt((v[0]-curr_x-LA_d)^2+(v[1]-curr_y-LA_d)^2)] for v in wp_list if abs(v[0]-curr_x-LA_tol)<=LA_tol and (v[1] - curr_y-LA_tol)<=LA_tol]
	ordered_vals = sorted(within_bubble, key=lambda obj: obj[3])
	for i in ordered_vals:
		# some logic to check which one actually is the right goal x,y
		# output of this for loop should be the goal x,y
	find_rad_of_curve(goal_x,goal_y)
# motion logic that assigns a given v/w = r based on r from desired curvature
# last step is to make sure this happens every second for whatever set of
	# waypoints it is provided

def pure_pursuit():
    global curr_x,curr_y,curr_psi
    global wp_list, LA_d, LA_tol #look ahead distance

    rospy.init_node('pure_pursuit')
    rospy.Subscriber('hedge_pos',hedge_pos,get_xy,queue_size=10)
    rospy.Subscriber('/euler_angles',Vector3,get_Psi,queue_size=10)
    rospy.Subscriber('/waypoints',___,grab_waypoint,queue_size=10)
    pub = rospy.Publisher('/ecu_pwm',ECU,queue_size=10)

    rospy.Subscriber('
    rate = rospy.Rate(10)

    max_steer = np.pi/6
    K = 400/max_steer
    V = 1

    while not rospy.is_shutdown():# and r.successful():
#        msg.servo = 1500 - delta*K #/ 10 * 800
        pub.publish(msg)
        rate.sleep()


if __name__ == '__main__':
    try:
        pure_pursuit()
    except rospy.ROSInterruptException:
        pass
