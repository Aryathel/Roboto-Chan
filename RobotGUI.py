#Import Tkinter Module
import tkinter as tk
from tkinter import messagebox
import serial

#Set up the USB readin for the Serial cable to the Arduino
ser = serial.Serial('/dev/tty*', 9600) #needs to be updated with proper terminal later

#Start the Root GUI
root = tk.Tk()

#Reading the Serial Monitor to find the current values
currentValue = ser.readline()

#Parameters for the Root Window
root.title("Roboto-chan Controls")
root.geometry("800x800")

#Entries Function for User Text Entry Test
def submit_entries():
	X = entry1.get()
	Y = entry2.get()
	Z = entry3.get()
	print("X: %s\nY: %s\nZ: %s" % (X, Y, Z))

def show_entries():
	X = entry1.get()
	Y = entry2.get()
	Z = entry3.get()
	messagebox.showinfo("User Entries", "X: %s\nY: %s\nZ: %s" % (X, Y, Z))

#Test Function for Buttons
def test():
	print("This is a test button.")

#Button Control for Simple Movement
def rotate_right():
	increment = entry4.get()


#User Text Entry Test
tk.Label(root, text = "X").grid(row = 0)
tk.Label(root, text = "Y").grid(row = 1)
tk.Label(root, text = "Z").grid(row = 2)

entry1 = tk.Entry(root)
entry2 = tk.Entry(root)
entry3 = tk.Entry(root)

entry1.grid(row = 0, column = 1)
entry2.grid(row = 1, column = 1)
entry3.grid(row = 2, column = 1)

#Buttons For Entry Fields
tk.Button(root, text = "Quit", command = root.quit).grid(row = 3, column = 0, pady = 10)
tk.Button(root, text = "Show Entries", command = show_entries).grid(row = 3, column = 1, pady = 10)
tk.Button(root, text = "Submit", comman = submit_entries).grid(row = 3, column = 2, pady = 10)

tk.Label(root, text = "Movement Increment:").grid(row = 4, pady = 10)

entry4 = tk.Entry(root)
entry4.grid(row = 5)
entry4.insert(5, "10")


tk.Button(root, text = "Move Forward", command = test).grid(row = 8, column = 3)
tk.Button(root, text = "Rotate Left", command = test).grid(row = 9, column = 2)
tk.Button(root, text = "Activate/Release Claw", command = test).grid(row = 9, column = 3)
tk.Button(root, text = "Rotate Right", command = test).grid(row = 9, column = 4)
tk.Button(root, text = "Move Backward", command = test).grid(row = 10, column = 3) 

#Restart the Loop
root.mainloop()