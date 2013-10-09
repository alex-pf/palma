# -*- coding: utf-8 -*-
import os



def readPoints(fileName):
	f = open(fileName)
	points = f.read()
	return points

def offsetPoint(point, axis, distance):
	point[axis] = point[axis]+distance
	return point


def palma(args):
	print (u'Исходне данные')
	print args.file
	print args.radius
	print args.count
	print args.seg
	print args.rotate
	print (u'Точки')
	print (u'x y z')
	pointList = readPoints(args.file)
	print pointList[0]
        
