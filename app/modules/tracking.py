import cv2
import numpy as np
import time
from threading import Thread
from Queue import Queue
import pid
from threading import Thread, Lock
import traceback




class ProcessTracking(Thread):
    """PID controller for visual tracking with opencv """    

    def __init__(self, piscopeController):
        Thread.__init__(self)
        self.mutex = Lock()

        self.piscopeController = piscopeController
        self.setDaemon(True) # terminate on exit
        self.status = "Initial"
        self.reset()

        self.lk_params = dict( winSize  = (15, 15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

        self.feature_params = dict( maxCorners = 5,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )




    def getStatus(self):
        return self.status
        
    def addFrame(self, image):
        if self.queue.qsize() < 1:
            self.queue.put(image)

    def updateCorrection(self):
        self.x_correction = 0
        self.y_correction = 0
        if self.xerror != 0:
            self.x_correction = self.controllerX.GenOut(-self.xerror)
        if self.yerror != 0:
            self.y_correction = self.controllerY.GenOut(-self.yerror)
        print self.x_correction,self.y_correction #, self.x_correction, self.y_correction


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
                if len(tr) >  500:
                    del tr[0]
                new_tracks.append(tr)

                if(len(tr)>=2):
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
        self.mutex.acquire()
        try:
            self.frame = frame
        finally:
            self.mutex.release()
        
        
        rows,cols = frame.shape[:2]        
        #M = cv2.getRotationMatrix2D((cols/2,rows/2),45,1)
        #rotated_frame = cv2.warpAffine(frame,M,(cols,rows))
        #self.updateError(rotated_frame)
        self.updateError(frame)
        self.updateCorrection()
        #print self.x_correction, self.y_correction
        if time.time() - self.last_command > 2:
            self.piscopeController.setAlt(self.y_correction)        
            self.piscopeController.setAzimuth(self.x_correction)
            self.last_command = time.time()
                

    def reset(self):
        self.xerror = 0
        self.yerror = 0

        self.controllerX = pid.PID()
        self.controllerY = pid.PID()

        self.controllerX.SetKp(25.0)
        self.controllerX.SetKi(0.0)
        self.controllerY.SetKp(25.0)
        self.controllerY.SetKi(0.0)

        self.x_correction = 0
        self.y_correction = 0

        self.prev_gray = None
        self.tracks = []
        self.draw_trails = True

        self.xerror = 0
        self.yerror = 0
              
        self.last_command = 0        
        self.frame = None
        self.queue = Queue(maxsize=1)
        

                
    def run(self):
        framecount = 0
        while True:
            try:
                frame = self.queue.get()
                if frame != None:
                    self.updatePiScope(frame)
                    framecount = 0
                framecount += 1
                self.status = framecount
            except Exception as e:
                print("ERROR in ProcessTracking:"+str(e))
                tb = traceback.format_exc()
                print(tb)


    def getFrame(self):
        if self.frame==None:
            return None
        self.mutex.acquire()
        try:
            vis_frame = self.frame.copy()
        finally:
            self.mutex.release()

        rows,cols = vis_frame.shape[:2]        
        #M = cv2.getRotationMatrix2D((cols/2,rows/2),45,1)
        #vis_frame = cv2.warpAffine(vis_frame,M,(cols,rows))

        #draw_str(vis_frame, (20, 20), 'track count: %d' % len(tracker.tracks))
        if self.draw_trails:
            cv2.polylines(vis_frame, [np.int32(tr) for tr in [[t[:2] for t in tr]  for tr in self.tracks]], False, (0, 255, 0))

        for tr in self.tracks:
            cv2.circle(vis_frame, (tr[-1][0], tr[-1][1]), 2, (0, 255, 0), -1)

        return vis_frame
