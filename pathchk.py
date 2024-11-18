#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein 
Email: hamdy.aea@protonmail.com
Date of creation:  18-11-2024
Last update: 18-11-2024
Version: 1.0
Description: The pathchk command from GNU coreutils in Python3.  
Example of use: python3 pathchk.py -p file1.txt file2.txt
'''
import argparse
import os
import sys
import re

def is_valid_name(name, check_posix, check_empty_and_leading_dash):
    """
    Check if a file name is valid based on POSIX standards and system-specific rules.
    """
    # Check if the name is empty
    if not name:
        return False
    
    # Check for leading dash for POSIX systems (unless --portability is set)
    if check_empty_and_leading_dash and name.startswith("-"):
        return False

    # Check for most POSIX systems file name validity
    if check_posix:
        # POSIX file name validation: cannot contain slashes, null characters or other illegal chars
        if "/" in name:
            return False
        if re.search(r'[<>:"/\|?*]', name):  # Checking for characters not allowed in filenames
            return False

    return True

def check_names(names, check_posix, check_empty_and_leading_dash):
    """
    Check each name in the list and report whether it is valid or not.
    """
    for name in names:
        if is_valid_name(name, check_posix, check_empty_and_leading_dash):
            print(f"{name}: valid")
        else:
            print(f"{name}: invalid")

def main():
    """
    Main entry point for the pathchk command.
    """
    parser = argparse.ArgumentParser(description="Check whether file names are valid or portable.")
    parser.add_argument("names", nargs="+", help="File names to check")
    parser.add_argument("-p", action="store_true", help="Check for most POSIX systems")
    parser.add_argument("-P", action="store_true", help="Check for empty names and leading '-'")
    parser.add_argument("--portability", action="store_true", help="Check for all POSIX systems (equivalent to -p -P)")
    parser.add_argument("--version", action="version", version="pathchk.py 1.0", help="Output version information")

    args = parser.parse_args()

    # Check names based on the provided arguments
    check_names(args.names, args.p or args.portability, args.P or args.portability)

if __name__ == "__main__":
    main()

