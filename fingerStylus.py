import sys
import cv2
import numpy as np
import pyautogui


def main(argv):
    # Init webcam
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()

    # Correspond webcam resolution to monitor resolution
    videoHeight = frame.shape[0]
    videoWidth = frame.shape[1]
    screenWidth, screenHeight = pyautogui.size()
    widthScalar = screenWidth/videoWidth
    heightScalar = screenHeight/videoHeight

    while(True):
        # Loads an image
        ret, frame = cap.read()

        # gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        # gray = cv2.medianBlur(gray, 5)

        #cv2.imshow('red', frame[:, :, 2])
        # Assume fingertip looks like a circle
        circles = cv2.HoughCircles(frame[:, :, 2], cv2.HOUGH_GRADIENT, 1, videoHeight,
                                   param1=100, param2=30,
                                   minRadius=15, maxRadius=35)

        if circles is not None:
            # Assume fingertip is strongest circle
            circle = circles[0][0]
            circle = np.uint16(np.around(circle))

            # circle center
            center = (circle[0], circle[1])
            if frame[center[1], center[0]][2] == 255:
                #print(frame[center[1], center[0]])
                # Move cursor to finger center
                pyautogui.moveTo(screenWidth - center[0]*widthScalar, center[1]*heightScalar)
                # Show circle outline
                #cv2.circle(frame, center, 1, (0, 100, 100), 3)
                # If finger is close to webcam, assume click
                #radius = circle[2]
                if circle[2] > 30:
                    pyautogui.click(screenWidth - center[0]*widthScalar, center[1]*heightScalar)
                #cv2.circle(frame, center, radius, (255, 0, 255), 3)

        #cv2.imshow("detected circles", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    return 0


if __name__ == "__main__":
    main(sys.argv[1:])
