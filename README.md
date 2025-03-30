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

### (Optional but Strongly Recommended Step) Set a Static IP

Run the following command to list the available network interfaces:
```sh
ip address
```

You'll see output like the below. In this example, ens18 is the interface name (yours may be different).
```sh
2: ens18: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    inet 192.168.1.100/24 brd 192.168.1.255 scope global dynamic ens18
```

Edit or create a new file in /etc/systemd/network/ for the interface:
```sh
sudo vim /etc/systemd/network/10-static.network
```

Add the following configuration (updated for your system):
```sh
[Match]
Name=ens18

[Network]
Address=192.168.2.7/24
Gateway=192.168.2.1
DNS=4.2.2.4 8.8.4.4
```

Run the following commands to enabe systemd-networkd and apply the changes:
```sh
sudo systemctl restart systemd-networkd
sudo systemctl enable systemd-networkd
```

Verify the new IP configuration with:
```sh
ip address
```


### (Optional) Disable WiFi (assuming a Raspberry Pi with an ethernet connection)

Run the following command to list the available network interfaces:
```sh
ip address
```

You'll see output like the below. In this example, wlan0 is the interface name (yours may be different).
```sh
3: wlan0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP mode DORMANT group default qlen 1000
    link/ether d8:3a:dd:89:ab:d1 brd ff:ff:ff:ff:ff:ff
```

Edit the following file:
```sh
sudo vim /boot/firmware/config.txt
```

Add to it:
```sh
dtoverlay=disable-wifi
```

Restar the system:
```sh
sudo shutdown -r now
```


### Change the password of the user 'pi' if you haven't done so already:
```sh
passwd
```

### Update the operating system:
```sh
sudo apt-get update
sudo apt-get upgrade
```

### Set your local timezone:
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
