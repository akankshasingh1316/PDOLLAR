# coding=utf-8
import os
import sys
import argparse
import shutil
from dollarpy import Recognizer, Template, Point

def add_template(gestureFile):
	source = os.path.join(gestureFile)
	# print source
	destination = os.path.join('Templates')
	#print destination
	filename = gestureFile.split('\\')[-1]
	# print filename
	destination_path = os.path.join(destination,filename)
	print destination_path
	if(os.path.isfile(destination_path)):
		print "Template Already Exists."
	else:
		shutil.copy(gestureFile, destination)
		print "Template Added."

def clear_templates():
	source = os.path.join('Templates')
	for files in os.listdir(source):
		files = os.path.join(source, files)
		# print files
		os.remove(files)
	print "All Templates Removed."
	
def read_template_points(event_points):

	all_templates = []

	path = os.path.join('Templates')
	if (os.listdir(path)==[]):
		print "No Templates."
	else:
		for filename in os.listdir(path):
			new_path = path + "/" + filename
			TemplateObject = open(new_path, "r")
			
			line =  TemplateObject.readline()
			filename = line.strip()
			
			stroke_count = 0
			template_points = []
			
			for line in TemplateObject:
				
				line = line.strip()
				row = line.split(',')
				
				if (line == 'BEGIN'):
					stroke_count = stroke_count + 1
				elif (line == 'END'):
					continue
				else:
					row = line.split(',')
					x = int(row[0])
					y = int(row[1])
					template_points.append(Point(x,y,stroke_count))
			
			new_template = Template(filename, template_points)
			all_templates.append(new_template)

		recognizer = Recognizer(all_templates)
		result = recognizer.recognize(event_points)
		print(result)  # Output: ('X', 0.733770116545184)


def read_event_points(event_file):
	
	event_points = []
	stroke_count = 0
	# event_file = "D:/College/Semester 8/Natural User Interaction/Assignment1_$P/A1_TestingFiles/eventfiles/arrowhead_eventfile.txt"
	EventObject = open(event_file, "r")

	for line in EventObject:
		
		line = line.strip()
		
		if (line == 'MOUSEDOWN'):
			stroke_count = stroke_count + 1
		elif (line == 'MOUSEUP'):
			continue
		elif (line == 'RECOGNIZE'):
			result = read_template_points(event_points)
			# print result
			event_points = []
			stroke_count = 0
		else:
			row = line.split(',')
			x = int(row[0])
			y = int(row[1])
			event_points.append(Point(x,y,stroke_count))
	# print event_points

def main(argv):
	
	if (len(sys.argv) <= 1 or sys.argv[1] == '-h'):
		# print str(sys.argv[1])
		print "\nNo Arguments Passed.Pass Arguments as per Help Screen\n\n" \
		"-h			Display Help Message Again\n\n" \
		"-t <gestureFile>	Add A Template. Please specify the path of the \n			<gestureFile>\n\n" \
		"-r			Clear All Templates\n\n"\
		"<EventStream>		Recognize Gesture from Eventream. Please specify the path \n			of the <EventStream>\n\n"
	
	if (len(sys.argv) > 1):
		if (sys.argv[1] == '-r'):
			clear_templates()
		if (sys.argv[1] == '-t'):
			if(len(sys.argv) == 2):
				print "Invalid Input. Template File Not Specified."
			else:
				template_name = str(sys.argv[2])
				# path = os.path.join("A1_TestingFiles\gestureFiles")
				# template_path = os.path.join("A1_TestingFiles\gestureFiles",template_name)
				if (os.path.isfile(template_name)):
					add_template(template_name)
				else:
					print "Incorrect Template File Specified. No Such Template File Exists."
		elif (sys.argv[1].endswith('.txt')):
			if(os.path.isfile(sys.argv[1])):
				eventstream_name = str(sys.argv[1])
				# eventstream_path = os.path.join("A1_TestingFiles\eventfiles",eventstream_name)
				# print eventstream_path
				read_event_points(eventstream_name)
			else:
				print "Incorrect EventStream Specified. No Such EventStream Exists."

if __name__ == "__main__":
   main(sys.argv[1:])