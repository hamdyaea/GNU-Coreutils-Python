#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  17-11-2024
Last update: 17-11-2024
Version: 1.0
Description: The nice command from GNU coreutils in Python3.  
Example of use: python3 nice.py
'''

import os
import sys
import subprocess
import argparse

def get_niceness():
    """Return the current niceness of the process."""
    try:
        with open('/proc/self/stat', 'r') as f:
            fields = f.read().split()
            return int(fields[17])  # Niceness is at position 18 (index 17)
    except Exception as e:
        print(f"Error getting niceness: {e}")
        sys.exit(125)

def set_niceness(niceness):
    """Set the niceness of the current process."""
    try:
        os.setpriority(os.PRIO_PROCESS, 0, niceness)
    except PermissionError:
        print("Error: You must have the appropriate privileges to set niceness.")
        sys.exit(126)
    except Exception as e:
        print(f"Error setting niceness: {e}")
        sys.exit(125)

def execute_command(command, args, niceness):
    """Execute the command with the specified niceness."""
    try:
        set_niceness(niceness)
        subprocess.run([command] + args)
    except FileNotFoundError:
        print(f"Command '{command}' not found.")
        sys.exit(127)
    except Exception as e:
        print(f"Error executing command: {e}")
        sys.exit(125)

def main():
    parser = argparse.ArgumentParser(description="Run a program with modified scheduling priority.")

    parser.add_argument('-n', '--adjustment', type=int, default=10, help="Add integer N to the niceness (default 10).")
    parser.add_argument('command', nargs='?', type=str, help="The command to run with adjusted niceness.")
    parser.add_argument('args', nargs=argparse.REMAINDER, help="Arguments for the command.")

    parser.add_argument('--version', action='version', version="nice.py 1.0", help="Output version information and exit.")

    args = parser.parse_args()

    # If no command is provided, print the current niceness
    if args.command is None:
        niceness = get_niceness()
        print(f"Current niceness: {niceness}")
    else:
        # Execute the command with the specified niceness adjustment
        niceness = get_niceness() + args.adjustment
        execute_command(args.command, args.args, niceness)

if __name__ == "__main__":
    main()

