#!/usr/bin/env python

import rospy
import csv
import os
from sensor_msgs.msg import LaserScan



class dataLogger():
    def  __init__(self):
        rospy.loginfo("Setting up Data Logger")
        rospy.init_node('data_logger', anonymous=True)
#Section CSV
        try:
		self.fileH = open("/home/faps/catkin_ws/src/data_logger/output/data_log.csv", 'wt')
		self.fileWriter = csv.writer(self.fileH)
	except:
		rospy.logerr("Error opening specified output file : %s"%outFile)
		sys.exit(2)
        rospy.loginfo("Opened CSV-File")
        self.count = 1
        # Set header for CSV file 		
# Section ROS
        rospy.loginfo("Setting up subscriber")
        #Setup subscriber for laser topic
        rospy.Subscriber("/rplidar_scan", LaserScan, self.log_data)
        rate=rospy.Rate(100)
        rospy.loginfo("Done, starting loop...")
#Setup callback loop
        while not rospy.is_shutdown():
            rate.sleep()
#Setup shutdown
        rospy.loginfo("Shutdown recieved, saving data")
	self.fileH.close()
	rospy.loginfo("Done!")

    def log_data(self, msg):
        if self.count == 1:
            headerRow = ["Time", "Header_sequence", "Header_secs", "Header_nsecs", "angle_min", "angle_max", "angle_increment","time_increment", "scan_time", "range_min", "range_max" ]
            for i in range(len(msg.ranges)):
                headerRow.append("Range%s"%(i+1))
            if len(msg.intensities) >= 1:
                for i in range(len(msg.intensities)):
                    headerRow.append("Intensity%s"%(i+1))					
            self.fileWriter.writerow(headerRow)
         ##Get current data
        t = rospy.get_rostime()
        columns = [t, msg.header.seq, msg.header.stamp.secs, msg.header.stamp.nsecs, msg.angle_min, msg.angle_max, msg.angle_increment, msg.time_increment, msg.scan_time, msg.range_min, msg.range_max ]
        for i in range(len(msg.ranges)): 
            columns.append(msg.ranges[i])
        if len(msg.intensities) >= 1:
            for i in range(len(msg.intensities)): 
                columns.append(msg.intensities[i])
        self.fileWriter.writerow(columns)
        self.count = self.count + 1
        if (self.count % 100 == 0):
            rospy.loginfo("Processed %s records..."%self.count)



if __name__ == '__main__':
    dataLogger()
    rospy.spin()
