#! /usr/bin/python

import rospy
from geometry_msgs.msg import Twist
from rospy import Publisher, Subscriber
from turtlesim.msg import Pose
import math
import numpy as np


class Turtle_follower:
    def __init__(self):
        self.subscriber_turtle1 = Subscriber('/turtle1/pose', Pose, self.follow)
        self.publisher = Publisher('/leo/cmd_vel', Twist, queue_size=10)
        self.subscriber_leo = Subscriber('/leo/pose', Pose, self.update_pose)
        self.pose = Pose()

    def update_pose(self, pose):
        self.pose = pose
        
    def new_ang(self, new_theta):
    	ang = new_theta - self.pose.theta
    	while ang > np.pi:
            ang -= 2 * np.pi
        while ang < - np.pi:
            ang += 2 * np.pi
        return ang

    def follow(self, pose):
        msg = Twist()
        p1, p2 = np.array([pose.x, pose.y]), np.array([self.pose.x, self.pose.y])
        distance = np.linalg.norm(p1-p2)
        
        if distance > 1:
            new_theta = math.atan2(pose.y - self.pose.y, pose.x - self.pose.x)
                       
            msg.linear.x = min(distance, 2)
            msg.angular.z = self.new_ang(new_theta)
            self.publisher.publish(msg)

rospy.init_node('turtle')
Turtle_follower()

rospy.spin()
