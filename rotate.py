from math import * 

'''
x'=x\cos\theta-y\sin\theta\\
y'=x\sin\theta+y\cos\theta.

'''

def hRotatePoint(pts, num, angle):
    angle = radians(float(angle)*float(num))
    rezPoint = []
    rezPoint.append(pts[0]*cos(angle) - pts[1]*sin(angle))
    rezPoint.append(pts[1]*cos(angle) + pts[0]*sin(angle))
    rezPoint.append(pts[2])
    return rezPoint
