import cv2
import time

class Camera:
    '''
    Camera module to abstract between the Raspberry Pi camera or a standard
    USB camera. Useful for testing and debugging
    '''
    
    def __init__(self, rpiCam=False, cameraNum=0, width=640, height=480, fps=32):
        self.rpiCam = rpiCam
        self.width = width
        self.height = height
        self.fps = fps
        self.cameraNum = cameraNum
        
        if self.rpiCam:
            self.setupRpiCam()
        else:
            self.setupUsbCam()
        
    def setupRpiCam(self):
        # import the necessary packages
        from picamera.array import PiRGBArray
        from picamera import PiCamera
        
        # initialize the camera and grab a reference to the raw camera capture
        camera = PiCamera()
        camera.resolution = (self.width, self.height)
        camera.framerate = self.fps
        self.camera = camera
        self.rawCapture = PiRGBArray(camera, size=(self.width, self.height))
        
        # wait for camera to warm up
        time.sleep(0.1)

    def setupUsbCam(self):
        # initialize the camera and grab a reference to the raw camera capture
        self.rawCapture = cv2.VideoCapture(self.cameraNum)

        # wait for camera to warm up
        time.sleep(0.1)

    def grabFrame(self):
        '''
        Grab a single frame from the camera
        '''
        
        if self.rpiCam:
            self.camera.capture(self.rawCapture, format="bgr")
            image = self.rawCapture.array
            return image
        else:
            ret, image = self.rawCapture.read()
            return image
        
    def streamFrames(self):
        '''
        Generator to stream images from the camera as numpy arrays. The pixels
        are stored as BGR (blue, green, red)
        '''
        
        if self.rpiCam:
            # capture frames from the camera
            for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
                try:
                    yield frame.array
                except:
                    break
                finally:
                    self.rawCapture.truncate(0)
        else:
            while True:
                try:
                    yield self.grabFrame()
                except:
                    break
                finally:
                    self.rawCapture.release()
