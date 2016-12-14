#!/usr/bin/env python2

# import the necessary packages
import imutils
import cv2
import sys
import math
import numpy as np
import control

def findHand(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    minGray = np.amin(gray)
    maxGray = np.amax(gray)

    #light_thresh = minGray + (maxGray - minGray) / 2
    light_thresh = np.average(gray) + 40

    # threshold the image, then perform a series of erosions +
    # dilations to remove any small regions of noise
    thresh = cv2.threshold(gray, light_thresh, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.erode(thresh, None, iterations=4)
    thresh = cv2.dilate(thresh, None, iterations=4)

    # find contours in thresholded image, then grab the largest
    # one
    allContours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    allContours = allContours[0]

    if len(allContours) == 0:
        return None
    handContour = max(allContours, key=cv2.contourArea)

    return handContour

def findSharpPoints(handContour, curveLen = 75, curveAngleThresh = 50):
    if len(handContour) < 2*curveLen:
        return []

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

        if ang < curveAngleThresh:
            extremePoints.append(tuple(points[1][0]))

        angleIndices += 1

    return extremePoints

def eDist(a,b):
    ''' Returns euclidean distance from a to b
    '''

    xd = a[0] - b[0]
    yd = a[1] - b[1]
    return math.sqrt(xd*xd + yd*yd)

def filterFingertips(sharpPoints, distThresh = 50):
    ''' List of sharp points should be in order

    Might return two next two each other if a a cluster spans from the end of
    the list to the beginning
    '''

    if len(sharpPoints) == 0:
        return []

    lastPoint = sharpPoints[0]

    centers = []

    clusteredPoints = [lastPoint]
    for p in sharpPoints[1:]:
        if eDist(lastPoint, p) > distThresh:
            # We're starting a new cluster
            centers.append(clusteredPoints[len(clusteredPoints)/2])
            clusteredPoints[:] = []
        clusteredPoints.append(p)
        lastPoint = p
    if len(clusteredPoints) > 0:
        centers.append(clusteredPoints[len(clusteredPoints)/2])

    return centers


def getHandCenter(handContour):
    handContourMoments = cv2.moments(handContour)
    return (int(handContourMoments['m10'] / handContourMoments['m00']),
            int(handContourMoments['m01'] / handContourMoments['m00']))

def findFingerDirection(handCenter, fingerLoc):
    ''' Returns strings either 'w' 'a' 's' or 'd'
    '''
    fingertipVec = (fingerLoc[0] - handCenter[0], fingerLoc[1] - handCenter[1])
    if fingertipVec[1] > 100:
        return 's'
    elif fingertipVec[1] < -100:
        return 'w'
    elif fingertipVec[0] > 100:
        return 'a'
    elif fingertipVec[0] < -100:
        return 'd'

def showFingertips(image, handContour, fingertips, handCenter, fDir, sharpPoints):
    cv2.drawContours(image, [handContour], -1, (0, 255, 255), 2)

    # Draw interesting stuff
    if handCenter:
        cv2.circle(image, handCenter, 10, (255, 0, 0), -1)
    for point in sharpPoints:
        cv2.circle(image, point, 3, (100, 100, 0), -1)
    for point in fingertips:
        cv2.circle(image, point, 10, (0, 0, 255), -1)
    cv2.putText(image, fDir, (60, 60), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,0,255), 5)

    #image = cv2.resize(image, (500,500))

    # show the output image
    cv2.imshow("Image", image)

def extract_and_show_fingertips(image):
    handContour = findHand(image)

    fdir = ''
    fingertips = []
    sharpPoints = []
    handCenter = None
    if handContour is not None:
        sharpPoints = findSharpPoints(handContour)
        fingertips = filterFingertips(sharpPoints)
        handCenter = getHandCenter(handContour)

        if len(fingertips) > 0:
            middleTip = fingertips[len(fingertips)/2]
            fdir = findFingerDirection(handCenter, middleTip)

    showFingertips(image, handContour, fingertips, handCenter, fdir, sharpPoints)
    return fdir

if __name__ == '__main__':
    try:
        imfilename = sys.argv[1]
    except IndexError:
        imfilename = "examples/peace.jpg"

    image = cv2.imread(imfilename)

    extract_and_show_fingertips(image)

    while cv2.waitKey(0) & 0xFF != ord('q'):
        pass
