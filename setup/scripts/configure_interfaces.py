#!/usr/bin/python3

import os
import json
import netifaces


# Note - DHCP6 items commented out as no working "base" config exists..
#  so removing comments from DHCP6 file creates errors with lines that 
#  should/should not have commas, etc.


###############################################################################
#                          Global Variables                                   #
###############################################################################

g_log_path = "python_log.log"
g_dhcp4_file = "/etc/kea/kea-dhcp4.conf"
#g_dhcp6_file = "/etc/kea/kea-dhcp6.conf"
g_ctrl_file = "/etc/kea/kea-ctrl-agent.conf"
g_dhcp4_dic = {}
#g_dhcp6_dic = {}
g_ctrl_dic = {}




###############################################################################
#                         Commodity Functions                                 #
###############################################################################

# Function: is_root()
#   Checks to see whether a user is root
#
#   version 1.0
def is_root():
    is_root = False

    if os.geteuid() == 0:
        is_root = True
    else:
        is_root = False
        
    return is_root




# Function: printl( log )
#   Appends lines to a log file
#
#   version 1.0
def printl( log ):

    try:
        with open(g_log_path, 'a') as f:
            print( log, file=f)
    except FileNotFoundError:
        print("Error - printl - File Not Found")
        return
    except Exception as err:
        print(f"Error - printl - {err=}, {type(err)=}")
        return

    return




# Function: fn_read_json_file( file_path )
#   1st: Tests to ensure the file is available and appropriate
#   2nd: Reads a JSON file into a dictionary
#   3rd: Returns the dictionary
#
#   version 1.0
def fn_read_json_file( file_path ):

    # Local Variables
    fn_name = "fn_read_json_file"
    dictionary = {}

    # Read a JSON file to a python dictionary
    try:
        with open( file_path ) as json_file:
            dictionary = json.load( json_file )
    except FileNotFoundError:
        printl(f"Error - {fn_name} - File Not Found")
        return "error"
    except Exception as err:
        printl(f"Error - {fn_name} - {err=}, {type(err)=}")
        return "error"
    except BaseException as berr:
        printl(f"Error - {fn_name} - {berr=}, {type(berr)=}")
        return "error"

    return dictionary




# Function: fn_write_dic_to_json( dic, file_path )
#   This fn will Create or Overwrite existing files
#   > Any existing file in this place will be erased
#
#   version 1.0
def fn_write_dic_to_json( dic, file_path ):

    # Local Variables
    was_successful = True
    fn_name = "fn_write_dic_to_json"
    json_dumps_str = json.dumps(dic,indent=4)

    # Execution
    try:
        with open(file_path, 'w') as f:
            print(json_dumps_str, file=f)
    except FileNotFoundError:
        printl(f"Error - {fn_name} - File Not Found")
        return "error"
    except Exception as err:
        printl(f"Error - {fn_name} - {err=}, {type(err)=}")
        return "error"
    except BaseException as berr:
        printl(f"Error - {fn_name} - {berr=}, {type(berr)=}")
        return "error"

    return was_successful




###############################################################################
#                      KEA - Commodity Functions                              #
###############################################################################

