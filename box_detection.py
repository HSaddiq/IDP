import numpy as np
import cv2
from img_utils import find_box_coords

img = cv2.imread('intial screengrabs/c22.png', -1)

coords = find_box_coords(img)
annotated_image = img.copy()

for i in coords:
    print(i)
    cv2.circle(annotated_image, i, 2, (0, 0, 255), -1)

cv2.imshow('original', img)
cv2.imshow('centre of masses found', annotated_image)

cv2.waitKey(0)
cv2.destroyAllWindows()
