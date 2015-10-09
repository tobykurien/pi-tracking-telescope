#!/usr/bin/env python
import os
import time
import subprocess
 
# Full list of Exposure and White Balance options
#list_ex  = ['off','auto','night','nightpreview','backlight',
#            'spotlight','sports','snow','beach','verylong',
#            'fixedfps','antishake','fireworks']
#list_awb = ['off','auto','sun','cloud','shade','tungsten',
#            'fluorescent','incandescent','flash','horizon']
 
# Refined list of Exposure and White Balance options. 50 photos.
#list_ex  = ['off','auto','night','backlight','fireworks']
#list_awb = ['off','auto','sun','cloud','shade','tungsten',
#            'fluorescent','incandescent','flash','horizon']
 
# Test list of Exposure and White Balance options. 6 photos.
list_ex  = ['auto','night']
list_awb = ['auto','fluorescent']
 
# EV level
photo_ev = 0
 
# Photo dimensions and rotation
photo_width  = 1680
photo_height = 1050
photo_rotate = 0
 
photo_interval = 0 # Interval between photos (seconds)
photo_counter  = 0    # Photo counter
 
total_photos = len(list_ex) * len(list_awb)
 
# Delete all previous image files
try:
  os.remove("photo_*.jpg")
except OSError:
  pass
 
# Lets start taking photos!
try:
 
  print "Starting photo sequence"
 
  for ex in list_ex:
    for awb in list_awb:
      photo_counter = photo_counter + 1
      filename = 'photo_' + ex + '_' + awb + '.jpg'
      cmd = 'raspistill -o ' + filename + ' -t 1000 -ex ' + ex + ' -awb ' + awb + ' -ev ' + str(photo_ev) + ' -w ' + str(photo_width) + ' -h ' + str(photo_height) + ' -rot ' + str(photo_rotate)
      pid = subprocess.call(cmd, shell=True)
      print ' [' + str(photo_counter) + ' of ' + str(total_photos) + '] ' + filename
      time.sleep(photo_interval)
 
  print "Finished photo sequence"
 
except KeyboardInterrupt:
  # User quit
  print "\nGoodbye!"

