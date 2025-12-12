# Unofficial Acer Gaming RGB keyboard backlight and Turbo mode Linux kernel module (Acer Predator, Acer Helios, Acer Nitro)
![](keyboard.webp)

[![GitHub repo Good Issues for newbies](https://img.shields.io/github/issues/JafarAkhondali/acer-predator-turbo-and-rgb-keyboard-linux-module/good%20first%20issue?style=flat&logo=github&logoColor=green&label=Good%20First%20issues)](https://github.com/JafarAkhondali/acer-predator-turbo-and-rgb-keyboard-linux-module/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22) [![GitHub Help Wanted issues](https://img.shields.io/github/issues/JafarAkhondali/acer-predator-turbo-and-rgb-keyboard-linux-module/help%20wanted?style=flat&logo=github&logoColor=b545d1&label=%22Help%20Wanted%22%20issues)](https://github.com/JafarAkhondali/acer-predator-turbo-and-rgb-keyboard-linux-module/issues?q=is%3Aopen+is%3Aissue+label%3A%22help+wanted%22) [![GitHub Help Wanted PRs](https://img.shields.io/github/issues-pr/JafarAkhondali/acer-predator-turbo-and-rgb-keyboard-linux-module/help%20wanted?style=flat&logo=github&logoColor=b545d1&label=%22Help%20Wanted%22%20PRs)](https://github.com/JafarAkhondali/acer-predator-turbo-and-rgb-keyboard-linux-module/pulls?q=is%3Aopen+is%3Aissue+label%3A%22help+wanted%22) [![GitHub repo Issues](https://img.shields.io/github/issues/JafarAkhondali/acer-predator-turbo-and-rgb-keyboard-linux-module?style=flat&logo=github&logoColor=red&label=Issues)](https://github.com/JafarAkhondali/acer-predator-turbo-and-rgb-keyboard-linux-module/issues?q=is%3Aopen)   [![](https://dcbadge.vercel.app/api/server/bNa4Qw8rPH)](https://discord.gg/ybWvSRfSY5)
    
Inspired by [faustus(for asus)](https://github.com/hackbnw/faustus), this project extends the current Acer-WMI Linux kernel module to support Acer gaming functions.



> **Warning**
> ## Use at your own risk! Acer was not involved in developing this driver, and everything is developed by reverse engineering the official Predator Sense app. This driver interacts with low-level WMI methods that haven't been tested on all series.  

> **Note**
> # Note to contributors:
> I started to record a miniseries to share my experience in creating this project on [YouTube](https://www.youtube.com/watch?v=97-WNhUmoig&list=PLv2kA4LxAI4Dq2ic_hU9bdvxIzoz5SzBr). This will help you to contribute to this project or similar projects that are using WMI for communication.

**Will this work on my laptop?**

Compatibility table:


| Product name |                                           Turbo Mode (Implemented)                                           |                                             Turbo Mode (Tested)                                             | RGB (Implemented) | RGB (Tested) |
|--------------|:------------------------------------------------------------------------------------------------------------:|:-----------------------------------------------------------------------------------------------------------:|:-----------------:|:------------:|
| AN515-45     |                                                      -                                                       |                                                      -                                                      |        Yes        |     Yes      |
| AN515-55     |                                                      -                                                       |                                                      -                                                      |        Yes        |     Yes      |
| AN515-56     |                                                      -                                                       |                                                      -                                                      |        Yes        |     Yes      |
| AN515-57     |                                                      -                                                       |                                                      -                                                      |        Yes        |     Yes      |
| AN515-58     |                                                      -                                                       |                                                      -                                                      |        Yes        |     Yes      |
| AN517-41     |                                                      -                                                       |                                                      -                                                      |        Yes        |     Yes      |
| PH315-52     |                                                     Yes                                                      |                                                     Yes                                                     |        Yes        |     Yes      |
| PH315-53     |                                                     Yes                                                      |                                                     Yes                                                     |        Yes        |     Yes      |
| PH315-54     |                                                     Yes                                                      |                                                     Yes                                                     |        Yes        |     Yes      |
| PH315-55     |                                                     Yes                                                      |   [Buggy](https://github.com/JafarAkhondali/acer-predator-turbo-and-rgb-keyboard-linux-module/issues/122)   |        Yes        |      No      |
| PH317-53     |                                                     Yes                                                      |                                                     Yes                                                     |        Yes        |     Yes      |
| PH317-54     |                                                     Yes                                                      |                                                     No                                                      |        Yes        |      No      |
| PH517-51     |                                                     Yes                                                      |                                                     No                                                      |        Yes        |      No      |
| PH517-52     |                                                     Yes                                                      |                                                     No                                                      |        Yes        |      No      |
| PH517-61     | [Partial#94](https://github.com/JafarAkhondali/acer-predator-turbo-and-rgb-keyboard-linux-module/issues/94)  | [Partial#94](https://github.com/JafarAkhondali/acer-predator-turbo-and-rgb-keyboard-linux-module/issues/94) |        Yes        |     Yes      |
| PH717-71     |                                                     Yes                                                      |                                                     No                                                      |        Yes        |      No      |
| PH717-72     |                                                     Yes                                                      |                                                     No                                                      |        Yes        |      No      |
| PHN18-71     |                                                     Yes                                                      |                                                     Yes                                                     |        Yes        |     Yes      |
| PT314-51     |                                                      No                                                      |                                                     No                                                      |        Yes        |     Yes      |
| PT315-51     |                                                     Yes                                                      |                                                     Yes                                                     |        Yes        |     Yes      |
| PT314-52s    |                                                     Yes                                                      |                                                     Yes                                                     |        Yes        |      No      |
| PT315-52     |                                                     Yes                                                      |                                                     No                                                      |        Yes        |      No      |
| PT316-51     |                                                     Yes                                                      |                                                     Yes                                                     |        Yes        |     Yes      |
| PT316-51s     |                                                    Yes                                                      |                                                     Yes                                                     |        Yes        |     No       |
| PT515-51     |                                                     Yes                                                      |                                                     Yes                                                     |        Yes        |     Yes      |
| PT515-52     |                                                     Yes                                                      |                                                     No                                                      |        Yes        |      No      |
| PT516-52s    |                                                     Yes                                                      |                                                     No                                                      |        Yes        |     Yes      |
| PT917-71     |                                                     Yes                                                      |                                                     No                                                      |        Yes        |      No      |




Obviously, I don't have access to all these models, so if it worked (or not) for you, kindly please mention your model on issues so we can ship this to Linux kernel.

You can find your model using this command:
`sudo dmidecode -s system-product-name`
___
#### RGB Keyboard:
I think dynamic RGB effects should work only on 4-zone RGB keyboards like 300 series but haven't tested other models.

Check the output of this command:  
`# file /sys/bus/wmi/devices/7A4DDFE7-5B5D-40B4-8595-4408E0CC7F56/`  
If the directory exists, it may work fine. Otherwise, RGB will not work at all.

## Requirements
If you have secure boot enabled, you are not using Ubuntu and installation failed with error `Key was rejected by service`, you can sign the module yourself by following the instructions [here](https://github.com/JafarAkhondali/acer-predator-turbo-and-rgb-keyboard-linux-module/issues/28#issuecomment-1054423776). Make sure you have `rsync` installed. You can check that by doing `rsync --version` in your terminal, and if you don't have it, just install it by doing `sudo apt install rsync`.

Install Linux headers using your distro package manager:
Ubuntu (or other Debian based distros):  
`sudo apt-get install linux-headers-$(uname -r) gcc make`

Arch (I don't use arch anymore btw):  
`sudo pacman -S linux-headers`



## Install one time (Module won't work after reboot)
```bash
git clone https://github.com/JafarAkhondali/acer-predator-turbo-and-rgb-keyboard-linux-module
cd "acer-predator-turbo-and-rgb-keyboard-linux-module"
chmod +x ./*.sh
sudo ./install.sh
```

### Install as a systemd service (Will work after reboot) for Arch Linux from [ExodiaOS Repo](https://github.com/Exodia-OS/exodia-repo/blob/master/x86_64/)

```bash

# Download the latest version of Predator-Sense-CLI available)

sudo pacman -U Predator-Sense-CLI-{version}-any.pkg.tar.zst

```

## Install as a systemd service (Will work after reboot)
```bash
git clone https://github.com/JafarAkhondali/acer-predator-turbo-and-rgb-keyboard-linux-module
cd "acer-predator-turbo-and-rgb-keyboard-linux-module"
chmod +x ./*.sh
sudo ./install_service.sh
```

## Install as an openrc service (Will work after reboot)
```bash
git clone https://github.com/JafarAkhondali/acer-predator-turbo-and-rgb-keyboard-linux-module
cd "acer-predator-turbo-and-rgb-keyboard-linux-module"
chmod +x ./*.sh
sudo ./install_openrc.sh
```

## Usage
Turbo mode should work fine by using the turbo button on the keyboard.

For RGB, the module will mount a new character device at `/dev/acer-gkbbl-0` to communicate with kernel space. 

You can use the `keyboard.py`, which is a simple script that provides an easy-to-understand CLI for setting your keyboard RGB. To run the script, just use the following command 

```bash
python keyboard.py
```

If you want more control, you also have access to the `facer_rgb.py`; this can be useful if you are building your scripts. Instruction for using `facer_rgb.py` is given below, or check the help for more advanced usage:  
`./facer_rgb.py --help`

```
usage: facer_rgb.py [-h] [-m MODE] [-z ZONE] [-s SPEED] [-b BRIGHTNESS] [-d DIRECTION] [-cR RED] [-cG GREEN] [-cB BLUE]

Interacts with experimental Acer-wmi kernel module.
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
    
    You can use values between 1-9 to adjust the speed or increase speed even more than 255, but keep in mind
    that values higher than 9 were not used in the official PredatorSense application.

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
    config directory is "$HOME/.config/predator/saved profiles/"

optional arguments:
  -h, --help     show this help message and exit
  -m MODE
  -z ZONE
  -s SPEED
  -b BRIGHTNESS
  -d DIRECTION
  -cR RED
  -cG GREEN
  -cB BLUE
  -save NAME
  -load NAME
  -list
```
Sample usages:

Breath effect with Purple color(speed=4, brightness=100):  
`./facer_rgb.py -m 1 -s 4 -b 100 -cR 255 -cG 0 -cB 255`

Neon effect(speed=3, brightness=100):  
`./facer_rgb.py -m 2 -s 3 -b 100`

Wave effect(speed=5, brightness=100):  
`./facer_rgb.py -m 3 -s 5 -b 100`

Shifting effect with Blue color (speed=5, brightness=100):  
`./facer_rgb.py -m 4 -s 5 -b 100 -cR 0 -cB 255 -cG 0`

Zoom effect with Green color (speed=7, brightness=100):  
`./facer_rgb.py -m 5 -s 7 -b 100 -cR 0 -cB 0 -cG 255`

Static waving (speed=0):
`./facer_rgb.py -m 3 -s 0 -b 100`

Static mode coloring (zone=1 => most left zone, color=blue):  
`./facer_rgb.py -m 0 -z 1 -cR 0 -cB 255 -cG 0`

Static mode coloring (zone=4 => most right zone, color=purple) and save it as example:  
`./facer_rgb.py -m 0 -z 4 -cR 255 -cB 255 -cG 0`

Load the previously saved profile:
`./facer_rgb.py -load example`


## Known problems
If installation failed, check this [issue](https://github.com/JafarAkhondali/acer-predator-turbo-and-rgb-keyboard-linux-module/issues/4#issuecomment-905486393)
If something didn't look right, do a reboot (or boot to windows) and play a little with some Predator Sense app to reset ACPI registers. 

## Uninstall:
Simply run `./uninstall.sh` and (hopefully) everything should be back to normal.  
If you have installed it as a service, simply run `./uninstall_service.sh`

## Uninstall FOR Arch Linux Only

If you install it from AUR repository RUN `sudo pacman -R Predator-Sense-systemd-git`

## Contributors
I lost access to my Acer device. The main reason this project isn’t dead (yet) is because of all the amazing people contributing to it:  

<a href="https://github.com/JafarAkhondali/acer-predator-turbo-and-rgb-keyboard-linux-module/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=JafarAkhondali/acer-predator-turbo-and-rgb-keyboard-linux-module" />
</a>

## Feedback:
If this worked or didn't work for you, kindly make a new issue, and attach the following if possible:  
`sudo dmidecode | grep "Product Name" -B 2 -A 4`  
`sudo cat /sys/firmware/acpi/tables/DSDT > dsdt.aml`



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
- [x] Install as a systemd service (Thanks to [Kapitoha](https://github.com/Kapitoha))
- [x] Add support for saving\load\list profiles (Thanks to [jayrfs](https://github.com/JafarAkhondali/acer-predator-turbo-and-rgb-keyboard-linux-module/pull/33))
- [x] Install as openrc service (Thanks to [Axtloss](https://github.com/JafarAkhondali/acer-predator-turbo-and-rgb-keyboard-linux-module/pull/36))
- [x] Make binary package For Arch Linux (By [mmsaeed509](https://github.com/mmsaeed509)). 
- [x] GUI(Electron): ([Zehra](https://github.com/zehratullayl/Linux-Predator-GUI))
- [x] GUI(wxPython with tray icon): ([x211321](https://github.com/x211321/RGB-Config-Acer-gkbbl-0))
- [x] GUI(PyQt): ([0xb4dc0d3x](https://github.com/0xb4dc0d3x/Acer-RGB-Keyboard-Linux-Module-GUI))
- [x] CLI(Bash): ([Zeaksblog/acer-rgb-menu](https://github.com/Zeaksblog/acer-rgb-menu))
- [x] Add DKMS or an Event to recompile module after kernel upgrades #113
- [ ] Custom Fans speed
- [ ] Implement RGB Dynamic effects (per key RGB)  
- [ ] Implement RGB Static coloring (per key RGB)  


## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=JafarAkhondali/acer-predator-turbo-and-rgb-keyboard-linux-module&type=Date)](https://star-history.com/#JafarAkhondali/acer-predator-turbo-and-rgb-keyboard-linux-module&Date)


## License
GNU General Public License v3
