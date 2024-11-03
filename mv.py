#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  3-11-2024
Last update: 3-11-2024
Version: 1.0
Description: A clone of the mv command from coreutils in Python3.  
Example of use: python3 mv.py file.txt backup/
'''

import os
import shutil
import argparse

VERSION = "1.0.0"

def main():
    parser = argparse.ArgumentParser(description="Move or rename files and directories.")
    
    parser.add_argument("source", nargs="?", help="Source file or directory")
    parser.add_argument("dest", nargs="?", help="Destination file or directory")
    
    parser.add_argument("-f", "--force", action="store_true", help="do not prompt before overwriting")
    parser.add_argument("-v", "--verbose", action="store_true", help="explain what is being done")
    parser.add_argument("-t", "--target-directory", help="move all SOURCE arguments into DIRECTORY")
    parser.add_argument("-T", "--no-target-directory", action="store_true", help="treat DEST as a normal file")
    parser.add_argument("--backup", nargs="?", const="~", help="make a backup of each existing destination file")
    parser.add_argument("-S", "--suffix", default="~", help="override the usual backup suffix")
    parser.add_argument("--strip-trailing-slashes", action="store_true", help="remove any trailing slashes from each SOURCE argument")
    parser.add_argument("--update", choices=["all", "none", "none-fail", "older"], default="older", help="control which existing files are updated")
    parser.add_argument("--version", action="version", version=f"mv.py version {VERSION}", help="output version information and exit")

    # Parse arguments
    args = parser.parse_args()

    # If --version or --help is invoked, exit here as argparse handles it
    if args.source is None or args.dest is None:
        if not (args.version or args.help):
            parser.error("the following arguments are required: source, dest")

    move(args)


def move(args):
    # Handling options
    source = args.source.rstrip("/") if args.strip_trailing_slashes else args.source
    dest = args.dest

    # Check if destination exists and handle overwrite conditions
    if os.path.exists(dest):
        if args.force:
            if args.verbose:
                print(f"Overwriting {dest}")
            shutil.move(source, dest)
        elif args.backup:
            backup_name = dest + (args.backup if args.backup else args.suffix)
            os.rename(dest, backup_name)
            if args.verbose:
                print(f"Backup created: {backup_name}")
            shutil.move(source, dest)
        else:
            print(f"mv: '{dest}' already exists. Use -f to force overwrite.")
    else:
        shutil.move(source, dest)
        if args.verbose:
            print(f"Moved '{source}' to '{dest}'")

if __name__ == "__main__":
    main()

