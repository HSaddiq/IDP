import cv2
import img_utils
from classes import bot, box
import utils
import time
from concurrent.futures import ThreadPoolExecutor, Future
import numpy as np
import serial

cap = cv2.VideoCapture("test_videos/arucov3.avi")
robot = bot()

# Wait for autofocus
# time.sleep(5)

# Step 1 - get location of boxes:
ret, first_frame = cap.read()

first_frame_hsv = cv2.cvtColor(first_frame, cv2.COLOR_BGR2HSV)
box_coords = img_utils.find_box_coords(first_frame_hsv)

boxes = []
for i in box_coords:
    boxes.append(box(i[0], i[1], True))

while True:
    # capture frame-by-frame
    ret, frame = cap.read()

    try:
        for box in boxes:
            if box.available:
                cv2.circle(frame, (box.x, box.y), 6, (255, 255, 255), 1)

            else:
                cv2.circle(frame, (box.x, box.y), 6, (0, 0, 255), 1)

    except:
        pass

    cv2.line(frame, (0, 90), (640, 90), (0, 0, 0))
    cv2.line(frame, (0, 450), (640, 450), (0, 0, 0))
    cv2.line(frame, (485, 0), (485, 480), (0, 0, 0))
    cv2.line(frame, (270, 0), (270, 480), (0, 0, 0))

    # Trying to find position of unloading for boxes - second end state
    cv2.circle(frame, (0, 265), 10, (0, 255, 0), -1)

    # trying to find position of finish
    cv2.circle(frame, (48, 60), 10, (0, 0, 0), -1)

    cv2.imshow("frame", frame)
    cv2.waitKey(10)
    if cv2.waitKey(1) & 0xFF == ord('a'):
        break
