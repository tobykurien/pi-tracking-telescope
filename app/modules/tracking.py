import cv2
import numpy as np
import time
from threading import Thread
from Queue import Queue
import pid


class ProcessTracking(Thread):
    """PID controller for visual tracking with opencv """    

    def __init__(self, piscopeController):
        Thread.__init__(self)
        self.piscopeController = piscopeController
        self.queue = Queue()
        self.setDaemon(True) # terminate on exit
        self.status = "Initial"
        self.controllerX = pid.PID()
        self.controllerY = pid.PID()

        self.x_correction = 0
        self.y_correction = 0

        self.prev_gray = None
        self.track_len = 5000
        self.tracks = []

        self.xerror = 0
        self.yerror = 0

        self.lk_params = dict( winSize  = (15, 15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

        self.feature_params = dict( maxCorners = 500,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )




    def getStatus(self):
        return self.status
        
    def addFrame(self, image):
        if self.queue.qsize() < 10:
            self.queue.put(image)

    def updateCorrection(self):
        self.x_correction = 0
        self.y_correction = 0
        if self.xerror != 0:
            self.x_correction = self.controllerX.GenOut(self.xerror)
        if self.yerror != 0:
            self.y_correction = self.controllerY.GenOut(self.yerror)
        print self.xerror,self.yerror, self.x_correction, self.y_correction


    def updateError(self, frame):
        self.frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      
        if len(self.tracks) > 0:
            img0, img1 = self.prev_gray, self.frame_gray
            p0 = np.float32([tr[-1][:2] for tr in self.tracks]).reshape(-1, 1, 2)
            p1, st, err = cv2.calcOpticalFlowPyrLK(img0, img1, p0, None, **self.lk_params)
            p0r, st, err = cv2.calcOpticalFlowPyrLK(img1, img0, p1, None, **self.lk_params)
            d = abs(p0-p0r).reshape(-1, 2).max(-1)
            good = d < 1
            new_tracks = []

            self.xerror = 0.0
            self.yerror = 0.0
            self.n = 0.0

            current_time = time.time()
            for tr, (x, y), good_flag in zip(self.tracks, p1.reshape(-1, 2), good):
                if not good_flag:
                    continue
                tr.append((x, y, current_time))
                if len(tr) > self.track_len:
                    del tr[0]
                new_tracks.append(tr)

                if(len(tr)>2):
                    t = np.float32([v[2] for v in tr])
                    x = np.float32([v[0] for v in tr])
                    y = np.float32([v[1] for v in tr])


                    self.xerror = self.xerror + (x[-1] - x[0])
                    self.yerror = self.yerror + (y[-1] - y[0])
                    self.n = self.n + 1.0

            if self.n>0:
                self.xerror = self.xerror / float(self.n)
                self.yerror = self.yerror / float(self.n)

            self.tracks = new_tracks

              
          

        if self.xerror==0 and self.yerror==0:
              current_time = time.time()
              mask = np.zeros_like(self.frame_gray)
              mask[:] = 255
              p = cv2.goodFeaturesToTrack(self.frame_gray, mask = mask, **self.feature_params)
              if p is not None:
                  for x, y in np.float32(p).reshape(-1, 2):
                      self.tracks.append([(x, y, current_time)])


        self.prev_gray = self.frame_gray


    def updatePiScope(self,frame):
        self.updateError(frame)
        self.updateCorrection()
        self.piscopeController.setCorrection(self.x_correction, self.y_correction)        

                
    def run(self):
        while True:
            try:
                frame = self.queue.get()
                self.updatePiScope(frame)
                self.status = self.queue.qsize()
            except:
                print("ERROR in ProcessTracking")
