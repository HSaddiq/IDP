import numpy as np
import cv2
import time

# FOR CAPTURING DIRECTLY FROM WEBCAM
cap = cv2.VideoCapture(1)

# FOR CAPTURING FROM SAMPLE VIDEO
cap = cv2.VideoCapture('table3_1.avi')

while(True):
        
    # capture frame-by-frame
    ret, frame = cap.read()

    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Define upper and lower blue HSV for finding the boxes
    lower_blue = np.array([101, 0, 180])
    upper_blue = np.array([105, 255, 255])
    
    # get a mask of all pixels that satisfy this constraint
    filtered_boxes = cv2.inRange(hsv, lower_blue, upper_blue)
    
    gaussian = cv2.GaussianBlur(filtered_boxes,(5,5),1)
    
    # get contours of boxes within mask
    thresh = cv2.threshold(filtered_boxes, 127, 255, 0)[1]
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
    
    # find centroid of each contour
    annotated_image = frame.copy()
    
    print("coords:")
    for c in contours[:]:
        
        if(len(c) >= 6):
            # get x and y coordinates of contour:
            moments = cv2.moments(c)
        
            # use equation in openCV documentation
            if moments["m00"] != 0:
                xbar = int(moments["m10"] / moments["m00"])
                ybar = int(moments["m01"] / moments["m00"])
        
        
                # Print list of coords from current frame
                #print(xbar, ybar)
                
                # Draw on annotated image:
                cv2.circle(annotated_image, (xbar, ybar), 2, (0, 0, 255), -1)
            
    contoured_image = cv2.drawContours(frame.copy(), contours, -1, (0, 255, 0), 1)
    
    cv2.imshow('contours found', contoured_image)
    cv2.imshow('centre of masses found', annotated_image)
    cv2.imshow('gaussian', gaussian)
            
    print("\n")
    time.sleep(1)


cv2.waitKey(0)
cv2.destroyAllWindows()
