#Import Tkinter Module
import Tkinter as tk
import tkMessageBox
import serial
import time
import math

from cffi import FFI
ffi = FFI()
ffi.cdef("""
        int find_optimal_base_us(int, int);
""")

armtest = ffi.dlopen("/home/pi/Desktop/Roboto-Chan_local/armtest/target/armv7-unknown-linux-gnueabihf/release/libarmtest.so")

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

def toggleLabels():
        global polar

        if polar:
                polar != polar
                toggleButton.config(text = "Cartesian")
                toggleButton.update()

                textEntryTop.config(text = "X")
                textRnteyTop.update()

                textEntryMid.config(text = "Y")
                textEntryMid.update()

                textEntryBot.config(text = "Z")
                textEntryBot.update()

                movementIncrementLabel.config(text = "Movement increment (mm):")
                movementIncrementLabel.update()

                lyposButton.config(text = "Y+")
                lyposButton.update()

                lynegButton.config(text = "Y-")
                lynegButton.update()

                bxposButton.config(text = "X+")
                bxposButton.update()

                bxnegButton.config(text = "X-")
                bxnegButton.update()

                rznegButton.config(text = "Z-")
                rznegButton.update()

                rzposButton.config(text = "Z+")
                rzposButton.update()
                return
        elif not polar:
                polar != polar
                toggleButton.config(text = "Polar")
                toggleButton.update()

                textEntryTop.config(text = "B")
                textEntryTop.update()

                textEntryMid.config(text = "R")
                textEntryMid.update()

                textEntryBot.config(text = "L")
                textEntryBot.update()

                movementIncrementLabel.config(text = "Movement increment (degrees):")
                movementIncrementLabel.update()

                lyposButton.config(text = "L CW")
                lyposButton.update()

                lynegButton.config(text = "L CCW")
                lynegButton.update()

                bxposButton.config(text = "B CW")
                bxposButton.update()

                bxnegButton.config(text = "B CCW")
                bxnegButton.update()

                rznegButton.config(text = "R CCW")
                rznegButton.update()

                rzposButton.config(text = "R CW")
                rzposButton.update()
                return

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

#Function for Keeping People From Doing Dumb Stuff With The Entry Boxes
def entryProtection():
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


        if int(Left) >= int(leftMax):
                entry3.config(text = leftMax)
                entry3.update()
        elif int(Left) < int(leftMin):
                entry3.config(text = leftMin)
                entry3.update()

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

#Globals for using the step function
lastWrittenBase = -1;
lastWrittenRight = -1;
lastWrittenLeft = -1;

def updateXYZ():
        global curXYZ
        updateData()
        bA = int(entries[4]) - 21
        rA = 180 - int(entries[5]) - 2
        lA = 180 - int(entries[6]) - 13
        print("Using the following angles to calculate Cartesian position - B: %s, R: %s, L: %s" % (bA, rA, lA))
        pR = (16.669 * math.cos(math.radians(bA)), 15.561 * math.sin(math.radians(bA)), 30.125) #Position of right servo point of rotation
        print("Point of rotation on the right servo: (%s, %s, %s)" % pR)
        pRe = (pR[0] * math.cos(math.radians(bA)), pR[1] + (80 * math.cos(math.radians(rA))) * math.sin(math.radians(bA)), pR[2] + 80 * math.sin(math.radians(rA))) #Right arm endpoint
        print("Location of the end of the right arm: (%s, %s, %s)" % pRe)
        #Claw base endpoint:
        pCb = (pRe[0] - math.cos(math.radians(-1 / bA)) * 10.375 + (80 * math.cos(math.radians(lA))) * math.cos(math.radians(bA)), pRe[1] + (80 * math.cos(math.radians(lA))) * math.sin(math.radians(bA)), pRe[2] + 80 * math.sin(math.radians(lA)))
        print("Location of the base of the claw section: (%s, %s, %s)" % pCb)
        pCe = (int(pCb[0]*(- 1.625 - 12) * math.cos(math.radians(bA))), int(pCb[1] + 56.793 * math.sin(math.radians(bA))), int(pCb[2] - 1.2 - 3.25 - 1.625))
        print("Location of the end of the claw: (%s, %s, %s)" % pCe)
        curXYZ = pCe

curXYZ = (0, 0, 0)

def printXYZ():
        print("Current XYZ: (%s, %s, %s)" % (curXYZ))

def printCartesianAngles():
        updateData()
        print("Current angles - B: %s, R: %s, L: %s" % (int(entries[4]) - 21, 180 - int(entries[5]) - 2, 180 - int(entries[6]) - 13))

def cartesianDebugInfo():
        printXYZ()
        printCartesianAngles()

updateXYZ()

locsToWriteTo = [(0, 0, 0)]


def clearLTWT():
        global locsToWriteTo
        for i in range(0, len(locsToWriteTo)):
                locsToWriteTo.pop()

