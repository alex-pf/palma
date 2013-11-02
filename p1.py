# -*- coding: utf-8 -*-
import os
import csv
import rotate as R

def readPoints(fileName):
	list = []
	try:
		f1 = open(fileName, 'r')
		reader = csv.reader(f1)
		for row in reader:
				list.append(row)
		f1.close()
	except:
		print "rror 1: CSV file ton't read."
		exit(0)
	return list
	
def makeFloor(floorPoint,num):
	rez = []
	for point in floorPoint:
		rez.append(R.hRotatePoint(point,num))
	return rez

def writeToCSV(list, fName):
	f  = open(fName , "wb")
	writer = csv.writer(f, delimiter='\t', quotechar='"', quoting=csv.QUOTE_ALL)
	for row in list:
		line = sum(row,[])
		writer.writerow(line)
	f.close()


def palma(args):
	print (u'Исходне данные')
	print args.file
	print args.radius
	print args.count
	print args.seg
	print args.rotate
	print (u'Точки')
	print (u'x y z')
	basePoints = readPoints(args.file)
	thePalm = []
	for floor in xrange(0,int(args.count)):
		thePalm.append(makeFloor(basePoints, floor))
	writeToCSV(thePalm, 'result.csv' )
