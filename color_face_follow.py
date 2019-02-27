import cv2
import numpy as np
import serial

def nothing(x):
    pass

# INIT #
center=0
error=0
exist=0

follow_type = "face" #color or face
ard_send = False #send to arduino

show = {
	"original" : False,
	"mask" : True,
	"mask result" : True,
}
########

if (ard_send):
	PORT='COM3'
	ser=serial.Serial(PORT,9600)

cap = cv2.VideoCapture(0)

if (follow_type == "color"):
	cv2.namedWindow('image')
	cv2.namedWindow('morpho')
	# create trackbars for color change
	cv2.createTrackbar('Hmin','image',0,255,nothing)
	cv2.createTrackbar('Smin','image',0,255,nothing)
	cv2.createTrackbar('Vmin','image',222,255,nothing)
	cv2.createTrackbar('Hmax','image',201,255,nothing)
	cv2.createTrackbar('Smax','image',173,255,nothing)
	cv2.createTrackbar('Vmax','image',255,255,nothing)
	cv2.createTrackbar('opening','morpho',1,50,nothing)
	cv2.createTrackbar('closing','morpho',1,50,nothing)
	cv2.setTrackbarMin ('opening','morpho',1)
	cv2.setTrackbarMin ('closing','morpho',1)
else:
	face_cascade = cv2.CascadeClassifier("C:\\Users\\faidra\\AppData\\Local\\conda\\conda\\envs\\parousiasi_28.2.19\\Library\\etc\\haarcascades\\haarcascade_frontalface_default.xml") 
	eye_cascade = cv2.CascadeClassifier("C:\\Users\\faidra\\AppData\\Local\\conda\\conda\\envs\\parousiasi_28.2.19\\Library\\etc\\haarcascades\\haarcascade_eye.xml")

while(1):
	# Take each frame
	_, img = cap.read()
	img = cv2.flip(img,1)
	if(follow_type=="face"):
		#rgb2gray
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray, 1.1, 5)
		exist = False
		res = np.copy(img)
		for (x,y,w,h) in faces:
			res = cv2.rectangle(res,(x,y),(x+w,y+h),(255,0,0),2)
			roi_gray = gray[y:y+h, x:x+w]
			roi_color = res[y:y+h, x:x+w]
			#eyes = eye_cascade.detectMultiScale(roi_gray)
			#for (ex,ey,ew,eh) in eyes:
			#    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
			center=int((x+x+w)/2)
			exist = True
	else:
		# Convert BGR to HSV
		hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		# get current positions of four trackbars
		hmin = cv2.getTrackbarPos('Hmin','image')
		smin = cv2.getTrackbarPos('Smin','image')
		vmin = cv2.getTrackbarPos('Vmin','image')
		hmax = cv2.getTrackbarPos('Hmax','image')
		smax = cv2.getTrackbarPos('Smax','image')
		vmax = cv2.getTrackbarPos('Vmax','image')
		opening = cv2.getTrackbarPos('opening','morpho')
		closing = cv2.getTrackbarPos('closing','morpho')
		# define range in HSV
		lower=np.array([hmin,smin,vmin])
		upper=np.array([hmax,smax,vmax])
		# Threshold the HSV image to get the color
		mask = cv2.inRange(hsv, lower, upper)
		opening_kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(opening,opening))
		closing_kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(closing,closing))
		mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, opening_kernel)
		mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, closing_kernel)
		# Bitwise-AND mask and original image
		mask_res = cv2.bitwise_and(img,img, mask = mask)
		#find contours on mask
		_, contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		res = np.copy(img)
		if len(contours) != 0:
			biggest_c = max(contours, key = cv2.contourArea)
			cv2.drawContours(res, [biggest_c], -1, (0,255,0), 3)
			(x,y,w,h) = cv2.boundingRect(biggest_c)
			cv2.rectangle(res, (x,y), (x+w,y+h), (255, 0, 0), 2)
			center=int((x+x+w)/2)
			exist = True
		else:
			exist = False
			error = 0
		if(show['mask']):
			cv2.imshow('mask',mask)
		if(show['mask result']):
			cv2.imshow('mask result',mask_res)

	cv2.imshow('result',res)
	if(show['original']):
		cv2.imshow('original',img)

	#send to arduino
	if(exist and ard_send):
		height, width, _ = img.shape
		error=round(8*center/width)
		print(error)
		ser.write((str(error)+'\n').encode())
	k = cv2.waitKey(5) & 0xFF
	if k == ord('k'):
		break

if( ard_send):
	ser.close()
cv2.destroyAllWindows()	