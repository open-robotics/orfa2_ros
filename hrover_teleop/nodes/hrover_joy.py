#!/usr/bin/env python

import roslib; roslib.load_manifest('hrover_teleop')
import rospy

from sensor_msgs.msg import Joy
from orfa2_msgs.msg import Motor


MODE_TANK = 0
MODE_TWIST = 1

joy_mode = MODE_TANK

def main():
    pub = rospy.Publisher('serial_node/motor/integrated', Motor)
    rospy.init_node("hrover_joy")

    def joy_cb(j):
        global joy_mode

        m = Motor()
        m.header.stamp = rospy.Time.now()

        if j.buttons[9] == 1:
            joy_mode = MODE_TWIST if joy_mode == MODE_TANK else MODE_TANK

        if joy_mode == MODE_TANK:
            l = int(j.axes[1] * 1000)
            r = int(j.axes[4] * 1000)

        else:
            x, y = j.axes[0], j.axes[1]

            l = int(y * 1000 - x * 500)
            r = int(y * 1000 + x * 500)

        if l > 1000: l = 1000
        elif l < -1000: l = -1000

        if r > 1000: r = 1000
        elif r < -1000: r = -1000

        m.value = [l, r]
        pub.publish(m)

    rospy.Subscriber('joy', Joy, joy_cb)
    rospy.spin()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException: pass
