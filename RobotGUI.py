#Import Tkinter Module
import Tkinter as tk
import tkMessageBox
import serial
import time
import math

#Start the Root GUI
root = tk.Tk()

#Parameters for the Root Window
root.title("Roboto-chan Controls")
root.geometry("800x800")

#Set up the USB reading for the Serial cable to the Arduino
ser = serial.Serial('/dev/ttyUSB0', 9600) #needs to be updated with proper terminal later
print ser.name

time.sleep(10)

#Reading the Serial Monitor to find the current values
actuate = ser.write('a')
data = ser.readline()
print data
entries = data.split(" ")


#Function for Updating the Servo Positions
def updateData():
	global data
	global entries
	actuate = ser.write('a')
	data = ser.readline()
	entries = data.split(" ")

#Function For Reading Location
def updateLocs():
	global entries
	updateData()
	angleBase = entries[4]
	angleRight = entries[5]
	angleLeft = entries[6]
	angleClaw = entries[7].strip("\r\n")

	currentBaseAngleLabel.config(text="Base: %s" % (angleBase))
	currentBaseAngleLabel.update()
	currentBaseAngleLabel.after(200, updateLocs)

	currentRightAngleLabel.config(text="Right: %s" % (angleRight))
	currentRightAngleLabel.update()

	currentLeftAngleLabel.config(text="Left: %s" % (angleLeft))
	currentLeftAngleLabel.update()

	currentClawAngleLabel.config(text="Claw: %s" % (angleClaw))
	currentClawAngleLabel.update()

	#Labels For Stating The Min and Max The User Can Write To
	baseMaxMinLabel.config(text = "Minimum: %s || Maximum: %s" % (baseMin, baseMax))
	baseMaxMinLabel.update()

	rightMaxMinLabel.config(text = "Minimum: %s || Maximum: %s" % (rightMin, rightMax))
	rightMaxMinLabel.update()

	if int(angleRight) >= 87:
		leftMaxMinLabel.config(text = "Minimum: %s || Maximum: %s" % (str(mapVal(int(angleRight), int(rightMid), int(rightMax), 100, 105)), str(mapVal(int(angleRight), int(rightMid), int(rightMax), 180, 172))))
	elif int(angleRight) < 87:
		leftMaxMinLabel.config(text = "Minimum: %s || Maximum: 180" % (str(mapVal(int(angleRight), int(rightMid), int(rightMin), 100, 135))))

	leftMaxMinLabel.update()

#Entries Function for User Text Entry Test
def submit_entries():
	updateData()

	#Read the Entry Fields
	Base = entry1.get()
	Right = entry2.get()
	Left = entry3.get()

	#Safety Functions To Keep The Servo Within Our Bounds
	if int(Base) > 180:
		print("Angle Can Not Be Greater Than 180 Degrees!")
		tkMessageBox.showwarning("You are Dumb!", "The Base Angle Can Not Be More Than 180 Degrees!")
		Base = entries[4]
	elif int(Base) < 64:
		print("Angle Can Not Be Less Than 64 Degrees!")
		tkMessageBox.showwarning("You are Dumb!", "The Base Angle Can Not Be Less Than 64 Degrees!")
		Base = entries[4]

	if int(Right) > 156:
		print("Angle Can Not Be Greater Than 156 Degrees!")
		tkMessageBox.showwarning("You are Dumb!", "The Right Angle Can Not Be More Than 156 Degrees!")
		Right = entries[5]
	elif int(Right) < 46:
		print("Angle Can Not Be Less Than 46 Degrees!")
		tkMessageBox.showwarning("You are Dumb!", "The Right Angle Can Not Be Less Than 46 Degrees!")
		Right = entries[5]

	#Find Min and Max for Left Servo
	if int(Right) >= 87:
		leftMin = mapVal(int(Right), int(rightMid), int(rightMax), 100, 105)
		leftMax = mapVal(int(Right), int(rightMid), int(rightMax), 180, 172)
	elif int(Right) < 87:
		leftMin = mapVal(int(Right), int(rightMid), int(rightMin), 100, 135)
		leftMax = 180


	if int(Left) >= leftMax:
		print("Angle Can Not Be Greater Than %s Degrees!" % (leftMax))
		tkMessageBox.showwarning("You are Dumb!", "The Left Angle Can Not Be More Than %s Degrees!" % (leftMax))
		Left = entries[6]
	elif int(Left) < leftMin:
		print("Angle Can Not Be Less Than %s Degrees!" % (leftMin))
		tkMessageBox.showwarning("You are Dumb!", "The Left Angle Can Not Be Less Than %s Degrees!" % (leftMin))
		Left = entries[6]

	rotateBase(Base)
	rotateRight(Right)
	rotateLeft(Left)

