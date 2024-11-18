#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email:  hamdy.aea@protonmail.com
Date of creation:  18-11-2024
Last update: 18-11-2024
Version: 1.2
Description: The users command from GNU coreutils in Python3.  
Example of use: python3 users.py
'''
import os
import sys
import argparse
import struct

VERSION = "1.2"
DEFAULT_UTMP_FILE = "/var/run/utmp"

# Constants for common UTMP structures
UTMP_STRUCT_FORMAT = "hi32s4s32s256s"  # Adjust this format as needed
UTMP_ENTRY_SIZE = struct.calcsize(UTMP_STRUCT_FORMAT)
USER_PROCESS = 7  # Code for USER_PROCESS in UTMP


def read_utmp(file):
    """
    Reads the UTMP file and extracts logged-in users.
    """
    users = []

    try:
        with open(file, "rb") as f:
            while chunk := f.read(UTMP_ENTRY_SIZE):
                if len(chunk) < UTMP_ENTRY_SIZE:
                    # Skip incomplete entries
                    break

                # Unpack UTMP structure
                try:
                    ut_type, _, username, _, _, _ = struct.unpack(UTMP_STRUCT_FORMAT, chunk)
                except struct.error as e:
                    print(f"Error unpacking UTMP record: {e}", file=sys.stderr)
                    sys.exit(1)

                # Process logged-in user processes
                if ut_type == USER_PROCESS:
                    # Decode username and clean null characters
                    username = username.decode("utf-8", "ignore").strip("\x00")
                    if username:
                        users.append(username)
    except FileNotFoundError:
        print(f"Error: File '{file}' not found.", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied for file '{file}'.", file=sys.stderr)
        sys.exit(1)

    return users


def main():
    """
    Main entry point for the script.
    """
    parser = argparse.ArgumentParser(
        description="Print the user names of users currently logged in."
    )
    parser.add_argument(
        "file",
        nargs="?",
        default=DEFAULT_UTMP_FILE,
        help=f"File to read user session information from (default: {DEFAULT_UTMP_FILE}).",
    )
    parser.add_argument(
        "--version", action="version", version=f"users.py {VERSION}",
        help="Output version information and exit.",
    )

    args = parser.parse_args()

    # Read users from the specified UTMP file
    users = read_utmp(args.file)

    if users:
        print(" ".join(users))
    else:
        print("No users logged in.")


if __name__ == "__main__":
    main()

