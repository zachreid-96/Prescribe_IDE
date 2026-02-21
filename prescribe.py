#!/usr/bin/env python
from __future__ import print_function, absolute_import
import sys
import subprocess
import platform
import os
import re


class prescribe_file_commands:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            try:
                cls._instance.event_log_path = os.path.join(os.environ['USERPROFILE'],
                                                            'Kyocera_commands', 'event_log.txt')
                cls._instance.tiered_color_on_path = os.path.join(os.environ['USERPROFILE'],
                                                                  'Kyocera_commands', '3_tier_on.txt')
                cls._instance.tiered_color_off_path = os.path.join(os.environ['USERPROFILE'],
                                                                   'Kyocera_commands', '3_tier_off.txt')
                cls._instance.line_mode_60_path = os.path.join(os.environ['USERPROFILE'],
                                                               'Kyocera_commands', 'file_path_60.txt')
                cls._instance.line_mode_66_path = os.path.join(os.environ['USERPROFILE'],
                                                               'Kyocera_commands', 'file_path_66.txt')
                cls._instance.tray_switch_on_path = os.path.join(os.environ['USERPROFILE'],
                                                                 'Kyocera_commands', 'tray_switch_on.txt')
                cls._instance.tray_switch_off_path = os.path.join(os.environ['USERPROFILE'],
                                                                  'Kyocera_commands', 'tray_switch_off.txt')
                cls._instance.sleep_timer_on_path = os.path.join(os.environ['USERPROFILE'],
                                                                 'Kyocera_commands', 'sleep_timer_on.txt')
                cls._instance.sleep_timer_off_path = os.path.join(os.environ['USERPROFILE'],
                                                                  'Kyocera_commands', 'sleep_timer_off.txt')
                cls._instance.backup_FRPO_path = os.path.join(os.environ['USERPROFILE'],
                                                              'Kyocera_commands', 'backup.txt')
                cls._instance.init_FRPO_path = os.path.join(os.environ['USERPROFILE'],
                                                            'Kyocera_commands', 'initialize.txt')
            except KeyError:
                cls._instance.event_log_path = os.path.join(os.environ['HOME'],
                                                            'Kyocera_commands', 'event_log.txt')
                cls._instance.tiered_color_on_path = os.path.join(os.environ['HOME'], 'Kyocera_commands',
                                                                  '3_tier_on.txt')
                cls._instance.tiered_color_off_path = os.path.join(os.environ['HOME'], 'Kyocera_commands',
                                                                   '3_tier_off.txt')
                cls._instance.line_mode_60_path = os.path.join(os.environ['HOME'], 'Kyocera_commands',
                                                               'file_path_60.txt')
                cls._instance.line_mode_66_path = os.path.join(os.environ['HOME'], 'Kyocera_commands',
                                                               'file_path_66.txt')
                cls._instance.tray_switch_on_path = os.path.join(os.environ['HOME'], 'Kyocera_commands',
                                                                 'tray_switch_on.txt')
                cls._instance.tray_switch_off_path = os.path.join(os.environ['HOME'], 'Kyocera_commands',
                                                                  'tray_switch_off.txt')
                cls._instance.sleep_timer_on_path = os.path.join(os.environ['HOME'], 'Kyocera_commands',
                                                                 'sleep_timer_on.txt')
                cls._instance.sleep_timer_off_path = os.path.join(os.environ['HOME'], 'Kyocera_commands',
                                                                  'sleep_timer_off.txt')
                cls._instance.backup_FRPO_path = os.path.join(os.environ['HOME'],
                                                              'Kyocera_commands', 'backup.txt')
                cls._instance.init_FRPO_path = os.path.join(os.environ['HOME'],
                                                            'Kyocera_commands', 'initialize.txt')

            cls._instance.file_list = [
                cls._instance.event_log_path, cls._instance.tiered_color_on_path, cls._instance.tiered_color_off_path,
                cls._instance.line_mode_60_path, cls._instance.line_mode_66_path, cls._instance.tray_switch_on_path,
                cls._instance.tray_switch_off_path, cls._instance.sleep_timer_on_path,
                cls._instance.sleep_timer_off_path, cls._instance.backup_FRPO_path, cls._instance.init_FRPO_path
            ]

            cls._instance.event_log_command = '!R!KCFG"ELOG";EXIT;'
            cls._instance.tiered_color_on_command = '!R!KCFG"TCCM",1;\n!R!KCFG"STCT",1,20;\n!R!KCFG"STCT",2,50;EXIT;'
            cls._instance.tiered_color_off_command = '!R!KCFG"TCCM",0;EXIT;'
            cls._instance.line_mode_60_command = '!R! FRPO U0,6; FRPO U1,60; EXIT;'
            cls._instance.line_mode_66_command = '!R! FRPO U0,6; FRPO U1,66; EXIT;'
            cls._instance.tray_switch_on_command = '!R! FRPO X9,9; FRPO R2,0; EXIT;'
            cls._instance.tray_switch_off_command = '!R! FRPO X9,0; FRPO R2,0; EXIT;'
            cls._instance.sleep_timer_on_command = '!R! FRPO N5,1; EXIT;'
            cls._instance.sleep_timer_off_command = '!R! FRPO N5,0; EXIT;'
            cls._instance.backup_FRPO_command = '!R! STAT,1; EXIT;'
            cls._instance.init_FRPO_command = '!R! FRPO INIT; EXIT;'

            cls._instance.file_command_list = [
                cls._instance.event_log_command, cls._instance.tiered_color_on_command,
                cls._instance.tiered_color_off_command, cls._instance.line_mode_60_command,
                cls._instance.line_mode_66_command, cls._instance.tray_switch_on_command,
                cls._instance.tray_switch_off_command, cls._instance.sleep_timer_on_command,
                cls._instance.sleep_timer_off_command, cls._instance.backup_FRPO_command,
                cls._instance.init_FRPO_command
            ]

        return cls._instance

    def get_event_log_info(self):
        return self.event_log_path, self.event_log_command

    def tiered_color_on_info(self):
        return self.tiered_color_on_path, self.tiered_color_on_command

    def tiered_color_off_info(self):
        return self.tiered_color_off_path, self.tiered_color_off_command

    def line_mode_60_info(self):
        return self.line_mode_60_path, self.line_mode_60_command

    def line_mode_66_info(self):
        return self.line_mode_66_path, self.line_mode_66_command

    def tray_switch_on_info(self):
        return self.tray_switch_on_path, self.tray_switch_on_command

    def tray_switch_off_info(self):
        return self.tray_switch_off_path, self.tray_switch_off_command

    def sleep_timer_on_info(self):
        return self.sleep_timer_on_path, self.sleep_timer_on_command

    def sleep_timer_off_info(self):
        return self.sleep_timer_off_path, self.sleep_timer_off_command

    def backup_FRPO_info(self):
        return self.backup_FRPO_path, self.backup_FRPO_command

    def init_FRPO_info(self):
        return self.init_FRPO_path, self.init_FRPO_command

    def delete_files(self):
        for file in self.file_list:
            if os.path.exists(file):
                os.remove(file)

    def create_files(self):
        for file, command in zip(self.file_list, self.file_command_list):
            with open(file, 'w') as f:
                f.write(command)


