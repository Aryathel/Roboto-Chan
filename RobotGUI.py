#Import Tkinter Module
import Tkinter as tk
import serial
import time


#Set up the USB reading for the Serial cable to the Arduino
ser = serial.Serial('/dev/ttyUSB1', 9600) #needs to be updated with proper terminal later
print ser.name

time.sleep(5)

#Start the Root GUI
root = tk.Tk()

#Reading the Serial Monitor to find the current values
actuate = ser.write('s')
time.sleep(0.5)
data = ser.readline()

print data
entries = data.split(" ")

#Parameters for the Root Window
root.title("Roboto-chan Controls")
root.geometry("800x800")

#Function for Updating the Servo Positions
def updateData():
	global data
	actuate = ser.write('s')
	time.sleep(0.5)
	data = ser.readline()
	print(data)
	entries = data.split(" ")
	return entries

#Function For Reading Location
def updateLocs():
	updateData()
	time.sleep(0.5)
	angleBase = entries[4]
	print angleBase
	currentBaseAngleLabel['text'] = "Base Servo: " + angleBase

	angleRight = entries[5]
	print angleRight
	currentRightAngleLabel['text'] = "Right Servo: " + angleRight

	angleLeft = entries[6]
	print angleLeft
	currentLeftAngleLabel['text'] = "Left Servo: " + angleLeft

#Entries Function for User Text Entry Test
def submit_entries():

	#Read the Entry Fields
	Base = entry1.get()
	Right = entry2.get()
	Left = entry3.get()

	#Safety Functions To Keep The Servo Within Our Bounds
	if int(Base) > 180:
		print("Angle Can Not Be Greater Than 180 Degrees!")
		Base = 180
	if int(Base) < 64:
		print("Angle Can Not Be Less Than 64 Degrees!")
		Base = 64

	if int(Right) > 180:
		print("Angle Can Not Be Greater Than 180 Degrees!")
		Right = 180
	if int(Right) < 90:
		print("Angle Can Not Be Less Than 90 Degrees!")
		Right = 90

	if int(Left) > 160:
		print("Angle Can Not Be Greater Than 160 Degrees!")
		Left = 160
	if int(Left) < 51:
		print("Angle Can Not Be Less Than 51 Degrees!")
		Left = 51

	print("Base: %s\nRight: %s\nLeft: %s" % (Base, Right, Left))

#Test Function for Buttons
def test():
	print("This is a test button.")

#Functions for Simple Movement
def rotateRight():
	updateLocs()
	increment = entry4.get()
	angleBase = entries[4]
	newAngleBase = int(angleBase) + int(increment)
	print(angleBase)
	if newAngleBase > 180:
		print("Angle Can Not Be Greater Than 180 Degrees!")
		newAngleBase = 180
	print(newAngleBase)

def rotateLeft():
	updateData()
	increment = entry4.get()
	angleBase = entries[4]
	newAngleBase = int(angleBase) - int(increment)
	print(angleBase)
	if newAngleBase < 64:
		print("Angle Can Not Be Less Than 64 Degrees!")
		newAngleBase = 64
	print(newAngleBase)

def rotateRightServoForward():
	updateData()
	increment = entry4.get()
	angleRight = entries[5]
	newAngleRight = int(angleRight) + int(increment)
	print(angleRight)
	if newAngleRight > 180:
		print("Angle Can Not Be Greater Than 180 Degrees!")
		newAngleRight = 180
	print(newAngleRight)

def rotateRightServoBackward():
	updateData()
	increment = entry4.get()
	angleRight = entries[5]
	newAngleRight = int(angleRight) - int(increment)
	print(angleRight)
	if newAngleRight < 90:
		print("Angle Can Not Be Less Than 90 Degrees!")
		newAngleRight = 90
	print(newAngleRight)

def rotateLeftServoForward():
	updateData()
	increment = entry4.get()
	angleLeft = entries[6]
	newAngleLeft = int(angleLeft) + int(increment)
	print(angleLeft)
	if newAngleLeft > 160:
		print("Angle Can Not Be Greater Than 160 Degrees!")
		newAngleLeft = 160
	print(newAngleLeft)

def rotateLeftServoBackward():
	updateData()
	increment = entry4.get()
	angleLeft = entries[6]
	newAngleLeft = int(angleLeft) - int(increment)
	print(angleLeft)
	if newAngleLeft < 51:
		print("Angle Can Not Be Less Than 51 Degrees!")
		newAngleLeft = 51
	print(newAngleLeft)

#Labels For Reading The Current Locations of the Servos
currentBaseAngleLabel = tk.Label(root)
currentBaseAngleLabel.grid(row = 0, column = 0)

currentRightAngleLabel = tk.Label(root)
currentRightAngleLabel.grid(row = 1, column = 0)

currentLeftAngleLabel = tk.Label(root)
currentLeftAngleLabel.grid(row = 2, column = 0)

#User Text Entry For Simple Movements
tk.Label(root, text = "X").grid(row = 0, column = 2)
tk.Label(root, text = "Y").grid(row = 1, column = 2)
tk.Label(root, text = "Z").grid(row = 2, column = 2)

entry1 = tk.Entry(root)
entry2 = tk.Entry(root)
entry3 = tk.Entry(root)

entry1.grid(row = 0, column = 3)
entry2.grid(row = 1, column = 3)
entry3.grid(row = 2, column = 3)

#Buttons For Entry Fields
tk.Button(root, text = "Quit", command = root.quit).grid(row = 3, column = 0, pady = 10)
tk.Button(root, text = "Submit", command = submit_entries).grid(row = 3, column = 2, pady = 10)


#Simple Movement Increment Field
tk.Label(root, text = "Movement Increment:").grid(row = 4, pady = 10)

entry4 = tk.Entry(root)
entry4.grid(row = 5)
entry4.insert(5, "10")

#Buttons For Simple Movements
tk.Button(root, text = "Left Servo Forward", command = rotateLeftServoForward).grid(row = 8, column = 3)
tk.Button(root, text = "Left Servo Backward", command = rotateLeftServoBackward).grid(row = 10, column = 3)

tk.Button(root, text = "Rotate Base Left", command = rotateLeft).grid(row = 8, column = 5)
tk.Button(root, text = "Rotate Base Right", command = rotateRight).grid(row = 10, column = 5)

tk.Button(root, text = "Right Servo Forward", command = rotateRightServoForward).grid(row = 8, column = 1)
tk.Button(root, text = "Right Servo Backward", command = rotateRightServoBackward).grid(row = 10, column = 1)

tk.Button(root, text = "Activate/Release Claw", command = test).grid(row = 9, column = 0)

#Restart the Loop
root.mainloop()
