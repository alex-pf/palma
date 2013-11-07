# -*- coding: utf-8 -*-
import os
import csv
import rotate as R
import draw_stl as stl

def readPoints(fileName):
	list = []
	try:
		f1 = open(fileName, 'r')
		reader = csv.reader(f1, delimiter='\t')
		for row in reader:
				list.append(row)
		f1.close()
	except:
		print "rror 1: CSV file ton't read."
		exit(0)
	rez=[]
	for row in list:
		line=[]
		for point in row:
			line.append(float(point))
		rez.append(line)
	return rez
	
def makeFloor(floorPoint,num, angle, seg):
	rez = []
	for point in floorPoint:
		p = R.hRotatePoint(point,num, angle)
		p[2] = num*seg
		rez.append(p)
	return rez

def makeCeiling(floor, seg):
	rez = []
	for point in floor:
		rez.append([point[0],point[1],point[2]+seg])
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
	floor=0
	while floor < int(args.count):
		f = makeFloor(basePoints, floor, args.rotate, args.seg)
		c = makeCeiling(f, args.seg)
		thePalm.append(f)
		thePalm.append(c)
		floor+=1
	'''
	writeToCSV(thePalm, 'result.csv' )
	print thePalm
	print '---------------------'
	print stl.setPointList('result.csv')
	'''
	writeToCSV(thePalm, 'result.csv' )
	R = stl.createSTLtabe(thePalm)
	stl.writeToSTL(R,'cube2.stl')
