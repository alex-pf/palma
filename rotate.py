from math import * 

'''
x'=x\cos\theta-y\sin\theta\\
y'=x\sin\theta+y\cos\theta.

'''

def hRotatePoint(pts, num, angle):
    angle = radians(float(int(angle)*int(num)))
    rezPoint = []
    rezPoint.append(float(pts[0])*cos(angle) - float(pts[1])*sin(angle))
    rezPoint.append(float(pts[1])*cos(angle) + float(pts[0])*sin(angle))
    rezPoint.append(float(pts[2]))
    return rezPoint
