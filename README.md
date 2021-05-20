# Acer Predator Helios 300 RGB backlight keyboard linux kernel module
Inspired by https://github.com/hackbnw/faustus, this projects extends current acer-wmi linux kernel module to support acer gaming functions


Experimental unofficial Linux platform driver module for Acer Predator Helios Gaming series laptops.
# WARNING: Use at your own risk. This driver interacts with low-level WMI methods which hasn't been tested on all series.  

---
**Does this works on my laptop?**  
Check the output of this command:  
`# file /sys/bus/wmi/devices/7A4DDFE7-5B5D-40B4-8595-4408E0CC7F56/`  
If the directory exists, it should work fine. Otherwise please don't try to install the module as it won't work.

## Install
Make sure secure boot is disabled, then:  
```bash
git clone https://github.com/JafarAkhondali/acer-helios-300-rgb-keyboard-linux-module
cd "acer-helios-300-rgb-keyboard-linux-module"
chmod +x ./install.sh
./install.sh
```

## Usage
The module will mount a new character device at `/dev/acer-gkbbl-0`.  
To make it easier to interact with this device, a simple python has been attached.  
`python3 facer_rgb.py`  
or check help for more advanced usage:  
`python3 facer_rgb.py --help`

```
-m [mode index]
Animation effect modes:

    1 -> Breath [Accepts RGB color]
    2 -> Neon
    3 -> Wave
    4 -> Shifting [Accepts RGB color]
    5 -> Zoom [Accepts RGB color]

-s [speed]
Animation Speed:

    0 -> No animation speed (static)
    1 -> Slowest animation speed
    9 -> Fastest animation speed
    
    You can use values between 1-9 to adjust the speed, or increase speed even more than 255, but keep in mind
    that values higher than 9 were not used in official PredatorSense application.

-b [brightness]
Keyboard backlight Brightness:

    0   -> No backlight (turned off)
    100 -> Maximum backlight brightness

-d [direction]
Animation direction:

    1   -> Right to Left
    2   -> Left to Right

-cR [red value]
Some modes require specific [R]GB color

    0   -> Minimum red range
    255 -> Maximum red range

-cG [green value]
Some modes require specific R[G]B color

    0   -> Minimum green range
    255 -> Maximum green range

-cB [blue value]
Some modes require specific RG[B] color

    0   -> Minimum blue range
    255 -> Maximum blue range
```
Sample usages:

Breath effect with Purple color(speed=4, brightness=100):  
`python3 facer_rgb.py -m 1 -s 4 -b 100 -cR 255 -cG 0 -cB 255`

Neon effect(speed=3, brightness=100):  
`python3 facer_rgb.py -m 2 -s 3 -b 100`

Wave effect(speed=5, brightness=100):  
`python3 facer_rgb.py -m 3 -s 5 -b 100`

Shifting effect with Blue color (speed=5, brightness=100):  
`python3 facer_rgb.py -m 4 -s 5 -b 100 -cR 0 -cB 255 -cG 0`

Zoom effect with Green color (speed=7, brightness=100):  
`python3 facer_rgb.py -m 5 -s 7 -b 100 -cR 0 -cB 0 -cG 255`

Static waving (speed=0):
`python3 facer_rgb.py -m 3 -s 0 -b 100`



## Uninstall:
Simply run `./uninstall.sh` and (hopefully) everything should be back to normal.

## Feedback:
If this worked, or didn't worked for you, kindly make a new issue, and attach the following if possible:  
`sudo dmidecode | grep "Product Name" -B 2 -A 4`  
`sudo cat /sys/firmware/acpi/tables/DSDT > dsdt.aml`

