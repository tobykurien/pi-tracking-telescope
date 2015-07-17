#!/bin/sh

ip addr show dev eth0
echo Connect to rtsp://ipaddress:8554/
raspivid -o - -t 0 -n -w 1024 -h 768 -fps 15 | cvlc stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554/}' :demux=h264
