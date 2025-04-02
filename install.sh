#!/bin/bash

######## Ensure the script is run with root privileges ########
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi


######## User-Set Variables ########
API_PASSWORD="keaPassword123"
ADMIN_DIR="/home/etch/kea_tools"
ADMIN_DIR_USER="etch"

######## Necessary Variables ########
API_PASSWORD_FILE="/etc/kea/kea-api-password"
LOG_DIR="/var/log/kea"
DHCP4_LOG_FILE="/var/log/kea/kea-dhcp4.log"
CTRL_LOG_FILE="/var/log/kea/kea-ctrl-agent.log"
DHCP4_CONFIG_FILE="/etc/kea/kea-dhcp4.conf"
CTRL_CONFIG_FILE="/etc/kea/kea-ctrl-agent.conf"



###############################################################################
#                              Kea Installation                               #
###############################################################################

# Inform the user
echo ""
echo "Beginning touchless installation..."
echo ""

# Pre-seed the Kea Control Agent prompts to enable touchless install
#   We will set a password later
echo "kea-ctrl-agent kea-ctrl-agent/make_a_choice select do_nothing" | debconf-set-selections
echo "kea-ctrl-agent kea-ctrl-agent/password-select select do_nothing" | debconf-set-selections

# Install KEA DHCP without prompts
sudo apt update
sudo apt install -y kea

# Confirm installation
if dpkg -l | grep -q kea; then
    echo "KEA DHCP installed successfully."
else
    echo "KEA DHCP installation failed."
    exit 1
fi



###############################################################################
#                         Initial Configuration                               #
###############################################################################

# Inform the user
echo ""
echo "Beginning initial configuration..."

#### Create Kea log files

# Create files
sudo touch "$CTRL_LOG_FILE"
sudo touch "$DHCP4_LOG_FILE"

# Set permissions for files so kea can write to them
sudo chown _kea:_kea "$CTRL_LOG_FILE"
sudo chown _kea:_kea "$DHCP4_LOG_FILE"

# Inform the user
echo "... log files created."


#### Create a password for kea services
# kea services will not start without a password file

# Write password to file
echo -n "$API_PASSWORD" | sudo tee "$API_PASSWORD_FILE" > /dev/null

# Set correct ownership and permissions
sudo chown _kea:_kea "$API_PASSWORD_FILE"
sudo chmod 600 "$API_PASSWORD_FILE"

# Inform th euser
echo "... password file created."


#### Restart the control agent service now that a password is set
sudo systemctl restart kea-ctrl-agent

# Inform the user
echo "... kea-ctrl-agent service restarted."


#### Wrap up this section
echo "... done."



###############################################################################
#                       Copy Initial Config Over                              #
###############################################################################

# Inform the user
echo ""
echo "Copying over initial config files..."


# Backup default files
sudo cp "$DHCP4_CONFIG_FILE" "$DHCP4_CONFIG_FILE".bak
sudo cp "$CTRL_CONFIG_FILE" "$CTRL_CONFIG_FILE".bak

# Inform the user
echo "... original configuration files backed up."


# Copy over defaults from github package
sudo cp ./setup/base_configs/kea-dhcp4.conf "$DHCP4_CONFIG_FILE"
sudo cp ./setup/base_configs/kea-ctrl-agent.conf "$CTRL_CONFIG_FILE"

# Inform the user
echo "... base configuration templates copied."


# Restart kea services
sudo systemctl restart kea-ctrl-agent
sudo systemctl restart kea-dhcp4-server

# Inform the user
echo "... kea services restarted."

# Wrap up this section
echo "... done."



###############################################################################
#                   Create Helper File Structure                              #
###############################################################################

# Inform the user
echo ""
echo "Creating a directory with shortcuts and helpful code snips..."


# Create the directory
sudo mkdir "$ADMIN_DIR"
sudo mkdir "$ADMIN_DIR"/config_scripts

# Validate
if [ ! -d "$ADMIN_DIR" ]; then
  echo "$ADMIN_DIR was Not created successfully."
  exit 1
fi

if [ ! -d "$ADMIN_DIR/config_scripts" ]; then
  echo "$ADMIN_DIR/config_scripts was Not created successfully."
  exit 1
fi


# Change directory ownership
sudo chown "$ADMIN_DIR_USER":"$ADMIN_DIR_USER" "$ADMIN_DIR"
sudo chown "$ADMIN_DIR_USER":"$ADMIN_DIR_USER" "$ADMIN_DIR"/config_scripts


# Copy files
sudo cp ./setup/scripts/restart_services.sh "$ADMIN_DIR"
sudo cp ./setup/scripts/view_leases.sh "$ADMIN_DIR"
sudo cp ./setup/scripts/configure_* "$ADMIN_DIR"/config_scripts

# Change file ownership
sudo chown "$ADMIN_DIR_USER":"$ADMIN_DIR_USER" "$ADMIN_DIR"/*
sudo chown "$ADMIN_DIR_USER":"$ADMIN_DIR_USER" "$ADMIN_DIR"/config_scripts/*


# Add symlinks for easier navigation
mkdir "$ADMIN_DIR"/server_config
sudo ln -s /etc/kea/kea-dhcp4.conf "$ADMIN_DIR"/server_config/kea-dhcp4.conf
sudo ln -s /etc/kea/kea-ctrl-agent.conf "$ADMIN_DIR"/server_config/kea-ctrl-agent.conf

mkdir "$ADMIN_DIR"/logs
sudo ln -s "$LOG_DIR"/kea-dhcp4.log "$ADMIN_DIR"/logs/kea-dhcp4.log
sudo ln -s "$LOG_DIR"/kea-ctrl-agent.log "$ADMIN_DIR"/logs/kea-ctrl-agent.log


# Wrap up this section
echo "... done."



###############################################################################
#                              Kea Installation                               #
###############################################################################

# Inform the user
echo ""
echo "Installing modules for post-setup helper scripts..."

# Install python3-netifaces
sudo apt install -y python3-netifaces

# Install jq
sudo apt install -y jq

# Wrap up this section
echo "... done."


###############################################################################
#                             Finish Out                                      #
###############################################################################

echo ""
echo "That's all I am configured to do.  Good luck!"
echo ""

#sudo chmod +rx /var/log/kea

