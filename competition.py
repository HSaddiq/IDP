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


# Step 2 - In 1 thread, continously update the location and bearing of bot
def update_bot_localisation():
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
            robot.bearing = - np.arctan2(
                (midpoint_top[1] - average_point[1]), (midpoint_top[0] - average_point[0])) * 180 / np.pi
            robot.bearing = (robot.bearing + 360) % 360
        #
        # #show all available boxes in white and completed boxes in red
        # Try except loop as some boxes might not be found

        try:
            for box in boxes:
                if box.available:
                    cv2.circle(frame, (box.x, box.y), 6, (255, 255, 255), 1)

                else:
                    cv2.circle(frame, (box.x, box.y), 6, (0, 0, 255), 1)

        except:
            pass

        cv2.line(frame, (robot.x, robot.y),
                 (robot.x + int(100 * np.cos(robot.bearing * np.pi / 180)),
                  robot.y - int(100 * np.sin(robot.bearing * np.pi / 180))),
                 (0, 0, 0))

        # get bearing to nearest available box
        # try as all boxes may be found

        try:
            # show nearest available box in green
            nearest_box = utils.get_nearest_box(boxes, robot)
            cv2.circle(frame, (nearest_box.x, nearest_box.y), 6, (0, 200, 0), 1)

            angle = utils.get_angle([robot.x, robot.y], [nearest_box.x, nearest_box.y], robot.bearing)

            cv2.line(frame, (robot.x, robot.y),
                     (robot.x + int(100 * np.cos((angle + robot.bearing) * np.pi / 180)),
                      robot.y - int(100 * np.sin((angle + robot.bearing) * np.pi / 180))),
                     (0, 0, 0))

            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, str(angle), (10, 200), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

        except:
            pass

        cv2.waitKey(10)

        # Trying to find position of unloading for boxes
        cv2.circle(frame, (0, 285), 10, (0, 255, 0), -1)

        # trying to find position of end state
        cv2.circle(frame, (48, 60), 10, (0, 0, 0), -1)

        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('a'):
            break


# Step 3 In 2nd thread, when serial read asks for next angle, calculate angle

def communicate_via_serial():
    time.sleep(3)
    global boxes

    ser = serial.Serial()

    ser.baudrate = 9600
    ser.port = "COM8"
    ser.open()

    while True:
        arduino_string = ser.readline()
        print(arduino_string)

        if arduino_string == b'requesting bearing\r\n':
            # if all boxes taken, send an angle of 5000 to indicate that end sequence must run
            if all([box.available is False for box in boxes]) or boxes is None:
                ser.write(str(str(5000) + "/n").encode("UTF-8"))

                # check if arduino received end sequence code
                arduino_string = ser.readline()
                print(arduino_string)

                # code for driving into the unloading stage
                unloading_position = [0, 285]

                angle_to_unloading = utils.get_angle([robot.x, robot.y], unloading_position,
                                                     robot.bearing)

                if angle_to_unloading < 0:
                    angle_to_unloading = 360 + angle_to_unloading

                print("sending {}".format(angle_to_unloading))

                # send angle to arduino via serial (0-360)1
                ser.write(str(str(angle_to_unloading) + "/n").encode("UTF-8"))

                # code for going to a point to the side of the end location aligning to end point

                # position_of_first_end_point = [50, 420]
                # angle_to_first_end_point = utils.get_angle([robot.x, robot.y], position_of_first_end_point,
                #                                            robot.bearing)
                #
                # if angle_to_first_end_point < 0:
                #     angle_to_first_end_point = 360 + angle_to_first_end_point
                #
                # # send angle to arduino via serial (0-360)1
                # ser.write(str(str(angle_to_first_end_point) + "/n").encode("UTF-8"))
                #
                # # wait for response
                # arduino_string = ser.readline()
                #
                # # send arduino distance measurement
                # distance_to_nearest_end_point = utils.get_distance([robot.x, robot.y], position_of_first_end_point)
                # ser.write(str(str(distance_to_nearest_end_point) + "/n").encode("UTF-8"))
                # print("needs to travel {} centimetres".format(distance_to_nearest_end_point))
                #
                # #wait for response
                # arduino_string = ser.readline()
                #
                # position_of_second_end_point = [50, 285]
                # angle_to_second_end_point = utils.get_angle([robot.x, robot.y], position_of_second_end_point,
                #                                             robot.bearing)
                #
                # if angle_to_second_end_point < 0:
                #     angle_to_second_end_point = 360 + angle_to_second_end_point
                #
                # # send angle to arduino via serial (0-360)
                # ser.write(str(str(angle_to_second_end_point) + "/n").encode("UTF-8"))

            # get nearest available box and mark as unavailable
            nearest_box = utils.get_nearest_box(boxes, robot)
            # get bearing to nearest available box
            angle = utils.get_angle([robot.x, robot.y], [nearest_box.x, nearest_box.y], robot.bearing)

            if angle < 0:
                angle = 360 + angle

            # send angle to arduino via serial (0-360)1
            ser.write(str(str(angle) + "/n").encode("UTF-8"))

        if arduino_string == b'processed box\r\n':
            # arduino got box - mark processed box as removed

            boxes, nearest_box = utils.get_nearest_box_with_removal(boxes, robot)


def test_camera():
    while True:
        ret, frame = cap.read()
        cv2.imshow("test", frame)
        # Wait for 'a' key to stop the program
        if cv2.waitKey(1) & 0xFF == ord('a'):
            break


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
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

    print("Boxes Found: {}".format(len(boxes)))

    pool = ThreadPoolExecutor(max_workers=2)
    pool.submit(update_bot_localisation)
    pool.submit(communicate_via_serial)
