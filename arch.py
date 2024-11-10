#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com 
Date of creation:  10-11-2024
Last update: 10-11-2024
Version: 1.0
Description: The arch command from GNU coreutils in Python3  
Example of use:  python3 arch.py
'''
import platform
import sys

def print_help():
    help_text = """
    Usage: arch [OPTION]...
    Print machine architecture.

    Options:
      --help     display this help and exit
      --version  output version information and exit
    """
    print(help_text)

def print_version():
    version_text = "arch 1.0"
    print(version_text)

def main():
    if len(sys.argv) > 1:
        option = sys.argv[1]
        if option == '--help':
            print_help()
        elif option == '--version':
            print_version()
        else:
            print("Invalid option. Use --help for usage information.")
    else:
        print(platform.machine())

if __name__ == "__main__":
    main()

