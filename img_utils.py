import numpy as np
import cv2


# Contains all functions related to bearing and positioning of robot

def find_box_coords(frame):
    # Returns a list of coordinate tuples having been given a frame of image //FRAME IN HSV

    # Define upper and lower blue HSV for finding the boxes
    lower_blue = np.array([80, 60, 160])
    upper_blue = np.array([120, 255, 255])

    # get a mask of all pixels that satisfy this constraint
    filtered_boxes = cv2.inRange(frame, lower_blue, upper_blue)

    # blurs the points together to try to reduce outliers
    gaussian = cv2.GaussianBlur(filtered_boxes, (5, 5), 3)

    # get contours of boxes within mask
    thresh = cv2.threshold(gaussian, 100, 255, 0)[1]
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

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

                # Print list of coords from current frame
                if ybar > 90 and ybar < 450 and xbar < 500 and xbar > 270:
                    list_of_coords.append((xbar, ybar))

    return (list_of_coords)


# Function that returns the centre of mass of a triangle between an upper and lower hue value

def find_triangle(frame, lower_hue, upper_hue):
    # get a mask of all pixels that satisfy this constraint
    filtered_triangle = cv2.inRange(frame, lower_hue, upper_hue)

    # blurs the points together to try to reduce outliers
    gaussian = cv2.GaussianBlur(filtered_triangle, (5, 5), 0)

    # get contours of boxes within mask
    thresh = cv2.threshold(gaussian, 100, 255, 0)[1]
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


# Testing suite
if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv2.imshow("test", frame)
        # Returns a list of coordinate tuples having been given a frame of image //FRAME IN HSV
        first_frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # Define upper and lower blue HSV for finding the boxes
        lower_blue = np.array([80, 60, 160])
        upper_blue = np.array([120, 255, 255])

        # get a mask of all pixels that satisfy this constraint
        filtered_boxes = cv2.inRange(first_frame_hsv, lower_blue, upper_blue)

        # blurs the points together to try to reduce outliers
        gaussian = cv2.GaussianBlur(filtered_boxes, (5, 5), 3)

        # get contours of boxes within mask
        thresh = cv2.threshold(gaussian, 100, 255, 0)[1]
        cv2.imshow("thresh", thresh)
        contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

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

                    # Print list of coords from current frame
                    list_of_coords.append((xbar, ybar))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