# Function: fn_remove_comments_from_file( in_fp, out_fp )
#   KEA accepts the use of Shell (#), C (//), and Multiline (/* */) comments
#    in its configuration file.  These are not JSON compliant.
#   This function takes a file which may contain those comments and
#    removes them, outputting a file with no comments.
#
#   FUTURE IMPROVEMENT: Move comments to a JSON-compliant block, as supported
#    by KEA
#
#   version 1.0
def fn_remove_comments_from_file( in_fp, out_fp ):

    # Local Variables
    fn_name = "fn_remove_comments_from_file"
    was_successful = True
    output_lines = []


    # Read in the file
    try:
        with open(in_fp, 'r') as in_file:
            raw_lines = in_file.readlines()
    except FileNotFoundError:
        printl(f"Error - {fn_name} - File Not Found")
        return "error"
    except Exception as err:
        printl(f"Error - {fn_name} - {err=}, {type(err)=}")
        return "error"
    except BaseException as berr:
        printl(f"Error - {fn_name} - {berr=}, {type(berr)=}")
        return "error"


    # Remove Shell comments ('#')
    uns_lines = []
    for line in raw_lines:
        uns_lines.append( line.split('#', 1)[0] )


    # Remove C comments ('//')
    unc_lines = []
    http_replacement = "MAYO_EATING_CONTEST"
    https_replacement = "MUSTARD_PIE"
    for line in uns_lines:

        exception_1 = line.replace('http://', http_replacement)
        exception_2 = exception_1.replace('https://', https_replacement)

        split_line = exception_2.split('//', 1)[0]

        fix_1 = split_line.replace(http_replacement, 'http://')
        fix_2 = fix_1.replace(https_replacement, 'https://')

        unc_lines.append( fix_2 )


    # Remove Multiline comments ('/*' to '*/')
    #  Will fail if a previous multiline comment ends on a line
    #   that then has real conent, and a new multiline
    #   comment then starts on the same line.
    #  This is an edge case I'm not solving for.
    unm_lines = []
    comment_line = False
    for line in unc_lines:
        if comment_line == False:
            if "/*" in line:
                comment_line = True
            if "*/" in line:
                comment_line = False
            unm_lines.append( line.split('/*', 1)[0] )
        else:
            if "*/" in line:
                comment_line = False
                unm_lines.append( line.split('*/', 1)[1] )
            else:
                continue

    # Strip trailing spaces, tabs, and newline characters
    stripped_lines = []
    for line in unm_lines:
        stripped_lines.append( line.rstrip() )


    # Make the rest of this function more obvious
    output_lines = stripped_lines


    # Write the output file
    try:
        with open(out_fp, 'w') as out_file:
            for line in output_lines:
                if len(line) > 0:
                    out_file.write(line + "\n")
                else:
                    continue
    except FileNotFoundError:
        printl(f"Error - {fn_name} - File Not Found")
        return "error"
    except Exception as err:
        printl(f"Error - {fn_name} - {err=}, {type(err)=}")
        return "error"
    except BaseException as berr:
        printl(f"Error - {fn_name} - {berr=}, {type(berr)=}")
        return "error"

    return was_successful




# Function: fn_read_configurations()
#   Reads all major configuration files and sends contents to
#   global dictionaries.
#
#   version 1.0
def fn_read_configuration():

    #### Global Variables ####
    global g_dhcp4_file
    #global g_dhcp6_file
    global g_ctrl_file
    global g_dhcp4_dic
    #global g_dhcp6_dic
    global g_ctrl_dic

    #### Local Variables ####
    was_good = True


    #### Remove Comments from Files Before Reading ####

    # DHCP4 Configuration File
    was_good = fn_remove_comments_from_file( g_dhcp4_file, g_dhcp4_file )
    if was_good == "error":
        print("CRIT - Could not remove comments from dhcp4 config. Exiting.")
        quit()
    else:
        pass

    # DHCP6 Configuration File
    #was_good = fn_remove_comments_from_file( g_dhcp6_file, g_dhcp6_file )
    #if was_good == "error":
    #    print("CRIT - Could not remove comments from dhcp6 config. Exiting.")
    #    quit()
    #else:
    #    pass

    # DHCP4 Configuration File
    was_good = fn_remove_comments_from_file( g_ctrl_file, g_ctrl_file )
    if was_good == "error":
        print("CRIT - Could not remove commnets from control agent config. Exiting.")
        quit()
    else:
        pass


    #### Read Config Files into Global Variables ####
    g_dhcp4_dic = fn_read_json_file( g_dhcp4_file )
    #g_dhcp6_dic = fn_read_json_file( g_dhcp6_file )
    g_ctrl_dic = fn_read_json_file( g_ctrl_file )

    if g_dhcp4_dic == "error":
        print("CRIT - Could not read the dhcp4 config. Exiting.")
        quit()
    #elif g_dhcp6_dic == "error":
    #    print("CRIT - Could not read the dhcp6 config. Exiting.")
    #    quit()
    elif g_ctrl_dic == "error":
        print("CRIT - Could not read the ctrl config. Exiting.")
        quit()
    else:
        pass

    return




