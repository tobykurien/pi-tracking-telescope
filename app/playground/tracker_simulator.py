import time
import random
import sys
import cv2
import numpy as np
from opencv_samples.common import draw_str

sys.path.append('../')
from modules.tracking import ProcessTracking

p = "../../../piscope-videos/constellation.mp4"
#p = "../../../piscope-videos/jupiter.mp4"

noise_x = 5
noise_y = 5
slope_x = 50 #(0.5 - random.random())*20
slope_y = 50 #(0.5 - random.random())*20
degree_per_step_x = 1.0 *(random.random()+0.5)
degree_per_step_y = 1.0 *(random.random()+0.5)
bump_x = 0.0
bump_y = 0.0
draw_trails=False

print slope_x,slope_y, degree_per_step_x, degree_per_step_y

last_time = time.time()

class PiScopeProxy:
   def __init__(self):
      self.x_correction = 0
      self.y_correction = 0

   def setCorrection(self, x_correction, y_correction):
      self.x_correction = x_correction
      self.y_correction = y_correction


cap = cv2.VideoCapture(p)
ret, frame = cap.read()  
rows,cols = frame.shape[:2]

piscope = PiScopeProxy()
tracker = ProcessTracking(piscope)
tracker.controllerX.SetKp(2.0)
tracker.controllerX.SetKi(1.0)
tracker.controllerY.SetKp(2.0)
tracker.controllerY.SetKi(1.0)

tracker.start()


def now():
   time.time() - time_origin

def bump(x):
   if random.random()<x:
      return 1
   else:
      return 0


while True:
      dt = (time.time() - last_time)
      last_time = time.time()

      x = int((0.5-random.random())*noise_x + dt*slope_x-dt*piscope.x_correction*degree_per_step_x+ bump(bump_x)*50)
      y = int((0.5-random.random())*noise_y + dt*slope_y-dt*piscope.y_correction*degree_per_step_y+bump(bump_y)*50)
      M = np.float32([[1,0,x],[0,1,y]])
      frame = cv2.warpAffine(frame,M,(cols,rows))

      tracker.queue.put(frame)
      
      vis_frame = frame.copy()
      draw_str(vis_frame, (20, 20), 'track count: %d' % len(tracker.tracks))
      if draw_trails:
         cv2.polylines(vis_frame, [np.int32(tr) for tr in [[t[:2] for t in tr]  for tr in tracker.tracks]], False, (0, 255, 0))

      for tr in tracker.tracks:
         cv2.circle(vis_frame, (tr[-1][0], tr[-1][1]), 2, (0, 255, 0), -1)

      cv2.imshow('lk_track', vis_frame)
      ch = 0xFF & cv2.waitKey(1)
      if ch == 27:
          break
      time.sleep(0.1)





