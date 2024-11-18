#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  18-11-2024
Last update: 18-11-2024
Version: 1.0
Description: The date command from GNU coreutils in Python3.  
Example of use: python3 date.py -R
'''
import argparse
import datetime
import os
import subprocess
import sys
import time
from dateutil import parser as date_parser

VERSION = "1.0"

def parse_date_string(date_string):
    """Parse a human-readable date string into a datetime object."""
    try:
        return date_parser.parse(date_string)
    except Exception as e:
        print(f"Error parsing date string: {e}", file=sys.stderr)
        sys.exit(1)

def format_date(dt, format_string):
    """Format a datetime object according to a given format string."""
    try:
        return dt.strftime(format_string)
    except Exception as e:
        print(f"Error formatting date: {e}", file=sys.stderr)
        sys.exit(1)

def print_date(options):
    """Display the current or specified date."""
    if options.utc:
        now = datetime.datetime.utcnow()
    elif options.date:
        now = parse_date_string(options.date)
    elif options.file:
        try:
            with open(options.file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    dt = parse_date_string(line.strip())
                    print(dt)
                return
        except FileNotFoundError:
            print(f"Error: File '{options.file}' not found", file=sys.stderr)
            sys.exit(1)
    elif options.reference:
        try:
            mtime = os.path.getmtime(options.reference)
            now = datetime.datetime.fromtimestamp(mtime)
        except FileNotFoundError:
            print(f"Error: Reference file '{options.reference}' not found", file=sys.stderr)
            sys.exit(1)
    else:
        now = datetime.datetime.now()

    if options.rfc_2822:
        print(now.strftime("%a, %d %b %Y %H:%M:%S %z"))
    elif options.rfc_3339:
        precision = options.rfc_3339.lower()
        if precision == "date":
            print(now.strftime("%Y-%m-%d"))
        elif precision == "seconds":
            print(now.strftime("%Y-%m-%d %H:%M:%S%z"))
        elif precision == "ns":
            print(now.strftime("%Y-%m-%d %H:%M:%S.%f%z"))
        else:
            print(f"Invalid --rfc-3339 value: {options.rfc_3339}", file=sys.stderr)
            sys.exit(1)
    elif options.format:
        print(format_date(now, options.format))
    else:
        print(now)

def set_date(date_string):
    """Set the system date to the specified date."""
    dt = parse_date_string(date_string)
    timestamp = time.mktime(dt.timetuple())

    try:
        subprocess.run(["sudo", "date", "-s", dt.strftime("%Y-%m-%d %H:%M:%S")], check=True)
        os.system(f"sudo hwclock --systohc")
    except Exception as e:
        print(f"Error setting system date: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Print or set the system date and time.")
    parser.add_argument(
        "format",
        nargs="?",
        help="Output the date in the specified format (e.g., +FORMAT).",
    )
    parser.add_argument(
        "-d", "--date", help="Display the specified date instead of the current date."
    )
    parser.add_argument(
        "-f", "--file", help="Read date strings from a file and display each date."
    )
    parser.add_argument(
        "-r", "--reference", help="Display the last modification time of a file."
    )
    parser.add_argument(
        "-R", "--rfc-2822", action="store_true", help="Output date in RFC 2822 format."
    )
    parser.add_argument(
        "--rfc-3339",
        choices=["date", "seconds", "ns"],
        help="Output date in RFC 3339 format.",
    )
    parser.add_argument(
        "-s", "--set", help="Set the system date to the specified date."
    )
    parser.add_argument(
        "-u", "--utc", action="store_true", help="Use UTC instead of local time."
    )
    parser.add_argument(
        "--version", action="version", version=f"date.py {VERSION}"
    )
    args = parser.parse_args()

    if args.set:
        set_date(args.set)
    else:
        print_date(args)

if __name__ == "__main__":
    main()

