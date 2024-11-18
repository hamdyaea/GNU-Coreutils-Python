#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  18-11-2024
Last update: 18-11-2024
Version: 1.0
Description: The link command GNU coreutils in Python3.  
Example of use: python3 link.py file1.txt file2.txt
'''
import argparse
import os
import sys

def create_link(file1, file2):
    """
    Create a hard link from FILE1 to FILE2 using os.link().
    """
    try:
        os.link(file1, file2)
        print(f"Link created: {file2} -> {file1}")
    except FileNotFoundError:
        sys.stderr.write(f"Error: {file1} not found.\n")
    except FileExistsError:
        sys.stderr.write(f"Error: {file2} already exists.\n")
    except OSError as e:
        sys.stderr.write(f"Error: {e.strerror}\n")

def main():
    """
    Main entry point for the link command.
    """
    parser = argparse.ArgumentParser(description="Create a hard link to a file.")
    parser.add_argument("file1", help="The existing file to link to")
    parser.add_argument("file2", help="The name of the link to create")
    parser.add_argument("--version", action="version", version="link.py 1.0", help="Output version information")

    args = parser.parse_args()

    # Create the link
    create_link(args.file1, args.file2)

if __name__ == "__main__":
    main()

