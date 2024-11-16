#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein 
Email: hamdy.aea@protonmail.com
Date of creation:  16-11-2024
Last update: 16-11-2024
Version: 1.0
Description: The dircolors command from GNU coreutils in Python3  
Example of use: python3 dircolors.py -p
'''
import argparse
import os
import sys

DEFAULT_DATABASE = """
# Configuration for LS_COLORS
# This is the default database.
# file types
di=01;34 # directory
ln=01;36 # symbolic link
so=01;35 # socket
pi=40;33 # pipe
ex=01;32 # executable
bd=40;33;01 # block device
cd=40;33;01 # character device
su=37;41 # setuid
sg=30;43 # setgid
tw=30;42 # sticky other writable
ow=34;42 # other writable
"""

def parse_arguments():
    parser = argparse.ArgumentParser(description="Color setup for ls.")
    parser.add_argument("file", nargs="?", help="File to read for LS_COLORS configuration.")
    parser.add_argument(
        "-b", "--sh", "--bourne-shell",
        action="store_true",
        help="Output Bourne shell code to set LS_COLORS."
    )
    parser.add_argument(
        "-c", "--csh", "--c-shell",
        action="store_true",
        help="Output C shell code to set LS_COLORS."
    )
    parser.add_argument(
        "-p", "--print-database",
        action="store_true",
        help="Output default color database."
    )
    parser.add_argument(
        "--print-ls-colors",
        action="store_true",
        help="Output fully escaped colors for display."
    )
    parser.add_argument("--version", action="version", version="dircolors 1.0")
    return parser.parse_args()

def load_database(file):
    """Load the color database from a file."""
    if not os.path.exists(file):
        print(f"dircolors: '{file}' does not exist.", file=sys.stderr)
        sys.exit(1)
    with open(file, "r") as f:
        return f.read()

def generate_ls_colors(database):
    """Parse a color database and generate LS_COLORS."""
    ls_colors = []
    for line in database.splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            key, _, value = line.partition("=")
            if key and value:
                ls_colors.append(f"{key}={value}")
    return ":".join(ls_colors)

def main():
    args = parse_arguments()

    if args.print_database:
        print(DEFAULT_DATABASE.strip())
        return

    database = DEFAULT_DATABASE
    if args.file:
        database = load_database(args.file)

    ls_colors = generate_ls_colors(database)

    if args.sh or args.bourne_shell:
        print(f"LS_COLORS='{ls_colors}'; export LS_COLORS")
    elif args.csh or args.c_shell:
        print(f"setenv LS_COLORS '{ls_colors}'")
    elif args.print_ls_colors:
        print(ls_colors)
    else:
        print("dircolors: No specific option selected. Use --help for usage.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

