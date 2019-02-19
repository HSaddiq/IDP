# this function returns a list of box coordinates via serial

import numpy as np
import cv2
import serial
import keyboard

ser = serial.Serial()

ser.baudrate = 9600
ser.port = "COM6"
ser.open()

start_string = ser.readline()


while True:

    if keyboard.is_pressed('0'):
        print("sending ON")
        ser.write(str("0000\n").encode('UTF-8'))

    elif keyboard.is_pressed('1'):
        print("sending OFF")
        ser.write(str("1111\n").encode('UTF-8'))

ser.close()