def update():
    print("")
    print("Or visit the following link to check for an updated version, find the newest 'Python-v' tag")
    print("https://github.com/zachreid-96/Prescribe_Scripting_Tool/releases")
    print("")
    safe_exit("SAFE EXIT - Displayed Update Link")


def help_options():
    print("")
    print("Please see the README.md for help with this script")
    print("Or visit the following link to see the README, script notes, or submit a bug report")
    print("https://github.com/zachreid-96/Prescribe_Scripting_Tool/tree/python")
    print("")
    print("The following are all commands passable via CLI (let ip_addr stand for any given IP address)")
    print("")
    print("python prescribe.py ip_addr event_log")
    print("python prescribe.py ip_addr tiered_color_on")
    print("python prescribe.py ip_addr tiered_color_off")
    print("python prescribe.py ip_addr 60_lines")
    print("python prescribe.py ip_addr 66_lines")
    print("python prescribe.py ip_addr tray_switch_on")
    print("python prescribe.py ip_addr tray_switch_off")
    print("python prescribe.py ip_addr sleep_timer_on")
    print("python prescribe.py ip_addr sleep_timer_off")
    print("python prescribe.py ip_addr print_error_list")
    print("python prescribe.py ip_addr backup")
    print("python prescribe.py ip_addr initialize")
    print("python prescribe.py --commands")
    print("python prescribe.py --commands print_error_list")
    print("python prescribe.py --commands delete_commands")
    print("python prescribe.py --commands create_commands")
    print("python prescribe.py --help")
    print("python prescribe.py --update")
    print("")
    safe_exit("SAFE EXIT - Displayed Help Options")


