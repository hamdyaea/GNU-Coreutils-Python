#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  3-11-2024
Last update: 3-11-2024
Version: 1.0
Description: The rm command from coreutils in Python3.  
Example of use: python3 rm.py fichier.txt
'''
import os
import sys
import argparse

def remove_file(filepath, force, interactive, verbose):
    """Remove a single file with options for interaction and verbosity."""
    if not os.path.exists(filepath):
        if verbose:
            print(f"rm: '{filepath}': No such file or directory")
        return

    if not os.access(filepath, os.W_OK) and not force:
        if interactive:
            response = input(f"rm: remove write-protected regular file '{filepath}'? (y/n) ")
            if response.lower() != 'y':
                print(f"Skipping '{filepath}'")
                return
        elif not force:
            print(f"rm: '{filepath}': Permission denied")
            return

    os.remove(filepath)
    if verbose:
        print(f"Removed '{filepath}'")

def remove_directory(dirpath, force, interactive, verbose):
    """Recursively remove a directory."""
    if not os.path.exists(dirpath):
        if verbose:
            print(f"rm: '{dirpath}': No such file or directory")
        return
    
    if not os.path.isdir(dirpath):
        remove_file(dirpath, force, interactive, verbose)
        return

    if interactive:
        response = input(f"rm: remove directory '{dirpath}'? (y/n) ")
        if response.lower() != 'y':
            print(f"Skipping directory '{dirpath}'")
            return

    for root, dirs, files in os.walk(dirpath, topdown=False):
        for name in files:
            remove_file(os.path.join(root, name), force, interactive, verbose)
        for name in dirs:
            os.rmdir(os.path.join(root, name))

    os.rmdir(dirpath)
    if verbose:
        print(f"Removed directory '{dirpath}'")

def main():
    parser = argparse.ArgumentParser(description="Remove (unlink) the FILE(s).")
    parser.add_argument('files', nargs='+', help='Files to remove')
    parser.add_argument('-f', '--force', action='store_true', help='ignore nonexistent files and arguments, never prompt')
    parser.add_argument('-i', action='store_true', help='prompt before every removal')
    parser.add_argument('-I', action='store_true', help='prompt once before removing more than three files, or when removing recursively')
    parser.add_argument('-r', '-R', '--recursive', action='store_true', help='remove directories and their contents recursively')
    parser.add_argument('-d', '--dir', action='store_true', help='remove empty directories')
    parser.add_argument('-v', '--verbose', action='store_true', help='explain what is being done')
    
    args = parser.parse_args()

    if args.I and len(args.files) > 3:
        response = input(f"rm: remove {len(args.files)} files? (y/n) ")
        if response.lower() != 'y':
            print("Aborting operation.")
            sys.exit(0)

    for file in args.files:
        if args.recursive or os.path.isdir(file):
            remove_directory(file, args.force, args.i or args.I, args.verbose)
        else:
            remove_file(file, args.force, args.i, args.verbose)

if __name__ == "__main__":
    main()

