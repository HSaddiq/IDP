import numpy as np
import cv2

cap = cv2.VideoCapture(1)
i = 0

while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if cv2.waitKey(1) & 0xFF == ord('c'):  # save on pressing 'y'
        cv2.imwrite('c{}.png'.format(i), frame)
        i += 1

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
