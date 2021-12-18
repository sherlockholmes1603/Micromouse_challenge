#! /usr/bin/env python3

import rospy

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
pub = None
import numpy as np
import sys, select, termios, tty
def clbk_laser(msg):
    # 
    regions = {
            'right':  min(min(msg.ranges[0:71]), 10),
            'fright': min(min(msg.ranges[71:143]), 10),
            'front':  min(min(msg.ranges[144:215]), 10),
            'fleft':  min(min(msg.ranges[216:287]), 10),
            'left':   min(min(msg.ranges[288:359]), 10),
        }
        
    take_action(regions)

def getKey():
	tty.setraw(sys.stdin.fileno())
	select.select([sys.stdin], [], [], 0)
	key = sys.stdin.read(1)
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
	return key

def take_action(regions):
    msg = Twist()
    linear_x = 0
    angular_z = 0
    
    state_description = ''
    
    if regions['front'] > 1 and regions['fleft'] > 1 and regions['fright'] > 1:
        state_description = 'case 1 - nothing'
        # linear_x = 0.6
        # angular_z = 0
    elif regions['front'] < 1 and regions['fleft'] > 1 and regions['fright'] > 1:
        state_description = 'case 2 - front'
        # linear_x = 0
        # angular_z = 0.3
    elif regions['front'] > 1 and regions['fleft'] > 1 and regions['fright'] < 1:
        state_description = 'case 3 - fright'
        # linear_x = 0
        # angular_z = 0.3
    elif regions['front'] > 1 and regions['fleft'] < 1 and regions['fright'] > 1:
        state_description = 'case 4 - fleft'
        # linear_x = 0
        # angular_z = -0.3
    elif regions['front'] < 1 and regions['fleft'] > 1 and regions['fright'] < 1:
        state_description = 'case 5 - front and fright'
        # linear_x = 0
        # angular_z = 0.3
    elif regions['front'] < 1 and regions['fleft'] < 1 and regions['fright'] > 1:
        state_description = 'case 6 - front and fleft'
        # linear_x = 0
        # angular_z = -0.3
    elif regions['front'] < 1 and regions['fleft'] < 1 and regions['fright'] < 1:
        state_description = 'case 7 - front and fleft and fright'
        # linear_x = 0
        # angular_z = 0.3
    elif regions['front'] > 1 and regions['fleft'] < 1 and regions['fright'] < 1:
        state_description = 'case 8 - fleft and fright'
        # linear_x = 0.3
        # angular_z = 0
    else:
        state_description = 'unknown case'
        rospy.loginfo(regions)

    key = getKey()
    if key == 'w':
        linear_x = 0.10
        angular_z = 0
    elif key == 's':
        linear_x = -0.10
        angular_z = 0
    elif key == 'a':
        linear_x = 0
        angular_z = 0.10
    elif key == 'd':
        linear_x = 0
        angular_z = -0.10
    elif key == 'x':
        linear_x = 0
        angular_z = 0
    rospy.loginfo(state_description)
    msg.linear.x = linear_x
    msg.angular.z = angular_z
    pub.publish(msg)

def main():
    
    global pub
    
    rospy.init_node('reading_laser')
    
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    
    sub = rospy.Subscriber('/my_mm_robot/laser/scan', LaserScan, clbk_laser)
    
    rospy.spin()

if __name__ == '__main__':
    settings = termios.tcgetattr(sys.stdin)
    main()
