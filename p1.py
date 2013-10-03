# -*- coding: utf-8 -*-
import os


def readPoints(fileName):
	f = open(fileName)
	points = f.read()
	return points
	
def palma(args):
	print args.file
	print args.radius
	print args.count
	print args.seg
	print args.rotate