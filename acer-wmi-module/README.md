# Gui for [acer keyboard rgb and turbo](https://github.com/JafarAkhondali/acer-predator-turbo-and-rgb-keyboard-linux-module)
![](flutter_app.png)
Inspired by https://github.com/hackbnw/faustus, this project extends current acer-wmi linux kernel module to support Acer gaming functions

Turbo mode should support Acer Helios Predator and Acer Triton Predator series. 
RGB Keyboard is only tested on Acer (Predator, Helios, Nitro) 300 series ( 4-zone RGB ). 

Experimental unofficial Linux platform driver module for Acer Predator Gaming series laptops.
## WARNING: Use at your own risk. This driver interacts with low-level WMI methods which haven't been tested on all series.  

**Will this work on my laptop?**

Compablity table:


| Product name  | Turbo Mode (Implemented)| Turbo Mode (Tested)| RGB (Impelmented)| RGB (Tested)|
| ------------- |:-----------------------:|:------------------:|:-----------------:|:------------:|
| AN515-45  |   -                   |   -               | Yes               |Yes           |
| AN515-55  |   -                   |   -               | Yes               |Yes           |
| AN517-41  |   -                   |   -               | Yes               |Yes           |
| PH315-52 |   Yes                   |   Yes               | Yes               |Yes           |
| PH315-53 |   Yes                   |   Yes               | Yes               |Yes           |
| PH317-53 |   Yes                   |   Yes               | Yes               |Yes           |
| PH317-54 |   Yes                   |   No               | Yes               |No           |
| PH517-51 |   Yes                   |   No               | Yes               |No           |
| PH517-52 |   Yes                   |   No               | Yes               |No           |
| PH517-61 |   Yes                   |   No               | Yes               |No           |
| PH717-71 |   Yes                   |   No               | Yes               |No           |
| PH717-72 |   Yes                   |   No               | Yes               |No           |
| PT314-51 |   No                   |   No               | Yes               |Yes           |
| PT315-51 |   Yes                   |   Yes               | Yes               |Yes           |
| PT315-52 |   Yes                   |   No               | Yes               |No           |
| PT515-51 |   Yes                   |   No               | Yes               |No           |
| PT515-52 |   Yes                   |   No               | Yes               |No           |
| PT917-71 |   Yes                   |   No               | Yes               |No           |




Obviously, I don't have access to all these models, so if it worked(or not) for you, kindly please mention your model on issues so we can ship this to Linux kernel.

You can find your model using this command:
`sudo dmidecode -s system-product-name`
___
#### RGB Keyboard:
I think dynamic RGB effects should work only on 4zone RGB keyboards like 300 series but haven't tested other models.

Check the output of this command:  
`# file /sys/bus/wmi/devices/7A4DDFE7-5B5D-40B4-8595-4408E0CC7F56/`  
If the directory exists, it may work fine. Otherwise, RGB will not work at all.

## Requirements
Secure boot must be disabled.  
Install linux headers using your distro package manager:
Ubuntu (or other Debian baseds distros):  
`sudo apt-get install linux-headers-$(uname -r)`

