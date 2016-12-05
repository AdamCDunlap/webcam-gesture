#!/usr/bin/env python2

# import the necessary packages
import imutils
import cv2
import sys
import math
import numpy as np
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
        return None,None
    handContour = max(allContours, key=cv2.contourArea)

    curveLen = 75

    if len(handContour) < 2*curveLen:
        return handContour, []

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
    return handContour, extremePoints

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
