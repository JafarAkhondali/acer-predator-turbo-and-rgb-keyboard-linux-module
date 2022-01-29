#!/bin/bash
rmmod facer
make
insmod src/facer.ko
dmesg | tail -n 30
