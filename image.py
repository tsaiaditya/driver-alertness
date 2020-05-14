from scipy.spatial import distance
from imutils import face_utils
import imutils
import dlib
import cv2
#from keys import PressKey, ReleaseKey, B
import time
import call
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
id=int(input("Enter Driver id:"))
t = 0.01
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")

web = webdriver.Chrome('./chromedriver', chrome_options=options)
#web = webdriver.Chrome('/Desktop/ML/lol/Driver-Alertness-System/chromedriver')
web.set_window_position(-10000,0)


def changevalue():
	web.get("http://127.0.0.1:8000/parameter/"+str(id)+"/update")
	desc = web.find_element_by_id('id_description')
	desc.clear()
	desc.send_keys('UNSAFE DRIVING'+ Keys.ENTER)
	web.find_element_by_xpath('/html/body/div/div[2]/div/div/form/button').click()
	web.close()
def eye_aspect_ratio(eye):
	A = distance.euclidean(eye[1], eye[5])
	B = distance.euclidean(eye[2], eye[4])
	C = distance.euclidean(eye[0], eye[3])
	ear = (A + B) / (2.0 * C)
	return ear

thresh = 0.25
frame_check = 20
detect = dlib.get_frontal_face_detector()
predict = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

cap=cv2.VideoCapture(0)
flag=0
reset = False
while True:
	ret, frame=cap.read()
	frame = imutils.resize(frame, width=450)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	subjects = detect(gray, 0)
	for subject in subjects:
		shape = predict(gray, subject)
		shape = face_utils.shape_to_np(shape)#converting to NumPy Array
		leftEye = shape[lStart:lEnd]
		rightEye = shape[rStart:rEnd]
		leftEAR = eye_aspect_ratio(leftEye)
		rightEAR = eye_aspect_ratio(rightEye)
		ear = (leftEAR + rightEAR) / 2.0
		leftEyeHull = cv2.convexHull(leftEye)
		rightEyeHull = cv2.convexHull(rightEye)
		cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
		cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
		if ear < thresh:
			flag += 1
			#print (flag)
			if flag >= frame_check:
				cv2.putText(frame, "****************ALERT!****************", (10, 30),
					cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
				cv2.putText(frame, "****************ALERT!****************", (10,325),
					cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
				changevalue()
				if not reset:
					reset = True
					#PressKey(B)
					time.sleep(t)
					#ReleaseKey(B)
					
					call.call("SOS!!! You've been registered as the emergency contact for <Person>")
		else:
			flag = 0
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("x"):
		cv2.destroyAllWindows()
		cap.release()
		break
