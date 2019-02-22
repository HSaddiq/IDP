import numpy as np
import cv2
from classes import box, bot

cap = cv2.VideoCapture("test_videos/aruco.avi")

robot = bot()

while True:
    # capture frame-by-frame
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_ARUCO_ORIGINAL)
    parameters = cv2.aruco.DetectorParameters_create()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    if len(corners) != 0:
        average_point = np.mean(corners[0][0], 0)
        robot.x = int(average_point[0])
        robot.y = int(average_point[1])
        top_left = corners[0][0][0]
        top_right = corners[0][0][1]
        midpoint_top = (top_left + top_right) / 2
        robot.bearing = np.arctan(
            (midpoint_top[1] - average_point[1]) / (midpoint_top[0] - average_point[0])) * 180 / np.pi

    cv2.circle(frame, (robot.x, robot.y), 2, (0, 0, 255), -1)
    # cv2.line(frame, (robot.x, robot.y),
    #          (robot.x + 100 * np.cos(robot.bearing * np.pi / 180), robot.y + 100 * np.sin(robot.bearing * np.pi / 180)),
    #          2, (0, 0, 255), -1)
    print(int(np.cos(robot.bearing * np.pi / 180)))
    cv2.line(frame, (robot.x, robot.y),
             (robot.x + int(100 * np.cos(robot.bearing * np.pi / 180)),
              robot.y + int(100 * np.sin(robot.bearing * np.pi / 180))),
             (0, 0, 0))

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, str(robot.bearing), (10, 500), font, 4, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.imshow("AruCo", frame)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
