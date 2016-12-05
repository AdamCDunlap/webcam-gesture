import cv2
import analyze_static

def main():
    webcam = cv2.VideoCapture(0)

    while(True):
        # Capture frame-by-frame
        _, frame = webcam.read()

        handContour, extremePoints = analyze_static.findFingertips(frame, 120)

        cv2.drawContours(frame, [handContour], -1, (0, 255, 255), 2)

        for point in extremePoints:
            cv2.circle(frame, point, 8, (0, 255, 255), -1)

        # show the output image
        cv2.imshow("Image", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    webcam.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
