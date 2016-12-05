#!/usr/bin/env python2

# import the necessary packages
import imutils
import cv2
import sys
import math
import numpy as np
import control

def findFingertips(image, light_thresh=100):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # threshold the image, then perform a series of erosions +
    # dilations to remove any small regions of noise
    thresh = cv2.threshold(gray, light_thresh, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=2)

    # find contours in thresholded image, then grab the largest
    # one
    allContours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    allContours = allContours[0] if imutils.is_cv2() else allContours[1]

    if len(allContours) == 0:
        return ''
    handContour = max(allContours, key=cv2.contourArea)

    curveLen = 75

    if len(handContour) < 2*curveLen:
        return ''

    # determine the most extreme points along the contour
    extremePoints = []
    angleIndices = np.array([-2*curveLen,-curveLen,0])

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
    
    if handContour is not None:
        cv2.drawContours(image, [handContour], -1, (0, 255, 255), 2)

        handContourMoments = cv2.moments(handContour)
        handCenter = (int(handContourMoments['m10'] / handContourMoments['m00']),
                      int(handContourMoments['m01'] / handContourMoments['m00']))

        pointDir = ''
        if len(extremePoints) > 0:
            midExtremePoint = extremePoints[len(extremePoints)/2]
            fingertipVec = (midExtremePoint[0] - handCenter[0], midExtremePoint[1] - handCenter[1])
            if fingertipVec[1] > 100:
                pointDir = 's'
            elif fingertipVec[1] < -100:
                pointDir = 'w'
            elif fingertipVec[0] > 100:
                pointDir = 'a'
            elif fingertipVec[0] < -100:
                pointDir = 'd'

        # Draw interesting stuff
        cv2.circle(image, handCenter, 10, (255, 0, 0), -1)
        for point in extremePoints:
            cv2.circle(image, point, 5, (0, 0, 255), -1)
        cv2.putText(image, pointDir, (60, 60), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,0,255), 5)

        image = cv2.resize(image, (500,500))

        # show the output image
        cv2.imshow("Image", image)

    return pointDir

if __name__ == '__main__':
    try:
        imfilename = sys.argv[1]
    except IndexError:
        imfilename = "examples/peace.jpg"

    # load the image, convert it to grayscale, and blur it slightly
    image = cv2.imread(imfilename)

    handContour, extremePoints = findFingertips(image)

    cv2.drawContours(image, [handContour], -1, (0, 255, 255), 2)

    for point in extremePoints:
        cv2.circle(image, point, 8, (0, 0, 255), -1)
    def main():
        webcam = cv2.VideoCapture(0)

    # show the output image
    cv2.imshow("Image", image)
    while cv2.waitKey(0) & 0xFF != ord('q'):
        pass
