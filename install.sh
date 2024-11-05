#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "[*] This script must be run as root"
   exit 1
fi

if [[ -f "/sys/bus/wmi/devices/7A4DDFE7-5B5D-40B4-8595-4408E0CC7F56/" ]]; then
    echo "[*] Sorry but your device doesn't have the required WMI module"
    exit 1
fi

if [ ! "$(uname -r | grep lts)" == "" ]; then
    echo LTS kernel detected
    MAKEFLAGS="LTS=1"
fi
# Remove previous chr devices if any exists
rm /dev/acer-gkbbl-0 /dev/acer-gkbbl-static-0 -f

# compile the kernel module
make $MAKEFLAGS

# remove previous acer_wmi module
rmmod acer_wmi

# install required modules
modprobe wmi
modprobe sparse-keymap
modprobe video

# install facer module
insmod src/facer.ko
dmesg | tail -n 10
echo "[*] Done"