# Passed args
# 	passed_ip = ip and should be the IP address
# 	passed_command = command and should be the desired prescribe command
# Gets the IP address from the user. Specifically the IP of the copier/printer
# If no input is entered, the pre-programmed error list will be displayed and exit intentionally
# Will then call split_ip
# NO RETURNS
def get_ip(ip, command):
    passed_ip = ip
    passed_command = command
    print("")
    print("For help using this script or to see all available commands enter '--help'")
    print("\tOr run the script again from CLI with arg '--help'")
    print("Please enter the Copier's IP in the following format: 10.120.11.68")
    print("Or press enter to display the error list")

    try:
        machine_ip = raw_input("Copier/Printer IP: ")
    except NameError:
        machine_ip = input("Copier/Printer IP: ")

    if machine_ip == "":
        error_list()
    elif machine_ip == "--help":
        help_options()
    else:
        split_ip(machine_ip, passed_command)


# Passed args
# 	passed_ip = ip and should be the IP address
# 	passed_command = command and should be the desired prescribe command
# Splits IP into octets and checks each octet to see if it is valid
# Will call pre-programmed error states if a flag is thrown, like too many or few octets or an invalid number
# Will then call ping_ip
# NO RETURNS
def split_ip(ip, command):
    passed_ip = ip
    passed_command = command

    ip_arr = passed_ip.split('.')
    ip_int_arr = []

    if len(ip_arr) == 4:
        for octet in ip_arr:
            try:
                ip_int_arr.append(int(octet))
            except ValueError:
                error_exit("[IP_INVALID_OCTET_ERROR]")

        if not 1 <= ip_int_arr[0] <= 223:
            error_exit("[IP_OCTET_BOUNDING_ERROR]")
        if not 0 <= ip_int_arr[1] <= 255:
            error_exit("[IP_OCTET_BOUNDING_ERROR]")
        if not 0 <= ip_int_arr[2] <= 255:
            error_exit("[IP_OCTET_BOUNDING_ERROR]")
        if not 1 <= ip_int_arr[3] <= 254:
            error_exit("[IP_OCTET_BOUNDING_ERROR]")

        new_ip = "{0}.{1}.{2}.{3}".format(ip_int_arr[0], ip_int_arr[1], ip_int_arr[2], ip_int_arr[3])
        ping_ip(new_ip, passed_command)
    else:
        if len(ip_arr) > 4:
            error_exit("[IP_TOO_MANY_OCTETS_ERROR]")
        else:
            error_exit("[IP_MISSING_OCTETS_ERROR]")


# Passed args
# 	passed_ip = ip and should be the IP address
# 	passed_command = command and should be the desired prescribe command
# Pings the passed IP address to confirm a connection before sending the command to the device
# Will call pre-programmed error states if a flag is thrown, like cannot ping device
# Will then call nc_command if all is good
# NO RETURNS
def ping_ip(ip, command):
    passed_ip = ip
    passed_command = command
    system = platform.system().lower()

    if system == 'windows':
        output = subprocess.check_output(['ping', '-n', '1', passed_ip]).decode('utf-8')
    else:
        output = subprocess.check_output(['ping', '-c', '1', passed_ip]).decode('utf-8')

    if output.__contains__("unreachable"):
        error_exit("[PING_TEST_FAILED_ERROR]")
    else:
        get_command(passed_command, passed_command)


