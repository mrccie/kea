# kea

Author: mrccie

Copyright: 2025, mrccie

Date: 1-JAN-2025

Version: 1.0


## PURPOSE

This package is designed to enable automatic deployment of a kea dhcp server system in a home/prosumer network. DHCP is important but should only be at the forefront of your thoughts if you want it to be.


## System Requirements

This solution has been tested on the following hardware:
- Platform: VM (4x vCPU, 4GB RAM, 24GB Disk) [moving to RPi after initial testing]
- OS: Ubuntu 24.04

Note:
- Resource utilization is nearly non-existent for a small network
- The installation notes below should not be used.  They pertain generally to a Raspberry Pi and will be updated as testing proceeds


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
git clone https://github.com/mrccie/kea
```

Go into the repository directory:
```sh
cd kea
```

Use the install script:
```sh
sudo ./install.sh
```


## What to Do Next?

If you want to customize your clock beyond the default behavior (ie. change brightness scheme, set to 24-hour mode, etc.), open a web browser and navigate to the IP address of your clock.  When using the web interface, please be aware that changes you make may take a minute or so to be picked up.
