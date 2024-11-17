#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein 
Email: hamdy.aea@protonmail.com
Date of creation:  17-11-2024
Last update: 17-11-2024
Version: 1.0
Description: The nohup command from GNU coreutils in Python3.  
Example of use: python3 nohup.py python3 myscript.py
'''

import os
import sys
import signal
import subprocess
import argparse

def run_nohup(command, output_file='nohup.out'):
    """Run a command immune to hangups, redirect output to a file."""
    # Ignore hangup signal
    signal.signal(signal.SIGHUP, signal.SIG_IGN)

    # Open the output file
    with open(output_file, 'a') as out_file:
        # Run the command with its arguments
        try:
            process = subprocess.Popen(command, stdout=out_file, stderr=subprocess.STDOUT)
            process.communicate()  # Wait for the process to complete
            return process.returncode
        except FileNotFoundError:
            sys.stderr.write(f"Command '{command[0]}' not found.\n")
            return 127
        except PermissionError:
            sys.stderr.write(f"Permission denied to execute '{command[0]}'.\n")
            return 126
        except Exception as e:
            sys.stderr.write(f"Error: {str(e)}\n")
            return 125

def main():
    parser = argparse.ArgumentParser(description="Run a command immune to hangups, with output to a non-tty.")
    
    # Define arguments
    parser.add_argument('command', nargs='+', help="Command and its arguments to run.")
    parser.add_argument('-o', '--output', default='nohup.out', help="Output file (default: nohup.out)")

    # Version and help
    parser.add_argument('--version', action='version', version="nohup.py 1.0", help="output version information and exit")

    # Parse arguments
    args = parser.parse_args()

    # Run the command with nohup
    exit_code = run_nohup(args.command, args.output)

    # Exit with the return code of the command
    sys.exit(exit_code)

if __name__ == "__main__":
    main()

