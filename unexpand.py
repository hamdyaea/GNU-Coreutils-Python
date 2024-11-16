#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein 
Email:  hamdy.aea@protonmail.com
Date of creation:  16-11-2024
Last update: 16-11-2024
Version: 1.0
Description: The unexpand command from GNU coreutils in Python3  
Example of use: python3 unexpand.py file.txt
'''

import sys
import argparse


def unexpand_line(line, tab_width, all_blanks, only_leading):
    """Convert spaces in the given line to tabs based on options."""
    if not all_blanks and not only_leading:
        return line  # Default behavior: no conversion unless specified.

    converted = []
    space_count = 0
    leading_space = True

    for char in line:
        if char == ' ' and (leading_space or all_blanks):
            space_count += 1
            if space_count == tab_width:
                converted.append('\t')
                space_count = 0
        else:
            if space_count > 0:
                converted.append(' ' * space_count)
                space_count = 0
            converted.append(char)
            if char != ' ':
                leading_space = False

    if space_count > 0:
        converted.append(' ' * space_count)

    return ''.join(converted)


def process_file(file, tab_width, all_blanks, only_leading):
    """Process a single file or standard input."""
    with (sys.stdin if file == '-' else open(file, 'r')) as f:
        for line in f:
            print(unexpand_line(line.rstrip('\n'), tab_width, all_blanks, only_leading))


def main():
    parser = argparse.ArgumentParser(
        description="Convert spaces to tabs, mimicking the GNU unexpand command."
    )
    parser.add_argument(
        "-a", "--all", action="store_true", help="Convert all blanks instead of just leading blanks."
    )
    parser.add_argument(
        "--first-only",
        action="store_true",
        help="Convert only leading sequences of blanks (overrides -a).",
    )
    parser.add_argument(
        "-t", "--tabs",
        type=str,
        default="8",
        help="Specify tab stops. Default is 8. Can be a single number or a list of comma-separated positions.",
    )
    parser.add_argument(
        "files", nargs="*", default=["-"], help="Files to process. Use '-' for standard input."
    )
    parser.add_argument(
        "--version", action="version", version="unexpand.py 1.0", help="Show version and exit."
    )

    args = parser.parse_args()

    # Determine tab width or positions
    try:
        tab_width = int(args.tabs) if args.tabs.isdigit() else 8
    except ValueError:
        print("Error: Invalid tab width specified.", file=sys.stderr)
        sys.exit(1)

    # Process each file
    for file in args.files:
        process_file(file, tab_width, args.all, args.first_only)


if __name__ == "__main__":
    main()

