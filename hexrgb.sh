#!/usr/bin/env bash
hex="$1"
cR=$(printf "%d %d %d\n" 0x${hex:0:2} 0x${hex:2:2} 0x${hex:4:2} | awk 'BEGIN { FS = " " }; { print $1 }')
cG=$(printf "%d %d %d\n" 0x${hex:0:2} 0x${hex:2:2} 0x${hex:4:2} | awk 'BEGIN { FS = " " }; {print $2 }')
cB=$(printf "%d %d %d\n" 0x${hex:0:2} 0x${hex:2:2} 0x${hex:4:2} | awk 'BEGIN { FS = " " }; {print $3 }')

python3 /home/amy/rgbKbr/facer_rgb.py -m 4 -s 1 -b 50 -cR $cR -cG $cG -cB $cB
sleep 2.14
python3 /home/amy/rgbKbr/facer_rgb.py -m 4 -s 0 -b 50 -cR $cR -cG $cG -cB $cB
