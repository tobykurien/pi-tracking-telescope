import sys
sys.path.append('/home/pi/scopex/pi-tracking-telescope/app/control')

import serial
import time
import os
import subprocess
import threading
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
import video
from common import anorm2, draw_str
from time import clock


 
def _find_getch():
    try:
        import termios
    except ImportError:
        # Non-POSIX. Return msvcrt's (Windows') getch.
        import msvcrt
        return msvcrt.getch

    # POSIX system. Create and return a getch that manipulates the tty.
    import sys, tty
    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    return _getch

def read_from_port(ser):
        while True:
           reading = ser.readline().decode()
           if reading !="": sys.stdout.write(reading)

'''def showVideo():
    camera.capture(rawCapture, format="bgr")
    image = rawCapture.array
    cv2.imshow('SCOPEX', image)
    rawCapture.truncate(0) 
'''


def takePicture(ex='night',awb='auto',photo_ev=0, photo_width=1680, photo_height=1050, photo_rotate=0):
  filename = 'photo_%.3f' + ex + '_' + awb + '.jpg'
  filename = filename % time.time()
  
  cmd = 'raspistill -o ' + filename + ' -t 1000 -ex ' + ex + ' -awb ' + awb + ' -ev ' + str(photo_ev) + ' -w ' + str(photo_width) + ' -h ' + str(photo_height) + ' -rot ' + str(photo_rotate)
  pid = subprocess.call(cmd, shell=True)


def takePictureOpenCV(ex='night',awb='auto',photo_ev=0, photo_width=2592, photo_height=1944, photo_rotate=0):
    global camera
    global rawCapture
    camera.resolution = (photo_width, photo_height)
    camera.framerate = 32
    time.sleep(2)
    camera.start_preview()
    # Camera warm-up time
    time.sleep(2)
    filename = 'photo_%.3f' + ex + '_' + awb + '.jpg'
    filename = filename % time.time()

    camera.capture(filename) 
    camera.stop_preview() 



getch = _find_getch()
found = False
i = 0
while not found:
    try:
       ser = serial.Serial("/dev/ttyACM%s" % i, baudrate=9600, timeout=0.15)
       found = True
    except:
       i+=1 
       if(i>10): i=0
       time.sleep(0.1)

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)
do_showVideo = False
cv2.namedWindow("SCOPEX")
print "Ready!"
while True:
    #c = getch()
    key = cv2.waitKey(30) & 0xFF 
    if key != 255:
        c = chr(key)
        if c=='q' or c=='Q':
           sys.exit(0)
        elif c=='p' or c=='P':
           takePictureOpenCV()
        elif c=='v' or c=='V':
           do_showVideo = not do_showVideo
           if do_showVideo: camera.start_preview()
           else: camera.stop_preview()
        else:
           ser.write(c)
    
