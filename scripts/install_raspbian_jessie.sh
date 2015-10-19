#!/bin/sh

sudo apt-get update
sudo apt-get upgrade
sudo rpi-update

sudo apt-get install libopencv-dev python-opencv libgl1-mesa-dri

echo "Done, but reboot is required."
