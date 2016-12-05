import cv2
import analyze_static

def main():
    webcam = cv2.VideoCapture(0)

    while(True):
        # Capture frame-by-frame
        _, frame = webcam.read()

        handContour, extremePoints = analyze_static.findFingertips(frame, 120)

        if handContour is not None:
            cv2.drawContours(frame, [handContour], -1, (0, 255, 255), 2)

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
            cv2.circle(frame, handCenter, 10, (255, 0, 0), -1)
            for point in extremePoints:
                cv2.circle(frame, point, 5, (0, 0, 255), -1)
            cv2.putText(frame, pointDir, (60, 60), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,0,255), 5)

        # show the output image
        cv2.imshow("Image", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    webcam.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
