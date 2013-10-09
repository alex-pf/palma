# -*- coding: utf-8 -*-
import os
import sys
import getopt
import argparse
'''
myPath = os.path.join(os.environ.get("GIT_HOME") + u"palma")
if not myPath in sys.path:
	sys.path.append(myPath)
'''
import p1
	
def main():
	p1.palma(args)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	#parser.add_argument('-h', dest='--help', action=p1.help() )		#Помощь (эта подсказка)
	parser.add_argument('-f', '--file', help=(u'Имя файла с точками (Должен лежать в директории со скриптами)') )
	parser.add_argument('-r', '--radius', help=(u'Радиус изгиба пальмы') )
	parser.add_argument('-c', '--count', help=(u'Количество сегментов') )
	parser.add_argument('-s', '--seg', help=(u'Высота сегмента (град)') )
	parser.add_argument('-o', '--rotate', help=(u'Поворот сегмента (град)') )
	args = parser.parse_args()
	main()
