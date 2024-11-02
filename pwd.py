#!/usr/bin/env python3

# Developer: Mehdi Marhol
# Contact: kbmehdi69@gmail.com

# This software is a basic copy of the famous pwd command in Linux coreutils.

import os
import sys

VERSION = "1.0"
AUTHOR = "Mehdi Marhol"

def print_logical_path():
    """
    Prints the logical path of the current directory from the PWD environment variable.
    """
    logical_path = os.environ.get("PWD", os.getcwd())
    print(logical_path)

def print_physical_path():
    """
    Prints the physical path of the current directory, resolving symbolic links.
    """
    print(os.path.realpath(os.getcwd()))

def show_help():
    """
    Display help information about the command options.
    """
    print("Usage: python pwd.py [OPTION]...")
    print("Print the full filename of the current working directory.\n")
    print("  -L, --logical     use PWD from environment, even if it contains symlinks")
    print("  -P, --physical    avoid all symlinks")
    print("      --help        display this help and exit")
    print("      --version     output version information and exit\n")
    print("If no option is specified, -P is assumed.\n")


def show_version():
    """
    version and author information
    """
    print(f"pwd.py version {VERSION}")
    print(AUTHOR)

if __name__ == "__main__":
    # Default to physical path if no options specified
    option = "-P" if len(sys.argv) == 1 else sys.argv[1]

    # Process options
    if option in ("-L", "--logical"):
        print_logical_path()
    elif option in ("-P", "--physical"):
        print_physical_path()
    elif option == "--help":
        show_help()
    elif option == "--version":
        show_version()
    else:
        print(f"Invalid option: {option}\n")
        show_help()