# Passed args
# 	passed_ip = ip and should be the IP address
# 	passed_command = command and should be the desired prescribe command
# Prints Command List for user to see and make a choice
# Expects a num (int) and will throw intentional error if anything else is entered
# Returns number (int) based on user choice in menu
def get_command(ip, command):
    passed_ip = ip
    passed_command = command

    user_choice = -99
    command_dictionary = []
    command_dictionary.append("print_error_list")
    command_dictionary.append("event_log")
    command_dictionary.append("tiered_color_on")
    command_dictionary.append("tiered_color_off")
    command_dictionary.append("60_lines")
    command_dictionary.append("66_lines")
    command_dictionary.append("tray_switch_on")
    command_dictionary.append("tray_switch_off")
    command_dictionary.append("sleep_timer_on")
    command_dictionary.append("sleep_timer_off")
    command_dictionary.append("backup")
    command_dictionary.append("initialize")
    command_dictionary.append("delete_commands")
    command_dictionary.append("create_commands")

    if passed_command == "":
        print("Command Options:")
        print("[ 1 ] - Event Log")
        print("[ 2 ] - Turn on 3 Tier Color")
        print("[ 3 ] - Turn off 3 Tier Color")
        print("[ 4 ] - Turn on 60 Lines Mode")
        print("[ 5 ] - Turn on 66 Lines Mode")
        print("[ 6 ] - Turn on Tray Switch")
        print("[ 7 ] - Turn off Tray Switch")
        print("[ 8 ] - Turn on Sleep Timer")
        print("[ 9 ] - Turn off Sleep Timer")
        print("[ 10 ] - Backup FRPO Settings")
        print("[ 11 ] - Initialize FRPO Settings")

        print("")

        try:
            user_choice = str(input("Enter Menu Choice: "))
        except NameError:
            user_choice = str(input("Enter Menu Choice: "))

    if user_choice == -99:
        user_choice = str(command_dictionary.index(passed_command))

    if user_choice == "1":
        event_log(passed_ip)
    elif user_choice == "2" or user_choice == "3":
        toggle_tiered_color(passed_ip, user_choice)
    elif user_choice == "4" or user_choice == "5":
        toggle_line_mode(passed_ip, user_choice)
    elif user_choice == "6" or user_choice == "7":
        toggle_tray_switch(passed_ip, user_choice)
    elif user_choice == "8" or user_choice == "9":
        toggle_sleep_timer(passed_ip, user_choice)
    elif user_choice == "10" or user_choice == "11":
        backup_initialize(passed_ip, user_choice)

    error_exit("[INVALID_COMMAND_ENTRY_ERROR]")


# Passed args
# 	passed_ip = ip and should be the IP address
# Will create command file if needed
# Prints out the machines event log
# NO RETURNS
def event_log(ip):
    prescribe_commands = prescribe_file_commands()
    event_log_path, event_log_command = prescribe_commands.get_event_log_info()

    if not os.path.exists(event_log_path):
        with open(event_log_path, 'w') as f:
            f.write(event_log_command)

    send_lpr_command(ip, event_log_path)


# Passed args
# 	passed_ip = ip and should be the IP address
# 	passed_command = command and should be the desired prescribe command
# Will create command file if needed
# Toggles sleep timer ON/OFF
# When turning ON 3 tiered color
#   Uses the following 'default' structure where
#   Level 1 = 0-2% color, Level 2 = 2-5% color, and Level 3 = 6+% color
# NO RETURNS
def toggle_tiered_color(ip, command):
    prescribe_commands = prescribe_file_commands()
    tiered_color_on, tiered_color_on_command = prescribe_commands.tiered_color_on_info()
    tiered_color_off, tiered_color_off_command = prescribe_commands.tiered_color_off_info()

    if command == "2":
        if not os.path.exists(tiered_color_on):
            with open(tiered_color_on, 'w') as f:
                f.write(tiered_color_on_command)
        send_lpr_command(ip, tiered_color_on)

    elif command == "3":
        if not os.path.exists(tiered_color_off):
            with open(tiered_color_off, 'w') as f:
                f.write(tiered_color_off_command)
        send_lpr_command(ip, tiered_color_off)


