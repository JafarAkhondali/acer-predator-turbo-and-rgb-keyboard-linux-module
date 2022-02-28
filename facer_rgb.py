#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

PAYLOAD_SIZE = 16
CHARACTER_DEVICE = "/dev/acer-gkbbl-0"

PAYLOAD_SIZE_STATIC_MODE = 4
CHARACTER_DEVICE_STATIC = "/dev/acer-gkbbl-static-0"

CONFIG_DIRECTORY = str(Path.home()) + "/.config/predator/saved profiles"
path = Path(CONFIG_DIRECTORY)
path.mkdir(parents=True, exist_ok=True)

parser = argparse.ArgumentParser(description=f"""Interacts with experimental Acer-wmi kernel module.
-m [mode index]
    Effect modes:
    0 -> Static [Accepts ZoneID[1,2,3,4] + RGB Color]
    1 -> Breath [Accepts RGB color]
    2 -> Neon
    3 -> Wave
    4 -> Shifting [Accepts RGB color]
    5 -> Zoom [Accepts RGB color]

-z [ZoneID]
    Zone ID(Only in static mode):
    Possible values: 1,2,3,4

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

-save [profile name]
    Add as last argument to save to a profile

-load [profile name]
    Loads the profile if it exists

-list
    Lists all the saved profiles in config directory
    config directory is '{CONFIG_DIRECTORY}'

Some sample commands:

Breath effect with Purple color(speed=4, brightness=100):
./facer_rgb.py -m 1 -s 4 -b 100 -cR 255 -cG 0 -cB 255

Neon effect(speed=3, brightness=100):
./facer_rgb.py -m 2 -s 3 -b 100

Wave effect(speed=5, brightness=100):
./facer_rgb.py -m 3 -s 5 -b 100

Shifting effect with Blue color (speed=5, brightness=100):
./facer_rgb.py -m 4 -s 5 -b 100 -cR 0 -cB 255 -cG 0

Zoom effect with Green color (speed=7, brightness=100):
./facer_rgb.py -m 5 -s 7 -b 100 -cR 0 -cB 0 -cG 255 -save zoom

Static waving (speed=0) and save it as example:
./facer_rgb.py -m 3 -s 0 -b 100 -save example

Load the previously saved profile:
./facer_rgb.py -load example
""", formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('-m',
                    type=int,
                    dest='mode',
                    default=3)

parser.add_argument('-z',
                    type=int,
                    dest='zone',
                    default=1)

parser.add_argument('-s',
                    type=int,
                    dest='speed',
                    default=4)

parser.add_argument('-b',
                    type=int,
                    dest='brightness',
                    default=100)

parser.add_argument('-d',
                    type=int,
                    dest='direction',
                    default=1)

parser.add_argument('-cR',
                    type=int,
                    dest='red',
                    default=50)

parser.add_argument('-cG',
                    type=int,
                    dest='green',
                    default=255)

parser.add_argument('-cB',
                    type=int,
                    dest='blue',
                    default=50)

parser.add_argument('-save')

parser.add_argument('-load')

parser.add_argument('-list',
                    action='store_true')

args = parser.parse_args()

if args.list:
    print("Saved profiles:")
    for filepath in list(path.glob('*.*')): print(f"\t{filepath.stem}")
    exit()

if args.load:
    with open(f"{CONFIG_DIRECTORY}/{args.load}.json", 'rt') as f:
        t_args = argparse.Namespace()
        t_args.__dict__.update(json.load(f))
        args = parser.parse_args(namespace=t_args)

if args.save:
    with open(f"{CONFIG_DIRECTORY}/{args.save}.json", 'wt') as f:
        vars(args).pop('save')
        vars(args).pop('load')
        json.dump(vars(args), f, indent=4)

if args.mode == 0:
    # Static coloring mode
    payload = [0] * PAYLOAD_SIZE_STATIC_MODE
    if args.zone < 1 or args.zone > 8:
        print("Invalid Zone ID entered! Possible values are: 1, 2, 3, 4 from left to right")
    payload[0] = 1 << (args.zone - 1)
    payload[1] = args.red
    payload[2] = args.green
    payload[3] = args.blue
    with open(CHARACTER_DEVICE_STATIC, 'wb') as cd:
        cd.write(bytes(payload))

    # Tell WMI To use STATIC coloring
    # Dynamic coloring mode
    payload = [0] * PAYLOAD_SIZE
    payload[2] = args.brightness
    with open(CHARACTER_DEVICE, 'wb') as cd:
        cd.write(bytes(payload))



else:
    # Dynamic coloring mode
    payload = [0] * PAYLOAD_SIZE
    payload[0] = args.mode
    payload[1] = args.speed
    payload[2] = args.brightness
    payload[3] = 8 if args.mode == 3 else 0
    payload[4] = args.direction
    payload[5] = args.red
    payload[6] = args.green
    payload[7] = args.blue

    with open(CHARACTER_DEVICE, 'wb') as cd:
        cd.write(bytes(payload))
