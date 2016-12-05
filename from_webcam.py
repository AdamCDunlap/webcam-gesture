import cv2
import analyze_static
import control
import time

holdTime = 3
def main():
    webcam = cv2.VideoCapture(0)
    prevDirection = ''
    prevTime = time.time()

    while(True):
        # Capture frame-by-frame
        _, frame = webcam.read()

        curDirection = analyze_static.findFingertips(frame, 120)

        # Check if enough time has elapsed
        newTime = time.time()

        if curDirection != prevDirection:
            prevTime = newTime
            alreadyPressed = False
        elif newTime - prevTime > holdTime and not alreadyPressed and curDirection != '':
            print 'Yaaay'
            if curDirection =='w':
                control.vid_pause()
            elif curDirection == 'a':
                control.vid_back()
            elif curDirection == 'd':
                control.vid_fwd()
            elif curDirection == 's':
                control.vid_pause()
            alreadyPressed = True

        prevDirection = curDirection

        #if newTime - prevTime >= holdTime:
        #    if curDirection == prevDirection:
        #        prevTime = newTime
        #    else:
        #        # If user hasn't, keep the old prevDirection
        #        prevDirection = curDirection
        #        prevTime = newTime
        #        if curDirection =='w':
        #            control.vid_pause()
        #        elif curDirection == 'a':
        #            control.vid_fwd()
        #        elif curDirection == 'd':
        #            control.vid_back()
        #        elif curDirection == 's':
        #            control.vid_pause()
            
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    webcam.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
