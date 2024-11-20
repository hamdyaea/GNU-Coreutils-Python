#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein 
Email: hamdy.aea@protonmail.com
Date of creation:  20-11-2024
Last update: 20-11-2024
Version: 1.0
Description: The printenv command from GNU coreutils in Python3.  
Example of use:  python3 printenv.py
'''

import os
import sys

def printenv(specific_vars=None):
    """
    Print environment variables
    
    Args:
    specific_vars (list): List of specific environment variables to print
    """
    try:
        # If no specific variables requested, print all
        if not specific_vars:
            for key, value in os.environ.items():
                print(f"{key}={value}")
        else:
            # Print only requested variables
            for var in specific_vars:
                value = os.environ.get(var)
                if value is not None:
                    print(value)
                else:
                    # Variable not found
                    print(f"printenv: {var}: No such environment variable", file=sys.stderr)
                    sys.exit(1)
    
    except Exception as e:
        print(f"printenv error: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    # Parse command-line arguments
    args = sys.argv[1:]
    printenv(args)

if __name__ == "__main__":
    main()