# Passed args
# 	passed_ip = ip and should be the IP address
# 	passed_command = command and should be the desired prescribe command
# Will create command file if needed
# Toggles line mode between 60/66 lines a page
# NO RETURNS
def toggle_line_mode(ip, command):
    prescribe_commands = prescribe_file_commands()
    line_mode_60, line_mode_60_command = prescribe_commands.line_mode_60_info()
    line_mode_66, line_mode_66_command = prescribe_commands.line_mode_66_info()

    if command == "4":
        if not os.path.exists(line_mode_60):
            with open(line_mode_60, 'w') as f:
                f.write(line_mode_60_command)
        send_lpr_command(ip, line_mode_60)

    elif command == "5":
        if not os.path.exists(line_mode_66):
            with open(line_mode_66, 'w') as f:
                f.write(line_mode_66_command)
        send_lpr_command(ip, line_mode_66)


# Passed args
# 	passed_ip = ip and should be the IP address
# 	passed_command = command and should be the desired prescribe command
# Will create command file if needed
# Toggles tray switch ON/OFF
# NO RETURNS
def toggle_tray_switch(ip, command):
    prescribe_commands = prescribe_file_commands()
    tray_switch_on, tray_switch_on_command = prescribe_commands.tray_switch_on_info()
    tray_switch_off, tray_switch_off_command = prescribe_commands.tray_switch_off_info()

    if command == "6":
        if not os.path.exists(tray_switch_on):
            with open(tray_switch_on, 'w') as f:
                f.write(tray_switch_on_command)
        send_lpr_command(ip, tray_switch_on)

    elif command == "7":
        if not os.path.exists(tray_switch_off):
            with open(tray_switch_off, 'w') as f:
                f.write(tray_switch_off_command)
        send_lpr_command(ip, tray_switch_off)


# Passed args
# 	passed_ip = ip and should be the IP address
# 	passed_command = command and should be the desired prescribe command
# Will create command file if needed
# Toggles sleep timer ON/OFF
# Toggle ON sets Sleep Timer to 5 minutes
# NO RETURNS
def toggle_sleep_timer(ip, command):
    prescribe_commands = prescribe_file_commands()
    sleep_timer_on, sleep_timer_on_command = prescribe_commands.sleep_timer_on_info()
    sleep_timer_off, sleep_timer_off_command = prescribe_commands.sleep_timer_off_info()

    if command == "8":
        if not os.path.exists(sleep_timer_on):
            with open(sleep_timer_on, 'w') as f:
                f.write(sleep_timer_on_command)
        send_lpr_command(ip, sleep_timer_on)

    elif command == "9":
        if not os.path.exists(sleep_timer_off):
            with open(sleep_timer_off, 'w') as f:
                f.write(sleep_timer_off_command)
        send_lpr_command(ip, sleep_timer_off)


