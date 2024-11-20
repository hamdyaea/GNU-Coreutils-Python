#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  20-11-2024
Last update: 20-11-2024
Version: 1.0
Description: The stty command from GNU coreutils in Python3.  
Example of use: python3 stty.py
'''

import sys
import termios
import tty
import fcntl
import os

class STTYCommand:
    def __init__(self, fd=sys.stdin.fileno()):
        self.fd = fd

    def get_terminal_attributes(self):
        """Get current terminal attributes"""
        try:
            attrs = termios.tcgetattr(self.fd)
            return attrs
        except termios.error as e:
            print(f"Error getting terminal attributes: {e}", file=sys.stderr)
            return None

    def display_speed(self):
        """Display input and output baud rates"""
        try:
            ispeed = termios.tcgetattr(self.fd)[2]
            ospeed = termios.tcgetattr(self.fd)[3]
            print(f"Input speed: {ispeed}")
            print(f"Output speed: {ospeed}")
        except termios.error as e:
            print(f"Error getting speed: {e}", file=sys.stderr)

    def display_line_settings(self):
        """Display basic line settings"""
        try:
            attrs = self.get_terminal_attributes()
            if attrs:
                print(f"Control modes: {attrs[2]}")
                print(f"Local modes: {attrs[3]}")
                print(f"Input modes: {attrs[0]}")
                print(f"Output modes: {attrs[1]}")
        except Exception as e:
            print(f"Error displaying settings: {e}", file=sys.stderr)

    def run(self, args):
        """Main method to handle different stty operations"""
        if len(args) == 0:
            # Default: display current settings
            self.display_line_settings()
            self.display_speed()
        elif args[0] == 'speed':
            self.display_speed()
        else:
            print(f"Unsupported operation: {' '.join(args)}", file=sys.stderr)
            sys.exit(1)

def main():
    stty = STTYCommand()
    stty.run(sys.argv[1:])

if __name__ == "__main__":
    main()
