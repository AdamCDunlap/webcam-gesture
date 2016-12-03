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
allContours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
allContours = allContours[0] if imutils.is_cv2() else allContours[1]
handContour = max(allContours, key=cv2.contourArea)

# determine the most extreme points along the contour
extremePoints = []
angleIndices = np.array([-120,-60,0])

while angleIndices[2] < len(handContour):
    # check if angle is greater than 130
    # if angle is greater than 270 then discard
    # else count as a "finger"

    points = handContour[angleIndices] 

    ang = math.degrees(
            math.atan2(points[2][0][1]-points[1][0][1], points[2][0][0]-points[1][0][0]) -
            math.atan2(points[0][0][1]-points[1][0][1], points[0][0][0]-points[1][0][0])
          )

    while ang < 0:
        ang += 360
    while ang > 360:
        ang -= 360

    if ang < 50:
        extremePoints.append(tuple(points[1][0]))

    angleIndices += 1

extLeft = tuple(handContour[handContour[:, :, 0].argmin()][0])
extRight = tuple(handContour[handContour[:, :, 0].argmax()][0])
extTop = tuple(handContour[handContour[:, :, 1].argmin()][0])
extBot = tuple(handContour[handContour[:, :, 1].argmax()][0])

cv2.drawContours(image, [handContour], -1, (0, 255, 255), 2)

for point in extremePoints:
    cv2.circle(image, point, 8, (0, 255, 255), -1)

# show the output image
cv2.imshow("Image", image)
cv2.waitKey(0)