###############################################################################
#                     KEA - Script Purpose Functions                          #
###############################################################################

# Function: fn_get_interface_info()
#   Collects all of the interfaces and associated IP addresses
#   on a system into a dictionary, which is returned.
#
#   version 1.0
def fn_get_interface_info():

    #### Local Variables ####
    iface_dic = {}
    ipv4_key = 0
    ipv6_key = 0


    #### Collect Information fron netifaces ####

    # Identify the index in netifaces that IPv4 returns with
    #   This can change per system
    ipv4_key = netifaces.AF_INET

    # Identify the index in netifaces that IPv6 returns with
    #   This can change per system
    ipv6_key = netifaces.AF_INET6

    # Get a list of all interfaces on the system
    iface_dic = {}
    for interface in netifaces.interfaces():
        iface_dic[interface] = {'ipv4':[], 'ipv6':[]}

    # Harvest the IP info for each interface
    # (note: in some circumstances an interface may have multiple IPs)
    for interface in iface_dic:

        v4_info = netifaces.ifaddresses( interface )[ipv4_key]
        v6_info = netifaces.ifaddresses( interface )[ipv6_key]

        for entry in v4_info:
            ipv4_addr = entry['addr']
            iface_dic[interface]['ipv4'].append( ipv4_addr )

        for entry in v6_info:
            ipv6_addr = entry['addr']
            iface_dic[interface]['ipv6'].append( ipv6_addr )


    return iface_dic




# Function: fn_correlate_ifaces( iface_dic )
#   Flags whether an iface is in use by a service.
#
#   version 1.0
def fn_correlate_ifaces( iface_dic ):

    #### Global Variables ####
    global g_dhcp4_dic


    #### Enrich the Interface Dictionary ####
    
    # Elucidate which interfaces are configured for purpose
    for iface in iface_dic:
        if iface in g_dhcp4_dic["Dhcp4"]["interfaces-config"]["interfaces"]:
            iface_dic[iface]["dhcp4_enabled"] = "Yes"
        else:
            iface_dic[iface]["dhcp4_enabled"] = "No"

    return iface_dic




# Function: fn_print_dhcp4_choices( iface_dic )
#   Displays IPv4 interfaces and user proposed changes
#
#   version 1.0
def fn_print_dhcp4_choices( iface_dic ):

    #### Local Variables ####
    choice_dic = {}

    #### Main Print Screen ####
    print("\tNo.  Interface\tDHCP Enabled?\tIPv4 Address")
    i = 1
    for iface in iface_dic:

        choice_dic[str(i)] = iface
        ipv4 = iface_dic[iface]["ipv4"]

        if iface_dic[iface]["dhcp4_enabled"] == "Yes":
            enabled = "y"
        elif iface_dic[iface]["dhcp4_enabled"] == "Yes*":
            enabled = "y*"
        elif iface_dic[iface]["dhcp4_enabled"] == "No*":
            enabled = "n*"
        else:
            enabled = "n"

        if len(iface) < 6:
            print( f"\t{i}    {iface}\t\t     {enabled}\t\t{ipv4}" )
        else:
            print( f"\t{i}    {iface}\t     {enabled}\t\t{ipv4}" )

        i += 1

    print()
    print("\t* = proposed change")
    print()

    return choice_dic



