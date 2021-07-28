#!/usr/bin/env python

from __future__ import print_function

import threading

import roslib; roslib.load_manifest('final')
import rospy

from geometry_msgs.msg import Twist
from std_msgs.msg import String

import sys, select, termios, tty

msg = """
Reading from the keyboard  and Publishing to Twist!
---------------------------
Moving around:
   u    i    o
   j    k    l
   m    ,    .

For Holonomic mode (strafing), hold down the shift key:
---------------------------
   U    I    O
   J    K    L
   M    <    >

t : up (+z)
b : down (-z)

anything else : stop

q/z : increase/decrease max speeds by 10%
w/x : increase/decrease only linear speed by 10%
e/c : increase/decrease only angular speed by 10%

CTRL-C to quit
"""

moveBindings = {
        'y':(1,0,0,0),
        'u':(1,0,0,-1),
        'g':(0,0,0,1),
        'j':(0,0,0,-1),
        't':(1,0,0,1),
        'n':(-1,0,0,0),
        'm':(-1,0,0,1),
        'b':(-1,0,0,-1),
        'O':(1,-1,0,0),
        'I':(1,0,0,0),
        'J':(0,1,0,0),
        'L':(0,-1,0,0),
        'U':(1,1,0,0),
        '<':(-1,0,0,0),
        '>':(-1,-1,0,0),
        'M':(-1,1,0,0),
        't':(0,0,1,0),
        'b':(0,0,-1,0),
    }

speedBindings={
        'q':(1.1,1.1),
        'z':(.9,.9),
        'w':(1.1,1),
        'x':(.9,1),
        'e':(1,1.1),
        'c':(1,.9),
    }



def callback(key):
    rospy.loginfo(key.data)

    speed = rospy.get_param("~speed", 0.2)
    turn = rospy.get_param("~turn", 0.5)
    repeat = rospy.get_param("~repeat_rate", 0.0)

    x = 0
    y = 0
    z = 0
    th = 0

    key = key.data

    if key in moveBindings.keys():
        x = moveBindings[key][0]
        y = moveBindings[key][1]
        z = moveBindings[key][2]
        th = moveBindings[key][3]
    elif key in speedBindings.keys():
        speed = speed * speedBindings[key][0]
        turn = turn * speedBindings[key][1]
    
    rospy.loginfo(x)
    twist = Twist()
    # Copy state into twist message.
    twist.linear.x = x * speed
    twist.linear.y = y * speed
    twist.linear.z = z * speed
    twist.angular.x = 0
    twist.angular.y = 0
    twist.angular.z = th * turn

    rospy.loginfo(twist )
    publisher.publish(twist)


if __name__=="__main__":
    rospy.init_node('final')
    subscriber = rospy.Subscriber('movement', String, callback)
    publisher = rospy.Publisher('cmd_vel', Twist, queue_size = 1)
    rospy.spin()
