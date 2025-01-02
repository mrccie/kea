#!/bin/bash

######## Ensure the script is run with root privileges ########
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

######## Restart Services ########
sudo systemctl restart kea-ctrl-agent
sudo systemctl restart kea-dhcp4-server

