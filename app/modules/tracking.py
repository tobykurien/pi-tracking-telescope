import cv2
from threading import Thread
from Queue import Queue

class ProcessTracking(Thread):
    """Stacks multiple frames for long-exposure and de-noising"""
    
    def __init__(self):
        Thread.__init__(self)
        self.queue = Queue()
        self.setDaemon(True) # terminate on exit
        #self.outputFrame = None

    def addFrame(self, image):
        if self.queue.qsize() < 10:
            self.queue.put(image)
                
    def run(self):
        alpha = 0.1    # weight of the new frame 
        beta = 1        # weight of the current frame
        gamma = 0       # scalar added to each sum

        while True:
            try:
                frame = self.queue.get()
                if self.outputFrame is None:
                    self.outputFrame = frame
                else:
                    # accumulate the differences
                    cv2.addWeighted(self.outputFrame, beta, frame, 
                                    alpha, gamma, self.outputFrame) 
            except:
                print("ERROR in ProcessStacking")
