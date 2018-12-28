import cv2
import sys
import os
import csv


tracker_types = ['KCF','TLD', 'MEDIANFLOW', 'MOSSE']


def get_info(file):

	f = open(file)
	reader = csv.reader(f)
	for row in reader:
		x1 = float(row[0])
		y1 = float(row[1])
		x2 = float(row[2])
		y2 = float(row[3])
		x3 = float(row[4])
		y3 = float(row[5])
		x4 = float(row[6])
		y4 = float(row[7])
		return (x1,y1,x2,y2,x3,y3,x4,y4)



def createtracker(type):

	
	tracker_type = tracker_types[type]
	
	if tracker_type == 'BOOSTING':
		tracker = cv2.TrackerBoosting_create()
	if tracker_type == 'MIL':
		tracker = cv2.TrackerMIL_create()
	if tracker_type == 'KCF':
		tracker = cv2.TrackerKCF_create()
	if tracker_type == 'TLD':
		tracker = cv2.TrackerTLD_create()
	if tracker_type == 'MEDIANFLOW':
		tracker = cv2.TrackerMedianFlow_create()
	if tracker_type == 'GOTURN':
		tracker = cv2.TrackerGOTURN_create()
	if tracker_type == 'MOSSE':
		tracker = cv2.TrackerMOSSE_create()
	if tracker_type == "CSRT":
		tracker = cv2.TrackerCSRT_create()


	return (tracker,tracker_type)




def producebox(corners):
	

	x1 = corners[0]
	y1 = corners[1]
	x2 = corners[2]
	y2 = corners[3]
	x3 = corners[4]
	y3 = corners[5]
	x4 = corners[6]
	y4 = corners[7]

	left = min ([x1,x2,x3,x4])
	top = min ([y1,y2,y3,y4])

	right = max ([x1,x2,x3,x4])
	bottom = max ([y1,y2,y3,y4])


	H = (bottom - top) + 1
	W = (right - left) + 1

	bbox = (left,top,W,H)
	return bbox


def runalgorithm(folder,bbox,trackertype):

	tracker, tracker_type = createtracker(trackertype)

	f= open(folder + tracker_type + ".output" ,"w+")

	filename = folder + "00000001.jpg" 

	
	frame = cv2.imread(filename)


	# Initialize tracker with first frame and bounding box
	ok = tracker.init(frame, bbox)

	fileindex = 2




	while True:
		
		Running_output = str(fileindex) + ","

		filename = folder + "%08d.jpg" %fileindex

		fileindex = fileindex + 1

		# Read a new frame
		frame = cv2.imread(filename)
		if frame is None:
			break

		# Start timer
		timer = cv2.getTickCount()

		# Update tracker
		ok, bbox = tracker.update(frame)

		# Calculate Frames per second (FPS)
		fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
		Running_output = Running_output + str(fps) + ","

		# Draw bounding box
		if ok:
			# Tracking success
			p1 = (int(bbox[0]), int(bbox[1]))
			p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
			cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)




			Running_output = Running_output + "%d,%d,%d,%d" %(bbox[0], bbox[1], bbox[2], bbox[3])


			#output rectangle to file

		else :
			# Tracking failure
			cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
			Running_output = Running_output = Running_output + "-1,-1,-1,-1" 

			#output failed to file

		# Display tracker type on frame
		cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2)

		# Display FPS on frame
		cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2)

		# Display result
		cv2.imshow("Tracking", frame)

		# Exit if ESC pressed
		k = cv2.waitKey(1) & 0xff
		if k == 27 : break
	


		f.write(Running_output + " \n")


	f.close()




		











topfolder = "D:/Programing_project/vot2016/"
subdir = os.listdir(topfolder)




	

for y in subdir:


	if y == "singer2": continue
	
	#folder = topfolder + "singer2/" 
	folder = topfolder + y + "/" 
	ground_file = folder + "groundtruth.txt"

	#folder = topfolder + "ball1/"

	#corners = (496,419,536,419,536,461,496,461)
	corners = get_info(ground_file)



	for x in range (0, len(tracker_types)):

		bbox = producebox(corners)

		runalgorithm(folder,bbox,x)
	#break

	





