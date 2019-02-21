import numpy as np
import cv2


# Contains all functions related to bearing and positioning of robot

def find_box_coords(frame):
    # Returns a list of coordinate tuples having been given a frame of image //FRAME IN HSV

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Define upper and lower blue HSV for finding the boxes
    lower_blue = np.array([101, 0, 180])
    upper_blue = np.array([105, 255, 255])
    
    # get a mask of all pixels that satisfy this constraint
    filtered_boxes = cv2.inRange(hsv, lower_blue, upper_blue)
    
    # blurs the points together to try to reduce outliers
    gaussian = cv2.GaussianBlur(filtered_boxes,(5,5),3)
    
    # get contours of boxes within mask
    thresh = cv2.threshold(gaussian, 50, 255, 0)[1]
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
        
    # find centroid of each contour
    annotated_image = frame.copy()
    
    list_of_coords = []
    
    #print("coords:")
    for c in contours[:]:
        
        # checks that each identified blob is large enough to be consideres a box
        if(len(c) >= 5):
            # get x and y coordinates of contour:
            moments = cv2.moments(c)
        
            # use equation in openCV documentation
            if moments["m00"] != 0:
                xbar = int(moments["m10"] / moments["m00"])
                ybar = int(moments["m01"] / moments["m00"])
        
        
                # Print list of coords from current frame
                list_of_coords.append((xbar, ybar))
                
                # Draw on annotated image:
                cv2.circle(annotated_image, (xbar, ybar), 2, (0, 0, 255), -1)
           
    return(list_of_coords)


# Function that returns the centre of mass of a triangle between an upper and lower hue value

def find_triangle(frame, lower_hue, upper_hue):
    # get a mask of all pixels that satisfy this constraint
    filtered_triangle = cv2.inRange(frame, lower_hue, upper_hue)

    # blurs the points together to try to reduce outliers
    gaussian = cv2.GaussianBlur(filtered_triangle, (5, 5), 0)

    # get contours of boxes within mask
    thresh = cv2.threshold(gaussian, 150, 255, 0)[1]
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
    list_of_coords = []

    for c in contours:

        # checks that each identified blob is large enough to be consideres a box
        if (len(c) >= 5):
            # get x and y coordinates of contour:
            moments = cv2.moments(c)

            # use equation in openCV documentation
            if moments["m00"] != 0:
                xbar = int(moments["m10"] / moments["m00"])
                ybar = int(moments["m01"] / moments["m00"])

                list_of_coords.append((xbar, ybar))

    return list_of_coords[0]
