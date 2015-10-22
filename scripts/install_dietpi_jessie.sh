#!/bin/sh
# Install PiScope on DietPi (Jessie) for a lightweight installation (under 1Gb)

# install basic xserver stuff
apt-get install xinit xterm

# install fluxbox for a basic "desktop", only ~2Mb
apt-get install fluxbox

# install the rest of the needed dependencies
./install_raspbian_jessie.sh

