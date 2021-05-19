# /usr/bin/python3
import argparse

PAYLOAD_SIZE = 16
CHARACTER_DEVICE = "/dev/acer-gkbbl-0"

parser = argparse.ArgumentParser(description="""Interacts with experimental Acer-wmi kernel module.
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

Some sample commands:

Breath effect with Purple color(speed=4, brightness=100):
python3 facer_rgb.py -m 1 -s 4 -b 100 -cR 255 -cG 0 -cB 255

Neon effect(speed=3, brightness=100):
python3 facer_rgb.py -m 2 -s 3 -b 100

Wave effect(speed=5, brightness=100):
python3 facer_rgb.py -m 3 -s 5 -b 100

Shifting effect with Blue color (speed=5, brightness=100):
python3 facer_rgb.py -m 4 -s 5 -b 100 -cR 0 -cB 255 -cG 0

Zoom effect with Green color (speed=7, brightness=100):
python3 facer_rgb.py -m 5 -s 7 -b 100 -cR 0 -cB 0 -cG 255

Static waving (speed=0):
python3 facer_rgb.py -m 3 -s 0 -b 100
""", formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('-m',
                    type=int,
                    dest='mode',
                    default=3)

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

payload = [0] * 16

args = parser.parse_args()

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

