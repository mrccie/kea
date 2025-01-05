#!/usr/bin/python3

import os
import json


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




# Function: fn_is_v4_subnet( v4_net ):
#   Checks a string to see if it represents a valid subnet with a format
#   of x.x.x.x/nn.  If the string is not formatted properly the function
#   will return information about what is wrong.
#
#   version 1.0
def fn_is_v4_subnet( v4_net ):

    #### Local Variables ####
    valid_or_not = False
    slash_split = ""
    mask = 0
    network_list = []   # str list
    octet_list = []     # int list


    #### Validate Format of Network Mask ####
    slash_split = v4_net.split("/")
    if len(slash_split) != 2:
        return("Network mask not present or not formatted correctly. Try again.")
    try:
        mask = int(slash_split[1])
        if mask >= 0 and mask <= 32:
            pass
        else:
            return("Network mask must be between 0 and 32. Try again.")
    except ValueError:
        return("Network mask is not a number. Try again.")


    #### Validate Format of Network Component ####
    network_list = slash_split[0].split(".")
    if len(network_list) != 4:
        return("Network not properly formatted. Try again.")
    for octet in network_list:
        try:
            octet = int(octet)
            if octet >= 0 and octet <= 255:
                octet_list.append( octet )
                pass
            else:
                return("Network octet out of range. Try again.")
        except ValueError:
            return("Network octet not a number. Try again.")


    #### Validate that the Subnet Mask Applies Correctly ####
    for octet in octet_list:
        if mask == 0:       # No bits in octet are masked
            if octet > 0:
                return ("Network definition includes host bits. Try again.")
            else:
                pass
        elif mask >= 8:     # All bits in octet are masked
            mask -= 8
        else:   # Some number of bits in this octet are masked
            bit = 7
            while mask > 0:
                bit_value = 2**bit
                if octet >= bit_value:
                    octet -= bit_value
                mask -= 1
                bit -= 1
            if octet > 0:
                return("Network definition includes host bits. Try again.")
            else:
                pass
            

    valid_or_not = True

    return valid_or_not




###############################################################################
#                     KEA - Script Purpose Functions                          #
###############################################################################

# Function: fn_print_scope_menu()
#   Allows the user to pick between the main options in this script/
#
#   version 1.0
def fn_print_main_scope_menu():

    #### Local Variables ####
    user_choice = ""

    #### Print Choices ####
    print()
    print("What scope changes would you like to make?")
    print()
    print("\ta.   Add Scope")
    print("\td.   Delete Scope")
    print("\tm.   Modify Scope")
    print("\tp.   Print Scopes")
    print("\tq.   Quit")
    print()

    #### Get User Choice ####
    while True:
        user_choice = input("Selection (a/d/m/p/q): ")

        if user_choice.lower().startswith("a"):
            user_choice = "a"
            break
        elif user_choice.lower().startswith("d"):
            user_choice = "d"
            break
        elif user_choice.lower().startswith("m"):
            user_choice = "m"
            break
        elif user_choice.lower().startswith("p"):
            user_choice = "p"
            break
        elif user_choice.lower().startswith("q"):
            user_choice = "q"
            break
        else:
            print("Please choose 'a', 'd', 'm', 'p', or 'q'.")

    return user_choice




# Function: fn_print_dhcp4_choices()
#   Prints the scopes in the dhcp4 configuration file.
#
#   version 1.0
def fn_print_dhcp4_scopes():

    #### Local Variables ####
    choice_dic = {}

    #### Main Print Screen ####

    print()
    print("Active scopes on this system:")
    print("\tID   Subnet")

    for scope in g_dhcp4_dic["Dhcp4"]["subnet4"]:
        id_num = scope["id"]
        subnet = scope["subnet"]

        print(f"\t{id_num}    {subnet}")

    print()

    return




