﻿# Волшебная строчка превращающая кодировку файла в Utf-8 без BOM , без неё NetBeans тупит, не понимая кирилицу

__author__="alex"
__date__ ="$Mar 28, 2014 10:00:20 AM$"

from math import * 

# Принять файл на вход, распарсить получить полилинии - контуры
def get_base(fileName):
    file = open(fileName,'r')
    stringList = file.readlines()
    polylineList = [] # Результат - список полилиний в виде списка списков списков
    for str in stringList:
        polyline = []
        for point in str.strip('\n').split('    '):
            P=[]
            for ord in point.split():
                P.append(float(ord))
            polyline.append(P)
        polylineList.append(polyline)
    return polylineList

# Принять параметры: количество этажей, высота этажей в градусах, смещения центра изгиба пальмы, угол поворота этажа

def get_param_list():
    param_list= {'count':9,'height':2,'offset':20000,'rotate':30,'zoom':0.1}
    return param_list

def zoom(polyline,z):
    rez = []
    z = 1-z
    for point in polyline:
        rez.append([point[0]*z,point[1]*z,point[2]])
    return rez
    

def h_rotate_polyline(polyline,angle):
    res = []
    angle = radians(float(angle))
    for pts in polyline:
        rezPoint = []
        rezPoint.append(pts[0]*cos(angle) - pts[1]*sin(angle))
        rezPoint.append(pts[1]*cos(angle) + pts[0]*sin(angle))
        rezPoint.append(pts[2])
        res.append(rezPoint)
    return res

def v_rotate_polyline(polyline,angle,offset):
    angle = radians(float(angle))
    resPolyline = []
    for point in polyline:
        ofsetPoint = [point[0]+offset,point[1],point[2]]
        rotatePoint = []
        rotatePoint.append(ofsetPoint[0]*cos(angle) - ofsetPoint[2]*sin(angle))
        rotatePoint.append(ofsetPoint[1])
        rotatePoint.append(ofsetPoint[2]*cos(angle) + ofsetPoint[0]*sin(angle))
                
        normalPoint = [rotatePoint[0]-offset,rotatePoint[1],rotatePoint[2]]
        resPolyline.append(normalPoint) 
    return resPolyline


def extension_wall(polylineList, angle, offset, floorNum):
    
    topPolylineList = []
    downPolylineList = []
    for polyline in polylineList:
        topPolylineList.append(v_rotate_polyline(polyline,angle*(floorNum+1),offset))
        downPolylineList.append(v_rotate_polyline(polyline,angle*floorNum,offset))
    poligonList = []
    for i in xrange(len(polylineList)):
        for j in xrange(len(polylineList[i])):
            rect1 = [downPolylineList[i][j-1],topPolylineList[i][j],downPolylineList[i][j]]
            rect2 = [downPolylineList[i][j-1],topPolylineList[i][j-1],topPolylineList[i][j]]
            poligonList.append(rect1)
            poligonList.append(rect2)
            
#    for polyline in downPolylineList:
#        ppp = rectPolygon(polyline)
#        print ppp
#        poligonList += ppp
#    for polyline in topPolylineList:
#        poligonList += rectPolygon(polyline[::-1])
    return poligonList
    
def get_stl(rectList):
    stlText = []
    l1 = '    facet normal 1 0 0\n        outer loop'
    l2 = '        endloop\n    endfacet'
    stlText.append('solid OpenSCAD_Model')
    for rect in rectList:
        stlText.append(l1)
        for point in rect:
            stlText.append('            vertex ' + str(point[0]) + ' ' + str(point[1]) + ' ' + str(point[2]))
        stlText.append(l2)
    stlText.append('endsolid OpenSCAD_Model')
    return stlText

def get_palma(name):
    polilyneList = get_base(name + '.txt')
    param =  get_param_list()
    floorList = []
    for f in xrange(param.get('count')):
        floor = []
        for pl in polilyneList:
            polyline = pl
            polyline = zoom(polyline,param.get('zoom')*f)
            polyline = h_rotate_polyline(polyline, param.get('rotate')*f )
            floor.append(polyline)
        floorList.append(floor)
    V = []
    for f in xrange(len(floorList)):
        V = V + (extension_wall(floorList[f], param.get('height'), param.get('offset'), f) )
    stl = get_stl(V)
    stlFile = open(name+'.stl','w')
    stlFile.write('\n'.join(stl))
    stlFile.close()



