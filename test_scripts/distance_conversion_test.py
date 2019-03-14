
import cv2
import img_utils
from classes import bot, box
import utils
import time
from concurrent.futures import ThreadPoolExecutor, Future
import numpy as np
import serial

ser = serial.Serial()

ser.baudrate = 9600
ser.port = "COM8"
ser.open()

arduino_string = ser.readline()
ser.write(str(str(100) + "/n").encode("UTF-8"))