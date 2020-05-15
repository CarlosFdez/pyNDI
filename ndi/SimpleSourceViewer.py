# pyNDI Made by CarlosFdez
# Example by Joel Luther-Braun / Github(@Hantoo)

#pyNDI Import
import finder
import receiver
import lib
#Other Import
import cv2
import imutils

find = finder.create_ndi_finder()
NDIsources = find.get_sources()

recieveSource = None; 

# If there is one or more sources then list the names of all source.
# If only 1 source is detected, then automatically connect to that source.
# If more than 1 source detected, then list all sources detected and allow user to choose source.
if(len(NDIsources) > 0):
	print(str(len(NDIsources)) + " NDI Sources Detected")
	for x in range(len(NDIsources)):
		print(str(x) + ". "+NDIsources[x].name + " @ "+str(NDIsources[x].address))
	if(len(NDIsources) == 1):
		#If only one source, connect to that source
		recieveSource = NDIsources[0]
		print("Automatically Connecting To Source...")
	else:
		awaitUserInput = True;
		while(awaitUserInput):
			print("")
			try:
				key = int(input("Please choose a NDI Source Number to connect to:"))
				if(key < len(NDIsources) and key >= 0):
					awaitUserInput = False
					recieveSource = NDIsources[key]
				else:
					print("Input Not A Number OR Number not in NDI Range. Please pick a number between 0 and "+ str(len(NDIsources)-1))		
			except:
				print("Input Not A Number OR Number not in NDI Range. Please pick a number between 0 and "+ str(len(NDIsources)-1))
		
		#If more than one source, ask user which NDI source they want to use		
else:
	print("No NDI Sources Detected - Please Try Again")



print("Width Resized To 500px. Not Actual Source Size")
reciever = receiver.create_receiver(recieveSource)

while(1):
	frame = reciever.read()
	size = [str(frame.shape[0]),str(frame.shape[1]), frame.shape[2]]
	frame = imutils.resize(frame, width=500)
	cv2.putText(frame, recieveSource.name,(0,15),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
	cv2.putText(frame, "Size:"+ size[1] + "x" +size[0],(0,35),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
	mode = ""
	if(size[2] == 4):
		mode = "RGB Alpha"
	if(size[2] == 3):
		mode = "RGB"	
	cv2.putText(frame, "Mode:"+ mode,(0,55),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
	
	cv2.imshow("image", frame)
	k = cv2.waitKey(30) & 0xff
	if k == 27:
		break
  
print("User Quit")
cv2.destroyAllWindows()