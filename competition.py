########
# MAIN PROGRAM FOR IDP 2019 LENT 2 TEAM 201


#####

import cv2
import img_utils
from classes import bot, box
import utils
import time
from concurrent.futures import ThreadPoolExecutor, Future
import numpy as np
import serial

cap = cv2.VideoCapture("test_videos/aruco.avi")
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


# Step 2 - In 1 thread, continously update the location and bearing of bot
def update_bot_localisation():
    print("test")
    while True:
        # capture frame-by-frame
        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_ARUCO_ORIGINAL)
        parameters = cv2.aruco.DetectorParameters_create()

        corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

        if len(corners) != 0:
            average_point = np.mean(corners[0][0], 0)
            robot.x = int(average_point[0])
            robot.y = int(average_point[1])
            top_left = corners[0][0][0]
            top_right = corners[0][0][1]
            midpoint_top = (top_left + top_right) / 2
            robot.bearing = - np.arctan(
                (midpoint_top[1] - average_point[1]) / (midpoint_top[0] - average_point[0])) * 180 / np.pi
            robot.bearing = (robot.bearing + 360) % 360

        nearest_box = utils.get_nearest_box(boxes, robot)
        cv2.circle(frame, (nearest_box.x, nearest_box.y), 2, (0, 0, 255), -1)




        # get nearest available box
        nearest_box = utils.get_nearest_box(boxes, robot)
        # get bearing to nearest available box

        cv2.line(frame, (robot.x, robot.y),
                 (robot.x + int(100 * np.cos(robot.bearing * np.pi / 180)),
                  robot.y - int(100 * np.sin(robot.bearing * np.pi / 180))),
                 (0, 0, 0))

        angle = utils.get_angle([robot.x, robot.y], [nearest_box.x, nearest_box.y], robot.bearing)

        cv2.line(frame, (robot.x, robot.y),
                 (robot.x + int(100 * np.cos(robot.bearing * np.pi / 180)),
                  robot.y - int(100 * np.sin(robot.bearing * np.pi / 180))),
                 (0, 0, 0))

        cv2.line(frame, (robot.x, robot.y),
                 (robot.x + int(100 * np.cos((angle+robot.bearing) * np.pi / 180)),
                  robot.y - int(100 * np.sin((angle+robot.bearing) * np.pi / 180))),
                 (0, 0, 0))

        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('a'):
            break


# Step 3 In 2nd thread, when serial read asks for next angle, calculate angle

def communicate_via_serial():
    ser = serial.Serial()

    ser.baudrate = 9600
    ser.port = "COM4"
    ser.open()

    while True:
        arduino_string = ser.readline()
        print(arduino_string)

        # get nearest available box
        nearest_box = utils.get_nearest_box(boxes, robot)
        # get bearing to nearest available box
        angle = utils.get_angle([robot.x, robot.y], [nearest_box.x, nearest_box.y], robot.bearing)
        print(angle)

        # send angle to arduino via serial (0-360)1
        ser.write(str(str(angle) + "/n").encode("UTF-8"))

def test_camera():
    print("test")

    while True:
        ret,frame = cap.read()
        cv2.imshow("test",frame)
        # Wait for 'a' key to stop the program
        if cv2.waitKey(1) & 0xFF == ord('a'):
            break



if __name__ == '__main__':
    pool = ThreadPoolExecutor(max_workers=2)
    pool.submit(update_bot_localisation)
    # pool.submit(communicate_via_serial)
    #pool.submit(test_camera)