Arch (I don't use arch anymore btw):  
`sudo pacman -S linux-headers`

## Buid gui backend
I wrote a custom backend for changing the keyboard mode in rust with a websocket backend for the gui
this needs [cargo](https://doc.rust-lang.org/cargo/getting-started/installation.html) installed
You also need to edit src/main.rs at line 34 and set the 127, 0, 0, 1 to your pc's local ip address
```bash
git clone https://github.com/axtloss/acer-predator-rgb-keyboard-gui
cd acer-predator-rgb-keyboard-gui/keybrgbCtrl/
make release
make install
```

## Build phone gui
make sure you have [flutter](https://flutter.dev/) installed and running (flutter doctor doesnt show errors for android)
here you need to edit lib/main.dart at line 26 and change the 127.0.0.1 to the ip you set in the rust file (ill automate this as soon as i can)
```bash
git clone https://github.com/axtloss/acer-predator-rgb-keyboard-gui
cd acer-predator-rgb-keyboard-gui/nitro_keybrgb/
flutter build apk
adb install build/app/outputs/flutter-apk/app-release.apk # make sure your android device is connected via adb
```

## Desktop gui
the desktop gui can be found in nitro_keybrgb_pc/ but it's not finished yet as I currently have no way of building for linux (nixos issue :P)


## Install Kernel module one time (Module won't work after reboot)
```bash
git clone https://github.com/JafarAkhondali/acer-predator-turbo-and-rgb-keyboard-linux-module
cd "acer-predator-turbo-and-rgb-keyboard-linux-module"
chmod +x ./install.sh
sudo ./install.sh
```



## Install Kernel module as a service (Will work after reboot)
```bash
git clone https://github.com/JafarAkhondali/acer-predator-turbo-and-rgb-keyboard-linux-module
cd "acer-predator-turbo-and-rgb-keyboard-linux-module"
chmod +x ./*.sh
sudo ./install_service.sh
```



## Usage
Turbo mode should work fine by using the turbo button on keyboard.

For RGB, the module will mount a new character device at `/dev/acer-gkbbl-0` to communicate
with kernel space.  
The python script in upstream has been replaced with the keybrgbCtrl rust project
**Note that this has only been tested on the acer nitro 5 AN515-55**
```
Control your keyboard backlight

USAGE:
    keybrgbctl [FLAGS] [OPTIONS]

FLAGS:
    -h, --help         Prints help information
    -V, --version      Prints version information
    -ws, --websocket    Start websocket server

OPTIONS:
    -b, --brightness <BRIGHTNESS>    Set the brightness of the keyboard
    -c, --color <COLOR>              Set the color of the keyboard
    -d, --direction <DIRECTION>      Set the direction of the keyboard [possible values: left, right]
    -m, --mode <MODE>                Set the mode of the keyboard [possible values: static, breath, neon, wave,
                                     shifting, zoom]
    -s, --speed <SPEED>              Set the speed of the keyboard
```
some examples for the usage:
```bash
keybrgbctl -ws # This starts the websocket used by the flutter app

# Static colouring 
#NOTE: different zones seem to be broken,
#so I didn't implement that feature here, zones wont be supported I used a workaround to get the whole keyboard one static colour
keybrgbctl -m static -b 100 -c ff00ff

# breathe with colour purple at speed 5
keybrgbctl -m breathe -b 100 -c ff00ff -s 5

# wave at speed 4 direction left
keybrgbctl -m wave -b 100 -d left

# neon at speed 8
keybrgbctl -m neon -b 100 -s 8

# shifting at speed 3 with colour purple direction right
keybrgbctl -m shifting -b 100 -s 3 -d right

# zoom with colour purple speed 9
keybrgbctl -m zoom -b 100 -s 9 
```

## Known problems
If installation failed, check this [issue](https://github.com/JafarAkhondali/acer-predator-turbo-and-rgb-keyboard-linux-module/issues/4#issuecomment-905486393)
If something didn't look right, do a reboot (or boot to windows) and play a little with some Predator Sense app to reset ACPI registers. 

## Uninstall:
Simply run `./uninstall.sh` and (hopefully) everything should be back to normal.  
If you have installed it as a service, simply run `./uninstal_service.sh`

## Feedback:
If this worked or didn't worked for you, kindly make a new issue, and attach the following if possible:  
`sudo dmidecode | grep "Product Name" -B 2 -A 4`  
`sudo cat /sys/firmware/acpi/tables/DSDT > dsdt.aml`

## Donation:
I do not take donations, but if you want to donate, donate to the original author of this kernel module, without his development I wouldnt've made this: https://github.com/JafarAkhondali/acer-predator-turbo-and-rgb-keyboard-linux-module#donation


## Contributing
**Are you a developer?**

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request

## Roadmap:
- [x] Send patch to kernel mainline (currently only turbo mode for 315-53 is implemented)  
- [x] Implement Turbo mode  
- [x] Implement RGB Dynamic effects (4-zone)  
- [x] Implement RGB Static coloring (4-zone)
- [x] Install as a system service (Thanks to [Kapitoha](https://github.com/Kapitoha))
- [X] GUI
- [ ] Custom Fans speed
- [ ] Implement RGB Dynamic effects (per key RGB)  
- [ ] Implement RGB Static coloring (per key RGB)  


## License
GNU General Public License v3 <br>
The code in keybrgbCtl/src/hexrgb.rs has been modified from https://github.com/shrirambalaji/cli-hex-rgb and falls under the MIT license

