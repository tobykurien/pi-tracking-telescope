#!/bin/sh
# Install PiScope on DietPi (Jessie) for a lightweight installation (under 1Gb)

# install basic xserver stuff
sudo apt-get -y install xinit xterm

# install the rest of the needed dependencies
./install_raspbian_jessie.sh

