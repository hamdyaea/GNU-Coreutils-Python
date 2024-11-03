#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  3-11-2024
Last update: 3-11-2024
Version: 1.0
Description: rmdir from coreutils in Python3  
Example of use: python3 rmdir.py empty_dir
'''
import os
import shutil
import errno
import argparse

def remove_directory(path, ignore_non_empty, force, verbose):
    """Remove a directory, handling verbosity, non-empty cases, and force deletion."""
    try:
        if force:
            shutil.rmtree(path)
            if verbose:
                print(f"Forcibly removed directory: '{path}'")
        else:
            os.rmdir(path)
            if verbose:
                print(f"Removed directory: '{path}'")
    except OSError as e:
        if e.errno == errno.ENOTEMPTY:
            if ignore_non_empty:
                if verbose:
                    print(f"Skipped non-empty directory: '{path}'")
            elif not force:
                print(f"rmdir: '{path}': Directory not empty")
        else:
            print(f"rmdir: '{path}': {e}")

def main():
    parser = argparse.ArgumentParser(description="Remove empty directories.")
    parser.add_argument('directories', nargs='+', help='Directories to remove')
    parser.add_argument('-f', '--force', action='store_true', help='Force removal of non-empty directories')
    parser.add_argument('--ignore-fail-on-non-empty', action='store_true', help='Ignore failure to remove a non-empty directory')
    parser.add_argument('-p', '--parents', action='store_true', help='Remove DIRECTORY and its ancestors')
    parser.add_argument('-v', '--verbose', action='store_true', help='Output a diagnostic for every directory processed')
    
    args = parser.parse_args()

    for directory in args.directories:
        if args.parents:
            # Traverse up the directory path, removing ancestors as possible
            path_parts = directory.split(os.sep)
            for i in range(len(path_parts), 0, -1):
                path = os.sep.join(path_parts[:i])
                if path:  # Skip if path is empty
                    remove_directory(path, args.ignore_fail_on_non_empty, args.force, args.verbose)
        else:
            # Remove only the specified directory
            remove_directory(directory, args.ignore_fail_on_non_empty, args.force, args.verbose)

if __name__ == "__main__":
    main()

