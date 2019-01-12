
import csv
import math
import os
import cv2




#change the path to where you would like the data to output to

summary = open("D:/Programing_project/Science_fair/results.txt","w+")


#change this to the path of your dataset
topfolder = "D:/Programing_project/vot2016/"


#make sure this is the same as before, in the same order
tracker_types = ['KCF','TLD', 'MEDIANFLOW', 'MOSSE']







def compare (data,truth,folder):

	DataW = data[2]
	DataH = data[3]
	Datax = data[0]
	Datay = data[1]


	truthW = truth[2]
	truthH = truth[3]
	truthx = truth[0]
	truthy = truth[1]



	centertx = truthx + (truthW/2)
	centerty = truthy + (truthH/2)

	centerdx = Datax + (DataW/2)
	centerdy = Datax + (DataH/2)






	cent_dist = math.sqrt((centerdx  - centertx)**2 + (centerdy -centerty)**2)






	image_file = folder + "00000001.jpg" 


	frame = cv2.imread(image_file)
	height, width = frame.shape[:2]





	diag = math.sqrt(width**2 + height**2)


	return (cent_dist / diag *100) 














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




subdir = os.listdir(topfolder)



for y in subdir:


	if y == "singer2": continue


	folder = topfolder + y + "/" 
	ground_file = folder + "groundtruth.txt"
	truth = open(ground_file)

	truth_rects = []
	reader = csv.reader(truth)
	for row in reader:
		x1 = float(row[0])
		y1 = float(row[1])
		x2 = float(row[2])
		y2 = float(row[3])
		x3 = float(row[4])
		y3 = float(row[5])
		x4 = float(row[6])
		y4 = float(row[7])

		truths = (x1,y1,x2,y2,x3,y3,x4,y4)
		truth_rect = producebox(truths)

		truth_rects.append(truth_rect)


	for tracker_type in tracker_types:
	
		data = []


		datafile= open(folder + tracker_type + ".output" ,"r")
		reader = csv.reader(datafile)
		for row in reader:
			frame = int(row[0])
			fps = float(row[1])
			L = float(row[2])
			T = float(row[3])
			W = float(row[4])
			H = float(row[5])


			if L != -1: 
				pos = compare ((L,T,W,H),truth_rects[frame -1],folder)
				data.append((frame,fps,pos))


		fps_sum = 0.0
		pos_sum = 0.0

		for d in data:
			
			fps_sum = fps_sum + d[1]


			pos_sum = pos_sum + d[2]


		fps_avg = 0
		pos_avg = 0 

		if len(data) != 0:
			fps_avg = (fps_sum/len(data))
			pos_avg = (pos_sum/len(data))
	

		summary.write ("%s %s fps:%f pos:%f\n" %(y,tracker_type,fps_avg,pos_avg))
		print("%s %s fps:%f pos:%f" %(y,tracker_type,fps_avg,pos_avg))
summary.close()