def f(P,M,L):
    try:
        a = (L[0]-M[0])+M[0]
        b = (L[1]-M[1])*(P[0]-M[0])
        return a*b
    except:
        print 'ERROR:'
        print P
        print M
        print L
        return 'ERROR'


def u(P,G,M,L):
    if f(P,M,L)* f(G,M,L)>0:
        return True
    else:
        return False


def point_in_rect(p,a,b,c):
    # Обход по часовой стрелке!
    if u(p,a,b,c) and u(p,b,c,a) and u(p,c,a,b):
        return True
    else:
        return False

def get_angle(a,b,c):
    # Вычисляем угол abc b - вершина
    # смещаем b в 0,0
    a = [a[0]-b[0],a[1]-b[1]]
    c = [c[0]-b[0],c[1]-b[1]]
    # Остались точка a и с
    at1 = atan2(a[0],a[1])
    at2 = atan2(c[0],c[1])
    ang =  at1  - at2
    print 'a={0}  b={1}'.format(a,c)
    print '{0} - {1} = {2}'.format(at1,at2,ang)
    return ang # Если ang > 0 значит угол меньше 180 градусов
    
def rectPolygon(polyline):
    if len(polyline)==3:
        print polyline
        return [polyline]
    else:
        rectList = []
        litePL = [] +  polyline
        a = litePL.pop(-2)
        b = litePL.pop(-1)
        c = litePL.pop(0)
        print [a,b,c]
        ang = get_angle(a,b,c)
        ln = len([p for p in litePL if point_in_rect(p,a,b,c)])
        if ang>0 and ln==0:
            polyline.pop(-1)
            rectList.append([a,b,c])
            rectList = rectList + rectPolygon(polyline)
        else:
            polyline.append(polyline.pop(0))
            rectList = rectList + rectPolygon(polyline)
        return rectList
        
            


            
                


if __name__ == "__main__":
    name = 'star'
    #get_palma(name)
#    polyline = [[-1,-2],[2,-2],[4,4],[-2,4],[2,2]]
#    polyline = [[-300,-400,0],[-400,100,0],[0,0,0],[100,300,0],[400,-100,0],[200,-500,0]]
#    polyline = [[-6.09172980904259, 300.0, 348.9949670250097], [193.78643559477678, 200.0, 355.9748663655099], [293.72551829668555, 0.0, 359.46481603576], [193.78643559477678, -200.0, 355.9748663655099], [-6.09172980904259, -300.0, 348.9949670250097], [-205.96989521286196, -200.0, 342.0150676845095], [-305.90897791477073, 0.0, 338.5251180142594], [-205.96989521286196, 200.0, 342.0150676845095]]
#    polyline = get_base(name+'.txt')[0]
#    print polyline
#    stlFile = open(name+'.stl','w')
#    stlFile.write('\n'.join(get_stl(rectPolygon(polyline))))
#    stlFile.close()
    a , c = 2 , 0
    print '{0} - {1} = {2}'.format(a,c,atan2(a,c))
    a,c = 3,1
    print '{0} - {1} = {2}'.format(a,c,atan2(a,c))
    a,c = 0,2
    print '{0} - {1} = {2}'.format(a,c,atan2(a,c))
    a,c = -3,4
    print '{0} - {1} = {2}'.format(a,c,atan2(a,c))
    a,c = -5,0
    print '{0} - {1} = {2}'.format(a,c,atan2(a,c))
    a,c = -4,-5
    print '{0} - {1} = {2}'.format(a,c,atan2(a,c))
    a,c = 0,-6
    print '{0} - {1} = {2}'.format(a,c,atan2(a,c))
    a,c = 3,-2
    print '{0} - {1} = {2}'.format(a,c,atan2(a,c))