# Passed args
# 	passed_ip = ip and should be the IP address
# 	passed_command = command and should be the desired prescribe command
# Will create command file if needed
# Initializes FRPO settings or backups them up by printing Service Status Page
# NO RETURNS
def backup_initialize(ip, command):
    prescribe_commands = prescribe_file_commands()
    init_FRPO, init_FRPO_command = prescribe_commands.init_FRPO_info()
    backup_FRPO, backup_FRPO_command = prescribe_commands.backup_FRPO_info()
    try:
        init_FRPO = os.path.join(os.environ['USERPROFILE'], 'Kyocera_commands', 'initialize.txt')
        backup_FRPO = os.path.join(os.environ['USERPROFILE'], 'Kyocera_commands', 'backup.txt')
    except KeyError:
        init_FRPO = os.path.join(os.environ['HOME'], 'Kyocera_commands', 'initialize.txt')
        backup_FRPO = os.path.join(os.environ['HOME'], 'Kyocera_commands', 'backup.txt')

    if command == "10":
        if not os.path.exists(backup_FRPO):
            with open(backup_FRPO, 'w') as f:
                f.write(backup_FRPO_command)
        send_lpr_command(ip, backup_FRPO)

    elif command == "11":
        if not os.path.exists(init_FRPO):
            with open(init_FRPO, 'w') as f:
                f.write(init_FRPO_command)
        send_lpr_command(ip, init_FRPO)


