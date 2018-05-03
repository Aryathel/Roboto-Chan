#Import Tkinter Module
from Tkinter import *
import serial
import time

time.sleep(3)

#Set up the USB readin for the Serial cable to the Arduino
ser = serial.Serial('/dev/ttyUSB0', 9600) #needs to be updated with proper terminal later

#Start the Root GUI
root = Tk()

#Reading the Serial Monitor to find the current values


#Function for Updating Data
def updateData():
	global data
	data = ser.readline().split("  ")
	print(data)

updateData()

#Parameters for the Root Window
root.title("Roboto-chan Controls")
root.geometry("800x800")

#Entries Function for User Text Entry Test
def submit_entries():
	X = entry1.get()
	Y = entry2.get()
	Z = entry3.get()
	print("X: %s\nY: %s\nZ: %s" % (X, Y, Z))

#Test Function for Buttons
def test():
	print("This is a test button.")

#Button Control for Simple Movement
def rotateRight():
	updateData()
	increment = entry4.get()
	angleBase = data[4].split(" ")
	newAngleBase = int(angleBase[2]) + int(increment)
	print(angleBase[2])
	if newAngleBase > 180:
		print("Angle Can Not Be Larger Than 180 Degrees!")
		newAngleBase = 180
	print(newAngleBase)

def rotateLeft():
	increment = entry4.get()
	angleBase = data[4].split(" ")
	newAngleBase = int(angleBase[2]) - int(increment)
	print(angleBase[2])
	if newAngleBase < 64:
		print("Angle Can Not Be Less Than 64 Degrees!")
		newAngleBase = 64
	print(newAngleBase)

def rotateRightServoForward():
	increment = entry4.get()
	angleRight = data[5].split(" ")
	newAngleRight = int(angleRight[2]) + int(increment)
	print(angleRight[2])
	if newAngleRight > 180:
		print("Angle Can Not Be Greater Than 180 Degrees!")
		newAngleRight = 180
	print(newAngleBase)

def rotateRightServoBackward():
	increment = entry4.get()
	angleRight = date[5].split(" ")
	newAngleRight = int(angleRight[2]) - int(increment)
	print(angleRight[2])
	if newAngleRight < 90:
		print("Angle Can Not Be Less Than 90 Degrees!")
		newAngleRight = 90
	print(newAngleRight)

#User Text Entry Test
Label(root, text = "X").grid(row = 0)
Label(root, text = "Y").grid(row = 1)
Label(root, text = "Z").grid(row = 2)

entry1 = Entry(root)
entry2 = Entry(root)
entry3 = Entry(root)

entry1.grid(row = 0, column = 1)
entry2.grid(row = 1, column = 1)
entry3.grid(row = 2, column = 1)

#Buttons For Entry Fields
Button(root, text = "Quit", command = root.quit).grid(row = 3, column = 0, pady = 10)
Button(root, text = "Submit", command = submit_entries).grid(row = 3, column = 2, pady = 10)

Label(root, text = "Movement Increment:").grid(row = 4, pady = 10)

entry4 = Entry(root)
entry4.grid(row = 5)
entry4.insert(5, "10")


Button(root, text = "Move Forward", command = test).grid(row = 8, column = 3)
Button(root, text = "Rotate Left", command = rotateLeft).grid(row = 9, column = 2)
Button(root, text = "Activate/Release Claw", command = test).grid(row = 9, column = 3)
Button(root, text = "Rotate Right", command = rotateRight).grid(row = 9, column = 4)
Button(root, text = "Move Backward", command = test).grid(row = 10, column = 3) 
Button(root, text = "Move Upwards", command = test).grid(row = 8, column = 1)
Button(root, text = "Move Downwards", command = test).grid(row = 10, column = 1)

#Restart the Loop
root.mainloop()
