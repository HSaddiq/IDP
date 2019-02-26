# this function returns a list of box coordinates via serial

import numpy as np
import serial
import time

ser = serial.Serial()

ser.baudrate = 9600
ser.port = "COM6"
ser.open()

#continuous loop waiting for arduino to request a bearing

while(True):
    
    if(str(ser.readline())[2:15] == "arduino ready"):
        
        print("arduino: arduino ready")
        ser.write(str("python ready").encode('UTF-8'))
        print("python ready")
        
        time.sleep(0.5)
        
        if(str(ser.readline())[2:20] == "requesting bearing"):
            
            print("arduino: requesting bearing")
            
            bearing = input("type bearing: ")
            ser.write(str(bearing).encode('UTF-8'))
            
            # the arduino currently waits 3 seconds for the user to type a bearing, thus the python waits 4 seconds for safety
            print("waiting...")
            time.sleep(4)
            
            if(str(ser.readline())[2:10] == "received"):
                print("received")
                
                # this prints all the movement stages
                print(ser.readline())
                print(ser.readline())
                print(ser.readline())
                print(ser.readline())
            
ser.close()