# Passed args
# 	ip = ip of the device
# 	command = the desired prescribe command .txt file path
# First checks if LPR is enabled and ready to use in both windows and unix/macOS systems
# Uses LPR to send the command to the machine
# NO RETURNS
def send_lpr_command(ip, command):
    system = platform.system().lower()
    if system == 'windows':
        try:
            subprocess.call(['where', 'lpr'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
            error_exit("[LPR_NOT_ENABLED_ERROR]")
    else:
        try:
            subprocess.call(['which', 'lpr'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
            error_exit("[LPR_NOT_ENABLED_ERROR]")

    subprocess.call(['lpr', '-S', ip, '-P', '9100', command],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)


# Passed args
# 	command = the desired prescribe command
# Gathers a list of all programmed prescribe command file entries
# 98 - Checks if file exists then deletes it if TRUE
# 99 - Creates fresh
# NO RETURNS
def prescribe_file_handler(command):
    prescribe_commands = prescribe_file_commands()

    if command == "98" or command == "delete_commands":
        prescribe_commands.delete_files()
        safe_exit("SAFE EXIT - Deleted all Prescribe Command .txt files")
    elif command == "99" or command == "create_commands":
        prescribe_commands.create_files()
        safe_exit("SAFE EXIT - Created all Prescribe Command .txt files")

    exit()


def safe_exit(safe_condition):
    print("")
    try:
        raw_input("{0}. Press any key to exit...".format(safe_condition))
    except NameError:
        input("{0}. Press any key to exit...".format(safe_condition))
    exit()


# Passed args
#   err_condition = whatever pre-programmed error code happened
# Will let the user know that an intentional error state happened
# Will also print out the programmed error code
# NO RETURNS
def error_exit(err_condition):
    print("")
    try:
        raw_input("{0}. Press any key to exit...".format(err_condition))
    except NameError:
        input("{0}. Press any key to exit...".format(err_condition))
    exit()


# NO PASSED ARGS
# Prints out all pre-programmed error codes, description, and an example or two
# NO RETURNS
def error_list():
    print("")
    print("ERROR_CODE: IP_MISSING_OCTETS_ERROR")
    print("DESCRIPTION: The IP address is missing one or more octets.")
    print("EXAMPLE: 192.168.1. or 192..1.25")
    print("")
    print("ERROR_CODE: IP_TOO_MANY_OCTETS_ERROR")
    print("DESCRIPTION: The IP address has too many octets.")
    print("EXAMPLE: 19.2.168.1.25")
    print("")
    print("ERROR_CODE: IP_INVALID_OCTET_ERROR")
    print("DESCRIPTION: The IP address contains an invalid octet.")
    print("EXAMPLE: 192.16i.1.25")
    print("")
    print("ERROR_CODE: IP_OCTET_BOUNDING_ERROR")
    print("DESCRIPTION: The IP address contains an invalid octet.")
    print("EXAMPLE: 192.1680.1.25")
    print("")
    print("ERROR_CODE: PING_TEST_FAILED_ERROR")
    print("DESCRIPTION: Could not ping the copier/printer.")
    print("Please double check network settings on PC and on copier/printer.")
    print("")
    print("ERROR_CODE: LP_NOT_ENABLED_ERROR")
    print("DESCRIPTION: LPR is not enabled.")
    print("Please enable LPR.")
    print("")
    print("ERROR_CODE: IP_MISMATCH_ERROR")
    print("DESCRIPTION: Invalid menu selection at IP Mismatch.")
    print("An Invalid menu option was detected when selecting to continue with the passed IP or the defined IP.")
    print("")
    print("ERROR_CODE: CLI_INVALID_ARGUMENTS_ERROR")
    print("DESCRIPTION: A process error with Command Line Interface (CLI) arguments was detected and could not be "
          "handled.")
    print("Please review arguments and try again. If error persists, please contact with author of the script.")
    print("")

    try:
        raw_input("Press any key to exit...")
    except NameError:
        input("Press any key to exit...")
    exit()


if __name__ == "__main__":

    declared_ip = "0.0.0.0"

    # Removes the file path of script from sys.argv
    index = [i for i, s in enumerate(sys.argv) if "prescribe.py" in s]
    if len(sys.argv) > 0:
        sys.argv.pop(index[0])

    # Logic to handle no arguments (args) passed, or a simple double click run of script
    if len(sys.argv) == 0:
        if declared_ip == "0.0.0.0":
            get_ip("", "")
        else:
            ping_ip(declared_ip, "")

    # Logic to handle one arg passed via CLI call
    elif len(sys.argv) == 1:

        pattern = r"^(?:\d{1,3}\.){3}\d{1,3}$"

        # Checks is passed arg is in IP address format
        if re.match(pattern, sys.argv[0]):

            if (sys.argv[0] == declared_ip) and declared_ip != "0.0.0.0":
                ping_ip(sys.argv[0], "")

            # Checks is passed ip matches declared ip (if applicable)
            elif (sys.argv[0] != declared_ip) and declared_ip != "0.0.0.0":
                print()
                print("Passed IP does not match Defined IP\n")
                print("Enter (Y) to continue with Passed IP: {0}".format(sys.argv[0]))
                print("Enter (N) to continue with Defined IP: {0}\n".format(declared_ip))
                try:
                    choice = raw_input("Your choice (Y/N): ")
                except NameError:
                    choice = input("Your choice (Y/N): ")

                if choice.lower() == "y":
                    ping_ip(sys.argv[0], "")
                elif choice.lower() == "n":
                    ping_ip(declared_ip, "")
                else:
                    error_exit("[IP_MISMATCH_ERROR]")
            elif (sys.argv[0] != declared_ip) and declared_ip == "0.0.0.0":
                ping_ip(sys.argv[0], "")
            else:
                error_exit("[CLI_INVALID_ARGUMENTS_ERROR]")

        elif sys.argv[0] == "--commands":
            print("Command Options:")
            print("[ 0 ] - Display Error Menu List")
            print("[ 98 ] - Delete all Prescribe Command files")
            print("[ 99 ] - Create all Prescribe Command files")
            print("")

            try:
                user_choice = str(input("Enter Menu Choice: "))
            except NameError:
                user_choice = str(input("Enter Menu Choice: "))

            if user_choice == "0":
                error_list()
            elif user_choice == "98" or user_choice == "99":
                prescribe_file_handler(user_choice)
            else:
                error_exit("[CLI_INVALID_ARGUMENTS_ERROR]")

        elif sys.argv[0] == "--preview":
            print("Current Command Options:")
            print("[ 1 ] - Event Log")
            print("[ 2 ] - Turn on 3 Tier Color")
            print("[ 3 ] - Turn off 3 Tier Color")
            print("[ 4 ] - Turn on 60 Lines Mode")
            print("[ 5 ] - Turn on 66 Lines Mode")
            print("[ 6 ] - Turn on Tray Switch")
            print("[ 7 ] - Turn off Tray Switch")
            print("[ 8 ] - Turn on Sleep Timer")
            print("[ 9 ] - Turn off Sleep Timer")
            print("[ 10 ] - Backup FRPO Settings")
            print("[ 11 ] - Initialize FRPO Settings")
            print("")
            print("To See the Error List Enter '0' or run again with arg '--commands print_error_list")
            print("")
            safe_exit("SAFE EXIT - Displayed Current Command Options")

        elif sys.argv[0] == "--help":
            help_options()
        elif sys.argv[0] == "--update":
            update()
        else:
            if declared_ip == "0.0.0.0":
                get_ip("", sys.argv[0])
            elif declared_ip != "0.0.0.0":
                ping_ip(declared_ip, sys.argv[0])

            # Failsafe if args cannot be parsed or processed correctly
            else:
                error_exit("[CLI_INVALID_ARGUMENTS_ERROR]")

    # Logic to handle 2 passed args via CLI call
    elif len(sys.argv) == 2:
        pattern = r"^(?:\d{1,3}\.){3}\d{1,3}$"

        # Checks is first passed arg is in IP address format
        # Assumes [0] is IP and [1] is command
        if re.match(pattern, sys.argv[0]):
            if (sys.argv[0] == declared_ip) and declared_ip != "0.0.0.0":
                ping_ip(sys.argv[0], "")

            # Checks is passed ip matches declared ip (if applicable)
            elif (sys.argv[0] != declared_ip) and declared_ip != "0.0.0.0":
                print()
                print("Passed IP does not match Defined IP\n")
                print("Enter (Y) to continue with Passed IP: {0}".format(sys.argv[0]))
                print("Enter (N) to continue with Defined IP: {0}\n".format(declared_ip))
                try:
                    choice = raw_input("Your choice (Y/N): ")
                except NameError:
                    choice = input("Your choice (Y/N): ")

                if choice.lower() == "y":
                    ping_ip(sys.argv[0], sys.argv[1])
                elif choice.lower() == "n":
                    ping_ip(declared_ip, sys.argv[1])
                else:
                    error_exit("[IP_MISMATCH_ERROR]")
            elif (sys.argv[0] != declared_ip) and declared_ip == "0.0.0.0":
                ping_ip(sys.argv[0], sys.argv[1])

        # Checks is second passed arg is in IP address format
        # Assumes [0] is command and [1] is IP
        elif re.match(pattern, sys.argv[1]):
            if (sys.argv[1] == declared_ip) and declared_ip != "0.0.0.0":
                ping_ip(sys.argv[1], sys.argv[0])

            # Checks is passed ip matches declared ip (if applicable)
            elif (sys.argv[1] != declared_ip) and declared_ip != "0.0.0.0":
                print()
                print("Passed IP does not match Defined IP\n")
                print("Enter (Y) to continue with Passed IP: {0}".format(sys.argv[0]))
                print("Enter (N) to continue with Defined IP: {0}\n".format(declared_ip))
                try:
                    choice = raw_input("Your choice (Y/N): ")
                except NameError:
                    choice = input("Your choice (Y/N): ")

                if choice.lower() == "y":
                    ping_ip(sys.argv[1], sys.argv[0])
                elif choice.lower() == "n":
                    ping_ip(declared_ip, sys.argv[0])
                else:
                    error_exit("[IP_MISMATCH_ERROR]")

            elif (sys.argv[0] != declared_ip) and declared_ip == "0.0.0.0":
                ping_ip(sys.argv[1], sys.argv[0])

            else:
                error_exit("[CLI_INVALID_ARGUMENTS_ERROR]")

        elif sys.argv[0] == "--commands":
            if sys.argv[1] == "print_error_list":
                error_list()
            elif sys.argv[1] == "delete_commands":
                prescribe_file_handler(sys.argv[1])
            elif sys.argv[1] == "create_commands":
                prescribe_file_handler(sys.argv[1])
            else:
                error_exit("[CLI_INVALID_ARGUMENTS_ERROR]")

        # Failsafe if args cannot be parsed or processed correctly
        else:
            error_exit("[CLI_INVALID_ARGUMENTS_ERROR]")

    # Failsafe if args cannot be parsed or processed correctly
    else:
        error_exit("[CLI_INVALID_ARGUMENTS_ERROR]")
