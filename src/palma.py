# Волшебная строчка превращающая кодировку файла в Utf-8 без BOM , без неё NetBeans тупит, не понимая кирилицу

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
    param_list= {'count':10,'height':3,'offset':10000,'rotate':11,'zoom':0.05}
    return param_list

def zoom(polyline,z):
    rez = []
    z = 1-z
    for point in polyline:
        rez.append([point[0]*z,point[1]*z,point[2]])
    

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
            rect3 = [topPolylineList[i][j],topPolylineList[i][j-1],topPolylineList[i][j-2]]
            rect4 = [downPolylineList[i][j-2],downPolylineList[i][j-1],downPolylineList[i][j]]
            poligonList.append(rect1)
            poligonList.append(rect2)
            poligonList.append(rect3)
            poligonList.append(rect4)
    return poligonList
    
def get_stl(poligonList):
    stlText = []
    l1 = '    facet normal 1 0 0\n        outer loop'
    l2 = '        endloop\n    endfacet'
    stlText.append('solid OpenSCAD_Model')
    for poligon in poligonList:
        stlText.append(l1)
        for point in poligon:
            stlText.append('            vertex ' + str(point[0]) + ' ' + str(point[1]) + ' ' + str(point[2]))
        stlText.append(l2)
    stlText.append('endsolid OpenSCAD_Model')
    return stlText

if __name__ == "__main__":
    name = 'points'
    polilyneList = get_base(name + '.txt')
    print polilyneList
    param =  get_param_list()
    
    floorList = []
    for f in xrange(param.get('count')):
        floor = []
        for pl in polilyneList:
            polyline = zoom(pl,param.get('zoom')*f)
            polyline = h_rotate_polyline(pl, param.get('rotate')*f )
            floor.append(polyline)
        floorList.append(floor)
    
    V = []
    for f in xrange(len(floorList)):
        V = V + (extension_wall(floorList[f], param.get('height'), param.get('offset'), f) )
        
    
    stl = get_stl(V)
    stlFile = open(name+'.stl','w')
    stlFile.write('\n'.join(stl))