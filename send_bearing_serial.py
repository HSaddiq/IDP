# this function returns a list of box coordinates via serial

import numpy as np
import serial
import time

ser = serial.Serial()

ser.baudrate = 9600
ser.port = "COM7"
ser.open()

start_string = ser.readline()

print(start_string)


while(True):

    bearing = input("type bearing")
    
    if (bearing == 'q'):
        break
    
    ser.write(str(bearing).encode('UTF-8'))

    print(ser.readline())
    time.sleep(0.1)
    print(ser.readline())

ser.close()
