import numpy as np
import cv2
import img_utils

cap = cv2.VideoCapture("bearing.avi")

while (cap.isOpened()):
    ret, frame = cap.read()
    cv2.imshow('frame', frame)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    back_triangle_coord = img_utils.find_triangle(hsv, np.array([25, 25, 180]), np.array([50, 255, 255]))
    front_triangle_coord = img_utils.find_triangle(hsv, np.array([160, 25, 180]), np.array([170, 255, 255]))

    annotated = frame.copy()
    vector = (front_triangle_coord[0] - back_triangle_coord[0], front_triangle_coord[1] - back_triangle_coord[1])
    cv2.line(annotated, back_triangle_coord,
             (back_triangle_coord[0] + 3 * vector[0], back_triangle_coord[1] + 3 * vector[1]),
             (0, 0, 255), 3)

    cv2.circle(annotated, back_triangle_coord, 3, (0, 0, 0), -1)
    cv2.circle(annotated, front_triangle_coord, 3, (0, 0, 0), -1)

    cv2.imshow("annotated", annotated)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