# Function: fn_add_dhcp4_scope()
#  Adds a scope as requested by the user.
#
#  version 1.0
def fn_add_dhcp4_scope():

    #### Global Variables ####
    global g_dhcp4_dic
    global g_dhcp4_file


    #### Local Variables ####
    existing_ids = []
    existing_nets = []
    next_scope_id = ""
    user_input = ""
    input_id = 0
    input_net = ""
    added_scope_dic = {}


    #### Print Existing Scope List ####
    print()
    print("***** ACTIVE MODE: ADD v4 SCOPE *****")
    fn_print_dhcp4_scopes()

    
    #### Get List of All Existing Scopes and IDs ####
    for scope in g_dhcp4_dic["Dhcp4"]["subnet4"]:
        existing_ids.append( scope["id"] )
        existing_nets.append( scope["subnet"] )


    #### Identify Next Available Scope ID ####
    i = 1
    while True:
        if i in existing_ids:
            i += 1
        else:
            next_scope_id = i
            break


    #### Get New Scope ID From User ####
    while True:

        user_input = input(f"Enter an ID number for the new scope (#, or 'c' to cancel): [{next_scope_id}] ")
        if user_input == "c":
            return

        elif user_input == "":
            input_id = next_scope_id
            break

        else:
            try:
                input_id = int( user_input )
                if input_id > 0 and input_id < 4294967295:
                    if input_id not in existing_ids:
                        break
                    else:
                        print("Identifiers must be unique. Select one not currently in use.")
                else:
                    print("Identifiers must be greater than 0 and less than 4294967295.")

            except ValueError:
                print("Invalid input. Please enter a number or hit 'enter' to accept a default value.")


    #### Get New Scope Subnet From User ####
    while True:

        user_input = input("Enter a new subnet (x.x.x.x/nn, or 'c' to cancel): ")
        if user_input == "c":
            return

        elif user_input in existing_nets:
            print("Cannot add a network that already exists. Try again or cancel.")

        else:
            is_v4_subnet = fn_is_v4_subnet(user_input)

            if is_v4_subnet == True:
                input_net = user_input
                break
            else:
                print(f"{is_v4_subnet}")


    #### Confirm User Choice ####
    print()
    print(f"You are proposing to add the scope:")
    print(f"\tID   Subnet")
    print(f"\t{input_id}    {input_net}")
    print()
    

    while True:

        user_confirm = input("Are you SURE you want to continue (y/n)? ")
        print()

        if user_confirm.lower().startswith("y"):
            printl(f" Adding scope (ID={input_id}) (Subnet={input_net})")
            break
        elif user_confirm.lower().startswith("n"):
            print("You have selected to cancel. Returning to main menu.")
            input("Press return to continue.")
            return
        else:
            print("Input not 'y' or 'n'. Try again.")
            print()


    #### Add The Scope ####
    added_scope_dic["id"] = input_id
    added_scope_dic["subnet"] = input_net
    g_dhcp4_dic["Dhcp4"]["subnet4"].append( added_scope_dic )

    print("xxxxxxxxxxx WRITING CHANGES DISABLED -- UNCOMMENT TO ENABLE")
    #fn_write_dic_to_json( g_dhcp4_dic, g_dhcp4_file )


    #### Inform The User ####
    print("Scope successfully added")
    input("Press return to continue to main menu.")


    return




# Function: fn_delete_dhcp4_scope()
#  Deletes scopes as requested by the user.
#
#   version 1.0
def fn_delete_dhcp4_scope():

    #### Global Variables ####
    global g_dhcp4_dic
    global g_dhcp4_file


    #### Local Variables ####
    need_choice = True
    user_choice = ""
    match_found = False
    matched_id = ""
    matched_scope = ""
    user_confirm = ""


    #### Print Existing Scope List ####
    print()
    print("***** ACTIVE MODE: DELETE v4 SCOPE *****")
    fn_print_dhcp4_scopes()


    #### Get User Choice ####
    while need_choice == True:

        user_choice = input("Enter ID # of scope to delete (#, or 'c' to cancel): ")

        if user_choice.lower().startswith("c"):
            print("You have selected to cancel. Returning to main menu.")
            return
        else:
            pass

        for scope in g_dhcp4_dic["Dhcp4"]["subnet4"]:
            if user_choice == str(scope["id"]):
                matched_scope = scope["subnet"]
                need_choice = False
                break
            else:
                pass

        if need_choice == True:
            print("Input not an ID number or 'c'. Try again.")
        else:
            pass


    #### Confirm User Choice ####
    print()
    print(f"WARNING: This will delete the scope {matched_scope}!")

    while True:

        user_confirm = input("Are you SURE you want to continue (y/n)? ")

        if user_confirm.lower().startswith("y"):
            printl(f" Deleting scope {matched_scope}")
            break
        elif user_confirm.lower().startswith("n"):
            print("You have selected to cancel. Returning to main menu.")
            return
        else:
            print("Input not 'y' or 'n'. Try again.")
            print()


    #### Delete The Scope ####
    i = 0
    for scope in g_dhcp4_dic["Dhcp4"]["subnet4"]:
        if user_choice == str(scope["id"]):
            del g_dhcp4_dic["Dhcp4"]["subnet4"][i]
            print("xxxxxxxxxxx WRITING CHANGES DISABLED -- UNCOMMENT TO ENABLE")
            #fn_write_dic_to_json( g_dhcp4_dic, g_dhcp4_file )
        else:
            i += 1


    #### Inform The User ####
    print("Scope successfully deleted.")
    input("Press return to continue to main menu.")


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


clear_screen = True
while True:
    if clear_screen == True:
        os.system("clear")

    scope_action = fn_print_main_scope_menu()

    if scope_action == "a":     # Add Scope
        os.system("clear")
        fn_add_dhcp4_scope()
        clear_screen = True

    elif scope_action == "d":   # Delete Scope
        os.system("clear")
        fn_delete_dhcp4_scope()
        clear_screen = True

    elif scope_action == "m":   # Modify Scope
        pass

    elif scope_action == "p":   # Print Scopes
        os.system("clear")
        fn_print_dhcp4_scopes()
        clear_screen = False

    elif scope_action == "q":   # Quit
        printl(" User selected 'quit'. Terminating.")
        print("Exiting.")
        quit()


quit()





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



