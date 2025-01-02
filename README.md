# kea

Author: mrccie

Copyright: 2020, mrccie

Date: 21-SEP-2020

Version: 1.0


## PURPOSE

rpi-7seg-clock is a package designed to drive a 7-segment clock (and, optionally, a digital light sensor) with a Raspberry Pi.  Hopefully this package will let you focus on what's important (cool looking cases) and offload what isn't (the mundane software).

This package will also enable a (very ugly and very basic) web server on the Raspberry Pi that enables you to customize clock settings and even reboot/shut down the Pi.


## System Requirements

This solution has been tested on the following hardware:
- Platform: Raspberry Pi 3B+, Raspberry Pi Zero
- OS: Rasbian 10 (buster)
- Clock Display: [Adafruit 1.2" 4-Digit 7-Segment Display w/ I2C Backpack](https://www.adafruit.com/product/1270) (available in multiple colors)
- [Digital Light Sensor](https://www.amazon.com/gp/product/B00NLA4D4U/ref=ppx_yo_dt_b_asin_title_o02_s01?ie=UTF8&psc=1) (optional)

Note:
- Some soldering is required for the 7-segment display and backpack
- Any digital light sensor should work; there's nothing special about the one linked


## Raspberry Pi Initialization

If you're installing on a Pi from scratch, you'll need to do a few things first.

[Steps to set up a headless RPi](https://www.tomshardware.com/reviews/raspberry-pi-headless-setup-how-to,6028.html)

(Optional but Recommended Step)
[You can also set a static IP](https://www.raspberrypi.org/documentation/configuration/tcpip/).  
An example would be to modify the file <b>/etc/dhcpcd.conf</b> to read as follows (for a wireless connection):
```sh
interface wlan0
static ip_address=192.168.1.50/24    
static routers=192.168.1.1
static domain_name_servers=208.67.220.220 8.8.8.8
```

Change the password of the user 'pi' if you haven't done so already:
```sh
passwd
```

Update the operating system:
```sh
sudo apt-get update
sudo apt-get upgrade
```

Set your local timezone:
```sh
sudo raspi-config
> 5 - Localization Options
>> L2 - Change Time Zone
>>> Pick accordingly
>>>> Finish
```


## Installation: Pre-Requisites and Git

This is just on Git for now.

Pre-requisites:
- Raspberry Pi has internet connectivity
- Terminal access to the Pi (local or via SSH)
- RECOMMENDED: Configure the Pi with a static IP for web reachability

Enable i2c Interface:
```sh
sudo raspi-config
> 3 - Interfacing Options
>> P5 - I2C
>>> Would you like to enable... Yes
>>>> Finish
```
(You may receive an error like 'modprobe: FATAL: Module i2c-dev not found in directory /lib/modules/5.4.83+'; this can be ignored)

Install git:
```sh
sudo apt-get install -y git
```

(Optional) Configure git:
```sh
git config --global user.email "<email>"
git config --global user.name "<username>"
```

Make a directory to clone this repository to:
```sh
mkdir git
cd git
```


## Installation

Clone this repository:
```sh
git clone https://github.com/mrccie/rpi-7seg-clock
```

Go into the repository directory:
```sh
cd rpi-7seg-clock
```

Use the install script:
```sh
sudo ./install.sh
```


## What to Do Next?

If you want to customize your clock beyond the default behavior (ie. change brightness scheme, set to 24-hour mode, etc.), open a web browser and navigate to the IP address of your clock.  When using the web interface, please be aware that changes you make may take a minute or so to be picked up.
