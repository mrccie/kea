#!/bin/bash

######## User-Set Variables ########
API_PASSWORD="keaPassword123"
API_USERNAME="kea-api"
CTRL_AGENT_IP="127.0.0.1"
CTRL_AGENT_PORT="8080"


######## Ensure the Password/Username/Port/IP is Set ########

#---- Delete this section once you set the variables
echo "Please edit this file to set the API password/username/IP/port"
echo " then remove the sections of the script where marked."
exit 1
#----- / Stop Deleting Here


######## Restart Services ########
curl -s -X POST -H "Content-Type: application/json" -u "$API_USERNAME":"$API_PASSWORD" -d '{ "command": "lease4-get-all", "service": [ "dhcp4" ] }' http://"$CTRL_AGENT_IP":"$CTRL_AGENT_PORT" | jq '.'