#Test Function for Buttons
def test():
	print("This is a test button.")

#Function for Finding the Max and Min of the Left Servo At Any Given Time
def mapVal(a, b, c, d, e):
	return int((a-b) * (e-d) / (c-b) + d)

#Functions for Planning Movement
def rotateBaseRight():
	updateData()
	increment = entry4.get()
	angleBase = entries[4]
	newAngleBase = int(angleBase) + int(increment)
	print(angleBase)
	if newAngleBase > 180:
		print("Angle Can Not Be Greater Than 180 Degrees!")
		newAngleBase = 180
	print(newAngleBase)
	rotateBase(newAngleBase)

def rotateBaseLeft():
	updateData()
	increment = entry4.get()
	angleBase = entries[4]
	newAngleBase = int(angleBase) - int(increment)
	print(angleBase)
	if newAngleBase < 64:
		print("Angle Can Not Be Less Than 64 Degrees!")
		newAngleBase = 64
	print(newAngleBase)
	rotateBase(newAngleBase)

def rotateRightServoForward():
	updateData()
	increment = entry4.get()
	angleRight = entries[5]
	newAngleRight = int(angleRight) + int(increment)
	print(angleRight)
	if newAngleRight > 156:
		print("Angle Can Not Be Greater Than 156 Degrees!")
		newAngleRight = 156
	print(newAngleRight)
	rotateRight(newAngleRight)

def rotateRightServoBackward():
	updateData()
	increment = entry4.get()
	angleRight = entries[5]
	newAngleRight = int(angleRight) - int(increment)
	print(angleRight)
	if newAngleRight < 46:
		print("Angle Can Not Be Less Than 46 Degrees!")
		newAngleRight = 46
	print(newAngleRight)
	rotateRight(newAngleRight)

def rotateLeftServoBackward():
	updateData()
	increment = entry4.get()
	angleLeft = entries[6]
	newAngleLeft = int(angleLeft) + int(increment)
	print(angleLeft)
	if newAngleLeft > 180:
		print("Angle Can Not Be Greater Than 180 Degrees!")
		newAngleLeft = 180
	print(newAngleLeft)
	rotateLeft(newAngleLeft)

def rotateLeftServoForward():
	updateData()
	increment = entry4.get()
	angleLeft = entries[6]
	newAngleLeft = int(angleLeft) - int(increment)
	print(angleLeft)
	if newAngleLeft < 100:
		print("Angle Can Not Be Less Than 100 Degrees!")
		newAngleLeft = 100
	print(newAngleLeft)
	rotateLeft(newAngleLeft)

#Functions for Actuating Movement
def rotateBase(newAngle):
	ser.write('s')
	ser.write('1')
	ser.write(str(newAngle) + ',')

def rotateRight(newAngle):
	ser.write('s')
	ser.write('2')
	ser.write(str(newAngle) + ',')

def rotateLeft(newAngle):
	ser.write('s')
	ser.write('3')
	ser.write(str(newAngle) + ',')

def writeusBase(newus):
	print("Thingy")

def writeusRight(newus):
	print("Thingy")

def writeusLeft(newus):
	print("Thingy")

#Globals for using the step function
lastWrittenBase = 0;
lastWrittenRight = 0;
lastWrittenLeft = 0;

def updateXYZ():
	global curXYZ
	updateData()
        bA = int(entries[4]) - 21
        rA = int(entries[5]) + 3
        lA = int(entries[6]) - 167
        pR = (16.669 * math.cos(bA), 15.561 * math.sin(bA), 30.125) #Position of right servo point of rotation
        pRe = (pR[0] * math.cos(bA), pR[1] + (80 * math.cos(rA)) * math.sin(bA), pR[2] + 80 * math.sin(rA)) #Right arm endpoint
        #Claw base endpoint:
        pCb = (pRe[0] - math.cos(-1 / bA) * 10.375 + (80 * math.cos(lA)) * math.cos(bA), pRe[1] + (80 * math.cos(lA)) * math.sin(bA), pRe[2] + 80 * math.sin(lA))
	pCe = (pCb[0] - 1.625 - 12, pCb[1] + 56.793, pCb[2] - 1.2 - 3.25 - 1.625)
	curXYZ = pCe

