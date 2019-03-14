import numpy as np
import cv2
import img_utils

# Captures video
cap = cv2.VideoCapture("bearing.avi")

while (cap.isOpened()):
    ret, frame = cap.read()
    
    # Show the raw video feed
    cv2.imshow('frame', frame)
    
    # Get hue saturation value
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Get coordinates of 2 triangles based on lower and upper bound hue values
    back_triangle_coord = img_utils.find_triangle(hsv, np.array([25, 25, 180]), np.array([50, 255, 255]))
    front_triangle_coord = img_utils.find_triangle(hsv, np.array([160, 25, 180]), np.array([170, 255, 255]))
    
    annotated = frame.copy()
    
    # Define a vector connecting the front and back triangles
    vector = (front_triangle_coord[0] - back_triangle_coord[0], front_triangle_coord[1] - back_triangle_coord[1])
    
    #########################
    # Get the current bearing
    current_bearing = np.arctan2((front_triangle_coord[1] - back_triangle_coord[1]),(front_triangle_coord[0] - back_triangle_coord[0]))
    
    current_bearing = -current_bearing*180/np.pi
    
    if(current_bearing < 0):
        current_bearing = 360 + current_bearing
    print(current_bearing)
    
    # Draw a red line of defined length along the vector
    cv2.line(annotated, back_triangle_coord,
             (back_triangle_coord[0] + 3 * vector[0], back_triangle_coord[1] + 3 * vector[1]),
             (0, 0, 255), 3)
    
    # Draw black circles on the the identified triangles
    cv2.circle(annotated, back_triangle_coord, 3, (0, 0, 0), -1)
    cv2.circle(annotated, front_triangle_coord, 3, (0, 0, 0), -1)

    # Show the annotated video feed
    cv2.imshow("annotated", annotated)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