def stepTo(x, y):
        global lastWrittenBase
        global lastWrittenLeft
        global lastWrittenRight
        global locsToWriteTo
        global curXYZ
        clearLTWT()
        updateXYZ()
        dX = x - curXYZ[0]
        dY = y - curXYZ[1]
        dZ = 0 - curXYZ[2]
        distXY = math.sqrt(dX**2 + dY**2)
        distXYZ = math.sqrt(distXY**2 + dZ**2)
        numIters = int(distXYZ / 0.1)
        thetaXY = math.atan(dY / dX)
        thetaXYZ = math.atan(dZ / distXY)
        for i in range(1, numIters + 1):
                newXYZ = (curXYZ[0] + i * 0.1 * math.cos(thetaXY), curXYZ[1] + i * 0.1 * math.sin(thetaXY), curXYZ[2] + i * 0.1 * math.sin(thetaXYZ))
                print("Calculating for: (%s, %s, %s)" % (newXYZ[0], newXYZ[1], newXYZ[2]))
                newLTWTb = lastWrittenBase
                newLTWTr = lastWrittenRight
                newLTWTl = lastWrittenLeft
                baseus = armtest.find_optimal_base_us(int(newXYZ[0]), int(newXYZ[1]))
                print("Found angle to write: %s" % ((baseus - 1200) * 116 / 1254))
                if lastWrittenBase != baseus:
                        newLTWTb = baseus
                        lastWrittenBase = baseus
                locsToWriteTo.append((newLTWTb, newLTWTr, newLTWTl))

def submitStepTo():
        global locsToWriteTo
        global lastWrittenBase
        global lastWrittenRight
        global lastWrittenLeft

        updateData()

        #Read the entry fields
        x = int(entry1.get())
        y = int(entry2.get())
        z = int(entry3.get())

        print("For testing purposes...")
        print("Optimal base us for x = 0, y = 10: %s" % armtest.find_optimal_base_us(0, 10))

        print("Starting calculations for movement...")
        stepTo(x, y)
        print("Done!")

        for i in range(0, len(locsToWriteTo)):
                if locsToWriteTo[i][0] < 1200:
                        print("Unable to complete action! us value (%s) is too small - min: 1200" % locsToWriteTo[i][0])
                        if 0 < i:
                                setLastWritten(locsToWriteTo[i - 1][0], locsToWriteTo[i - 1][1], locsToWriteTo[i - 1][2])
                        return
                if locsToWriteTo[i][0] > 2390:
                        print("Unable to complete action! us value (%s) is too large - max: 2390" % locsToWriteTo[i][0])
                        if 0 < i:
                                setLastWritten(locsToWriteTo[i - 1][0], locsToWriteTo[i - 1][1], locsToWriteTo[i - 1][2])
                        return
                #if locsToWriteTo[i][1]... finish these
                for j in range(0, 3):
                        ser.write('u')
                        ser.write(list(str(j))[0])
                        ser.write(str(locsToWriteTo[i][j]) + ",")

def setLastWritten(b, r, l):
        global lastWrittenBase
        global lastWrittenRight
        global lastWrittenLeft

#Polar or Cartesian?
polar = True

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

def standin():
        toggleLabels()

#Toggle button for "polar"/Cartesian
toggleButton = tk.Button(root, text = "Polar", width = 10, relief = "raised", command = standin).grid(row = 3, column = 1, pady = 10)

#User Text Entry For Simple Movements
textEntryTop = tk.Label(root, text = "B").grid(row = 0, column = 2)
textEntryMid = tk.Label(root, text = "R").grid(row = 1, column = 2)
textEntryBot = tk.Label(root, text = "L").grid(row = 2, column = 2)

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

tk.Button(root, text = "wewe", command = submitStepTo).grid(row = 3, column = 3, pady = 10)

tk.Button(root, text = "Cartesian Debug Info", command = cartesianDebugInfo).grid(row = 3, column = 4, pady = 10)


#Simple Movement Increment Field
movementIncrementLabel = tk.Label(root, text = "Movement increment (degrees)").grid(row = 4, pady = 10)

entry4 = tk.Entry(root)
entry4.grid(row = 5)
entry4.insert(0, "10")

#Buttons For Simple Movements
lyposButton = tk.Button(root, text = "Left Servo Forward", command = rotateLeftServoForward).grid(row = 8, column = 3)
lynegButton = tk.Button(root, text = "Left Servo Backward", command = rotateLeftServoBackward).grid(row = 10, column = 3)

bxposButton = tk.Button(root, text = "Rotate Base Clockwise", command = rotateBaseLeft).grid(row = 8, column = 4)

bxnegButton = tk.Button(root, text = "Rotate Base Anti-Clockwise", command = rotateBaseRight).grid(row = 10, column = 4)

rznegButton = tk.Button(root, text = "Right Servo Forward", command = rotateRightServoForward).grid(row = 8, column = 1)
rzposButton = tk.Button(root, text = "Right Servo Backward", command = rotateRightServoBackward).grid(row = 10, column = 1)

tk.Button(root, text = "Activate/Release Claw", command = test).grid(row = 9, column = 0)

updateLocs()



#Restart the Loop
root.mainloop()
