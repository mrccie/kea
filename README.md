# kea

Author: mrccie

Copyright: 2025, mrccie

Date: 31-MAR-2025

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

### (Optional but Strongly Recommended Step) Set a Static IP - HEADLESS SETUP (if a GUI is in use, set it in Network Manager)

Run the following command to list the available network interfaces:
```sh
ip address
```

You'll see output like the below. In this example, eth0 is the interface name (yours may be different).
```sh
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether d8:3a:dd:89:ee:4c brd ff:ff:ff:ff:ff:ff
    inet 192.168.2.118/24 brd 192.168.2.255 scope global dynamic noprefixroute eth0
       valid_lft 50497sec preferred_lft 50497sec
    inet6 fe80::e5ed:478a:a19e:548/64 scope link noprefixroute
       valid_lft forever preferred_lft forever
```

Edit or create a new file in /etc/systemd/network/ for the interface:
```sh
sudo vim /etc/systemd/network/10-static.network
```

Add the following configuration (updated for your system):
```sh
[Match]
Name=eth0

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

(If You're Running a GUI-based distro as Headless...) Disable NetwokManager or it will interfere with DNS
```sh
sudo systemctl stop NetworkManager
sudo systemctl disable NetworkManager

sudo rm /etc/resolv.conf
```

Set up DNS manually:
```sh
echo "nameserver 4.2.2.4" | sudo tee /etc/resolv.conf
echo "nameserver 8.8.8.8" | sudo tee -a /etc/resolv.conf
```

Make sure the file can't be overwritten by marking it immutable:
```sh
sudo chattr +i /etc/resolv.conf
```

Restart Networking
```sh
sudo systemctl restart systemd-networkd
```

Validate DNS is operational:
```sh
ping -c 3 google.com
```


### (Optional) Disable WiFi (assuming a Raspberry Pi with an ethernet connection)

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

There are a few tools built into ~/kea_tools.  Navigate there and check them out.  If they don't do enough for you, Google is your friend!

Note: If you want to accept this scripts default API username and password, you can simply edit the "view_leases.sh" file to remove the "info" section, as the defaults are already loaded.
