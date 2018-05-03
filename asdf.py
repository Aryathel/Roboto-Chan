import serial
import time

ser = serial.Serial('/dev/ttyUSB1', 9600)

print(ser.name)

while 1:
    blah = ser.readline()
    if blah != '':
        print blah
