#!/bin/sh
sudo apt-get update
#sudo apt-get upgrade
#sudo rpi-update

# install needed python libraries
sudo apt-get -y install libopencv-dev python-opencv python-yaml python-picamera

# enable opengl on rpi
sudo apt-get -y install libgl1-mesa-dri

echo "Done, but reboot is required."

