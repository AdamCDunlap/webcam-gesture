#!/usr/bin/env python2

# import the necessary packages
import imutils
import cv2
import sys
import math
import numpy as np

try:
    imfilename = sys.argv[1]
except IndexError:
    imfilename = "examples/peace.jpg"

# load the image, convert it to grayscale, and blur it slightly
image = cv2.imread(imfilename)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)

# threshold the image, then perform a series of erosions +
# dilations to remove any small regions of noise
thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)[1]
thresh = cv2.erode(thresh, None, iterations=2)
thresh = cv2.dilate(thresh, None, iterations=2)

# find contours in thresholded image, then grab the largest
# one
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
c = max(cnts, key=cv2.contourArea)

hull = cv2.convexHull(c)

# determine the most extreme points along the contour
extremePoints = []
angleIndices = np.array([-120,-60,0])
while angleIndices[2] < len(c):
#if True:
    # check if angle is greater than 130
    # if angle is greater than 270 then discard
    # else count as a "finger"

    points = c[angleIndices]



    #d01s = (points[0][0][0] - points[1][0][0])**2 + (points[0][0][1] - points[1][0][1])**2
    #d02s = (points[0][0][0] - points[2][0][0])**2 + (points[0][0][1] - points[2][0][1])**2
    #d12s = (points[1][0][0] - points[2][0][0])**2 + (points[1][0][1] - points[2][0][1])**2
    ##ang = math.degrees(math.acos((d01s + d02s - d12s)/(2*math.sqrt(d01s)*math.sqrt(d02s))))


    #a = (points[1-1][0][0] - points[2-1][0][0], points[1-1][0][1] - points[2-1][0][1])
    #b = (points[1-1][0][0] - points[3-1][0][0], points[1-1][0][1] - points[3-1][0][1])

    #adotb = a[0]*b[0] + a[1]*b[1]
    #maga = math.sqrt(a[0]**2 + a[1]**2)
    #magb = math.sqrt(b[0]**2 + b[1]**2)
    #ang = math.degrees(math.acos(adotb / (maga * magb)))

    #ang2 = math.degrees(math.acos((d01s + d02s - d12s)/(2*math.sqrt(d01s)*math.sqrt(d02s))))


    #if ang < 0:
    #    print 'Angles are neg:', ang
    #    break

    #if abs(ang - ang2) > .01:
    #    print 'Angles are different:', ang, ang2
    #    break

    # USE atan2
    ang = math.degrees(
            math.atan2(points[2][0][1]-points[1][0][1], points[2][0][0]-points[1][0][0]) -
            math.atan2(points[0][0][1]-points[1][0][1], points[0][0][0]-points[1][0][0])
          )
    # result = atan2(P3.y - P1.y, P3.x - P1.x) -
    #          atan2(P2.y - P1.y, P2.x - P1.x);

    while ang < 0:
        ang += 360
    while ang > 360:
        ang -= 360

    #print ang

    #if ang > 70 and ang < 220:
    if ang < 50:
        extremePoints.append(tuple(points[1][0]))

    angleIndices += 1

extLeft = tuple(c[c[:, :, 0].argmin()][0])
extRight = tuple(c[c[:, :, 0].argmax()][0])
extTop = tuple(c[c[:, :, 1].argmin()][0])
extBot = tuple(c[c[:, :, 1].argmax()][0])

# draw the outline of the object, then draw each of the
# extreme points, where the left-most is red, right-most
# is green, top-most is blue, and bottom-most is teal
cv2.drawContours(image, [c], -1, (0, 255, 255), 2)
cv2.drawContours(image, [hull], -1, (255, 0, 255), 2)

print len(extremePoints)

print extLeft

#cv2.circle(image, tuple(c[-70][0]), 8, (0, 0, 255), -1)
#cv2.circle(image, tuple(c[-0][0]), 8, (0, 255, 255), -1)
#cv2.circle(image, tuple(c[70][0]), 8, (255, 255, 255), -1)

for point in extremePoints:
    cv2.circle(image, point, 8, (0, 255, 255), -1)
#cv2.circle(image, extLeft, 8, (0, 0, 255), -1)
#cv2.circle(image, extRight, 8, (0, 255, 0), -1)
#cv2.circle(image, extTop, 8, (255, 0, 0), -1)
#cv2.circle(image, extBot, 8, (255, 255, 0), -1)

# show the output image
cv2.imshow("Image", image)
cv2.waitKey(0)
