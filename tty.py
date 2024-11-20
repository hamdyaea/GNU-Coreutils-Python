#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  20-11-2024
Last update: 20-11-2024
Version: 1.0
Description: The tty command from GNU coreutils in Python3.  
Example of use: python3 tty.py
'''

import os
import sys

def main():
    """
    Simulate the GNU coreutils tty command.
    Prints the file name of the terminal connected to standard input.
    """
    try:
        # Try to get the terminal device name
        tty_name = os.ttyname(sys.stdin.fileno())
        print(tty_name)
        sys.exit(0)
    except OSError:
        # If not connected to a terminal
        print("not a tty", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
