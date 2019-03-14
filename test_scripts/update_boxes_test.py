import utils
import img_utils
import cv2
from classes import box

first_frame = cv2.imread("intial screengrabs/c11.png")

first_frame_hsv = cv2.cvtColor(first_frame, cv2.COLOR_BGR2HSV)
box_coords = img_utils.find_box_coords(first_frame_hsv)
print(box_coords)

boxes = []

for i in box_coords:
    boxes.append(box(i[0], i[1], True))

print([box.available for box in boxes])

cv2.imshow("boxes", first_frame)

cv2.waitKey(0)
cv2.destroyAllWindows()