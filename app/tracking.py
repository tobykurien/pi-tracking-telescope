# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
 
import numpy as np
import video
from common import anorm2, draw_str
from time import clock
 
lk_params = dict( winSize  = (15, 15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

feature_params = dict( maxCorners = 500,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )

track_len = 10
detect_interval = 5
tracks = []
#cam = video.create_capture(video_src)
frame_idx = 0
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
 
# allow the camera to warmup
time.sleep(0.1)
 
# capture frames from the camera
for frm in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	frame = frm.array

	frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	vis = frame.copy()

	if len(tracks) > 0:
		img0, img1 = prev_gray, frame_gray
		p0 = np.float32([tr[-1] for tr in tracks]).reshape(-1, 1, 2)
		p1, st, err = cv2.calcOpticalFlowPyrLK(img0, img1, p0, None, **lk_params)
		p0r, st, err = cv2.calcOpticalFlowPyrLK(img1, img0, p1, None, **lk_params)
		d = abs(p0-p0r).reshape(-1, 2).max(-1)
		good = d < 1
		new_tracks = []
		for tr, (x, y), good_flag in zip(tracks, p1.reshape(-1, 2), good):
			if not good_flag:
				continue
			tr.append((x, y))
			if len(tr) > track_len:
				del tr[0]
			new_tracks.append(tr)
			cv2.circle(vis, (x, y), 2, (0, 255, 0), -1)
		tracks = new_tracks
		cv2.polylines(vis, [np.int32(tr) for tr in tracks], False, (0, 255, 0))
		draw_str(vis, (20, 20), 'track count: %d' % len(tracks))

	if frame_idx % detect_interval == 0:
		mask = np.zeros_like(frame_gray)
		mask[:] = 255
		for x, y in [np.int32(tr[-1]) for tr in tracks]:
			cv2.circle(mask, (x, y), 5, 0, -1)
		p = cv2.goodFeaturesToTrack(frame_gray, mask = mask, **feature_params)
		if p is not None:
			for x, y in np.float32(p).reshape(-1, 2):
				tracks.append([(x, y)])


	frame_idx += 1
	prev_gray = frame_gray
	cv2.imshow('lk_track', vis)


	# show the frame
	
	key = cv2.waitKey(1) & 0xFF
 
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
