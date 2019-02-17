import numpy as np
import cv2

img = cv2.imread('intial screengrabs/c22.png', -1)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Define upper and lower blue HSV for finding the boxes
lower_blue = np.array([101, 0, 180])
upper_blue = np.array([105, 255, 255])

# get a mask of all pixels that satisfy this constraint
filtered_boxes = cv2.inRange(hsv, lower_blue, upper_blue)

# get contours of boxes within mask
thresh = cv2.threshold(filtered_boxes, 127, 255, 0)[1]
contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]

# find centroid of each contour
annotated_image = img.copy()


for c in contours[:]:
    # get x and y coordinates of contour:
    moments = cv2.moments(c)

    # use equation in openCV documentation
    if moments["m00"] != 0:
        xbar = int(moments["m10"] / moments["m00"])
        ybar = int(moments["m01"] / moments["m00"])

        # Draw on annotated image:
        cv2.circle(annotated_image, (xbar, ybar), 2, (0, 0, 255), -1)

contoured_image = cv2.drawContours(img.copy(), contours, -1, (0, 255, 0), 1)

cv2.imshow('original', img)
cv2.imshow('contours found', contoured_image)
cv2.imshow('centre of masses found', annotated_image)

cv2.imwrite("c22_contours.png", contoured_image)
cv2.imwrite("c22_coms.png", annotated_image)


cv2.waitKey(0)
cv2.destroyAllWindows()