# Function: fn_select_interfaces( iface_dic )
#   Collects all of the interfaces and associated IP addresses
#   on a system into a dictionary, which is returned.
#
#   version 1.0
def fn_select_interfaces( iface_dic ):

    #### Local Variables ####
    run_outer = True
    run_inner = True
    choice_dic = {}


    #### Get User Selections ####

    # Main Loop
    while run_outer:

        run_inner = True

        print()
        print("The following interfaces are installed on this system:")
        print()
        choice_dic = fn_print_dhcp4_choices( iface_dic )


        while run_inner:

            user_input = input("Select an interface to toggle (#, p=print, d=done): ").lower()

            if user_input in ("p", "print"):
                run_inner = False
                continue

            elif user_input in ("d", "done"):
                run_inner = False
                run_outer = False
                continue

            elif user_input in choice_dic.keys():
                print(f"You selected {choice_dic[user_input]}")
                toggle_iface = choice_dic[user_input]
                if iface_dic[toggle_iface]["dhcp4_enabled"] == "Yes":
                    iface_dic[toggle_iface]["dhcp4_enabled"] = "No*"
                elif iface_dic[toggle_iface]["dhcp4_enabled"] == "Yes*":
                    iface_dic[toggle_iface]["dhcp4_enabled"] = "No"
                elif iface_dic[toggle_iface]["dhcp4_enabled"] == "No":
                    iface_dic[toggle_iface]["dhcp4_enabled"] = "Yes*"
                elif iface_dic[toggle_iface]["dhcp4_enabled"] == "No*":
                    iface_dic[toggle_iface]["dhcp4_enabled"] = "Yes"
                else:
                    printl("CRIT - Exception hit in fn_select_interfaces. Quitting.")
                    print("CRIT - Exception hit in fn_select_interfaces. Quitting.")
                    quit()

            else:
                print(f"Command not a valid number, 'd' or 'p'. Try again.")


    #### Confirm User Choices ####

    print()
    print()
    print("You have selected to listen on the following interfaces:")
    print()

    while True:

        # Print table for user
        choice_dic = fn_print_dhcp4_choices( iface_dic )

        # Get user choice
        user_input = input("Do you want to confirm this choice? (yes/no): ").lower()
        if user_input.lower().startswith("y"):
            return iface_dic


        elif user_input.lower().startswith("n"):
            print("You elected not to make any changes. Aborting.")
            quit()

    return




###############################################################################
#                           KEA - Main Execution                              #
###############################################################################

# Check if user is root
is_root = is_root()
if is_root:
    printl("User ran 'configure_interfaces.py'")
else:
    printl("CRIT - configure_interfaces.py not run as root. Terminating.")
    print("CRIT - This script must be run as root to modify files.")
    quit()


# Read all running configuration files
fn_read_configuration()

# Collect information about all existing interfaces
iface_dic = fn_get_interface_info()

# Correlate running config and interfae information
iface_dic = fn_correlate_ifaces( iface_dic )

# Get the user to select interfaces to run dhcpv4 on
iface_dic = fn_select_interfaces( iface_dic )


#### Make the changes ####

# Update the configuration dictionary
g_dhcp4_dic["Dhcp4"]["interfaces-config"]["interfaces"] = []
for iface in iface_dic:
    if iface_dic[iface]["dhcp4_enabled"] == "Yes":
        g_dhcp4_dic["Dhcp4"]["interfaces-config"]["interfaces"].append( iface )
    elif iface_dic[iface]["dhcp4_enabled"] == "Yes*":
        g_dhcp4_dic["Dhcp4"]["interfaces-config"]["interfaces"].append( iface )
    else:
        pass


# Write the configuration dictionary
was_good = fn_write_dic_to_json( g_dhcp4_dic, g_dhcp4_file )

# Inform the user
if was_good:
    printl("Interface changes were made the dhcpv4 configuration file.")
    print("Your changes have been made. Please restart services for changes to take effect.")
else:
    printl("CRIT - An error has occurred with writing the dhcp4 changes. Please check the logs and try again.")
    print("CRIT - An error has occurred with writing the dhcp4 changes. Please check the logs and try again.")



