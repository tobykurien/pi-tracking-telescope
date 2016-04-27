import cv2
import time
import io
import yuv2rgb
import pygame

class Camera:
    '''
    Camera module to abstract between the Raspberry Pi camera or a standard
    USB camera. Useful for testing and debugging
    '''
    
    def __init__(self, rpiCam=False, cameraNum=0, width=640, height=480, fps=30):
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
	camera.crop = (0.0, 0.0, 1.0, 1.0)
        self.camera = camera
        self.rawCapture = PiRGBArray(camera, size=(self.width, self.height))
        self.rgb = bytearray(self.width * self.height * 3)
        self.yuv = bytearray(self.width * self.height * 3 / 2)
        
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
            stream = io.BytesIO()
            self.camera.capture(stream, use_video_port=True, format='raw')
	    stream.seek(0)
	    stream.readinto(self.yuv)
            stream.close()
            yuv2rgb.convert(self.yuv, self.rgb, self.width, self.height)
            #image = self.rawCapture.array
            #self.rawCapture.truncate(0)
            return pygame.image.frombuffer(self.rgb[0:(self.width*self.height*3)], (self.width, self.height), 'RGB')
        else:
            _, image = self.rawCapture.read()
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
                    self.rawCapture.truncate(0)
                except:
                    break
                finally:
                    self.cleanup()
        else:
            while True:
                try:
                    yield self.grabFrame()
                except:
                    break
                finally:
                    self.cleanup()
                    
    def cleanup(self):
        if self.rpiCam:
            self.camera.close()
        else:
            self.rawCapture.release()
    
    def startPreview(self):
	if self.rpiCam:
	   self.camera.start_preview()
