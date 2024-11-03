#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  3-11-2024
Last update: 3-11-2024
Version: 1.0
Description: The mkdir command from coreutils in Python3.  
Example of use: python3 mkdir.py -v nouveau_dossier
'''
import os
import sys
import argparse
import stat

def create_directory(path, mode, verbose):
    """Create a directory with specified mode and verbosity."""
    try:
        os.makedirs(path, exist_ok=True)
        if mode is not None:
            # Apply the specified mode
            os.chmod(path, mode)
        if verbose:
            print(f"Directory created: '{path}'")
    except Exception as e:
        print(f"mkdir: '{path}': {e}")

def main():
    parser = argparse.ArgumentParser(description="Make directories.")
    parser.add_argument('directories', nargs='+', help='Directories to create')
    parser.add_argument('-m', '--mode', type=str, help='Set file mode (as in chmod), not a=rwx - umask')
    parser.add_argument('-p', '--parents', action='store_true', help='No error if existing, make parent directories as needed')
    parser.add_argument('-v', '--verbose', action='store_true', help='Print a message for each created directory')
    
    args = parser.parse_args()

    # Parse mode argument if provided
    mode = None
    if args.mode:
        try:
            mode = int(args.mode, 8)  # Convert octal string to integer
        except ValueError:
            print(f"mkdir: invalid mode: '{args.mode}'")
            sys.exit(1)

    for directory in args.directories:
        if args.parents:
            create_directory(directory, mode, args.verbose)
        else:
            # Only create the directory if it does not already exist
            try:
                os.mkdir(directory)
                if mode is not None:
                    os.chmod(directory, mode)
                if args.verbose:
                    print(f"Directory created: '{directory}'")
            except FileExistsError:
                if args.verbose:
                    print(f"Directory already exists: '{directory}'")
            except Exception as e:
                print(f"mkdir: '{directory}': {e}")

if __name__ == "__main__":
    main()

