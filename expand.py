#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  16-11-2024
Last update: 16-11-2024
Version: 1.0
Description: The expand command from GNU coreutils in Python3  
Example of use: python3 expand.py file.txt
'''
import argparse
import sys
from typing import List, Optional

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Convert tabs to spaces in each FILE, writing to standard output."
    )
    parser.add_argument(
        "-i", "--initial",
        action="store_true",
        help="Do not convert tabs after non-blanks."
    )
    parser.add_argument(
        "-t", "--tabs",
        type=str,
        default="8",
        help=(
            "Specify tab positions as a single number (tab width) or "
            "a comma-separated list of tab stops. Defaults to 8."
        )
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="Files to process. Use '-' or omit to read from standard input."
    )
    parser.add_argument("--version", action="version", version="expand 1.0")
    return parser.parse_args()

def parse_tab_stops(tabs: str) -> List[int]:
    """Parse the tab positions from the `-t` or `--tabs` argument."""
    if "," in tabs:
        # List of tab positions
        stops = []
        for part in tabs.split(","):
            if part.startswith("/"):
                stops.append(int(part[1:]))
            elif part.startswith("+"):
                stops.append(int(part[1:]))
            else:
                stops.append(int(part))
        return stops
    else:
        # Single tab width
        return [int(tabs)]

def expand_line(line: str, tab_stops: List[int], initial_only: bool) -> str:
    """Expand tabs to spaces in a single line."""
    result = []
    position = 0
    stop_index = 0

    for char in line:
        if char == "\t":
            if initial_only and "".join(result).lstrip():
                result.append("\t")
            else:
                if stop_index < len(tab_stops):
                    next_stop = tab_stops[stop_index]
                    spaces = next_stop - position % next_stop
                    position += spaces
                    result.append(" " * spaces)
                    stop_index += 1
                else:
                    result.append(" " * (8 - position % 8))  # Default tab width
                    position += 8 - position % 8
        else:
            result.append(char)
            position += 1

    return "".join(result)

def process_file(file: Optional[str], tab_stops: List[int], initial_only: bool):
    """Process a single file or standard input."""
    if file == "-" or not file:
        input_stream = sys.stdin
    else:
        input_stream = open(file, "r")

    try:
        for line in input_stream:
            print(expand_line(line.rstrip("\n"), tab_stops, initial_only))
    finally:
        if input_stream is not sys.stdin:
            input_stream.close()

def main():
    args = parse_arguments()

    # Parse tab stops
    tab_stops = parse_tab_stops(args.tabs)

    # Process each file
    if not args.files or args.files == ["-"]:
        process_file("-", tab_stops, args.initial)
    else:
        for file in args.files:
            process_file(file, tab_stops, args.initial)

if __name__ == "__main__":
    main()

