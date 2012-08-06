#!/bin/sh
##
## Script for setting up OpenNao for wlantest
##
## Author(s):
##  - Maxence VIALLON <mviallon@aldebaran-robotics.com>
##

IP_LOCAL=192.168.2.4
IP_AP=192.168.3.1

# /dev/random doesn't provide enough random and /dev/urandom is a secured enough RNG
rm /dev/random
ln -s /dev/urandom /dev/random

#Loading virtual interfaces
modprobe mac80211_hwsim

#Setting up ip parameters
ifconfig eth0 $IP_LOCAL
ifconfig wlan1 $IP_AP

#Starting dhcpd
dhcpd