curXYZ = (0, 0, 0)

updateXYZ()

locsToWriteTo = [(0, 0, 0)]

def stepTo(x, y, z):
	global lastWrittenBase
	global lastWrittenLeft
	global lastWrittenRight
	global locsToWriteTo
	locsToWriteTo.clear()
	updateXYZ()
	dX = x - curXYZ[0]
	dY = y - curXYZ[1]
	dZ = z - curXYZ[2]
	distXY = sqrt(dX**2 + dY**2)
	distXYZ = sqrt(distXY**2 + dZ**2)
	numIters = int(distXYZ / 0.1)
	thetaXY = math.atan(dY, dX)
	thetaXYZ = math.atan(dZ, distXY)
	for i in range(1, numIters + 1):
		newXYZ = (curXYZ[0] + i * math.cos(thetaXY), curXYZ[1] + i * math.sin(thetaXY), curXYZ[2] + i * math.sin(thetaXYZ))
		newDist = sqrt(sqrt(newXYZ[0]**2 + newXYZ[1]**2)**2 + newXYZ[2]**2)
		minErr = 100
		us = 0
		for j in range(1200, 2391):
			eX = (newXYZ[0] - newDist * math.cos(mapVal(j, 1200, 2390, 64, 180)))**2
			eY = (newXYZ[1] - newDist * math.sin(mapVal(j, 1200, 2390, 64, 180)))**2
			if sqrt(eX + eY) < minErr:
				us = j

		newBA = atan(newXYZ[1], newXYZ[0])

#Defining Variables for the Minimum and Maximum Servo Locations
baseMin = 64
baseMax = 180

rightMin = 46
rightMid = 87
rightMax = 156

#Labels For Reading The Current Locations Of The Servos
currentBaseAngleLabel = tk.Label(root)
currentBaseAngleLabel.grid(row = 0, column = 0)

currentRightAngleLabel = tk.Label(root)
currentRightAngleLabel.grid(row = 1, column = 0)

currentLeftAngleLabel = tk.Label(root)
currentLeftAngleLabel.grid(row = 2, column = 0)

currentClawAngleLabel = tk.Label(root)
currentClawAngleLabel.grid(row = 3, column = 0)

#Labels For Stating The Min and Max The User Can Write To
baseMaxMinLabel = tk.Label(root, text = "Minimum:  || Maximum: ")
baseMaxMinLabel.grid(row = 0, column = 4)

rightMaxMinLabel = tk.Label(root, text = "Minimum: %s || Maximum: %s")
rightMaxMinLabel.grid(row = 1, column = 4)

leftMaxMinLabel = tk.Label(root, text = "Minimum: %s || Maximum: %s")
leftMaxMinLabel.grid(row = 2, column = 4)

#User Text Entry For Simple Movements
tk.Label(root, text = "B").grid(row = 0, column = 2)
tk.Label(root, text = "R").grid(row = 1, column = 2)
tk.Label(root, text = "L").grid(row = 2, column = 2)

entry1 = tk.Entry(root)
entry1.insert(0, entries[4])

entry2 = tk.Entry(root)
entry2.insert(0, entries[5])

entry3 = tk.Entry(root)
entry3.insert(0, entries[6])

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
entry4.insert(0, "10")

#Buttons For Simple Movements
tk.Button(root, text = "Left Servo Forward", command = rotateLeftServoForward).grid(row = 8, column = 3)
tk.Button(root, text = "Left Servo Backward", command = rotateLeftServoBackward).grid(row = 10, column = 3)

tk.Button(root, text = "Rotate Base Clockwise", command = rotateBaseLeft).grid(row = 8, column = 4)

tk.Button(root, text = "Rotate Base Anti-Clockwise", command = rotateBaseRight).grid(row = 10, column = 4)

tk.Button(root, text = "Right Servo Forward", command = rotateRightServoForward).grid(row = 8, column = 1)
tk.Button(root, text = "Right Servo Backward", command = rotateRightServoBackward).grid(row = 10, column = 1)

tk.Button(root, text = "Activate/Release Claw", command = test).grid(row = 9, column = 0)

updateLocs()

#Restart the Loop
root.mainloop()
