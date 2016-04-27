import cv2
from threading import Thread
from Queue import Queue

class ProcessTracking(Thread):
    """Stacks multiple frames for long-exposure and de-noising"""
    
    def __init__(self):
        Thread.__init__(self)
        self.queue = Queue()
        self.setDaemon(True) # terminate on exit
        self.status = "Initial"
        #self.outputFrame = None

    def getStatus(self):
        return self.status
        
    def addFrame(self, image):
        if self.queue.qsize() < 10:
            self.queue.put(image)
                
    def run(self):
        while True:
            try:
                frame = self.queue.get()
                self.status = self.queue.qsize()
            except:
                print("ERROR in ProcessTracking")
