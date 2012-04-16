#!/usr/bin/env python

import roslib; roslib.load_manifest('hrover_teleop')
import rospy

from sensor_msgs.msg import Joy
from orfa2_msgs.msg import Motor

def main():
    pub = rospy.Publisher('serial_node/motor/integrated', Motor)
    rospy.init_node("hrover_joy")

    def joy_cb(j):
        m = Motor()
        m.header.stamp = rospy.Time.now()
        m.speed[0] = int(j.axes[1] * 1000)
        m.speed[1] = int(j.axes[4] * 1000)
        pub.publish(m)

    rospy.Subscriber('joy', Joy, joy_cb)
    rospy.spin()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException: pass
