#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  17-11-2024
Last update: 17-11-2024
Version:  1.0
Description:  the logname command from GNU coreutils in Python3. 
Example of use: python3 logname.py
'''
import os
import sys

def print_help():
    print("Usage: logname [OPTION]")
    print("Print the user's login name.")
    print()
    print("Options:")
    print("  --help     display this help and exit")
    print("  --version  output version information and exit")

def print_version():
    print("logname 1.0 (Python)")

def get_login_name():
    # Obtient le nom d'utilisateur du login en cours
    return os.getenv("LOGNAME") or os.getenv("USER") or os.getenv("USERNAME")

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            print_help()
            sys.exit(0)
        elif sys.argv[1] == "--version":
            print_version()
            sys.exit(0)
        else:
            print(f"Unknown option: {sys.argv[1]}")
            sys.exit(1)
    
    # Afficher le nom d'utilisateur
    login_name = get_login_name()
    if login_name:
        print(login_name)
    else:
        print("No login name found.")
        sys.exit(1)

if __name__ == "__main__":
    main()

