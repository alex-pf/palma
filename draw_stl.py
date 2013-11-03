import p1

def setPointList(fname):
    raw = p1.readPoints(fname)
    pointList = []
    for row in raw:
        pLine = []
        i = 0
        while i < len(row):
            x=int(row[i])
            i+=1
            y=int(row[i])
            i+=1
            z=int(row[i])
            i+=1
            pLine.append([x,y,z])
        pointList.append(pLine)
    return pointList

def createSTLtabe(pointList):
    i=0
    result = []
    while i < len(pointList)-1:
        p=0
        while p<len(pointList[i]):
            p1 = pointList[i][p]
            p2 = pointList[i+1][p]
            p3 = pointList[i][p-1]
            result.append([p1,p2,p3])
            
            p1 = pointList[i][p]
            if p==len(pointList[i])-1:
                p2 = pointList[i+1][0]
            else:
                p2 = pointList[i+1][p+1]
            p3 = pointList[i+1][p]
            result.append([p1,p2,p3])
            p+=1
        i+=1
    return result


def writeToSTL(tabe, fname):
    l1 = '  facet normal 1 0 0\n    outer loop\n'
    l2 = '    endloop\n  endfacet\n'
    f = open(fname, 'w')
    f.write('solid OpenSCAD_Model\n')
    for row in tabe:
        f.write(l1)
        for point in row:
            s = ('      vertex ' + str(point[0]) + ' ' + str(point[1]) + ' ' + str(point[2])+' \n')
            f.write(s)
        f.write(l2)
    f.write('endsolid OpenSCAD_Model')
    f.close()

'''
solid OpenSCAD_Model
  facet normal 1 0 0
    outer loop  
	vertex 0 0 0
	vertex 0 0 10
	vertex 0 10 0
    endloop
  endfacet
'''


pointList = setPointList('cube.csv')
R = createSTLtabe(pointList)
#p1.writeToCSV(R,'cube2.csv')
writeToSTL(R,'cube2.stl')