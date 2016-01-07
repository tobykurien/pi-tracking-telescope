import cv2
from threading import Thread
from Queue import Queue

class ProcessFocus(Thread):
    """Work out a focus value for a given frame"""
    
    def __init__(self):
        Thread.__init__(self)
        self.queue = Queue()
        self.focus = -1
        self.setDaemon(True) # terminate on exit

    def variance_of_laplacian(self, image):
        # compute the Laplacian of the image and then return the focus
        # measure, which is simply the variance of the Laplacian
        return cv2.Laplacian(image, cv2.CV_64F).var()
        
    def run(self):
        frame = None
        while True:
            try:
                frame = self.queue.get()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                self.focus = self.variance_of_laplacian(gray)
            except:
                print("ERROR in ProcessFocus")