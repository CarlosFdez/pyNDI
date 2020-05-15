# pyNDI Made by CarlosFdez
# Example by Joel Luther-Braun / Github(@Hantoo)

# TKInter GUI example showing NDI Sources
# When the list is updated/refreshed, every 30 seconds, the frame refresh will stop for 5 seconds
# If the source being used is closed then the program will crash


#pyNDI Import
import finder
import receiver
import lib
#Other Import
import imutils
import tkinter as tk
import time
import numpy as np
import PIL
from PIL import Image, ImageTk

recieveSource = None; 
NDIsources = None;
NDISourceList = None;
# FUNCTIONS
def getSources():
	return find.get_sources()

def setNDISource(value):
	global recieveSource
	global frameimage 
	global currentStatus
	currentStatus.set("Retreving NDI Source")
	frameimage = None
	recieveSource = receiver.create_receiver(NDIsources[value])
	 
def generateSourceList():
	global currentStatus
	global NDIsources
	global NDISourceList
	currentStatus.set("Refreshing NDI List")
	NDIsources = getSources()
	if NDISourceList is not None:
		NDISourceList.destroy()
	NDISourceList = tk.Frame()
	if(len(NDIsources) > 0):
		print(str(len(NDIsources)) + " NDI Sources Detected")
		for x in range(len(NDIsources)):
			frame = tk.Frame(master=NDISourceList,relief=tk.RAISED,borderwidth=1)
			frame.grid(row=x, column=0)
			button = (tk.Button(master=frame,text=NDIsources[x].name,width=100,height=1,command=lambda idx = x: setNDISource(idx)))
			button.pack()


	else:
		label = tk.Label(master=NDISourceList, text="No Sources Detected")
		label.pack()
	NDISourceList.pack()

def refreshFrame():
	global frameimage
	global currentStatus
	global recieveSource
	frameimage = None;
	if(recieveSource != None):
		currentStatus.set("Playing NDI Source")
		try:
			frame = recieveSource.read()
		except:
			recieveSource = None
			print("Lost source")
			currentStatus.set("Current NDI Source Lost")
			return
		frame = imutils.resize(frame, width=500)
		b, g, r, a = frame.T
		frame = np.array([r, g, b, a])
		frame = frame.transpose()
		#frameChange = frame.transpose()
		frameimage = ImageTk.PhotoImage(image=Image.fromarray(frame, mode="RGBA"))
	
	if(frameimage != None):
		canvas.create_image(0,0, anchor="nw", image=frameimage)

current_milli_time = lambda: int(round(time.time() * 1000))

# FUNCTIONs END



# Main Program

find = finder.create_ndi_finder()
#NDIsources = find.get_sources()resol
frameimage = None;

window = tk.Tk()
window.title("NDI Monitor")

canvas = tk.Canvas(width=500,height=300)
canvas.pack()
frameskip = 30;
frames = 0
nextRefreshTime = 0
nextRefreshTime_List = current_milli_time() + 10000
nextTimeInMilliseconds = 50;
currentStatus = tk.StringVar()
currentStatus.set("Awaiting NDI Source")
generateSourceList()
tk.Label(textvariable=currentStatus).pack()

while(1):

	if current_milli_time() > nextRefreshTime:
		refreshFrame()
		nextRefreshTime = current_milli_time() + nextTimeInMilliseconds
	if current_milli_time() > nextRefreshTime_List:
		generateSourceList()
		nextRefreshTime_List = current_milli_time() + 30000
	#if frames % frameskip == 0: 
		
	window.update()
	frames = frames + 1
# Main Program End
