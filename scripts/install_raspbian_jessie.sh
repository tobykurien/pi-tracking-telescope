#!/bin/sh

sudo apt-get update
sudo apt-get upgrade
sudo rpi-update

# install needed python libraries
sudo apt-get install libopencv-dev python-opencv python-yaml

# enable opengl on rpi
sudo apt-get install libgl1-mesa-dri

echo "Done, but reboot is required."

