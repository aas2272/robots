#!/usr/bin/env python

'''
Talker node that publishes nlp input data
'''

import rospy

#from second_law.msg import Nlp_input
from std_msgs.msg import String
from sys import argv

def talker(data):
	#publishes NLP parsed data
	pub = rospy.Publisher('nlp_data', String, queue_size=10)
	rospy.init_node('nlp_talker', anonymous = True)

	print "NLP input received of: ", data

	rospy.loginfo(data)

	pub.publish(data)

if __name__ == '__main__':
	try:
		script, filename = argv
		txt = open(filename,"r")
		msg = txt.readlines()
		talker(msg[0])
	except rospy.ROSInterruptException:
		pass
